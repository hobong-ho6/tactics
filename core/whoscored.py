"""WhoScored(Opta) matchCentreData 이벤트 → 팀·선수 파생 지표 (2026-09-08 신설).

지금까지 PPDA는 브라우저 콘솔 JS로 회차마다 다시 짜서 계산했다(불변규칙 4 위반 — core 밖 재구현).
이 모듈이 정본이다. 입력은 `matchCentreData.events` 리스트(dict) 그대로이며, 좌표 규약은
WhoScored 원본: **x = 그 팀의 공격 방향 0~100, y 낮음 = 오른쪽**(SofaScore와 동일 관례 —
2026-09-01 Cash/Maatsen 좌우로 검증, team_match_stats.ppda_method 주석).

이벤트 종류 (type.displayName):
  수비액션(PPDA 분모·수비 국면 그리드)  Tackle · Interception · Challenge · Foul(범한 것) ·
                                          Clearance · BlockedPass · Aerial · BallRecovery
  보유 국면 그리드                         Pass · TakeOn · BallTouch · Goal · MissedShots ·
                                          SavedShot · ShotOnPost · Dispossessed
  ⚠️ PPDA 분모는 위 8종 중 앞 4종만(기존 정의 유지 — 바꾸면 기존 14행과 비교 불가).
"""
from .encode import cells_from_points, encode

__all__ = ["ppda", "def_x", "phase_cells", "segment_metrics", "PHASE_METRICS", "PHASE_GROUPS", "PPDA_METHOD", "DEF_X_METHOD"]

PPDA_DEN = {"Tackle", "Interception", "Challenge", "Foul"}
DEF_TYPES = PPDA_DEN | {"Clearance", "BlockedPass", "Aerial", "BallRecovery"}
POSS_TYPES = {"Pass", "TakeOn", "BallTouch", "Goal", "MissedShots", "SavedShot",
              "ShotOnPost", "Dispossessed"}

PPDA_METHOD = ("분자=상대가 자기 진영 3/5(x<60)에서 시도한 패스 · 분모=해당 팀 수비액션"
               "(Tackle·Interception·Challenge·Foul) 상대 진영 2/5(x>40). "
               "원천=WhoScored matchCentreData(Opta) — core.whoscored.ppda")
DEF_X_METHOD = ("팀 수비액션 8종(Tackle·Interception·Challenge·Foul·Clearance·BlockedPass·"
                "Aerial·BallRecovery)의 x 평균(자기 공격 방향 0~100). 라인 높이 프록시 — "
                "core.whoscored.def_x")


def _type(e):
    t = e.get("type")
    return t.get("displayName") if isinstance(t, dict) else t


def ppda(events, team_id, opp_id):
    """(ppda, 분자, 분모). 분모 0이면 (None, 분자, 0)."""
    num = sum(1 for e in events if e.get("teamId") == opp_id
              and _type(e) == "Pass" and e.get("x", 100) < 60)
    den = sum(1 for e in events if e.get("teamId") == team_id
              and _type(e) in PPDA_DEN and e.get("x", 0) > 40)
    return (round(num / den, 2) if den else None), num, den


def def_x(events, team_id):
    """(수비액션 x 평균, n). 표본 0이면 (None, 0)."""
    xs = [e["x"] for e in events if e.get("teamId") == team_id
          and _type(e) in DEF_TYPES and e.get("x") is not None]
    return (round(sum(xs) / len(xs), 1) if xs else None), len(xs)


def phase_cells(events, player_id):
    """선수 한 명의 국면별 5×5 카운트 → dict(cells_poss, cells_def, map25_poss, map25_def, n_poss, n_def).
    cells는 CSV 문자열(player_matches.cells와 같은 규약), map25는 core.encode.encode."""
    poss = [e for e in events if e.get("playerId") == player_id and _type(e) in POSS_TYPES]
    dfn = [e for e in events if e.get("playerId") == player_id and _type(e) in DEF_TYPES]
    cp, cd = cells_from_points(poss), cells_from_points(dfn)
    return dict(cells_poss=",".join(map(str, cp)), cells_def=",".join(map(str, cd)),
                map25_poss=encode(cp), map25_def=encode(cd), n_poss=len(poss), n_def=len(dfn))


