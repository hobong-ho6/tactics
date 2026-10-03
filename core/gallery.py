"""FUT 갤러리 평가 **단일 정본** (2026-10-02 신설 · migration 092).

왜 (사용자 지시 「내 카드들로 어떤 갤러리 팀들을 완성할 수 있는지」):
  갤러리 세트 등급(D~S)은 세트에 넣은 카드의 **아이템 점수** 합으로 매겨진다.
  fut.gg는 세트 정의·등급 임계는 주지만 **내 진행도는 주지 않는다** ⇒ 보유 카드로 우리가 계산한다.

⭐ 카드 점수는 **fut.gg `gradingScore`**를 쓴다(2026-10-02 · migration 094 · 등급 B — EA 데이터를 fut.gg가 전달).
   아스톤 빌라 27장 대조에서 아래 커뮤니티 표와 27/27 일치했고, 표에 없는 카드(아이콘·특별·98)까지 값이 있다.
   ⚠️ 아래 표(`item_score`)는 그 값이 **결손일 때만** 대신한다(커뮤니티 정리값 · 등급 D).
   브론즈 20 · 실버 35 · 골드 75=90 … 84=830 · 85=2,100 …. 스트림라인 SBC의 「Score 제출」과 같은 체계다.
⭐⭐ **태그 보너스를 추정한다**(2026-10-03 사용자 지시 「태그로 인해 점수를 더 얻는 부분을 분석하고 갤러리 시스템에 반영」).
   분석: fut.gg가 세트마다 풀어 둔 최저가 조합 347개(카드 2,542장)의 총점을 재현하는 규칙을 찾았다.
   ⑴ 태그 %는 **그 태그에 해당하는 카드의 점수에만** 붙는다(세트 전체가 아니다 — 전체 방식은 오차 중앙값 +8%로 기각).
   ⑵ 같은 선수 두 장 이상은 「Multiples」 · 클럽 없는 카드(히어로)는 「Different Club」에서 각자 다른 값 · 「Same」은 최대 그룹.
   ⑶ 표는 공개 21종(timesaver 정리 · 등급 D). 재현 정확도: 오차 중앙값 −1.3%(약간 낮게) · |오차| 90%가 4% 안 ·
      정확 일치 26/347 — ⇒ **정확한 식이 아니라 추정**이다. 아스톤 빌라 실측 4,524 ↔ 추정 최적 4,413(−2.5%)로 같은 경향.
   ⇒ 등급은 두 개를 둔다: `grade` = 기본 점수만(**확정 하한**) · `est_grade` = 태그 포함 **추정**.
   ⛔ First Owner(+150~500%)·Holographic은 넣지 않는다 — 이전 소유자 수가 「본인 포함」인지 미확정이고
      홀로그램 여부는 원장에 없다. 그래서 실제 점수는 추정보다 **더 높을 수** 있다.
⚠️ 갤러리는 **진화 전 원래 카드**로 점수를 매긴다(가이드 공통) ⇒ `player_card_items.ovr`(아이템 정의)를 쓴다.
⚠️ 한 카드를 여러 세트에 쓸 수 있다고 본다(세트에 넣어도 카드가 소모되지 않는다 — 가이드 공통 · 등급 D).
"""
import collections
import json

GRADES = ["D", "C", "B", "A", "S"]
RANK = {g: i for i, g in enumerate(GRADES)}

_GOLD = {75: 90, 76: 100, 77: 120, 78: 140, 79: 160, 80: 180, 81: 280, 82: 340, 83: 410, 84: 830,
         85: 2100, 86: 4100, 87: 5500, 88: 8300, 89: 11000, 90: 14000, 91: 19000, 92: 20000, 93: 25000,
         94: 30000, 95: 40000, 96: 55000, 97: 85000, 99: 100000}


def item_score(ovr):
    """OVR → 아이템 점수. 표에 없는 값(98)은 None(⛔ 지어내지 않는다)."""
    if ovr is None:
        return None
    if ovr <= 64:
        return 20
    if ovr <= 74:
        return 35
    return _GOLD.get(ovr)


