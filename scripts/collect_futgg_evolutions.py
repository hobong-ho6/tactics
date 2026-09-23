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
import urllib.parse
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
                attrs={ATTR_KR[k]: card[k] for k in ATTR_KR if card.get(k) is not None},   # 34속성 — 역할 가중 점수의 원료
                position=card.get("position"), playstyles=ps,
                roles_plus=card.get("rolesPlus") or [], roles_plus_plus=card.get("rolesPlusPlus") or [],
                card_image_url=(IMG + card["cardImagePath"]) if card.get("cardImagePath") else None)


# ⛔⛔ **코스메틱 전용 진화는 적재하지 않는다** (2026-09-22 사용자 지시
#    「능력치나 플레이스타일 업그레이드 없이 카드 코스메틱만 바꾸는 진화는 제거하고 앞으로 등록하지 말아줘」).
#    실측(Ones to Watch Retro 18·19·20): 기준 카드 ↔ 적용 후가 **OVR·6대 스탯·Role+·Role++·PlayStyle 전부 동일**하고
#    바뀌는 것은 `rarity_id`(카드 겉모습)뿐이다.
#    ⚠️ 이걸 판정할 때 `player_evolutions.roles_plus_after`를 **증가분으로 읽지 말 것** — 「적용 후 상태」라서
#      원래 갖고 있던 Role+가 그대로 찍힌다. 2026-09-22에 그걸 이득으로 오독해 「코스메틱 아니다」로 잘못 보고했다.
#      **반드시 기준 카드(`player_card_items`)와 before/after로 대조**한다.
#    ⭐ 모르는 upgrade 키는 **실효로 간주**한다 — 놓쳐서 남기는 쪽이 잘못 지우는 쪽보다 안전하다.
COSMETIC_UPGRADES = {"rarity_id"}


def _upgrade_keys(e):
    out = set()
    for lv in (e.get("levels") or []):
        for u in (lv.get("upgrades") or []):
            out.add(u.get("upgrade"))
        for og in (lv.get("upgradeOptions") or []):
            src = og if isinstance(og, list) else (og.get("upgrades") or [])
            for u in src:
                out.add(u.get("upgrade"))
    return {k for k in out if k}


def is_cosmetic(e):
    """겉모습만 바꾸는 진화인가 — 업그레이드 키가 하나 이상이고 전부 코스메틱일 때만 True."""
    ks = _upgrade_keys(e)
    return bool(ks) and ks <= COSMETIC_UPGRADES


CATALOG_COLS = [
    "game_version", "evo_id", "name", "slug", "url", "description", "category", "unlock_text",
    "coins_cost", "points_cost", "token_cost", "repeatability", "is_reward", "is_gk", "is_timed",
    "training_time", "created_at", "end_time", "end_submission_time", "requirements_text",
    "total_upgrades_text", "levels", "allowed_prior_ids", "number_of_players", "is_expired",
    "source", "confidence", "pulled"]
