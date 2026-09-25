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
# ⛔⛔ **포메이션은 DB가 정본이다**(migration 070 · fut.gg 번들에서 받은 FC27 29종).
#    종전엔 4종을 여기 박아 썼다 — SBC는 챌린지마다 포메이션이 고정이라 목록이 모자라면 기록조차 못 한다.
#    ⭐ 칸 자격은 `gen`(번들의 generalPositionSlots · 등급 A)으로 본다 — 그 칸에 설 수 있는 카드 포지션이다.
FORMS = {}          # name → [{i,uniq,gen,label,x,y}] · main()이 DB에서 채운다
GEN_POS = {0: "GK", 2: "RWB", 3: "RB", 5: "CB", 7: "LB", 8: "LWB", 10: "CDM", 12: "RM",
           14: "CM", 16: "LM", 18: "CAM", 21: "CF", 23: "RW", 25: "ST", 27: "LW"}
# 카드 포지션 → 그 칸에 설 수 있는가. ⚠️ 좌우 변형(LWB↔LB 등)은 EA가 같은 칸으로 취급한다(등급 D).
NEAR = {"RWB": {"RWB", "RB"}, "LWB": {"LWB", "LB"}, "RB": {"RB", "RWB"}, "LB": {"LB", "LWB"},
        "RW": {"RW", "RM"}, "LW": {"LW", "LM"}, "RM": {"RM", "RW"}, "LM": {"LM", "LW"},
        "CF": {"CF", "ST"}, "ST": {"ST", "CF"}}


# ⛔ 배치 국소탐색의 무작위 — **고정 시드**다. 같은 입력에 같은 배치가 나와야 판정이 재현된다.
PLACE_RNG = random.Random(11)


def slot_accepts(gen_id):
    base = GEN_POS.get(gen_id)
    return NEAR.get(base, {base}) if base else set()


def positions_of(p):
    return {x.strip() for x in str(p.get("positions") or p.get("best_pos") or "").split("/") if x.strip()}


