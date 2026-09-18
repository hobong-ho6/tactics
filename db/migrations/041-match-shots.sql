-- 041 — match_shots: 슛 단위 xG (2026-09-18, 사용자 지시 「다른 축구 분석 사이트가 어떻게 시각화하는지 수집해서 개선」).
-- 왜: 축구 분석 사이트의 표준 경기 시각화 두 개 — **xG 레이스**(누적 xG 계단선 + 득점 표식)와 **슛 맵**(위치·xG 크기·결과) — 는
--   슛 단위 행이 있어야 그려진다. 지금까지는 팀 합계 xG만 있었다(team_match_stats).
-- 원천: SofaScore `/api/v1/event/{eid}/shotmap`(xg·xgot·좌표·상황·신체부위, 브라우저 fetch) · FotMob matchDetails `content.shotmap.shots`
--   (event_id가 FotMob id인 5경기). ⚠️ **제공사가 다르면 xG를 같은 축에 놓지 않는다** — source에 제공사 명기, 화면은 경기 단위로 한 제공사만 쓴다.
PRAGMA foreign_keys = ON;
BEGIN;
CREATE TABLE match_shots(
  id INTEGER PRIMARY KEY,
  match_id INTEGER NOT NULL REFERENCES matches(id),
  minute INTEGER NOT NULL, added INTEGER,
  side TEXT NOT NULL CHECK(side IN ('v','o')),
  player_id INTEGER REFERENCES players(id), player_name TEXT,
  xg REAL, xgot REAL,
  outcome TEXT,                 -- goal / save / miss / block / post (제공사 어휘를 정규화)
  situation TEXT,               -- regular / corner / set-piece / fast-break / penalty / free-kick (제공사 어휘 그대로)
  body_part TEXT,
  x REAL, y REAL,               -- 제공사 좌표 그대로(SofaScore: 공격 방향 x 0~100, y 0~100 · FotMob: x 0~105, y 0~68) — 화면이 provider별로 변환
  provider TEXT NOT NULL,       -- 'SofaScore' | 'FotMob'
  source TEXT NOT NULL, confidence TEXT
);
CREATE INDEX ix_match_shots_m ON match_shots(match_id, minute);
COMMIT;
