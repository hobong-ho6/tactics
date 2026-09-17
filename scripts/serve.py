#!/usr/bin/env python3
"""Serve the exported site locally without browser or intermediary caches."""

from argparse import ArgumentParser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import io
import json
import sqlite3
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # The site is a live view of generated JSON. A stale response can make
        # the UI disagree with db/tactics.db, so local previews never cache.
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    # ── 내 구단 원장 쓰기 API (2026-09-18, 사용자 지시 「내 얼티밋 팀을 관리할 수 있어야 해」) ──
    # POST /api/fut/<account|player|player_set|evolve>  body=JSON(fut_club.run의 kw)
    # ⭐ 페이지가 DB를 직접 고치지 않는다 — scripts/fut_club.py와 **같은 함수**로 db/tactics.db에 쓰고
    #    곧바로 scripts/export.py(게이트 강제)를 돌려 site/data와 프리뷰 미러를 재생성한다(불변규칙 1·4·5).
    #    localhost 프리뷰 전용이다 — 정적 배포본에는 이 경로가 없고 화면이 CLI 명령을 대신 보여준다.
    def do_POST(self):
        if not self.path.startswith("/api/fut/"):
            self.send_error(404); return
        cmd = self.path[len("/api/fut/"):].strip("/")
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        from scripts import fut_club
        from core import DB
        out = io.StringIO()
        try:
            con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
            con.execute("PRAGMA foreign_keys=ON")
            with redirect_stdout(out):
                fut_club.run(con, cmd, **body)
            con.commit(); con.close()
            exp = subprocess.run([sys.executable, str(ROOT / "scripts" / "export.py")], capture_output=True, text=True, cwd=ROOT)
            ok = exp.returncode == 0
            msg = out.getvalue().strip() + ("" if ok else "\n⛔ export 실패:\n" + exp.stdout[-800:] + exp.stderr[-800:])
        except (SystemExit, Exception) as e:      # noqa: BLE001 — 사용자에게 사유를 그대로 보여준다
            ok, msg = False, out.getvalue().strip() + "\n" + str(e)
        data = json.dumps({"ok": ok, "message": msg}, ensure_ascii=False).encode("utf-8")
        self.send_response(200 if ok else 400)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)


def main():
    parser = ArgumentParser()
    parser.add_argument("--directory", required=True)
    parser.add_argument("--port", type=int, default=8123)
    parser.add_argument("--bind", default="127.0.0.1")
    args = parser.parse_args()

    handler = partial(NoCacheHandler, directory=args.directory)
    server = ThreadingHTTPServer((args.bind, args.port), handler)
    print(
        f"Serving {args.directory} at http://{args.bind}:{args.port} "
        "(cache disabled)",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
