import argparse
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import threading
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from core import Store, Worker, LANGUAGES, atomic_json
from i18n import error_info

BUNDLE = Path(__file__).resolve().parent.parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=str(BUNDLE / "data"))
    parser.add_argument("--port", type=int, default=8788)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    store = Store(args.data, BUNDLE)
    store.installed = store.installation_complete()
    worker = Worker(store)
    session = secrets.token_urlsafe(32)
    model_job = {"running": False, "state": "idle", "detail": ""}

    def setup_model(language):
        model_job.update(running=True, state="installing", detail="")
        try:
            env = BUNDLE / ".venv"
            python = env / "bin/python3"
            with (store.root / "model-install.log").open("w") as log:
                if not python.exists():
                    subprocess.run([sys.executable, "-m", "venv", str(env)], check=True, stdout=log, stderr=log, timeout=120)
                subprocess.run([str(python), "-m", "pip", "install", "argostranslate==1.9.6"], check=True, stdout=log, stderr=log, timeout=1200)
                subprocess.run([str(python), str(BUNDLE / "assistant/install_model.py"), language, str(BUNDLE / "models")], check=True, stdout=log, stderr=log, timeout=1800)
            model_job.update(state="done", detail="")
        except Exception as error:
            model_job.update(state="failed", detail=str(error))
        finally:
            model_job["running"] = False

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, code, data, content_type="application/json; charset=utf-8", headers=None):
            if isinstance(data, dict) and data.get("error") and "error_info" not in data:
                data["error_info"] = error_info(data["error"])
            raw = data if isinstance(data, bytes) else json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            for key, value in (headers or {}).items():
                self.send_header(key, value)
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(raw)

        def authenticated(self):
            host = self.headers.get("Host", "")
            allowed = {"127.0.0.1:%d" % self.server.server_port, "localhost:%d" % self.server.server_port}
            if host not in allowed:
                return False
            token = self.headers.get("X-Session", "")
            cookie = self.headers.get("Cookie", "")
            cookies = dict(part.strip().split("=", 1) for part in cookie.split(";") if "=" in part)
            return secrets.compare_digest(token or cookies.get("session", ""), session)

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/":
                query = urllib.parse.parse_qs(parsed.query)
                if query.get("session", [""])[0] != session and not self.authenticated():
                    return self.reply(403, {"error": "请使用启动助手打开的链接"})
                catalogs = (BUNDLE / "assistant/locales.json").read_text(encoding="utf-8").replace("<", "\\u003c")
                page = (BUNDLE / "assistant/index.html").read_text(encoding="utf-8").replace("__SESSION__", session).replace("__I18N__", catalogs)
                raw = page.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(raw)))
                self.send_header("Set-Cookie", "session=%s; HttpOnly; SameSite=Strict; Path=/" % session)
                self.send_header("Cache-Control", "no-store")
                self.send_header("Referrer-Policy", "no-referrer")
                self.send_header("X-Frame-Options", "DENY")
                self.end_headers()
                self.wfile.write(raw)
                return
            if not self.authenticated():
                return self.reply(403, {"error": "会话无效"})
            if parsed.path.startswith("/docs/"):
                language = parsed.path[len("/docs/"):].removesuffix(".md") if hasattr(str, "removesuffix") else parsed.path[len("/docs/"):-3]
                locale = language[len("manual-"):] if language.startswith("manual-") else language
                if locale not in LANGUAGES or parsed.path != "/docs/" + language + ".md":
                    return self.reply(404, {"error": "未找到页面"})
                path = BUNDLE / "docs" / (language + ".md")
                if not path.is_file():
                    return self.reply(404, {"error": "未找到页面"})
                return self.reply(200, path.read_bytes(), "text/plain; charset=utf-8")
            if parsed.path == "/api/status":
                status = store.status()
                status["error_info"] = error_info(status.get("error", ""))
                status["model"] = model_job.copy()
                status["progress"] = worker.progress.snapshot()
                return self.reply(200, status)
            if parsed.path == "/api/manual-package":
                try:
                    language, archive = store.export_manual()
                    version = (BUNDLE / "VERSION").read_text().strip()
                    name = "Dressmaker-Languages-Manual-%s-%s.zip" % (language, version)
                    return self.reply(200, archive, "application/zip", {"Content-Disposition": 'attachment; filename="' + name + '"'})
                except Exception as error:
                    return self.reply(400, {"error": str(error), "error_info": error_info(error)})
            if parsed.path == "/api/entries":
                try:
                    params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
                    def param(key, default):
                        return params.get(key, [default])[0]
                    try:
                        page, page_size = int(param("page", "1")), int(param("page_size", "50"))
                    except ValueError:
                        raise ValueError("无效的词典筛选条件") from None
                    result = store.browse_entries(param("q", ""), param("state", "all"),
                                                 param("provider", "all"), param("kind", "all"),
                                                 param("order", "source"), page, page_size)
                    return self.reply(200, result)
                except Exception as error:
                    return self.reply(400, {"error": str(error), "error_info": error_info(error)})
            return self.reply(404, {"error": "未找到页面"})

        def do_POST(self):
            if not self.authenticated() or not secrets.compare_digest(self.headers.get("X-Session", ""), session):
                return self.reply(403, {"error": "会话无效"})
            origin = self.headers.get("Origin")
            if origin and origin not in {"http://127.0.0.1:%d" % self.server.server_port, "http://localhost:%d" % self.server.server_port}:
                return self.reply(403, {"error": "禁止跨站请求"})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length < 0 or length > 100000:
                    raise ValueError("请求内容过大")
                data = json.loads(self.rfile.read(length) or b"{}")
                if self.path == "/api/settings":
                    store.save_config(data)
                    worker.last_model_attempt.clear()
                    worker.cooldown = 0
                elif self.path == "/api/scan":
                    store.scan()
                elif self.path == "/api/translate":
                    worker.request_translation()
                elif self.path == "/api/save":
                    with store.lock:
                        if data.get("language", store.config["language"]) != store.config["language"]:
                            raise ValueError("目标语言已更改，请刷新列表后保存")
                        store.cache_put(data["source"], store.config["language"], data["value"], "manual")
                        if store.installed:
                            store.publish()
                elif self.path == "/api/install":
                    store.install()
                elif self.path == "/api/uninstall":
                    store.uninstall()
                elif self.path == "/api/model":
                    language = data.get("language", store.config["language"])
                    if language not in LANGUAGES or language == "en":
                        raise ValueError("请选择要安装模型的目标语言")
                    if model_job["running"]:
                        raise ValueError("已有模型正在安装")
                    model_job["running"] = True
                    threading.Thread(target=setup_model, args=(language,), daemon=True).start()
                elif self.path == "/api/shutdown":
                    worker.stop.set()
                    threading.Thread(target=self.server.shutdown, daemon=True).start()
                else:
                    return self.reply(404, {"error": "未知操作"})
                return self.reply(200, {"ok": True})
            except Exception as error:
                return self.reply(400, {"error": str(error), "error_info": error_info(error)})

    server = None
    for port in range(args.port, args.port + 10):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
            break
        except PermissionError as error:
            raise RuntimeError("Local network access is required to start the assistant.") from error
        except OSError:
            pass
    if server is None:
        raise RuntimeError("8788–8797 端口均被占用")
    url = "http://127.0.0.1:%d/?session=%s" % (server.server_port, session)
    atomic_json(store.root / "session.json", {"url": url, "pid": os.getpid()})
    print("针影裁梦多语言助手已启动：" + url, flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    thread = threading.Thread(target=worker.run, daemon=True)
    thread.start()
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        worker.stop.set()
        server.server_close()

if __name__ == "__main__":
    main()
