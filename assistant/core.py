"""Independent Mac companion. Only owns its plugin, configuration and translation data."""
import collections
import datetime
import html
import io
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import struct
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from providers import BingWeb

LANGUAGES = {"zh-CN": "简体中文", "ja": "日本語", "ko": "한국어", "fr": "Français", "de": "Deutsch", "es": "Español", "en": "English（原文）"}
ARGOS_CODES = {"zh-CN": "zh", "ja": "ja", "ko": "ko", "fr": "fr", "de": "de", "es": "es"}
GAME_DEFAULT = Path.home() / "Library/Application Support/Steam/steamapps/common/Dressmaker"
PROTECTED = re.compile(r"<[^>\n]+>|\{[^{}\n]*\}|\[\$?[^\[\]\n]+\]|%(?:\d+\$)?[-+\d.]*[sdfi]|\\[nrt]|\r?\n")

def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".write-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(value, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return default

def manual_archive(bundle, language, values, known_sources):
    """Build an installable ZIP entirely in memory, without writing to the game."""
    bundle = Path(bundle)
    if language not in LANGUAGES:
        raise ValueError("暂不支持此语言")
    plugin = bundle / "BepInEx/plugins/DressmakerLanguages/DressmakerLanguages.dll"
    if not plugin.is_file():
        raise ValueError("缺少已编译的游戏插件")
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(plugin, "BepInEx/plugins/DressmakerLanguages/DressmakerLanguages.dll")
        configs = {"runtime.json": {"language": language}, "known-sources.json": known_sources,
                   "translations." + language + ".json": values}
        for name, value in configs.items():
            archive.writestr("BepInEx/config/DressmakerLanguages/" + name,
                             json.dumps(value, ensure_ascii=False, indent=2) + "\n")
        for locale in LANGUAGES:
            archive.write(bundle / "docs" / ("manual-" + locale + ".md"), "INSTALL." + locale + ".md")
        archive.writestr("README.md", "Dressmaker Languages · Manual installation\n\n" +
                        " · ".join("[%s](INSTALL.%s.md)" % (name, locale) for locale, name in LANGUAGES.items()) + "\n")
        archive.write(bundle / "LICENSE", "LICENSE")
    return output.getvalue()

def protect(source):
    tokens = []
    def replace(match):
        marker = "ZXQPH%dQXZ" % len(tokens)
        tokens.append((marker, match.group()))
        return marker
    return PROTECTED.sub(replace, source), tokens

def restore(translated, tokens):
    for marker, token in tokens:
        if translated.count(marker) != 1:
            raise ValueError("译文破坏了标签或变量，已拒绝写入")
        translated = translated.replace(marker, token)
    return translated

def validate(source, translated):
    if not isinstance(translated, str) or not translated.strip() or len(translated) > max(10000, len(source) * 15):
        raise ValueError("译文为空或过长")
    if collections.Counter(PROTECTED.findall(source)) != collections.Counter(PROTECTED.findall(translated)):
        raise ValueError("译文中的格式标签或变量与原文不一致")
    if any(x in translated.upper() for x in ("MYMEMORY WARNING", "QUERY LENGTH LIMIT", "INVALID LANGUAGE PAIR", "TOO MANY REQUESTS")):
        raise ValueError("翻译服务返回了错误提示")
    return translated

def request_json(url, payload=None, timeout=15):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "DressmakerLanguages/0.1", "Content-Type": "application/json", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read(2 * 1024 * 1024 + 1)
        if len(raw) > 2 * 1024 * 1024:
            raise ValueError("接口返回内容过大")
        return json.loads(raw.decode("utf-8"))

def loader_literals(path):
    """Read ECMA-335 #US heap without loading or executing the game assembly."""
    p = Path(path).read_bytes()
    b = p.index(b"BSJB")
    v = struct.unpack_from("<I", p, b + 12)[0]
    pos = (b + 16 + v + 3) & ~3
    n = struct.unpack_from("<H", p, pos + 2)[0]
    pos += 4
    heap = b""
    for _ in range(n):
        offset, size = struct.unpack_from("<II", p, pos)
        end = p.index(b"\0", pos + 8)
        name = p[pos + 8:end]
        pos = (end + 4) & ~3
        if name == b"#US":
            heap = p[b + offset:b + offset + size]
    result, pos = [], 1
    while pos < len(heap):
        first = heap[pos]
        pos += 1
        if first & 0x80 == 0:
            length = first
        elif first & 0xc0 == 0x80:
            length = ((first & 0x3f) << 8) | heap[pos]
            pos += 1
        else:
            length = ((first & 0x1f) << 24) | int.from_bytes(heap[pos:pos + 3], "big")
            pos += 3
        if length:
            result.append(heap[pos:pos + length - 1].decode("utf-16-le", errors="replace"))
        pos += length
    return result

