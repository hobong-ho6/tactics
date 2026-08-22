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
    # ⚠️ Δovr는 **선택**이다 — FC26에 없던 신규·유스 선수 카드에는 변화값 필드가 아예 없다.
    #    필수로 두면 그 선수들이 조용히 전부 누락된다(2026-08-22에 유스 14명이 이렇게 빠졌다).
    r"(?P<flag>OFFICIAL|PREDICTION) \| (?P<club>[^|]+?) \| (?:(?P<dovr>[+-]?\d+) \| )?"
    r"(?P<short>[^|]+?) \| (?P<ovr>\d{2,3}) \| (?P<pos>[A-Z]{2,3}) \| "
    r"(?P<k1>[A-Z]{3}) \| (?P<v1>\d{1,3}) \| (?P<k2>[A-Z]{3}) \| (?P<v2>\d{1,3}) \| "
    r"(?P<k3>[A-Z]{3}) \| (?P<v3>\d{1,3}) \| (?P<k4>[A-Z]{3}) \| (?P<v4>\d{1,3}) \| "
    r"(?P<k5>[A-Z]{3}) \| (?P<v5>\d{1,3}) \| (?P<k6>[A-Z]{3}) \| (?P<v6>\d{1,3})")

JS = """async () => {
  // Predictions 토글이 있으면 눌러 둘 다 받는다 — 호출부가 필요할 때만 쓴다.
  return document.body.innerText.replace(/\\n/g, ' | ');
}"""


# fut.gg 상세 라벨 → FC26 `attrs`의 한글 키(sofifa 라벨). ⭐ 키를 맞춰야 FC26↔FC27 비교가 성립한다.
ATTR_MAP = {
    "Acceleration": "가속", "Sprint Speed": "질주 속도",
    "Att. Pos.": "공격 위치 선정", "Finishing": "결정력", "Shot Power": "슈팅력",
    "Long Shots": "중거리슛", "Volleys": "발리 슛", "Penalties": "페널티킥",
    "Vision": "시야", "Crossing": "크로스", "Fk Acc.": "프리킥 정확도",
    "Short Pass": "짧은 패스", "Long Pass": "긴 패스", "Curve": "커브",
    "Agility": "민첩성", "Balance": "균형 감각", "Reactions": "반응력",
    "Ball Control": "볼컨트롤", "Dribbling": "드리블", "Composure": "침착",
    "Interceptions": "차단력", "Heading Acc.": "헤딩 정확도",
    "Def. Aware.": "수비 위치 선정", "Stand Tackle": "스탠딩 태클", "Slide Tackle": "슬라이딩 태클",
    "Jumping": "점프", "Stamina": "체력", "Strength": "힘", "Aggression": "공격성",
    # GK
    "Diving": "다이빙", "Handling": "핸들링", "Kicking": "킥", "Positioning": "포지셔닝",
    "Reflexes": "반사신경", "GK Speed": "GK 스피드",
}


def parse_attrs(text):
    """상세 페이지 텍스트에서 속성 라벨→값을 뽑는다.

    ⛔⛔ **라벨과 값 사이에 「순위 배지」 숫자가 끼어든다** — 원문이 `Vision | 4 | 79`처럼
        `{라벨} | {순위} | {값}`이 되는 경우가 있다(순위 배지가 붙은 속성만). 따라서
        **라벨 뒤 첫 숫자를 취하면 순위를 값으로 읽는다**(2026-08-22에 이 버그로 시야 79→4,
        점프 89→1 같은 값이 들어갔다). ⇒ **라벨과 다음 라벨 사이의 마지막 숫자**가 값이다.
    """
    text = text.replace("\n", " | ")
    # FC27 상세는 「FC 27 Attributes」, FC26 상세는 「Attributes」로 헤더가 다르다.
    i = text.find("FC 27 Attributes")
    if i < 0:
        i = text.find("Attributes")
    if i < 0:
        return {}, None
    seg = text[i:i + 4000]
    out = {}
    for en, kr in ATTR_MAP.items():
        # 라벨 **직후의 연속 숫자열**만 본다. 「라벨 | 값」이면 1개, 「라벨 | 순위 | 값」이면 2개다
        # ⇒ 2개 이상이면 **두 번째**가 값이다. 구간 전체의 마지막 숫자를 쓰면 그룹 헤더 숫자를 먹는다.
        m = re.search(re.escape(en) + r"(?![A-Za-z.])((?:\s*\|\s*\d{1,3})+)", seg)
        if not m:
            continue
        nums = re.findall(r"\d{1,3}", m.group(1))
        out[kr] = int(nums[1] if len(nums) >= 2 else nums[0])
    acc = re.search(r"AcceleRATE \| ([A-Za-z ]+?) \|", seg)
    return out, (acc.group(1).strip() if acc else None)


