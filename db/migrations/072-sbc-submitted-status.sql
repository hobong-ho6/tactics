-- 072 SBC 제출로 소모된 카드를 원장에 남긴다 (2026-09-26 사용자 지시
--    「sbc를 제출해서 내가 완료처리할 수 있도록 하고, 완료처리되면 해당 스쿼드의 선수들은
--      스쿼드에서 없어진 걸로 처리 및 다른 sbc 해법 재계산하도록 수정」)
--
-- 왜 상태값을 새로 만드나:
--   ⑴ SBC 제출은 **되돌릴 수 없고 카드가 구단에서 영구 제거된다**(EA 도움말 · game_system_changes 2026-09-25).
--   ⑵ 그런데 EA·fut.gg는 **어떤 카드를 냈는지 주지 않는다** — 다음 싱크 전까지 우리 원장엔 그대로
--      「보유」로 남아, 다음 SBC 해법이 **이미 낸 카드를 또 쓴다**(2026-09-25에 실제로 그랬다).
--   ⑶ `sold`로 적으면 거짓이 된다. 판 게 아니라 **SBC에 넣은 것**이고, 싱크의 「EA에 없으면 판 것」
--      경로와도 뜻이 갈린다. ⇒ 별도 상태 `sbc`.
--
-- ⛔ 「별도 컬럼 + 쿼리마다 필터」로 하지 않는다 — 거르는 걸 한 군데라도 빠뜨리면 조용히 틀린다.
--    `status`는 이미 모든 보유 쿼리가 보는 **단일 정본**이라 여기에 값을 더하는 게 맞다(불변규칙 13 ①).
-- ⭐ 어느 챌린지가 먹었는지 함께 적는다 — 완료 취소(되돌리기)와 출처 추적에 필요하다.
--
-- ⚠️ SQLite는 CHECK를 ALTER로 못 고친다 ⇒ 테이블 재작성. **id를 보존**하므로 이 테이블을 참조하는
--    fut_evolution_log · fut_club_player_stats · fc_sbc_exclusions의 FK는 그대로 유효하다.

PRAGMA foreign_keys=OFF;

CREATE TABLE fut_club_players_new(
  id INTEGER PRIMARY KEY,
  account_id INTEGER NOT NULL REFERENCES fut_accounts(id),
  player_id INTEGER REFERENCES players(id),   -- 우리 DB 선수면 연결(조인 규칙: player_id)
  ea_item_id INTEGER,                         -- 보유 아이템(카드) id — player_card_items.ea_item_id
  name TEXT NOT NULL,                         -- 표시용
  acquired TEXT, acquired_how TEXT,           -- 입수일·경로(팩/이적시장/보상/SBC)
  -- ⭐ 'sbc' = SBC에 제출해 소모됨(2026-09-26, migration 072). 'sold'(판매)와 구분한다.
  status TEXT NOT NULL DEFAULT 'owned' CHECK(status IN ('owned','sold','discarded','sbc')),
  current_ovr INTEGER, current_six TEXT,      -- 마지막 기록 시점 상태(진화 적용 후 갱신)
  current_playstyles TEXT, current_roles_plus TEXT, current_roles_plus_plus TEXT,
  evo_count INTEGER NOT NULL DEFAULT 0,       -- 적용한 진화 단계 수(로그와 일치해야 한다)
  notes TEXT,
  updated TEXT NOT NULL, chem_style_ea INTEGER, chem_points INTEGER, gg_player_id TEXT, synced_at TEXT, current_attrs TEXT, is_untradeable INTEGER, is_in_active_squad INTEGER, is_captain INTEGER, kit_number INTEGER, number_of_owners INTEGER,
  -- 어느 챌린지에 넣었나(status='sbc'일 때만). 되돌리기와 출처 추적용.
  sbc_challenge_ea_id INTEGER,
  UNIQUE(account_id, ea_item_id)
);

INSERT INTO fut_club_players_new(
  id, account_id, player_id, ea_item_id, name, acquired, acquired_how, status, current_ovr, current_six,
  current_playstyles, current_roles_plus, current_roles_plus_plus, evo_count, notes, updated,
  chem_style_ea, chem_points, gg_player_id, synced_at, current_attrs, is_untradeable,
  is_in_active_squad, is_captain, kit_number, number_of_owners)
SELECT
  id, account_id, player_id, ea_item_id, name, acquired, acquired_how, status, current_ovr, current_six,
  current_playstyles, current_roles_plus, current_roles_plus_plus, evo_count, notes, updated,
  chem_style_ea, chem_points, gg_player_id, synced_at, current_attrs, is_untradeable,
  is_in_active_squad, is_captain, kit_number, number_of_owners
FROM fut_club_players;

DROP TABLE fut_club_players;
ALTER TABLE fut_club_players_new RENAME TO fut_club_players;

PRAGMA foreign_keys=ON;
