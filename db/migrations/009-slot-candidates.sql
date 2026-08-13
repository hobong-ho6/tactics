-- 화면 공통 슬롯 후보 풀.
--
-- squad_entries / transfer_targets / prescriptions를 각 페이지가 따로 합치면서
-- CONFIRMED 승격 선수가 이적 행과 스쿼드 행으로 중복되고, duties만 있는 선수는
-- 화면마다 노출 여부가 달라진 문제를 막는다.
--
-- 정본 우선순위: squad_entries > transfer_targets.
-- transfer_targets는 이적 이력으로 보존하되, 같은 player_id가 같은 슬롯 유형의
-- squad_entries에 승격돼 있으면 공통 후보 풀에서는 숨긴다.

CREATE UNIQUE INDEX IF NOT EXISTS uq_squad_entries_regime_player_type
ON squad_entries(regime_id, player_id, slot_type);

DROP VIEW IF EXISTS v_slot_candidates;
CREATE VIEW v_slot_candidates AS
SELECT
  r.id AS regime_id,
  r.team_code,
  sl.formation,
  sl.pos,
  sl.slot_type,
  se.player_id,
  COALESCE(se.label, p.name_kr, p.name) AS label,
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

UNION ALL

SELECT
  r.id AS regime_id,
  r.team_code,
  sl.formation,
  sl.pos,
  sl.slot_type,
  COALESCE(tt.player_id, tp.id) AS player_id,
  CASE WHEN tt.likelihood='CONFIRMED'
       THEN COALESCE(tt.short_label, tt.name_kr, tt.name) || '(합류확정)'
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
