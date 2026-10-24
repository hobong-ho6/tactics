-- 124 SBC 막힌 칸 (2026-10-24 사용자 지적 「Spooky Nights는 LW/RW/LM/RM은 막힌 자리라 여기엔 카드를 안 넣는 거야」).
--
-- 왜: 인원이 11명 미만인 챌린지(브릭 챌린지 · 「Players: 7」)는 포메이션 중 일부 칸이 **막혀 있다**.
--   계산기는 어느 칸이 막혔는지 몰라 11칸 중 아무 7칸이나 골랐다 — Spooky Nights 해법이 디 마리아를 막힌 RM에 넣었다.
--   EA·fut.gg·FUTWIZ 어디도 막힌 칸을 주지 않아(FUTWIZ는 포메이션·인원만) 인게임 확인값을 기록한다.
-- 읽기: scripts/sbc_solve.py가 막힌 칸을 뺀 포메이션으로만 배치하고 해법 JSON에 blocked로 남긴다.
-- 쓰기: fut_club.py sbc_formation --blocked LM,RM,…(사용자 확인) — 수집기는 만들지 않는다.
ALTER TABLE fc_sbc_formations ADD COLUMN blocked_slots TEXT;   -- JSON ["LM","RM",…] · NULL = 막힌 칸 없음/모름
UPDATE fc_sbc_formations SET blocked_slots='["LM","RM","LW","RW"]',
       source=source || ' ‖ 2026-10-24 막힌 칸 LM·RM·LW·RW — 사용자 인게임 확인',
       updated='2026-10-24'
 WHERE game_version='FC27' AND challenge_ea_id=112;
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-24', '124-sbc-blocked-slots',
  'fc_sbc_formations.blocked_slots — 브릭 챌린지의 막힌 칸 · Spooky Nights(112) 3-4-3 중 LM·RM·LW·RW 막힘(사용자 확인) · sbc_solve.py가 그 칸을 빼고 배치');
