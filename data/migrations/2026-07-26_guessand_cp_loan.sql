-- Guessand(18) 크리스탈 팰리스 임대(2026-01-30~시즌말) 실측 수집
-- SofaScore player id 930245. 수집일 2026-07-26.
-- 주의: player_seasons PK(player_id,season) 때문에 팰리스 임대 행은 별도 추가 불가
--       (2025-26 빌라 행 유지). 임대 사실은 아래 행들의 source/confidence에 명기.

-- ===== Crystal Palace 임대 45분+ 7경기 =====
INSERT OR REPLACE INTO player_match_positions
(season,player_id,event_id,date,opponent,venue,competition,minutes,rating,avg_x,avg_y,started,pos_class,source,confidence) VALUES
('2025-26',18,14025209,'2026-02-11','Burnley','H','Premier League',58,6.2,58.7,58.2,1,'C-fwd','api.sofascore.com /event/14025209 (2026-07-26)','HIGH — API 공식. Crystal Palace 임대 신분. 히트포인트 48'),
('2025-26',18,15380228,'2026-02-26','Zrinjski','H','Conference League',90,8.2,67.6,74.3,1,'L-fwd','api.sofascore.com /event/15380228 (2026-07-26)','HIGH — API 공식. CP 임대. 1골, 임대 최고 평점이나 상대는 컨퍼런스리그 하위 시드. 히트포인트 71'),
('2025-26',18,14023981,'2026-03-05','Tottenham','A','Premier League',67,6.5,57.6,55.3,1,'C-fwd','api.sofascore.com /event/14023981 (2026-07-26)','HIGH — API 공식. CP 임대. 히트포인트 42'),
('2025-26',18,15632045,'2026-03-12','AEK Larnaca','H','Conference League',90,6.3,66.5,61.8,1,'L-fwd','api.sofascore.com /event/15632045 (2026-07-26)','HIGH — API 공식. CP 임대. 히트포인트 73'),
('2025-26',18,14023991,'2026-03-15','Leeds','H','Premier League',90,6.4,61.7,61.2,1,'L-fwd','api.sofascore.com /event/14023991 (2026-07-26)','HIGH — API 공식. CP 임대. PL 선발 90분이나 0골 xG0.04. 히트포인트 45'),
('2025-26',18,15632053,'2026-03-19','AEK Larnaca','A','Conference League',76,6.4,57.9,51.4,1,'C-fwd','api.sofascore.com /event/15632053 (2026-07-26)','HIGH — API 공식. CP 임대. 히트포인트 35'),
('2025-26',18,15632638,'2026-04-09','Fiorentina','H','Conference League',65,7.4,66.1,61.8,1,'L-fwd','api.sofascore.com /event/15632638 (2026-07-26)','HIGH — API 공식. CP 임대. 이 경기 후 무릎 부상으로 9경기 결장(5/17 브렌트포드전 벤치 복귀)');

-- ===== 임대 통합 프로파일 =====
INSERT OR REPLACE INTO player_role_map
(player_id,season,game_version,kind,pos_label,x,y,role_id,focus,map25,rationale) VALUES
(18,'2025-26','FC26','measured:CP-loan','CAM',40,62,NULL,NULL,'01100|22111|32431|X7443|12311',
 '팰리스 임대 45분+ 7경기 통합(글라스너 3-4-2-1의 좌측 10번/세컨톱). 평균 y≈60.6(중앙-좌측), x≈62.3. mid-left 24%+att-left 17%가 최빈 — 니스 measured:ST 프로파일(중앙+좌하프스페이스 드리프트)과 방향 일치. 즉 팰리스는 게상을 "맞는 역할"에 썼다. 그러나 산출은 부분 회복에 그침: 45분+ 평점 6.77, 경기당 xG 0.17·xA 0.05·키패스 0.14 — 빌라 우측(xG 0.17)과 동일 수준, 니스 베스트6(xG 0.62·xA 0.44)에는 크게 미달. 2골 모두 컨퍼런스리그(즈린스키)·PL 교체 18분(울버햄튼), PL 선발 경기 평점 6.2~6.5. 결론: 역할 교정만으로 니스 산출이 복원되지 않음 — 니스 24-25 폭발에는 리그 수준·xG 초과달성(10골/xG7.77) 요인이 겹쳐 있었다는 방증. 4/9 이후 무릎 부상 9경기 결장으로 표본 확장 불가');