def place(xi, form):
    """11명을 포메이션 슬롯에 배치.

    ⛔⛔ **종전엔 탐욕법이었다**(맞는 칸부터 채우고 남으면 아무 데나) — 2026-09-25 사용자 지시
       「최적 배치로 고치자」에 따라 바꿨다. 탐욕은 먼저 집은 사람이 다른 칸의 유일한 후보를 뺏어
       **자리 안 맞음이 실제보다 많이 나왔고**, 케미가 낮게 잡혀 챌린지가 「못 찾음」으로 떨어졌다.

    지금 하는 것 — 두 단계:
      ⑴ **최대 이분 매칭**(증가 경로)으로 «자리 맞는 사람 수»를 최대화한다. 여기는 최적이 보장된다.
      ⑵ 그 인원을 유지하면서 **쌍 교환으로 케미를 올린다**.
    ⚠️ ⑵가 필요한 이유: 케미는 «자리 맞는 사람들» 사이의 클럽·리그·국적 **개수**로 정해져서
       매칭 하나가 정해도 조합에 따라 달라진다. 자리 맞는 인원이 같아도 누가 어디 서느냐로 갈린다.

    ⛔⛔ **목적함수는 케미다 — 자리 맞는 인원이 아니다**(2026-09-25 실측으로 정정).
       처음엔 «인원 우선, 케미는 동점 처리»로 짰다가 Silver Upgrade의 케미가 **9 → 2로 떨어졌다**.
       「자리 맞는 사람을 늘리면 손해 볼 게 없다」고 본 게 틀렸다 — 최대 매칭끼리는 **포함 관계가 아니라서**
       인원이 같거나 늘어도 **맞는 사람이 통째로 바뀐다**. 같은 클럽 4명이 맞던 자리가
       제각각인 5명으로 갈리면 케미는 내려간다. ⇒ 케미를 먼저 보고 인원은 동점일 때만 본다.
    ⚠️ 국소 탐색이라 전역 최적은 보장하지 않는다 — 그래서 **여러 출발점**에서 돌려 가장 좋은 것을 쓴다."""
    slots = FORMS[form]
    n, m = len(slots), len(xi)
    fitok = [[bool(positions_of(p) & slot_accepts(s["gen"])) for p in xi] for s in slots]

    # ⑴ 최대 이분 매칭 — 칸 ← 선수. 쾨니그식 증가 경로(11×11이라 단순 구현으로 충분하다).
    at = [-1] * n          # 칸 i에 선 선수 인덱스
    def aug(i, seen):
        for j in range(m):
            if fitok[i][j] and j not in seen:
                seen.add(j)
                if all(at[k] != j for k in range(n)) or aug(next(k for k in range(n) if at[k] == j), seen):
                    at[i] = j
                    return True
        return False
    for i in range(n):
        aug(i, set())

    # 남은 칸은 남은 선수로 채운다(자리 안 맞음 = 케미 0).
    used = {j for j in at if j >= 0}
    rest = [j for j in range(m) if j not in used]
    for i in range(n):
        if at[i] < 0 and rest:
            at[i] = rest.pop(0)


    # ⑵ 쌍 교환으로 **케미**를 올린다(동점이면 자리 맞는 인원이 많은 쪽).
    def score(assign):
        f = [xi[assign[i]] for i in range(n) if assign[i] >= 0 and fitok[i][assign[i]]]
        return (chem_total(f), len(f))

    def climb(assign):
        cur = score(assign)
        improved = True
        while improved:
            improved = False
            for i in range(n):
                for k in range(i + 1, n):
                    if assign[i] < 0 or assign[k] < 0:
                        continue
                    assign[i], assign[k] = assign[k], assign[i]
                    s = score(assign)
                    if s > cur:
                        cur, improved = s, True
                    else:
                        assign[i], assign[k] = assign[k], assign[i]
        return cur, assign

    # ⚠️ 출발점을 여럿 둔다 — 최대 매칭 하나에서만 오르면 그 봉우리에 갇힌다(위 주석의 실측이 그 경우다).
    #    ⛔ 무작위는 `PLACE_RNG` 고정 시드다 — 같은 입력에 같은 배치가 나와야 결과가 재현된다.
    best = climb(list(at))
    for _ in range(12):
        cand = list(at)
        PLACE_RNG.shuffle(cand)
        s, aa = climb(cand)
        if s > best[0]:
            best = (s, aa)
    at = best[1]
    return [(slots[i]["label"], slots[i]["x"], slots[i]["y"],
             xi[at[i]] if at[i] >= 0 else None,
             at[i] >= 0 and fitok[i][at[i]],
             # ⭐ 이 칸에 설 수 있는 포지션 — 자리가 안 맞을 때 **무엇을 사야 하는지**의 답이다.
             sorted(slot_accepts(slots[i]["gen"]))) for i in range(n)]


def best_placement(xi, form=None):
    """배치. ⛔⛔ **포메이션이 기록돼 있으면 그것만 쓴다**(2026-09-25).
       인게임 SBC는 챌린지마다 포메이션이 고정인데 EA·fut.gg가 그 값을 주지 않는다
       (`fc_sbc_formations` = 사용자 기록). 종전엔 **케미가 가장 높은 것을 임의로 골라** 보여줘서
       인게임 화면과 달랐다 — 그게 이 함수가 인자를 받게 된 이유다.
       ⚠️ 기록이 없으면 후보를 다 시도하되, 돌려주는 포메이션은 **추정**이다(화면이 그렇게 적는다)."""
    if form and form in FORMS:
        pl = place(xi, form)
        return chem_total([p for _n, _x, _y, p, fit, _w in pl if p and fit]), form, pl
    # ⚠️ 추정일 때 29종을 다 돌면 탐색이 무거워진다 — **흔한 포메이션 6종**만 본다(어차피 추정이다).
    GUESS = [f for f in ("4-2-3-1", "4-4-2", "4-3-3", "3-5-2", "4-1-4-1", "5-2-1-2") if f in FORMS] or list(FORMS)
    best = None
    for f in GUESS:
        pl = place(xi, f)
        ch = chem_total([p for _n, _x, _y, p, fit, _w in pl if p and fit])
        if best is None or ch > best[0]:
            best = (ch, f, pl)
    return best


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


GK_RULE = "스쿼드에 골키퍼 정확히 1명(EA 규칙 · 조건 문장에 없지만 없으면 제출 자체가 안 된다)"


def gk_cost(xi):
    """⛔⛔ **EA는 GK 슬롯을 골키퍼로만 채울 수 있다.** 조건 문장에는 안 나오지만 없으면 제출이 불가하다.
       (2026-09-25 실측: 배치를 붙이고 나서야 「Norway v Portugal」 해에 GK가 없다는 게 드러났다 —
        그 전까지는 11명만 맞으면 된다고 보고 있었다.)"""
    n = sum(1 for p in xi if "GK" in positions_of(p))
    return abs(n - 1)


