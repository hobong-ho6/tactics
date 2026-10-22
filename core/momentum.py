"""경기 모멘텀(분 단위 −100~100) 집계 — 단일 정본 (2026-10-22 신설 · migration 120 `match_momentum`).

원천은 SofaScore `/api/v1/event/<eid>/graph`(graphPoints minute·value · +=홈 우세). `match_momentum.value`는
**우리 팀 기준**(+ = 우리 우세)으로 저장한다 — 홈/원정에 따라 부호를 뒤집어 넣는다(`sign_for_side`).
경기 흐름 3묶음(`match_tactical_changes`·경기 분석 화면)의 경계를 수치로 제안하는 데 쓴다 — 제안일 뿐 판정이 아니다.
"""
from __future__ import annotations


def sign_for_side(side: str) -> int:
    """우리 팀이 home이면 +1, away면 −1 — graph는 홈 우세가 양수."""
    return 1 if side == "home" else -1


def runs(points: list[tuple[int, int]], min_len: int = 5) -> list[dict]:
    """같은 부호가 min_len분 이상 이어지는 구간. [{'start','end','sign','mean'}] (0은 직전 부호를 잇는다)."""
    out, cur = [], None
    for minute, v in sorted(points):
        s = (v > 0) - (v < 0)
        if s == 0 and cur:
            s = cur["sign"]
        if cur and s == cur["sign"]:
            cur["end"] = minute
            cur["vals"].append(v)
        else:
            if cur:
                out.append(cur)
            cur = {"start": minute, "end": minute, "sign": s, "vals": [v]}
    if cur:
        out.append(cur)
    res = []
    for r in out:
        if r["end"] - r["start"] + 1 >= min_len:
            res.append({"start": r["start"], "end": r["end"], "sign": r["sign"],
                        "mean": round(sum(r["vals"]) / len(r["vals"]), 1)})
    return res


def propose_boundaries(points: list[tuple[int, int]], k: int = 2, min_len: int = 5) -> list[int]:
    """흐름 3묶음(경계 k=2) 제안 — 긴 같은 부호 구간의 **시작 분** 중 평균 절대값이 큰 순으로 k개(45분 하프 경계 제외)."""
    rs = [r for r in runs(points, min_len) if r["start"] > 0]
    rs.sort(key=lambda r: -abs(r["mean"]) * (r["end"] - r["start"] + 1))
    picks = []
    for r in rs:
        if all(abs(r["start"] - b) >= min_len for b in picks):
            picks.append(r["start"])
        if len(picks) >= k:
            break
    return sorted(picks)
