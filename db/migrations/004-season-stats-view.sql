-- 004 · 시즌 성적 뷰 (2026-08-11)
-- 사용자 요청: Fotmob 선수 페이지처럼 대회별 시즌 성적(경기·선발·골·어시·분·평점)을 선수 페이지에서 비교.
-- 집계는 뷰로 DB에 둔다 (export는 1:1 사상 원칙 유지).
--
-- ⚠️ competition 라벨이 수집 시기별로 혼재한다('PL' vs 'Premier League', 'EL' vs 'UEFA Europa League',
--    NULL 152행). 불변규칙 2(추가만·재작성 금지)를 지켜 **원본 행은 건드리지 않고 뷰에서만 정규화**한다.

DROP VIEW IF EXISTS v_player_season_stats;
CREATE VIEW v_player_season_stats AS
SELECT player_id, season,
       CASE competition
         WHEN 'PL' THEN 'Premier League'
         WHEN 'EL' THEN 'UEFA Europa League'
         WHEN 'CL' THEN 'UEFA Champions League'
         WHEN 'FIFA World Cup' THEN 'World Cup'
         WHEN '' THEN '미분류'
         ELSE COALESCE(competition, '미분류')
       END AS competition,
       COUNT(*)        AS n,
       SUM(started)    AS starts,
       SUM(minutes)    AS minutes,
       SUM(goals)      AS goals,
       SUM(assists)    AS assists,
       ROUND(AVG(rating),2) AS avg_rating,
       COUNT(rating)   AS rating_n
FROM player_matches
GROUP BY player_id, season,
       CASE competition
         WHEN 'PL' THEN 'Premier League'
         WHEN 'EL' THEN 'UEFA Europa League'
         WHEN 'CL' THEN 'UEFA Champions League'
         WHEN 'FIFA World Cup' THEN 'World Cup'
         WHEN '' THEN '미분류'
         ELSE COALESCE(competition, '미분류')
       END;
