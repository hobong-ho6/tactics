-- 140 보유 카드의 현재 포지션 · 진화 기록의 적용 후 포지션(2026-11-26 사용자 지시 「B안으로 고치기」).
--
-- 왜: EA가 11-25에 낸 훈련 캠프형 진화 Switchback Dynamo(2692)가 처음 보는 보상 `alternative_positions`(값 = EA 포지션 id ·
--   3=RB · 7=LB)를 준다. 스탯은 안 바뀌고 **카드의 보조 포지션이 늘어난다**. 그런데 포지션은 **기준 카드**
--   (`player_card_items.positions`)에서만 읽어서, 진화로 늘어난 포지션을 담을 칸이 없었다 → G29가 막았다.
--   ⇒ 개인기·약발(139)과 같은 꼴로 **보유 카드의 현재값 열**을 둔다. 형식은 기준 카드와 같다(「주 포지션/보조/…」 슬래시 구분).
-- 쓰기: ⑴ 클럽 싱크(GG Club playerDef의 position + alternativePositionIds — EA 실측 · 주 경로. 훈련 캠프형은 시간이 지나면 자동 진행된다)
--       ⑵ `fut_club.py evolve/complete`(카탈로그 보상 → 합집합 · 싱크 전 임시값).
-- 읽기: export가 COALESCE(현재값, 기준 카드)로 내보낸다 — 진화 조건 판정(포지션·Max Pos.)은 그 값을 그대로 쓴다.
ALTER TABLE fut_club_players ADD COLUMN current_positions TEXT;
ALTER TABLE fut_evolution_log ADD COLUMN positions_after TEXT;
INSERT INTO _migration_log(run_at, v1_path, note) VALUES(date('now','localtime'), '140-fut-club-positions',
  'fut_club_players.current_positions · fut_evolution_log.positions_after 신설 — 진화 보상 alternative_positions(포지션 추가)를 저장 · 기준 카드 positions는 그대로');
