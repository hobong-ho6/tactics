-- 118 인게임 전술(pulled 코드) ↔ 시즌 프리셋(team_tactic_setups.kind) 연결 (2026-10-22 구현 검토 §2.2 「인게임 코드 ↔ 프리셋 연결 없음」 · §2.3 #10).
--
-- 왜: fut_tactics의 pulled 행이 어느 프리셋(optimal · optimal:low-possession …)을 켜 둔 것인지 적는 칸이 없어
--   「LB가 #33 값인데 괴리인지 의도인지」를 판별할 수 없었다(리서치 §1.2 LB 행).
-- 적재: scripts/fut_tactic_setup_kind.py(club_sync.py 전술 단계가 부른다)가 현행 버전·현 시즌 team_tactic_setups와
--   포메이션·3축(빌드업·수비 접근·라인)을 대조해 setup_kind를 채우고, 11칸 역할/포커스를 slot_canon_roles(optimal)와 대조한
--   차이를 setup_diff에 적는다. 3축이 어느 kind와도 안 맞으면 둘 다 NULL + 보고.
ALTER TABLE fut_tactics ADD COLUMN setup_kind TEXT;
ALTER TABLE fut_tactics ADD COLUMN setup_diff TEXT;
INSERT INTO _migration_log (run_at, v1_path, note) VALUES
 ('2026-10-22', '118-fut-tactics-setup-kind',
  'fut_tactics.setup_kind·setup_diff — pulled 코드 ↔ team_tactic_setups.kind 자동 판정(포메이션+3축 일치 · 11칸은 slot_canon 대조 차이를 setup_diff에) · scripts/fut_tactic_setup_kind.py · club_sync 전술 단계');
