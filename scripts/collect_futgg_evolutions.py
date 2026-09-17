#!/usr/bin/env python3
"""FC 진화(Evolutions) 경로 수집 — fut.gg paths API (2026-09-17 신설).

왜 (사용자 지시 2026-09-17 「어떻게 진화하면 좋을지도 수집해서 페이지 내에서 최적의 제안을 보여줘」):
  진화는 **내가 적용하면 생기는 결과**라 발매 카드(`player_card_items`)와 층이 다르다. 한 선수에게
  경로 후보가 여럿 붙고 각 후보는 단계·비용·속성 델타·결과 카드를 갖는다.

경로: `/api/fut/evolutions/v2/{game}/paths/v2/{basePlayerEaId}/`
  ⚠️ **base eaId만 받는다** — 특별 카드 id는 404다(2026-09-17 실증: 이강인 OTW 50575428 → "Not found").
  ⚠️ 진화는 **기간제**다 — `pulled`가 정본이고 재수집은 덮지 않고 날짜별로 쌓는다(UNIQUE에 pulled 포함).

⭐ 2026-09-17 확장(migration 036): 응답에 박힌 **진화 객체를 `fc_evolutions` 카탈로그로도 적재**하고(요구조건·단계별
   업그레이드·마감·해금 경로 — 별도 카탈로그 API는 404), 경로마다 **단계별 결과 카드 `path_json`**을 남긴다.
   같은 pulled 행이 이미 있으면 path_json/path_choices만 갱신한다(사실 보강, 덮어쓰기 아님).

⛔ **「최적」 판정은 여기서 하지 않는다.** 이 스크립트는 사실(경로·비용·델타·결과 카드)만 적재하고,
   추천은 화면이 그 선수의 처방 역할과 대조해 만든다 — 처방이 바뀌면 추천도 바뀌어야 하기 때문이다.

사용:
    .venv/bin/python scripts/collect_futgg_evolutions.py --dry-run
    .venv/bin/python scripts/collect_futgg_evolutions.py --games 27
    .venv/bin/python scripts/collect_futgg_evolutions.py --games 27 --team AVL
"""
import argparse
import datetime as dt
import json
import sqlite3
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "tactics.db"
UA = {"User-Agent": "Mozilla/5.0"}
API = "https://www.fut.gg/api/fut"

