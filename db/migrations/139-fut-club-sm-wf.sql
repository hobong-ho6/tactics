-- 139 보유 카드의 현재 개인기·약발(2026-11-20 사용자 지적 「마조의 약발이 4일텐데」).
--
-- 왜: 화면은 개인기·약발을 **기준 카드**(`player_card_items.skill_moves/weak_foot`)에서 읽었다. 진화가 별을 올려도
--   싱크는 그 표의 **빈 칸만** 채우므로(카드 수집기 값을 덮지 않는 규칙) 진화 후 값이 영영 안 들어왔다.
--   실측: 보유 카드 14장이 어긋났다(마조 3★/3★ → EA 4★/4★ · 파우 토레스 약발 2 → 3 · 맥긴 개인기 2 → 3 …).
--   ⇒ 6대 스탯·29속성·PlayStyle처럼 **보유 카드의 현재값 열**로 둔다. GG Club(`playerDef.skillMoves/weakFoot`)이 EA 실측을 준다.
-- 읽기: export가 COALESCE(현재값, 기준 카드)로 내보낸다 — 화면은 손대지 않는다.
ALTER TABLE fut_club_players ADD COLUMN current_skill_moves INTEGER;
ALTER TABLE fut_club_players ADD COLUMN current_weak_foot INTEGER;
INSERT INTO _migration_log(run_at, v1_path, note) VALUES(date('now','localtime'), '139-fut-club-sm-wf',
  'fut_club_players.current_skill_moves·current_weak_foot 신설 — 진화로 오른 개인기·약발(EA 실측)을 싱크마다 저장 · 기준 카드 값은 그대로');
