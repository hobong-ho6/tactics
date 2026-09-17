-- 035 — fc_role_familiarity_map: Role+/++ raw id → 역할 이름 해석표 (2026-09-17).
-- 왜: `player_card_items.roles_plus(_plus)`와 `player_evolutions.roles_*_after`는 **raw id 배열**이다.
--     fut.gg `/api/fut/roles/`의 각 역할이 `plusEaId`·`plusPlusEaId`를 들고 있어 이 id로 해석된다.
-- ⛔ **이 표는 커널이 아니다.** FC27 커널(`game_roles`·`game_role_focus`)은 역할 목록 변화가 확정되기 전까지
--    만들지 않는다(obs#629). 여기 있는 것은 **숙련도 id ↔ 이름** 대응뿐이고 좌표·kernel25를 담지 않는다.
PRAGMA foreign_keys = ON;
BEGIN;
CREATE TABLE fc_role_familiarity_map(
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  ea_id INTEGER NOT NULL,           -- plusEaId 또는 plusPlusEaId
  kind TEXT NOT NULL CHECK(kind IN ('plus','plusplus')),
  slug TEXT NOT NULL,               -- 'cm-box-to-box'
  name TEXT NOT NULL,               -- 'Box-To-Box'
  position_name TEXT,               -- 'CM'
  source TEXT, confidence TEXT, pulled TEXT NOT NULL,
  PRIMARY KEY(game_version, ea_id, kind)
);
COMMIT;
