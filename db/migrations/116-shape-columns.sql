-- 116 경기 전용 팀 설정에 「보유 형태 · 비보유 형태」 정형 2칸 (2026-10-22 구현 검토 §2.2 「비보유 형태 정형 없음」).
--
-- 왜: 바이킹전(#62)의 「보유 3-2-5 / 비보유 4-4-2」처럼 게임 포메이션(4-2-3-1 Wide)과 실축 형태가 다른 사실이
--   리포트 산문·match_hypotheses에만 있었다 — 기계가 대조할 수 없고(G37 밖), FC 포메이션 ↔ 실축 형태 괴리(재현 한계 #20)를
--   경기마다 다시 산문으로 적고 있었다. 어휘는 실축 숫자 형태(「3-2-5」「4-4-2」「2-4-4」…)로 고정하고 NULL은 「미기록」이다.
-- 적재: scripts/load_match_extras.py JSON "shapes": {"in": "3-2-5", "out": "4-4-2"} · G37이 AVL 리포트(report_date ≥ 2026-10-14)의 결손을 막는다.
ALTER TABLE match_game_setups ADD COLUMN shape_in_possession TEXT;
ALTER TABLE match_game_setups ADD COLUMN shape_out_possession TEXT;
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-22', '116-shape-columns',
  'match_game_setups.shape_in_possession·shape_out_possession — 보유/비보유 실축 형태 정형(어휘 숫자 형태 · NULL=미기록) · load_match_extras.py "shapes" · G37 AVL 필수');
