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

__all__ = ["ppda", "def_x", "phase_cells", "segment_metrics", "set_pieces", "gk_ids_of", "PHASE_METRICS", "PHASE_GROUPS",
           "receptions", "RECV_METHOD",
           "PPDA_METHOD", "DEF_X_METHOD", "carry_est", "CARRY_EST_METHOD"]

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
#    segment_metrics()가 계산하는 것은 def_x·ppda·own_half_pass_pct와 gk_long_share(gk_ids를 줄 때 · 2026-10-22)다. 나머지는
#    수집 회차가 리포트에서 근거를 들고 넣는 지표. ⭐ gk_long_share는 G37 ⑹이 AVL 리포트(≥2026-10-22) side='v'에 요구한다 —
#    WS JSON이 없으면 SofaScore 선수 스탯(totalLongBalls/totalPass)으로 경기 전체 1행이라도 넣는다(출처·confidence 명기).
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


def _quals(e):
    """이벤트 qualifier displayName 집합 — {'Longball', 'CornerTaken', 'Cross', …}. 축약 전사본은 빈 집합일 수 있다."""
    out = set()
    for q in e.get("qualifiers") or []:
        t = q.get("type") if isinstance(q, dict) else None
        name = t.get("displayName") if isinstance(t, dict) else t
        if name:
            out.add(name)
    return out


def gk_ids_of(match_centre):
    """matchCentreData(home/away.players[].position=='GK') → GK WhoScored playerId 집합. events만 있는 입력이면 빈 집합."""
    ids = set()
    for side in ("home", "away"):
        for p in ((match_centre.get(side) or {}).get("players") or []) if isinstance(match_centre, dict) else []:
            if p.get("position") == "GK" and p.get("playerId") is not None:
                ids.add(p["playerId"])
    return ids


def segment_metrics(events, team_id, opp_id, cuts=(15, 30, 45, 60, 75), gk_ids=None):
    """구간 [a, b)마다 def_x(양 팀)·ppda(양 팀)·own_half_pass_pct(양 팀)·gk_long_share(양 팀 · gk_ids를 줄 때만) 행 목록.
    반환 dict(side 'v'|'o', metric, seg_from, seg_to(None=종료), value, n) — match_phase_metrics 열과 같다.
    표본 0인 칸은 행을 만들지 않는다(0으로 지어내지 않는다).
    gk_long_share = GK 패스 중 Longball qualifier 비율(%) · n=GK 패스 수(2026-10-22 · G37 ⑹ AVL 필수 — gk_ids는 gk_ids_of())."""
    edges = [0, *sorted(set(int(c) for c in cuts if 0 < int(c) < 130)), None]
    gk_ids = set(gk_ids or ())
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
            gp = [e for e in seg if e.get("teamId") == me and _type(e) == "Pass" and e.get("playerId") in gk_ids]
            if gp:
                out.append(dict(side=side, metric="gk_long_share", seg_from=a, seg_to=b,
                                value=round(100 * sum("Longball" in _quals(e) for e in gp) / len(gp), 1), n=len(gp)))
    return out


# ── 세트피스 (2026-10-22 · migration 117 match_set_pieces) ───────────────────────────────────────
# Opta qualifier: 코너 = Pass + CornerTaken · FK = Pass + FreekickTaken(상대 진영 x≥50만 — 자기 진영 FK는 리스타트일 뿐이다)
#   또는 슛 + DirectFreekick · PK = 슛 + Penalty. 타깃 = 킥 뒤 20초 안 같은 팀의 첫 볼 이벤트(키커 제외).
#   결과 = 그 20초 안 같은 팀 슛이 있으면 goal|shot, 없으면 킥 패스의 outcomeType으로 retained|lost(슛 kind는 슛 결과).
SHOT_TYPES = {"Goal", "MissedShots", "SavedShot", "ShotOnPost"}
_SHOT_OUTCOME = {"Goal": "goal", "MissedShots": "miss", "SavedShot": "saved", "ShotOnPost": "post"}
_SP_WINDOW = 20   # 초


def _secs(e):
    return int(_clock(e)) * 60 + int(e.get("second") or 0)


