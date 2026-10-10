import json
from pathlib import Path
import sys
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

BUNDLE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BUNDLE / 'assistant'))
from core import Store, protect
from providers import BingWeb, BING_PAGE_ERROR, SERVICE_ERROR

PAGE = 'IG:"ABCDE123"; <div data-iid="translator.5023"> var params_AbusePreventionHelper = [123,"public-session-token",3600000];'

class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name), BUNDLE)
        self.store.save_config({'game':str(Path(self.temp.name)/'game'), 'provider':'bing', 'online':True, 'offline_model':False})

    def tearDown(self):
        self.store.db.close()
        self.temp.cleanup()

    def test_bing_session_and_mapping_and_reuse(self):
        adapter = BingWeb()
        good = json.dumps([{'translations':[{'to':'zh-Hans','text':'月光锦缎'}]}])
        with patch.object(adapter, 'read', side_effect=[PAGE,good,good]) as read:
            self.assertEqual(adapter.translate('Moonlit brocade','zh-CN'),'月光锦缎')
            self.assertEqual(adapter.translate('Moonlit brocade','zh-CN'),'月光锦缎')
            self.assertEqual(read.call_count,3)
            request = read.call_args_list[1].args[0]
            self.assertIn(b'to=zh-Hans', request.data)
            self.assertIn('www.bing.com/ttranslatev3?', request.full_url)

    def test_changed_page_or_challenge_never_executed(self):
        for page in ['<html>Verify you are human</html>', PAGE.replace('3600000','"bad"'), PAGE.replace('"public-session-token"','null')]:
            with self.assertRaisesRegex(ValueError,BING_PAGE_ERROR):
                BingWeb.parse_session(page)

    def test_bing_error_responses_rejected(self):
        for reply in ['<html>captcha</html>','{"statusCode":429}', '[]', '[{"translations":[{"to":"fr","text":"wrong language"}]}]']:
            adapter = BingWeb()
            with patch.object(adapter, 'read', side_effect=[PAGE,reply]):
                with self.assertRaisesRegex(ValueError,SERVICE_ERROR):
                    adapter.translate('Moonlit brocade','zh-CN')

    def test_bing_cached_and_available_offline(self):
        with patch.object(self.store.bing,'translate',return_value='月光锦缎') as request:
            self.assertEqual(self.store.translate('Moonlit brocade'),('月光锦缎','bing'))
            self.assertEqual(request.call_count,1)
        self.store.save_config({'online':False})
        with patch.object(self.store.bing,'translate',side_effect=AssertionError('offline network')):
            self.assertEqual(self.store.translate('Moonlit brocade'),('月光锦缎','bing'))

    def test_opt_in_fallback_uses_actual_provider_and_budget(self):
        self.store.save_config({'fallback':True})
        source='Moonlit brocade'
        reply={'responseStatus':200,'responseData':{'translatedText':'月光锦缎'}}
        with patch.object(self.store.bing,'translate',side_effect=urllib.error.URLError('unavailable')), patch('core.request_json',return_value=reply), patch('core.time.sleep'):
            self.assertEqual(self.store.translate(source),('月光锦缎','mymemory'))
        budget=self.store.db.execute('SELECT bytes FROM budget').fetchone()[0]
        self.assertEqual(budget,2*len(source.encode()))
        self.assertEqual(self.store.cache_get(source,'zh-CN')[1],'mymemory')

    def test_fallback_off_is_single_attempt(self):
        with patch.object(self.store.bing,'translate',side_effect=ValueError(SERVICE_ERROR)), patch('core.request_json',side_effect=AssertionError('fallback disabled')):
            with self.assertRaises(ValueError): self.store.translate('Moonlit brocade')
        self.assertIsNone(self.store.cache_get('Moonlit brocade','zh-CN'))

    def test_budget_exhaustion_prevents_both_providers(self):
        self.store.save_config({'fallback':True,'daily_bytes':0})
        with patch.object(self.store.bing,'translate',side_effect=AssertionError('budget exceeded')), patch('core.request_json',side_effect=AssertionError('budget exceeded')):
            with self.assertRaises(ValueError): self.store.translate('Moonlit brocade')

    def test_format_damage_not_cached_or_sent_to_fallback(self):
        self.store.save_config({'fallback':True})
        source='Moonlit brocade {0}'
        with patch.object(self.store.bing,'translate',return_value='月光锦缎'), patch('core.request_json',side_effect=AssertionError('unsafe fallback')):
            with self.assertRaises(ValueError): self.store.translate(source)
        self.assertIsNone(self.store.cache_get(source,'zh-CN'))

    def test_legacy_settings_add_fallback_without_resetting_choices(self):
        root=Path(self.temp.name)/'legacy';root.mkdir()
        (root/'settings.json').write_text(json.dumps({'language':'fr','online':False,'provider':'libre','libre_url':'https://example.org'}))
        store=Store(root,BUNDLE)
        self.assertFalse(store.config['fallback'])
        self.assertFalse(store.config['online'])
        self.assertEqual(store.config['language'],'fr')
        store.db.close()

if __name__ == '__main__': unittest.main()
