#!/usr/bin/env python3
"""FC25·FC26 출시판 게임스탯 수집 — fut.gg 아이템 정의 API (버전별 변화 추적용).

왜 (2026-09-12 신설, 사용자 지시 「게임스탯은 FC25부터 수집해 변화 과정을 볼 수 있게」):
  fut.gg `/api/fut/player-item-definitions/{game}/{eaId}/`가 **curl로 200**이고(브라우저 불필요),
  한 응답에 OVR·6종합·**34속성**·키·몸무게·PlayStyles(+)·AcceleRATE·주발·생년월일·`createdAt`이 전부 있다.
  기존 FC27 09-10 행의 `card_image_url`에 EA id(`27-{eaId}`)가 박혀 있어 그 id로 과거 버전을 조회한다.

⭐⭐ **fut.gg base 아이템 = 그 버전 「출시판」 값이다(라이브 갱신 미반영).** 실증: 왓킨스 FC26 base = 84(fut.gg Δ 기준 출시판)
   ↔ 우리 sofifa 2026-07-23(시즌 말 라이브판) = 82. ⇒ 이 스크립트의 행은 **출시 시점 스냅샷**이고
   `roster_date`는 아이템 `createdAt`(EA 레이팅 공개일)이다. 기존 FC26 sofifa 행(시즌 말)과 **시점이 다르므로 공존**한다.

⚠️ 여자 선수와 EA id 공간이 겹치지 않지만 **이름 매칭은 성별을 가른다** — 09-10 수집이 리스 제임스에 로렌 제임스(265249)의
   키·몸무게·카드를 붙였다(obs 기록). 이 스크립트는 `gender==1`·이름 토큰 교차를 검사해 불일치면 적재하지 않고 보고한다.

사용:
    .venv/bin/python scripts/collect_futgg_history.py --dry-run
    .venv/bin/python scripts/collect_futgg_history.py --games 25 26
    .venv/bin/python scripts/collect_futgg_history.py --players 198 --ea 198=243630   # id 수동 지정
"""
import argparse
import datetime as dt
import json
import re
import sqlite3
import sys
import time
import unicodedata
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "tactics.db"
UA = {"User-Agent": "Mozilla/5.0"}
API = "https://www.fut.gg/api/fut"

RELEASED = {"25": "2024-09-27", "26": "2025-09-26", "27": "2026-09-25"}

# fut.gg 정의 필드 → FC26/FC27 `attrs`의 한글 라벨(sofifa 라벨). 키를 맞춰야 버전 간 비교가 성립한다.
ATTR_MAP = {
    "attributeAcceleration": "가속", "attributeSprintSpeed": "질주 속도",
    "attributePositioning": "공격 위치 선정", "attributeFinishing": "결정력", "attributeShotPower": "슈팅력",
    "attributeLongShots": "중거리슛", "attributeVolleys": "발리 슛", "attributePenalties": "페널티킥",
    "attributeVision": "시야", "attributeCrossing": "크로스", "attributeFkAccuracy": "프리킥 정확도",
    "attributeShortPassing": "짧은 패스", "attributeLongPassing": "긴 패스", "attributeCurve": "커브",
    "attributeAgility": "민첩성", "attributeBalance": "균형 감각", "attributeReactions": "반응력",
    "attributeBallControl": "볼컨트롤", "attributeDribbling": "드리블", "attributeComposure": "침착",
    "attributeInterceptions": "차단력", "attributeHeadingAccuracy": "헤딩 정확도",
    "attributeDefensiveAwareness": "수비 위치 선정", "attributeStandingTackle": "스탠딩 태클",
    "attributeSlidingTackle": "슬라이딩 태클", "attributeJumping": "점프", "attributeStamina": "체력",
    "attributeStrength": "힘", "attributeAggression": "공격성",
    "attributeGkDiving": "다이빙", "attributeGkHandling": "핸들링", "attributeGkKicking": "킥",
    "attributeGkPositioning": "포지셔닝", "attributeGkReflexes": "반사신경",
}
GK_ATTRS = {"가속", "질주 속도", "반응력", "다이빙", "핸들링", "킥", "포지셔닝", "반사신경"}   # 기존 GK 행의 attrs 키 집합
OUTFIELD_DROP = {"다이빙", "핸들링", "킥", "포지셔닝", "반사신경"}                            # 기존 필드 행은 GK 5속성 미포함
# positionId → 표기. v2 목록에서 관측된 값(2026-09-12)으로 고정하고, 미지의 id는 그대로 문자열로 남긴다.
POS = {0: "GK", 2: "RWB", 3: "RB", 5: "CB", 7: "LB", 8: "LWB", 10: "CDM", 12: "RM", 14: "CM", 16: "LM",
       18: "CAM", 21: "CF", 23: "RW", 25: "ST", 27: "LW"}
