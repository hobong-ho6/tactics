-- 029 — 인게임 캡처 읽기 규칙 2종을 뷰로 고정 (2026-09-08, 사용자 지시).
-- ⑴ v_ingame_capture_norm: 캡처별 자기진영 비중(행3~4)과 **그 경기 팀 평균 대비 편차**. 경기 간 기준선이 44.9→40.8→27.7%로
--    흔들려(점유율로 설명 안 됨) 절대값 대신 편차로 읽는다. 조작 오염·GK는 팀 평균 계산에서 제외.
-- ⑵ v_kernel_fidelity: 역할×포커스별 게임↔커널 코사인 집계(조작 오염 제외). 「EA 커널이 게임 배치를 예측한다」는 처방의 핵심 가정을
--    역할군별로 보정하는 표 — FB·WM(.21~.43)은 낮고 DM dlp·CB(.55~.76)는 높다(테스트 1~3, 42장).
PRAGMA foreign_keys = ON;
BEGIN;
CREATE VIEW v_ingame_capture_norm AS
WITH c AS (
  SELECT id, tactic_code, player_id, game_version, ref_kind, cosine, note, cells,
         (note LIKE '%조작 오염%') AS controlled,
         -- 자기진영 = 25칸 중 16~25번째(행3·행4) 가중치 합 / 전체
         (SELECT SUM(CAST(value AS REAL)) FROM (
            SELECT value, row_number() OVER () rn FROM json_each('[' || cells || ']')) WHERE rn > 15)
         / (SELECT SUM(CAST(value AS REAL)) FROM json_each('[' || cells || ']')) * 100.0 AS own_pct
  FROM ingame_captures),
m AS (
  SELECT tactic_code, AVG(own_pct) AS team_mean_own, COUNT(*) AS n_players
  FROM c WHERE controlled = 0 AND ref_kind NOT LIKE 'kernel:gk_%' GROUP BY tactic_code)
SELECT c.id, c.tactic_code, c.player_id, c.game_version, c.ref_kind, c.cosine, c.controlled,
       ROUND(c.own_pct, 1) AS own_pct, ROUND(m.team_mean_own, 1) AS team_mean_own,
       ROUND(c.own_pct - m.team_mean_own, 1) AS own_delta, m.n_players
FROM c JOIN m ON m.tactic_code = c.tactic_code;

CREATE VIEW v_kernel_fidelity AS
SELECT game_version,
       substr(ref_kind, 8, instr(ref_kind, '/') - 8)                          AS role_id,
       substr(ref_kind, instr(ref_kind, '/') + 1,
              instr(ref_kind, '@') - instr(ref_kind, '/') - 1)                AS focus,
       COUNT(*) AS n, COUNT(DISTINCT tactic_code) AS n_matches, COUNT(DISTINCT player_id) AS n_players,
       ROUND(AVG(cosine), 2) AS cos_avg, ROUND(MIN(cosine), 2) AS cos_min, ROUND(MAX(cosine), 2) AS cos_max,
       CASE WHEN COUNT(*) >= 3 AND AVG(cosine) >= 0.6 THEN 'HIGH'
            WHEN COUNT(*) >= 3 AND AVG(cosine) >= 0.45 THEN 'MID'
            WHEN COUNT(*) >= 3 THEN 'LOW'
            ELSE 'n<3' END AS fidelity
FROM ingame_captures
WHERE ref_kind LIKE 'kernel:%' AND note NOT LIKE '%조작 오염%'
GROUP BY game_version, role_id, focus;

INSERT INTO _migration_log(run_at, v1_path, note) VALUES
 (date('now'), '029-ingame-fidelity-views',
  'v_ingame_capture_norm(자기진영 편차 = 개인 − 그 경기 비조작·비GK 팀 평균) · v_kernel_fidelity(역할×포커스 게임↔커널 cos 집계, 조작 제외, n≥3에서 HIGH≥.6/MID≥.45/LOW). 사용자 지시 2026-09-08 「뷰랑 편차 규칙」.');
COMMIT;
