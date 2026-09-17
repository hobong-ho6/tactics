#!/usr/bin/env python3
"""관리 선수 카드 시세 스냅샷 — fut.gg 목록 API (2026-09-18 신설, migration 037).

왜 (사용자 지시 「제한된 자원에서 누구를 먼저 사야 하는지 등 선수 가격 정보까지」):
  구매 우선순위는 처방 역할(전술 필요)과 시세(자원)의 대조다. 시세는 매일 움직이므로 날짜별 스냅샷으로 쌓고
  화면이 최신값을 읽는다. ⛔ 우선순위 판정은 여기서 하지 않는다.

원천: `/api/fut/players/v2/{game}/?ea_ids=…`(40개씩) — `currentDbPrice`·`hasPrice`·`momentumPercentage`.
  전용 가격 API(`/api/fut/player-prices/`)는 Cloudflare 403이라 쓰지 않는다.
  ⚠️ 시장이 열리기 전에는 hasPrice=0 → price NULL로 적재한다(「미형성」이지 0이 아니다).

사용:
    .venv/bin/python scripts/collect_futgg_prices.py --games 27
"""
import argparse
import datetime as dt
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DB = ROOT / "db" / "tactics.db"
from scripts.collect_futgg_history import API, get   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", nargs="*", default=["27"])
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    a = ap.parse_args()
    con = sqlite3.connect(DB)
    for g in a.games:
        gv = f"FC{g}"
        items = con.execute("SELECT ea_item_id, player_id FROM player_card_items WHERE game_version=? ORDER BY ea_item_id", (gv,)).fetchall()
        ids = [i for i, _ in items]
        pid = dict(items)
        rows, priced = [], 0
        for i in range(0, len(ids), 40):
            d = get(f"{API}/players/v2/{g}/?ea_ids=" + ",".join(map(str, ids[i:i + 40])))
            for x in (d or {}).get("data", []):
                has = 1 if x.get("hasPrice") else 0
                price = x.get("currentDbPrice") if has else None
                priced += has
                rows.append((gv, x["eaId"], pid.get(x["eaId"]), price, has, x.get("momentumPercentage"), "console",
                             f"fut.gg {API}/players/v2/{g}/?ea_ids=… currentDbPrice ({a.pulled} 수집, collect_futgg_prices.py)",
                             "MEDIUM — fut.gg 집계 시세(콘솔 기본). hasPrice=0이면 시장 미형성이라 NULL." , a.pulled))
        con.executemany("""INSERT INTO player_card_prices(game_version, ea_item_id, player_id, price, has_price, momentum, platform,
                             source, confidence, pulled) VALUES(?,?,?,?,?,?,?,?,?,?)
                           ON CONFLICT(game_version, ea_item_id, platform, pulled) DO UPDATE SET
                             price=excluded.price, has_price=excluded.has_price, momentum=excluded.momentum""", rows)
        con.commit()
        print(f"{gv}: 카드 {len(ids)}장 조회 → {len(rows)}행 적재 · 시세 있음 {priced}장 · 미형성 {len(rows) - priced}장 (pulled {a.pulled})")
    print("\n다음: python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
