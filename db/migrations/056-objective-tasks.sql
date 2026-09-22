-- 진화 해금 과제 (2026-09-22 신설 — 사용자 질문 「이거 어떻게 얻는 거야?」에서)
-- fc_evolutions.unlock_text는 **과제 이름만** 들고 있어서 「그래서 뭘 하면 되나」를 매번 fut.gg에서 봐야 했다.
-- ⇒ 목표 그룹 페이지의 과제(이름·조건·보상)를 스냅샷으로 적재하고, 화면이 진화 카드에 같이 띄운다.
-- ⚠️ 기간제다 — 스냅샷이므로 pulled이 정본이고, 지난 회차 행을 덮지 않는다(불변규칙 2).
CREATE TABLE IF NOT EXISTS fc_objective_tasks(
  id INTEGER PRIMARY KEY,
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  group_slug TEXT NOT NULL,          -- /objectives/seasonal/82-ones-we-watched-... 의 경로
  group_name TEXT,                   -- 화면 표기 그룹명
  group_category TEXT,               -- seasonal / campaigns / mastery / foundations / fc-pro …
  task_name TEXT NOT NULL,           -- fc_evolutions.unlock_text와 맞추는 키
  task_text TEXT,                    -- 실제 조건 문장(원문)
  task_text_kr TEXT,                 -- 한국어 번역(불변규칙 11)
  reward TEXT,                       -- 이 과제의 보상 표기(예: Evo Unlock)
  source TEXT, confidence TEXT,
  pulled TEXT NOT NULL,
  UNIQUE(game_version, group_slug, task_name, pulled)
);
CREATE INDEX IF NOT EXISTS ix_obj_task_name ON fc_objective_tasks(task_name);
