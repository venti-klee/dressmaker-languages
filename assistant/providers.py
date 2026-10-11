"""Optional public webpage adapters. No login, proxy rotation or challenge bypass."""
import http.cookiejar
import json
import re
import threading
import time
import urllib.parse
import urllib.request

SERVICE_ERROR = "免费接口限额或暂不可用"
BING_PAGE_ERROR = "必应网页接口已变化或暂不可用"
GOOGLE_PAGE_ERROR = "Google 网页接口已变化或暂不可用"
MAX_RESPONSE = 2 * 1024 * 1024


class GoogleWeb:
    """Experimental public web endpoint. No accounts, keys or challenge bypass."""
    ENDPOINT = "https://translate.googleapis.com/translate_a/single"

    def read(self, request):
        with urllib.request.urlopen(request, timeout=15) as response:
            if urllib.parse.urlparse(response.url).hostname != "translate.googleapis.com":
                raise ValueError(GOOGLE_PAGE_ERROR)
            raw = response.read(MAX_RESPONSE + 1)
            if len(raw) > MAX_RESPONSE:
                raise ValueError("接口返回内容过大")
            return raw.decode("utf-8")

    def translate(self, text, language):
        query = urllib.parse.urlencode({"client": "gtx", "sl": "en", "tl": language,
                                       "dt": "t", "q": text})
        request = urllib.request.Request(self.ENDPOINT + "?" + query, headers={
            "User-Agent": "Mozilla/5.0 (compatible; DressmakerLanguages/0.1.3)",
            "Accept": "application/json", "Referer": "https://translate.google.com/"})
        try:
            reply = json.loads(self.read(request))
            if not isinstance(reply, list) or not reply or not isinstance(reply[0], list) or not reply[0]:
                raise ValueError()
            parts = reply[0]
            if any(not isinstance(part, list) or len(part) < 2 or not isinstance(part[0], str)
                   or not isinstance(part[1], str) for part in parts):
                raise ValueError()
            # Reject partial replies instead of caching a truncated translation.
            if "".join(part[1] for part in parts) != text:
                raise ValueError()
            translated = "".join(part[0] for part in parts)
            if not translated.strip():
                raise ValueError()
            return translated
        except (ValueError, KeyError, IndexError, TypeError):
            raise ValueError(GOOGLE_PAGE_ERROR) from None


class BingWeb:
    PAGE = "https://www.bing.com/translator"

    def __init__(self):
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.lock = threading.Lock()
        self.session = None
        self.expires = 0
        self.sequence = 0

    def read(self, request):
        with self.opener.open(request, timeout=15) as response:
            # Never continue from a login/challenge or another site's redirect.
            if urllib.parse.urlparse(response.url).hostname != "www.bing.com":
                raise ValueError(BING_PAGE_ERROR)
            raw = response.read(MAX_RESPONSE + 1)
            if len(raw) > MAX_RESPONSE:
                raise ValueError("接口返回内容过大")
            return raw.decode("utf-8")

    @staticmethod
    def parse_session(page):
        ig = re.search(r'\bIG:\s*"([A-Za-z0-9]+)"', page)
        iid = re.search(r'data-iid="([A-Za-z0-9_.-]+)"', page)
        params = re.search(r'params_AbusePreventionHelper\s*=\s*(\[[^\]\n]+\])', page)
        try:
            key, token, expiry_ms = json.loads(params.group(1))
            if not ig or not iid or not isinstance(key, int) or not isinstance(token, str) or not token or not isinstance(expiry_ms, (int, float)) or expiry_ms <= 0:
                raise ValueError()
            return {"IG": ig.group(1), "IID": iid.group(1), "key": key,
                    "token": token, "ttl": min(expiry_ms / 1000, 3600)}
        except (AttributeError, ValueError, TypeError):
            raise ValueError(BING_PAGE_ERROR) from None

    def translate(self, text, language):
        target = "zh-Hans" if language == "zh-CN" else language
        headers = {"User-Agent": "Mozilla/5.0 (compatible; DressmakerLanguages/0.1.3)",
                   "Accept": "text/html"}
        with self.lock:
            if not self.session or time.monotonic() >= self.expires:
                page = self.read(urllib.request.Request(self.PAGE, headers=headers))
                self.session = self.parse_session(page)
                self.expires = time.monotonic() + max(1, self.session["ttl"] - 30)
                self.sequence = 0
            self.sequence += 1
            session = self.session
            query = urllib.parse.urlencode({"isVertical": "1", "IG": session["IG"],
                                           "IID": session["IID"] + "." + str(self.sequence)})
            body = urllib.parse.urlencode({"fromLang": "en", "text": text, "to": target,
                                          "key": session["key"], "token": session["token"]}).encode()
            headers.update({"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded",
                            "Referer": self.PAGE})
            raw = self.read(urllib.request.Request("https://www.bing.com/ttranslatev3?" + query,
                                                  data=body, headers=headers))
            try:
                reply = json.loads(raw)
                values = reply[0]["translations"]
                translated = next(x["text"] for x in values if x.get("to", "").lower() == target.lower())
                if not isinstance(translated, str) or not translated.strip():
                    raise ValueError()
                return translated
            except (ValueError, KeyError, IndexError, TypeError, StopIteration):
                # Do not save HTML, rate-limit messages or malformed replies as translations.
                raise ValueError(SERVICE_ERROR) from None
