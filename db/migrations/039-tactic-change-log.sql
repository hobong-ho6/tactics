-- 039 — tactic_change_log: 시즌 전술 「설정 층」 변경 이력 (2026-09-18, 사용자 지시
--       「업데이트 된다면 갱신일과 왜 변화되었는지 히스토리를 기록해서 보여주고 현재 리포트의 전술 업데이트 일도 보여줘」).
--
-- 무엇을 기록하나: core/tactic_state.py가 펴는 세 층(slot_canon · team_setup · starter)의 키별 before→after.
--   manager_profiles(서사 11축)는 덧붙임 문단의 `[YYYY-MM-DD …]` 표식이 자체 히스토리라 여기 넣지 않는다 — 화면이 그 표식을 파싱한다.
-- 누가 쓰나: scripts/tactic_changes.py — ⑴ `--backfill`은 git 이력(db/dump/*.sql)에서 커밋 단위로 복원(사유 = 커밋 제목),
--   ⑵ 평시에는 DB 현재 상태 ↔ 로그의 마지막 상태를 대조해 새 변경을 `--reason`과 함께 추가한다.
-- ⛔ G19가 「로그에 없는 설정 변경」을 막는다 — 설정 층을 바꿨으면 같은 회차에 사유를 남겨야 export가 통과한다.
PRAGMA foreign_keys = ON;
BEGIN;
CREATE TABLE tactic_change_log(
  id INTEGER PRIMARY KEY,
  regime_id INTEGER NOT NULL REFERENCES regimes(id),
  layer TEXT NOT NULL CHECK(layer IN ('slot_canon','team_setup','starter')),
  key TEXT NOT NULL,                 -- slot_canon: 'formation|pos' · team_setup: 'season|kind' · starter: 'pos_label'
  before TEXT,                       -- NULL = 신설
  after TEXT,                        -- NULL = 삭제
  changed_at TEXT NOT NULL,          -- 날짜(YYYY-MM-DD)
  reason TEXT NOT NULL,              -- 왜 바뀌었나 — obs# 참조 권장
  source TEXT NOT NULL               -- 'git:<hash>' (backfill) 또는 'tactic_changes.py <날짜>'
);
CREATE INDEX ix_tactic_change_log_r ON tactic_change_log(regime_id, changed_at);
COMMIT;
