import sys
import tempfile
import unittest
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BUNDLE / "assistant"))
from core import Store


class DictionaryBrowserTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / "data", BUNDLE)
        self.store.save_config({"game": str(Path(self.temp.name) / "game"), "auto": False, "online": False})
        self.store.dictionary = {"Brocade": "织锦", "Ecru": "浅米色", "Glossary": "术语"}
        self.store.db.executemany("INSERT INTO pending VALUES (?,?)", [
            ("Aurora", "display"), ("Brocade", "display"), ("Cloud", "content"),
            ("Drift", "loader"), ("Ecru", "display"), ("FabricId", "display")])
        for source, value, provider in [
            ("Brocade", "被词典覆盖的旧译文", "bing"), ("Cloud", "云纹", "google"),
            ("Drift", "漂移", "bing"), ("Ecru", "米色手改", "manual"),
            ("FabricId", "FabricId", "original"), ("History", "历史", "libre")]:
            self.store.cache_put(source, "zh-CN", value, provider)
        self.store.cache_put("Private other language", "ko", "다른 언어", "google")

    def tearDown(self):
        self.store.db.close()
        self.temp.cleanup()

    def sources(self, **filters):
        return [item["source"] for item in self.store.browse_entries(**filters)["entries"]]

    def test_browse_includes_dictionary_and_cache_without_expanding_worker_queue(self):
        self.assertEqual(len(self.sources()), 8)
        self.assertEqual(set(self.sources(kind="stored")), {"Glossary", "History"})
        self.assertEqual(len(self.sources(kind="collected")), 6)
        self.assertEqual(len(self.store.entries()), 6)

    def test_missing_uses_effective_dictionary_and_manual_values(self):
        result = self.store.browse_entries(state="missing")
        self.assertEqual([item["source"] for item in result["entries"]], ["Aurora"])
        self.assertEqual(result["counts"], {"missing": 1, "translated": 6, "original": 1})
        records = {item["source"]: item for item in self.store.browse_entries()["entries"]}
        self.assertEqual((records["Brocade"]["value"], records["Brocade"]["provider"]), ("织锦", "dictionary"))
        self.assertEqual((records["Ecru"]["value"], records["Ecru"]["provider"]), ("米色手改", "manual"))

    def test_channels_use_actual_effective_provider(self):
        self.assertEqual(self.sources(provider="bing"), ["Drift"])
        self.assertEqual(self.sources(provider="google"), ["Cloud"])
        self.assertEqual(self.sources(provider="manual"), ["Ecru"])
        self.assertEqual(self.sources(provider=""), ["Aurora"])
        self.assertEqual(self.sources(provider="dictionary"), ["Brocade", "Glossary"])

    def test_filters_combine_search_status_provider_and_kind(self):
        self.assertEqual(self.sources(query="云", state="translated", provider="google", kind="content"), ["Cloud"])
        self.assertEqual(self.sources(query="云", state="missing", provider="google", kind="content"), [])

    def test_search_is_literal_case_insensitive_and_searches_saved_translation(self):
        self.assertEqual(self.sources(query="  cLoUd "), ["Cloud"])
        self.assertEqual(self.sources(query="手改"), ["Ecru"])
        self.assertEqual(self.sources(query="被词典覆盖"), [])
        for text in ["100% weave", "under_score"]:
            self.store.db.execute("INSERT INTO pending VALUES (?, 'content')", (text,))
        self.assertEqual(self.sources(query="%"), ["100% weave"])
        self.assertEqual(self.sources(query="_"), ["under_score"])

    def test_originals_are_separate_from_translated_and_missing(self):
        self.assertEqual(self.sources(state="original"), ["FabricId"])
        self.assertNotIn("FabricId", self.sources(state="translated"))
        self.assertNotIn("FabricId", self.sources(state="missing"))

    def test_paginated_results_have_no_gaps_duplicates_or_500_row_cap(self):
        self.store.db.executemany("INSERT INTO pending VALUES (?, 'content')", [("Page %04d" % n,) for n in range(537)])
        sources = []
        for page in range(1, 23):
            result = self.store.browse_entries(query="Page ", page=page, page_size=25)
            self.assertEqual((result["matching"], result["pages"]), (537, 22))
            sources.extend(item["source"] for item in result["entries"])
        self.assertEqual(sources, ["Page %04d" % n for n in range(537)])
        result = self.store.browse_entries(query="Page ", page=999, page_size=25)
        self.assertEqual((result["page"], result["start"], result["end"]), (22, 526, 537))

    def test_sorting_and_empty_page_metadata(self):
        self.assertEqual(self.sources(order="source_desc"), list(reversed(self.sources())))
        self.assertEqual(self.sources(order="priority")[:4], ["Aurora", "Brocade", "Ecru", "FabricId"])
        self.store.db.execute("UPDATE translations SET updated='2020-01-01' WHERE source='Cloud'")
        self.store.db.execute("UPDATE translations SET updated='2099-01-01' WHERE source='Drift'")
        self.assertEqual(self.sources(order="recent")[0], "Drift")
        empty = self.store.browse_entries(query="not-found", page=99)
        self.assertEqual((empty["page"], empty["pages"], empty["start"], empty["end"]), (1, 1, 0, 0))

    def test_other_languages_do_not_leak_into_results(self):
        self.assertNotIn("Private other language", self.sources())
        self.store.save_config({"language": "ko"})
        self.store.dictionary = {}
        self.assertEqual(self.sources(provider="google"), ["Private other language"])
        self.assertEqual(len(self.sources(state="missing")), 6)

    def test_english_target_keeps_original_without_claiming_missing(self):
        self.store.save_config({"language": "en"})
        self.store.dictionary = {}
        self.assertEqual(self.sources(state="missing"), [])
        self.assertEqual(len(self.sources(state="original")), 6)

    def test_invalid_filters_and_unbounded_pages_are_rejected(self):
        for filters in [{"state": "unknown"}, {"kind": "unknown"}, {"order": "unknown"},
                        {"page": 0}, {"page": 1000001}, {"page": True},
                        {"page_size": 100000}, {"page_size": 0}, {"query": "x" * 1001}]:
            with self.subTest(filters=filters), self.assertRaisesRegex(ValueError, "无效的词典筛选条件"):
                self.store.browse_entries(**filters)


if __name__ == "__main__":
    unittest.main()
