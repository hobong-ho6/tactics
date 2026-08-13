#!/usr/bin/env python3
"""SofaScore 실측 수집 — 브라우저 MCP 없이 셸에서 실행 (Codex CLI·cron·Claude Code 공용).

왜 Playwright인가: SofaScore API는 sofascore.com 오리진에서만 열린다(curl은 UA/Referer를
붙여도 403 — docs/30 ②). 지금까지는 에이전트의 브라우저 툴로 오리진 JS를 돌렸는데,
그 툴이 없는 실행 환경(Codex CLI 등)에서는 재현이 불가능했다. Playwright의 실제
Chromium을 같은 오리진에 띄우면 동일한 fetch가 그대로 통한다(2026-08-13 검증).

수집 JS는 `core.sofascore.js_collect`를 그대로 쓴다 — 세션 내 재구현 금지(불변규칙 4).

사용:
    .venv/bin/python scripts/collect_sofascore.py 863653 --from 2025-08-01 --to 2026-08-13
    ... --out /tmp/rows.json      # 파싱된 행을 JSON으로 저장
    ... --min-minutes 45 --min-hp 15   # §3 표본 기준으로 걸러서 출력
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.sofascore import js_collect, parse_collected  # noqa: E402

ORIGIN = "https://www.sofascore.com/robots.txt"   # 동일 오리진 경량 페이지 (홈은 렌더러가 언다)


def collect(player_id, date_from, date_to, pages=3, timeout_ms=180_000):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(ORIGIN, wait_until="domcontentloaded")
        page.evaluate("() => {%s}" % js_collect(player_id, date_from, date_to, pages))
        page.wait_for_function("() => window.__DONE === 1", timeout=timeout_ms)
        raw = page.evaluate("() => window.__SER()")
        browser.close()
    return parse_collected(raw) if raw.strip() else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("player_id", type=int, help="SofaScore player id")
    ap.add_argument("--from", dest="date_from", required=True)
    ap.add_argument("--to", dest="date_to", required=True)
    ap.add_argument("--pages", type=int, default=3, help="events/last 페이지 수 (기본 3)")
    ap.add_argument("--min-minutes", type=int, default=0)
    ap.add_argument("--min-hp", type=int, default=0)
    ap.add_argument("--out")
    a = ap.parse_args()

    rows = collect(a.player_id, a.date_from, a.date_to, a.pages)
    kept = [r for r in rows
            if (r["minutes"] or 0) >= a.min_minutes and r["hit_points"] >= a.min_hp]

    print(f"수집 {len(rows)}경기 → 기준 통과 {len(kept)}경기 "
          f"(45분+ 기준 {a.min_minutes} · 히트포인트 {a.min_hp})", file=sys.stderr)
    payload = json.dumps(kept, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).write_text(payload, encoding="utf-8")
        print(a.out, file=sys.stderr)
    else:
        print(payload)


if __name__ == "__main__":
    main()
