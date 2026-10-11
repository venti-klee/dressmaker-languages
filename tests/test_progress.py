import sys
import tempfile
import threading
import time
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

BUNDLE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BUNDLE / 'assistant'))
from core import Store, Worker
from progress import TranslationProgress


class ProgressTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / 'data', BUNDLE)
        self.store.save_config({'game': str(Path(self.temp.name) / 'game'), 'online': False,
                                'offline_model': False, 'auto': False})
        self.worker = Worker(self.store)

    def tearDown(self):
        self.store.db.close()
        self.temp.cleanup()

    def add(self, *sources):
        for source in sources:
            self.store.add_pending(source)

    def test_bad_format_rejects_one_translation_without_blocking_other_words(self):
        self.add('Quux Alpha', 'Quux Bravo')
        self.store.save_config({'online': True})
        attempts = []
        def translate(source, config, on_progress=None):
            attempts.append(config['online'])
            if source.endswith('Alpha'):
                raise ValueError('译文破坏了标签或变量，已拒绝写入')
            return '有效译文', 'google'
        with patch.object(self.store, 'translate', side_effect=translate), patch.object(self.worker.stop, 'wait'):
            self.worker.process_batch(self.store.config.copy())
        self.assertEqual(attempts, [True, True])
        self.assertEqual(self.worker.cooldown, 0)
        result = self.worker.progress.snapshot()
        self.assertEqual((result['failed'], result['translated']), (1, 1))

    def test_outcomes_distinguish_failures_from_kept_originals(self):
        self.add('Quux Alpha', 'Quux Bravo', 'Quux Charlie')
        def translate(source, config, on_progress=None):
            if source.endswith('Alpha'):
                return '成功译文', 'argos-offline'
            if source.endswith('Bravo'):
                return source, 'untranslated'
            raise TimeoutError('timed out')
        with patch.object(self.store, 'translate', side_effect=translate):
            self.worker.process_batch(self.store.config.copy())
        result = self.worker.progress.snapshot()
        self.assertEqual((result['total'], result['processed']), (3, 3))
        self.assertEqual((result['translated'], result['untranslated'], result['failed']), (1, 1, 1))
        self.assertEqual(result['recent'][0]['error_info']['key'], 'error_network')
        self.assertFalse(result['active'])

    def test_current_word_visible_while_offline_model_is_blocked(self):
        self.add('Quux Alpha')
        self.store.save_config({'offline_model': True})
        started, release = threading.Event(), threading.Event()
        def offline(source, language):
            started.set()
            if not release.wait(3):
                raise RuntimeError('test model timed out')
            return '模型译文'
        with patch.object(self.store, 'offline', side_effect=offline):
            thread = threading.Thread(target=self.worker.process_batch, args=(self.store.config.copy(),))
            thread.start()
            try:
                self.assertTrue(started.wait(1))
                result = self.worker.progress.snapshot()
                self.assertEqual(result['current'], 'Quux Alpha')
                self.assertEqual(result['provider'], 'argos-offline')
                self.assertEqual(result['processed'], 0)
                self.assertTrue(result['active'])
                self.assertEqual(self.store.status()['cached'], 0)
            finally:
                release.set()
                thread.join(3)
        self.assertFalse(thread.is_alive())
        self.assertEqual(self.worker.progress.snapshot()['translated'], 1)

    def test_rate_wait_and_fallback_report_the_actual_service(self):
        self.store.save_config({'online': True, 'provider': 'bing', 'fallback': True})
        self.add('Quux Alpha')
        self.worker.progress.begin('zh-CN', 1)
        self.worker.progress.current('Quux Alpha')
        stages = []
        def stage(phase, provider, wait_until=0):
            self.worker.progress.stage(phase, provider, wait_until)
            stages.append(self.worker.progress.snapshot())
        reply = {'responseStatus': 200, 'responseData': {'translatedText': '备用服务译文'}}
        with patch.object(self.store.bing, 'translate', side_effect=urllib.error.URLError('offline')), patch('core.request_json', return_value=reply), patch('core.time.sleep'):
            value, provider = self.store.translate('Quux Alpha', on_progress=stage)
        self.assertEqual(provider, 'mymemory')
        self.assertTrue(any(s['state'] == 'waiting' and s['provider'] == 'mymemory' and s['wait_until'] > time.time() for s in stages))
        self.assertEqual(stages[-1]['provider'], 'mymemory')
        self.assertEqual(stages[-1]['current'], 'Quux Alpha')

    def test_repeated_start_does_not_reset_active_progress(self):
        self.worker.request_translation()
        self.assertEqual(self.worker.progress.snapshot()['state'], 'queued')
        self.worker.progress.begin('zh-CN', 2)
        self.worker.progress.current('Quux Alpha')
        self.worker.progress.record('Quux Alpha', '译文', 'dictionary', 'success')
        self.worker.request_translation()
        self.assertEqual(self.worker.progress.snapshot()['processed'], 1)
        self.worker.progress.finish()
        self.worker.request_translation()
        self.assertEqual(self.worker.progress.snapshot()['processed'], 0)

    def test_language_change_interrupts_batch_without_claiming_completion(self):
        self.add('Quux Alpha', 'Quux Bravo')
        def translate(source, config, on_progress=None):
            self.store.save_config({'language': 'fr'})
            return '译文', 'dictionary'
        with patch.object(self.store, 'translate', side_effect=translate):
            self.worker.process_batch(self.store.config.copy())
        result = self.worker.progress.snapshot()
        self.assertEqual(result['state'], 'interrupted')
        self.assertEqual((result['processed'], result['total']), (1, 2))
        self.assertEqual(result['language'], 'zh-CN')
        self.assertEqual(result['recent'][0]['language'], 'zh-CN')

    def test_game_write_failure_keeps_successful_cache_and_does_not_cooldown(self):
        self.add('Quux Alpha')
        self.store.installed = True
        def translate(source, config, on_progress=None):
            self.store.cache_put(source, config['language'], '缓存译文', 'bing')
            return '缓存译文', 'bing'
        with patch.object(self.store, 'translate', side_effect=translate), patch.object(self.store, 'publish', side_effect=PermissionError('denied')), patch.object(self.worker.stop, 'wait'):
            self.worker.process_batch(self.store.config.copy())
        result = self.worker.progress.snapshot()
        self.assertEqual((result['translated'], result['failed']), (1, 0))
        self.assertEqual(self.worker.cooldown, 0)
        self.assertEqual(self.store.cache_get('Quux Alpha', 'zh-CN')[0], '缓存译文')
        self.assertIn('denied', self.store.error)

    def test_recent_results_are_bounded_and_snapshot_is_detached(self):
        progress = TranslationProgress()
        progress.begin('zh-CN', 15)
        for index in range(15):
            progress.record(str(index), '译文', 'dictionary', 'success')
        snapshot = progress.snapshot()
        self.assertEqual(snapshot['processed'], 15)
        self.assertEqual(len(snapshot['recent']), 10)
        snapshot['recent'][0]['source'] = 'tampered'
        self.assertEqual(progress.snapshot()['recent'][0]['source'], '14')

    def test_online_error_shows_cooldown_and_zero_candidate_run_finishes(self):
        self.add('Quux Alpha')
        self.store.save_config({'online': True})
        with patch.object(self.store, 'translate', side_effect=TimeoutError('timed out')):
            self.worker.process_batch(self.store.config.copy())
        result = self.worker.progress.snapshot()
        self.assertEqual(result['state'], 'cooldown')
        self.assertGreater(result['wait_until'], time.time())
        progress = TranslationProgress()
        progress.begin('fr', 1)
        progress.finish('cooldown', time.time() - 1)
        self.assertEqual(progress.snapshot()['state'], 'finished')
        with self.store.lock:
            self.store.db.execute('DELETE FROM pending')
            self.store.db.commit()
        self.worker.request_translation()
        self.worker.process_batch(self.store.config.copy(), all_candidates=True)
        self.assertFalse(self.worker.progress.snapshot()['active'])
        self.assertEqual(self.worker.progress.snapshot()['total'], 0)

    def test_network_failure_keeps_remaining_batch_unprocessed_and_remembers_manual_scope(self):
        for source in ['Quux Alpha', 'Quux Bravo', 'Quux Charlie']:
            self.store.add_pending(source, 'loader')
        self.store.save_config({'online': True})
        with patch.object(self.store, 'translate', side_effect=TimeoutError('timed out')) as translate:
            self.worker.process_batch(self.store.config.copy(), all_candidates=True)
        result = self.worker.progress.snapshot()
        self.assertEqual(translate.call_count, 1)
        self.assertEqual((result['total'], result['processed'], result['remaining']), (3, 1, 2))
        self.assertEqual((result['translated'], result['untranslated'], result['failed']), (0, 0, 1))
        self.assertTrue(self.worker.deferred_batch[1])
        self.assertTrue(result['retry'])

    def test_repeated_start_during_cooldown_does_not_reset_counters_or_call_service(self):
        self.store.save_config({'online': True})
        self.add('Quux Alpha', 'Quux Bravo')
        with patch.object(self.store, 'translate', side_effect=TimeoutError('timed out')):
            self.worker.process_batch(self.store.config.copy())
        cooldown = self.worker.cooldown
        with patch.object(self.store, 'translate', side_effect=AssertionError('cooldown request')):
            self.worker.request_translation()
            self.worker.process_batch(self.store.config.copy(), all_candidates=True)
        self.assertEqual(self.worker.cooldown, cooldown)
        self.assertEqual((self.worker.progress.snapshot()['processed'], self.worker.progress.snapshot()['remaining']), (1, 1))

    def test_expired_resumable_cooldown_is_queued_not_finished(self):
        progress = TranslationProgress()
        progress.begin('zh-CN', 3)
        progress.record('Quux Alpha', '', 'google', 'failed', TimeoutError('timed out'))
        progress.finish('cooldown', time.time() - 1, retry=True)
        result = progress.snapshot()
        self.assertEqual((result['state'], result['active'], result['remaining']), ('queued', True, 2))

    def test_manual_batch_resumes_after_cooldown_without_auto_enabled(self):
        self.store.add_pending('Quux Alpha', 'loader')
        self.store.add_pending('Quux Bravo', 'loader')
        self.store.save_config({'online': True, 'auto': False})
        with patch.object(self.store, 'translate', side_effect=TimeoutError('timed out')):
            self.worker.process_batch(self.store.config.copy(), all_candidates=True)
        self.worker.cooldown = 0
        self.worker.last_model_attempt.clear()
        attempts = []
        def translate(source, config, on_progress=None):
            attempts.append(source)
            self.store.cache_put(source, config['language'], '本机模型译文', 'argos-offline')
            if len(attempts) == 2:
                self.worker.stop.set()
            return '本机模型译文', 'argos-offline'
        with patch.object(self.store, 'translate', side_effect=translate):
            self.worker.run()
        self.assertEqual(attempts, ['Quux Alpha', 'Quux Bravo'])
        self.assertEqual(self.worker.progress.snapshot()['translated'], 2)

    def test_changed_settings_cancel_old_deferred_batch(self):
        self.store.add_pending('Quux Alpha', 'loader')
        self.store.save_config({'online': True})
        with patch.object(self.store, 'translate', side_effect=TimeoutError('timed out')):
            self.worker.process_batch(self.store.config.copy(), all_candidates=True)
        self.store.save_config({'language': 'fr'})
        def stop_wait(seconds):
            self.worker.stop.set()
        with patch.object(self.store, 'translate', side_effect=AssertionError('old language retry')), patch.object(self.worker.stop, 'wait', side_effect=stop_wait):
            self.worker.run()
        self.assertIsNone(self.worker.deferred_batch)
        self.assertEqual(self.worker.progress.snapshot()['state'], 'interrupted')

    def test_identity_result_does_not_count_as_translated(self):
        self.add('512 MiB')
        self.worker.process_batch(self.store.config.copy())
        self.assertEqual(self.worker.progress.snapshot()['translated'], 0)
        self.assertEqual(self.store.cache_get('512 MiB', 'zh-CN'), ('512 MiB', 'original'))

    def test_oversized_entry_does_not_pause_other_entries_or_schedule_service_retry(self):
        self.add('Quux Alpha', 'Quux Bravo')
        self.store.save_config({'online': True})
        def translate(source, config, on_progress=None):
            if source.endswith('Alpha'):
                raise ValueError('单条超过免费接口的 500 字节限制，请安装离线模型或手动翻译')
            return '有效译文', 'argos-offline'
        with patch.object(self.store, 'translate', side_effect=translate):
            self.worker.process_batch(self.store.config.copy())
        result = self.worker.progress.snapshot()
        self.assertEqual((result['processed'], result['translated'], result['failed']), (2, 1, 1))
        self.assertEqual(self.worker.cooldown, 0)
        self.assertIsNone(self.worker.deferred_batch)


if __name__ == '__main__':
    unittest.main()