def set_pieces(events):
    """events → [dict(kind, minute, team_id, taker, target, flank, outcome)] — taker/target은 WhoScored playerId.
    flank는 코너만(y≥50=L · y 낮음=오른쪽 규약). qualifier가 없는 축약 전사본이면 빈 목록이다(0으로 지어내지 않는다)."""
    out = []
    for i, e in enumerate(events):
        q, typ = _quals(e), _type(e)
        if typ == "Pass" and "CornerTaken" in q:
            kind = "corner"
        elif typ == "Pass" and "FreekickTaken" in q and (e.get("x") or 0) >= 50:
            kind = "fk"
        elif typ in SHOT_TYPES and "Penalty" in q:
            kind = "pk"
        elif typ in SHOT_TYPES and "DirectFreekick" in q:
            kind = "fk"
        else:
            continue
        row = dict(kind=kind, minute=int(e.get("minute") or 0), team_id=e.get("teamId"),
                   taker=e.get("playerId"), target=None, flank=None, outcome=None)
        if typ in SHOT_TYPES:
            row["outcome"] = _SHOT_OUTCOME[typ]
            out.append(row)
            continue
        if kind == "corner" and e.get("y") is not None:
            row["flank"] = "L" if e["y"] >= 50 else "R"
        t0 = _secs(e)
        for n in events[i + 1:]:
            if _secs(n) - t0 > _SP_WINDOW:
                break
            if n.get("teamId") != e.get("teamId"):
                continue
            if row["target"] is None and n.get("playerId") not in (None, e.get("playerId")) \
                    and _type(n) in POSS_TYPES | {"Aerial"}:
                row["target"] = n["playerId"]
            if _type(n) in SHOT_TYPES:
                row["outcome"] = "goal" if _type(n) == "Goal" else "shot"
                break
        if row["outcome"] is None:
            row["outcome"] = "retained" if _successful(e) else "lost"
        out.append(row)
    return out


# ── 운반(carry) **추정** (2026-10-22 · FC27 구현 검토 §2.2 「운반 — 공급원 없음」) ──────────────────────────
# ⚠️ Opta 공개 이벤트에는 캐리 이벤트가 없다(SofaScore·FotMob 경기 단위도 없다). 바이킹전 D+1 대조표 10행이 손으로 센 추정을
#    core에 올려 같은 정의로 재현되게 한다. **추정이다** — 컬럼 이름(carry_est_*)과 method 문자열에 그렇게 박는다.
CARRY_EST_METHOD = ("추정 — 같은 선수의 연속 볼 이벤트 쌍(시작=직전 팀 동료 성공 패스의 endX/endY(수신) 또는 본인 직전 볼 이벤트 x/y, "
                    "끝=본인 다음 볼 이벤트 x/y · 사이에 다른 선수 볼 이벤트 없음 · 15초 이내 · 세트피스·스로인 제외)의 전진 거리 Δx. "
                    "prog10=Δx≥10(피치 길이 %) · m=Δx×1.05m(105m 피치). 원천=WhoScored matchCentreData(Opta) — core.whoscored.carry_est")
_CARRY_MAX_SEC = 15
_CARRY_SKIP_Q = {"CornerTaken", "FreekickTaken", "ThrowIn", "GoalKick", "KickOff"}


