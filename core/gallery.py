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
   ⭐ **First Owner**(+150/300/500%)는 「보유한 사람 수」(GG Club numberOfOwners)가 **0이나 1**인 카드로 본다
      (2026-10-03 사용자 지적 「보유한 사용자 수가 0이나 1이면 되잖아」). 검증: 아스톤 빌라 First Owner 카드는 4장뿐이라
      5장 문턱에 못 미쳐 보너스가 없다 — 실측 4,524가 +150% 없이 추정 4,413 근처였던 것과 맞는다.
   ⛔ Holographic은 원장에 여부가 없어 넣지 않는다.
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
TAGS = {"first": [(5, 150), (10, 300), (20, 500)], "bronze": [(5, 20), (10, 40), (20, 80)], "silver": [(5, 15), (10, 30), (20, 60)], "golden": [(5, 1), (10, 2), (20, 4)],
        "club": [(5, 1), (10, 2), (20, 4)], "league": [(5, 1), (10, 2), (20, 8)], "nation": [(5, 1), (10, 2), (20, 4)],
        "diffclub": [(5, 1), (10, 2), (20, 4)], "diffleague": [(5, 1), (10, 2), (20, 4)], "diffnation": [(5, 1), (10, 2), (20, 4)],
        "def": [(5, 3), (10, 6), (15, 10)], "mid": [(5, 3), (10, 6), (15, 10)], "att": [(5, 3), (10, 6), (15, 10)],
        "gk": [(3, 3), (6, 6), (10, 15)], "totw": [(3, 4), (6, 8), (10, 15)], "hero": [(2, 8), (4, 12), (6, 20)],
        "icon": [(2, 10), (4, 15), (6, 25)], "skill": [(3, 3), (5, 6), (10, 12)], "wf": [(3, 3), (5, 6), (10, 12)],
        "multi": [(2, 10), (3, 15), (4, 20)]}
TAG_KR = {"first": "퍼스트 오너", "bronze": "브론즈", "silver": "실버", "golden": "골드", "club": "같은 클럽", "league": "같은 리그", "nation": "같은 국적",
          "diffclub": "다른 클럽", "diffleague": "다른 리그", "diffnation": "다른 국적", "def": "수비진", "mid": "중원",
          "att": "공격진", "gk": "골키퍼", "totw": "TOTW", "hero": "히어로", "icon": "아이콘", "skill": "개인기 5성",
          "wf": "약발 5성", "multi": "같은 선수 중복"}
# ⭐ 태그 설명·영문 이름(2026-10-03 사용자 지시 「태그별 가산점을 정리해서 갤러리 탭에 정보 넣어」).
#   화면은 이 표와 TAGS를 export로 받아 그린다(⛔ 화면이 다시 적지 않는다). 영문 이름은 공개 21종 정리(timesaver)의 표기다.
TAG_INFO = {
    "first": ("First Owner", "보유한 사람 수 0·1(팩·보상으로 처음 받은 카드)"),
    "bronze": ("Bronze", "OVR 64 이하"), "silver": ("Silver", "OVR 65~74"), "golden": ("Golden", "OVR 75 이상"),
    "club": ("Same Club", "가장 많은 같은 클럽 카드(여자팀은 다른 클럽)"), "league": ("Same League", "가장 많은 같은 리그 카드"),
    "nation": ("Same Nation", "가장 많은 같은 국적 카드"),
    "diffclub": ("Different Club", "서로 다른 클럽 수 — 클럽마다 최고 점수 1장에만 가산(클럽 없는 카드는 각자 별개 · 여자팀은 다른 클럽)"),
    "diffleague": ("Different League", "서로 다른 리그 수 — 리그마다 최고 점수 1장에만 가산"), "diffnation": ("Different Nation", "서로 다른 국적 수 — 국적마다 최고 점수 1장에만 가산"),
    "def": ("Defensive Wall", "CB·LB·RB — 보조 포지션 포함"), "mid": ("Midfield Control", "CDM·CM·CAM·LM·RM — 보조 포지션 포함"),
    "att": ("All out Attack", "ST·RW·LW — 보조 포지션 포함"), "gk": ("Hands Only", "골키퍼"),
    "totw": ("TOTW", "Team of the Week 카드"), "hero": ("Heroic", "히어로 카드"), "icon": ("Iconic", "아이콘 카드"),
    "skill": ("Skilled", "개인기 5성"), "wf": ("Ambidextrous", "약발 5성"), "multi": ("Multiples", "같은 선수의 다른 버전 카드 — 가장 큰 묶음 하나에만 가산(같은 카드 두 장은 한 장만 들어간다)"),
}
# 계산에 넣지 못한 태그 — 화면이 「미반영」으로 함께 보여 준다(조용히 빼지 않는다).
TAG_UNUSED = [{"name": "Holographic", "kr": "홀로그램", "desc": "홀로그램 카드", "tiers": [[2, 8], [4, 12], [6, 20]],
               "why": "원장에 홀로그램 여부가 없다"}]


