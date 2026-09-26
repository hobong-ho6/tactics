#!/usr/bin/env python3
"""진화 단계 **역추정** — 「이 카드는 무슨 진화를 어디까지 밟았나」를 스탯으로 되짚는다.

왜 (2026-09-26 사용자 지시 「코드로 돌리지 않고 직접 클로드로 수행하는 건 뭐냐」→「모두진행」):
  fut.gg·EA 어느 쪽도 **적용된 진화 경로를 주지 않는다**
  (「GG Club tracks your players' final stats, but not the evolution path that created them.」).
  그래서 club-sync 런북 §3-2는 판정 순서를 이렇게 적어 뒀다:
    ⑴ 기준 카드(`player_card_items`) ↔ 클럽 카드의 **스탯 차이**
    ⑵ **카탈로그 단계별 보상과의 일치**
    ⑶ EA 실측 PlayStyle
  ⛔ 그런데 ⑴⑵는 **판단이 아니라 알고리즘**인데 지금까지 세션이 매 회차 손으로 풀었다.
     손으로 풀면 ⓐ 조합(갈림길)을 빠뜨리고 ⓑ 회차마다 결론이 달라질 수 있다.
  ⇒ 기계가 전수로 맞춰 보고, **사람은 ⑶과 「어느 쪽이 맞나」만 판단한다**(불변규칙 13 ④).

⛔⛔ **이 스크립트는 원장에 쓰지 않는다.** 후보를 제시할 뿐이다 —
   「스탯이 맞는다」는 **충분조건이 아니다**(다른 진화가 같은 결과를 낼 수 있다).
   기록은 사용자 확인 뒤 `fut_club.py evolve`로 한다(그쪽에 게이트가 있다).

사용:
    python3 scripts/evo_detect.py                 # 로그가 없는데 스탯이 변한 보유 카드 전부
    python3 scripts/evo_detect.py --player 30     # 한 장만
    python3 scripts/evo_detect.py --verify        # **이미 적힌 로그**가 현재 스탯을 설명하는지 검산
"""
import argparse
import itertools
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                        # noqa: E402
from core.futgg_attrs import apply_upgrades                # noqa: E402

MAX_COMBOS = 4096          # 갈림길 조합 상한 — 넘으면 그 진화는 「조합 과다」로 건너뛰고 **그 사실을 적는다**


def levels_of(con, evo_id):
    r = con.execute("SELECT levels FROM fc_evolutions WHERE evo_id=? ORDER BY pulled DESC", (evo_id,)).fetchone()
    return json.loads(r["levels"]) if r and r["levels"] else []


def step_sources(lv):
    """한 단계가 줄 수 있는 보상 묶음들. 갈림길이면 가지 수만큼, 아니면 한 개."""
    opts = lv.get("upgradeOptions") or []
    if opts:
        return [list(o if isinstance(o, list) else (o.get("upgrades") or [])) for o in opts]
    return [list(lv.get("upgrades") or [])]


def try_evo(base, target, lv_rows):
    """`base`에 이 진화를 1..n단계까지 얹어 `target`과 **29속성 전부** 맞는 조합을 찾는다.

    ⭐ 부분 일치도 돌려준다 — 완전 일치가 없을 때 「몇 개나 맞았나」가 다음 단서다.
    반환: [(맞은 단계수, picks, 불일치 속성 dict)] — 불일치 0이 정답 후보다.
    """
    out, combos = [], 1
    for lv in lv_rows:
        combos *= max(1, len(step_sources(lv)))
        if combos > MAX_COMBOS:
            return None                                    # 조합 과다 — 호출부가 사실로 적는다
    for n in range(1, len(lv_rows) + 1):
        picks_space = [range(len(step_sources(lv))) for lv in lv_rows[:n]]
        for picks in itertools.product(*picks_space):
            at = dict(base)
            for lv, k in zip(lv_rows[:n], picks):
                apply_upgrades(at, step_sources(lv)[k])
            # ⛔ **공통 키만 본다**(2026-09-26 실측). 기준 카드는 29속성인데 GG Club의
            #    `current_attrs`는 GK 5속성까지 34개라, 전부 대조하면 **언제나 불일치**가 나서
            #    정답을 아는 케이스(알리송 반복 배급 4단계)조차 「설명 안 됨」으로 나왔다.
            bad = {a: (at[a], target[a]) for a in target if a in at and at[a] != target[a]}
            out.append((n, list(picks), bad))
    out.sort(key=lambda x: (len(x[2]), x[0]))
    return out


