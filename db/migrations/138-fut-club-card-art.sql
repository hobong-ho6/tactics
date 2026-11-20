-- 138 보유 카드의 「지금 모습」 재료(2026-11-20 사용자 지시 「내 구단의 카드들 현재 얼티밋팀의 코스메틱 적용한 카드로
--     업데이트해줘 맥긴의 경우는 카드이미지도 없어」).
--
-- 왜: 화면은 기준 카드(`player_card_items.card_image_url`)의 완성 이미지를 쓰고, 진화로 바뀐 OVR·스탯은 픽셀을 지우고
--   다시 쓰는 방식(evocard.js)으로 덧칠했다. ⛔ 코스메틱 진화(카드 디자인 교체 — 예: João Gomes 「Ultimate Scream Retro 20」)는
--   완성 이미지가 어디에도 없어 반영할 길이 없었다.
--   ⭐ fut.gg GG Club 화면은 완성 이미지를 쓰지 않고 **판(레어도 프레임) + 선수 렌더 + 글자**를 합성한다(2026-11-20 실측 —
--   Gomes 카드 = rarities-level-0-large/136 + player-item/27-273463 + 텍스트). 그 재료는 GG Club 보유 목록의
--   `playerDef`(카드별 **현재** 레어도·렌더·로고·글자색)에 다 있다.
--   ⇒ 싱크마다 카드별 재료를 저장하고 화면이 같은 방식으로 합성한다(코스메틱·진화·이미지 결손을 한 번에 해결).
-- 형식: JSON {frame, render, nation, league, club, text, line, rarity_ea, rarity} — URL은 fut.gg CDN 원본 경로.
--   ⚠️ 겉모습 축이다 — 성능 판단에 쓰지 않는다. 매 싱크 현재값으로 덮는다(current_* 열과 같은 성격).
ALTER TABLE fut_club_players ADD COLUMN card_art TEXT;
INSERT INTO _migration_log(run_at, v1_path, note) VALUES(date('now','localtime'), '138-fut-club-card-art',
  'fut_club_players.card_art 신설 — GG Club playerDef의 현재 레어도 판·선수 렌더·로고·글자색(코스메틱 진화 카드 합성용)');
