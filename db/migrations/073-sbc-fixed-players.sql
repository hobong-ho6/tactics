-- 073 SBC가 **고정해 주는 선수** (2026-09-26 사용자 지시 「Madrid Dreams RW이 얀디오망데로 고정값임」)
--
-- 무엇인가: 일부 챌린지는 특정 칸에 **SBC가 카드를 미리 박아** 둔다(바꿀 수 없다).
--   Madrid Dreams 설명이 그걸 말한다 — 「Celebrate Yan Diomandé's transfer to Real Madrid with this challenge!」
--   (이 챌린지로 얀 디오망데의 레알 마드리드 이적을 축하하세요!).
--
-- ⛔⛔ **내 보유 카드가 아니다.** SBC가 주는 카드라 `fut_club_players`에 없다 ⇒ 별도 표에 카드 사실을 적는다.
--   그 카드는 조건 판정에 **그대로 들어간다**(클럽·리그·국적·등급·케미·인원). 빼고 풀면 답이 틀린다.
--   실측: Madrid Dreams는 「Max. Clubs in Squad: 4」·「Min. 3 Players from the same Club」이 걸려 있어
--   레알 마드리드 1장이 미리 박혀 있느냐가 해답을 통째로 바꾼다.
--
-- ⛔ EA·fut.gg는 이 값을 주지 않는다 — **사용자가 화면에서 읽어 알려 준 것**이 유일한 출처다
--    (포메이션 기록 `fc_sbc_formations`(069) · 완료 기록 `fut_sbc_log`(068)과 같은 축).
-- ⚠️ 카드 사실(클럽·리그·국적·포지션·OVR)은 fut.gg에서 받아 채운다 — 이름만 적고 추측하지 않는다.
CREATE TABLE IF NOT EXISTS fc_sbc_fixed(
  game_version    TEXT NOT NULL REFERENCES game_versions(code),
  challenge_ea_id INTEGER NOT NULL,
  slot            TEXT NOT NULL,          -- 그 칸의 표시 이름(RW·LCB…). fc_formations.slots[].label과 같은 표기
  ea_item_id      INTEGER,                -- 확정되면 적는다. 모르면 NULL(아래 카드 사실로 판정한다)
  name            TEXT NOT NULL,
  ovr             INTEGER, club TEXT, league TEXT, nation TEXT, positions TEXT,
  is_special      INTEGER NOT NULL DEFAULT 0,
  source TEXT, confidence TEXT, updated TEXT,
  PRIMARY KEY(game_version, challenge_ea_id, slot)
);

INSERT INTO fc_sbc_fixed(game_version, challenge_ea_id, slot, ea_item_id, name, ovr, club, league, nation,
                         positions, is_special, source, confidence, updated)
VALUES('FC27', 32, 'RW', NULL, 'Yan Diomande', 84, 'Real Madrid', 'LALIGA EA SPORTS', 'Ivory Coast',
       'RW/RM/LM/LW', 0,
       '고정 사실: 사용자 보고(2026-09-26, 인게임 화면) — EA·fut.gg가 주지 않는 축이다. '
       || '카드 사실: fut.gg /api/fut/players/v2/27/?name=diomande (2026-09-26 조회)',
       'MEASURED(사용자 확인) — 어느 칸에 고정인지는 사용자가 읽은 값. '
       || '⚠️ fut.gg에 같은 선수 카드가 둘이다(Rare 84 eaId 78012 · Ones to Watch 84 eaId 50409660). '
       || '클럽·리그·국적·포지션·OVR이 **동일**해 판정 결과가 갈리지 않으므로 ea_item_id를 비워 둔다 — '
       || '⛔ 둘 중 하나로 찍어 적으면 확인하지 않은 사실이 된다.',
       '2026-09-26');