# ⭐ 인게임 「태그 용어집」에서 단계까지 확인한 태그(2026-10-03 PS 리모트 캡처 · captures/gallery-2026-10-03 · 등급 A).
#    용어집은 21칸이고 나머지 9칸은 「미발견」(해당 태그를 아직 받은 적 없음)이라 문구가 안 보인다 → 공개 표(등급 D).
#    확인한 12종은 공개 표와 단계·%가 전부 같았다.
TAG_VERIFIED = {"att", "mid", "def", "gk", "multi", "first", "golden", "league", "club", "diffclub", "diffnation", "nation"}


def tag_table():
    """화면용 태그 정리표 — [{key, name, kr, desc, tiers:[[개수, %]], applied, grade}]."""
    # 나머지 8종은 fut.gg 페이지에 내장된 EA 형식 태그 정의(capturedAt 2026-09-27)와 일치 — 데이터마이닝 등급 B(2026-10-03 조사)
    rows = [{"key": k, "name": TAG_INFO[k][0], "kr": TAG_KR[k], "desc": TAG_INFO[k][1],
             "tiers": [list(t) for t in TAGS[k]], "applied": True, "grade": "A" if k in TAG_VERIFIED else "B"}
            for k in TAGS]
    return rows + [dict(u, key=None, applied=False, grade="B") for u in TAG_UNUSED]


# ⭐ 포지션 목록은 인게임 태그 용어집 문구 그대로다(2026-10-03 캡처 · 등급 A) — FC27 카드에 CF·LWB·RWB는 없다(545장 0).
POS_GROUP = {"def": {"CB", "LB", "RB"}, "mid": {"CDM", "CM", "CAM", "LM", "RM"},
             "att": {"ST", "RW", "LW"}, "gk": {"GK"}}


def _pct(n, table):
    p = 0
    for m, pc in table:
        if n >= m:
            p = pc
    return p


def is_first_owner(c):
    """보유한 사람 수 0·1 = 처음 가진 사람이 나(팩·보상). 값이 없으면 판정하지 않는다(⛔ 지어내지 않는다)."""
    n = c.get("number_of_owners")
    return n is not None and n <= 1


def _poss(c):
    """카드의 **모든** 포지션(주+보조). ⭐ 포지션 태그는 보조 포지션까지 센다(2026-10-03 인게임 실측 · 등급 C —
       아스톤 빌라에서 Cash RB/RM·Maatsen LB/LM이 수비벽과 미드필드 컨트롤 양쪽에 하이라이트됐다)."""
    return set((c.get("positions") or c.get("best_pos") or "").split("/")) - {""}


def _club_key(c):
    """같은/다른 클럽 판정 키 = (클럽, 리그). ⛔ fut.gg는 여자팀에 남자팀 클럽 id를 준다(빌라 여자팀도 2)
       — 인게임은 여자팀을 **다른 클럽**으로 본다(Kielland가 같은 클럽 태그에서 빠짐 · 2026-10-03 실측 · 등급 C)."""
    return None if c.get("club_ea_id") is None else (c["club_ea_id"], c.get("league_ea_id"))


