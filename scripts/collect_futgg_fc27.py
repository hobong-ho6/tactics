#!/usr/bin/env python3
"""FC27 선수 스탯 수집 — fut.gg 클럽별 레이팅 페이지(공식/예측 구분).

왜 fut.gg인가 (2026-08-22 신설):
  FC27 Ratings Database가 **2026-08-21 09:00 PT**에 열렸다. 그런데 우리 기존 경로인
  **sofifa는 403**이고 futbin·cmtracker도 403이다(obs#274 계열). fut.gg는 200이고,
  ⭐ **「EA가 확정한 공식 레이팅만 Official로 표시하고 미확정 선수는 Predictions로 분리」**한다
  — 즉 provenance가 소스 자체에 붙어 있다. 이 스크립트는 그 구분을 그대로 DB로 옮긴다.

⚠️ **공식/예측을 반드시 갈라 읽어야 한다.** 2026-08-22 시점 전체 공식은 **677명**뿐이고
   예측이 17,084명이다. 프리미어리그 드롭은 끝났고(08-19) 다음 예정은 쉬퍼리그다
   ⇒ **AVL·CHE·LIV은 공식이 있고 ATM(라리가)은 예측만 있을 수 있다.**

⛔ **attrs(35속성)·playstyles는 이 경로로 수집되지 않는다.** EA 공식 스케줄상
   **PlayStyles는 09-10판에서** 들어오고(obs#249), 그것이 우리 정본이다. 이 회차는 **1단계**다.

⚠️ 여자팀이 같은 클럽 페이지에 섞여 있다(예: 빌라 Men 11 / Women 9).
   `players`·`squad_entries`와 이름이 매칭되지 않는 행은 `player_id=NULL`로 적재하고 보고한다.

사용:
    .venv/bin/python scripts/collect_futgg_fc27.py --team AVL --dry-run
    .venv/bin/python scripts/collect_futgg_fc27.py --team AVL CHE LIV ATM --include-predictions
"""
import argparse
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "tactics.db"

CLUBS = {                       # fut.gg 클럽 슬러그 (2026-08-22 확인)
    "AVL": "2-aston-villa",
    "CHE": "5-chelsea",
    "LIV": "9-liverpool",
    "ATM": "240-atletico-de-madrid",
}

# 공식 확정 행의 텍스트 형태:
#   "{full} FC 27 official rating | {full} | OFFICIAL | {club} | {Δovr} | {short} | {ovr} | {pos}
#    | K1 | v1 | ... K6 | v6 | (Δ 목록…)"
CARD_RE = re.compile(
    r"(?P<full>[^|]+?) FC 27 (?:official rating|rating prediction) \| [^|]+ \| "
    r"(?P<flag>OFFICIAL|PREDICTION) \| (?P<club>[^|]+?) \| (?P<dovr>[+-]?\d+) \| "
    r"(?P<short>[^|]+?) \| (?P<ovr>\d{2,3}) \| (?P<pos>[A-Z]{2,3}) \| "
    r"(?P<k1>[A-Z]{3}) \| (?P<v1>\d{1,3}) \| (?P<k2>[A-Z]{3}) \| (?P<v2>\d{1,3}) \| "
    r"(?P<k3>[A-Z]{3}) \| (?P<v3>\d{1,3}) \| (?P<k4>[A-Z]{3}) \| (?P<v4>\d{1,3}) \| "
    r"(?P<k5>[A-Z]{3}) \| (?P<v5>\d{1,3}) \| (?P<k6>[A-Z]{3}) \| (?P<v6>\d{1,3})")

JS = """async () => {
  // Predictions 토글이 있으면 눌러 둘 다 받는다 — 호출부가 필요할 때만 쓴다.
  return document.body.innerText.replace(/\\n/g, ' | ');
}"""


def norm(s):
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return re.sub(r"[^a-z ]", "", s.casefold()).strip()