def base_attrs(con, cp):
    """기준 카드의 29속성. ⚠️ 진화 아이템은 ea_item_id가 달라질 수 있어 `base_ea_id`로도 찾는다."""
    for sql, arg in (("SELECT attrs FROM player_card_items WHERE ea_item_id=?", cp["ea_item_id"]),
                     ("SELECT attrs FROM player_card_items WHERE player_id=? AND is_base=1", cp["player_id"])):
        if arg is None:
            continue
        r = con.execute(sql, (arg,)).fetchone()
        if r and r["attrs"]:
            return json.loads(r["attrs"])
    return None


def verify_chain(con, cp, cur, base):
    """**원장에 적힌 진화를 적힌 순서대로** 이어 붙여 현재 스탯을 설명하는지 본다.

    ⭐ 단일 탐색과 목적이 다르다 — 저쪽은 「무슨 진화였나」를 찾고, 이쪽은 「적어 둔 게 맞나」를 검산한다.
       보유 카드 대부분은 진화를 **여러 개 쌓았기** 때문에 단일 탐색은 당연히 실패한다(2026-09-26 실측 6장 중 5장).
    ⚠️ 갈림길을 고른 기록이 없던 옛 행이 있어, 가지는 **전수로 맞춰 본다**(조합이 상한을 넘으면 그 사실을 적는다).
    """
    rows = con.execute("""SELECT evo_id, level FROM fut_evolution_log
                           WHERE club_player_id=? AND is_void=0 ORDER BY applied_at, id""", (cp["id"],)).fetchall()
    if not rows:
        return None
    steps, combos = [], 1
    for r in rows:
        lv = next((x for x in levels_of(con, r["evo_id"]) if x.get("idx") == r["level"]), None)
        if lv is None:
            return ("미상", f"카탈로그에 evo#{r['evo_id']} {r['level']}단계가 없다")
        src = step_sources(lv)
        steps.append(src)
        combos *= len(src)
        if combos > MAX_COMBOS:
            return ("미상", f"갈림길 조합이 {MAX_COMBOS}개를 넘는다")
    best = None
    for picks in itertools.product(*[range(len(s)) for s in steps]):
        at = dict(base)
        for src, k in zip(steps, picks):
            apply_upgrades(at, src[k])
        bad = {a: (at[a], cur[a]) for a in cur if a in at and at[a] != cur[a]}
        if best is None or len(bad) < len(best[1]):
            best = (list(picks), bad)
        if not bad:
            break
    return best


