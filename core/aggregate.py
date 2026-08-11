"""통합 그리드 집계 — 경기별 그리드 → 선수 대표 그리드.

공식 (카마라 행 역산으로 24/25칸 재현 검증, obs#139):
  경기별 max 정규화 → 균등가중 합 → encode (X=최대, half-up, 9클램프)

규칙 (docs/30):
  · 포지션-순수 — 같은 포지션 경기끼리만 묶는다 (혼합 시 뭉개진 그리드 — 로저스 사례)
  · 히트포인트 15 미만 경기는 제외
  · 표본 2경기 미만이면 집계를 만들지 않는다
  · 표본 확장은 경기 수보다 맥락 다양성(홈/원정·승/패)이 우선 — 균등가중 top-N 확장 금지
  · @dom(2골차+ 승) / @tight(무·패·1골차 승) 분리는 버킷당 2경기 이상일 때
"""
import sqlite3

from . import DB
from .encode import encode

__all__ = ["aggregate_rows", "player_aggregate"]


def aggregate_rows(rows):
    """rows: [(cells_csv, rating, minutes, avg_x, avg_y), …] →
    dict(map25, n, avg_rating, minutes, tool_x, tool_y). 표본 부족이면 None."""
    if len(rows) < 2:
        return None
    acc = [0.0] * 25
    rts, mins, txs, tys = [], 0, [], []
    for cells_s, rating, minutes, ax, ay in rows:
        c = [int(x) for x in cells_s.split(",")]
        m = max(c)
        if m:
            acc = [a + v / m for a, v in zip(acc, c)]
        if rating:
            rts.append(rating)
        mins += minutes or 0
        if ax is not None and ay is not None:
            txs.append(100 - ay)      # 툴x = 100 − 소파y
            tys.append(ax)            # 툴y = 소파x
    return dict(
        map25=encode(acc), n=len(rows),
        avg_rating=round(sum(rts) / len(rts), 2) if rts else None,
        minutes=mins,
        tool_x=round(sum(txs) / len(txs), 2) if txs else None,
        tool_y=round(sum(tys) / len(tys), 2) if tys else None)


def player_aggregate(player_id, where="", params=(), db_path=None, min_hp=15):
    """player_matches에서 조건에 맞는 경기를 골라 집계.
    where 예: "competition='Bundesliga'" / "lineup_pos='M'" """
    con = sqlite3.connect(db_path or DB)
    q = (f"SELECT cells, rating, minutes, avg_x, avg_y FROM player_matches "
         f"WHERE player_id=? AND cells IS NOT NULL AND hit_points>=? ")
    if where:
        q += f"AND ({where}) "
    rows = con.execute(q, (player_id, min_hp, *params)).fetchall()
    con.close()
    return aggregate_rows(rows)
