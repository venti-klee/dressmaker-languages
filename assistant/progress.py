"""Thread-safe, in-memory translation activity; snapshots never wait on the model or API."""
import copy
import threading
import time
from i18n import error_info


class TranslationProgress:
    def __init__(self):
        self.lock = threading.Lock()
        self.data = dict(state="idle", active=False, batch=0, language=None, total=0,
                         processed=0, translated=0, untranslated=0, failed=0,
                         current="", provider="lookup", wait_until=0, started_at=0,
                         ended_at=0, recent=[], error_info=None, retry=False)

    def queue(self, language):
        with self.lock:
            if self.data["active"]:
                return False
            self.data.update(state="queued", active=True, language=language,
                             current="", provider="lookup", wait_until=0, error_info=None,
                             total=0, processed=0, translated=0, untranslated=0, failed=0,
                             started_at=0, ended_at=0, retry=False)
            return True

    def begin(self, language, total):
        with self.lock:
            batch = self.data["batch"] + 1
            self.data.update(state="running", active=True, batch=batch, language=language,
                             total=total, processed=0, translated=0, untranslated=0, failed=0,
                             current="", provider="lookup", wait_until=0, started_at=time.time(),
                             ended_at=0, error_info=None, retry=False)

    def current(self, source):
        with self.lock:
            self.data.update(state="running", current=source, provider="lookup", wait_until=0)

    def stage(self, phase, provider, wait_until=0):
        with self.lock:
            self.data.update(state="waiting" if phase == "waiting" else "running",
                             provider=provider, wait_until=wait_until)

    def record(self, source, value, provider, outcome, error=None):
        with self.lock:
            self.data["processed"] += 1
            self.data[{"success": "translated", "untranslated": "untranslated", "failed": "failed"}[outcome]] += 1
            info = error_info(error) if error else None
            self.data["error_info"] = info or self.data["error_info"]
            self.data["recent"].insert(0, dict(source=source, value=value, provider=provider,
                                              outcome=outcome, error_info=info, language=self.data["language"]))
            del self.data["recent"][10:]
            self.data.update(current="", wait_until=0)

    def finish(self, state="finished", wait_until=0, error=None, retry=False):
        with self.lock:
            self.data.update(state=state, active=False, current="", wait_until=wait_until, ended_at=time.time(), retry=retry)
            if error:
                self.data["error_info"] = error_info(error)

    def snapshot(self):
        with self.lock:
            result = copy.deepcopy(self.data)
        if result["state"] == "cooldown" and result["wait_until"] <= time.time():
            result.update(state="queued" if result["retry"] else "finished", active=result["retry"], wait_until=0)
        result["remaining"] = max(0, result["total"] - result["processed"])
        result["elapsed"] = max(0, (result["ended_at"] or time.time()) - result["started_at"]) if result["started_at"] else 0
        return result
