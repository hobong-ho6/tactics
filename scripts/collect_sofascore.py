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
from core.aggregate import aggregate_rows  # noqa: E402
from core.kernel import Kernel  # noqa: E402
from core.sofascore import js_collect, parse_collected  # noqa: E402

ORIGIN = "https://www.sofascore.com/robots.txt"   # 동일 오리진 경량 페이지 (홈은 렌더러가 언다)

# 이식 회귀 앵커. 지정된 전체 구간·표본 기준으로 실행했을 때만 자동 검증한다.
# 일반 수집의 일부 구간을 고정 기대값과 잘못 비교하지 않기 위한 제한이다.
REGRESSION_ANCHORS = {
    (863653, "2025-08-01", "2026-08-13", 45, 15): {
        "label": "완비사카 RB",
        "competitions": {"Premier League", "FA Cup"},
        "regime_id": 1,
        "pos": "RB",
        "n": 25,
        "map25": "000140002X001290003900234",
        "role": "fb_att_wb",
        "focus": "Support",
        "sim": 0.932,
    },
}


def collect(player_id, date_from, date_to, pages=3, timeout_ms=180_000):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(ORIGIN, wait_until="domcontentloaded")
        page.evaluate("() => {%s}" % js_collect(player_id, date_from, date_to, pages))
        page.wait_for_function("() => window.__DONE === 1", timeout=timeout_ms)
        raw = page.evaluate("() => window.__SER()")
        diag = json.loads(page.evaluate("() => window.__DIAG_SER()"))
        browser.close()
    page_states = diag.get("pages", [])
    if page_states and not any(
            isinstance(item.get("status"), int) and 200 <= item["status"] < 300
            for item in page_states):
        states = ", ".join(
            f"page {item.get('page')}={item.get('status') or item.get('error', 'ERROR')}"
            for item in page_states)
        raise RuntimeError(f"SofaScore 경기목록 접근 실패 — {states}")
    return parse_collected(raw) if raw.strip() else []


def verify_regression_anchor(player_id, date_from, date_to, min_minutes, min_hp, rows):
    """문서화된 이식 앵커를 core 집계·커널로 재현한다. 해당 명령이 아니면 no-op."""
    anchor = REGRESSION_ANCHORS.get(
        (player_id, date_from, date_to, min_minutes, min_hp))
    if not anchor:
        return

    sample = [r for r in rows if r["competition"] in anchor["competitions"]]
    agg = aggregate_rows([
        (r["cells"], r["rating"], r["minutes"], r["avg_x"], r["avg_y"])
        for r in sample
    ])
    if not agg:
        raise SystemExit(f"⛔ {anchor['label']} 회귀 실패 — 집계 표본 부족")

    role, focus, sim = Kernel("FC26").best_fit_slot(
        agg["map25"], anchor["regime_id"], anchor["pos"])
    ok = (
        agg["n"] == anchor["n"]
        and agg["map25"] == anchor["map25"]
        and role == anchor["role"]
        and focus == anchor["focus"]
        and round(sim, 3) == anchor["sim"]
    )
    result = (
        f"{anchor['label']} {agg['n']}경기 · {role}/{focus} · "
        f"{anchor['pos']} 적합 {sim:.3f}"
    )
    if not ok:
        raise SystemExit(f"⛔ 이식 회귀 실패 — {result} · map25={agg['map25']}")
    print(f"✅ 이식 회귀 통과 — {result}", file=sys.stderr)


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

    try:
        rows = collect(a.player_id, a.date_from, a.date_to, a.pages)
    except RuntimeError as exc:
        raise SystemExit(f"⛔ {exc}") from exc
    kept = [r for r in rows
            if (r["minutes"] or 0) >= a.min_minutes and r["hit_points"] >= a.min_hp]

    verify_regression_anchor(
        a.player_id, a.date_from, a.date_to, a.min_minutes, a.min_hp, kept)

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
