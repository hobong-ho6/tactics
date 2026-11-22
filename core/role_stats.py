"""게임 역할 판정 = 히트맵(커널) + 실제 경기 스탯 합산 — 정본 (2026-11-22 신설).

왜(사용자 지시 2026-11-22 「게임 역할 정할때 히트맵과 선수 역할, 스탯등도 참조하도록 해줘」 · 선택: 실제 경기
스탯·행동 / 점수 합산):
  종전 역할 판정은 커널(서는 위치 그리드)뿐이라, 같은 자리에 서서 **다른 일을 한 선수**를 가르지 못했다.
  실증(선덜랜드전 11-21): 알리송 = 윙어 자리 + 크로스 0 · 박스 터치 9 / 카마라·고레츠카 = 둘 다 딥라잉/로밍
  1위인데 패스 90 vs 37.

스탯 쪽 근거:
  역할·포커스마다 EA가 단 특성 태그(`game_role_focus.plus` / `.negative` · 등급 A)를 **측정 가능한 스탯**에
  대응시킨다(TRAIT 표). 85개 조합에 손으로 기대치를 적지 않고, 태그 하나당 한 줄만 정한다.
  ⚠️ 태그 → 스탯 대응 자체는 **판단값**이다(EA가 태그의 스탯 정의를 밝힌 적 없음 · 등급 D). 위치만 뜻하는 태그
  (Movement·Out of Position·Stamina Usage 등)는 커널이 이미 보므로 넣지 않는다.
  - plus 태그: 그 행동이 많을수록 맞다 · negative 태그: 그 역할의 약점이라 **적을수록** 맞다(1 − 백분위).

정규화:
  같은 라인군(넓은 쪽 W+WM · CAM · CM+DM · FB · CB · ST)에서 뛴 경기 기록(45분+)과 비교한 백분위 0~1.
  출전 합계 45분 미만이면 스탯을 쓰지 않는다(90분 환산 부풀림). 빠진 스탯은 건너뛰고, 측정 가능한 태그가 하나도 없거나 스탯이 없으면 stat_fit=None → 커널 단독(표시한다).

합산: score = W_KERNEL × 커널 적합 + W_STATS × 스탯 적합 (W = 0.6 / 0.4 · 사용자 선택 「점수 합산」).
  ⛔ 이 가중을 다른 곳에서 다시 정의하지 않는다 — 여기서 import한다(불변규칙 13 ② 단일 정본).
  GK는 커널 단독(측정 가능한 태그 대응 없음).
"""
import bisect
import json

from core.classify import GROUP

__all__ = ["W_KERNEL", "W_STATS", "TRAIT", "POOL", "features", "Reference", "stat_fit", "rank"]

W_KERNEL, W_STATS = 0.6, 0.4
MIN_MIN = 45
# 백분위 비교군 — 슬롯 라인군을 기능이 비슷한 것끼리 묶는다(표본 확보).
POOL = {"W": "WIDE", "WM": "WIDE", "CAM": "CAM", "CM": "MID", "DM": "MID", "FB": "FB", "CB": "CB", "ST": "ST", "GK": "GK"}

