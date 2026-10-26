-- 125 진화의 토큰 종류 (2026-10-26 사용자 지적 「The Haunted Wall … 지금 FC27 진화에는 안 나와」 · 「Wicked Winger는 얼티밋 스크림 토큰으로 구매하는 거 아니야?」).
--
-- 왜: fut.gg 진화 객체는 토큰 스토어형을 `tokenCost` + `eventTokenId`로 준다. 수집기는 tokenCost만 받고 eventTokenId를 버렸고,
--   화면(evorules.js acquireRoute)은 tokenCost를 아예 보지 않아 Haunted Wall(500)·Wicked Winger(900)가 「진화 랩에서 바로 시작 (무료)」로 떴다.
--   같은 사고 두 번째(첫 번째 = Composed Stopper · migration 122 손 보충) ⇒ 불변규칙 13 — 보충 행이 아니라 fut.gg 필드를 받는다.
-- eventTokenId 정본: fut.gg /token-store/ 서버 상태(2026-10-26 열람) 1=Gallery Token · 2=Champions Token · 3=Ultimate Scream Token.
-- 관측(2026-10-26 fut.gg paths API): 2606 Composed Stopper 125·2 · 2622 The Haunted Wall 500·3 · 2623 Wicked Winger 900·3.
--   ⇒ 2606은 migration 122의 정황 판정(C · 챔피언스 토큰)이 fut.gg 필드로 맞았다.
-- 쓰기: scripts/collect_futgg_evolutions.py catalog_row(event_token_id=eventTokenId). 아래 UPDATE는 비어 있던 새 칸을 오늘 관측값으로 채운다(기존 값 덮어쓰기 아님).
ALTER TABLE fc_evolutions ADD COLUMN event_token_id INTEGER;   -- fut.gg eventTokenId · NULL = 토큰형 아님/미수집
UPDATE fc_evolutions SET event_token_id=2 WHERE game_version='FC27' AND evo_id=2606 AND token_cost>0;
UPDATE fc_evolutions SET event_token_id=3 WHERE game_version='FC27' AND evo_id IN (2622, 2623) AND token_cost>0;
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-26', '125-evo-event-token',
  'fc_evolutions.event_token_id — fut.gg eventTokenId(1 갤러리·2 챔피언스·3 얼티밋 스크림) · 2606=2 · 2622·2623=3 · 화면 획득 조건이 token_cost+토큰 종류로 판정(종전 「무료」 오표기)');