def check(xi, conds):
    """못 맞춘 조건 문장 + 총 위반 크기."""
    fail, cost = [], 0
    g = gk_cost(xi)
    if g:
        fail.append(GK_RULE)
        cost += g
    for (kind, v), text in conds:
        c = cost1(xi, kind, v)
        cost += c
        if c:
            fail.append(text)
    return fail, cost


def breakdown(xi, conds, chem=None):
    """조건 **전부**를 충족/미충족으로 갈라 돌려준다(2026-09-25 사용자 지시
       「만족한 조건과 불만족한 조건을 알려주고 어떤 조건을 사야 하는지 표시해줘」).

    ⛔ `check()`는 **못 맞춘 것만** 준다 — 그러면 「어디까지는 됐나」를 화면이 말할 수 없다.
    ⭐ `gap`은 `cost1`의 위반 크기 그대로다. 인원 축 조건에서는 그 값이 곧
       **「몇 명을 더 사야 하는가」**라서 구매 표시의 근거가 된다(등급 C — 우리 계산).
    ⚠️ 그룹 축(같은 클럽 Min 3 등)의 gap도 인원이지만 **아무 카드나로는 안 풀린다** —
       그건 `group_hints()`가 문장으로 짚는다."""
    out = [{"text": GK_RULE, "ok": not gk_cost(xi), "gap": gk_cost(xi), "kind": "gk"}]
    for (kind, v), text in conds:
        # ⛔⛔ 케미는 **배치 반영값으로 판정한다**(2026-09-25). 탐색용 `chem_total`은 포지션을 무시한
        #    **상한**이라, 그대로 쓰면 머리말엔 「케미 7」이 찍히는데 체크리스트는 「✅ Min. 18」이 된다
        #    (실측: Norway v Portugal). 화면 두 곳이 서로 다른 말을 하는 것 자체가 버그다.
        c = max(0, v - chem) if (kind == "chem" and chem is not None) else cost1(xi, kind, v)
        out.append({"text": text, "ok": not c, "gap": c, "kind": kind})
    return out


FORM_OF = {}          # challenge_ea_id → 기록된 포메이션. main()이 채운다
CUR_FORM = [None]     # 지금 푸는 챌린지의 포메이션(없으면 None)


def chem_ok(xi, conds):
    """⛔⛔ 탐색용 `chem_total`은 **포지션을 무시**해서 실제보다 높게 나온다(상한).
       ⇒ 해를 찾으면 **배치까지 해서** 케미 조건을 다시 본다. 통과해야 진짜 해다.
       (2026-09-25: 종전엔 이 검증이 없어 「케미 26」 같은 값이 배치하면 안 나올 수 있었다.)"""
    need = [v for (k, v), _ in conds if k == "chem"]
    if not need:
        return True, None
    ch, form, pl = best_placement(xi, CUR_FORM[0])
    return ch >= max(need), (ch, form, pl)


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
            ok_ch, info = chem_ok(xi, conds)
            if ok_ch:
                return xi, cands, None
            # ⛔ 조건표는 통과했는데 **배치하면 케미가 모자란** 경우 — 그 사실을 보고에 남긴다
            #    (2026-09-25: 안 남겨서 「남은 위반 0인데 실패」라는 읽을 수 없는 보고가 나왔다).
            need = max(v for (k, v), _ in conds if k == "chem")
            fail, cost = [f"배치 후 케미 {info[0]} < 필요 {need} ({info[1]} 기준 · 포지션이 맞아야 케미가 붙는다)"], 1
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
                ok_ch, info = chem_ok(xi, conds)
                if ok_ch:
                    return xi, cands, None
                need = max(v for (k, v), _ in conds if k == "chem")
                fail, cost = [f"배치 후 케미 {info[0]} < 필요 {need} ({info[1]} 기준)"], 1
        # ⭐ **가장 가까운 해의 11명을 함께 들고 나간다**(2026-09-25 사용자 지시
        #    「못 풀더라도 현재 스쿼드 기준으로 채울 수 있는 선수들을 채우고」).
        #    종전엔 위반 목록만 남기고 그 11명을 버려서 「무엇까지는 됐나」를 볼 수 없었다.
        if best is None or cost < best[1]:
            best = (fail, cost, list(xi))
    return None, cands, best