# 특성 태그 → [(스탯 키, 부호)] · 부호 −1 = 적을수록 그 특성(예: 중앙 지원 = 크로스가 적다).
TRAIT = {
    "Defending": [("tkl_int", 1), ("recoveries", 1)],
    "Defence Support": [("tkl_int", 1), ("recoveries", 1)],
    "Supports the Defence": [("tkl_int", 1), ("recoveries", 1)],
    "Defence Option": [("tkl_int", 1)],
    "Aggressiveness": [("tackles", 1), ("duels_won", 1)],
    "Pressure": [("recoveries", 1), ("tackles", 1)],
    "Physical": [("duels_won", 1), ("aerials_won", 1)],
    "Creative": [("key_passes", 1), ("xa", 1), ("line_breaking", 1)],
    "Attacking": [("shots", 1), ("xg", 1)],
    "Attacking Runs": [("box_touches", 1), ("recv_through", 1)],
    "Attack Support": [("opp_half_share", 1), ("key_passes", 1)],
    "Supports Attacks": [("opp_half_share", 1), ("key_passes", 1)],
    "Supports Attack": [("opp_half_share", 1), ("key_passes", 1)],
    "Supports Play": [("passes", 1)],
    "Build-Up Support": [("passes", 1), ("line_breaking", 1), ("long_att", 1)],
    "Pass Option": [("passes", 1), ("touches", 1)],
    "Wide Support": [("crosses", 1)],
    "Dynamic Width": [("crosses", 1)],
    "Limited Width": [("crosses", 1)],          # negative 태그로만 나온다 → 크로스가 적을수록
    "Support Centrally": [("box_touches", 1), ("crosses", -1)],
    "Supports Centrally": [("box_touches", 1), ("crosses", -1)],
    "Stays Back": [("box_touches", -1), ("shots", -1)],
    "Stay in Position": [("box_touches", -1)],
}


def _n(d, *keys):
    for k in keys:
        v = d.get(k)
        if v is not None:
            return float(v)
    return None


def features(row):
    """player_matches 한 행(dict: minutes, 컬럼들, stats_json) → {스탯 키: 값(경기 합계)} · 없는 키는 빠진다."""
    d = json.loads(row["stats_json"] or "{}") if row.get("stats_json") else {}
    col = lambda k: row.get(k) if row.get(k) is not None else d.get(k)  # noqa: E731
    out = {}
    t, i = col("tackles"), col("interceptions")
    if t is not None and i is not None:
        out["tkl_int"] = float(t) + float(i)
    for k, src in (("tackles", ("tackles",)), ("recoveries", ("recoveries",)), ("duels_won", ("duels_won", "duel_won")),
                   ("aerials_won", ("aerials_won",)), ("key_passes", ("key_passes",)), ("xa", ("xa", "expected_assists")),
                   ("xg", ("xg", "expected_goals")), ("shots", ("shots_total", "total_shots")),
                   ("box_touches", ("touches_opp_box",)), ("recv_through", ("recv_through_n",)),
                   ("passes", ("pass_total",)), ("line_breaking", ("line_breaking_passes",)), ("long_att", ("long_att",)),
                   ("crosses", ("crosses_att",)), ("touches", ("touches",))):
        v = col(src[0]) if row.get(src[0]) is not None else _n(d, *src)
        if v is not None:
            out[k] = float(v)
    oh, ow = _n(d, "opp_half_pass_att"), _n(d, "own_half_pass_att")
    if oh is not None and ow is not None and oh + ow > 0:
        out["opp_half_share"] = (oh, oh + ow)   # 비율은 (분자, 분모)로 들고 다닌다
    return out


def per90(rows):
    """여러 경기 행 → {키: 90분당 값(비율 키는 비율)} — 키마다 그 키가 있는 경기 분만 분모로 쓴다."""
    num, mins = {}, {}
    for r in rows:
        m = float(r["minutes"] or 0)
        if m <= 0:
            continue
        for k, v in features(r).items():
            if isinstance(v, tuple):
                a, b = num.get(k, (0.0, 0.0))
                num[k] = (a + v[0], b + v[1])
            else:
                num[k] = num.get(k, 0.0) + v
                mins[k] = mins.get(k, 0.0) + m
    out = {}
    for k, v in num.items():
        if isinstance(v, tuple):
            out[k] = v[0] / v[1] if v[1] else None
        elif mins.get(k):
            out[k] = v / mins[k] * 90
    return {k: v for k, v in out.items() if v is not None}


