-- 2026-07-22 임대 복귀 1군 자원 스탯 등재 (25/26 임대처 실측)
-- 대상: Kosta Nedeljković(RB Leipzig), Samuel Iling-Junior(WBA→Pisa), Joe Gauci(Port Vale)
-- 방식: SofaScore API 풀 파이프라인. 좌표 규약/포지션-순수/그리드 orientation(row0=공격,col0=좌) 준수.
BEGIN;

-- 1) players (id 27~29)
INSERT INTO players(id,name,primary_position,shirt_no,minutes_2526,notes) VALUES
(27,'Kosta Nedeljkovic','RB',20,NULL,
 '26/27 RB 뎁스 복귀. 25/26 RB 라이프치히 임대: 분데스 5경기(3선발)·252분·평점6.3 + DFB포칼 1경기(45분·평점7.0), 0G/0A. 12월 집중 출전 후 이탈. 실측 우측 딥RB. Source: SofaScore player 1152923 (2026-07-22).'),
(28,'Samuel Iling-Junior','LM',19,NULL,
 '26/27 LM 복귀(#19). 25/26 이중 임대 — 웨스트브롬(챔피언십 9월~1월) 24경기·14선발·1290분·평점6.53·1골이 본체, 이후 피사(세리에A 2~3월) 5경기 교체·107분. WBA 등록상 LM이나 실측 주력은 우측(RM/AMR) 12선발, 좌측(LW/AML)은 후반 4선발. Source: SofaScore player 996919 (2026-07-22).'),
(29,'Joe Gauci','GK',18,NULL,
 '26/27 백업 GK 복귀. 25/26 포트 베일(리그원) 주전: 34경기 전선발·3060분·평점6.94·클린시트11·세이브89·실점40·세이브율62% + EFL컵 2경기(1CS). GK라 히트맵/평균위치 미수집(시즌 요약만). Source: SofaScore player 966874 season stats (2026-07-22).');

-- 2) player_seasons — 25/26(임대처) + 26/27(빌라 복귀)
INSERT INTO player_seasons(player_id,season,club,primary_position,shirt_no,minutes) VALUES
(27,'2025-26','RB Leipzig (loan)','RB',NULL,297),
(28,'2025-26','West Brom (loan)','LM',NULL,1397),
(29,'2025-26','Port Vale (loan)','GK',NULL,3240),
(27,'2026-27','Aston Villa','RB',20,NULL),
(28,'2026-27','Aston Villa','LM',19,NULL),
(29,'2026-27','Aston Villa','GK',18,NULL);

-- 3) player_match_positions — 25/26 임대처 경기별 실측 (Gauci=GK 제외)
-- source/confidence 공통 문구는 각 행에 반영. pos_class: y<40 R / 40-60 C / y>60 L, x>=52 전진, <45분 NULL.
-- Nedeljković (RB Leipzig)
INSERT INTO player_match_positions(season,player_id,event_id,date,opponent,venue,competition,minutes,rating,avg_x,avg_y,started,pos_class,source,confidence) VALUES
('2025-26',27,14065064,'2025-08-30','1. FC Heidenheim','H','Bundesliga',1,NULL,30.00,19.30,0,NULL,'SofaScore API /event/14065064/average-positions + /lineups (2026-07-22)','HIGH on min/avg coords (API); <45min→pos_class NULL. Loan club RB Leipzig.'),
('2025-26',27,14065091,'2025-09-20','1. FC Köln','H','Bundesliga',10,6.7,34.20,14.40,0,NULL,'SofaScore API /event/14065091/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); <45min→NULL. Loan club RB Leipzig.'),
('2025-26',27,14994248,'2025-12-02','1. FC Magdeburg','H','DFB Pokal',45,7.0,52.54,20.15,0,'RM/AMR','SofaScore API /event/14994248/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y20 R lane, x52.5 advanced. Loan club RB Leipzig.'),
('2025-26',27,14065167,'2025-12-06','Eintracht Frankfurt','H','Bundesliga',90,6.9,46.86,16.14,1,'pivot-right','SofaScore API /event/14065167/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y16 R lane, x47 pivot. Loan club RB Leipzig.'),
('2025-26',27,14062138,'2025-12-12','1. FC Union Berlin','A','Bundesliga',81,5.6,43.08,15.16,1,'pivot-right','SofaScore API /event/14062138/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y15 R lane, x43 pivot. Loan club RB Leipzig.'),
('2025-26',27,14062143,'2025-12-20','Bayer 04 Leverkusen','H','Bundesliga',70,6.0,44.13,16.70,1,'pivot-right','SofaScore API /event/14062143/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y17 R lane, x44 pivot. Loan club RB Leipzig.');

