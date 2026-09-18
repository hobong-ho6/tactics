#!/usr/bin/env python3
"""관리 선수의 FC 카드 버전 수집 — fut.gg all-versions API (2026-09-14 신설).

왜 (사용자 지시 2026-09-14 「관리중인 선수들의 FC27 새 카드가 나오면 그 카드 정보도 확인할 수 있게」):
  `player_game_stats`는 **base(기본) 카드 = 능력치 정본**만 담는다. 시즌이 열리면 같은 선수에게
  TOTW·이벤트 카드가 계속 붙는데, 그건 능력치 정본이 아니라 **별도 아이템**이다.
  `/api/fut/players/v2/all-versions/{basePlayerEaId}/`가 한 응답에 그 선수의 **전 버전·전 카드**를
  6대 스탯·34속성·PlayStyles(+)·Role+/++·스킬무브·약발까지 붙여서 준다(curl 200, 브라우저 불필요).

⚠️ 희귀도 이름(`rarityName`)만 이 응답에 없다 — 목록 API `/api/fut/players/v2/{game}/?ea_ids=…`에서
   따로 받아 채운다(한 번에 여러 id 조회 가능).
⛔ **Role+/++는 raw id로만 적재한다** — FC27 역할 카탈로그(`/api/fut/roles/`)가 09-18 전까지 미공개라
   id→이름을 발명할 수 없다(docs/21 ②). 카탈로그가 열리면 이름 해석은 그때 붙인다.
⚠️ base eaId는 `player_game_stats`의 FC27 `card_image_url`(`27-{eaId}`)에서 회수한다 — 그 값이
   오염되면 남의 카드를 긁어온다(09-14 다트로↔웨슬리 포파나 실증) ⇒ 응답의 `basePlayerEaId`와
   우리 id가 다르면 적재하지 않고 보고한다.

사용:
    .venv/bin/python scripts/collect_futgg_cards.py --dry-run
    .venv/bin/python scripts/collect_futgg_cards.py --games 27
    .venv/bin/python scripts/collect_futgg_cards.py --games 26 27 --team AVL
"""
import argparse
import datetime as dt
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DB = ROOT / "db" / "tactics.db"

