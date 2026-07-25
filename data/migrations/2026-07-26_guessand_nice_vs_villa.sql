-- Guessand(18) Nice 2024-25 vs Villa 2025-26 실측 비교 수집
-- SofaScore player id 930245. 수집일 2026-07-26.
-- source 공통: /api/v1/event/<eid>/player/930245/{statistics,heatmap} + /api/v1/event/<eid>/average-positions

INSERT OR IGNORE INTO seasons(code,label) VALUES('2024-25','2024-25');

INSERT OR REPLACE INTO player_seasons(player_id,season,club,primary_position,shirt_no,minutes)
VALUES(18,'2024-25','Nice','ST/RW',NULL,3086);

-- ===== Nice 2024-25 베스트 6경기 (45분+, 평점순) =====
INSERT OR REPLACE INTO player_match_positions
(season,player_id,event_id,date,opponent,venue,competition,minutes,rating,avg_x,avg_y,started,pos_class,source,confidence) VALUES
('2024-25',18,12450958,'2024-09-01','Angers','A','Ligue 1',88,8.7,72.0,52.7,1,'C-fwd','api.sofascore.com /event/12450958 statistics+average-positions (2026-07-26)','HIGH — API 공식 평점·평균좌표. 2골 xG1.24. 히트포인트 47'),
('2024-25',18,12450187,'2025-05-17','Brest','H','Ligue 1',78,8.6,67.6,51.1,1,'C-fwd','api.sofascore.com /event/12450187 (2026-07-26)','HIGH — API 공식. 1골1도움. 히트포인트 47'),
('2024-25',18,12451024,'2025-02-08','Lens','H','Ligue 1',90,8.5,61.9,27.0,1,'R-fwd','api.sofascore.com /event/12451024 (2026-07-26)','HIGH — API 공식. 터치74 키패스4. 히트포인트 86'),
('2024-25',18,12450985,'2025-01-26','Marseille','H','Ligue 1',90,8.3,54.0,23.9,1,'R-fwd','api.sofascore.com /event/12450985 (2026-07-26)','HIGH — API 공식. 1골1도움. 히트포인트 39'),
('2024-25',18,12450986,'2024-09-20','Saint-Étienne','H','Ligue 1',45,8.3,56.2,51.2,0,'C-fwd','api.sofascore.com /event/12450986 (2026-07-26)','HIGH — API 공식. 45분 출전(교체) 1골1도움 xG1.08. 히트포인트 25로 그리드는 MEDIUM'),
('2024-25',18,12450941,'2025-01-03','Rennes','H','Ligue 1',89,8.1,55.9,30.3,1,'R-fwd','api.sofascore.com /event/12450941 (2026-07-26)','HIGH — API 공식. 1골1도움. 히트포인트 40');

