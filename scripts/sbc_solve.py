#!/usr/bin/env python3
"""보유 카드로 SBC를 달성할 수 있는지 판정하고, 되면 스쿼드를 짜 준다
   (2026-09-25 신설, 사용자 지시 「지금 가지고 있는 선수들로 SBC 달성할수 있는지 확인하고
    가능하다면 달성할수있는 스쿼드를 짜줘」).

⛔⛔ **못 읽은 조건은 「달성 가능」으로 세지 않는다.** fut.gg는 조건을 사람이 읽는 문장으로만 주므로
   (`fc_sbc_challenges.requirements_text`) 파싱이 전부다. 모르는 문장이 하나라도 있으면 그 챌린지는
   **판정 불가**로 분류하고 그 문장을 찍는다 — 조용히 무시하면 「된다」는 거짓 보고가 된다.

⚠️ 근거 등급(CLAUDE.md 불변규칙 12):
   · 조건 문장·보상·마감 = **A**(fut.gg가 EA 정의를 노출)
   · 카드 등급(Bronze/Silver/Gold) = **D** — EA가 표로 공개한 적 없고 OVR 구간(≤64/65–74/75+)은 통설이다.
     ⭐ 다만 특수 카드는 OVR과 무관하게 골드로 본다(`is_special`).
   · 팀 레이팅 산식 = **D** — EA 비공개. 커뮤니티 통용식(평균 + 초과분/인원)을 쓴다.
   · 케미스트리 = 화면(`site/evolutions.html`)과 **같은 FC27 기준선**을 쓴다(클럽 2/4/7 · 리그 3/5/8 · 국적 2/5/8).

사용:
    .venv/bin/python scripts/sbc_solve.py
    .venv/bin/python scripts/sbc_solve.py --set 19          # 한 세트만
    .venv/bin/python scripts/sbc_solve.py --tries 800       # 탐색 횟수
"""
import argparse
import json
import math
import random
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DB = ROOT / "db" / "tactics.db"

TIER = {"Bronze": 0, "Silver": 1, "Gold": 2}
# FC27 케미 기준선 — ⛔ 화면(evolutions.html CHEM_TIERS)과 같은 값이다. 갈리면 둘 다 고친다.
CHEM = {"club": [(7, 3), (4, 2), (2, 1)], "league": [(8, 3), (5, 2), (3, 1)],
        "nation": [(8, 3), (5, 2), (2, 1)]}
FORM = ["GK", "LB", "CB", "CB", "RB", "CDM", "CDM", "LM", "CAM", "RM", "ST"]   # 4-2-3-1


def tier_of(p):
    """카드 등급. ⚠️ 등급 D — EA 공개표가 없다. 특수 카드는 OVR과 무관하게 골드."""
    if p["is_special"]:
        return 2
    return 2 if p["ovr"] >= 75 else 1 if p["ovr"] >= 65 else 0


def team_rating(ovrs):
    """팀 레이팅. ⚠️ 등급 D — EA 산식 비공개. 커뮤니티 통용식(평균 + 평균 초과분의 평균)."""
    if not ovrs:
        return 0
    avg = sum(ovrs) / len(ovrs)
    return math.floor(avg + sum(max(0, o - avg) for o in ovrs) / len(ovrs))


def chem_total(xi):
    """팀 케미 합. ⛔ 포지션이 맞아야 카운트에 든다 — 그래서 배치 문제다(화면과 같은 규칙)."""
    cnt = {k: {} for k in CHEM}
    for p in xi:
        for k in CHEM:
            if p[k]:
                cnt[k][p[k]] = cnt[k].get(p[k], 0) + 1
    def tier(n, tb):
        for need, pt in tb:
            if n >= need:
                return pt
        return 0
    return sum(min(3, sum(tier(cnt[k][p[k]], CHEM[k]) if p[k] else 0 for k in CHEM)) for p in xi)