# ── 구매 후보 (2026-09-25 사용자 지시 「구매해야 하는 포지션은 가격이 저렴한 선수로 제안」) ──
#   ⛔ 시장 전체를 우리가 들고 있지 않다 — `player_card_prices`는 관리 4팀 카드뿐이다.
#      ⇒ fut.gg 목록 API로 **그 챌린지 조건에 맞는 카드**를 받아 `currentDbPrice`로 싼 순으로 고른다.
#   ⚠️ 가격은 fut.gg 집계 시세다(등급 MEDIUM) — 실제 이적시장 호가와 다를 수 있다.
#   ⚠️ 시세 미형성(hasPrice=0)은 **0원이 아니라 모름**이다 — 제안에서 뺀다.
FUTGG = "https://www.fut.gg/api/fut"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", "Accept": "application/json"}


def _get(url):
    import urllib.request
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.load(r)


# ⛔ 그룹 조건(클럽·리그·국적 편중)은 **아무 싼 카드나 사서 풀리지 않는다** — 어느 축을 채워야 하는지가 답이다.
#    카드 목록을 던지면 「이걸 사면 된다」로 오독되므로, 그런 조건은 **문장으로** 짚는다.
GROUP_HINT = {
    ("same", "Min"):  "같은 {f} 선수를 더 확보해야 한다 — 아무 싼 카드나로는 안 풀린다",
    ("same", "Max"):  "한 {f}에 쏠린 인원을 줄여야 한다 — 다른 {f} 카드가 필요하다",
    ("distinct", "Min"): "{f} 종류를 더 늘려야 한다",
    ("distinct", "Max"): "{f} 종류를 줄여야 한다 — 이미 쓰는 {f}에서 더 사 모아야 한다",
    ("distinct", "Exact"): "{f} 종류를 정확히 맞춰야 한다",
}
FIELD_KR = {"club": "클럽", "league": "리그", "nation": "국적",
            "Clubs": "클럽", "Leagues": "리그", "Nationalities": "국적"}


def group_hints(fails, conds):
    """못 맞춘 조건 중 **그룹 축**을 골라 사람이 읽을 조언으로 바꾼다."""
    out = []
    for (kind, v), text in conds:
        if text not in fails:
            continue
        if kind == "same":
            mode, _k, f = v
            out.append((text, GROUP_HINT[("same", mode)].format(f=FIELD_KR.get(f, f))))
        elif kind == "distinct":
            mode, fld, _k = v
            out.append((text, GROUP_HINT[("distinct", mode)].format(f=FIELD_KR.get(fld, fld))))
        elif kind == "chem":
            out.append((text, "케미가 모자란다 — 같은 클럽·리그·국적을 묶어야 오른다"))
        elif kind == "rating":
            out.append((text, "팀 레이팅이 모자란다 — OVR 높은 카드가 필요하다"))
    return out


