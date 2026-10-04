"""진화 경로(player_evolutions) 「바뀐 행만 저장」 규약의 정본 (migration 099 · 2026-10-04).

행 = pulled부터 last_seen까지 같은 내용으로 **연속 관측된** 경로. 그날 유효한 경로는 pulled ≤ 날짜 ≤ last_seen.
⛔ 수집기·마이그레이션·export·게이트가 각자 비교식을 다시 쓰지 않는다 — 여기 둘을 import한다(불변규칙 13 ②).
"""

# 내용 비교에서 빼는 칸 — 관측 메타데이터
META = {"id", "pulled", "last_seen", "source", "confidence"}


def content_key(row):
    """행(dict) → 내용 비교 키. 메타데이터 칸을 뺀 나머지 전부."""
    return tuple(sorted((k, row[k]) for k in row if k not in META))


def seen_on(alias="e"):
    """「그날(?) 관측된 행」 SQL 조건 — 바인딩 하나(날짜)를 받는다."""
    return f"? BETWEEN {alias}.pulled AND {alias}.last_seen"
