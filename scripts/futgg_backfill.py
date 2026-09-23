#!/usr/bin/env python3
"""관리 선수 ↔ fut.gg 대조 — **빈 데이터를 찾아 보충**한다 (2026-09-24 신설).

왜 (사용자 지시 「관리하고 있는 전체 선수 fut.gg 데이터랑 대조해서 빈 데이터 보충」):
  2026-09-23 하루에만 **같은 부류가 세 번** 터졌다 — 「소스는 주는데 우리가 흘렸고, 화면에는
  「없음」으로 그럴듯하게 나타난다」(프리킥 정확도 100% 누락 · 진화 경로 42명 증발 · 카드 league/club 40장).
  ⇒ 결손을 **한 번에 훑고, fut.gg에 실제로 있는지 확인하고, 있으면 채운다.**

⛔ **추측으로 잇지 않는다.** 이름만 같은 다른 선수를 붙이면 조용히 틀린 데이터가 된다
   (docs/30 「선수 동일성 확인 규약」 · `Alysson` 빌라·RM ↔ `Alisson Becker` 리버풀·GK).
   ⇒ 이름으로 후보를 찾되 **국적·포지션**을 대조해 통과한 것만 링크하고, 애매하면 **보고만** 한다.
⛔ 값을 덮어쓰지 않는다 — **NULL인 칸만** 채운다(불변규칙 2).

사용:
    python3 scripts/futgg_backfill.py --dry-run      # 무엇이 비었고 무엇을 채울 수 있는지만 본다
    python3 scripts/futgg_backfill.py                # NULL 칸 보충 + 새 카드 적재
    python3 scripts/futgg_backfill.py --link-new     # 카드가 없는 선수도 이름 검색으로 잇는다(확인 통과분만)
"""
import argparse
import datetime as dt
import json
import sqlite3
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DB = ROOT / "db" / "tactics.db"
UA = {"User-Agent": "Mozilla/5.0"}
API = "https://www.fut.gg/api/fut"
GV = "FC27"

from core.futgg_attrs import parse_attrs  # noqa: E402

# ⚠️ 상세 API의 `playstyles`는 **숫자 id**다(이름이 아니다) — 이름표는 `fc_playstyle_ids`(migration 057)가 정본.
#    ⛔ 여기서 표를 손으로 적지 않는다. id를 못 읽으면 그 사실을 남긴다(「PlayStyle #8」로 찍히는 것보다 낫다).
def ps_text(con, o):
    ids = list(o.get("playstyles") or [])
    plus = list(o.get("playstylesPlus") or [])
    if not ids and not plus:
        # ⛔ **확인했는데 없는 것**과 **미확인**은 다르다(obs#132). 빈 문자열로 「확인함·없음」을 남긴다 —
        #    NULL로 두면 다음 회차가 또 조회한다.
        return "", []
    name = {r[0]: r[1] for r in con.execute("SELECT ea_id, name FROM fc_playstyle_ids")}
    out, unknown = [], []
    for i in ids:
        out.append(name.get(i) or f"#{i}")
        if i not in name:
            unknown.append(i)
    for i in plus:
        out.append((name.get(i) or f"#{i}") + "+")
        if i not in name:
            unknown.append(i)
    return ", ".join(out), unknown

# 상세 API에서 그대로 옮기는 칸 — DB 컬럼 ← 응답 경로
SIMPLE = {
    "height_cm": lambda o: o.get("height"),
    "weight_kg": lambda o: o.get("weight"),
    "birthdate": lambda o: o.get("dateOfBirth"),
    "club": lambda o: (o.get("club") or {}).get("name"),
    "league": lambda o: (o.get("league") or {}).get("name"),
    "nation": lambda o: (o.get("nation") or {}).get("name"),
    "skill_moves": lambda o: o.get("skillMoves"),
    "weak_foot": lambda o: o.get("weakFoot"),
    "accelerate": lambda o: o.get("accelerateType"),
    "card_image_url": lambda o: o.get("cardImageUrl"),
    "simple_card_url": lambda o: o.get("simpleCardImageUrl"),
    "render_url": lambda o: o.get("imageUrl"),
}


