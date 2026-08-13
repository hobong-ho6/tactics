-- 화면의 "현재 스쿼드"와 역사 데이터 보존을 분리한다.
-- squad_entries는 실측 이력으로 남기고, 확정 이탈은 transfer_outgoing을 통해 숨긴다.

INSERT INTO transfer_outgoing(
  team_code,window,player_id,dest_club,likelihood,last_news_date,rationale,source,confidence
)
SELECT
  'AVL','2026-summer',15,'임대 종료 — 26/27 빌라 명단 제외','CONFIRMED','2026-08-11',
  '25/26 빌라 임대 종료. 2026-08-11 Fotmob 26/27 스쿼드 전수 대조에서 명단 제외를 확인했다. '
  || 'squad_entries는 과거 실측 보존을 위해 삭제하지 않고 현재 스쿼드 화면에서만 제외한다.',
  'Fotmob /api/data/teams?id=10252&tab=squad 전수 대조 (2026-08-11); obs#152',
  'HIGH — 외부 현행 명단과 내부 squad_entries 전수 대조. obs#152에 반대 방향 오류로 기록됨.'
WHERE NOT EXISTS (
  SELECT 1 FROM transfer_outgoing
  WHERE team_code='AVL' AND window='2026-summer' AND player_id=15
);

-- 만잠비는 CONFIRMED 합류 후 CAM·DM만 squad_entries로 승격되고 LM/WM 행이 빠져 있었다.
-- 선수 비교를 현재 스쿼드 전용으로 바꿔도 그의 실제 LM 후보 자격이 사라지지 않도록 승격한다.
INSERT INTO squad_entries(
  regime_id,player_id,label,slot_type,lh,map25,rate_v,rate_basis,rate_note,
  fit_role,fit_focus,fit_sim,source,confidence,sort_order,grid_club,grid_caveat
)
SELECT
  1,55,'만잠비(합류확정)','WM','CONFIRMED',map25,avg_rating,'national',
  '스위스 대표팀 12경기 평균 7.2',fit_role,fit_focus,fit_sim,
  'transfer_targets id=122 LM 승격 (현재 스쿼드 정합성 수리)',
  'CONFIRMED 영입은 squad_entries 승격이 규칙. LM 적합은 대표팀 전진 배치 표본.',
  16,'SC Freiburg + 스위스 대표팀',
  '⚠️ 빌라 공식전 0경기 — 대표팀 표본은 포지션 혼입(CAM 선발 2경기뿐)이고 좌우 평균 산물이다(obs#156).'
FROM transfer_targets
WHERE id=122
  AND NOT EXISTS (
    SELECT 1 FROM squad_entries
    WHERE regime_id=1 AND player_id=55 AND slot_type='WM'
  );