def official_dictionary(game, target):
    folder = Path(game) / "BepInEx/config/DressmakerMods/localization-reference"
    to_locale = {"zh-CN": "zh-hans", "ja": "ja", "en": "en"}.get(target)
    if not to_locale:
        return {}
    en = read_json(folder / "en.json", {})
    to = read_json(folder / (to_locale + ".json"), {})
    if not en or not to:
        return {}
    targets = {(table["name"], str(e["id"])): e.get("value", "") for table in to.get("tables", []) for e in table.get("entries", [])}
    result = {}
    for table in en.get("tables", []):
        for e in table.get("entries", []):
            src = e.get("value", "")
            dst = targets.get((table["name"], str(e["id"])), "")
            if src and dst:
                try:
                    result[src] = validate(src, dst)
                except ValueError:
                    pass
    return result

class Store:
    def __init__(self, root, bundle):
        self.root = Path(root)
        self.bundle = Path(bundle)
        self.root.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self.db = sqlite3.connect(str(self.root / "translations.sqlite3"), check_same_thread=False)
        self.db.execute("CREATE TABLE IF NOT EXISTS translations (source TEXT, language TEXT, value TEXT, provider TEXT, updated TEXT, PRIMARY KEY(source, language))")
        self.db.execute("CREATE TABLE IF NOT EXISTS pending (source TEXT PRIMARY KEY, kind TEXT)")
        self.db.execute("CREATE TABLE IF NOT EXISTS budget (day TEXT PRIMARY KEY, bytes INTEGER)")
        self.db.commit()
        defaults = {"language": "zh-CN", "online": True, "offline_model": True, "provider": "mymemory", "daily_bytes": 4500, "libre_url": "", "game": str(GAME_DEFAULT), "auto": True, "fallback": False}
        self.config = dict(defaults, **read_json(self.root / "settings.json", {}))
        self.bing = BingWeb()
        self.network_lock = threading.Lock()
        self.next_request = 0
        self.error = ""
        self.installed = False
        self.dictionary = {}
        self.reload_dictionary()

    @property
    def game(self):
        return Path(self.config["game"]).expanduser().resolve()

    @property
    def plugin_data(self):
        return self.game / "BepInEx/config/DressmakerLanguages"

    def save_config(self, changes):
        with self.lock:
            for key, value in changes.items():
                if key in {"online", "offline_model", "auto", "fallback"}:
                    if not isinstance(value, bool):
                        raise ValueError("开关必须为布尔值")
                elif key == "language":
                    if value not in LANGUAGES:
                        raise ValueError("暂不支持此语言")
                elif key == "provider":
                    if value not in {"mymemory", "libre", "bing"}:
                        raise ValueError("未知翻译服务")
                elif key == "libre_url":
                    parsed = urllib.parse.urlparse(value)
                    if value and (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password):
                        raise ValueError("LibreTranslate 地址必须为 HTTPS，不能包含账号密码")
                elif key == "daily_bytes":
                    if not isinstance(value, int) or not 0 <= value <= 50000:
                        raise ValueError("每日预算必须在 0 到 50000 字节之间")
                elif key == "game":
                    if not isinstance(value, str) or not value.strip():
                        raise ValueError("请填写游戏目录")
                else:
                    raise ValueError("未知设置")
            self.config.update(changes)
            atomic_json(self.root / "settings.json", self.config)
            self.reload_dictionary()
            if self.installed:
                self.publish()

    def reload_dictionary(self):
        language = self.config["language"]
        self.dictionary = read_json(self.bundle / "assistant/dictionary.json", {}).get(language, {}).copy()
        self.dictionary.update(official_dictionary(self.game, language))

    def add_pending(self, source, kind="display"):
        if not isinstance(source, str) or not source.strip() or len(source) > 2000:
            return
        if not re.search("[A-Za-z]", source) or re.match(r"^(?:https?://|[/\\]|[A-Z]:\\)", source):
            return
        with self.lock:
            self.db.execute("INSERT INTO pending VALUES (?,?) ON CONFLICT(source) DO UPDATE SET kind=CASE WHEN excluded.kind='display' THEN 'display' WHEN pending.kind='loader' THEN excluded.kind ELSE pending.kind END", (source, kind))
            self.db.commit()

    def scan(self):
        game = self.game
        if not (game / "BepInEx/plugins/DressmakerMods.dll").is_file():
            raise ValueError("此目录未找到 Yuuma ModLoader，请先安装其 Mac 版")
        sources = set()
        # Read display fields; never rewrite the source manifests or item identifiers.
        def visit(j):
            if isinstance(j, dict):
                for key, value in j.items():
                    if key.lower() in {"name", "displayname", "display_name", "description", "tooltip", "title"} and isinstance(value, str):
                        sources.add(value)
                    elif isinstance(value, (dict, list)):
                        visit(value)
            elif isinstance(j, list):
                for value in j:
                    visit(value)
        for directory in [game / "Mods", game / "BepInEx/config/DressmakerMods"]:
            if directory.exists():
                for file in directory.rglob("*.json"):
                    if "localization-reference" in file.parts or file.stat().st_size > 10 * 1024 * 1024:
                        continue
                    if directory.name == "DressmakerMods" and "reference" in file.name:
                        continue  # Official items must keep the base game's localization.
                    visit(read_json(file, {}))
        # Offer only likely user-visible literals in the editor. Runtime collection is more precise.
        for source in loader_literals(game / "BepInEx/plugins/DressmakerMods.dll"):
            if source in self.dictionary or (" " in source and 4 <= len(source) <= 500 and not re.search(r"(?:https?://|[/\\]|\b(?:Exception|UnityEngine|System\.)|^Could not|^Registered|^Exported|^Loaded|\.dll|\.json)", source)):
                self.add_pending(source, "loader")
        for source in sources:
            self.add_pending(source, "content")
        with self.lock:
            existing = set(read_json(self.root / "known-sources.json", []))
            atomic_json(self.root / "known-sources.json", sorted(existing | sources))
            if self.installed:
                self.publish()
        return len(sources)

    def cache_get(self, source, language):
        with self.lock:
            return self.db.execute("SELECT value, provider FROM translations WHERE source=? AND language=?", (source, language)).fetchone()

    def cache_put(self, source, language, value, provider):
        validate(source, value)
        with self.lock:
            self.db.execute("INSERT OR REPLACE INTO translations VALUES (?,?,?,?,?)", (source, language, value, provider, datetime.datetime.utcnow().isoformat()))
            self.db.commit()

    def compose(self, source):
        # Require every word to be recognized. Do not cache half-translated names.
        lower = {k.lower(): v for k, v in self.dictionary.items() if len(k) < 80 and not PROTECTED.search(k)}
        parts = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|[^A-Za-z]+", source)
        words = [p for p in parts if re.search("[A-Za-z]", p)]
        if not words or len(words) > 10 or PROTECTED.search(source):
            return None
        if not all(word.lower() in lower for word in words):
            return None
        out = "".join(lower[p.lower()] if re.search("[A-Za-z]", p) else p for p in parts)
        if self.config["language"] in {"zh-CN", "ja", "ko"}:
            out = re.sub(r"(?<=[\u3000-\u9fff\uac00-\ud7af]) +(?=[\u3000-\u9fff\uac00-\ud7af])", "", out)
        return out

    def offline(self, source, language):
        try:
            import argostranslate.translate
        except ImportError:
            return None
        installed = argostranslate.translate.get_installed_languages()
        en = next((x for x in installed if x.code == "en"), None)
        target = next((x for x in installed if x.code == ARGOS_CODES.get(language)), None)
        if not en or not target:
            return None
        translator = en.get_translation(target)
        if translator is None:
            return None
        masked, tokens = protect(source)
        return restore(translator.translate(masked), tokens)

    def network(self, source, language, config=None):
        config = config or self.config.copy()
        # Serialise all public requests, including manual calls and fallback attempts.
        with self.network_lock:
            try:
                return self.network_once(source, language, config)
            except (ValueError, urllib.error.URLError, TimeoutError) as error:
                # Budget, input and format errors must never trigger another request.
                if not config.get("fallback") or config["provider"] == "mymemory" or isinstance(error, ValueError) and str(error) not in {"免费接口限额或暂不可用", "必应网页接口已变化或暂不可用"}:
                    raise
                fallback = dict(config, provider="mymemory", fallback=False)
                return self.network_once(source, language, fallback)

    def network_once(self, source, language, config):
        masked, tokens = protect(source)
        if len(masked.encode("utf-8")) > 500:
            raise ValueError("单条超过免费接口的 500 字节限制，请安装离线模型或手动翻译")
        if config["provider"] == "libre" and not config["libre_url"]:
            raise ValueError("请填写你可使用的 LibreTranslate HTTPS 地址")
        with self.lock:
            config = config or self.config.copy()
            day = datetime.datetime.utcnow().date().isoformat()
            row = self.db.execute("SELECT bytes FROM budget WHERE day=?", (day,)).fetchone()
            used = row[0] if row else 0
            size = len(masked.encode("utf-8"))
            if used + size > config["daily_bytes"]:
                raise ValueError("今日免费接口预算已用完；离线词典和缓存仍然可用")
            self.db.execute("INSERT OR REPLACE INTO budget VALUES (?,?)", (day, used + size))
            self.db.commit()
        delay = self.next_request - time.monotonic()
        if delay > 0:
            time.sleep(delay)
        self.next_request = time.monotonic() + 3
        if config["provider"] == "bing":
            result = self.bing.translate(masked, language)
        elif config["provider"] == "libre":
            reply = request_json(config["libre_url"].rstrip("/") + "/translate", {"q": masked, "source": "en", "target": ARGOS_CODES.get(language, language), "format": "text"})
            result = reply.get("translatedText", "")
        else:
            url = "https://api.mymemory.translated.net/get?" + urllib.parse.urlencode({"q": masked, "langpair": "en|" + language})
            reply = request_json(url)
            if str(reply.get("responseStatus")) != "200" or reply.get("quotaFinished"):
                raise ValueError("免费接口限额或暂不可用")
            result = html.unescape(reply.get("responseData", {}).get("translatedText", ""))
        return restore(result, tokens), config["provider"]

    def translate(self, source, config=None):
        # Hold configuration stable while a language change races with a network reply.
        with self.lock:
            config = config or self.config.copy()
            language = config["language"]
            cached = self.cache_get(source, language)
            if cached and cached[1] == "manual":
                return cached[0], "manual"
            dictionary = self.dictionary.copy() if language == self.config["language"] else read_json(self.bundle / "assistant/dictionary.json", {}).get(language, {})
            dictionary_value = dictionary.get(source)
            composed = self.compose(source) if language == self.config["language"] else None
        if language == "en":
            return source, "original"
        if dictionary_value:
            return dictionary_value, "dictionary"
        if cached:
            return cached[0], cached[1]
        if composed:
            self.cache_put(source, language, composed, "dictionary-composed")
            return composed, "dictionary-composed"
        if config.get("offline_model"):
            try:
                result = self.offline(source, language)
            except Exception as error:
                self.error = "离线模型未能翻译此条文本：" + str(error)
                result = None
            if result and result != source:
                self.cache_put(source, language, result, "argos-offline")
                return result, "argos-offline"
        if config.get("online"):
            result, provider = self.network(source, language, config)
            if result != source:
                self.cache_put(source, language, result, provider)
                return result, provider
        return source, "untranslated"

    def entries(self, query="", limit=500):
        with self.lock:
            language = self.config["language"]
            rows = self.db.execute("SELECT p.source,p.kind,t.value,t.provider FROM pending p LEFT JOIN translations t ON p.source=t.source AND t.language=? WHERE p.source LIKE ? ORDER BY CASE p.kind WHEN 'display' THEN 0 WHEN 'content' THEN 1 ELSE 2 END,p.source LIMIT ?", (language, "%" + query + "%", limit)).fetchall()
            return [{"source": src, "kind": kind, "value": self.dictionary.get(src, value or ""), "provider": "dictionary" if src in self.dictionary and provider != "manual" else (provider or ""), "manual": provider == "manual"} if provider != "manual" else {"source": src, "kind": kind, "value": value, "provider": provider, "manual": True} for src, kind, value, provider in rows]

    def runtime_snapshot(self):
        with self.lock:
            language = self.config["language"]
            values = self.dictionary.copy()
            values.update({s: v for s, v in self.db.execute("SELECT source,value FROM translations WHERE language=? AND provider='manual'", (language,))})
            for source, value in self.db.execute("SELECT source,value FROM translations WHERE language=? AND provider!='manual'", (language,)):
                values.setdefault(source, value)
            return language, values, read_json(self.root / "known-sources.json", [])

    def export_manual(self):
        with self.lock:
            language, values, sources = self.runtime_snapshot()
            return language, manual_archive(self.bundle, language, values, sources)

    def publish(self):
        with self.lock:
            language, values, sources = self.runtime_snapshot()
            atomic_json(self.plugin_data / ("translations." + language + ".json"), values)
            atomic_json(self.plugin_data / "known-sources.json", sources)
            atomic_json(self.plugin_data / "runtime.json", {"language": language})

    def installation_complete(self):
        language = self.config["language"]
        return ((self.game / "BepInEx/plugins/DressmakerLanguages/DressmakerLanguages.dll").is_file()
                and read_json(self.plugin_data / "runtime.json", {}).get("language") == language
                and (self.plugin_data / ("translations." + language + ".json")).is_file()
                and (self.plugin_data / "known-sources.json").is_file())

    def install(self):
        plugin = self.bundle / "BepInEx/plugins/DressmakerLanguages/DressmakerLanguages.dll"
        if not plugin.is_file():
            raise ValueError("缺少已编译的游戏插件")
        if not (self.game / "BepInEx/plugins/DressmakerMods.dll").is_file():
            raise ValueError("请先安装 Yuuma ModLoader 的 Mac 版")
        target = self.game / "BepInEx/plugins/DressmakerLanguages"
        backup = self.root / "backups" / datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        if target.exists():
            shutil.copytree(target, backup / "plugin")
        if self.plugin_data.exists():
            shutil.copytree(self.plugin_data, backup / "config")
        self.installed = False
        try:
            target.mkdir(parents=True, exist_ok=True)
            shutil.copy2(plugin, target / plugin.name)
            self.scan()
            self.publish()
            self.installed = True
        except Exception:
            self.installed = self.installation_complete()
            raise

    def uninstall(self):
        # Move only owned files into backups, retaining translations and all original mods.
        backup = self.root / "backups" / ("uninstall-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f"))
        backup.mkdir(parents=True, exist_ok=True)
        for path, name in [(self.game / "BepInEx/plugins/DressmakerLanguages", "plugin"), (self.plugin_data, "config")]:
            if path.exists():
                shutil.move(str(path), str(backup / name))
        self.installed = False

    def status(self):
        with self.lock:
            language = self.config["language"]
            total = self.db.execute("SELECT COUNT(*) FROM pending").fetchone()[0]
            cached = self.db.execute("SELECT COUNT(*) FROM translations WHERE language=?", (language,)).fetchone()[0]
            return {"config": self.config, "languages": LANGUAGES, "installed": self.installed, "pending": total, "cached": cached, "dictionary": len(self.dictionary), "error": self.error}