def norm(s):
    # ⚠️ 하이픈은 **공백으로** 바꾼다 — 삭제하면 안 된다. 상세 링크 슬러그는
    #    `taylor-harwood-bellis`(하이픈→공백)로 오는데 DB 표기는 `Taylor Harwood-Bellis`라
    #    하이픈을 지우면 `taylor harwoodbellis` ↔ `taylor harwood bellis`로 갈려 영구 미매칭이 된다.
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z]+", " ", s.casefold())).strip()


def parse(text):
    out = []
    for m in CARD_RE.finditer(text):
        d = m.groupdict()
        out.append({
            "full": d["full"].strip(), "short": d["short"].strip(),
            "official": d["flag"] == "OFFICIAL", "club": d["club"].strip(),
            "ovr": int(d["ovr"]), "pos": d["pos"],
            "dovr": int(d["dovr"]) if d.get("dovr") is not None else None,
            "stats": [(d[f"k{i}"], int(d[f"v{i}"])) for i in range(1, 7)],
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", nargs="*", default=[], choices=list(CLUBS))
    ap.add_argument("--clubs", nargs="*", default=[],
                    help="fut.gg 클럽 슬러그 직접 지정. ⭐ **FC27 DB는 26/27 이적을 반영하지 않으므로 "
                         "신규 영입은 전 소속 클럽 페이지에 있다** — 그 결손을 닫는 경로다")
    ap.add_argument("--scan-all", action="store_true",
                    help="⭐ 전체 레이팅 목록(/players/rating-predictions/?page=N)을 전수 스캔해 "
                         "`players`에 있는 선수를 모두 채운다. **클럽 슬러그가 필요 없어 「26/27 이적 미반영」 "
                         "결손을 구조적으로 닫는다** — 선수가 어느 클럽 페이지에 있든 잡힌다")
    ap.add_argument("--max-pages", type=int, default=500, help="--scan-all 상한(기본 500)")
    ap.add_argument("--include-predictions", action="store_true",
                    help="공식 미확정 선수의 예측값도 적재한다(행에 예측임을 명기)")
    ap.add_argument("--roster-date", default=None, help="기본: 오늘")
    ap.add_argument("--include-unmatched", action="store_true",
                    help="`players` 미매칭 행도 적재(⚠️ 여자팀이 같은 페이지에 섞여 있다 — 기본 제외)")
    ap.add_argument("--attrs", action="store_true",
                    help="⭐ FC27 **세부 35속성 + AcceleRATE**를 선수 상세 페이지에서 수집해 기존 FC27 행의 "
                         "비어 있는 attrs를 채운다(/players/{eaId}-{slug}/27-{eaId}/). "
                         "키는 FC26 attrs의 한글 라벨로 맞춘다 — 그래야 FC26↔FC27 비교가 성립한다")
    ap.add_argument("--attrs-version", choices=["26", "27"], default="27",
                    help="--attrs가 어느 버전 상세를 읽을지. ⭐ FC26도 같은 소스(fut.gg)에서 받아야 "
                         "속성 비교의 provenance가 섞이지 않는다 — sofifa(FC26) ↔ fut.gg(FC27) 혼합은 피한다")
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
    rows, unmatched, attr_rows = [], [], []
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page()
        targets = [(t, CLUBS[t]) for t in a.team] + [(f"slug:{c}", c) for c in a.clubs]
        if a.scan_all:
            # 마지막 페이지는 페이지네이션 링크에서 읽는다(하드코딩 금지 — 드롭마다 늘어난다).
            pg.goto("https://www.fut.gg/players/rating-predictions/",
                    wait_until="domcontentloaded", timeout=60_000)
            pg.wait_for_timeout(2500)
            last = pg.evaluate("""() => Math.max(0, ...[...document.querySelectorAll("a[href*='page=']")]
                 .map(a => +(a.getAttribute('href').match(/page=(\\d+)/)||[0,0])[1]))""")
            last = min(last or 1, a.max_pages)
            print(f"[scan-all] 전체 {last}페이지 스캔 시작 (matched만 적재)")
            for n in range(1, last + 1):
                pg.goto(f"https://www.fut.gg/players/rating-predictions/?page={n}",
                        wait_until="domcontentloaded", timeout=60_000)
                pg.wait_for_timeout(1200)
                cards = parse(pg.evaluate(JS))
                hit = 0
                for c in cards:
                    h = by_name.get(norm(c["full"])) or by_name.get(norm(c["short"]))
                    if not h:
                        continue          # 우리 DB에 없는 선수는 버린다(2만 명을 넣지 않는다)
                    c["pid"], c["kr"] = h
                    c["team"], c["slug"] = "scan-all", f"page{n}"
                    rows.append(c); hit += 1
                if hit:
                    print(f"  page {n:>3}/{last}: 매칭 {hit}명 — "
                          + ", ".join(x["kr"] for x in rows[-hit:]))
                elif n % 50 == 0:
                    print(f"  page {n:>3}/{last}: …")
        if a.attrs:
            slugs = [CLUBS[t] for t in a.team] + list(a.clubs) or list(CLUBS.values())
            links = {}
            for slug in slugs:
                pg.goto(f"https://www.fut.gg/players/rating-predictions/clubs/{slug}/",
                        wait_until="domcontentloaded", timeout=60_000)
                pg.wait_for_timeout(2500)
                for h in pg.eval_on_selector_all(
                        "a[href*='/27-']", "els=>els.map(e=>e.getAttribute('href'))"):
                    m = re.match(r"/players/(\d+)-([a-z0-9-]+)/27-\1/?$", h or "")
                    if m:
                        links[m.group(1)] = (h, m.group(2).replace("-", " "))
            print(f"[attrs] 상세 링크 {len(links)}건 수집 — 우리 DB 매칭분만 방문한다")
            done = 0
            for ea, (href, nm) in links.items():
                hit = by_name.get(norm(nm))
                if not hit:
                    continue
                pid, kr = hit
                url = re.sub(r"/27-", f"/{a.attrs_version}-", "https://www.fut.gg" + href)
                pg.goto(url, wait_until="domcontentloaded", timeout=60_000)
                # ⚠️ 속성 블록은 클라이언트에서 늦게 렌더된다 — 고정 대기(900ms)로는 못 잡는다.
                #    텍스트가 나타날 때까지 폴링한다(최대 ~5초).
                body = ""
                for _ in range(10):
                    pg.wait_for_timeout(500)
                    body = pg.inner_text("body")
                    if "Attributes" in body:
                        break
                at, acc = parse_attrs(body)
                if not at:
                    print(f"  ⚠️ {kr}: 속성 블록 없음"); continue
                attr_rows.append((pid, kr, ea, at, acc)); done += 1
                if done % 10 == 0:
                    print(f"  … {done}명 수집")
            print(f"[attrs] {done}명 속성 수집 완료")
        if not targets and not a.scan_all and not a.attrs:
            sys.exit("--team · --clubs · --scan-all 중 하나는 필요하다")
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
                  f" {'공식' if c['official'] else '예측'}"
                  f" {('Δ%+d' % c['dovr']) if c['dovr'] is not None else 'Δ없음(신규)'}")
        return

    cur = con.cursor()
    if attr_rows:
        import json
        upd = 0
        for pid, kr, ea, at, acc in attr_rows:
            gv = "FC" + a.attrs_version
            # ⚠️ 같은 버전에 roster_date가 여럿이다 — **최신 행만** 채운다(화면이 최신을 쓰므로).
            #    전 행에 뿌리면 06-30 로스터 행에 08-22 수집 속성이 붙어 provenance가 번진다.
            cur.execute(f"""UPDATE player_game_stats SET attrs=?, accelerate=COALESCE(accelerate,?),
                           detail_date=?, confidence=COALESCE(confidence,'')||?
                           WHERE game_version='{gv}' AND player_id=? AND (attrs IS NULL OR attrs='')
                             AND roster_date=(SELECT MAX(roster_date) FROM player_game_stats
                                              WHERE game_version='{gv}' AND player_id=?)""",
                        (json.dumps(at, ensure_ascii=False), acc, roster,
                         f" ⭐ [{roster}] 세부 {len(at)}속성(fut.gg FC{a.attrs_version} 상세)"
                         + (f" + AcceleRATE({acc})" if acc else "")
                         + f" 수집 — fut.gg 상세 /players/{ea}-…/27-{ea}/. "
                           "키는 FC26 attrs의 한글 라벨로 맞췄다(비교 가능성 확보). "
                           "⛔ **playstyles는 여전히 없다** — 그 페이지의 PlayStyles 목록은 "
                           "커뮤니티 투표 %이지 EA 확정값이 아니다(09-10판이 정본, obs#249).",
                         pid, pid))
            upd += cur.rowcount
        con.commit()
        print(f"\n적재: attrs +{upd}행")
        if not rows:
            return
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
                + (f"fut.gg 표기 OVR 변화 Δ{c['dovr']:+d}. " if c["dovr"] is not None else
                   "⭐ fut.gg에 **Δ 필드가 없다 = FC26에 없던 신규 카드**다(유스·신규 등재). ")
                + "⚠️ **Δ의 기준 시점을 밝히지 않으면 부호가 뒤집힌다** — fut.gg Δ는 FC26 **출시판** 기준이고 "
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