def tag_bonus(cards):
    """카드 묶음 → (기본 점수, 태그 보너스 추정, 내역 {태그: (개수, %, 보너스)})."""
    sc = lambda L: sum(card_score(c) or 0 for c in L)                            # noqa: E731
    out, bonus = {}, 0.0

    # ⭐⭐ 태그마다 **해당 카드 점수 합 × % 를 내림**한다(2026-10-03 인게임 실측 · 등급 C —
    #    아스톤 빌라 보너스 544 = 192+40+79+79+77+77, 스타터 세트 4,113 = 4,035+26×3 둘 다 1점 단위 일치).
    def add(k, L, n=None):
        nonlocal bonus
        n = len(L) if n is None else n
        p = _pct(n, TAGS[k])
        if p:
            v = sc(L) * p // 100
            bonus += v
            out[k] = (n, p, v)
    ovr = lambda c: c.get("ovr") or 0                                            # noqa: E731
    add("first", [c for c in cards if is_first_owner(c)])
    add("bronze", [c for c in cards if ovr(c) <= 64])
    add("silver", [c for c in cards if 65 <= ovr(c) <= 74])
    add("golden", [c for c in cards if ovr(c) >= 75])
    for k, key in (("club", _club_key), ("league", lambda c: c.get("league_ea_id")), ("nation", lambda c: c.get("nation"))):
        grp = collections.defaultdict(list)
        for c in cards:          # 값이 없는 카드(클럽 없는 히어로 등)는 각자 다른 값으로 센다(fut.gg 조합 재현에서 확인)
            grp[key(c) if key(c) is not None else ("none", id(c))].append(c)
        real = [g for v, g in grp.items() if not (isinstance(v, tuple) and v and v[0] == "none")]
        if real:
            # 「Same」 = 가장 큰 무리 하나(동률이면 점수 합이 큰 쪽)
            add(k, max(real, key=lambda g: (len(g), sc(g))))
        # ⭐ 「Different」 = 서로 다른 값의 **개수**로 단계를 정하고, 보너스는 **값마다 점수가 가장 높은 카드 1장씩**의 합에 붙는다
        #    (fut.gg 갤러리 계산기 152건 전부 일치 · 등급 B — 2026-10-03 커뮤니티 조사). 종전엔 전체 카드에 붙여 과대 추정했다.
        add("diff" + k, [max(g, key=lambda c: card_score(c) or 0) for g in grp.values()])
    for k, ps in POS_GROUP.items():
        add(k, [c for c in cards if _poss(c) & ps])
    # TOTW = rarity 3(fut.gg에 내장된 EA 형식 태그 정의 `RARE 3` · 등급 B). 희귀도 id가 없으면 이름으로
    add("totw", [c for c in cards if c.get("rarity_ea_id") == 3
                 or (c.get("rarity_ea_id") is None and "week" in (c.get("rarity_name") or "").lower())])
    add("hero", [c for c in cards if c.get("is_hero")])
    add("icon", [c for c in cards if c.get("is_icon")])
    add("skill", [c for c in cards if (c.get("skill_moves") or 0) >= 5])
    add("wf", [c for c in cards if (c.get("weak_foot") or 0) >= 5])
    # ⭐ 「중복!」 = 같은 선수(BASE_DEF_ID) 중 **가장 큰 묶음 하나**(동률이면 점수 합이 큰 쪽)에만 붙는다
    #    (fut.gg 내장 EA 형식 정의 + 계산기 16건 재현 · 등급 B — 2026-10-03). 종전엔 중복된 카드 전부에 붙였다.
    bg = collections.defaultdict(list)
    for c in cards:
        if c.get("base_ea_id"):
            bg[c["base_ea_id"]].append(c)
    big = max(bg.values(), key=lambda g: (len(g), sc(g)), default=[])
    if len(big) >= 2:
        add("multi", big)
    # ⚠️ **가장 큰 태그 10개만** 반영한다(futgenie 「only the ten biggest tags count(가장 큰 태그 10개만 반영)」 · 단일 출처 D —
    #    인게임 프리미어 리그·라리가 화면의 태그 칩도 정확히 10개였다 2026-10-03). 11번째부터 버린다.
    if len(out) > 10:
        keep = sorted(out, key=lambda k: -out[k][2])[:10]
        out = {k: out[k] for k in keep}
        bonus = sum(v[2] for v in out.values())
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
    # ⭐ First Owner 문턱(5·10·20장)을 채우는 조합도 후보로 넣는다 — +150% 이상이라 점수 순 선택을 뒤집을 수 있다.
    fo = [c for c in el if is_first_owner(c)]
    other = [c for c in el if not is_first_owner(c)]
    for k in (5, 10, 20):
        if len(fo) >= k and k <= req:
            # 문턱 k장은 First Owner로 채우고, 남는 칸은 점수 순(First Owner 포함)으로
            pick = fo[:k]
            cands.append(pick + [c for c in el if c not in pick][:req - k])
    if fo:
        cands.append((fo + other)[:req])           # First Owner를 최대한 먼저
    best = max(cands, key=lambda P: sum(tag_bonus(P)[:2]))
    return best


PLACED_ID0 = 1_000_000   # 인게임 전사 카드의 id = −(PLACED_ID0 + fut_gallery_placed.id) — 원장(양수)·스토리지(음수 작은 값)와 안 겹친다