class Reference:
    """라인군별 백분위 기준 — 경기 처방 슬롯(match_player_prescriptions.pos_label)이 있는 45분+ 경기 기록."""

    def __init__(self, con):
        cur = con.execute("""
            SELECT DISTINCT mp.pos_label, pm.* FROM match_player_prescriptions mp
            JOIN match_reports r ON r.id = mp.report_id
            JOIN player_matches pm ON pm.match_id = r.match_id AND pm.player_id = mp.player_id
            WHERE mp.starter = 1 AND pm.minutes >= ?""", (MIN_MIN,))
        names = [c[0] for c in cur.description]
        self.dist = {}
        for t in cur.fetchall():
            row = dict(zip(names, t))
            pool = POOL.get(GROUP.get(row["pos_label"]))
            if not pool:
                continue
            for k, v in per90([row]).items():
                self.dist.setdefault(pool, {}).setdefault(k, []).append(v)
        for p in self.dist.values():
            for v in p.values():
                v.sort()

    def pct(self, pool, key, value):
        arr = self.dist.get(pool, {}).get(key)
        if not arr or len(arr) < 8:
            return None
        lo, hi = bisect.bisect_left(arr, value), bisect.bisect_right(arr, value)
        return (lo + hi) / 2 / len(arr)


def stat_fit(ref, con, role, focus, slot_type, p90):
    """(점수 0~1 | None, 쓰인 태그 목록) — 역할·포커스의 EA 특성 태그를 그 선수 90분당 스탯 백분위로 채점."""
    pool = POOL.get(slot_type)
    if pool in (None, "GK") or not p90:
        return None, []
    r = con.execute("SELECT plus, negative FROM game_role_focus WHERE role_id=? AND focus=? "
                    "ORDER BY (game_version='FC27') DESC LIMIT 1", (role, focus)).fetchone()
    if not r:
        return None, []
    scores, used = [], []
    for tags, neg in ((json.loads(r[0] or "[]"), False), (json.loads(r[1] or "[]"), True)):
        for tag in tags:
            ps = []
            for key, sign in TRAIT.get(tag, ()):
                if key in p90:
                    p = ref.pct(pool, key, p90[key])
                    if p is not None:
                        ps.append(p if sign > 0 else 1 - p)
            if ps:
                s = sum(ps) / len(ps)
                scores.append(1 - s if neg else s)
                used.append(("−" if neg else "+") + tag)
    return (sum(scores) / len(scores) if scores else None), used


def rank(kernel, ref, con, map25, x, slot_type, stat_rows, top=None):
    """슬롯 역할군 전 조합을 합산 점수로 정렬 → [dict(role, focus, kernel, stats, score, tags)].
    stat_rows = 그 선수의 player_matches 행(dict) 목록(단일 경기면 한 행). 스탯이 없으면 score = 커널."""
    from core.kernel import decode, cos
    v = decode(map25)
    # 표본 규약(core.classify MIN_MINUTES와 같은 45분) — 짧은 교체 출전은 90분 환산이 부풀어 스탯을 쓰지 않는다.
    p90 = per90(stat_rows) if stat_rows and sum(float(r["minutes"] or 0) for r in stat_rows) >= MIN_MIN else {}
    out = []
    for (role, focus), lst in kernel.variants.items():
        if kernel.role_group.get(role) != slot_type:
            continue
        k = cos(v, min(lst, key=lambda t: abs(t[0] - x))[1])
        s, tags = stat_fit(ref, con, role, focus, slot_type, p90)
        out.append(dict(role=role, focus=focus, kernel=k, stats=s, tags=tags,
                        score=k if s is None else W_KERNEL * k + W_STATS * s))
    out.sort(key=lambda d: -d["score"])
    return out[:top] if top else out


def rank_slot(kernel, ref, con, regime_id, pos, map25, stat_rows, top=None):
    """slots 기하(팀 고유 x·slot_type)로 rank() — 경기 처방·시즌 처방 어느 쪽이든 이 함수 하나로 부른다.
    ⭐ 1·2위 격차(Δ)와 2위 후보는 이 결과의 score로 잰다(커널 단독 Δ가 아니다 · docs/30 7단계)."""
    row = con.execute("SELECT x, slot_type FROM slots WHERE regime_id=? AND pos=? LIMIT 1", (regime_id, pos)).fetchone()
    if not row:
        raise KeyError(f"slots에 없음: regime={regime_id} pos={pos}")
    return rank(kernel, ref, con, map25, row[0], row[1], stat_rows, top)
