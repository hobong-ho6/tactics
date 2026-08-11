"""포지션 사후 분류 — lineup_pos(G/D/M/F)는 포지션-순수 집계에 너무 거칠다 (2026-08-11).
avg_x(공격방향)/avg_y(낮음=오른쪽)와 슬롯 x 정본표로 세분류한다. 좌표 규약: docs/30."""

def pos_class(avg_x, avg_y, lineup_pos):
    """대략적 슬롯 분류. 반환: GK/LB/LCB/RCB/RB/LDM/RDM/LM/CAM/RM/ST 또는 None(판정 불가)."""
    if lineup_pos == 'G':
        return 'GK'
    if avg_x is None or avg_y is None:
        return None
    right = avg_y < 40      # 소파 y 낮음=오른쪽
    left = avg_y > 60
    if lineup_pos == 'D':
        if left:  return 'LB' if avg_x > 35 else 'LCB'
        if right: return 'RB' if avg_x > 35 else 'RCB'
        return 'LCB' if avg_y > 50 else 'RCB'
    if lineup_pos == 'M':
        if avg_x >= 60:     # 전진 미드필더
            return 'LM' if left else ('RM' if right else 'CAM')
        return 'LDM' if avg_y >= 50 else 'RDM'
    if lineup_pos == 'F':
        return 'LM' if left else ('RM' if right else 'ST')
    return None
