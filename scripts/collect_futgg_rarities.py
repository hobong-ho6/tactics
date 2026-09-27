#!/usr/bin/env python3
"""레어도 판(카드 틀) 자산 수집 — 브론즈/실버/골드 3단계 (2026-09-27 신설, migration 084).

왜 (사용자 지시 「진화해서 금카가 된 건 금카로 카드 이미지도 바꿔줘」):
  ⛔⛔ **진화 카드의 완성 이미지는 어디에도 없다**(실측). `paths/v2`의 단계별 카드는
     OVR 65와 75가 **같은 이미지 파일**을 가리키고, GG Club은 아이템 id를 **base 그대로** 준다.
  ⭐ fut.gg 화면이 골드로 보이는 건 **클라이언트가 합성**하기 때문이다 —
     빈 판 + 선수 렌더(`player-item/`) + 텍스트·로고. 판은 `rarity.imageUrls`에 **3단계 배열**로 온다.
  ⇒ 그 판을 받아 두면 우리도 같은 방식으로 그릴 수 있다.

원천: `/api/fut/players/v2/all-versions/{base_ea_id}/` 응답의 `rarity` 객체.
  ⚠️ 전용 레어도 API는 없다(`/api/fut/rarities/`는 404). 그래서 **우리가 이미 가진 카드들**의
     응답에서 훑어 모은다 — 보유·관리 4팀 카드가 쓰는 레어도면 충분하다.
  ⭐ 못 받은 레어도는 **그냥 없는 것**으로 둔다(화면이 기존 방식으로 물러선다). 지어내지 않는다.

사용:
    .venv/bin/python scripts/collect_futgg_rarities.py --games 27
"""
import argparse
import datetime as dt
import json
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DB = ROOT / "db" / "tactics.db"
from scripts.collect_futgg_history import API, get   # noqa: E402


def rows_from(rar, gv, pulled, src):
    """`rarity` 객체 → level별 행. ⚠️ 배열이 3개면 1·2·3, 하나뿐이면 level 3만 채운다."""
    urls = rar.get("imageUrls") or ([rar["imageUrl"]] if rar.get("imageUrl") else [])
    comp = rar.get("compactImageUrls") or ([rar["compactImageUrl"]] if rar.get("compactImageUrl") else [])
    line = rar.get("lineColor") or []
    text = rar.get("textColor") or []
    if not urls:
        return []
    pick = lambda a, i: (a[i] if isinstance(a, list) and len(a) > i else (a if isinstance(a, str) else None))  # noqa: E731
    out = []
    n = len(urls)
    for i in range(n):
        level = i + 1 if n == 3 else 3          # 한 장뿐이면 특별 카드 — 골드 자리에 둔다
        out.append((gv, rar.get("eaId"), rar.get("name"), level,
                    urls[i], pick(comp, i), pick(line, i), pick(text, i),
                    rar.get("dominantColor"), 1 if rar.get("isSpecial") else 0, pulled, src,
                    "HIGH — fut.gg가 EA 자산 경로를 그대로 준다. ⚠️ level은 배열 인덱스이지 EA 공식 표기가 아니다."))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", nargs="*", default=["27"])
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    a = ap.parse_args()
    con = sqlite3.connect(DB)
    for g in a.games:
        gv = f"FC{g}"
        # ⭐ 레어도는 몇 종 안 되므로 **레어도별로 한 장만** 조회하면 된다.
        bases = con.execute(
            """SELECT rarity_ea_id, MIN(COALESCE(base_ea_id, ea_item_id)) FROM player_card_items
                WHERE game_version=? AND rarity_ea_id IS NOT NULL GROUP BY rarity_ea_id""", (gv,)).fetchall()
        seen, rows = set(), []
        for rid, ea in bases:
            d = get(f"{API}/players/v2/all-versions/{ea}/")
            for item in ((d or {}).get("data") or []):
                rar = item.get("rarity") or {}
                key = rar.get("eaId")
                if key is None or key in seen:
                    continue
                seen.add(key)
                rows += rows_from(rar, gv, a.pulled,
                                  f"fut.gg {API}/players/v2/all-versions/{ea}/ rarity ({a.pulled}, collect_futgg_rarities.py)")
            time.sleep(0.2)
        con.executemany("""INSERT INTO fc_rarity_assets(game_version, rarity_ea_id, rarity_name, level,
                             image_url, compact_url, line_color, text_color, dominant_color, is_special,
                             pulled, source, confidence) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                           ON CONFLICT(game_version, rarity_ea_id, level, pulled) DO UPDATE SET
                             image_url=excluded.image_url, line_color=excluded.line_color,
                             text_color=excluded.text_color""", rows)
        con.commit()
        three = sum(1 for r in rows if r[3] == 1)
        print(f"{gv}: 레어도 {len(seen)}종 → {len(rows)}행 적재 (3단계 보유 {three}종 · pulled {a.pulled})")
        miss = [rid for rid, _ in bases if rid not in seen]
        if miss:
            print(f"   ⚠️ 판을 못 받은 레어도 {len(miss)}종: {miss[:8]} — 화면은 기존 방식으로 물러선다(지어내지 않는다).")
    print("\n다음: python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