-- Iling-Junior (West Brom, Championship)
INSERT INTO player_match_positions(season,player_id,event_id,date,opponent,venue,competition,minutes,rating,avg_x,avg_y,started,pos_class,source,confidence) VALUES
('2025-26',28,14059516,'2025-09-13','Derby County','H','Championship',17,6.6,77.31,26.45,0,NULL,'SofaScore API /event/14059516/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); <45min→NULL. Loan club West Brom.'),
('2025-26',28,14059540,'2025-09-26','Leicester City','H','Championship',72,7.7,51.60,37.54,1,'pivot-right','SofaScore API /event/14059540/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y37.5 R lane, x51.6 pivot. Loan club West Brom.'),
('2025-26',28,14059552,'2025-10-01','Norwich City','A','Championship',85,6.9,43.43,39.41,1,'pivot-right','SofaScore API /event/14059552/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y39.4 R lane (near C boundary), x43 pivot. Loan club West Brom.'),
('2025-26',28,14059558,'2025-10-04','Millwall','A','Championship',28,6.2,67.04,19.36,0,NULL,'SofaScore API /event/14059558/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); <45min→NULL. Loan club West Brom.'),
('2025-26',28,14059576,'2025-10-18','Preston North End','H','Championship',87,6.3,53.47,21.05,1,'RM/AMR','SofaScore API /event/14059576/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y21 R lane, x53.5 advanced. Loan club West Brom.'),
('2025-26',28,14059585,'2025-10-22','Watford','A','Championship',70,6.0,61.34,21.22,1,'RM/AMR','SofaScore API /event/14059585/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y21 R lane, x61 advanced. Loan club West Brom.'),
('2025-26',28,14059594,'2025-10-25','Ipswich Town','A','Championship',71,6.7,58.81,27.80,1,'RM/AMR','SofaScore API /event/14059594/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y28 R lane, x59 advanced. Loan club West Brom.'),
('2025-26',28,14059612,'2025-11-01','Sheffield Wednesday','H','Championship',60,6.2,61.55,20.34,1,'RM/AMR','SofaScore API /event/14059612/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y20 R lane, x61.5 advanced. Loan club West Brom.'),
('2025-26',28,14059617,'2025-11-04','Charlton Athletic','A','Championship',81,7.2,53.83,19.09,1,'RM/AMR','SofaScore API /event/14059617/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y19 R lane, x54 advanced. Loan club West Brom.'),
('2025-26',28,14059634,'2025-11-08','Oxford United','H','Championship',11,6.6,39.11,25.80,0,NULL,'SofaScore API /event/14059634/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); <45min→NULL. Loan club West Brom.'),
('2025-26',28,14059641,'2025-11-22','Coventry City','A','Championship',45,6.8,39.84,25.35,0,'pivot-right','SofaScore API /event/14059641/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y25 R lane, x40 pivot; sub-on 45min. Loan club West Brom.'),
('2025-26',28,14059655,'2025-11-26','Birmingham City','H','Championship',11,6.4,77.90,76.40,0,NULL,'SofaScore API /event/14059655/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); <45min→NULL (L-lane cameo). Loan club West Brom.'),
('2025-26',28,14059671,'2025-11-29','Swansea City','H','Championship',45,6.3,69.39,19.44,1,'RM/AMR','SofaScore API /event/14059671/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y19 R lane, x69 advanced. Loan club West Brom.'),
('2025-26',28,14059690,'2025-12-09','Southampton','A','Championship',90,6.2,60.02,15.27,1,'RM/AMR','SofaScore API /event/14059690/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y15 R lane, x60 advanced. Loan club West Brom.'),
('2025-26',28,14059708,'2025-12-12','Sheffield United','H','Championship',1,NULL,26.45,41.15,0,NULL,'SofaScore API /event/14059708/average-positions + /lineups (2026-07-22)','HIGH on min/avg coords (API); <45min→NULL. Loan club West Brom.'),
('2025-26',28,14059712,'2025-12-20','Hull City','A','Championship',9,6.5,60.16,79.34,0,NULL,'SofaScore API /event/14059712/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); <45min→NULL (L-lane cameo). Loan club West Brom.'),
('2025-26',28,14059732,'2025-12-26','Bristol City','H','Championship',25,7.2,62.27,46.01,0,NULL,'SofaScore API /event/14059732/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); <45min→NULL. Loan club West Brom.'),
('2025-26',28,14059742,'2025-12-29','Queens Park Rangers','H','Championship',84,6.5,58.70,17.12,1,'RM/AMR','SofaScore API /event/14059742/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y17 R lane, x59 advanced. Loan club West Brom.'),
('2025-26',28,14059752,'2026-01-01','Swansea City','A','Championship',80,6.7,52.89,22.15,1,'RM/AMR','SofaScore API /event/14059752/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y22 R lane, x52.9 advanced. Loan club West Brom.'),
('2025-26',28,14059758,'2026-01-05','Leicester City','A','Championship',11,6.7,67.09,71.30,0,NULL,'SofaScore API /event/14059758/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); <45min→NULL (L-lane cameo). Loan club West Brom.'),
('2025-26',28,14059778,'2026-01-16','Middlesbrough','H','Championship',90,6.5,55.36,83.53,1,'LW/AML','SofaScore API /event/14059778/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y83.5 L lane, x55 advanced. Loan club West Brom.'),
('2025-26',28,14059787,'2026-01-20','Norwich City','H','Championship',90,4.8,60.92,77.64,1,'LW/AML','SofaScore API /event/14059787/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y77.6 L lane, x61 advanced; team 0-5 loss. Loan club West Brom.'),
('2025-26',28,14059794,'2026-01-23','Derby County','A','Championship',82,6.7,57.36,66.99,0,'LW/AML','SofaScore API /event/14059794/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y67 L lane, x57 advanced; early sub-on. Loan club West Brom.'),
('2025-26',28,14059814,'2026-01-31','Portsmouth','A','Championship',45,6.5,53.87,83.01,1,'LW/AML','SofaScore API /event/14059814/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y83 L lane, x54 advanced. Loan club West Brom.');

