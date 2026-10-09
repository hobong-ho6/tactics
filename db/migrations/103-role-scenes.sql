-- 103 역할 장면 해설 — 2026-10-09 사용자 지시 「각 역할을 숫자 히트맵·장면 예시로 다시 설명하고 비교해
--   게임 시스템 쪽에 추가」.
--
-- 왜: game_role_focus.movement_kr은 커널 수치 요약이라 「그 자리에서 무엇을 하나」가 안 읽혔다.
--   히트맵이 같아도 행동이 다른 조합(어드밴스드 Attack = 포처 Support 등)을 장면으로 갈라 보여 준다.
-- ⭐ 내용은 db/seeds/role-scenes-FC26.json이 정본이고 scripts/load_role_scenes.py가 **빈 칸만** 채운다(불변규칙 2).
-- ⚠️ 해석층이다(D) — EA 원문(A)·커널(B)을 읽은 것이고 인게임 통제 실측이 아니다. 근거는 game_role_groups.source·confidence.
ALTER TABLE game_roles ADD COLUMN identity_kr TEXT;        -- 역할 정체성 한 줄
ALTER TABLE game_roles ADD COLUMN focus_axis_kr TEXT;      -- 포커스가 바꾸는 것
ALTER TABLE game_role_focus ADD COLUMN scene_attack_kr TEXT;  -- 군 공통 공격 장면에서의 행동
ALTER TABLE game_role_focus ADD COLUMN scene_defend_kr TEXT;  -- 군 공통 수비 장면에서의 행동
CREATE TABLE game_role_groups(
  game_version  TEXT NOT NULL REFERENCES game_versions(code),
  position_type TEXT NOT NULL,             -- game_roles.position_type
  scene_attack_kr TEXT NOT NULL,           -- 이 군의 모든 역할에 같은 장면을 건다(비교 가능하게)
  scene_defend_kr TEXT NOT NULL,
  compare_kr    TEXT,                      -- 군 안 역할 비교 요약
  source TEXT, confidence TEXT,
  PRIMARY KEY(game_version, position_type)
);