# ── 구간별 지표 (2026-10-20 · migration 109 match_phase_metrics) ─────────────────────────────
# ⭐ 경기 분석 화면 「경기 흐름」의 지표 목록·라벨·단위 **정본**이다(사용자 지시 「경기 흐름 … 항상 제공」).
#    export가 이 표를 그대로 내보내고, G37이 match_phase_metrics.metric ⊆ 이 키를 지킨다 — 화면에 다시 적지 않는다.
#    segment_metrics()가 계산하는 것은 앞 셋(def_x·ppda·own_half_pass_pct)뿐이다. 나머지는 수집 회차가
#    리포트에서 근거를 들고 넣는 지표(GK 롱패스 비중 등 — 경기마다 대상 선수가 다르다).
PHASE_METRICS = {
    "def_x":             dict(label="수비 액션 높이", unit="", lo_good=False, group="press",
                              help="팀 수비 액션 8종의 평균 x(자기 공격 방향 0~100) — 높을수록 앞에서 막는다. " + DEF_X_METHOD),
    "ppda":              dict(label="PPDA", unit="", lo_good=True, group="press",
                              help="상대 패스 수 ÷ 우리 수비 액션 — 낮을수록 강하게 압박한다. " + PPDA_METHOD),
    "own_half_pass_pct": dict(label="자기 진영 패스 성공률", unit="%", lo_good=False, group="build",
                              help="자기 진영(x<50)에서 시도한 패스의 성공 비율 — 상대 압박에 빌드업이 버티는가."),
    "possession":        dict(label="점유", unit="%", lo_good=False, group="flow", help="구간 점유율."),
    "gk_long_share":     dict(label="GK 롱패스 비중", unit="%", lo_good=False, group="build",
                              help="골키퍼 패스 중 롱패스(≥32m) 비율 — 짧은 빌드업에서 직접 배급으로 넘어갔는가."),
    "own_third_losses":  dict(label="자기 1/3 볼 손실", unit="회", lo_good=True, group="build", help="자기 진영 1/3에서 공을 잃은 횟수."),
    "box_touches_p10":   dict(label="상대 박스 터치 /10분", unit="", lo_good=False, group="threat", help="상대 페널티 박스 안 터치 수(10분당)."),
    "shots_p10":         dict(label="슈팅 /10분", unit="", lo_good=False, group="threat", help="슈팅 수(10분당)."),
    "xg":                dict(label="구간 xG", unit="", lo_good=False, group="threat", help="그 구간에 쌓인 기대득점."),
}


# 「경기 흐름」 묶음 — 화면이 이 순서·제목으로 칸을 묶는다(2026-10-20 사용자 지적 「그래프가 나열돼 잘 안 보임」).
PHASE_GROUPS = [["press", "압박 — 높이·강도"], ["build", "우리 빌드업"], ["threat", "위협 — 박스·슈팅"], ["flow", "점유"]]   # 배열 = 순서 보존(export JSON은 키를 정렬한다)


def _clock(e):
    """경기 시계 분 — 전반 추가시간은 전반 마지막 구간에, 후반은 45분부터(WS minute는 후반에 45로 다시 시작한다)."""
    m = e.get("minute") or 0
    per = e.get("period")
    per = per.get("value") if isinstance(per, dict) else per
    return min(m, 44.99) if per == 1 else max(m, 45)


def _successful(e):
    o = e.get("outcomeType")
    return (o.get("displayName") if isinstance(o, dict) else o) == "Successful"


def segment_metrics(events, team_id, opp_id, cuts=(15, 30, 45, 60, 75)):
    """구간 [a, b)마다 def_x(양 팀)·ppda(양 팀)·own_half_pass_pct(양 팀) 행 목록.
    반환 dict(side 'v'|'o', metric, seg_from, seg_to(None=종료), value, n) — match_phase_metrics 열과 같다.
    표본 0인 칸은 행을 만들지 않는다(0으로 지어내지 않는다)."""
    edges = [0, *sorted(set(int(c) for c in cuts if 0 < int(c) < 130)), None]
    out = []
    for a, b in zip(edges, edges[1:]):
        seg = [e for e in events if _clock(e) >= a and (b is None or _clock(e) < b)]
        for side, me, them in (("v", team_id, opp_id), ("o", opp_id, team_id)):
            dx, n = def_x(seg, me)
            if dx is not None:
                out.append(dict(side=side, metric="def_x", seg_from=a, seg_to=b, value=dx, n=n))
            pp, _num, den = ppda(seg, me, them)
            if pp is not None:
                out.append(dict(side=side, metric="ppda", seg_from=a, seg_to=b, value=pp, n=den))
            ps = [e for e in seg if e.get("teamId") == me and _type(e) == "Pass" and e.get("x", 100) < 50]
            if ps:
                out.append(dict(side=side, metric="own_half_pass_pct", seg_from=a, seg_to=b,
                                value=round(100 * sum(map(_successful, ps)) / len(ps), 1), n=len(ps)))
    return out
