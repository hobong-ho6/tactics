-- 영입 후보에게도 종합/스탯 기반 평가를 담을 수 있게 한다.
--
-- 왜: `player_evaluations.regime_id`가 NOT NULL이라 **우리 스쿼드가 아닌 선수는 평가 행을 만들 수 없었다.**
-- 그런데 불변규칙 7은 원소속 체제의 판단을 우리 체제 행으로 넣는 것을 금지한다 ⇒ 두 규칙이 맞물려
-- 영입 후보는 「평가를 쓸 곳이 없는」 상태였고, player.html의 「종합 평가」·「스탯 기반 평가」 패널이
-- 후보에게는 영구히 비어 있었다.
--
-- `player_duties`는 같은 문제를 **regime_id NULL 허용**으로 이미 풀어 뒀다(그 행은 transfer_targets에
-- 걸려 있으면 export가 함께 싣는다). 평가 테이블도 같은 규약으로 맞춘다 — 새 개념을 만들지 않는다.
--
-- ⚠️ UNIQUE(regime_id, player_id)는 그대로 둔다. SQLite에서 NULL은 UNIQUE 비교에서 서로 같지 않으므로
--    regime_id IS NULL 행은 선수당 여러 개가 들어갈 수 있다 — 후보 평가는 1인 1행 규약을 사람이 지킨다.
PRAGMA foreign_keys = OFF;
BEGIN;

CREATE TABLE player_evaluations_new(
  id INTEGER PRIMARY KEY,
  regime_id INTEGER REFERENCES regimes(id),   -- NULL = 아직 우리 선수가 아니다(영입 후보). 불변규칙 7.
  player_id INTEGER NOT NULL REFERENCES players(id),
  overall TEXT NOT NULL,
  traits TEXT,
  strengths TEXT,
  stat_eval TEXT,
  fit_emery TEXT,
  fit_alonso TEXT,
  fit_iraola TEXT,
  source TEXT,
  confidence TEXT,
  updated TEXT, fotmob_eval TEXT,
  UNIQUE(regime_id, player_id)
);

INSERT INTO player_evaluations_new
  SELECT id, regime_id, player_id, overall, traits, strengths, stat_eval,
         fit_emery, fit_alonso, fit_iraola, source, confidence, updated, fotmob_eval
  FROM player_evaluations;

DROP TABLE player_evaluations;
ALTER TABLE player_evaluations_new RENAME TO player_evaluations;

COMMIT;
PRAGMA foreign_keys = ON;