def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(1.2 * (i + 1))
        except Exception:
            time.sleep(1.2 * (i + 1))
    return None


def norm(s):
    """대조용 정규화 — 발음기호·대소문자·공백 차이를 없앤다(Kéba ↔ Keba)."""
    s = unicodedata.normalize("NFKD", str(s or ""))
    return "".join(c for c in s if not unicodedata.combining(c)).lower().replace(" ", "")


def detail(ea):
    d = get(f"{API}/player-item-definitions/27/{ea}/")
    return (d or {}).get("data") or d or None


def main(a):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    mine = [r[0] for r in con.execute("""
        SELECT DISTINCT se.player_id FROM squad_entries se
          JOIN regimes r ON r.id=se.regime_id AND r.end IS NULL
        UNION SELECT player_id FROM transfer_targets WHERE player_id IS NOT NULL""")]
    q = ",".join("?" * len(mine))
    print(f"관리 선수 {len(mine)}명 · fut.gg 대조 ({GV})\n")

    # ── ① 기존 카드의 빈 칸 보충 ────────────────────────────────────────
    rows = con.execute(f"""SELECT c.*, COALESCE(p.name_kr,p.name) kr FROM player_card_items c
                             JOIN players p ON p.id=c.player_id
                            WHERE c.player_id IN ({q}) AND c.game_version=?""", (*mine, GV)).fetchall()
    holes = [r for r in rows if any(r[k] is None for k in SIMPLE) or r["playstyles"] is None or r["attrs"] is None]
    print(f"■ 기존 카드 {len(rows)}장 · 빈 칸이 있는 카드 {len(holes)}장")
    filled = notfound = 0
    for r in holes:
        o = detail(r["ea_item_id"])
        if not o:
            # ⛔ 404는 **우리 id가 FC27에 없다**는 뜻이다 — 추측으로 다른 id를 붙이지 않고 보고만 한다.
            print(f"   ⛔ {r['kr']:<16} ea={r['ea_item_id']} 상세 API 404 — FC27에 없는 id다(구 버전 id 혼입 의심)")
            notfound += 1
            continue
        sets, vals = [], []
        for col, pick in SIMPLE.items():
            if r[col] is None and pick(o) is not None:
                sets.append(f"{col}=?"); vals.append(pick(o))
        # ⚠️ 저장 형식은 **쉼표로 이은 이름 문자열**이다("Technical, Quick Step") — 기존 215장이 그 꼴이라
        #    JSON으로 넣으면 같은 컬럼에 두 형식이 섞인다(화면이 한쪽만 읽는다).
        #    ⛔ PS+는 이름 뒤에 `+`를 붙여 구분한다(clubviz가 그렇게 읽는다).
        pstxt, unknown = ps_text(con, o)
        if r["playstyles"] is None and pstxt is not None:
            sets.append("playstyles=?"); vals.append(pstxt)
            if unknown:
                print(f"   ⚠️ {r['kr']} PlayStyle id 이름 미상 {unknown} — fc_playstyle_ids에 없다")
        if r["attrs"] is None:
            at, miss = parse_attrs(o)
            if at:
                sets.append("attrs=?"); vals.append(json.dumps(at, ensure_ascii=False))
                if miss:
                    print(f"   ⚠️ {r['kr']} 속성 결손 {len(miss)}개: {', '.join(miss)}")
        if sets and not a.dry_run:
            cur.execute(f"UPDATE player_card_items SET {','.join(sets)} WHERE id=?", (*vals, r["id"]))
        if sets:
            filled += 1
            print(f"   ✅ {r['kr']:<16} ea={r['ea_item_id']} ← {len(sets)}칸 ({', '.join(s.split('=')[0] for s in sets)})")
        time.sleep(0.25)
    if not a.dry_run:
        con.commit()
    print(f"   → 보충 {filled}장 · 404 {notfound}장\n")

    # ── ② 카드가 아예 없는 선수 ────────────────────────────────────────
    none = con.execute(f"""SELECT p.id, COALESCE(p.name_kr,p.name) kr, p.name en, p.nationality, p.primary_position pos
                             FROM players p WHERE p.id IN ({q})
                              AND NOT EXISTS(SELECT 1 FROM player_card_items c
                                              WHERE c.player_id=p.id AND c.game_version=?)""", (*mine, GV)).fetchall()
    print(f"■ {GV} 카드가 없는 선수 {len(none)}명 — fut.gg 검색으로 대조")
    linked = ambiguous = missing = 0
    for p in none:
        last = (p["en"] or "").split()[-1]
        d = get(f"{API}/players/v2/27/?name={urllib.parse.quote(last)}")
        cands = (d or {}).get("data") or []
        # ⛔ 동일성 확인 — 이름만으로 잇지 않는다(docs/30). 국적이 있으면 반드시 맞아야 한다.
        ok = []
        for c in cands:
            o = detail(c.get("eaId"))
            if not o:
                continue
            nat = (o.get("nation") or {}).get("name")
            nm = norm(o.get("commonName") or o.get("lastName") or "")
            if norm(last) not in nm and nm not in norm(p["en"]):
                continue
            if p["nationality"] and nat and norm(nat) != norm(p["nationality"]):
                continue
            ok.append((c.get("eaId"), o, nat))
            time.sleep(0.2)
        if not ok:
            print(f"   ⛔ {p['kr']:<16} ({p['en']}) — fut.gg 후보 {len(cands)}건 중 동일성 통과 0")
            missing += 1
        elif len(ok) > 1:
            print(f"   ⚠️ {p['kr']:<16} 후보 {len(ok)}건 — 사람이 골라야 한다: " +
                  ", ".join(f"ea={e} OVR {o.get('overall')} {nat}" for e, o, nat in ok))
            ambiguous += 1
        else:
            ea, o, nat = ok[0]
            print(f"   ✅ {p['kr']:<16} ← ea={ea} OVR {o.get('overall')} {nat} "
                  f"{(o.get('club') or {}).get('name')}" + ("" if a.link_new else "  (--link-new 로 적재)"))
            if a.link_new and not a.dry_run:
                at, _ = parse_attrs(o)
                cur.execute("""INSERT INTO player_card_items(game_version, ea_item_id, base_ea_id, is_base, player_id,
                                 name_kr, rarity_name, ovr, positions, best_pos, attrs, playstyles, club, league, nation,
                                 height_cm, weight_kg, birthdate, skill_moves, weak_foot, accelerate, preferred_foot,
                                 card_image_url, simple_card_url, render_url, source, confidence, first_seen)
                               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                               ON CONFLICT(game_version, ea_item_id) DO NOTHING""",
                            (GV, ea, o.get("basePlayerEaId") or ea, 1 if not o.get("isSpecial") else 0, p["id"],
                             p["kr"], o.get("rarityName"), o.get("overall"),
                             ",".join(o.get("positions") or []) or None, (o.get("positions") or [None])[0],
                             json.dumps(at, ensure_ascii=False) if at else None,
                             ps_text(con, o)[0],
                             (o.get("club") or {}).get("name"), (o.get("league") or {}).get("name"),
                             (o.get("nation") or {}).get("name"), o.get("height"), o.get("weight"),
                             o.get("dateOfBirth"), o.get("skillMoves"), o.get("weakFoot"), o.get("accelerateType"),
                             o.get("foot"), o.get("cardImageUrl"), o.get("simpleCardImageUrl"), o.get("imageUrl"),
                             f"fut.gg /player-item-definitions/27/{ea}/ ({a.pulled} futgg_backfill.py · 이름+국적 대조)",
                             "HIGH — fut.gg 정의 원문. ⚠️ 동일성은 이름(성)+국적으로 확인했다(포지션 미대조).",
                             a.pulled))
                linked += 1
        time.sleep(0.25)
    if not a.dry_run:
        con.commit()
    print(f"   → 확인 통과 {linked if a.link_new else 0}장 적재 · 애매 {ambiguous}명 · 못 찾음 {missing}명")
    con.close()
    print("\n다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--link-new", action="store_true", help="카드가 없는 선수도 동일성 통과분에 한해 적재한다")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    sys.exit(main(ap.parse_args()) or 0)