def buy_candidates(conds, want, limit=6):
    """조건을 만족하는 **싼 카드**를 fut.gg에서 찾는다. want = 몇 명이 필요한가."""
    q = []
    for (kind, v), _ in conds:
        if kind == "ovr_max": q.append(f"overall__lte={v}")
        elif kind == "ovr_min": q.append(f"overall__gte={v}")
        elif kind == "ovr_range": q.append(f"overall__gte={v[0]}&overall__lte={v[1]}")
        elif kind == "qual_exact" and v == 0: q.append("overall__lte=64")
        elif kind == "qual_exact" and v == 1: q.append("overall__gte=65&overall__lte=74")
        elif kind == "qual_min" and v == 2: q.append("overall__gte=75")
    # ⭐ `sorts=overall`이 **오름차순**이다(2026-09-25 실측: 75,75,75… / `-overall`이면 95,95,94…).
    #    ⛔ 빼면 fut.gg 기본 정렬(인기순으로 보임)이 와서 88~90 아이콘이 「싼 후보」로 찍힌다.
    q.append("sorts=overall")
    try:
        d = _get(f"{FUTGG}/players/v2/27/?" + "&".join(q or ["overall__lte=64"]))
    except Exception as e:
        return [], f"시세 조회 실패({type(e).__name__})"
    ids = [x["eaId"] for x in (d.get("data") or [])][:40]
    if not ids:
        return [], "조건에 맞는 카드를 못 찾았다"
    try:
        pr = _get(f"{FUTGG}/players/v2/27/?ea_ids=" + ",".join(map(str, ids)))
    except Exception as e:
        return [], f"시세 조회 실패({type(e).__name__})"
    out, priced = [], 0
    for x in (pr.get("data") or []):
        has = bool(x.get("hasPrice"))
        priced += has
        out.append({"name": x.get("commonName") or x.get("lastName"), "ovr": x.get("overall"),
                    "price": x.get("currentDbPrice") if has else None,
                    "nation": (x.get("nation") or {}).get("name"),
                    "league": (x.get("league") or {}).get("name"),
                    "club": (x.get("club") or {}).get("name")})
    # ⛔⛔ **FC27 시세가 아직 없다**(2026-09-25 실측: 조회한 카드 전부 hasPrice=false · 우리 `player_card_prices`
    #    247행도 전량 has_price=0). 시세가 없으면 「싼 순」이 성립하지 않는다.
    #    ⇒ 0원으로 세워 거짓 순위를 만들지 않고, **OVR 낮은 순**으로 물러서되 그 사실을 함께 돌려준다.
    #      (필러 카드는 OVR이 낮을수록 싼 경향이라는 **판단값**이지 실측이 아니다 — 등급 D.)
    if priced:
        out.sort(key=lambda r: r["price"] if r["price"] is not None else 10 ** 9)
        return out[:max(limit, want)], None
    out.sort(key=lambda r: r["ovr"] or 99)
    return out[:max(limit, want)], ("⚠️ fut.gg가 FC27 시세를 아직 주지 않는다(조회분 전부 hasPrice=false) — "
                                    "가격순이 아니라 **OVR 낮은 순**이다(싼 경향이라는 판단값 · 등급 D)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="FC27")
    ap.add_argument("--set", type=int, help="세트 ea_id 하나만")
    # ⛔⛔ **탐색 횟수는 한 곳에만 둔다**(2026-09-25). 종전엔 여기 400 · `fut_club.py`가 500이라
    #    **부르는 경로에 따라 같은 챌린지가 「달성 가능」과 「못 찾음」으로 갈렸다**(실측: Norway v
    #    Portugal이 400에선 못 찾고 500에선 풀렸다). 값을 옮겨 적지 말고 이 기본값을 쓴다.
    ap.add_argument("--tries", type=int, default=1200)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--save", action="store_true", help="판정 결과를 fc_sbc_solutions에 적는다(화면이 읽는다)")
    ap.add_argument("--include-squad", action="store_true",
                    help="활성 스쿼드(선발+교체) 선수도 후보에 넣는다. 기본은 **제외**한다 — 쓰고 있는 카드다")
    ap.add_argument("--buy", action="store_true", help="보유분으로 안 되는 챌린지에 **싼 구매 후보**를 붙인다(fut.gg 조회)")
    ap.add_argument("--protect-club", nargs="*", default=["Aston Villa"],
                    help="SBC에 내지 않을 클럽(기본 아스톤 빌라 — 내 팀 축이라 소모하면 안 된다). "
                         "--protect-club 만 쓰면 보호 없음")
    a = ap.parse_args()
    rng = random.Random(a.seed)

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    pool = [dict(r) for r in con.execute("""
        SELECT c.id, COALESCE(i.name_kr, c.name) name, COALESCE(c.current_ovr, i.ovr) ovr,
               i.nation, i.league, i.club, i.positions, i.best_pos, i.card_image_url,
               COALESCE(i.is_special,0) is_special,
               c.is_untradeable, c.ea_item_id
          FROM fut_club_players c LEFT JOIN player_card_items i
            ON i.ea_item_id=c.ea_item_id AND i.game_version=?
         WHERE c.status='owned' AND COALESCE(c.current_ovr, i.ovr) IS NOT NULL""", (a.game,))]
    # ⭐⭐ **활성 스쿼드는 기본 제외**(2026-09-25 사용자 지시 「내 활성 스쿼드의 선수들은 SBC 구성할 때 제외」).
    #    지금 쓰고 있는 11+12명을 SBC에 넣어 버리면 팀이 무너진다 — 넣고 싶으면 --include-squad.
    squad_ids = {r[0] for r in con.execute(
        "SELECT ea_item_id FROM fut_squad_slots WHERE ea_item_id IS NOT NULL")}
    in_squad = [p for p in pool if p["ea_item_id"] in squad_ids]
    if not a.include_squad:
        pool = [p for p in pool if p["ea_item_id"] not in squad_ids]
        print(f"⛔ 활성 스쿼드 {len(in_squad)}명 제외 — 남은 후보 {len(pool)}장 (넣으려면 --include-squad)")
    # ⭐⭐ **보호 클럽**(2026-09-25 사용자 지시 「아스톤 빌라 선수는 제외하고 재구성」).
    #    ⛔ 빌라는 이 저장소의 주 팀 축이다 — SBC에 내면 감독 재현·처방 대조에 쓰던 카드가 사라진다.
    #       활성 스쿼드 밖이라도 빼는 이유가 그것이다(실측: 빌라 25장 중 활성 밖이 5장).
    if a.protect_club:
        prot = [p for p in pool if p["club"] in a.protect_club]
        pool = [p for p in pool if p["club"] not in a.protect_club]
        print(f"⛔ 보호 클럽 {'·'.join(a.protect_club)} {len(prot)}명 제외 — 남은 후보 {len(pool)}장")
    miss = [p["name"] for p in pool if not p["club"] or not p["league"] or not p["nation"]]
    print(f"후보 카드 {len(pool)}장" + (f" · ⚠️ 클럽/리그/국적 결손 {len(miss)}장은 그룹 조건에서 빠진다: "
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

    # ⭐ 이미 완료한 챌린지는 풀지 않는다(2026-09-25) — 스쿼드를 제안할 이유가 없고 탐색만 낭비다.
    #   ⛔ 「완료」는 EA·fut.gg가 주지 않는 축이라 `fut_sbc_log`(사용자 기록)가 유일한 출처다(migration 068).
    FORMS.update({r[0]: json.loads(r[1]) for r in con.execute(
        "SELECT name, slots FROM fc_formations WHERE game_version=?", (a.game,))})
    if not FORMS:
        raise SystemExit("⛔ 포메이션이 없다 — .venv/bin/python scripts/collect_futgg_formations.py 먼저 돌릴 것")
    print(f"📐 포메이션 {len(FORMS)}종 적재")
    FORM_OF.update({r[0]: r[1] for r in con.execute(
        "SELECT challenge_ea_id, formation FROM fc_sbc_formations WHERE game_version=?", (a.game,))})
    if FORM_OF:
        print(f"📐 포메이션 기록 {len(FORM_OF)}챌린지 — 그 안에서만 배치한다")
    done_ids = {r[0] for r in con.execute(
        "SELECT challenge_ea_id FROM fut_sbc_log WHERE game_version=?", (a.game,))}
    if done_ids:
        rows = [r for r in rows if r["challenge_ea_id"] not in done_ids]
        print(f"🏁 이미 완료한 {len(done_ids)}챌린지는 판정에서 제외 — 남은 {len(rows)}개를 푼다")
    # ⭐ **챌린지별 제외**(migration 071 · 2026-09-25 사용자 지시 「선수를 스쿼드에서 제외하고 재계산」).
    #    ⛔ 전역 제외(활성 스쿼드·보호 클럽)와 축이 다르다 — 「이번 건에는 안 쓴다」는 챌린지마다 다른 판단이다.
    EXCL = {}
    for cid, pid in con.execute(
            "SELECT challenge_ea_id, club_player_id FROM fc_sbc_exclusions WHERE game_version=?", (a.game,)):
        EXCL.setdefault(cid, set()).add(pid)
    if EXCL:
        print(f"🚫 챌린지별 제외 {sum(len(v) for v in EXCL.values())}건 / {len(EXCL)}챌린지")
    ok, no, undec, oneclick = [], [], [], []
    for r in rows:
        conds, bad = parse(json.loads(r["requirements_text"] or "[]"))
        if bad:
            undec.append((r, bad)); continue
        ex = EXCL.get(r["challenge_ea_id"]) or set()
        pool_c = [p for p in pool if p["id"] not in ex] if ex else pool
        CUR_FORM[0] = FORM_OF.get(r["challenge_ea_id"])
        size = next((v for (k, v), _ in conds if k == "size"), None)
        if size is None:
            # ⛔ 원클릭 챌린지는 **제출 인원을 fut.gg가 주지 않는다** — 11명으로 가정하면 거짓 보고가 된다.
            #    조건은 1인 필터뿐이므로 「몇 장이 조건을 통과하나」만 센다.
            if r["challenge_type"] == "ONE_CLICK_CHALLENGE":
                oneclick.append((r, conds, [p for p in pool_c if per_player_ok(p, conds)]))
                continue
            size = 11
        xi, cands, best = solve(pool_c, conds, size, a.tries, rng)
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
        known = FORM_OF.get(r["challenge_ea_id"])
        ch, form, pl = best_placement(xi, known)
        print(f"\n✅ {head(r)}  [{size}명 · {form}{'' if known else '(추정 — 미기록)'} · 보상 {aw} · 마감 {(r['end_time'] or '')[:10]}]")
        for nm, _x, _y, p, fit, _w in pl:
            if not p:
                continue
            print(f"     {nm:<4} {p['ovr']:>3} {p['name']:<22} {str(p['club'] or '—')[:18]:<18} "
                  f"{str(p['nation'] or '—')[:14]:<14}{'' if fit else '  ⚠️ 자리 안 맞음(케미 0)'}"
                  + ("  [거래불가]" if p["is_untradeable"] else ""))
        print(f"     └ 팀 레이팅 {team_rating([p['ovr'] for p in xi])} · 케미 {ch} (배치 반영)")
    for r, _x, size, cands, conds, best in no:
        print(f"\n❌ {head(r)}  [{size}명 필요 · 조건 통과 카드 {len(cands)}장]")
        if a.buy:
            hints = group_hints(set(best[0]) if best else set(), conds)
            for t, h in hints:
                print(f"     └ 🎯 「{t}」 → {h}")
            need = max(0, size - len(cands))
            cb, err = ([], None) if hints else buy_candidates(conds, need or 3)
            if err and not cb:
                print(f"     └ 구매 후보: {err}")
            elif cb:
                if err:
                    print(f"     └ {err}")
                print(f"     └ 💰 구매 후보:")
                for x in cb:
                    pz = f"{x['price']:>8,}코인" if x['price'] is not None else "  시세없음"
                    print(f"         {pz}  {x['ovr']:>3} {str(x['name'])[:20]:<20} "
                          f"{str(x['league'] or '')[:20]:<20} {x['nation'] or ''}")
        if len(cands) < size:
            print(f"     └ ⛔ **불가 확정** — 1인 조건(등급·OVR)을 통과하는 카드가 {len(cands)}장뿐이다.")
        elif best:
            print(f"     └ ⚠️ **못 찾음**(불가 증명 아님) — 가장 가까운 해에서 남은 위반 {best[1]}:")
        # ⭐ **충족/미충족을 둘 다 찍는다**(2026-09-25 사용자 지시) — 못 찾았다는 말만으론
        #    「어디까지는 됐나」를 알 수 없다. 미충족에는 부족분(= 몇 명 더)을 붙인다.
        part = best[2] if best else sorted(cands, key=lambda p: -p["ovr"])[:size]
        if part:
            pch = best_placement(part, FORM_OF.get(r["challenge_ea_id"]))[0]
            for c in breakdown(part, conds, pch):
                print(f"         {'✅' if c['ok'] else '⛔'} {c['text']}"
                      + ("" if c["ok"] else f"  ← {c['gap']}만큼 모자라다"))
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
    # ⭐ `pos`를 함께 싣는다 — 화면이 **포메이션을 바꿔 미리 그릴** 때 필요하다(2026-09-25 사용자 지시
    #    「포메이션을 선택하면 포메이션이 변경돼야 정확히 고를 수 있어」). 없으면 재배치를 못 한다.
    slim = lambda p: {"id": p["id"], "name": p["name"], "ovr": p["ovr"], "club": p["club"],
                      "league": p["league"], "nation": p["nation"], "untradeable": p["is_untradeable"],
                      "pos": sorted(positions_of(p)), "card": p["card_image_url"]}
    bad_save = []
    for r, xi, size, cands, _cd, _b in ok:
        known = FORM_OF.get(r["challenge_ea_id"])
        ch, form, pl = best_placement(xi, known)
        # ⛔⛔ **저장 직전에 다시 검증한다 — 통과 못 하면 ok로 적지 않는다**(2026-09-25 사용자 지적
        #    「노르웨이 대 포르투갈 해법이 문제의 조건을 만족하지 않고 있어」).
        #    탐색이 고른 11명과 **실제로 저장되는 배치**는 다른 단계에서 만들어진다 —
        #    그 사이에 어긋날 여지를 「조심하자」로 막지 않고 여기서 **막는다**(불변규칙 13 ③ 게이트).
        #    ⚠️ 케미는 배치에 의존하므로 `form`을 세워 놓고 재계산한다.
        prev, CUR_FORM[0] = CUR_FORM[0], form
        fail, _c = check(xi, _cd)
        okch, _i = chem_ok(xi, _cd)
        CUR_FORM[0] = prev
        if fail or not okch:
            bad_save.append((r["name"], fail or ["케미 미달"]))
            rows.append((a.game, r["challenge_ea_id"], today, aid, "not_found", None, None, None,
                         len(cands), "저장 직전 재검증 실패: " + " / ".join(fail or ["케미 미달"]), src, conf))
            continue
        # ⭐ 슬롯·좌표를 함께 저장한다 — 화면이 **피치 모양**으로 그린다(2026-09-25 사용자 지시
        #    「포메이션 모습으로 보여줘 · 어떤 포지션의 선수인지도 모르겠어」).
        squad = [dict(slim(p), slot=nm, x=x, y=y, fit=fit, want=want)
                 for nm, x, y, p, fit, want in pl if p]
        rows.append((a.game, r["challenge_ea_id"], today, aid, "ok",
                     json.dumps({"formation": form, "formation_known": bool(known), "partial": False,
                                 "players": squad, "checks": breakdown(xi, _cd, ch)}, ensure_ascii=False),
                     team_rating([p["ovr"] for p in xi]), ch, len(cands), None, src, conf))
    # ⭐⭐ **못 풀어도 최선 스쿼드를 남긴다**(2026-09-25 사용자 지시 「못 풀더라도 현재 스쿼드 기준으로
    #    채울 수 있는 선수들을 채우고 / 만족한 조건과 불만족한 조건을 알려주고 / 어떤 조건을 사야 하는지」).
    #    ⛔ 이건 **제출 가능한 답이 아니다** — `partial=True`로 못박고 화면이 해법과 다르게 그린다.
    for r, _x, size, cands, conds, best in no:
        imp = len(cands) < size
        # 부분 스쿼드: 탐색이 닿은 가장 가까운 11명. 인원 자체가 모자라면(impossible) 통과 카드 전부.
        part = best[2] if best else sorted(cands, key=lambda p: -p["ovr"])[:size]
        known = FORM_OF.get(r["challenge_ea_id"])
        sj = None
        if part:
            prev, CUR_FORM[0] = CUR_FORM[0], None
            ch, form, pl = best_placement(part, known)
            CUR_FORM[0] = prev
            sj = json.dumps({"formation": form, "formation_known": bool(known), "partial": True,
                             "players": [dict(slim(p), slot=nm, x=x, y=y, fit=fit, want=want)
                                         for nm, x, y, p, fit, want in pl if p],
                             "checks": breakdown(part, conds, ch),
                             "hints": [{"text": t, "how": h} for t, h in
                                       group_hints({c["text"] for c in breakdown(part, conds, ch) if not c["ok"]},
                                                   conds)]}, ensure_ascii=False)
        rows.append((a.game, r["challenge_ea_id"], today, aid, "impossible" if imp else "not_found",
                     sj, team_rating([p["ovr"] for p in part]) if part else None,
                     ch if part else None, len(cands),
                     (f"1인 조건 통과 카드 {len(cands)}장 < 필요 {size}명" if imp
                      else "남은 위반: " + " / ".join(best[0]) if best else "해를 못 찾았다"), src, conf))
    for r, conds, cs in oneclick:
        rows.append((a.game, r["challenge_ea_id"], today, aid, "oneclick", None, None, None, len(cs),
                     "원클릭 제출 — fut.gg가 제출 인원을 주지 않아 인원 판정을 하지 않는다", src, conf))
    for r, bad in undec:
        rows.append((a.game, r["challenge_ea_id"], today, aid, "unparsed", None, None, None, None,
                     "못 읽은 조건: " + " / ".join(bad), src, conf))
    if bad_save:
        print(f"\n⛔ 저장 직전 재검증에서 탈락 {len(bad_save)}건 — ok로 적지 않았다(not_found로 내린다):")
        for nm, why in bad_save:
            print(f"   · {nm} — {' / '.join(why)}")
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
