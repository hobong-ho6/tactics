-- 006 · Fotmob 상세 시즌 스탯 (2026-08-11)
-- 사용자 요청: "풋몹 API가 열렸으면 등록된 선수들의 전체 시즌 스탯을 가져오고 스탯 기반으로 종합평가 보충".
--
-- 출처: /api/data/playerStats?playerId={fotmob_id}&seasonId={entryId}
--   · entryId는 /api/data/playerData 의 statSeasons[].tournaments[].entryId
--   · statsSection.items[].items[] 각 항목이 statValue·per90·percentileRank·percentileRankPer90을 준다.
-- ⭐ 005의 fotmob_traits(6축)보다 훨씬 촘촘하다 — 선수당 40여 지표에 각각 리그 동포지션 백분위가 붙는다.
--    traits는 페이지 요약용으로 남기고, 상세 비교·평가 근거는 이 표를 쓴다.

CREATE TABLE fotmob_detail_stats(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  pulled TEXT,
  season TEXT,                 -- '2025/2026'
  league TEXT,                 -- 'Premier League'
  metric_key TEXT NOT NULL,    -- Fotmob localizedTitleId (안정 키)
  metric TEXT,                 -- 영문 표시명 원문
  metric_kr TEXT,
  stat_value TEXT,             -- 합계 원값 (문자열 — %·분수 혼재)
  per90 REAL,
  percentile INTEGER,          -- 같은 리그 동포지션 대비 백분위(합계 기준)
  percentile_per90 INTEGER,    -- 90분당 기준 백분위
  source TEXT,
  UNIQUE(player_id, season, league, metric_key)
);

-- 006b (2026-08-11) · 사용자 요청: "Fotmob 스탯 기준으로도 선수를 평가 — 비교 기준 영역 하단에".
-- stat_eval(우리 실측 중심)과 분리한다: fotmob_eval은 **리그 동포지션 백분위만으로** 내리는 평가다.
ALTER TABLE player_evaluations ADD COLUMN fotmob_eval TEXT;