class Worker:
    def __init__(self, store):
        self.store = store
        self.stop = threading.Event()
        self.wake = threading.Event()
        self.offset = 0
        self.path = None
        self.cooldown = 0
        self.last_model_attempt = {}

    def ingest(self):
        path = self.store.plugin_data / "pending.jsonl"
        if path != self.path:
            self.path, self.offset = path, 0
        if not path.exists():
            return
        if path.stat().st_size < self.offset:
            self.offset = 0
        with path.open("rb") as file:
            file.seek(self.offset)
            for raw in file:
                if not raw.endswith(b"\n"):
                    break  # A writer may still be appending the last line.
                self.offset += len(raw)
                try:
                    self.store.add_pending(json.loads(raw.decode("utf-8"))["source"])
                except (ValueError, KeyError, UnicodeError):
                    pass

    def run(self):
        while not self.stop.is_set():
            try:
                self.ingest()
                with self.store.lock:
                    config = self.store.config.copy()
                if config.get("auto") or self.wake.is_set():
                    all_candidates = self.wake.is_set()
                    self.wake.clear()
                    for item in self.store.entries(limit=10000):
                        if self.stop.is_set():
                            break
                        if item["value"]:
                            continue
                        if item["kind"] == "loader" and not all_candidates:
                            continue  # Do not spend a free quota on invisible DLL literals.
                        key = (config["language"], item["source"])
                        if time.monotonic() - self.last_model_attempt.get(key, -3600) < 300:
                            continue
                        self.last_model_attempt[key] = time.monotonic()
                        attempt = config.copy()
                        if time.monotonic() < self.cooldown:
                            attempt["online"] = False
                        try:
                            value, provider = self.store.translate(item["source"], attempt)
                            if provider != "untranslated":
                                self.store.error = ""
                            if provider != "untranslated" and self.store.installed:
                                self.store.publish()
                            if provider in {"mymemory", "libre", "bing"}:
                                self.stop.wait(1.5)
                        except Exception as error:
                            self.store.error = str(error)
                            if attempt.get("online"):
                                self.cooldown = time.monotonic() + 300
                        if config != self.store.config:
                            break
            except Exception as error:
                self.store.error = str(error)
            self.stop.wait(2)