# 리그 세트 → EA 리그 id. ⛔ 세트 정의에 리그 id가 없어(이름뿐) **fut.gg가 그 세트에 대해 풀어 둔 조합 카드**의
#   리그 id로 정했다(2026-10-02 — 9세트 모두 조합 20장이 한 리그였다). 이름 문자열로 잇지 않는다(불변규칙 6).
LEAGUE_SET = {108: 13, 100: 2216, 103: 31, 109: 53, 111: 16, 115: 2218, 120: 2215, 121: 2222, 122: 19}
# 희귀도 세트 판정. 대상 규칙을 못 정한 세트는 **판정하지 않는다**(supported=0) — 지어내지 않는다.
RARITY_RULE = {
    99: lambda c: c["rarity_ea_id"] == 3,                         # TOTW (fut.gg 조합 20장 전부 rarityEaId 3)
    102: lambda c: bool(c["is_hero"]),                            # Heroes
    114: lambda c: (c["rarity_name"] or "") == "Squad Foundations",
    116: lambda c: not c["is_special"],                           # Starter Set — 「Bronze, Silver or Gold players」
}


def card_score(c):
    """카드 한 장의 갤러리 점수 — fut.gg gradingScore가 정본, 없으면 표."""
    gs = c.get("grading_score")
    return gs if gs is not None else item_score(c["ovr"])


def eligible(card, s):
    """카드가 세트에 들어가는가. 판정 규칙이 없으면 None."""
    if s["club_ea_id"]:
        return s["club_ea_id"] in (card["club_ea_id"], card["sibling_club_ea_id"])
    if s["set_id"] in LEAGUE_SET:
        return card["league_ea_id"] == LEAGUE_SET[s["set_id"]]
    rule = RARITY_RULE.get(s["set_id"])
    return None if rule is None else rule(card)


def grade_of(score, grades):
    got = None
    for g in grades:
        if score >= g["threshold"]:
            got = g["name"]
    return got


# ── 태그 보너스(추정) ─────────────────────────────────────────────────────────────────────
# (최소 개수, %) 구간표 — 공개 21종 중 원장으로 가를 수 있는 것만(First Owner·Holographic 제외 · 위 머리말).
TAGS = {"bronze": [(5, 20), (10, 40), (20, 80)], "silver": [(5, 15), (10, 30), (20, 60)], "golden": [(5, 1), (10, 2), (20, 4)],
        "club": [(5, 1), (10, 2), (20, 4)], "league": [(5, 1), (10, 2), (20, 8)], "nation": [(5, 1), (10, 2), (20, 4)],
        "diffclub": [(5, 1), (10, 2), (20, 4)], "diffleague": [(5, 1), (10, 2), (20, 4)], "diffnation": [(5, 1), (10, 2), (20, 4)],
        "def": [(5, 3), (10, 6), (15, 10)], "mid": [(5, 3), (10, 6), (15, 10)], "att": [(5, 3), (10, 6), (15, 10)],
        "gk": [(3, 3), (6, 6), (10, 15)], "totw": [(3, 4), (6, 8), (10, 15)], "hero": [(2, 8), (4, 12), (6, 20)],
        "icon": [(2, 10), (4, 15), (6, 25)], "skill": [(3, 3), (5, 6), (10, 12)], "wf": [(3, 3), (5, 6), (10, 12)],
        "multi": [(2, 10), (3, 15), (4, 20)]}
TAG_KR = {"bronze": "브론즈", "silver": "실버", "golden": "골드", "club": "같은 클럽", "league": "같은 리그", "nation": "같은 국적",
          "diffclub": "다른 클럽", "diffleague": "다른 리그", "diffnation": "다른 국적", "def": "수비진", "mid": "중원",
          "att": "공격진", "gk": "골키퍼", "totw": "TOTW", "hero": "히어로", "icon": "아이콘", "skill": "개인기 5성",
          "wf": "약발 5성", "multi": "같은 선수 중복"}
