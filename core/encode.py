"""5×5 그리드 인코딩 — docs/30 ③ 정본 규약.

히트맵 포인트 → 셀 카운트: row = 4 − ⌊소파x/20⌋ · col = ⌊(100 − 소파y)/20⌋
(툴 좌표: 행0 = 공격 방향, 열0 = 좌측 터치라인)

map25 = 'X'(최댓값 셀) / round(v/max*10) half-up / **최대 아닌 셀은 9로 클램프**.
클램프 근거(obs#139): v/max*10 ≥ 9.5인 비최대 셀이 round로 10이 되면 두 글자가
박혀 25자가 깨진다 — 정수 카운트에서는 드물지만 실수 집계에서는 흔하다.

⚠️ 반올림은 half-up이다(JS Math.round 의미론). 파이썬 내장 round()는 banker's라
쓰면 안 된다 — v1에 두 세대가 섞인 원인(마이그레이션에서 112행 정규화, 2026-08-11).
"""
import math

__all__ = ["encode", "cells_from_points", "regression_check"]


def encode(cells):
    """카운트/실수 리스트(25) → map25 문자열. 전부 0이면 None."""
    m = max(cells)
    if m == 0:
        return None
    return "".join(
        "X" if v == m else str(min(9, math.floor(v / m * 10 + 0.5))) for v in cells)


def cells_from_points(points):
    """SofaScore heatmap [{x,y},…] → 25칸 카운트 (툴 방향)."""
    c = [0] * 25
    for p in points:
        row = max(0, min(4, 4 - int(p["x"] // 20)))
        col = max(0, min(4, int((100 - p["y"]) // 20)))
        c[row * 5 + col] += 1
    return c


def regression_check(conn):
    """DB의 전 그리드에 대해 cells→map25 재인코딩 대조. (불일치 행 리스트, 총수) 반환.
    모든 DB 쓰기 스크립트가 시작 시 이걸 돌린다 — 인코더 회귀를 데이터가 잡는다."""
    bad = []
    total = 0
    for pid, eid, cells_s, m25 in conn.execute(
            "SELECT player_id, event_id, cells, map25 FROM player_matches "
            "WHERE cells IS NOT NULL AND map25 IS NOT NULL"):
        total += 1
        if encode([int(x) for x in cells_s.split(",")]) != m25:
            bad.append((pid, eid))
    return bad, total
