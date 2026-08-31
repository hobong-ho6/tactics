#!/usr/bin/env python3
"""경기 1건의 출전 선수 전원 실측을 수집해 JSON으로 저장 (match-watch §2 라운드 수집용).

collect_sofascore.py가 선수 축이라면 이쪽은 이벤트 축이다 — 라운드 수집은 라인업 전원이
대상이라 선수별 페이징이 필요 없다. 수집 JS는 `core.sofascore.js_event_collect`를 쓴다.

사용:
    .venv/bin/python scripts/collect_event.py 16363249 home --out /tmp/che_bri.json
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.sofascore import js_event_collect  # noqa: E402

ORIGIN = "https://www.sofascore.com/robots.txt"   # 동일 오리진 경량 페이지


def collect(event_id, side, timeout_ms=180_000):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(ORIGIN, wait_until="domcontentloaded")
        page.evaluate("() => {%s}" % js_event_collect(event_id, side))
        page.wait_for_function("() => window.__EV_DONE === 1", timeout=timeout_ms)
        data = json.loads(page.evaluate("() => window.__EV_SER()"))
        browser.close()
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("event_id", type=int)
    ap.add_argument("side", choices=["home", "away"], help="우리 팀이 어느 쪽인가")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    data = collect(a.event_id, a.side)
    Path(a.out).write_text(json.dumps(data, ensure_ascii=False, indent=1))
    print(f"{a.event_id} {data['home']} {data['score']} {data['away']} — "
          f"출전 {len(data['players'])}명 → {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