POS_GROUP = {"def": {"CB", "LB", "RB", "LWB", "RWB"}, "mid": {"CDM", "CM", "CAM", "LM", "RM"},
             "att": {"ST", "RW", "LW", "CF"}, "gk": {"GK"}}


def _pct(n, table):
    p = 0
    for m, pc in table:
        if n >= m:
            p = pc
    return p


def tag_bonus(cards):
    """카드 묶음 → (기본 점수, 태그 보너스 추정, 내역 {태그: (개수, %, 보너스)})."""
    sc = lambda L: sum(card_score(c) or 0 for c in L)                            # noqa: E731
    out, bonus = {}, 0.0

    def add(k, L, n=None):
        nonlocal bonus
        n = len(L) if n is None else n
        p = _pct(n, TAGS[k])
        if p:
            v = sc(L) * p / 100
            bonus += v
            out[k] = (n, p, round(v, 1))
    ovr = lambda c: c.get("ovr") or 0                                            # noqa: E731
    add("bronze", [c for c in cards if ovr(c) <= 64])
    add("silver", [c for c in cards if 65 <= ovr(c) <= 74])
    add("golden", [c for c in cards if ovr(c) >= 75])
    for k, col in (("club", "club_ea_id"), ("league", "league_ea_id"), ("nation", "nation")):
        cnt = collections.Counter(c.get(col) for c in cards if c.get(col) is not None)
        if cnt:
            top = cnt.most_common(1)[0][0]
            add(k, [c for c in cards if c.get(col) == top])
        # 「Different」 — 값이 없는 카드(클럽 없는 히어로 등)는 각자 다른 값으로 센다(fut.gg 조합 재현에서 확인)
        add("diff" + k, cards, len({c.get(col) if c.get(col) is not None else ("none", id(c)) for c in cards}))
    for k, ps in POS_GROUP.items():
        add(k, [c for c in cards if (c.get("best_pos") or "") in ps])
    add("totw", [c for c in cards if "week" in (c.get("rarity_name") or "").lower()])
    add("hero", [c for c in cards if c.get("is_hero")])
    add("icon", [c for c in cards if c.get("is_icon")])
    add("skill", [c for c in cards if (c.get("skill_moves") or 0) >= 5])
    add("wf", [c for c in cards if (c.get("weak_foot") or 0) >= 5])
    bc = collections.Counter(c.get("base_ea_id") for c in cards if c.get("base_ea_id"))
    dup = [c for c in cards if c.get("base_ea_id") and bc[c["base_ea_id"]] >= 2]
    if dup:
        add("multi", dup, max(bc.values()))
    return sc(cards), bonus, out


def _best_pick(el, req):
    """태그 포함 추정 총점이 가장 높은 req장. 점수 순 상위 + **포지션 구성별 상위**를 견준다
       (태그가 포지션 구성에 붙어서 「점수 높은 순」이 최선이 아닐 수 있다)."""
    el = sorted(el, key=lambda c: -(card_score(c) or 0))
    cands = [el[:req]]
    grp = {k: [c for c in el if (c.get("best_pos") or "") in ps] for k, ps in POS_GROUP.items()}
    rest = [c for c in el if not any((c.get("best_pos") or "") in ps for ps in POS_GROUP.values())]
    G = [grp["def"], grp["mid"], grp["att"], grp["gk"]]
    for d in range(min(req, len(G[0])) + 1):
        for m in range(min(req - d, len(G[1])) + 1):
            for a in range(min(req - d - m, len(G[2])) + 1):
                g = req - d - m - a
                pick = G[0][:d] + G[1][:m] + G[2][:a] + G[3][:min(g, len(G[3]))]
                if len(pick) < req:
                    pick += rest[:req - len(pick)]
                if len(pick) == req:
                    cands.append(pick)
    best = max(cands, key=lambda P: sum(tag_bonus(P)[:2]))
    return best


