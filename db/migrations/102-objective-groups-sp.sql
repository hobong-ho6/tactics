-- 102 FC 목표 그룹·SP 보상 정형화 — 2026-10-09 사용자 지시 「fut.gg SP 목표 수집해서 얼티밋팀 페이지에 넣어줘」.
--
-- 왜: fc_objective_tasks(097 이전부터)는 **과제 이름·조건 문장·보상 글자**만 들고 있었다(HTML 태그를 지워 읽음).
--   그래서 ⑴ 그룹 기간(시작·마감)이 없어 「이번 주 것」을 고를 수 없고 ⑵ 그룹 완료 보상(주간 목표 전부 → 750 SP)이 빠졌고
--   ⑶ 「250 SP」가 문자열이라 합계를 못 냈다. 텍스트 파서는 SP 과제를 11개만 잡았다.
-- ⇒ fut.gg 페이지에 박힌 **구조화 상태**(TanStack Start SSR)를 읽어 그룹 행을 따로 두고, 과제에 SP 정수를 붙인다.
-- ⚠️ 기간제다 — pulled 스냅샷으로 쌓는다(불변규칙 2). 화면은 최신 pulled 중 마감 전 그룹만 보인다.
CREATE TABLE fc_objective_groups(
  id             INTEGER PRIMARY KEY,
  game_version   TEXT NOT NULL,
  group_ea_id    INTEGER,
  group_slug     TEXT NOT NULL,            -- '<category>/<eaId-slug>' — fc_objective_tasks.group_slug와 같은 키
  group_name     TEXT,
  group_category TEXT,                     -- seasonal · foundations · milestones · campaigns · live-events · mastery · fc-pro
  description    TEXT,
  start_time     TEXT,                     -- UTC ISO (fut.gg startTime)
  end_time       TEXT,                     -- UTC ISO (fut.gg endTime) — NULL이면 상시
  tasks_count    INTEGER,
  group_sp       INTEGER,                  -- 그룹을 **전부** 끝냈을 때 받는 SP(과제별 SP와 별도)
  group_rewards  TEXT,                     -- 그룹 보상 이름 목록(JSON) — 팩·선수·코인 등 SP 외 보상
  source         TEXT,
  confidence     TEXT,
  pulled         TEXT NOT NULL,
  UNIQUE(game_version, group_slug, pulled)
);
ALTER TABLE fc_objective_tasks ADD COLUMN task_ea_id INTEGER;
ALTER TABLE fc_objective_tasks ADD COLUMN reward_sp INTEGER;   -- 과제 보상 중 SP 합(없으면 NULL)
ALTER TABLE fc_objective_tasks ADD COLUMN modes TEXT;          -- 인정 모드(JSON 배열) — 예 ["squad_battles","rivals"]
