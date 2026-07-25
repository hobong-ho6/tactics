-- 2026-07-24 유스 선수 George Hemmings 스탯 등재 (25/26)
-- 데이터 제약: PL2/UEFA 유스리그는 SofaScore 히트맵·평균위치 미제공(per-match 스탯만).
--   시니어 출전은 짧은 교체 위주(45분 단일 선발 1건)라 포지션-순수 measured 그리드 미생성.
--   → players.notes에 전 대회 요약, player_match_positions에 시니어 4경기만 기록.
BEGIN;

-- players (id 30)
INSERT INTO players(id,name,primary_position,shirt_no,minutes_2526,notes) VALUES
(30,'George Hemmings','DM',53,71,
 '25/26 유스(U21) DM, #53. 2007-03-04생(잉글랜드, 노팅엄 포레스트 유스→2024 빌라). 1군 데뷔 시즌 — 시니어 PL 2경기 25분(A아스널 8''·H에버튼 17'', 둘 다 평점6.6) + 유로파리그 2경기 46분(A페네르바체 1''·H잘츠부르크 45''선발 평점6.5, 실측 좌측 피봇 DM avg 44.5/67.6). 유로파리그 우승 스쿼드 멤버. 유스: PL2 Div1 11경기 전선발·928분·3어시(vs Leicester/Stoke/Man City U21; SofaScore 평점 미제공, FotMob 7.3 참고=QUALITATIVE), UEFA 유스리그 3경기 225분(평점 7.8/7.1/6.7), EFL트로피 1경기 90분 6.4, 프리시즌 AS로마 26''. PL2·유스리그는 SofaScore 히트맵·평균위치 미제공 → 포지션 그리드 미생성. 잉글랜드 U18/U19. Source: SofaScore player 1398204 (2026-07-24).');

-- player_seasons (2025-26 빌라 U21/1군 데뷔; minutes=시니어 대회 합 71)
INSERT INTO player_seasons(player_id,season,club,primary_position,shirt_no,minutes) VALUES
(30,'2025-26','Aston Villa','DM',53,71);

-- player_match_positions — 시니어 4경기만 (PL2/유스리그는 위치 데이터 없음)
INSERT INTO player_match_positions(season,player_id,event_id,date,opponent,venue,competition,minutes,rating,avg_x,avg_y,started,pos_class,source,confidence) VALUES
('2025-26',30,14025254,'2025-12-30','Arsenal','A','Premier League',8,6.6,55.70,59.80,0,NULL,'SofaScore API /event/14025254/average-positions + /player/1398204/statistics (2026-07-24)','HIGH on min/rating/avg coords (API); <45min→pos_class NULL. 1군 데뷔 교체.'),
('2025-26',30,14025064,'2026-01-18','Everton','H','Premier League',17,6.6,60.60,43.00,0,NULL,'SofaScore API /event/14025064/average-positions + /player/1398204/statistics (2026-07-24)','HIGH on min/rating/avg coords (API); <45min→NULL.'),
('2025-26',30,14572701,'2026-01-22','Fenerbahçe','A','Europa League',1,NULL,NULL,NULL,0,NULL,'SofaScore API /event/14572701/player/1398204/statistics (2026-07-24)','HIGH on minutes (API); 1분 출전, 평점/평균위치 없음.'),
('2025-26',30,14572676,'2026-01-29','Red Bull Salzburg','H','Europa League',45,6.5,44.50,67.60,1,'pivot-left','SofaScore API /event/14572676/average-positions + /player/1398204/statistics (2026-07-24)','HIGH on min/rating/avg coords (API); y67.6 L lane, x44.5 pivot → 좌측 피봇 DM. 단일 선발(표본 부족, measured 그리드 미생성).');

COMMIT;
