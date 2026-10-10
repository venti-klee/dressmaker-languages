import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

BUNDLE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BUNDLE / 'assistant'))
from core import Store, Worker, protect, restore, validate



class Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / 'data', BUNDLE)
        self.store.save_config({'game': str(Path(self.temp.name) / 'game'), 'online': False})

    def tearDown(self):
        self.store.db.close()
        self.temp.cleanup()

    def test_complete_offline_name_and_ui(self):
        with patch('core.request_json', side_effect=AssertionError('offline made request')):
            self.assertEqual(self.store.translate('Mod Manager')[0], '模组管理器')
            self.assertEqual(self.store.translate('Red Silk')[0], '红色真丝')
            self.assertEqual(self.store.translate('unlistedquux')[1], 'untranslated')

    def test_no_partial_translation(self):
        self.assertEqual(self.store.translate('Red Unknownxyz Silk')[0], 'Red Unknownxyz Silk')

    def test_manual_beats_dictionary_and_persists(self):
        self.store.cache_put('Mod Manager', 'zh-CN', '我的模组', 'manual')
        self.assertEqual(self.store.translate('Mod Manager')[0], '我的模组')
        reopened = Store(self.store.root, BUNDLE)
        self.assertEqual(reopened.translate('Mod Manager')[0], '我的模组')
        reopened.db.close()

    def test_language_separation_and_switch_back(self):
        self.store.cache_put('Something new', 'zh-CN', '新东西', 'mymemory')
        self.store.cache_put('Something new', 'fr', 'Quelque chose de nouveau', 'mymemory')
        self.store.save_config({'language': 'fr'})
        self.assertEqual(self.store.translate('Something new')[0], 'Quelque chose de nouveau')
        self.store.save_config({'language': 'zh-CN'})
        self.assertEqual(self.store.translate('Something new')[0], '新东西')

    def test_placeholder_round_trip(self):
        source = '<color=#ff00ff>Buy {0} [$name] %s</color>\n'
        masked, tokens = protect(source)
        result = restore(masked.replace('Buy', '购买'), tokens)
        self.assertEqual(validate(source, result), source.replace('Buy', '购买'))
        with self.assertRaises(ValueError):
            restore(masked.replace(tokens[0][0], ''), tokens)
        with self.assertRaises(ValueError):
            validate(source, result.replace('{0}', '{1}'))

    def test_no_failed_api_response_cached(self):
        self.store.save_config({'online': True})
        with patch('core.request_json', return_value={'responseStatus': 429, 'responseDetails': 'quota exceeded'}):
            with self.assertRaises(ValueError):
                self.store.translate('unlistedquux')
        self.assertIsNone(self.store.cache_get('unlistedquux', 'zh-CN'))

    def test_successful_network_cached_then_offline(self):
        self.store.save_config({'online': True})
        with patch('core.request_json', return_value={'responseStatus': 200, 'responseData': {'translatedText': '星光布料'}}) as request:
            self.assertEqual(self.store.translate('Starlight fabric')[0], '星光布料')
            self.assertEqual(request.call_count, 1)
        self.store.save_config({'online': False})
        with patch('core.request_json', side_effect=AssertionError('network made request')):
            self.assertEqual(self.store.translate('Starlight fabric')[0], '星光布料')

    def test_daily_budget_before_request(self):
        self.store.save_config({'online': True, 'daily_bytes': 0})
        with patch('core.request_json', side_effect=AssertionError('budget made request')):
            with self.assertRaises(ValueError):
                self.store.translate('unlistedquux')

    def test_incomplete_queue_line_not_consumed(self):
        self.store.plugin_data.mkdir(parents=True)
        queue = self.store.plugin_data / 'pending.jsonl'
        queue.write_bytes(b'{"source":"New item"}')
        worker = Worker(self.store)
        worker.ingest()
        self.assertEqual(worker.offset, 0)
        with queue.open('ab') as file: file.write(b'\n')
        worker.ingest()
        self.assertEqual(self.store.entries()[0]['source'], 'New item')

    def test_new_mod_is_discovered_after_rescan_without_rewriting_files(self):
        loader = self.store.game / 'BepInEx/plugins/DressmakerMods.dll'
        loader.parent.mkdir(parents=True)
        loader.write_bytes(b'fixture')
        folder = self.store.game / 'Mods/new-fabric'
        folder.mkdir(parents=True)
        manifest = folder / 'mod.json'
        content = '{"id":"keep-this-id","items":[{"displayName":"Moonlit brocade fabric","tooltip":"A new fabric"}]}'
        manifest.write_text(content)
        with patch('core.loader_literals', return_value=[]):
            self.store.scan()
            self.assertIn('Moonlit brocade fabric', {x['source'] for x in self.store.entries()})
            second = folder / 'extra.json'
            second.write_text('{"name":"Starlight lace"}')
            self.store.scan()
        self.assertIn('Starlight lace', {x['source'] for x in self.store.entries()})
        self.assertEqual(manifest.read_text(), content)
        self.assertEqual(set(json.loads((self.store.root/'known-sources.json').read_text())), {'Moonlit brocade fabric','A new fabric','Starlight lace'})

    def test_config_rejects_unsafe_inputs(self):
        for value in ['../escape', 'jp', 'zz']:
            with self.assertRaises(ValueError): self.store.save_config({'language': value})
        with self.assertRaises(ValueError): self.store.save_config({'online': 'false'})
        with self.assertRaises(ValueError): self.store.save_config({'libre_url': 'http://example.com'})

    def test_publish_and_uninstall_preserve_original_mods(self):
        self.store.plugin_data.mkdir(parents=True)
        original = self.store.game / 'Mods/example/mod.json'
        original.parent.mkdir(parents=True)
        original.write_text('{"id":"original-id"}')
        self.store.publish()
        self.assertEqual(json.loads((self.store.plugin_data / 'runtime.json').read_text())['language'], 'zh-CN')
        self.store.uninstall()
        self.assertEqual(original.read_text(), '{"id":"original-id"}')
        self.assertTrue(list((self.store.root / 'backups').glob('*/config/runtime.json')))

if __name__ == '__main__': unittest.main()