def carry_est(events, player_id):
    """선수 한 명의 운반 추정 → dict(carry_est_n, carry_est_prog10_n, carry_est_prog_m_sum, carry_est_method).
    모든 숫자는 추정이며 0은 「추정 쌍이 없음」이지 「운반이 없음」이 아니다(이벤트 없는 축약본이면 전부 0)."""
    seq = sorted((e for e in events if e.get("x") is not None and e.get("playerId") is not None),
                 key=lambda e: (_clock(e), e.get("second") or 0, e.get("eventId") or 0))
    n = prog = 0
    m_sum = 0.0
    prev = None                                   # 직전 볼 이벤트(누구의 것이든)
    for e in seq:
        typ = _type(e)
        is_ball = typ in POSS_TYPES
        if not is_ball:
            prev = None if typ in DEF_TYPES and e.get("playerId") != player_id else prev
            continue
        if e.get("playerId") == player_id and prev is not None and _CARRY_MAX_SEC >= _secs(e) - _secs(prev) >= 0 \
                and not (_quals(e) & _CARRY_SKIP_Q):
            start = None
            if prev.get("playerId") == player_id and not (_quals(prev) & _CARRY_SKIP_Q):
                start = (prev.get("x"), prev.get("y"))
            elif prev.get("teamId") == e.get("teamId") and _type(prev) == "Pass" and _successful(prev) \
                    and prev.get("endX") is not None:
                start = (prev["endX"], prev.get("endY"))
            if start is not None and start[0] is not None:
                dx = float(e["x"]) - float(start[0])
                n += 1
                if dx >= 10:
                    prog += 1
                if dx > 0:
                    m_sum += dx * 1.05
        prev = e
    return dict(carry_est_n=n, carry_est_prog10_n=prog, carry_est_prog_m_sum=round(m_sum, 1), carry_est_method=CARRY_EST_METHOD)


# ── 수신 귀속(receptions) (2026-10-22 · 경기 데이터 결손 검토 §2 「수신 위치 — JSON엔 있는데 귀속 함수가 없다」) ──────────
# Opta 이벤트는 패스의 끝 좌표(PassEndX/Y = endX/endY)를 패서 행에 둔다. 「누가 어디서 받았나」는 **같은 팀의 다음 볼 이벤트 주체**를
# 수신자로 귀속해 얻는다. 대조표 #13·#19(부엔디아·맥긴 내려와 받기)·#16(알리송 깊은 수신)이 손계산하던 값의 정본.
RECV_METHOD = ("수신 = 같은 팀 성공 패스(endX/endY 있음 · 패서≠본인) 직후 10초 이내 **같은 팀의 다음 볼 이벤트**(POSS_TYPES·Aerial)의 주체가 "
               "본인일 때, 수신 좌표는 그 패스의 endX/endY. deep=endX≥66.7(상대 진영 마지막 3분의 1) · deep80=endX≥80(리포트 손계산 호환) · "
               "prog=endX−패스 시작 x≥10 · through=패스 qualifier Throughball. 원천=WhoScored matchCentreData(Opta) — core.whoscored.receptions")
_RECV_MAX_SEC = 10
_RECV_DEEP_X = 66.7
_RECV_DEEP80_X = 80.0


def receptions(events, player_id):
    """선수 한 명의 수신 귀속 → dict(recv_n, recv_x_mean, recv_deep_n, recv_deep80_n, recv_prog_n, recv_through_n, recv_method).
    0은 「귀속된 수신이 없음」이지 「받은 적 없음」이 아니다(축약본이면 전부 0)."""
    seq = sorted((e for e in events if e.get("playerId") is not None),
                 key=lambda e: (_clock(e), e.get("second") or 0, e.get("eventId") or 0))
    xs, deep, deep80, prog, through = [], 0, 0, 0, 0
    for i, e in enumerate(seq):
        if _type(e) != "Pass" or not _successful(e) or e.get("endX") is None or e.get("playerId") == player_id:
            continue
        t0 = _secs(e)
        for n in seq[i + 1:]:
            if _secs(n) - t0 > _RECV_MAX_SEC:
                break
            if n.get("teamId") != e.get("teamId") or _type(n) not in POSS_TYPES | {"Aerial"}:
                continue
            if n.get("playerId") == player_id:
                ex = float(e["endX"])
                xs.append(ex)
                deep += ex >= _RECV_DEEP_X
                deep80 += ex >= _RECV_DEEP80_X
                prog += (ex - float(e.get("x") or 0)) >= 10
                through += "Throughball" in _quals(e)
            break                                      # 같은 팀의 첫 볼 이벤트가 수신자 — 그 뒤는 보지 않는다
    return dict(recv_n=len(xs), recv_x_mean=round(sum(xs) / len(xs), 1) if xs else None,
                recv_deep_n=deep, recv_deep80_n=deep80, recv_prog_n=prog, recv_through_n=through, recv_method=RECV_METHOD)
