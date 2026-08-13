#!/usr/bin/env python3
"""Fotmob 루머 목록 수집 — 브라우저 MCP 없이 셸에서 실행.

왜 Playwright인가: Fotmob 루머 표는 CSR이라 `WebFetch`/curl로는 셸만 받는다(2026-07-31 진단).
렌더링하는 클라이언트를 쓰면 그대로 풀린다.

⛔ 출력은 **리드 소스**다 — 이름·날짜 발굴에만 쓰고 **티어 근거로 쓰지 말 것**.
   Fotmob은 출처 라벨도 날짜 라벨도 틀린 전례가 있다(Watkins "Sky Sports" → 실제 터키 매체 /
   루헤리 "Today" → 실제 08-08). 티어 판정은 transfer-watch §2 원문 추적으로 별도 수행한다.

사용:
    .venv/bin/python scripts/fetch_fotmob.py AVL
    .venv/bin/python scripts/fetch_fotmob.py AVL CHE LIV
"""
import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "tactics.db"


def team_ids(codes):
    con = sqlite3.connect(DB)
    rows = dict(con.execute("SELECT code, fotmob_id FROM teams").fetchall())
    con.close()
    missing = [c for c in codes if not rows.get(c)]
    if missing:
        sys.exit(f"teams 테이블에 fotmob_id 없음: {missing}")
    return [(c, rows[c]) for c in codes]


def scrape(page, code, fotmob_id):
    page.goto(f"https://www.fotmob.com/rumours?teamIds={fotmob_id}",
              wait_until="networkidle", timeout=90_000)
    lines = [l.strip() for l in page.inner_text("main").split("\n") if l.strip()]
    # 헤더("Date")까지가 필터 UI, 그 뒤부터 루머 행이다.
    start = lines.index("Date") + 1 if "Date" in lines else 0
    return lines[start:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("codes", nargs="+", help="팀 코드 (AVL CHE LIV)")
    a = ap.parse_args()

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for code, fid in team_ids(a.codes):
            body = scrape(page, code, fid)
            print(f"\n═══ {code} (fotmob {fid}) — {len(body)}줄 ═══")
            print(" | ".join(body))
        browser.close()


if __name__ == "__main__":
    main()