def report(con, cp, catalog, verify):
    cur = json.loads(cp["current_attrs"]) if cp["current_attrs"] else None
    base = base_attrs(con, cp)
    name = cp["name"]
    if cur is None or base is None:
        print(f"  ⚪ {name}: 29속성이 없다(기준 카드 {'있음' if base else '없음'} · 현재 {'있음' if cur else '없음'}) — 판정 불가")
        return
    if not any(k in base and base[k] != cur[k] for k in cur):
        print(f"  ⚪ {name}: 기준 카드와 **똑같다** — 진화 흔적 없음")
        return
    diff = {k: (base[k], cur[k]) for k in cur if k in base and base[k] != cur[k]}
    print(f"\n■ {name} (보유 id {cp['id']}) — 기준 카드와 {len(diff)}개 속성이 다르다")
    logged = [r["evo_id"] for r in con.execute(
        "SELECT DISTINCT evo_id FROM fut_evolution_log WHERE club_player_id=? AND is_void=0", (cp["id"],))]
    if logged:
        print(f"   원장에 적힌 진화: {logged}")
    hits, skipped = [], []
    for evo_id, evo_name in catalog:
        lv_rows = levels_of(con, evo_id)
        if not lv_rows:
            continue
        res = try_evo(base, cur, lv_rows)
        if res is None:
            skipped.append(evo_name)
            continue
        n, picks, bad = res[0]
        if not bad:
            hits.append((evo_id, evo_name, n, picks))
    if hits:
        for evo_id, evo_name, n, picks in hits:
            pk = f" · 갈림길 {picks}" if any(p for p in picks) or len(picks) > 1 else ""
            mark = "✅" if evo_id in logged else "⭐ 원장에 없다"
            print(f"   {mark} {evo_name}(#{evo_id}) **{n}단계까지**{pk} 로 29속성이 전부 맞는다")
        if len(hits) > 1:
            print("   ⚠️ 후보가 여럿이다 — 스탯만으로는 못 가른다. PlayStyle(런북 §3-2 ⑶)이나 사용자 확인이 필요하다.")
    else:
        print("   ❌ 한 진화만으로는 설명되지 않는다 — 여러 진화가 쌓였거나 카탈로그에 없는 종류다.")
        print(f"      바뀐 속성: {', '.join(f'{k} {a}→{b}' for k, (a, b) in list(diff.items())[:8])}"
              + (f" 외 {len(diff)-8}" if len(diff) > 8 else ""))
    if skipped:
        print(f"   ⚠️ 조합이 {MAX_COMBOS}개를 넘어 건너뛴 진화: {', '.join(skipped[:5])}"
              + (f" 외 {len(skipped)-5}" if len(skipped) > 5 else ""))
    if verify and logged:
        ch = verify_chain(con, cp, cur, base)
        if ch is None:
            pass
        elif ch[0] == "미상":
            print(f"   ⚪ 사슬 검산 불가 — {ch[1]}")
        elif not ch[1]:
            print(f"   ✅ **원장에 적힌 진화를 순서대로 이으면 29속성이 전부 맞는다** (갈림길 {ch[0]})")
        else:
            print(f"   ⛔ **원장을 순서대로 이어도 {len(ch[1])}개가 안 맞는다** — 기록이 틀렸거나 싱크가 낡았다.")
            print("      " + " · ".join(f"{k} 계산 {a} ↔ EA {b}" for k, (a, b) in list(ch[1].items())[:6]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--player", type=int, help="fut_club_players.id 하나만")
    ap.add_argument("--verify", action="store_true", help="로그가 있는 카드도 포함해 **검산**한다")
    a = ap.parse_args()
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    catalog = [(r["evo_id"], r["name_kr"] or r["name"]) for r in con.execute(
        """SELECT evo_id, name, name_kr FROM fc_evolutions
            WHERE pulled=(SELECT MAX(pulled) FROM fc_evolutions) ORDER BY evo_id""")]
    q = """SELECT id, name, player_id, ea_item_id, current_attrs FROM fut_club_players
            WHERE status='owned' AND current_attrs IS NOT NULL"""
    args = ()
    if a.player:
        q += " AND id=?"
        args = (a.player,)
    rows = con.execute(q, args).fetchall()
    print(f"진화 단계 역추정 — 카탈로그 {len(catalog)}종 × 보유 {len(rows)}장")
    print("⛔ 여기서 원장에 쓰지 않는다 — 후보 제시일 뿐이다. 기록은 `fut_club.py evolve`로 한다.\n")
    n_hit = 0
    for cp in rows:
        has_log = con.execute("SELECT 1 FROM fut_evolution_log WHERE club_player_id=? AND is_void=0 LIMIT 1",
                              (cp["id"],)).fetchone()
        if has_log and not a.verify and not a.player:
            continue                                        # 이미 적힌 것은 --verify에서만 본다
        before = n_hit
        report(con, cp, catalog, a.verify)
        n_hit = before
    con.close()


if __name__ == "__main__":
    main()