from scripts.collect_futgg_history import (  # noqa: E402  같은 소스·같은 라벨 매핑을 재사용한다
    API, ATTR_MAP, FOOT, GK_ATTRS, OUTFIELD_DROP, POS, accelerate_label, get,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", nargs="*", default=["27"], help="적재할 게임 버전(기본 27)")
    ap.add_argument("--team", nargs="*", default=[], help="regime team_code로 대상 한정")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    playstyle = {x["eaId"]: x["name"] for x in get(f"{API}/playstyles/")["data"]}

    # 대상: 현 스쿼드 전원 × FC27 base 카드에서 회수한 eaId
    q = """SELECT DISTINCT g.player_id, g.name_kr, g.card_image_url
           FROM player_game_stats g
           JOIN squad_entries se ON se.player_id=g.player_id
           JOIN regimes r ON r.id=se.regime_id
           WHERE g.game_version='FC27' AND g.card_image_url LIKE '%/27-%'"""
    if a.team:
        q += " AND r.team_code IN (%s)" % ",".join("?" * len(a.team))
    targets = {}
    for r in con.execute(q, a.team):
        m = re.search(r"/27-(\d+)\.", r["card_image_url"])
        if m:
            targets[int(m.group(1))] = (r["player_id"], r["name_kr"])
    # ⭐ 2026-09-17 폴백(사용자 지시 「게임카드 없는 선수들은 모두 모으고」): FC27 game_stats에 카드 URL이 없는 스쿼드 선수는
    #    이름 검색 API로 base eaId를 찾는다. ⛔ 남자(gender==1)·이름 토큰 교차·**유일 일치**일 때만 받는다(obs#616 로렌 제임스 사고).
    q2 = """SELECT DISTINCT p.id, COALESCE(p.name_kr, p.name) kr, p.name en
            FROM squad_entries se JOIN regimes r ON r.id=se.regime_id AND r.end IS NULL
            JOIN players p ON p.id=se.player_id
            WHERE p.id NOT IN (SELECT player_id FROM player_game_stats WHERE game_version='FC27' AND card_image_url LIKE '%/27-%')"""
    if a.team:
        q2 += " AND r.team_code IN (%s)" % ",".join("?" * len(a.team))
    unresolved = []
    for r in con.execute(q2, a.team):
        toks = [t for t in re.split(r"[\s\-]+", (r["en"] or "").lower()) if len(t) > 2]
        hit = {}
        for tok in (toks[-1:] or toks):
            for it in (get(f"{API}/players/v2/27/?name={tok}") or {}).get("data", []):
                if it.get("gender") != 1:
                    continue
                full = f"{it.get('firstName','')} {it.get('lastName','')} {it.get('commonName') or ''}".lower()
                if all(t in full for t in toks):
                    hit[it.get("basePlayerEaId")] = it.get("commonName") or it.get("lastName")
        if len(hit) == 1:
            ea = next(iter(hit)); targets[ea] = (r["id"], r["kr"])
            print(f"  검색 폴백: {r['kr']} → base {ea} ({hit[ea]})")
        else:
            unresolved.append((r["kr"], r["en"], list(hit.values())[:4]))
    if unresolved:
        print("  ⚠️ 검색 폴백 미해결(유일 일치 아님):", unresolved)
    if not a.team:      # 팀 한정 실행이 아니면 **내 구단 보유분**도 함께 본다(2026-09-19 사용자 지시)
        for r in con.execute("""SELECT DISTINCT c.base_ea_id, COALESCE(c.name_kr, f.name) kr, c.player_id
                                FROM fut_club_players f JOIN player_card_items c ON c.ea_item_id=f.ea_item_id
                                WHERE f.status='owned' AND c.base_ea_id IS NOT NULL"""):
            targets.setdefault(r["base_ea_id"], (r["player_id"], r["kr"]))
        # 우리 카드 표에 없는 보유 선수는 **아이템 id를 base 후보로** 넣는다 — 대부분 base 카드다.
        # ⚠️ 특별 카드면 all-versions 응답의 basePlayerEaId가 달라 기존 mismatch 가드가 걸러낸다(적재하지 않고 보고).
        for r in con.execute("""SELECT f.ea_item_id, f.name FROM fut_club_players f
                                WHERE f.status='owned' AND f.ea_item_id IS NOT NULL
                                  AND f.ea_item_id NOT IN (SELECT ea_item_id FROM player_card_items)"""):
            targets.setdefault(r["ea_item_id"], (None, r["name"]))
    print(f"대상 {len(targets)}명 · 게임 {a.games}")

    cur = con.cursor()
    rows, mismatch = [], []
    for ea, (pid, kr) in sorted(targets.items(), key=lambda x: x[1][1]):
        d = get(f"{API}/players/v2/all-versions/{ea}/")
        for it in (d or {}).get("data", []):
            if str(it.get("game")) not in a.games:
                continue
            if it.get("basePlayerEaId") != ea:
                mismatch.append((kr, ea, it.get("eaId"), it.get("basePlayerEaId")))
                continue
            gk = it.get("position") == 0
            attrs = {ATTR_MAP[k]: it[k] for k in ATTR_MAP if it.get(k) is not None}
            attrs = {k: v for k, v in attrs.items() if (k in GK_ATTRS if gk else k not in OUTFIELD_DROP)}
            ps = [playstyle.get(i, f"PS#{i}") for i in it.get("playstyles") or []] + \
                 [playstyle.get(i, f"PS#{i}") + "+" for i in it.get("playstylesPlus") or []]
            positions = "/".join([POS.get(it.get("position"), str(it.get("position")))] +
                                 [POS.get(i, str(i)) for i in it.get("alternativePositionIds") or []])
            six = ([it.get("gkFaceDiving"), it.get("gkFaceHandling"), it.get("gkFaceKicking"),
                    it.get("gkFaceReflexes"), it.get("gkFaceSpeed"), it.get("gkFacePositioning")] if gk else
                   [it.get("facePace"), it.get("faceShooting"), it.get("facePassing"),
                    it.get("faceDribbling"), it.get("faceDefending"), it.get("facePhysicality")])
            rows.append(dict(
                game_version=f"FC{it['game']}", ea_item_id=it["eaId"], base_ea_id=ea,
                is_base=1 if it["eaId"] == ea else 0, player_id=pid, name_kr=kr,
                rarity_ea_id=it.get("rarityEaId"), rarity_name=None,
                released_at=(it.get("createdAt") or "")[:10] or None, club=None,
                positions=positions, best_pos=positions.split("/")[0] if positions else None,
                ovr=it.get("overall"), pac=six[0], sho=six[1], pas=six[2], dri=six[3], def_=six[4], phy=six[5],
                attrs=json.dumps(attrs, ensure_ascii=False) if attrs else None,
                playstyles=", ".join(ps) or None,
                roles_plus=json.dumps(it.get("rolesPlus") or []),
                roles_plus_plus=json.dumps(it.get("rolesPlusPlus") or []),
                skill_moves=it.get("skillMoves"), weak_foot=it.get("weakFoot"),
                accelerate=accelerate_label(it.get("accelerateType")), preferred_foot=FOOT.get(it.get("foot")),
                # 이미지: 목록 API cardImageUrl이 우선이고, 없으면 정의의 cardImagePath로 만든다(2026-09-17 — 20장이 NULL이었다)
                card_image_url=("https://game-assets.fut.gg/cdn-cgi/image/quality=85,format=auto,width=300/" + it["cardImagePath"])
                               if it.get("cardImagePath") else None,
                futgg_url=it.get("url"),
                acquisition=None, is_special=None, first_seen=a.pulled,   # 획득 경로·특별카드 여부는 아래 목록 API에서 채운다
                source=f"fut.gg /api/fut/players/v2/all-versions/{ea}/ ({a.pulled} 수집, collect_futgg_cards.py)",
                confidence="HIGH — EA 확정 아이템 정의. ⛔ Role+/++는 카탈로그 미공개라 raw id 목록이다(docs/21 ②).",
            ))

    # 희귀도 이름·클럽·카드 이미지는 목록 API에서(버전별로 묶어 한 번에)
    for gv in {r["game_version"] for r in rows}:
        ids = [r["ea_item_id"] for r in rows if r["game_version"] == gv]
        meta = {}
        for i in range(0, len(ids), 40):
            lst = get(f"{API}/players/v2/{gv[2:]}/?ea_ids=" + ",".join(map(str, ids[i:i + 40])))
            for x in (lst or {}).get("data", []):
                meta[x.get("eaId")] = x
        for r in rows:
            if r["game_version"] != gv:
                continue
            m = meta.get(r["ea_item_id"], {})
            r["rarity_name"] = m.get("rarityName")
            # ⭐ 획득 경로 — SBC/목표가 아니면 팩·이적시장이다(2026-09-19).
            #    ⚠️ 목록 API 응답이 없는 아이템은 NULL로 남긴다 — 「미조회」와 「팩」을 구분해야 한다.
            if r["ea_item_id"] in meta:
                r["acquisition"] = "SBC" if m.get("isSbc") else "Objective" if m.get("isObjective") else "Pack/Market"
                r["is_special"] = 1 if m.get("isSpecial") else 0
            r["club"] = (m.get("club") or {}).get("name")
            r["card_image_url"] = m.get("cardImageUrl") or r["card_image_url"]

    known = {x[0] for x in con.execute("SELECT ea_item_id FROM player_card_items WHERE game_version IN (%s)"
                                       % ",".join(f"'FC{g}'" for g in a.games))}
    fresh = [r for r in rows if r["ea_item_id"] not in known]
    # ⭐ 「처음 본 카드」와 「새로 나온 카드」는 다르다 — 대상 명단을 넓히면 옛 카드도 처음 보인다.
    #    알림은 **발매일 기준 14일 이내**만 신규 발매로 올리고, 나머지는 수집 확장으로 따로 적는다.
    cutoff = (dt.date.fromisoformat(a.pulled) - dt.timedelta(days=14)).isoformat()
    released = [r for r in fresh if (r["released_at"] or "")[:10] >= cutoff]
    backfill = [r for r in fresh if r not in released]
    promo = [r for r in rows if not r["is_base"]]
    print(f"\n수집 {len(rows)}장 (base {len(rows)-len(promo)} · 프로모 {len(promo)})")
    for r in sorted(promo, key=lambda x: (-x["ovr"] or 0)):
        print(f"  {r['game_version']} {r['name_kr']:<14} OVR {r['ovr']:<3} {r['rarity_name'] or '?':<32} {r['released_at']}")
    HOW = {"SBC": "SBC(스쿼드 빌딩 챌린지)", "Objective": "목표(Objectives)", "Pack/Market": "팩 또는 이적시장"}
    if released:
        print(f"\n⭐ 신규 발매 카드 {len(released)}장 (발매 {cutoff} 이후):")
        for r in sorted(released, key=lambda x: -(x["ovr"] or 0)):
            print(f"   {r['name_kr']:<14} OVR {r['ovr']:<3} {r['rarity_name'] or '?':<26} "
                  f"{HOW.get(r['acquisition'], '획득 경로 미조회')} · 발매 {r['released_at']}")
    else:
        print("\n신규 발매 카드 없음(이번 회차)")
    if backfill:
        print(f"수집 범위 확장으로 처음 담긴 기존 카드 {len(backfill)}장 — 알림 대상 아님")
    if mismatch:
        print("⛔ basePlayerEaId 불일치 — 적재하지 않음(카드 URL 오염 의심):")
        for m in mismatch:
            print("   ", m)
    if a.dry_run:
        return

    cols = list(rows[0]) if rows else []
    # 채움 전용 upsert — 이미 있는 값은 덮지 않고 **빈 칸만** 메운다(사람 손·이전 수집을 덮지 않는다).
    sql = ("INSERT INTO player_card_items(%s) VALUES(%s) ON CONFLICT(game_version, ea_item_id) DO UPDATE SET "
           "card_image_url=COALESCE(player_card_items.card_image_url, excluded.card_image_url), "
           "acquisition=COALESCE(excluded.acquisition, player_card_items.acquisition), "
           "is_special=COALESCE(excluded.is_special, player_card_items.is_special), "
           "first_seen=COALESCE(player_card_items.first_seen, excluded.first_seen)"
           % (",".join("def" if c == "def_" else c for c in cols), ",".join(f":{c}" for c in cols)))
    before = con.execute("SELECT COUNT(*) FROM player_card_items").fetchone()[0]
    for r in rows:
        cur.execute(sql, r)
    con.commit()
    after = con.execute("SELECT COUNT(*) FROM player_card_items").fetchone()[0]
    print(f"\n적재 신규 {after-before}행 (기존 {before} → {after})")
    print("다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
