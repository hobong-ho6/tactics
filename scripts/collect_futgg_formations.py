#!/usr/bin/env python3
"""FC27 포메이션 29종 수집 — fut.gg 웹앱 번들 (2026-09-25 신설, migration 070).

왜 (사용자 지시 2026-09-25 「선택 가능한 포메이션은 FC27에서 지원하는 모든 포메이션이어야」):
  솔버·화면이 4종을 코드에 박아 쓰고 있었다. SBC는 챌린지마다 포메이션이 고정이라 목록이 모자라면
  그 값을 기록할 수조차 없다.

원천: 번들의 포메이션 배열 `{id,index,name,uniquePositionSlots,generalPositionSlots}`
  · `generalPositionSlots` = **그 칸에 설 수 있는 카드 포지션**(등급 A — 번들 enum으로 확인).
  · `uniquePositionSlots`  = 좌우까지 가른 표시용 id.

⚠️ 표시 이름표(LCB/RCB…)와 피치 좌표는 **우리 판단값**이다(등급 D) — EA가 표로 공개한 적 없다.
   좌표는 화면이 피치를 그릴 때만 쓰고 판정에는 쓰지 않는다.

사용:
    .venv/bin/python scripts/collect_futgg_formations.py
"""
import argparse
import datetime as dt
import json
import re
import sqlite3
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DB = ROOT / "db" / "tactics.db"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

# EA 포지션 슬롯 id → 표시 이름. ⚠️ 등급 D(통용표). general 쪽만 번들 enum으로 확인됐다.
LABEL = {0: "GK", 1: "SW", 2: "RWB", 3: "RB", 4: "RCB", 5: "CB", 6: "LCB", 7: "LB", 8: "LWB",
         9: "RDM", 10: "CDM", 11: "LDM", 12: "RM", 13: "RCM", 14: "CM", 15: "LCM", 16: "LM",
         17: "RAM", 18: "CAM", 19: "LAM", 20: "RF", 21: "CF", 22: "LF", 23: "RW", 24: "RS",
         25: "ST", 26: "LS", 27: "LW"}
# 피치 좌표(가로 %, 세로 % — 아래가 우리 골대). ⚠️ 우리 레이아웃 값이지 EA 값이 아니다.
XY = {0: (50, 6), 1: (50, 16),
      2: (88, 34), 3: (88, 26), 4: (66, 22), 5: (50, 20), 6: (34, 22), 7: (12, 26), 8: (12, 34),
      9: (66, 42), 10: (50, 40), 11: (34, 42),
      12: (88, 56), 13: (64, 52), 14: (50, 52), 15: (36, 52), 16: (12, 56),
      17: (66, 66), 18: (50, 66), 19: (34, 66),
      20: (70, 80), 21: (50, 78), 22: (30, 80),
      23: (86, 78), 24: (62, 88), 25: (50, 88), 26: (38, 88), 27: (14, 78)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="FC27")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode()
    home = get("https://www.fut.gg/")
    ref = re.findall(r'src="([^"]*index-[^"]*\.js)"', home)
    if not ref:
        raise SystemExit("⛔ 번들 참조를 찾지 못했다 — fut.gg 배포 구조가 바뀌었다")
    js = get(ref[0] if ref[0].startswith("http") else "https://www.fut.gg" + ref[0])

    found = re.findall(
        r"\{id:(\d+),index:\d+,name:`([^`]+)`,uniquePositionSlots:\[([\d,]+)\],generalPositionSlots:\[([\d,]+)\]\}", js)
    if not found:
        raise SystemExit("⛔ 포메이션 배열을 찾지 못했다 — 번들 구조가 바뀌었다")
    rows = []
    for eid, name, uniq, gen in found:
        us = [int(x) for x in uniq.split(",")]
        gs = [int(x) for x in gen.split(",")]
        if len(us) != 11 or len(gs) != 11:
            print(f"  ⚠️ {name}: 슬롯이 11이 아니다({len(us)}/{len(gs)}) — 건너뛴다")
            continue
        slots = [{"i": i, "uniq": u, "gen": g, "label": LABEL.get(u, str(u)),
                  "x": XY.get(u, (50, 50))[0], "y": XY.get(u, (50, 50))[1]}
                 for i, (u, g) in enumerate(zip(us, gs))]
        rows.append((a.game, int(eid), name, json.dumps(slots, ensure_ascii=False),
                     f"fut.gg 웹앱 번들 포메이션 배열 ({ref[0].split('/')[-1]}, {a.pulled} 파싱, collect_futgg_formations.py)",
                     "A(슬롯 구성·general 포지션 = 번들 원문) · D(표시 이름표·피치 좌표는 우리 판단값)",
                     a.pulled))
    unknown = sorted({s for _g, _e, _n, sl, *_ in rows for s in
                      [x["uniq"] for x in json.loads(sl)] if s not in LABEL})
    print(f"포메이션 {len(rows)}종" + (f" · ⚠️ 이름표 없는 슬롯 id {unknown}" if unknown else ""))
    for r in rows[:3]:
        print(f"  {r[2]:<12} {[x['label'] for x in json.loads(r[3])]}")
    if a.dry_run:
        print("\n--dry-run — DB에 쓰지 않았다.")
        return
    con = sqlite3.connect(DB)
    con.executemany("""INSERT INTO fc_formations(game_version, ea_id, name, slots, source, confidence, pulled)
                       VALUES(?,?,?,?,?,?,?)
                       ON CONFLICT(game_version, ea_id) DO UPDATE SET
                         name=excluded.name, slots=excluded.slots, source=excluded.source,
                         confidence=excluded.confidence, pulled=excluded.pulled""", rows)
    con.commit()
    print(f"\n적재 {len(rows)}종 → fc_formations")


if __name__ == "__main__":
    main()
