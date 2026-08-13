-- 과거 서사 수집 행 중 출처명만 남고 URL이 빠진 검증 가능한 원문 보강.
-- 새 분석은 처음부터 player_duties.source에 원문 URL을 함께 기록한다.

UPDATE player_duties
SET source = source ||
  ' ; [원문 URL 보강] Marc Lamberts 「Introducing GK Sweeping Quality Score」 https://marclamberts.medium.com/introducing-gk-sweeping-quality-score-e0e16881811c' ||
  ' · TheMastermindSite 「Unai Emery – Aston Villa – Tactical Analysis – 2025-26 Edition」 https://themastermindsite.com/2025/12/29/unai-emery-aston-villa-tactical-analysis-2025-26-edition/'
WHERE id=1
  AND instr(source, 'marclamberts.medium.com/introducing-gk-sweeping-quality-score')=0;

UPDATE player_duties
SET source = source ||
  ' ; [원문 URL 보강] TheMastermindSite 「Unai Emery – Aston Villa – Tactical Analysis – 2025-26 Edition」 https://themastermindsite.com/2025/12/29/unai-emery-aston-villa-tactical-analysis-2025-26-edition/'
WHERE id IN (2,6,8,14)
  AND instr(source, 'themastermindsite.com/2025/12/29/unai-emery-aston-villa-tactical-analysis-2025-26-edition')=0;

UPDATE player_duties
SET source = source ||
  ' ; [원문 URL 보강] Total Football Analysis 「Unai Emery Tactics at Aston Villa 2025/2026」 https://totalfootballanalysis.com/data-analysis/unai-emery-tactics-aston-villa-2025-2026-data-analysis'
WHERE id=7
  AND instr(source, 'totalfootballanalysis.com/data-analysis/unai-emery-tactics-aston-villa-2025-2026-data-analysis')=0;