# ── 조건 파싱 ────────────────────────────────────────────────────────────────
# ⛔ 새 문장은 여기 추가한다. 못 읽으면 판정 불가로 떨어뜨린다(조용히 넘기지 않는다).
PATS = [
    (r"^Number of players: (\d+)$",                          lambda m: ("size", int(m[1]))),
    (r"^Player quality: Min\. (Bronze|Silver|Gold)$",         lambda m: ("qual_min", TIER[m[1]])),
    (r"^Exactly (Bronze|Silver|Gold) Players$",               lambda m: ("qual_exact", TIER[m[1]])),
    (r"^Player OVR: Max\. (\d+)$",                            lambda m: ("ovr_max", int(m[1]))),
    (r"^Player OVR: Min\. (\d+)$",                            lambda m: ("ovr_min", int(m[1]))),
    (r"^Player OVR: (\d+)[–-](\d+)$",                         lambda m: ("ovr_range", (int(m[1]), int(m[2])))),
    (r"^Min\. (\d+) Players: (Bronze|Silver|Gold)$",          lambda m: ("min_tier", (int(m[1]), TIER[m[2]]))),
    (r"^Min\. (\d+) player with minimum OVR of (\d+)$",       lambda m: ("min_n_ovr_ge", (int(m[1]), int(m[2])))),
    (r"^Min\. (\d+) player with maximum OVR of (\d+)$",       lambda m: ("min_n_ovr_le", (int(m[1]), int(m[2])))),
    (r"^Min\. (\d+) Players from: (.+)$",                     lambda m: ("min_from", (int(m[1]), [x.strip() for x in m[2].split(" OR ")]))),
    (r"^(Min|Max)\. (\d+) Players from the same (Club|League|Nation)$",
                                                              lambda m: ("same", (m[1], int(m[2]), m[3].lower()))),
    (r"^(Min|Max|Exact)\.? (Clubs|Leagues|Nationalities) in Squad: (\d+)$",
                                                              lambda m: ("distinct", (m[1], m[2], int(m[3])))),
    (r"^(Min|Max)\. Team Rating: (\d+)$",                     lambda m: ("rating", (m[1], int(m[2])))),
    (r"^Min\. Squad Total Chemistry Points: (\d+)$",          lambda m: ("chem", int(m[1]))),
    # ⭐ `League: X`는 **제출 카드 전원이 그 리그**라는 1인 조건이다(2026-09-25 확인 — fut.gg 설명
    #    「Submit Player Items from Premier League.」). 스쿼드 전체 조건이 아니다.
    (r"^League: (.+)$",                                       lambda m: ("league_is", m[1].strip())),
]
FIELD = {"Clubs": "club", "Leagues": "league", "Nationalities": "nation"}


def parse(reqs):
    out, bad = [], []
    for t in reqs:
        for pat, fn in PATS:
            m = re.match(pat, t.strip())
            if m:
                out.append((fn(m), t))
                break
        else:
            bad.append(t)
    return out, bad


def per_player_ok(p, conds):
    for (kind, v), _ in conds:
        if kind == "qual_min" and tier_of(p) < v: return False
        if kind == "qual_exact" and tier_of(p) != v: return False
        if kind == "ovr_max" and p["ovr"] > v: return False
        if kind == "ovr_min" and p["ovr"] < v: return False
        if kind == "ovr_range" and not (v[0] <= p["ovr"] <= v[1]): return False
        if kind == "league_is" and p["league"] != v: return False
    return True


def cost1(xi, kind, v):
    """조건 하나의 **위반 크기**. 0이면 충족. ⛔ 「맞았나/틀렸나」만 세면 국소 탐색에 기울기가 없다
       (2026-09-25 실측: 「Min. 11 Players: Silver」를 실버 24장을 갖고도 못 찾았다 — 거짓 불가였다)."""
    n = len(xi)
    if kind in ("qual_min", "qual_exact", "ovr_max", "ovr_min", "ovr_range", "league_is"):
        return sum(0 if per_player_ok(p, [((kind, v), "")]) else 1 for p in xi)
    if kind == "size":
        return abs(n - v)
    if kind == "min_tier":
        return max(0, v[0] - sum(1 for p in xi if tier_of(p) == v[1]))
    if kind == "min_n_ovr_ge":
        return max(0, v[0] - sum(1 for p in xi if p["ovr"] >= v[1]))
    if kind == "min_n_ovr_le":
        return max(0, v[0] - sum(1 for p in xi if p["ovr"] <= v[1]))
    if kind == "min_from":
        return max(0, v[0] - sum(1 for p in xi if p["nation"] in v[1] or p["league"] in v[1] or p["club"] in v[1]))
    if kind == "same":
        mode, k, f = v
        cnt = {}
        for p in xi:
            if p[f]:
                cnt[p[f]] = cnt.get(p[f], 0) + 1
        mx = max(cnt.values(), default=0)
        return max(0, k - mx) if mode == "Min" else max(0, mx - k)
    if kind == "distinct":
        mode, fld, k = v
        d = len({p[FIELD[fld]] for p in xi if p[FIELD[fld]]})
        return max(0, k - d) if mode == "Min" else max(0, d - k) if mode == "Max" else abs(d - k)
    if kind == "rating":
        r = team_rating([p["ovr"] for p in xi])
        return max(0, v[1] - r) if v[0] == "Min" else max(0, r - v[1])
    if kind == "chem":
        return max(0, v - chem_total(xi))
    return 0


def check(xi, conds):
    """못 맞춘 조건 문장 + 총 위반 크기."""
    fail, cost = [], 0
    for (kind, v), text in conds:
        c = cost1(xi, kind, v)
        cost += c
        if c:
            fail.append(text)
    return fail, cost


