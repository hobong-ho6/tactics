#!/usr/bin/env python3
"""FUT 갤러리 수집 — 세트 정의 + 등급별 최저 비용 조합 (2026-09-27 신설, migration 085).

왜 (사용자 「fut-gallery 에 갤러리 관련 메뉴가 있는데 이건 api가 없다는 거지?」):
  ⛔⛔ **「없다」고 단정한 내가 틀렸다.** `/api/gg-club/gallery/`(구단 하위)만 찔러 보고 보고했는데
     실제 경로는 **`/api/fut/gallery/{game}/hub/`**이고 **인증 없이 200**이다.
     ⇒ 없다는 결론은 **찔러 본 범위 안에서만** 유효하다 — 범위를 밝히지 않으면 있는 것을 없다고 말하게 된다.

무엇을 주나: 한 응답에 전부 들어 있다.
  · `categories[].sets[]` — 세트 정의(필요 장수 · 등급 임계 · 총 토큰 · 소속 clubEaId 등)
  · `sets[]` — 세트별 **등급별 최저 비용 조합**(`costTiers[{grade, threshold, tokens, cost, peakPrice, items}]`)
    ⭐ fut.gg가 시장 최저가로 풀어 준 답이다 — 우리가 다시 풀 필요가 없다.

⛔⛔ **내 수집 현황은 받을 수 없다**(개인 진행도 경로 전부 404).
   ⚠️ 우리 원장으로 근사하면 **과소 집계**다 — EA는 **계정 전체 이력**(판 카드 포함)을 인정하는데
      `fut_club_players`는 2026-09-17부터다. 화면이 그 한계를 적는다.
⚠️ `cost`는 **시세**라 금방 낡는다 — 날짜별 스냅샷으로 쌓고 최신만 쓴다(가격 축과 같은 성격).

사용:
    .venv/bin/python scripts/collect_futgg_gallery.py --games 27
"""
import argparse
import datetime as dt
import json
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
        url = f"{API}/gallery/fc{g}/hub/"
        d = (get(url) or {}).get("data")
        if not d:
            print(f"⛔ {gv}: 응답이 없다 — 경로가 바뀌었을 수 있다({url}). 지어내지 않고 멈춘다.")
            continue
        src = f"fut.gg {url} ({a.pulled} 수집, collect_futgg_gallery.py)"
        # ① 세트 정의 — categories[].sets[]
        rows = []
        for c in (d.get("categories") or []):
            for s in (c.get("sets") or []):
                rows.append((gv, s.get("id"), c.get("id"), c.get("name"),
                             s.get("name"), s.get("slug"), s.get("description"),
                             s.get("requiredCards"), s.get("totalTokens"),
                             s.get("clubEaId"), s.get("leagueEaId"), s.get("rarityEaId"),
                             (dt.datetime.utcfromtimestamp(s["startTime"]).isoformat()
                              if s.get("startTime") else None),
                             json.dumps(s.get("grades"), ensure_ascii=False), a.pulled, src,
                             "HIGH — fut.gg가 EA 세트 정의를 그대로 준다(등급 임계·토큰 포함)."))
        con.executemany("""INSERT INTO fc_gallery_sets(game_version,set_id,category_id,category_name,name,slug,
                             description,required_cards,total_tokens,club_ea_id,league_ea_id,rarity_ea_id,
                             start_time,grades_json,pulled,source,confidence)
                           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                           ON CONFLICT(game_version,set_id,pulled) DO UPDATE SET
                             name=excluded.name, required_cards=excluded.required_cards,
                             total_tokens=excluded.total_tokens, grades_json=excluded.grades_json""", rows)
        # ② 등급별 최저 비용 조합 — sets[].costTiers[]
        tiers = []
        for s in (d.get("sets") or []):
            for t in (s.get("costTiers") or []):
                tiers.append((gv, s.get("setId"), t.get("grade"), t.get("threshold"), t.get("tokens"),
                              t.get("cost"), t.get("peakPrice"), t.get("totalScore"),
                              json.dumps(t.get("items"), ensure_ascii=False), a.pulled, src,
                              "MEDIUM — fut.gg가 **시장 최저가**로 푼 조합이다. ⚠️ 내가 이미 수집한 카드를 "
                              "빼지 않았고, 시세라 회차마다 바뀐다."))
        con.executemany("""INSERT INTO fc_gallery_tiers(game_version,set_id,grade,threshold,tokens,cost,
                             peak_price,total_score,items_json,pulled,source,confidence)
                           VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
                           ON CONFLICT(game_version,set_id,grade,pulled) DO UPDATE SET
                             cost=excluded.cost, items_json=excluded.items_json,
                             total_score=excluded.total_score""", tiers)
        con.commit()
        tok = sum(r[8] or 0 for r in rows)
        print(f"{gv}: 세트 {len(rows)}종({len(d.get('categories') or [])}개 분류) · "
              f"등급 조합 {len(tiers)}행 · 토큰 총량 {tok} (capturedAt {str(d.get('capturedAt'))[:10]} · pulled {a.pulled})")
        print("   ⛔ **내 수집 현황은 받을 수 없다** — 개인 진행도 경로가 전부 404다. "
              "우리 원장으로 근사하면 계정 전체 이력을 모르므로 **과소 집계**가 된다.")
    print("\n다음: python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