FOOT = {1: "오른쪽", 2: "왼쪽"}
# FC26에서 폐지돼 현행 카탈로그(/api/fut/playstyles/, 36종)에 없는 FC25 PlayStyle id.
# 24=Trivela는 조나단 데이비드 FC25 페이지로 확인(2026-09-12). 나머지 셋은 FC24 카테고리 순서에서 추정 —
# 등장하면 선수 페이지 HTML에서 이름 존재를 확인하고, 없으면 raw id로 남겨 보고한다.
LEGACY_PS = {24: "Trivela", 4: "Power Header", 18: "Flair", 27: "Aerial"}


def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(1.5 * (i + 1))
        except Exception:
            time.sleep(1.5 * (i + 1))
    return None


def norm(s):
    s = "".join(c for c in unicodedata.normalize("NFKD", s or "") if not unicodedata.combining(c))
    return set(re.sub(r"[^a-z ]+", " ", s.casefold()).split())


def accelerate_label(code):
    return " ".join(w.capitalize() for w in (code or "").split("_")) or None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", nargs="*", default=["25", "26"], choices=["24", "25", "26", "27"])
    ap.add_argument("--players", nargs="*", type=int, default=[])
    ap.add_argument("--team", nargs="*", default=[], help="regime team_code로 squad_entries 대상 한정")
    ap.add_argument("--ea", nargs="*", default=[], help="player_id=eaId 수동 지정(예: 198=243630)")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    playstyle = {x["eaId"]: x["name"] for x in get(f"{API}/playstyles/")["data"]}
    verified_legacy = {24}

    def ps_name(i, d):
        if i in playstyle:
            return playstyle[i]
        name = LEGACY_PS.get(i)
        if name and i not in verified_legacy and d.get("url"):
            try:
                with urllib.request.urlopen(urllib.request.Request("https://www.fut.gg" + d["url"], headers=UA), timeout=30) as r:
                    if name in r.read().decode("utf-8", "ignore"):
                        verified_legacy.add(i)
                    else:
                        print(f"  ⚠️ legacy PS id {i}={name} 추정이 {d.get('commonName')} 페이지에서 확인되지 않음 — raw id 적재")
                        return f"PS#{i}"
            except Exception:
                return f"PS#{i}"
        return name or f"PS#{i}"

    # ── 대상: squad_entries 전원(또는 --players) ──
    if a.players:
        pids = a.players
    else:
        q = """SELECT DISTINCT se.player_id FROM squad_entries se JOIN regimes r ON r.id=se.regime_id"""
        if a.team:
            q += " WHERE r.team_code IN (%s)" % ",".join("?" * len(a.team))
        pids = [r[0] for r in con.execute(q, a.team)]
    players = {r["id"]: dict(r) for r in con.execute(
        "SELECT id, name, name_kr, sofifa_id, birth_year FROM players WHERE id IN (%s)" % ",".join(map(str, pids)))}

    # ── EA id: FC27 카드 URL(27-{eaId}) > players.sofifa_id(=EA id) > --ea 수동 ──
    ea_of = {}
    for r in con.execute("""SELECT player_id, card_image_url FROM player_game_stats
                            WHERE game_version='FC27' AND card_image_url LIKE '%/27-%' AND player_id IS NOT NULL"""):
        m = re.search(r"/27-(\d+)\.", r["card_image_url"])
        if m and r["player_id"] in players:
            ea_of.setdefault(r["player_id"], int(m.group(1)))
    for pid, p in players.items():
        if pid not in ea_of and p["sofifa_id"]:
            ea_of[pid] = p["sofifa_id"]
    for kv in a.ea:
        k, v = kv.split("=")
        ea_of[int(k)] = int(v)
    no_id = [players[p]["name_kr"] or players[p]["name"] for p in pids if p not in ea_of]
    print(f"대상 {len(pids)}명 · EA id 확보 {len(ea_of)} · 결손 {len(no_id)}: {', '.join(no_id)}")

    cur = con.cursor()
    for g in a.games:
        cur.execute("INSERT OR IGNORE INTO game_versions(code, released, notes) VALUES(?,?,?)",
                    (f"FC{g}", RELEASED.get(g), f"[{a.pulled}] 버전별 변화 추적용 — fut.gg 출시판 base 아이템(collect_futgg_history.py)"))

    ins, skip, miss, mismatch, id_fill = 0, 0, [], [], 0
    for pid in pids:
        p = players[pid]
        kr = p["name_kr"] or p["name"]
        ea = ea_of.get(pid)
        if not ea:
            continue
        # players.sofifa_id(=EA id) 빈 칸 채움 — 덮어쓰지 않는다
        if not p["sofifa_id"] and not a.dry_run:
            cur.execute("UPDATE players SET sofifa_id=? WHERE id=? AND sofifa_id IS NULL", (ea, pid))
            id_fill += 1
        for g in a.games:
            gv = f"FC{g}"
            d = get(f"{API}/player-item-definitions/{g}/{ea}/")
            d = d.get("data", d) if isinstance(d, dict) else None
            if not d:
                miss.append((kr, gv))
                continue
            # 동일성: 남자 + 이름 토큰 교차
            if d.get("gender") != 1 or not (norm(p["name"]) & norm(d.get("commonName", "") + " " + d.get("firstName", "") + " " + d.get("lastName", ""))):
                mismatch.append((kr, gv, ea, d.get("commonName"), d.get("gender")))
                continue
            roster = (d.get("createdAt") or "")[:10] or RELEASED.get(g)
            if cur.execute("SELECT 1 FROM player_game_stats WHERE game_version=? AND player_id=? AND roster_date=?",
                           (gv, pid, roster)).fetchone():
                skip += 1
                continue
            gk = d.get("position") == 0
            attrs = {ATTR_MAP[k]: d[k] for k in ATTR_MAP if d.get(k) is not None}
            attrs = {k: v for k, v in attrs.items() if (k in GK_ATTRS if gk else k not in OUTFIELD_DROP)}
            if gk:   # 기존 GK 행의 6종합 = DIV/HAN/KIC/REF/SPD/POS (마르티네스 09-10 행으로 검증)
                six = [d.get("gkFaceDiving"), d.get("gkFaceHandling"), d.get("gkFaceKicking"),
                       d.get("gkFaceReflexes"), d.get("gkFaceSpeed"), d.get("gkFacePositioning")]
            else:
                six = [d.get("facePace"), d.get("faceShooting"), d.get("facePassing"),
                       d.get("faceDribbling"), d.get("faceDefending"), d.get("facePhysicality")]
            ps = [ps_name(i, d) for i in d.get("playstyles") or []] + \
                 [ps_name(i, d) + "+" for i in d.get("playstylesPlus") or []]
            positions = "/".join([POS.get(d.get("position"), str(d.get("position")))] +
                                 [POS.get(i, str(i)) for i in d.get("alternativePositionIds") or []])
            age = None
            if d.get("dateOfBirth"):
                b = dt.date.fromisoformat(d["dateOfBirth"]); r = dt.date.fromisoformat(roster)
                age = r.year - b.year - ((r.month, r.day) < (b.month, b.day))
            # 카드 이미지·클럽명은 v2 목록에서
            lst = get(f"{API}/players/v2/{g}/?ea_ids={ea}")
            base = next((x for x in (lst or {}).get("data", []) if x.get("eaId") == ea), {}) if lst else {}
            club = (base.get("club") or {}).get("name")
            card = base.get("cardImageUrl")
            row = dict(
                game_version=gv, roster_date=roster, player_id=pid, name_kr=kr, sofifa_id=ea,
                sofifa_name=d.get("commonName"), club=club, positions=positions, best_pos=positions.split("/")[0],
                age=age, height_cm=d.get("height"), weight_kg=d.get("weight"), ovr=d.get("overall"), pot=None,
                pac=six[0], sho=six[1], pas=six[2], dri=six[3], def_=six[4], phy=six[5],
                attrs=json.dumps(attrs, ensure_ascii=False), playstyles=", ".join(ps) or None,
                accelerate=accelerate_label(d.get("accelerateType")), preferred_foot=FOOT.get(d.get("foot")),
                card_image_url=card, nationality=None,
                source=f"fut.gg /api/fut/player-item-definitions/{g}/{ea}/ (base 아이템, createdAt {d.get('createdAt','')[:10]}, "
                       f"{a.pulled} 수집, collect_futgg_history.py) · 카드/클럽 /api/fut/players/v2/{g}/?ea_ids={ea}",
                confidence=(f"MEDIUM-HIGH — ⭐ fut.gg base 아이템은 **{gv} 출시판 값**이다(라이브 갱신 미반영; 실증 왓킨스 FC26 base 84 = fut.gg Δ 기준 "
                            f"출시판 ↔ sofifa 시즌말 82). roster_date는 아이템 createdAt(EA 공개일). club은 {gv} DB 기준 소속. "
                            f"GK 6종합은 DIV/HAN/KIC/REF/SPD/POS 순으로 pac~phy에 적재(기존 행 규약). pot·가치·traits·역할숙련은 이 API에 없어 NULL(결손)."),
            )
            if a.dry_run:
                print(f"  [{gv}] {kr}: OVR {row['ovr']} {row['positions']} {row['roster_date']} {row['club']} PS={row['playstyles']}")
            else:
                cur.execute("""INSERT INTO player_game_stats(game_version, roster_date, player_id, name_kr, sofifa_id, sofifa_name, club,
                               positions, best_pos, age, height_cm, weight_kg, ovr, pot, pac, sho, pas, dri, def, phy, attrs, playstyles,
                               accelerate, preferred_foot, card_image_url, source, confidence)
                               VALUES(:game_version,:roster_date,:player_id,:name_kr,:sofifa_id,:sofifa_name,:club,:positions,:best_pos,:age,
                               :height_cm,:weight_kg,:ovr,:pot,:pac,:sho,:pas,:dri,:def_,:phy,:attrs,:playstyles,:accelerate,:preferred_foot,
                               :card_image_url,:source,:confidence)
                               ON CONFLICT(game_version, roster_date, name_kr) DO NOTHING""", row)
            ins += 1
    if not a.dry_run:
        con.commit()
    print(f"\n적재 {ins}행 · 기존 {skip}행 건너뜀 · players.sofifa_id 채움 {id_fill}")
    if miss:
        print(f"⚠️ 카드 없음(결손, NULL 유지) {len(miss)}건: " + ", ".join(f"{k}[{g}]" for k, g in miss))
    if mismatch:
        print("⛔ 동일성 불일치 — 적재하지 않음(사람이 판정):")
        for m in mismatch:
            print("   ", m)
    print("\n다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