# fut.gg 정의 필드 → 한글 라벨. `player_game_stats.attrs`·`player_card_items.attrs`와 **같은 키**를 쓴다.
ATTR_KR = {
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
SIX = [("facePace", "PAC"), ("faceShooting", "SHO"), ("facePassing", "PAS"),
       ("faceDribbling", "DRI"), ("faceDefending", "DEF"), ("facePhysicality", "PHY")]
SIX_GK = [("gkFaceDiving", "DIV"), ("gkFaceHandling", "HAN"), ("gkFaceKicking", "KIC"),
          ("gkFaceReflexes", "REF"), ("gkFaceSpeed", "SPD"), ("gkFacePositioning", "POS")]


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


def six_of(card):
    """6대 스탯 — GK는 DIV/HAN/KIC/REF/SPD/POS 순(다른 표와 같은 규약)."""
    keys = SIX_GK if card.get("position") == 0 else SIX
    return {label: card.get(k) for k, label in keys}


IMG = "https://game-assets.fut.gg/cdn-cgi/image/quality=85,format=auto,width=300/"


def step_of(card, i, playstyle):
    """경로 한 단계의 결과 카드 요약 — 화면이 「적용하면 무엇이 되는지」를 그대로 그린다. ⚠️ path[0]은 **적용 전 기준 카드**(step 0)."""
    ps = [playstyle.get(x, f"PS#{x}") for x in card.get("playstyles") or []] + \
         [playstyle.get(x, f"PS#{x}") + "+" for x in card.get("playstylesPlus") or []]
    return dict(step=i, evo_id=card.get("evolutionId"), ovr=card.get("overall"), six=six_of(card),
                position=card.get("position"), playstyles=ps,
                roles_plus=card.get("rolesPlus") or [], roles_plus_plus=card.get("rolesPlusPlus") or [],
                card_image_url=(IMG + card["cardImagePath"]) if card.get("cardImagePath") else None)


def catalog_row(e, gv, pulled):
    unlock = e.get("customUnlockable") or e.get("sbcName") or e.get("objectiveGroupName")
    return dict(
        game_version=gv, evo_id=e["id"], name=e.get("name") or "", slug=e.get("slug"),
        url=("https://www.fut.gg" + e["url"]) if e.get("url") else None, description=e.get("description"),
        category=e.get("categoryName"), unlock_text=unlock,
        coins_cost=e.get("coinsCost"), points_cost=e.get("pointsCost"), token_cost=e.get("tokenCost"),
        repeatability=e.get("repeatabilityCount"), is_reward=1 if e.get("isRewardEvolution") else 0,
        is_gk=1 if e.get("isGkEvolution") else 0, is_timed=1 if e.get("isTimed") else 0,
        training_time=e.get("totalTrainingTime"), created_at=e.get("createdAt"),
        end_time=e.get("endTime"), end_submission_time=e.get("endSubmissionTime"),
        requirements_text=json.dumps(e.get("requirementsText") or [], ensure_ascii=False),
        total_upgrades_text=json.dumps(e.get("totalUpgradesText") or [], ensure_ascii=False),
        levels=json.dumps(e.get("levels") or [], ensure_ascii=False),
        allowed_prior_ids=json.dumps(e.get("allowedPriorEvolutionIds") or []),
        number_of_players=e.get("numberOfPlayers"), is_expired=1 if e.get("isExpired") else 0,
        source=f"fut.gg paths API 응답에 내장된 evolution 객체 ({pulled} 수집, collect_futgg_evolutions.py)",
        confidence="HIGH — fut.gg가 EA 정의를 그대로 노출한다. ⚠️ 기간제 — end_time 이후는 사실이 아니다.",
        pulled=pulled)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", nargs="*", default=["27"], choices=["25", "26", "27"])
    ap.add_argument("--team", nargs="*", default=[], help="regime team_code로 대상 한정")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--fill-catalog", action="store_true",
                    help="우리 선수가 하나도 해당되지 않는 진화도 카탈로그에 넣는다(목록 페이지 id → fut.gg 적용가능 선수 1명의 paths)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    playstyle = {x["eaId"]: x["name"] for x in (get(f"{API}/playstyles/") or {}).get("data", [])}
    catalog = {}                                   # (gv, evo_id) → 행 — 여러 선수 응답에 같은 진화가 반복된다
    for gv in [f"FC{g}" for g in a.games]:
        q = ("SELECT DISTINCT c.player_id, c.name_kr, c.base_ea_id FROM player_card_items c "
             "WHERE c.game_version=? AND c.base_ea_id IS NOT NULL")
        params = [gv]
        if a.team:
            q += (" AND c.player_id IN (SELECT se.player_id FROM squad_entries se "
                  "JOIN regimes r ON r.id=se.regime_id WHERE r.team_code IN (%s))"
                  % ",".join("?" * len(a.team)))
            params += a.team
        targets = cur.execute(q + " ORDER BY c.name_kr", params).fetchall()
        print(f"{gv} 대상 {len(targets)}명 (base eaId 보유분)")

        ins = skip = 0
        no_path, errs = [], []
        for t in targets:
            ea, kr, pid = t["base_ea_id"], t["name_kr"], t["player_id"]
            d = get(f"{API}/evolutions/v2/{gv[2:]}/paths/v2/{ea}/")
            if d is None or "data" not in d:
                errs.append(kr)
                continue
            paths = d["data"]
            if not paths:
                no_path.append(kr)
                continue
            for p in paths:
                evos = p.get("evolutions") or []
                if not evos:
                    continue
                for e in evos:
                    catalog.setdefault((gv, e["id"]), catalog_row(e, gv, a.pulled))
                ids = [e.get("id") for e in evos]
                key = ">".join(str(i) for i in ids)
                chain = p.get("path") or []
                start, end = (chain[0] if chain else {}), (chain[-1] if chain else {})
                up = {ATTR_KR[k]: v for k, v in (p.get("upgrades") or {}).items()
                      if k in ATTR_KR and v}
                row = dict(
                    game_version=gv, player_id=pid, base_ea_id=ea, name_kr=kr, path_key=key,
                    evolution_ids=json.dumps(ids),
                    evolution_names=" → ".join((e.get("name") or "") for e in evos),
                    evolution_urls="\n".join("https://www.fut.gg" + (e.get("url") or "") for e in evos),
                    steps=len(evos),
                    coins_cost=p.get("coinsCost"), points_cost=p.get("pointsCost"),
                    training_time=p.get("totalTrainingTime"),
                    is_expired=1 if p.get("isExpired") else 0,
                    ovr_before=start.get("overall"), ovr_after=end.get("overall"),
                    upgrades=json.dumps(up, ensure_ascii=False) if up else None,
                    six_before=json.dumps(six_of(start), ensure_ascii=False) if start else None,
                    six_after=json.dumps(six_of(end), ensure_ascii=False) if end else None,
                    playstyles_after=json.dumps(end.get("playstyles") or []),
                    roles_plus_after=json.dumps(end.get("rolesPlus") or []),
                    roles_plus_plus_after=json.dumps(end.get("rolesPlusPlus") or []),
                    path_json=json.dumps([step_of(c, i, playstyle) for i, c in enumerate(chain)], ensure_ascii=False),   # step 0 = 기준 카드
                    path_choices=json.dumps(p.get("evolutionPathChoices") or []),
                    source=(f"fut.gg {API}/evolutions/v2/{gv[2:]}/paths/v2/{ea}/ "
                            f"({a.pulled} 수집, collect_futgg_evolutions.py)"),
                    confidence=("MEDIUM-HIGH — fut.gg가 EA 데이터에서 계산한 경로다. ⚠️ **진화는 기간제**라 "
                                "`pulled` 시점의 스냅샷이고 만료되면 사라진다. ⛔ 「최적」 판정은 이 행에 없다 — "
                                "화면이 그 선수의 처방 역할과 대조해 만든다."),
                    pulled=a.pulled)
                if a.dry_run:
                    print(f"  {kr:14} {row['evolution_names'][:52]:52} OVR {row['ovr_before']}→{row['ovr_after']}")
                    ins += 1
                    continue
                cols = ",".join(row)
                cur.execute(
                    f"INSERT INTO player_evolutions({cols}) VALUES({','.join('?' * len(row))}) "
                    "ON CONFLICT(game_version, base_ea_id, path_key, pulled) "
                    "DO UPDATE SET path_json=excluded.path_json, path_choices=excluded.path_choices "
                    "WHERE player_evolutions.path_json IS NULL",
                    tuple(row.values()))
                ins += cur.rowcount
                skip += 1 - cur.rowcount
        if not a.dry_run:
            con.commit()
        print(f"  적재 {ins}행 · 기존 {skip}행 · 경로 없음 {len(no_path)}명 · 조회 실패 {len(errs)}명")
        if no_path:
            print("  경로 없음:", ", ".join(no_path[:25]) + (" …" if len(no_path) > 25 else ""))
        if errs:
            print("  ⚠️ 조회 실패:", ", ".join(errs))
    if a.fill_catalog:
        # 우리 선수 응답에 안 나온 진화(예: 2491·2495)는 목록 페이지의 id를 긁어 fut.gg 적용가능 선수 1명의 paths로 객체를 받는다.
        import re
        for g in a.games:
            gv = f"FC{g}"
            try:
                with urllib.request.urlopen(urllib.request.Request("https://www.fut.gg/evolutions/", headers=UA), timeout=30) as r:
                    html = r.read().decode("utf-8", "ignore")
            except Exception:
                html = ""
            ids = sorted({int(x) for x in re.findall(r"/evolutions/(\d+)-", html)})
            missing = [i for i in ids if (gv, i) not in catalog]
            for eid in missing:
                el = get(f"{API}/evolutions/v2/{g}/v2/players/?evolutions_combinations={eid}&hide_combinations=true"
                         "&hide_reward_evolutions=false&show_non_upgraded_players=false")
                for it in (el or {}).get("data", [])[:5]:
                    d = get(f"{API}/evolutions/v2/{g}/paths/v2/{it.get('eaId')}/")
                    found = False
                    for pth in (d or {}).get("data", []):
                        for e in pth.get("evolutions") or []:
                            if e["id"] == eid:
                                catalog[(gv, eid)] = catalog_row(e, gv, a.pulled); found = True
                    if found:
                        break
            print(f"카탈로그 보강: 목록 {len(ids)}종 · 우리 선수 응답 밖 {len(missing)}종 → "
                  f"{sum(1 for i in missing if (gv, i) in catalog)}종 확보")
    if catalog and not a.dry_run:
        n = 0
        for row in catalog.values():
            cols = ",".join(row)
            cur.execute(f"INSERT INTO fc_evolutions({cols}) VALUES({','.join('?' * len(row))}) "
                        "ON CONFLICT(game_version, evo_id, pulled) DO NOTHING", tuple(row.values()))
            n += cur.rowcount
        con.commit()
        print(f"진화 카탈로그: 응답에서 {len(catalog)}종 발견 · 신규 {n}행 (fc_evolutions)")
    print("\n다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
