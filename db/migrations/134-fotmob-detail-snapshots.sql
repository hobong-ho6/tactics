-- 134 FotMob 상세 지표를 수집일별 스냅샷으로 쌓는다(2026-11-18 사용자 지시 「①로 진행해」).
--
-- 왜: UNIQUE(player_id, season, league, metric_key)에 수집일이 없어서, 진행 중 시즌의 값이 **처음 받은 날로 고정**됐다.
--   collect_fotmob_players.py는 ON CONFLICT DO NOTHING이라 이후 수집이 조용히 버려졌다
--   (실증: 알리송 PL 26/27이 10-18 「슈팅 1」에 멈춤 — 11-18 FotMob 실측은 슈팅 7·332분).
-- 어떻게: 키에 pulled를 넣어 날짜별로 **추가만** 한다(불변규칙 2). 읽는 쪽은 v_fotmob_detail_latest
--   (선수·시즌·리그·**지표**마다 가장 늦은 pulled)만 본다 — 시즌을 마친 행은 그대로 하나뿐이라 결과가 같다.
--   ⚠️ 지표 단위로 고른다: 옛 DO NOTHING 시절엔 나중 회차가 **새로 생긴 지표만** 넣었다(알리송 11-09 = 2행) —
--   선수·시즌 단위로 최신일을 고르면 그 2행만 남고 나머지 41개가 사라진다.
PRAGMA foreign_keys=OFF;
CREATE TABLE fotmob_detail_stats_new(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  pulled TEXT NOT NULL,
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
  UNIQUE(player_id, season, league, metric_key, pulled)
);
INSERT INTO fotmob_detail_stats_new
  SELECT id, player_id, pulled, season, league, metric_key, metric, metric_kr,
         stat_value, per90, percentile, percentile_per90, source
    FROM fotmob_detail_stats;
DROP TABLE fotmob_detail_stats;
ALTER TABLE fotmob_detail_stats_new RENAME TO fotmob_detail_stats;
CREATE INDEX ix_fotmob_detail_player ON fotmob_detail_stats(player_id, season, league, pulled);
PRAGMA foreign_keys=ON;

-- 선수·시즌·리그·지표마다 최신 수집일 값만 — 화면·평가는 이것만 읽는다.
CREATE VIEW v_fotmob_detail_latest AS
SELECT f.* FROM fotmob_detail_stats f
 WHERE f.pulled = (SELECT MAX(g.pulled) FROM fotmob_detail_stats g
                    WHERE g.player_id=f.player_id AND g.season IS f.season AND g.league IS f.league
                      AND g.metric_key=f.metric_key);

-- 134b 같은 꼴 두 표도 함께 고친다(같은 날 발견 — 알리송 시즌 요약이 09-13 「4경기 87분」, 특성이 08-11 브라질 리그 값에 멈춰 있었다).
--   fotmob_season_stats UNIQUE(player_id, league, season, metric) → + pulled
--   fotmob_traits       UNIQUE(player_id, metric)                → + pulled
PRAGMA foreign_keys=OFF;
CREATE TABLE fotmob_season_stats_new(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  pulled TEXT NOT NULL,
  league TEXT,                 -- 'Bundesliga 2025/2026'
  season TEXT,
  metric TEXT NOT NULL,        -- 라벨 원문 ('Goals','xG' 등)
  metric_kr TEXT,
  value TEXT,                  -- 원값 문자열 (%·소수 혼재)
  source TEXT,
  UNIQUE(player_id, league, season, metric, pulled)
);
INSERT INTO fotmob_season_stats_new SELECT id, player_id, pulled, league, season, metric, metric_kr, value, source FROM fotmob_season_stats;
DROP TABLE fotmob_season_stats;
ALTER TABLE fotmob_season_stats_new RENAME TO fotmob_season_stats;

CREATE TABLE fotmob_traits_new(
  id INTEGER PRIMARY KEY,
  player_id INTEGER NOT NULL REFERENCES players(id),
  pulled TEXT NOT NULL,        -- 수집일
  pos_group TEXT,              -- 비교 모집단 원문 (예: 'Stats compared to other midfielders')
  metric TEXT NOT NULL,        -- Fotmob key (chances_created 등)
  metric_kr TEXT,
  percentile INTEGER,          -- 0~100 (원값 0~1 × 100)
  source TEXT,
  UNIQUE(player_id, metric, pulled)
);
INSERT INTO fotmob_traits_new SELECT id, player_id, pulled, pos_group, metric, metric_kr, percentile, source FROM fotmob_traits;
DROP TABLE fotmob_traits;
ALTER TABLE fotmob_traits_new RENAME TO fotmob_traits;
PRAGMA foreign_keys=ON;

CREATE VIEW v_fotmob_season_latest AS
SELECT f.* FROM fotmob_season_stats f
 WHERE f.pulled = (SELECT MAX(g.pulled) FROM fotmob_season_stats g
                    WHERE g.player_id=f.player_id AND g.league IS f.league AND g.season IS f.season
                      AND g.metric=f.metric);
CREATE VIEW v_fotmob_traits_latest AS
SELECT t.* FROM fotmob_traits t
 WHERE t.pulled = (SELECT MAX(u.pulled) FROM fotmob_traits u
                    WHERE u.player_id=t.player_id AND u.metric=t.metric);

INSERT INTO _migration_log(run_at, v1_path, note)
VALUES('2026-11-18', '134-fotmob-detail-snapshots',
       'fotmob_detail_stats·fotmob_season_stats·fotmob_traits UNIQUE에 pulled 추가(날짜별 스냅샷) · v_fotmob_detail_latest·v_fotmob_season_latest·v_fotmob_traits_latest 신설 — 진행 중 시즌 값이 첫 수집일에 고정되던 문제');