def placed_cards(con, game="FC27"):
    """세트별 **인게임에 이미 들어가 있는** 아이템 중 우리 원장에 없는 것(migration 098 · 세트별 최신 캡처).
       ⭐ 넣은 아이템은 팔아도 남는다(EA 딥다이브 A) ⇒ 그 세트 후보에 무조건 들어간다. ⛔ 정본은 이 함수 하나다.
       원장과 맞은 행(club_player_id)은 원장 카드로 이미 후보라 뺀다. 아이템이 식별되면 그 아이템 정보를, 아니면 전사값만 쓴다
       — 미식별 카드는 클럽·리그를 세트 기준으로만 안다(태그 추정이 약간 거칠다)."""
    sets = {r[0]: (r[1], r[2]) for r in con.execute(
        """SELECT set_id, club_ea_id, league_ea_id FROM fc_gallery_sets WHERE game_version=?
             AND pulled=(SELECT MAX(pulled) FROM fc_gallery_sets WHERE game_version=?)""", (game, game))}
    item = {r[0]: r for r in con.execute(
        """SELECT ea_item_id, club_ea_id, league_ea_id, nation, positions, best_pos, base_ea_id, rarity_name,
                  COALESCE(is_icon,0), COALESCE(is_hero,0), skill_moves, weak_foot FROM player_card_items WHERE game_version=?""", (game,))}
    out = collections.defaultdict(list)
    for pid, sid, slot, sc, ov, pos, nat, ea in con.execute(
            """SELECT id, set_id, slot, score, ovr, pos, nation, ea_item_id FROM fut_gallery_placed p
                WHERE game_version=? AND club_player_id IS NULL
                  AND captured_at=(SELECT MAX(captured_at) FROM fut_gallery_placed WHERE game_version=p.game_version AND set_id=p.set_id)""",
            (game,)):
        club, league = sets.get(sid, (None, None))
        league = league or LEAGUE_SET.get(sid)
        # ⚠️ 원장 밖 아이템 = 싱크 사이에 들어왔다 바로 나간 카드(팩 → SBC·판매)라 **처음 가진 사람이 나**로 본다(퍼스트 오너).
        #    근거: 인게임 스냅숏 보너스가 이 가정에서만 맞는다(프리미어 리그·라리가·세리에 A — gallery_placed_load 검증 표) · 등급 C.
        c = dict(id=-(PLACED_ID0 + pid), name=f"인게임 #{slot}", placed=1, number_of_owners=1, grading_score=sc, ovr=ov,
                 positions=pos, best_pos=pos, nation=nat, club_ea_id=club, league_ea_id=league, ea_item_id=ea)
        if ea in item:
            _, c["club_ea_id"], c["league_ea_id"], c["nation"], c["positions"], c["best_pos"], c["base_ea_id"], c["rarity_name"], \
                c["is_icon"], c["is_hero"], c["skill_moves"], c["weak_foot"] = item[ea]
        out[sid].append(c)
    return dict(out)


def evaluate(sets, cards, placed=None):
    """세트마다 필요 장수로 등급을 매긴다. sets: fc_gallery_sets 행(dict) · cards: 클럽을 거친 카드(dict)
       · placed: {set_id: [카드]} 인게임에 이미 들어가 있는 원장 밖 아이템(placed_cards) — 그 세트 후보에 더한다."""
    placed = placed or {}
    # ⛔ **같은 카드(아이템)는 한 장만** 들어간다(2026-10-03 사용자 인게임 실측 「맥긴을 SBC 스토리지에 한 장 더 들고 있지만
    #    실제 갤러리에는 두 장이 안 들어간다」 · 등급 C). 「같은 선수 중복(Multiples)」은 **다른 버전**의 같은 선수다
    #    (예: 기본 카드 + 특수 카드 — base_ea_id가 같고 아이템이 다름). ⇒ 아이템당 한 장, 클럽 카드(양수 id)를 남긴다.
    seen, uniq = set(), []
    for c in sorted(cards, key=lambda c: c["id"] < 0):
        k = c.get("ea_item_id") or ("id", c["id"])
        if k not in seen:
            seen.add(k)
            uniq.append(c)
    cards = uniq
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
        have = {c.get("ea_item_id") for c in el if c.get("ea_item_id")}
        el += [c for c in placed.get(s["set_id"], []) if not c.get("ea_item_id") or c["ea_item_id"] not in have]
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
