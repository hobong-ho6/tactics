-- 005 · Fotmob 리그 백분위·시즌 스탯 (2026-08-11)
-- 사용자 요청: "풋몹에서 제공하는것처럼 선수의 스탯과 성적을 가져와서 비교" + 경기 스탯 탭의 '리그 전체' 모집단.
--
-- ⚠️ FBref 대체다. FBref는 스카우팅 리포트 백분위 표를 더 이상 무료 노출하지 않는다
--    (2026-08-11 확인: 브라우저로 /scout/365_m1/ 접근 시 표 0개, 'Percentile' 문자열 부재).
--    003의 fbref_percentiles 테이블은 스키마만 남기고 미사용 — 재개 시 그대로 쓸 수 있다.
--
-- Fotmob traits = **같은 포지션군 리그 선수 대비 백분위**(0~1). 모집단 라벨은 title 원문 보존.

ALTER TABLE players ADD COLUMN fotmob_id INTEGER;

CREATE TABLE fotmob_traits(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  pulled TEXT,                 -- 수집일
  pos_group TEXT,              -- 비교 모집단 원문 (예: 'Stats compared to other midfielders')
  metric TEXT NOT NULL,        -- Fotmob key (chances_created 등)
  metric_kr TEXT,
  percentile INTEGER,          -- 0~100 (원값 0~1 × 100)
  source TEXT,
  UNIQUE(player_id, metric)
);

-- Fotmob 주 리그 시즌 스탯 (per-90 및 합계 — 카테고리·라벨 원문 보존)
CREATE TABLE fotmob_season_stats(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  pulled TEXT,
  league TEXT,                 -- 'Bundesliga 2025/2026'
  season TEXT,
  metric TEXT NOT NULL,        -- 라벨 원문 ('Goals','xG' 등)
  metric_kr TEXT,
  value TEXT,                  -- 원값 문자열 (%·소수 혼재)
  source TEXT,
  UNIQUE(player_id, league, season, metric)
);
