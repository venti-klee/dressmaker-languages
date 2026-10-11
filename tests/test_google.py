import json
from pathlib import Path
import sys
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

BUNDLE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BUNDLE / 'assistant'))
from core import Store
from providers import GoogleWeb, GOOGLE_PAGE_ERROR


class GoogleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'data'
        self.store = Store(self.root, BUNDLE)
        self.store.save_config({'game': str(Path(self.temp.name) / 'game'), 'provider': 'google',
                                'online': True, 'offline_model': False})

    def tearDown(self):
        self.store.db.close()
        self.temp.cleanup()

    def test_segments_source_validation_and_encoded_request(self):
        adapter = GoogleWeb()
        reply = json.dumps([[['月光', 'Moonlit ', None], ['锦缎', 'brocade', None]]])
        with patch.object(adapter, 'read', return_value=reply) as read:
            self.assertEqual(adapter.translate('Moonlit brocade', 'zh-CN'), '月光锦缎')
            url = read.call_args.args[0].full_url
            self.assertIn('tl=zh-CN', url)
            self.assertIn('q=Moonlit+brocade', url)

    def test_challenges_errors_and_partial_replies_are_rejected(self):
        for reply in ['<html>captcha</html>', '{}', '[]', '[[]]',
                      '[[["译文", "different source"]]]', '[[[null,"Moonlit brocade"]]]']:
            with patch.object(self.store.google, 'read', return_value=reply):
                with self.assertRaisesRegex(ValueError, GOOGLE_PAGE_ERROR):
                    self.store.google.translate('Moonlit brocade', 'zh-CN')

    def test_boundary_spaces_are_preserved_without_rejecting_trimmed_source_echo(self):
        adapter = GoogleWeb()
        source = '  Moonlit brocade \t'
        reply = json.dumps([[['月光锦缎', 'Moonlit brocade']]])
        with patch.object(adapter, 'read', return_value=reply) as read:
            self.assertEqual(adapter.translate(source, 'zh-CN'), '  月光锦缎 \t')
            import urllib.parse
            query = urllib.parse.parse_qs(urllib.parse.urlparse(read.call_args.args[0].full_url).query)
            self.assertEqual(query['q'], ['Moonlit brocade'])

    def test_boundary_normalization_still_rejects_partial_and_changed_body(self):
        adapter = GoogleWeb()
        for echo in ['Moonlit', 'Moonlit  brocade', 'different source']:
            with patch.object(adapter, 'read', return_value=json.dumps([[['译文', echo]]])):
                with self.assertRaisesRegex(ValueError, GOOGLE_PAGE_ERROR):
                    adapter.translate(' Moonlit brocade ', 'zh-CN')

    def test_cached_translation_survives_reopen_offline_and_language_switch(self):
        with patch.object(self.store.google, 'translate', return_value='月光锦缎'):
            self.assertEqual(self.store.translate('Moonlit brocade'), ('月光锦缎', 'google'))
        self.store.db.close()
        self.store = Store(self.root, BUNDLE)
        self.store.save_config({'online': False, 'language': 'ja'})
        self.assertIsNone(self.store.cache_get('Moonlit brocade', 'ja'))
        self.store.save_config({'language': 'zh-CN'})
        with patch.object(self.store.google, 'translate', side_effect=AssertionError('offline network')):
            self.assertEqual(self.store.translate('Moonlit brocade'), ('月光锦缎', 'google'))

    def test_format_damage_is_not_cached_or_sent_to_fallback(self):
        self.store.save_config({'fallback': True})
        with patch.object(self.store.google, 'translate', return_value='缺少变量'), \
                patch('core.request_json', side_effect=AssertionError('unsafe fallback')):
            with self.assertRaises(ValueError):
                self.store.translate('Moonlit brocade {0}')
        self.assertIsNone(self.store.cache_get('Moonlit brocade {0}', 'zh-CN'))

    def test_optional_fallback_and_both_attempts_count_toward_budget(self):
        self.store.save_config({'fallback': True})
        reply = {'responseStatus': 200, 'responseData': {'translatedText': '月光锦缎'}}
        with patch.object(self.store.google, 'translate', side_effect=ValueError(GOOGLE_PAGE_ERROR)), \
                patch('core.request_json', return_value=reply), patch('core.time.sleep'):
            self.assertEqual(self.store.translate('Moonlit brocade'), ('月光锦缎', 'mymemory'))
        self.assertEqual(self.store.status()['budget']['used'], 2 * len('Moonlit brocade'))

    def test_budget_visible_and_increasing_it_preserves_spending_and_cache(self):
        source = 'Moonlit brocade'
        self.store.save_config({'daily_bytes': len(source)})
        with patch.object(self.store.google, 'translate', return_value='月光锦缎'):
            self.store.translate(source)
        self.assertEqual(self.store.status()['budget']['remaining'], 0)
        with patch.object(self.store.google, 'translate', side_effect=AssertionError('budget exceeded')):
            with self.assertRaises(ValueError):
                self.store.translate('Starlight lace')
        self.store.save_config({'daily_bytes': 20000})
        budget = self.store.status()['budget']
        self.assertEqual((budget['used'], budget['remaining']), (len(source), 20000 - len(source)))
        self.assertEqual(self.store.cache_get(source, 'zh-CN')[0], '月光锦缎')

    def test_paths_urls_and_email_are_masked_before_leaving_the_computer(self):
        source = 'Folder: /Users/example/My Game/file.json'
        def translate(masked, language):
            self.assertNotIn('/Users/', masked)
            self.assertNotIn('example', masked)
            return masked.replace('Folder:', '文件夹：')
        with patch.object(self.store.google, 'translate', side_effect=translate):
            self.assertEqual(self.store.translate(source)[0], '文件夹： /Users/example/My Game/file.json')
        for source in ['https://example.com/private?id=secret', 'person@example.com', r'C:\Users\example\My Game\save.json']:
            with patch.object(self.store.google, 'translate', side_effect=AssertionError('private value should stay local')):
                self.assertEqual(self.store.translate(source), (source, 'untranslated'))

    def test_measurements_stay_original_and_replace_bad_machine_cache(self):
        self.store.db.execute("INSERT INTO translations VALUES (?,?,?,?,?)", ('512 MiB', 'zh-CN', '第512章', 'google', 'test'))
        self.store.db.commit()
        with patch.object(self.store.google, 'translate', side_effect=AssertionError('measurement request')):
            self.assertEqual(self.store.translate('512 MiB'), ('512 MiB', 'untranslated'))
            self.assertEqual(self.store.translate('Automatic-save-20261011-120431-4c03c9.zip')[0], 'Automatic-save-20261011-120431-4c03c9.zip')
            self.assertEqual(self.store.translate('2026-10-11 12:04 · 1050 KB')[0], '2026-10-11 12:04 · 1050 KB')
        self.assertEqual(self.store.cache_get('512 MiB', 'zh-CN'), ('512 MiB', 'original'))


if __name__ == '__main__':
    unittest.main()
