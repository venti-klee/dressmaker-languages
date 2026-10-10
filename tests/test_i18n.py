import json
from pathlib import Path
import re
import sys
import unittest

BUNDLE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BUNDLE / "assistant"))
from i18n import ERROR_CODES, error_info

class LocalizationTests(unittest.TestCase):
    def setUp(self):
        self.catalogs = json.loads((BUNDLE / "assistant/locales.json").read_text())

    def test_every_locale_has_every_key_and_matching_variables(self):
        reference = self.catalogs["en"]
        self.assertEqual(set(self.catalogs), {"zh-CN", "en", "ja", "ko", "fr", "de", "es"})
        for language, catalog in self.catalogs.items():
            self.assertEqual(set(reference), set(catalog), language)
            for key, value in catalog.items():
                self.assertTrue(value.strip(), (language, key))
                self.assertEqual(set(re.findall(r"\{\w+\}", reference[key])), set(re.findall(r"\{\w+\}", value)), (language, key))

    def test_html_static_and_dynamic_labels_have_translations(self):
        page = (BUNDLE / "assistant/index.html").read_text()
        keys = re.findall(r'data-i18n(?:-placeholder|-aria)?="([^"]+)"', page)
        keys += re.findall(r"\bt\('([^']+)'", page)
        keys = [key for key in keys if not key.endswith("_")]
        keys += ["kind_display", "kind_content", "kind_loader", "model_idle", "model_installing", "model_done", "model_failed"]
        for language, catalog in self.catalogs.items():
            for key in keys:
                self.assertIn(key, catalog, (language, key))

    def test_backend_errors_are_localizable(self):
        for message, key in ERROR_CODES.items():
            self.assertEqual(error_info(message)["key"], key)
            for catalog in self.catalogs.values():
                self.assertIn(key, catalog)
        self.assertEqual(error_info(PermissionError("denied"))["key"], "error_permission")
        self.assertEqual(error_info(TimeoutError("timed out"))["key"], "error_network")
        self.assertIsNone(error_info(""))

    def test_guides_exist_and_all_local_links_resolve(self):
        for language in self.catalogs:
            path = BUNDLE / "docs" / (language + ".md")
            text = path.read_text()
            self.assertGreater(len(text), 3000, language)
            self.assertIn("0.1.1", text)
            self.assertIn("Start.command", text)
            self.assertIn("4,500" if language == "en" else "4", text)
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if not target.startswith("https://"):
                    self.assertTrue((path.parent / target).is_file(), (language, target))
        for filename in ["README.md", "使用说明.md", "README.zh-CN.md", "README.ja.md", "README.ko.md", "README.fr.md", "README.de.md", "README.es.md"]:
            path = BUNDLE / filename
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if not target.startswith("https://"):
                    self.assertTrue((path.parent / target).is_file(), target)

if __name__ == "__main__":
    unittest.main()