def evaluate(sets, cards):
    """세트마다 필요 장수로 등급을 매긴다. sets: fc_gallery_sets 행(dict) · cards: 보유 카드(dict)."""
    out = []
    for s in sets:
        grades = sorted(json.loads(s["grades_json"] or "[]"), key=lambda g: g["threshold"])
        flags = [(c, eligible(c, s)) for c in cards]
        if any(f is None for _, f in flags):
            out.append(dict(set_id=s["set_id"], supported=0, eligible_n=None, required_n=s["required_cards"],
                            base_score=None, grade=None, next_grade=None, next_gap=None, card_ids=[],
                            est_score=None, est_grade=None, tag_detail=None))
            continue
        el = [c for c, f in flags if f and card_score(c) is not None]
        req = s["required_cards"] or 0
        # ⛔⛔ **필요 장수를 채워야 완성되고, 완성해야 등급을 받는다**(2026-10-02 사용자 지적 · EA 도움말
        #    「You complete a Set by meeting its Player Item requirements. The Item Score … determines its grade.」).
        complete = bool(el) and len(el) >= req
        pick = _best_pick(el, req) if complete else sorted(el, key=lambda c: -(card_score(c) or 0))[:req]
        base, bonus, detail = tag_bonus(pick)
        est = round(base + bonus)
        g = grade_of(base, grades) if complete else None           # 확정 하한(기본 점수만)
        eg = grade_of(est, grades) if complete else None           # 태그 포함 추정
        nxt = next((x for x in grades if est < x["threshold"]), None) if complete else None
        out.append(dict(set_id=s["set_id"], supported=1, eligible_n=len(el), required_n=s["required_cards"],
                        base_score=base, grade=g, next_grade=nxt["name"] if nxt else None,
                        next_gap=(nxt["threshold"] - est) if nxt else None, card_ids=[c["id"] for c in pick],
                        est_score=est, est_grade=eg,
                        tag_detail=json.dumps({TAG_KR[k]: v for k, v in detail.items()}, ensure_ascii=False)))
    return out


# 목록에 올리는 최소 등급. ⭐ D부터 올린다(2026-10-02) — 등급은 **세트를 완성해야** 받으므로(필요 장수를 다 채워야)
#   D도 「카드 한 장」이 아니라 15~30장을 채운 결과다. 종전 C 기준은 「칸을 덜 채워도 등급」이라는 틀린 가정 위에 있었다.
MIN_LIST = "D"


def classify(evals, prev, mine):
    """평가 행 → (달성 가능, 더 높일 수 있음, NEW). ⛔ 스크립트와 export가 **이 함수 하나**를 쓴다.
       · 달성 가능 = 기록이 없고 (태그 포함 추정으로) MIN_LIST 이상이 나온다 · 더 높일 수 있음 = 기록보다 높은 등급이 나온다
       · NEW = 그중 **직전 회차보다** 등급이 오른 것(첫 회차는 비교 대상이 없어 비운다)."""
    rk = lambda g: RANK.get(g, -1)                                               # noqa: E731
    reach, higher, new = [], [], []
    for r in evals:
        if not r.get("supported", 1):
            continue
        # ⭐ 목록은 **태그 포함 추정 등급**으로 가른다(2026-10-03) — 확정 하한(grade)은 화면이 함께 보여 준다.
        g, sid = (r.get("est_grade") or r["grade"]), r["set_id"]
        if rk(g) < RANK[MIN_LIST] or rk(g) <= rk(mine.get(sid)):
            continue
        (higher if sid in mine else reach).append(sid)
        if prev and rk(g) > rk(prev.get(sid)):
            new.append(sid)
    return reach, higher, new


def mine(con, game="FC27"):
    """세트별 **지금 내 등급** = 완성 원장(`fut_gallery_completions`)의 최신 행. ⛔ 정본은 이 함수 하나다(migration 093)."""
    return {sid: g for sid, g in con.execute(
        """SELECT set_id, grade FROM fut_gallery_completions c
            WHERE game_version=? AND id=(SELECT MAX(id) FROM fut_gallery_completions
                                          WHERE game_version=c.game_version AND set_id=c.set_id)""", (game,))}