def solve(pool, conds, size, tries, rng):
    """무작위 재시작 + **위반 크기를 줄이는** 국소 교체.
       ⛔ 못 찾았다고 「불가능」이 아니다 — 최적 보장이 없는 탐색이라 보고에 그렇게 적는다."""
    cands = [p for p in pool if per_player_ok(p, conds)]
    if len(cands) < size:
        return None, cands, None
    best = None
    for t in range(tries):
        xi = rng.sample(cands, size)
        fail, cost = check(xi, conds)
        if not cost:
            return xi, cands, None
        for _ in range(400):
            i = rng.randrange(size)
            alt = rng.choice(cands)
            if any(alt["id"] == q["id"] for q in xi):
                continue
            trial = xi[:i] + [alt] + xi[i + 1:]
            f2, c2 = check(trial, conds)
            if c2 <= cost:                       # 같아도 받는다 — 평지를 건너야 빠져나온다
                xi, fail, cost = trial, f2, c2
            if not cost:
                return xi, cands, None
        if best is None or cost < best[1]:
            best = (fail, cost)
    return None, cands, best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="FC27")
    ap.add_argument("--set", type=int, help="세트 ea_id 하나만")
    ap.add_argument("--tries", type=int, default=400)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--save", action="store_true", help="판정 결과를 fc_sbc_solutions에 적는다(화면이 읽는다)")
    a = ap.parse_args()
    rng = random.Random(a.seed)

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    pool = [dict(r) for r in con.execute("""
        SELECT c.id, COALESCE(i.name_kr, c.name) name, COALESCE(c.current_ovr, i.ovr) ovr,
               i.nation, i.league, i.club, i.positions, COALESCE(i.is_special,0) is_special,
               c.is_untradeable
          FROM fut_club_players c LEFT JOIN player_card_items i
            ON i.ea_item_id=c.ea_item_id AND i.game_version=?
         WHERE c.status='owned' AND COALESCE(c.current_ovr, i.ovr) IS NOT NULL""", (a.game,))]
    miss = [p["name"] for p in pool if not p["club"] or not p["league"] or not p["nation"]]
    print(f"보유 카드 {len(pool)}장" + (f" · ⚠️ 클럽/리그/국적 결손 {len(miss)}장은 그룹 조건에서 빠진다: "
                                        f"{', '.join(miss[:5])}{' …' if len(miss) > 5 else ''}" if miss else ""))

    q = """SELECT s.name set_name, s.set_ea_id, s.category, s.end_time, s.is_repeatable,
                  ch.challenge_ea_id, ch.name, ch.requirements_text, ch.awards_text, ch.challenge_type
             FROM fc_sbc_challenges ch JOIN fc_sbc_sets s
               ON s.set_ea_id=ch.set_ea_id AND s.pulled=ch.pulled AND s.game_version=ch.game_version
            WHERE ch.game_version=? AND ch.pulled=(SELECT MAX(pulled) FROM fc_sbc_challenges)
              AND s.is_expired=0"""
    args = [a.game]
    if a.set:
        q += " AND s.set_ea_id=?"; args.append(a.set)
    rows = [dict(r) for r in con.execute(q + " ORDER BY s.category, s.name, ch.name", args)]

    ok, no, undec, oneclick = [], [], [], []
    for r in rows:
        conds, bad = parse(json.loads(r["requirements_text"] or "[]"))
        if bad:
            undec.append((r, bad)); continue
        size = next((v for (k, v), _ in conds if k == "size"), None)
        if size is None:
            # ⛔ 원클릭 챌린지는 **제출 인원을 fut.gg가 주지 않는다** — 11명으로 가정하면 거짓 보고가 된다.
            #    조건은 1인 필터뿐이므로 「몇 장이 조건을 통과하나」만 센다.
            if r["challenge_type"] == "ONE_CLICK_CHALLENGE":
                oneclick.append((r, conds, [p for p in pool if per_player_ok(p, conds)]))
                continue
            size = 11
        xi, cands, best = solve(pool, conds, size, a.tries, rng)
        (ok if xi else no).append((r, xi, size, cands, conds, best))

    def head(r):
        return f"{r['set_name']} › {r['name']}"
    print(f"\n{'='*70}\n■ 달성 가능 {len(ok)} · 불가/못 찾음 {len(no)} · 원클릭 {len(oneclick)} · 판정 불가 {len(undec)}\n{'='*70}")
    if oneclick:
        print("\n── 원클릭 제출(인원 수를 fut.gg가 주지 않는다 — 조건 통과 카드 수만 센다) ──")
        for r, conds, cs in oneclick:
            print(f"  {'✅' if cs else '❌'} {head(r)} — 조건 통과 {len(cs)}장 · {' / '.join(t for _c, t in conds)}")
    for r, xi, size, _c, _cd, _b in ok:
        aw = ", ".join(x["name"] for x in json.loads(r["awards_text"] or "[]")) or "—"
        print(f"\n✅ {head(r)}  [{size}명 · 보상 {aw} · 마감 {(r['end_time'] or '')[:10]}]")
        for p in sorted(xi, key=lambda x: -x["ovr"]):
            print(f"     {p['ovr']:>3} {p['name']:<22} {str(p['club'] or '—')[:18]:<18} "
                  f"{str(p['league'] or '—')[:22]:<22} {p['nation'] or '—'}"
                  + ("  [거래불가]" if p["is_untradeable"] else ""))
        print(f"     └ 팀 레이팅 {team_rating([p['ovr'] for p in xi])} · 케미(참고) {chem_total(xi)}")
    for r, _x, size, cands, conds, best in no:
        print(f"\n❌ {head(r)}  [{size}명 필요 · 조건 통과 카드 {len(cands)}장]")
        if len(cands) < size:
            print(f"     └ ⛔ **불가 확정** — 1인 조건(등급·OVR)을 통과하는 카드가 {len(cands)}장뿐이다.")
        elif best:
            print(f"     └ ⚠️ **못 찾음**(불가 증명 아님) — 가장 가까운 해에서 남은 위반 {best[1]}:")
            for t in best[0]:
                print(f"         · {t}")
    for r, bad in undec:
        print(f"\n⚠️ {head(r)} — 못 읽은 조건 {len(bad)}개(판정 안 함): {' / '.join(bad)}")

    if not a.save:
        print("\n(--save 를 주면 화면이 읽도록 fc_sbc_solutions에 적는다)")
        return
    import datetime as _dt
    today = _dt.date.today().isoformat()
    acc = con.execute("SELECT id FROM fut_accounts ORDER BY id LIMIT 1").fetchone()
    aid = acc["id"] if acc else None
    src = f"scripts/sbc_solve.py (보유 {len(pool)}장 기준, {today} 판정 · seed {a.seed} · tries {a.tries})"
    conf = ("판정 근거 등급: 조건·보상=A(fut.gg) · 카드 등급(Bronze/Silver/Gold)=D(OVR 구간 통설) · "
            "팀 레이팅 산식=D(EA 비공개·커뮤니티식) · 케미=화면과 같은 FC27 기준선. "
            "⛔ not_found는 불가 증명이 아니다 — 탐색이 최적을 보장하지 않는다.")
    rows = []
    slim = lambda p: {"id": p["id"], "name": p["name"], "ovr": p["ovr"], "club": p["club"],
                      "league": p["league"], "nation": p["nation"], "untradeable": p["is_untradeable"]}
    for r, xi, size, cands, _cd, _b in ok:
        rows.append((a.game, r["challenge_ea_id"], today, aid, "ok",
                     json.dumps([slim(p) for p in xi], ensure_ascii=False),
                     team_rating([p["ovr"] for p in xi]), chem_total(xi), len(cands), None, src, conf))
    for r, _x, size, cands, conds, best in no:
        imp = len(cands) < size
        rows.append((a.game, r["challenge_ea_id"], today, aid, "impossible" if imp else "not_found",
                     None, None, None, len(cands),
                     (f"1인 조건 통과 카드 {len(cands)}장 < 필요 {size}명" if imp
                      else "남은 위반: " + " / ".join(best[0]) if best else "해를 못 찾았다"), src, conf))
    for r, conds, cs in oneclick:
        rows.append((a.game, r["challenge_ea_id"], today, aid, "oneclick", None, None, None, len(cs),
                     "원클릭 제출 — fut.gg가 제출 인원을 주지 않아 인원 판정을 하지 않는다", src, conf))
    for r, bad in undec:
        rows.append((a.game, r["challenge_ea_id"], today, aid, "unparsed", None, None, None, None,
                     "못 읽은 조건: " + " / ".join(bad), src, conf))
    con.executemany("""INSERT INTO fc_sbc_solutions(game_version,challenge_ea_id,pulled,account_id,verdict,
                         squad_json,team_rating,chem_total,pool_size,note,source,confidence)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
                       ON CONFLICT(game_version,challenge_ea_id,pulled) DO UPDATE SET
                         verdict=excluded.verdict, squad_json=excluded.squad_json,
                         team_rating=excluded.team_rating, chem_total=excluded.chem_total,
                         pool_size=excluded.pool_size, note=excluded.note, source=excluded.source""", rows)
    con.commit()
    print(f"\n적재 {len(rows)}행 → fc_sbc_solutions ({today})")
    print("다음: python3 scripts/export.py")


if __name__ == "__main__":
    main()