def parse(text):
    out = []
    for m in CARD_RE.finditer(text):
        d = m.groupdict()
        out.append({
            "full": d["full"].strip(), "short": d["short"].strip(),
            "official": d["flag"] == "OFFICIAL", "club": d["club"].strip(),
            "ovr": int(d["ovr"]), "pos": d["pos"], "dovr": int(d["dovr"]),
            "stats": [(d[f"k{i}"], int(d[f"v{i}"])) for i in range(1, 7)],
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", nargs="*", default=[], choices=list(CLUBS))
    ap.add_argument("--clubs", nargs="*", default=[],
                    help="fut.gg 클럽 슬러그 직접 지정. ⭐ **FC27 DB는 26/27 이적을 반영하지 않으므로 "
                         "신규 영입은 전 소속 클럽 페이지에 있다** — 그 결손을 닫는 경로다")
    ap.add_argument("--include-predictions", action="store_true",
                    help="공식 미확정 선수의 예측값도 적재한다(행에 예측임을 명기)")
    ap.add_argument("--roster-date", default=None, help="기본: 오늘")
    ap.add_argument("--include-unmatched", action="store_true",
                    help="`players` 미매칭 행도 적재(⚠️ 여자팀이 같은 페이지에 섞여 있다 — 기본 제외)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.roster_date:
        roster = a.roster_date
    else:
        import datetime
        roster = datetime.date.today().isoformat()

    con = sqlite3.connect(DB)
    # 이름 매칭 사전: players 전체 + squad_entries 라벨
    by_name = {}
    for pid, name, kr in con.execute("SELECT id, name, name_kr FROM players"):
        by_name[norm(name)] = (pid, kr or name)
        if kr:
            by_name.setdefault(norm(kr), (pid, kr))

    from playwright.sync_api import sync_playwright
    rows, unmatched = [], []
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page()
        targets = [(t, CLUBS[t]) for t in a.team] + [(f"slug:{c}", c) for c in a.clubs]
        if not targets:
            sys.exit("--team 또는 --clubs 중 하나는 필요하다")
        for team, slug in targets:
            url = f"https://www.fut.gg/players/rating-predictions/clubs/{slug}/"
            pg.goto(url, wait_until="domcontentloaded", timeout=60_000)
            pg.wait_for_timeout(3000)
            cards = parse(pg.evaluate(JS))
            if not a.include_predictions:
                cards = [c for c in cards if c["official"]]
            off = sum(1 for c in cards if c["official"])
            print(f"[{team}] {len(cards)}행 파싱 · 공식 {off} · 예측 {len(cards) - off}")
            for c in cards:
                hit = by_name.get(norm(c["full"])) or by_name.get(norm(c["short"]))
                if hit:
                    c["pid"], c["kr"] = hit
                else:
                    c["pid"], c["kr"] = None, c["full"]
                    unmatched.append((team, c["full"], c["ovr"], c["official"]))
                c["team"], c["slug"] = team, slug
                rows.append(c)
        br.close()

    if unmatched:
        print(f"\n⚠️ `players` 미매칭 {len(unmatched)}행 — 여자팀·유스 포함 가능. player_id=NULL로 적재:")
        for t, n, o, of in unmatched[:25]:
            print(f"   [{t}] {n} OVR {o} {'공식' if of else '예측'}")
        if len(unmatched) > 25:
            print(f"   … 외 {len(unmatched) - 25}행")

    if a.dry_run:
        print("\n--dry-run — DB에 쓰지 않았다.")
        for c in rows[:12]:
            print(f"   {c['kr']:<14} {c['ovr']} {c['pos']:<4}"
                  f" {' '.join(f'{k}{v}' for k, v in c['stats'])}"
                  f" {'공식' if c['official'] else '예측'} Δ{c['dovr']:+d}")
        return

    cur = con.cursor()
    ins, skipped = 0, 0
    for c in rows:
        if c["pid"] is None and not a.include_unmatched:
            skipped += 1
            continue
        vals = dict(c["stats"])
        src = (f"fut.gg /players/rating-predictions/clubs/{c['slug']} "
               f"({'EA 공식 확정' if c['official'] else '**예측값**'}, {roster} 수집)")
        conf = ("⭐ FC27 **1단계** 수집이다 — EA 공식 스케줄상 **PlayStyles와 이적 반영은 09-10판**이고 "
                "그것이 정본이다(obs#249). 이 행에는 `attrs`(35속성)·`playstyles`가 없다. "
                + ("**EA가 확정한 공식 레이팅**이다. " if c["official"] else
                   "⛔ **EA 미확정 = fut.gg 예측값이다.** 공식 드롭 후 반드시 갱신할 것. ")
                + f"fut.gg 표기 OVR 변화 Δ{c['dovr']:+d}. "
                "⚠️ **Δ의 기준 시점을 밝히지 않으면 부호가 뒤집힌다** — fut.gg Δ는 FC26 **출시판** 기준이고 "
                "우리 FC26 행은 시즌 말 라이브판이다(obs#249). 우리 Δ는 DB 간 대조로 따로 산출할 것. "
                "⚠️ 이 경로는 6개 종합 스탯까지만 준다 — sofifa 상세(35속성)는 403으로 막혀 있다(obs#274).")
        cur.execute(
            """INSERT INTO player_game_stats(game_version, roster_date, player_id, name_kr,
               sofifa_name, club, positions, best_pos, ovr, pac, sho, pas, dri, def, phy,
               source, confidence)
               VALUES('FC27',?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(game_version, roster_date, name_kr) DO NOTHING""",
            (roster, c["pid"], c["kr"], c["full"], c["club"], c["pos"], c["pos"], c["ovr"],
             vals.get("PAC") or vals.get("DIV"), vals.get("SHO") or vals.get("HAN"),
             vals.get("PAS") or vals.get("KIC"), vals.get("DRI") or vals.get("REF"),
             vals.get("DEF") or vals.get("SPD"), vals.get("PHY") or vals.get("POS"),
             src, conf))
        ins += cur.rowcount
    con.commit()
    print(f"\n적재: player_game_stats(FC27, {roster}) +{ins}행 · 미매칭 제외 {skipped}행")
    print("⚠️ GK는 6칸이 DIV/HAN/KIC/REF/SPD/POS로 들어간다(FC26 행과 같은 규약).")
    print("다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
