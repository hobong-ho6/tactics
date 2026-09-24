-- 062 빈 문자열 라벨이 선수를 「이름 없음」으로 만들던 구멍 (2026-09-24, 선수 비교 화면 검증 중 발견)
--
-- 증상: 리버풀 WM군 비교에서 한 칸의 선수 이름이 **통째로 비어 있었다**(player_id 114 응구모하).
-- 원인: `squad_entries.label`이 이 한 행만 **빈 문자열('')**이고 나머지는 전부 NULL인데,
--   뷰가 `COALESCE(se.label, p.name_kr, p.name)`이라 **''는 「값이 있다」로 통과**했다.
--   ⇒ 이름 없는 라벨이 화면·랭킹·비교 패널 전부로 새어 나갔다(조인은 player_id라 데이터는 멀쩡했다).
--
-- ⛔ 「빈 문자열을 넣지 말자」는 규율로 막지 않는다 — 읽는 사람이 있어야 작동한다(CLAUDE.md 불변규칙 13).
--   ⇒ **뷰가 ''를 결손으로 읽게** 고친다. 그러면 같은 실수가 다시 들어와도 화면은 이름을 찾아낸다.
-- ⑵ 이미 들어와 있는 그 한 행은 NULL로 정규화한다(나머지 89행과 같은 모양이 된다).

UPDATE squad_entries SET label = NULL WHERE TRIM(COALESCE(label, '')) = '';

DROP VIEW IF EXISTS v_slot_candidates;
CREATE VIEW v_slot_candidates AS
SELECT
  r.id AS regime_id,
  r.team_code,
  sl.formation,
  sl.pos,
  sl.slot_type,
  se.player_id,
  COALESCE(NULLIF(TRIM(se.label), ''), p.name_kr, p.name) AS label,
  p.name AS name_en,
  COALESCE(p.name_kr, p.name) AS name_kr,
  'squad' AS source_kind,
  se.lh AS status,
  se.map25,
  se.rate_v AS rating,
  se.rate_basis,
  se.rate_note,
  se.fit_role,
  se.fit_focus,
  se.fit_sim,
  se.source,
  se.confidence,
  se.sort_order,
  se.grid_club,
  se.grid_caveat
FROM squad_entries se
JOIN regimes r ON r.id=se.regime_id
JOIN players p ON p.id=se.player_id
JOIN slots sl ON sl.regime_id=se.regime_id AND sl.slot_type=se.slot_type
-- pos_only: 좌우 쌍 슬롯(FB=LB/RB, CB=LCB/RCB, DM=LDM/RDM, WM=LM/RM)에서 한쪽만
-- 후보로 쓰고 싶을 때 그 pos를 적는다. NULL이면 종전대로 slot_type의 모든 pos에 노출된다.
WHERE (se.pos_only IS NULL OR se.pos_only = sl.pos)

UNION ALL

SELECT
  r.id AS regime_id,
  r.team_code,
  sl.formation,
  sl.pos,
  sl.slot_type,
  COALESCE(tt.player_id, tp.id) AS player_id,
  CASE WHEN tt.likelihood='CONFIRMED'
       THEN COALESCE(tt.short_label, tt.name_kr, tt.name)
       ELSE '영입·' || COALESCE(tt.short_label, tt.name_kr, tt.name) END AS label,
  tt.name AS name_en,
  COALESCE(tt.name_kr, tp.name_kr, tt.short_label, tt.name) AS name_kr,
  'transfer' AS source_kind,
  tt.likelihood AS status,
  tt.map25,
  tt.avg_rating AS rating,
  'transfer' AS rate_basis,
  '표본 ' || COALESCE(tt.sample_n, 0) || '경기 (' || COALESCE(tt.club, '') || ')' AS rate_note,
  tt.fit_role,
  tt.fit_focus,
  tt.fit_sim,
  tt.source,
  tt.confidence,
  10000 + tt.id AS sort_order,
  tt.club AS grid_club,
  CASE WHEN tt.map25 IS NOT NULL THEN '⚠️ 영입 전 현 소속팀 실측' END AS grid_caveat
FROM transfer_targets tt
JOIN regimes r ON r.team_code=tt.team_code AND r.end IS NULL
JOIN slots sl ON sl.regime_id=r.id AND sl.pos=(
  CASE tt.slot WHEN 'LW' THEN 'LM' WHEN 'RW' THEN 'RM' ELSE tt.slot END
)
LEFT JOIN players tp ON tp.id=tt.player_id OR (tt.player_id IS NULL AND tp.name=tt.name)
WHERE tt.map25 IS NOT NULL
  AND tt.likelihood!='OWNED'
  AND tt.likelihood NOT LIKE 'DEAD%'
  AND NOT EXISTS (
    SELECT 1
    FROM squad_entries se2
    WHERE se2.regime_id=r.id
      AND se2.player_id=COALESCE(tt.player_id, tp.id)
      AND se2.slot_type=sl.slot_type
  );
