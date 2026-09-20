#!/usr/bin/env python3
"""보유 카드의 fut.gg 케미 스타일 신호 수집 (2026-09-21 신설, 사용자 지시).

무엇을 받나 — fut.gg 선수 페이지의 케미 스타일 격자에서 스타일 19종마다:
  ⑴ **AcceleRATE 배지**(C/E/L) — 그 스타일을 붙였을 때의 가속 타입.
     ⚠️ 이것은 「케미 등급」이 아니다(2026-09-21 실측 확정 — migration 055 주석).
  ⑵ **커뮤니티 투표 비율**(%) — 투표가 있는 스타일만. 없으면 NULL(0이 아니다).

⭐ Playwright로 **셸에서 직접** 돈다 — 브라우저 MCP도 에이전트 컨텍스트도 거치지 않는다
   (docs/30: 브라우저→localhost 전송이 ERR_BLOCKED_BY_CLIENT로 막혀 1,285행을 컨텍스트로 나른 전례).
⛔ curl·WebFetch로는 안 된다 — 이 격자는 클라이언트 렌더라 정적 HTML에 없다.
⚠️ fut.gg에 부담을 주지 않도록 페이지마다 쉰다. 로그인은 필요 없다(공개 페이지).

사용:
    .venv/bin/python scripts/collect_futgg_chem.py --dry-run
    .venv/bin/python scripts/collect_futgg_chem.py                # 보유 전체
    .venv/bin/python scripts/collect_futgg_chem.py --items 236987 227174
"""
import argparse
import datetime as dt
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DB = ROOT / "db" / "tactics.db"

ACCEL = {"C": "Controlled", "E": "Explosive", "L": "Lengthy"}

# 페이지에서 격자와 투표 목록을 한 번에 뽑는다. 구조는 2026-09-21 실측(div.rounded 타일 + 투표 바).
JS = """() => {
  const out = {tiles: [], votes: [], accel: null};
  const t = document.body.innerText.replace(/\\s+/g, ' ');
  const m = t.match(/AcceleRATE\\s+(\\w+)/);
  out.accel = m ? m[1] : null;
  /* ⚠️ 'Basic' 이름으로 격자를 찾으면 **골키퍼를 통째로 놓친다**(2026-09-21 실증: 11장 전부 GK 실패).
     GK 페이지의 스타일은 `GK Basic · Wall · Glove · Shield · Cat` 5종이다.
     이름이 아니라 **구조**(이름 p + C/E/L 배지)로 타일을 찾는다 — 필드·GK 양쪽에 통한다. */
  const tiles = [...document.querySelectorAll('div.rounded')].filter(d =>
    d.querySelector('p') && d.lastElementChild && /^[CEL]$/.test((d.lastElementChild.textContent || '').trim()));
  if (tiles.length) {
    const grid = tiles[0].parentElement;
    out.tiles = [...grid.children].map(x => {
      const p = x.querySelector('p'), b = x.lastElementChild;
      return [p ? p.textContent.trim() : null, b ? b.textContent.trim() : null];
    }).filter(r => r[0]);
  }
  // 투표 바 — 「이름 … 45%」 행. 퍼센트 span이 있는 행만 센다.
  for (const row of document.querySelectorAll('div.flex.flex-row.items-center.gap-2')) {
    const spans = row.querySelectorAll('span');
    if (spans.length < 3) continue;
    const pct = [...spans].map(s => s.textContent.trim()).find(v => /^\\d+(\\.\\d+)?%$/.test(v));
    if (!pct) continue;
    const name = [...spans].map(s => s.textContent.trim())
      .find(v => v && !/%$/.test(v) && /^[A-Za-z][A-Za-z .'-]*$/.test(v));
    if (name) out.votes.push([name, parseFloat(pct)]);
  }
  return out;
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", nargs="*", type=int, default=[], help="ea_item_id 한정")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--sleep", type=float, default=1.2)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    q = """SELECT c.ea_item_id, c.name, i.futgg_url
             FROM fut_club_players c
             LEFT JOIN player_card_items i ON i.ea_item_id = c.ea_item_id
            WHERE c.status='owned'"""
    rows = [r for r in con.execute(q)]
    if a.items:
        rows = [r for r in rows if r["ea_item_id"] in a.items]
    todo = [r for r in rows if r["futgg_url"]]
    missing = [r["name"] for r in rows if not r["futgg_url"]]
    print(f"대상 {len(todo)}장 · futgg_url 결손 {len(missing)}장" + (f" ({', '.join(missing)})" if missing else ""))
    if a.dry_run:
        return

    from playwright.sync_api import sync_playwright

    ins, skipped, novote = 0, [], 0
    SRC = f"fut.gg 선수 페이지 케미 스타일 격자 직독 (Playwright, {a.pulled})"
    CONF = ("MEASURED(fut.gg 표기). ⚠️ 배지는 **등급이 아니라 그 스타일 적용 시 AcceleRATE**다 "
            "(2026-09-21 실측 확정: 카마라 전 스타일 C=Controlled · 음바페 대부분 E=Explosive). "
            "⚠️ vote_pct는 **커뮤니티 투표 비율**이고 fut.gg 편집부 추천이 아니다 — 인기이지 정답이 아니다.")

    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page()
        for n, r in enumerate(todo, 1):
            url = "https://www.fut.gg" + r["futgg_url"]
            try:
                pg.goto(url, wait_until="domcontentloaded", timeout=60_000)
                pg.wait_for_timeout(2200)
                data = pg.evaluate(JS)
            except Exception as e:  # 한 장이 실패해도 나머지를 계속 받는다
                skipped.append((r["name"], str(e)[:60]))
                continue
            tiles = data.get("tiles") or []
            if not tiles:
                skipped.append((r["name"], "격자 없음"))
                continue
            votes = {k: v for k, v in (data.get("votes") or [])}
            if not votes:
                novote += 1
            for style, badge in tiles:
                con.execute(
                    """INSERT OR REPLACE INTO futgg_chem_signals
                       (ea_item_id, pulled, style_name, accelerate, vote_pct, source, confidence)
                       VALUES (?,?,?,?,?,?,?)""",
                    (r["ea_item_id"], a.pulled, style, ACCEL.get(badge), votes.get(style), SRC, CONF))
                ins += 1
            print(f"  [{n}/{len(todo)}] {r['name']:<20} 스타일 {len(tiles)} · 투표 {len(votes)} · 현재 {data.get('accel')}")
            time.sleep(a.sleep)
        br.close()
    con.commit()
    print(f"\n적재 {ins}행 · 투표 0건 카드 {novote}장 · 실패 {len(skipped)}장")
    for nm, why in skipped:
        print(f"  ⚠️ {nm}: {why}")


if __name__ == "__main__":
    main()
