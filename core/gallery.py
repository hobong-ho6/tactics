"""FUT 갤러리 평가 **단일 정본** (2026-10-02 신설 · migration 092).

왜 (사용자 지시 「내 카드들로 어떤 갤러리 팀들을 완성할 수 있는지」):
  갤러리 세트 등급(D~S)은 세트에 넣은 카드의 **아이템 점수** 합으로 매겨진다.
  fut.gg는 세트 정의·등급 임계는 주지만 **내 진행도는 주지 않는다** ⇒ 보유 카드로 우리가 계산한다.

⚠️ 아이템 점수표는 **커뮤니티 정리값**이다(EA 미공개 · 등급 D — 2026-09-26 기준 여러 가이드가 같은 표).
   브론즈 20 · 실버 35 · 골드 75=90 … 84=830 · 85=2,100 …. 스트림라인 SBC의 「Score 제출」과 같은 체계다.
⚠️ **태그 보너스는 넣지 않는다** — 규칙이 자료마다 갈리고(TOTW 4/6/12% ↔ 4/8/15%) fut.gg 조합 점수와 대조해도
   한 건도 정확히 맞지 않았다(0/64 · 차이는 늘 +10~38%로 태그 쪽). 보너스는 **더하기만** 하므로
   여기 등급은 「**적어도 이 등급**」(하한)이다. ⛔ First Owner(+150~500%)는 원장에 이전 소유자 수가
   전부 0으로 와서 가를 수 없다.
⚠️ 갤러리는 **진화 전 원래 카드**로 점수를 매긴다(가이드 공통) ⇒ `player_card_items.ovr`(아이템 정의)를 쓴다.
⚠️ 한 카드를 여러 세트에 쓸 수 있다고 본다(세트에 넣어도 카드가 소모되지 않는다 — 가이드 공통 · 등급 D).
"""
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


def evaluate(sets, cards):
    """세트마다 상위 required장으로 등급을 매긴다. sets: fc_gallery_sets 행(dict) · cards: 보유 카드(dict)."""
    out = []
    for s in sets:
        grades = sorted(json.loads(s["grades_json"] or "[]"), key=lambda g: g["threshold"])
        flags = [(c, eligible(c, s)) for c in cards]
        if any(f is None for _, f in flags):
            out.append(dict(set_id=s["set_id"], supported=0, eligible_n=None, required_n=s["required_cards"],
                            base_score=None, grade=None, next_grade=None, next_gap=None, card_ids=[]))
            continue
        el = [c for c, f in flags if f and item_score(c["ovr"]) is not None]
        el.sort(key=lambda c: -item_score(c["ovr"]))
        req = s["required_cards"] or 0
        pick = el[:req]
        score = sum(item_score(c["ovr"]) for c in pick)
        # ⛔⛔ **필요 장수를 채워야 완성되고, 완성해야 등급을 받는다**(2026-10-02 사용자 지적 「등급은 세트를 완성했을 때만
        #    받을 수 있는 거 아니야?」 · EA 도움말 「You complete a Set by meeting its Player Item requirements. The Item Score …
        #    determines its grade.」). 종전엔 칸을 덜 채워도 점수만 넘으면 등급을 줬다 — Squad Foundations 2/4장에 C를 매겼다.
        #    ⇒ 모자라면 등급 없음(미완성). 점수는 넣을 수 있는 만큼의 합으로 남긴다(얼마나 왔나를 보이려고).
        g = grade_of(score, grades) if pick and len(el) >= req else None
        nxt = next((x for x in grades if score < x["threshold"]), None) if g else None
        out.append(dict(set_id=s["set_id"], supported=1, eligible_n=len(el), required_n=s["required_cards"],
                        base_score=score, grade=g, next_grade=nxt["name"] if nxt else None,
                        next_gap=(nxt["threshold"] - score) if nxt else None, card_ids=[c["id"] for c in pick]))
    return out


# 목록에 올리는 최소 등급. ⭐ D부터 올린다(2026-10-02) — 등급은 **세트를 완성해야** 받으므로(필요 장수를 다 채워야)
#   D도 「카드 한 장」이 아니라 15~30장을 채운 결과다. 종전 C 기준은 「칸을 덜 채워도 등급」이라는 틀린 가정 위에 있었다.
MIN_LIST = "D"


def classify(evals, prev, mine):
    """평가 행 → (달성 가능, 더 높일 수 있음, NEW). ⛔ 스크립트와 export가 **이 함수 하나**를 쓴다.
       · 달성 가능 = 기록이 없고 C 이상이 나온다 · 더 높일 수 있음 = 기록보다 높은 등급이 나온다
       · NEW = 그중 **직전 회차보다** 등급이 오른 것(첫 회차는 비교 대상이 없어 비운다)."""
    rk = lambda g: RANK.get(g, -1)                                               # noqa: E731
    reach, higher, new = [], [], []
    for r in evals:
        if not r.get("supported", 1):
            continue
        g, sid = r["grade"], r["set_id"]
        if rk(g) < RANK[MIN_LIST] or rk(g) <= rk(mine.get(sid)):
            continue
        (higher if sid in mine else reach).append(sid)
        if prev and rk(g) > rk(prev.get(sid)):
            new.append(sid)
    return reach, higher, new