-- Iling-Junior (Pisa, Serie A) — 전부 교체(45분 미만 4건 + 45분 1건 좌측)
INSERT INTO player_match_positions(season,player_id,event_id,date,opponent,venue,competition,minutes,rating,avg_x,avg_y,started,pos_class,source,confidence) VALUES
('2025-26',28,13981670,'2026-02-13','AC Milan','H','Serie A',33,6.6,61.69,63.68,0,NULL,'SofaScore API /event/13981670/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); <45min→NULL (L-lane). Loan club Pisa.'),
('2025-26',28,13981677,'2026-02-23','Fiorentina','A','Serie A',45,6.2,50.52,72.84,1,'pivot-left','SofaScore API /event/13981677/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); y73 L lane, x50.5 pivot. Loan club Pisa.'),
('2025-26',28,13981686,'2026-03-02','Bologna','H','Serie A',1,NULL,70.97,63.77,0,NULL,'SofaScore API /event/13981686/average-positions + /lineups (2026-07-22)','HIGH on min/avg coords (API); <45min→NULL. Loan club Pisa.'),
('2025-26',28,13981697,'2026-03-07','Juventus','A','Serie A',14,6.5,71.70,87.77,0,NULL,'SofaScore API /event/13981697/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); <45min→NULL (L-lane). Loan club Pisa.'),
('2025-26',28,13981718,'2026-03-22','Como','A','Serie A',14,6.6,45.39,77.09,0,NULL,'SofaScore API /event/13981718/average-positions + /lineups (2026-07-22)','HIGH on min/rating/avg coords (API); <45min→NULL (L-lane). Loan club Pisa.');

-- 4) player_role_map — 통합 measured 그리드 (season=2026-27: 복귀 시즌 스쿼드 평가용, 데이터 출처는 25/26 임대처)
INSERT INTO player_role_map(player_id,season,game_version,kind,pos_label,x,y,role_id,focus,map25,rationale) VALUES
(27,'2026-27','FC26','measured','RB',81.7,46.6,'','','00014000240002X0003900113',
 '25/26 RB 라이프치히 임대 우측 선발 4경기(≥45분: Magdeburg·Frankfurt·Union·Leverkusen)의 SofaScore 히트맵 균등가중 통합. tool orientation row0=공격/col0=좌. centroid tool_x81.7(우측)·tool_y46.6(딥). 우측 딥RB — 전진 빈도 낮음. 26/27 RB 뎁스 평가용. Source: SofaScore API /event/*/player/1152923/heatmap (2026-07-22).'),
(28,'2026-27','FC26','measured','RM/AMR',75.9,55.1,'','','001251015X011261013600122',
 '25/26 웨스트브롬 임대 우측 선발 12경기의 SofaScore 히트맵 균등가중 통합(주 포지션). tool orientation row0=공격/col0=좌. centroid tool_x75.9(우측)·tool_y55.1(전진). 등록상 LM이나 실측 주력은 우측 인사이드윙/윙백. 26/27 스쿼드 평가용. Source: SofaScore API /event/*/player/996919/heatmap (2026-07-22).'),
(28,'2026-27','FC26','measured:L','LW/AML',23.8,56.6,'','','64112X3210721008320031100',
 '25/26 웨스트브롬 임대 좌측 선발 4경기(1월 Middlesbrough·Norwich·Derby·Portsmouth)의 SofaScore 히트맵 균등가중 통합(부 포지션). tool orientation row0=공격/col0=좌. centroid tool_x23.8(좌측)·tool_y56.6(전진). 시즌 후반 좌측 전환 표본. Source: SofaScore API /event/*/player/996919/heatmap (2026-07-22).');

COMMIT;
