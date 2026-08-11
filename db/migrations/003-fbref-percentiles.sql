-- 003 · FBref 리그 전체 백분위 (2026-08-11)
-- 사용자 요청: 선수 페이지 '동료 대비 위치'를 탭으로 — 수집 풀(내부) / 리그 전체(FBref).
-- HANDOFF 외부 소스 백로그(FBref 리그 백분위)의 1차 수집분. 모집단·기간은 FBref 원문 그대로 보존.

CREATE TABLE fbref_percentiles(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  pulled TEXT,                -- 수집일 YYYY-MM-DD
  pos_group TEXT,             -- FBref 비교 포지션군 원문 (예: 'Midfielders')
  period TEXT,                -- 비교 기간·모집단 원문 (예: 'Last 365 days, Big 5 Leagues')
  metric TEXT NOT NULL,       -- FBref 지표명 영문 원문
  metric_kr TEXT,
  per90 TEXT,                 -- 원값 문자열 그대로 (%·소수 혼재하므로 TEXT)
  percentile INTEGER,         -- 0~100
  source TEXT,
  UNIQUE(player_id, metric, period)
);
