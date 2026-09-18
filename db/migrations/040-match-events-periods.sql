-- 040 — match_events · match_period_stats: 경기 타임라인과 하프별 수치의 정형 층 (2026-09-18, 사용자 지시
--       「경기 분석의 이런 데이터도 타임라인에 맞춰 시각적으로 표현」).
--
-- 왜: 득점·교체·카드 분(分)과 전·후반 점유/xG가 지금까지 **산문**(tactical_changes·phase_note)에만 있어 화면이 그릴 수 없었다.
--   타임라인·하프 비교는 정형 행이 있어야 그려진다. 원천은 SofaScore `/event/{id}/incidents`(match-watch §2 스코어 국면 원료와 같다)와
--   FotMob matchDetails 하프별 스탯 — 수집 회차가 채운다(§3에 단계 추가). 기존 경기는 리포트 원문에서 옮긴다(source에 명기).
PRAGMA foreign_keys = ON;
BEGIN;
CREATE TABLE match_events(
  id INTEGER PRIMARY KEY,
  match_id INTEGER NOT NULL REFERENCES matches(id),
  minute INTEGER NOT NULL,             -- 90+3 은 93
  added INTEGER,                       -- 추가시간 표기용(3) — minute은 합산값
  side TEXT NOT NULL CHECK(side IN ('v','o')),   -- v=우리 팀(matches.team_code) · o=상대
  kind TEXT NOT NULL CHECK(kind IN ('goal','own_goal','penalty_goal','penalty_miss','sub','yellow','red','gk_change','var')),
  player_id INTEGER REFERENCES players(id),
  player_name TEXT,                    -- 상대 선수 등 미등록자 표시용
  assist_player_id INTEGER REFERENCES players(id),
  assist_name TEXT,
  player_out_id INTEGER REFERENCES players(id),  -- sub: 나간 선수
  player_out_name TEXT,
  score_v INTEGER, score_o INTEGER,    -- 이 이벤트 직후 스코어(득점류만)
  note TEXT,
  source TEXT NOT NULL, confidence TEXT
);
CREATE INDEX ix_match_events_m ON match_events(match_id, minute);
CREATE TABLE match_period_stats(
  id INTEGER PRIMARY KEY,
  match_id INTEGER NOT NULL REFERENCES matches(id),
  period TEXT NOT NULL CHECK(period IN ('1H','2H','ET')),
  possession_v REAL, xg_v REAL, xg_o REAL, shots_v INTEGER, shots_o INTEGER, sot_v INTEGER, sot_o INTEGER,
  ppda_v REAL, ppda_o REAL,
  source TEXT NOT NULL, confidence TEXT,
  UNIQUE(match_id, period)
);
COMMIT;