-- ===== Villa 2025-26 전 경기 (45분+) =====
INSERT OR REPLACE INTO player_match_positions
(season,player_id,event_id,date,opponent,venue,competition,minutes,rating,avg_x,avg_y,started,pos_class,source,confidence) VALUES
('2025-26',18,14025091,'2025-08-31','Crystal Palace','H','Premier League',45,6.2,68.2,87.1,0,'L-fwd','api.sofascore.com /event/14025091 (2026-07-26)','HIGH — API 공식. 유일한 좌측 출전. 히트포인트 28'),
('2025-26',18,14025136,'2025-09-13','Everton','A','Premier League',45,6.7,56.0,17.4,0,'R-fwd','api.sofascore.com /event/14025136 (2026-07-26)','HIGH — API 공식. 히트포인트 20 그리드 MEDIUM'),
('2025-26',18,14598940,'2025-09-16','Brentford','A','EFL Cup',80,5.9,60.9,18.7,1,'R-fwd','api.sofascore.com /event/14598940 (2026-07-26)','HIGH — API 공식. 히트포인트 47'),
('2025-26',18,14025172,'2025-09-21','Sunderland','A','Premier League',73,6.8,54.9,20.6,1,'R-fwd','api.sofascore.com /event/14025172 (2026-07-26)','HIGH — API 공식. 히트포인트 45'),
('2025-26',18,14572679,'2025-09-25','Bologna','H','Europa League',90,6.3,59.7,29.2,1,'R-fwd','api.sofascore.com /event/14572679 (2026-07-26)','HIGH — API 공식. 히트포인트 33'),
('2025-26',18,14025181,'2025-09-28','Fulham','H','Premier League',83,6.5,57.3,16.3,1,'R-fwd','api.sofascore.com /event/14025181 (2026-07-26)','HIGH — API 공식. 히트포인트 46'),
('2025-26',18,14572642,'2025-10-02','Feyenoord','A','Europa League',90,6.3,59.1,21.4,1,'R-fwd','api.sofascore.com /event/14572642 (2026-07-26)','HIGH — API 공식. 히트포인트 42'),
('2025-26',18,14025249,'2025-10-19','Tottenham','A','Premier League',61,6.5,44.8,26.3,1,'R-pivot','api.sofascore.com /event/14025249 (2026-07-26)','HIGH — API 공식. 평균 x 44.8로 유일하게 피봇 깊이. 히트포인트 22 그리드 MEDIUM'),
('2025-26',18,14572811,'2025-10-23','GA Eagles','A','Europa League',90,7.3,66.8,25.1,1,'R-fwd','api.sofascore.com /event/14572811 (2026-07-26)','HIGH — API 공식. 1골 xG0.75, 빌라 최고평점 경기. 히트포인트 47'),
('2025-26',18,14025281,'2025-11-01','Liverpool','A','Premier League',59,5.7,53.6,33.6,1,'R-fwd','api.sofascore.com /event/14025281 (2026-07-26)','HIGH — API 공식. 터치 12. 히트포인트 19 그리드 MEDIUM'),
('2025-26',18,14572677,'2025-11-06','Maccabi Tel-Aviv','H','Europa League',74,6.5,54.4,11.6,1,'R-fwd','api.sofascore.com /event/14572677 (2026-07-26)','HIGH — API 공식. y 11.6 극단적 우측 고정. 히트포인트 36'),
('2025-26',18,14572678,'2025-11-27','Young Boys','H','Europa League',90,6.2,71.3,21.0,1,'R-fwd','api.sofascore.com /event/14572678 (2026-07-26)','HIGH — API 공식. att-right 61%. 히트포인트 44'),
('2025-26',18,14025129,'2025-12-03','Brighton','A','Premier League',86,5.3,56.9,24.0,1,'R-fwd','api.sofascore.com /event/14025129 (2026-07-26)','HIGH — API 공식. 1도움에도 팀내 최저급 평점, def-right 37%. 히트포인트 27 그리드 MEDIUM. 기존 appearances id54(경기 서술)와 상보'),
('2025-26',18,14572748,'2025-12-11','Basel','A','Europa League',90,7.2,62.0,14.9,1,'R-fwd','api.sofascore.com /event/14572748 (2026-07-26)','HIGH — API 공식. 1골. 히트포인트 52'),
('2025-26',18,14025064,'2026-01-18','Everton','H','Premier League',72,7.2,56.5,27.3,1,'R-fwd','api.sofascore.com /event/14025064 (2026-07-26)','HIGH — API 공식. 히트포인트 31');

-- ===== 통합 프로파일 (포지션-순수 규칙 준수: 니스는 중앙/우측 분리, 빌라는 좌측 1경기 제외) =====
INSERT OR REPLACE INTO player_role_map
(player_id,season,game_version,kind,pos_label,x,y,role_id,focus,map25,rationale) VALUES
(18,'2024-25','FC26','measured:ST','ST',49,65,NULL,NULL,'00101|61221|33475|46555|47X52',
 '니스 베스트6 중 중앙 출전 3경기(앙제 8.7·브레스트 8.6·생테티엔 8.3) 통합. SofaScore 평균 y≈51.7(중앙), x≈65.3(전진). att-centre 24%가 최빈 존, 좌우 하프스페이스로 자유 드리프트(mid-left 18%). 3경기 4골3도움 xG평균 0.96. 게상이 "잘할 때"의 주 프로파일 — 중앙 스트라이커/세컨톱으로 좌측 하프스페이스 드리프트 자유가 있을 때 최고 산출. 표본 3경기로 그리드는 MEDIUM-HIGH'),
(18,'2024-25','FC26','measured:RM','RM',73,57,NULL,NULL,'00112|0135X|00255|01379|01444',
 '니스 베스트6 중 우측 출전 3경기(랑스 8.5·마르세유 8.3·렌 8.1) 통합. 평균 y≈27(우측), x≈57.9. mid-right 32%·att-right 24%지만 att-centre+mid-centre 18%로 안쪽 침투 겸장 — 우측에서도 하프스페이스 진입이 잦은 인버티드형. 3경기 2골2도움 키패스 6. 니스에서는 우측 배치여도 중앙 관여가 유지됨'),
(18,'2025-26','FC26','measured','RM',79,58,NULL,NULL,'01112|01126|11136|0112X|01344',
 '빌라 45분+ 15경기 중 우측 14경기 통합(좌측 1경기 제외, 포지션-순수 규칙). 평균 y≈21.5(니스 우측 26.6보다 5p 더 측면 고정), att-right 32%+mid-right 31%+def-right 16% = 우측 레인에만 79%. 니스 대비 att-centre 10%로 중앙 관여 반감, def-right 16%로 수비 부담 배증. 산출 붕괴: 평점 8.42→6.44(니스 베스트6 대비), 니스 시즌 전체 7.30 대비도 -0.86. 터치 39→29, xG 0.62→0.17, xA 0.44→0.02, 키패스 1.5→0.4. 에메리 4-2-3-1 우측 윙어는 측면 고정+수비 트래킹 임무 — 게상의 강점(중앙 연계·하프스페이스 드리프트·박스 침투)이 구조적으로 차단된 배치. 실측 결론: 부적응이 아니라 역할 미스매치');
