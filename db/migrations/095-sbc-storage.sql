-- 095 SBC 스토리지 카드 원장 (2026-10-02 사용자 지시 「sbc 해법 찾을 때 내 sbc 스토리지 선수도 조회해?」 →
--   「1번 화면 등록으로 만들어줘」).
--
-- 왜: SBC 해법 후보는 클럽 원장(`fut_club_players` · GG Club 캡처)뿐이었다. SBC 스토리지의 중복 카드는
--   **SBC에만 쓸 수 있는 카드**라 가장 덜 아까운 재료인데 후보에 없었다.
--   ⛔ fut.gg는 스토리지를 주지 않는다(2026-10-02 실측 — GG Club API 경로 35개에 storage 없음 ·
--      인증 붙여 storage·sbc-storage 호출 404). ⇒ 사람이 화면에서 등록한다.
-- ⛔ `fut_club_players`에 넣지 않는다 — 원장은 (계정, 카드 id)가 UNIQUE인데 스토리지 카드는 대개 클럽 카드의
--   **중복본**이라 같은 id다. 또 클럽 싱크가 「EA 목록에 있으면 보유」로 상태를 되돌린다. ⇒ 별도 표.
-- 상태: stored(보관 중) · used(SBC에 냄 — used_challenge_ea_id) · removed(사용자가 뺌). 행은 지우지 않는다(불변규칙 2).
CREATE TABLE fut_sbc_storage(
  id           INTEGER PRIMARY KEY,
  account_id   INTEGER NOT NULL REFERENCES fut_accounts(id),
  game_version TEXT NOT NULL,
  ea_item_id   INTEGER NOT NULL,            -- player_card_items.ea_item_id (카드 정보는 거기서)
  name         TEXT NOT NULL,
  status       TEXT NOT NULL DEFAULT 'stored' CHECK(status IN ('stored','used','removed')),
  added_at     TEXT NOT NULL,
  used_challenge_ea_id INTEGER, used_at TEXT,
  source TEXT, notes TEXT
);
CREATE INDEX ix_sbc_storage_status ON fut_sbc_storage(account_id, game_version, status);