# ⭐ 이월 행은 `carried_from`에 **언제 관측한 값인지**를 남긴다(migration 059) —
#    산문에만 적으면 화면이 실측과 구분하지 못한다. NULL = 그 회차에 직접 받은 값.


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
    ap.add_argument("--elig-all", action="store_true",
                    help="적용 가능 선수를 **우리 DB FC27 카드 전체**로 확인한다(약 31분). 기본은 내 구단 보유 카드(약 4분).")
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
        no_path, errs, skipped_cosmetic = [], [], set()
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
                    if is_cosmetic(e):
                        skipped_cosmetic.add(e.get("name") or str(e["id"]))
                        continue
                    catalog.setdefault((gv, e["id"]), catalog_row(e, gv, a.pulled))
                # ⛔ **경로 전체가 코스메틱이면 경로도 적재하지 않는다** — 안 그러면 카탈로그에선 빠졌는데
                #    「선수별 진화 패스」에는 남아 화면이 둘로 갈린다(2026-09-22 실측 210행).
                if all(is_cosmetic(e) for e in evos):
                    continue
                ids = [e.get("id") for e in evos]
                key = ">".join(str(i) for i in ids)
                chain = p.get("path") or []
                start, end = (chain[0] if chain else {}), (chain[-1] if chain else {})
                up = {ATTR_KR[k]: v for k, v in (p.get("upgrades") or {}).items()
                      if k in ATTR_KR and v}
                if not up and len(chain) >= 2:      # fut.gg upgrades가 전부 0으로 오는 경로가 있다 — 결과 카드 − 기준 카드로 직접 낸다
                    up = {ATTR_KR[k]: end[k] - start[k] for k in ATTR_KR
                          if end.get(k) is not None and start.get(k) is not None and end[k] != start[k]}
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
                    "DO UPDATE SET path_json=excluded.path_json, path_choices=excluded.path_choices, "
                    "upgrades=COALESCE(player_evolutions.upgrades, excluded.upgrades) "
                    "WHERE player_evolutions.upgrades IS NULL OR player_evolutions.path_json NOT LIKE '%\"attrs\"%'",
                    tuple(row.values()))
                ins += cur.rowcount
                skip += 1 - cur.rowcount
        if not a.dry_run:
            con.commit()
        # ⭐ PlayStyle id→이름을 **누적 표에 덧칠**한다(migration 057) — 역산은 표본이 줄면 함께 줄기 때문이다.
        cand = {}
        for r in cur.execute("SELECT playstyles_after, path_json FROM player_evolutions WHERE playstyles_after IS NOT NULL").fetchall():
            try:
                ids = json.loads(r[0] or "[]")
                pj = json.loads(r[1] or "[]")
                names = (pj[-1].get("playstyles") if pj else None) or []
            except Exception:
                continue
            if not ids or len(ids) != len(names):
                continue
            for i in ids:
                c = cand.setdefault(i, {})
                for nm in names:
                    c[nm] = c.get(nm, 0) + 1
        added = 0
        for i, c in cand.items():
            top = max(c.values())
            best = [nm for nm, v in c.items() if v == top]
            if len(best) != 1:
                continue
            added += cur.execute(
                """INSERT INTO fc_playstyle_ids(game_version,ea_id,name,source,confidence,pulled)
                   VALUES(?,?,?,?,?,?) ON CONFLICT(game_version,ea_id) DO NOTHING""",
                (gv, i, best[0],
                 "player_evolutions id↔이름 교차 역산 (collect_futgg_evolutions.py)",
                 "HIGH — 동률이면 확정하지 않는다.", a.pulled)).rowcount
        if added:
            print(f"  🔤 PlayStyle 이름표 신규 {added}개(누적 표에 덧칠)")
        print(f"  적재 {ins}행 · 기존 {skip}행 · 경로 없음 {len(no_path)}명 · 조회 실패 {len(errs)}명")
        if skipped_cosmetic:
            print(f"  🎨 코스메틱 전용이라 제외 {len(skipped_cosmetic)}종: {', '.join(sorted(skipped_cosmetic))}")
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
            # ⭐⭐ 단독·특별카드 전용 진화는 **어떤 API로도 객체를 못 받는다**(2026-09-23 실측: 2495·2501).
            #    「적용 가능 선수」는 30명+ 응답하는데 그 선수들의 paths는 404거나, 200이어도 그 evo_id가 없다.
            #    ⇒ 목록에는 살아 있는데 이번 회차에 못 받았다면 **직전 행을 이월**한다.
            #    이월하지 않으면 export가 최신 pulled 스냅샷만 내보내므로 **화면에서 통째로 사라진다**
            #    (2026-09-23에 실제로 Pinged Pass·Relentless가 사라졌다 — 둘 다 마감 아니었다).
            # ⛔ 목록에서 빠진 종은 이월하지 않는다 — 그래야 마감 감지가 산다.
            carried = []
            for eid in [i for i in ids if (gv, i) not in catalog]:
                prev = cur.execute(
                    f"SELECT {','.join(CATALOG_COLS)},carried_from FROM fc_evolutions "
                    "WHERE game_version=? AND evo_id=? ORDER BY pulled DESC LIMIT 1", (gv, eid)).fetchone()
                if not prev:
                    continue                       # 코스메틱 제외분 등 — 애초에 적재한 적 없는 종
                row = dict(zip(CATALOG_COLS, prev))
                row["pulled"] = a.pulled
                row["carried_from"] = prev["carried_from"] or prev["pulled"]   # 최초 관측일을 물고 간다
                row["source"] = (f"{row['source']} · {a.pulled} 이월 — fut.gg 목록에는 있으나 "
                                 "paths·적용가능선수 API가 객체를 주지 않는 단독/특별카드 전용 진화")
                row["confidence"] = (f"MEDIUM — 목록 생존만 {a.pulled}에 확인했다. 내용은 "
                                     f"{row['carried_from']} 관측값 그대로이고 그 뒤 변경 여부는 확인할 수 없다.")
                catalog[(gv, eid)] = row
                carried.append(f"{eid} {row['name']}")
            if carried:
                print(f"  ↪️ 이월 {len(carried)}종(목록 생존 · API 미제공): {', '.join(carried)}")
    if catalog and not a.dry_run:
        n = 0
        for row in catalog.values():
            cols = ",".join(row)
            cur.execute(f"INSERT INTO fc_evolutions({cols}) VALUES({','.join('?' * len(row))}) "
                        "ON CONFLICT(game_version, evo_id, pulled) DO NOTHING", tuple(row.values()))
            n += cur.rowcount
        con.commit()
        print(f"진화 카탈로그: 응답에서 {len(catalog)}종 발견 · 신규 {n}행 (fc_evolutions)")

    # ── ⭐⭐ 적용 가능 선수 (migration 058, 2026-09-22 · 2026-09-23 전면 교체) ─────────────
    # ⛔ **경로 축만으로는 진화가 닫히지 않는다.** `paths/v2`는 base 카드 기준 조합 경로만 주므로
    #    ⑴ 특별 카드에만 열리는 진화(음바예 `paths/v2/50406097/` → 404)와
    #    ⑵ paths 응답이 아예 만들지 않는 단독 진화(Relentless 2495)를 통째로 놓친다.
    #
    # ⛔⛔ **종전 방식(목록 앞 8페이지 훑기)은 조용한 절단이었다 — 2026-09-23에 버렸다.**
    #    진화 하나의 적용 가능 선수가 **3,600~42,000명**인데 240명만 보고 「우리 선수 0명」이라고
    #    단정하고 있었다. 있는 것을 없다고 말하는 종류의 오류라 「수집 안 됨」보다 나쁘다.
    # ⇒ **우리 쪽에서 묻는다**: `&name=<성>`으로 그 진화의 풀을 **직접 검색**해 우리 카드 id와 대조한다.
    #    ⚠️ 판정은 **이름이 아니라 `eaId` 일치**로 한다 — 동명이인이 섞여 온다.
    #
    # ⚠️ **범위를 좁혀 둔다: 기본은 내 구단 보유 카드**(2026-09-23 실측 27명 × 16종 = 약 3.7분).
    #    우리 DB의 FC27 카드 전체(224명)로 넓히면 **약 31분**이라 매 회차 돌리기엔 무겁다 —
    #    필요하면 `--elig-all`. 미보유 선수는 base 카드라 **경로 축이 이미 덮는다.**
    #    ⛔ 범위를 화면이 알 수 있게 `source`에 적는다 — 「확인 안 함」을 「해당 없음」으로 읽으면 안 된다.
    for g in a.games:
        gv = f"FC{g}"
        if a.elig_all:
            cards = list(con.execute(
                "SELECT c.ea_item_id, c.player_id, c.is_base, COALESCE(p.name_kr, p.name) kr, p.name en "
                "FROM player_card_items c JOIN players p ON p.id=c.player_id WHERE c.game_version=?", (gv,)))
            scope = "우리 DB FC27 카드 전체"
        else:
            cards = list(con.execute(
                "SELECT c.ea_item_id, c.player_id, c.is_base, COALESCE(p.name_kr, p.name) kr, p.name en "
                "FROM fut_club_players f JOIN player_card_items c ON c.ea_item_id=f.ea_item_id "
                "JOIN players p ON p.id=c.player_id "
                "WHERE f.status='owned' AND c.game_version=? AND c.player_id IS NOT NULL", (gv,)))
            scope = "내 구단 보유 카드"
        by_ea = {r["ea_item_id"]: r for r in cards}
        # 성(마지막 토큰)으로 묶어 요청을 아낀다 — 같은 성이면 한 번만 묻는다.
        surnames = {}
        for r in cards:
            surnames.setdefault((r["en"] or r["kr"] or "").split()[-1], []).append(r)
        evo_ids = [r[0] for r in con.execute(
            "SELECT DISTINCT evo_id FROM fc_evolutions WHERE game_version=? AND is_expired=0 "
            "AND pulled=(SELECT MAX(pulled) FROM fc_evolutions WHERE game_version=?)", (gv, gv))]
        elig, misses = [], 0
        for eid in evo_ids:
            for sur in surnames:
                if not sur:
                    continue
                el = get(f"{API}/evolutions/v2/{g}/v2/players/?evolutions_combinations={eid}"
                         f"&hide_combinations=true&hide_reward_evolutions=false"
                         f"&show_non_upgraded_players=false&name={urllib.parse.quote(sur)}")
                if el is None:
                    misses += 1
                    continue
                for it in (el.get("data") or []):
                    o = by_ea.get(it.get("eaId"))
                    if o:
                        elig.append((gv, eid, o["player_id"], it["eaId"], o["is_base"], a.pulled,
                                     f"fut.gg /evolutions/v2/{g}/v2/players/?evolutions_combinations={eid}&name={sur} "
                                     f"({a.pulled} 수집 · 범위: {scope})"))
        if elig and not a.dry_run:
            cur.executemany(
                "INSERT INTO fc_evolution_eligibility(game_version,evo_id,player_id,ea_item_id,is_base,pulled,source) "
                "VALUES(?,?,?,?,?,?,?) ON CONFLICT DO NOTHING", elig)
            con.commit()
        # 경로 축이 덮지 못한 쌍을 **건수로 보고한다** — 조용히 넘기면 같은 구멍이 다시 생긴다.
        covered = set()
        for pid, ids_json in con.execute(
                "SELECT player_id, evolution_ids FROM player_evolutions WHERE game_version=? AND pulled=?", (gv, a.pulled)):
            for i in json.loads(ids_json or "[]"):
                covered.add((pid, i))
        pairs = {(p, e) for (_, e, p, *_r) in elig}
        gap = pairs - covered
        print(f"적용 가능 선수[{scope}]: 진화 {len(evo_ids)}종 × 성 {len(surnames)}개 조회 "
              f"· (선수,진화) {len(pairs)}쌍 · 그중 **경로 축이 못 덮은 {len(gap)}쌍**(특별 카드 전용·단독 진화)"
              + (f" · ⚠️ 조회 실패 {misses}건" if misses else ""))

    print("\n다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
