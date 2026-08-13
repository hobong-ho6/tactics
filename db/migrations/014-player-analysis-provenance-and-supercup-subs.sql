-- 선수 영상·스카우트 분석의 관찰 시점/표본 범위를 명시하고,
-- 2026 UEFA Super Cup 교체 5명의 원천 데이터·분석·경기 전용 처방을 보강한다.
PRAGMA foreign_keys = ON;
BEGIN;

ALTER TABLE player_duties ADD COLUMN observed_from TEXT;
ALTER TABLE player_duties ADD COLUMN observed_to TEXT;
ALTER TABLE player_duties ADD COLUMN sample_scope TEXT;
ALTER TABLE player_duties ADD COLUMN sample_note TEXT;

-- 기존 기록은 근거가 말하는 범위만 소급 분류한다. 날짜를 역추정할 수 없는 영상 종합은
-- 기간 미기록으로 남기고 UI에서 이를 명시한다.
UPDATE player_duties
SET sample_scope='unknown',
    sample_note='기존 기록에 개별 시청 경기·영상의 관찰 기간이 명시되지 않음'
WHERE sample_scope IS NULL;

UPDATE player_duties
SET observed_from='2026-08-12', observed_to='2026-08-12',
    sample_scope='specific_match',
    sample_note='2026-08-12 UEFA Super Cup PSG전 단일 경기 — SofaScore event 16260286와 경기 후 영상·기사 교차검증'
WHERE instr(source,'16260286')>0 OR duties LIKE '%PSG 슈퍼컵 단일경기%';

UPDATE player_duties
SET observed_from='2025-08-01', observed_to='2026-08-12',
    sample_scope='season',
    sample_note='2025/26 시즌 경기·시즌 리뷰 중심; 이적·감독 발언은 2026-08-12까지 포함'
WHERE sample_scope='unknown'
  AND (duties LIKE '%25/26%' OR duties LIKE '%2025-26%' OR duties LIKE '%2025/26%');

UPDATE player_duties
SET observed_to='2026-08-12', sample_scope='multi_source',
    sample_note='복수 경기·영상·스카우트 자료 종합. 개별 경기 목록은 기존 기록에 미기록되어 관찰 시작일은 확정하지 않음'
WHERE sample_scope='unknown'
  AND (duties LIKE '%영상 종합%' OR duties LIKE '%스카우트%');

-- 새 소속팀 기준으로 비어 있던 현재 스쿼드 영상·스카우트 분석.
INSERT OR IGNORE INTO player_duties(
  regime_id,season,player_id,position,duties,execution,adherence,
  game_role_implication,source,confidence,observed_from,observed_to,sample_scope,sample_note
) VALUES
(2,'2026-27',13,'CAM/left pocket',
 '알론소가 직접 요구한 임무는 스트라이커와 10번 가까이의 포켓에서 연결하고, 왼쪽 출발을 기본으로 우측까지 바꾸는 유연한 2선 공격수다.',
 '첼시 공식전은 아직 0경기다. 실측은 전부 빌라 2025/26 56경기 4,652분 평균 6.90이며, CAM보다 좌측 인사이드 표본의 적합이 높다. 따라서 감독 지시는 확인됐지만 새 팀에서의 실행은 미검증이다.',
 'PRESEASON PENDING — 감독의 역할 설명에는 정합하나 첼시 경기 표본이 생기기 전까지 수행 판정 보류.',
 'cam_playmaker/Roaming 또는 좌측 wm_insidefwd/Balanced 후보. 팔머·주앙 페드루와의 점유 구역은 첫 공식전에서 재검증.',
 'Chelsea 공식 영입 https://www.chelseafc.com/en/news/article/morgan-rogers-signs-for-chelsea ; Xabi Alonso 역할 설명 https://www.chelseafc.com/en/news/article/xabi-alonso-on-his-plan-for-great-signing-morgan-rogers-and-cole-palmer ; Chelsea 선수 인터뷰 https://www.chelseafc.com/en/news/article/morgan-rogers-interview-on-joy-family-and-finding-his-best-self',
 'HIGH 감독 발언·빌라 실측 / LOW 첼시 실행 — 공식전 0경기',
 '2025-08-01','2026-07-31','season','2025/26 Aston Villa 전체 실측 + 2026-07 Chelsea 공식 영입·감독 발언; Chelsea 경기 분석은 아님'),
(2,'2026-27',80,'LB',
 '라요에서 높은 좌측 폭과 전진을 반복한 공격형 레프트백. 첼시에서는 하토와 경쟁하며 알론소의 비대칭 윙백/풀백 구조에서 외곽 전진 옵션을 제공하는 것이 예상 임무다.',
 '2025/26 라요 전 대회 55경기 3,519분 평균 6.80, 1골 3도움. 45분+ LB 39경기 그리드는 fb_att_wb/Support .890이다. 단 모든 위치·스탯은 라요 소속 기록이다.',
 'TRANSFERRED — 이전 팀 임무는 실측으로 확인, 첼시·알론소 체제 수행은 공식전 0경기로 미검증.',
 'LB fb_att_wb/Support 후보. 하토와 같은 왼쪽을 공유하므로 선발·국면별 배치는 첫 공식전 뒤 확정.',
 'Chelsea 공식 영입 https://www.chelseafc.com/en/news/article/pep-chavarria-signs-for-chelsea ; reports/transfer-watch/2026-08-13.md ; SofaScore player 1010421',
 'HIGH 라요 55경기 원천 / LOW 첼시 역할 투영',
 '2025-08-01','2026-08-13','season','2025/26 Rayo Vallecano 시즌 전체 + 2026-08-13 Chelsea 공식 영입; Chelsea 경기 분석은 아님'),
(3,'2026-27',85,'RCB',
 '바르셀로나 표본에서 우측 센터백으로 전진해 끊고 배급하는 공격적 볼 플레잉 센터백. 리버풀에서는 자케 이후의 추가 보강이라 같은 RCB 자리를 두고 경쟁한다.',
 '2025/26 포함 수집 58경기 2,084분 평균 6.90. 45분+ 바르셀로나 RCB 22경기 표본은 cb_bpd/Aggressive .908이고 LCB 재배치 시 적합이 크게 하락한다.',
 'TRANSFERRED — 바르셀로나 역할은 실측 확인, 리버풀·이라올라 체제 실행은 공식전 0경기로 미검증.',
 'RCB cb_bpd/Aggressive. 자케와 적합 차 .005라 수치로 우열을 정하지 않고 좌우 유연성·가용성으로 선발 판단.',
 'Liverpool 공식 영입 https://www.liverpoolfc.com/news/liverpool-agree-deal-sign-ronald-araujo-loan ; Sky Sports https://www.skysports.com/football/news/11669/13570899 ; reports/transfer-watch/2026-08-12.md ; SofaScore player 925097',
 'HIGH 바르셀로나 원천 / LOW 리버풀 역할 투영',
 '2025-08-01','2026-08-12','season','2025/26 Barcelona 시즌 표본 + 2026-08-11 Liverpool 공식 영입; Liverpool 경기 분석은 아님'),
(3,'2026-27',88,'LM/RM',
 '폭발적인 속도와 직접 드리블을 쓰며 양쪽 윙을 소화하고, 공을 잃은 뒤 복귀에도 가담하는 와이드 공격수. 좌우 혼합 그리드는 위치를 뭉개므로 반드시 측면별로 본다.',
 '오사수나 2025/26 전 대회 34경기 2,766분 7골 5도움. 실측은 좌측 23경기 LM wm_wideplm/Attack .729, 우측 11경기 RM wm_winger/Balanced .772다.',
 'TRANSFERRED — 오사수나 시즌 수행은 확인, 이라올라 체제와 살라 이탈 뒤 우측 기용은 공식전 0경기로 미검증.',
 'LM wide playmaker/Attack와 RM winger/Balanced를 별도 보존. 평균낸 혼합 처방은 사용하지 않는다.',
 'Liverpool 공식 프로필 https://www.liverpoolfc.com/news/career-path-spain-impact-and-history-maker-get-know-victor-munoz ; Liverpool 공식 영입 https://www.liverpoolfc.com/news/liverpool-agree-deal-sign-spain-forward-victor-munoz ; SofaScore player 1145642 ; reports/transfer-watch/2026-08-13.md',
 'HIGH 오사수나 원천·구단 Opta 요약 / LOW 리버풀 실행',
 '2025-08-01','2026-08-13','season','2025/26 Osasuna 시즌 전체 34경기; Liverpool 공식전 분석은 아님'),
(3,'2026-27',89,'RCB/LCB',
 '공중 경합과 박스 수비가 강하면서도 라인을 깨는 전진 패스를 시도하는 침착한 센터백. 우측이 주 표본이지만 왼쪽도 소화해 아라우호보다 좌우 전환 여지가 크다.',
 '렌 2025/26 21경기. 우측 14경기 RCB cb_bpd/Aggressive .903, 좌측 7경기 LCB .850. 구단 Opta 요약은 공중 경합 승률 75.5%, 패스 성공률 90.4%, 클리어 4.9/90을 제시한다.',
 'TRANSFERRED — 렌 시즌 수행은 확인, 리버풀·이라올라 체제 실행은 공식전 0경기로 미검증.',
 'RCB cb_bpd/Aggressive 주 처방, 필요 시 LCB 대안. 어깨 부상으로 시즌이 짧아진 점을 가용성 변수로 유지.',
 'Liverpool 공식 팩트파일 https://www.liverpoolfc.com/news/jeremy-jacquet-factfile-aerial-dominance-van-dijk-respect-and-lfc-homework ; Liverpool 공식 영입 https://www.liverpoolfc.com/news/liverpool-complete-signing-jeremy-jacquet ; SofaScore player 1445625 ; reports/transfer-watch/2026-08-13.md',
 'HIGH 렌 원천·구단 Opta 요약 / LOW 리버풀 실행',
 '2025-08-01','2026-08-13','season','2025/26 Rennes 시즌 전체 21경기; Liverpool 공식전 분석은 아님');

UPDATE player_duties
SET source='SofaScore event 16260286 https://www.sofascore.com/api/v1/event/16260286 ; AS Emery interview 2026-08-12 https://as.com/futbol/internacional/unai-emery-habra-mas-cambios-f202608-n/ ; BeanymanSports post-match 2026-08-13 https://www.youtube.com/watch?v=cV0xoK0gK3w ; The Villa Park Podcast 2026-08-13 https://www.youtube.com/watch?v=NfejEXQj3sE ; reports/match-watch/2026-08-12-avl-psg-super-cup.md'
WHERE regime_id=1 AND player_id=30 AND position='LM';

UPDATE player_duties
SET source='SofaScore event 16260286 https://www.sofascore.com/api/v1/event/16260286 ; El País 2026-08-12 https://elpais.com/deportes/futbol/2026-08-12/el-psg-extiende-su-hegemonia-tras-vencer-la-supercopa-de-europa-ante-el-aston-villa.html ; AS 2026-08-12 https://as.com/futbol/internacional/invencible-luis-enrique-f202608-n/ ; BeanymanSports https://www.youtube.com/watch?v=cV0xoK0gK3w ; talkSPORT https://www.youtube.com/watch?v=6_VcfCoJTmQ ; reports/match-watch/2026-08-12-avl-psg-super-cup.md'
WHERE regime_id=1 AND player_id=61 AND position='ST' AND instr(duties,'PSG 슈퍼컵')>0;

-- 종합 평가가 비어 있던 현재 선수. 이미 확보된 실측과 공식 출처만 사용한다.
INSERT OR IGNORE INTO player_evaluations(
  regime_id,player_id,overall,traits,strengths,stat_eval,fit_emery,fit_alonso,fit_iraola,
  source,confidence,updated,fotmob_eval
) VALUES
(1,30,'B — 17세 유스지만 슈퍼컵 PSG전 90분을 소화하며 성인 공식전 좌측 역할의 첫 완전 표본을 남겼다. 단 한 경기만으로 시즌 대표 역할을 확정하지 않는다.',
 '왼쪽 안쪽 지원형 미드필더. 명목 LAM보다 낮고 중앙에 서며 압박·회수·짧은 연결로 외곽 풀백을 보조한다.',
 '장점은 전술 규율과 90분 가용성. 약점 판단은 표본 부족으로 보류하며, 성인 공식전 같은 위치 2경기 이상이 필요하다.',
 '수집 11경기 592분 평균 6.67. PSG전 90분 6.2, 20/25패스, 1키패스, 2슈팅(1유효), 3/9경합, 1태클, 6회수. 경기 그리드 wm_widemid/Support .788.',
 'MEDIUM — 에메리가 경기 전 해당 포지션을 준비시켰다고 확인했고 90분 실측이 일치한다.',
 'LOW — 알론소 체제 교차 투영 근거 없음.',
 'LOW — 이라올라 체제 교차 투영 근거 없음.',
 'SofaScore event 16260286; reports/match-watch/2026-08-12-avl-psg-super-cup.md; https://as.com/futbol/internacional/unai-emery-habra-mas-cambios-f202608-n/; https://www.youtube.com/watch?v=cV0xoK0gK3w',
 'HIGH 경기 원천 / MEDIUM 역할 — 성인 공식전 단일 경기','2026-08-13',NULL),
(2,80,'B — 라요의 대량 시즌 표본과 공격형 LB 적합은 확인됐지만 첼시 공식전이 없어 현재 평가는 이전 팀 수행과 알론소 전술 투영을 분리해야 한다.',
 '높고 넓게 전진하는 공격형 레프트백. 좌측 폭과 지원을 제공하되 새 팀에서는 하토와의 역할 분담이 미정이다.',
 '강점은 55경기 가용성과 전진 위치 반복. 위험은 라요에서의 역할을 첼시에 그대로 복사할 수 없다는 점이다.',
 '2025/26 전 대회 55경기 3,519분 평균 6.80, 1골 3도움. 경기당 xG .047, xA .089, 태클 1.33, 인터셉트 .76. 45분+ LB 39경기 fb_att_wb/Support .890.',
 'LOW — 에메리 체제 대상 아님.',
 'MEDIUM — 알론소의 비대칭 측면 구조에 형태는 맞지만 첼시 공식전 0경기.',
 'LOW — 이라올라 체제 대상 아님.',
 'SofaScore player 1010421; https://www.chelseafc.com/en/news/article/pep-chavarria-signs-for-chelsea; reports/transfer-watch/2026-08-13.md',
 'HIGH 라요 실측 / LOW 첼시 실행','2026-08-13',NULL),
(3,85,'A- — 우측 센터백 22경기 실측 .908로 리버풀의 공격적 RCB 요구에 높은 공간 적합을 보인다. 다만 리버풀 공식전은 아직 0경기다.',
 '전진 스텝아웃과 공격적 경합, 우측에서의 배급이 중심인 볼 플레잉 센터백.',
 '강점은 RCB 역할 적합과 상위 수준 경합. 약점은 좌측 재배치 적합 급락과 최근 가용성 맥락이다.',
 '수집 58경기 2,084분 평균 6.90, 듀얼승 2.31/경기. 45분+ 바르셀로나 RCB 22경기 평균 7.15, cb_bpd/Aggressive .908.',
 'LOW — 에메리 체제 대상 아님.',
 'LOW — 알론소 체제 대상 아님.',
 'MEDIUM-HIGH — 이라올라의 전방지향 RCB와 공간 적합. 리버풀 실행은 미검증.',
 'SofaScore player 925097; https://www.liverpoolfc.com/news/liverpool-agree-deal-sign-ronald-araujo-loan; reports/transfer-watch/2026-08-12.md',
 'HIGH 바르셀로나 실측 / LOW 리버풀 실행','2026-08-13',NULL),
(3,88,'B+ — 오사수나 34경기 7골 5도움의 즉시 전력 윙어. 좌우를 분리하면 두 측면 모두 유효하지만 리버풀의 우측 결손을 메우는지는 새 팀 공식전이 필요하다.',
 '폭발적 속도, 직접 드리블, 양측면 전환, 수비 복귀를 겸한 와이드 공격수.',
 '강점은 양쪽 윙과 1대1 돌파. 약점은 좌우 혼합 시 위치 데이터가 무의미해지고 강팀 점유 구조에서 같은 공간을 쓸지 미정이라는 점.',
 'Liverpool 공식 프로필 기준 오사수나 34경기 2,766분 7골 5도움. 좌 23경기 평균 7.03·LM wideplm/Attack .729, 우 11경기 RM winger/Balanced .772.',
 'LOW — 에메리 체제 대상 아님.',
 'LOW — 알론소 체제 대상 아님.',
 'MEDIUM — 이라올라의 수직 전환·와이드 압박과 특성 정합, 리버풀 공식전 0경기.',
 'SofaScore player 1145642; https://www.liverpoolfc.com/news/career-path-spain-impact-and-history-maker-get-know-victor-munoz; reports/transfer-watch/2026-08-13.md',
 'HIGH 오사수나 시즌 데이터 / LOW 리버풀 실행','2026-08-13',NULL),
(3,89,'A- — 렌 RCB 14경기 .903과 LCB 7경기 .850으로 양쪽 이동 가능한 전진 배급형 센터백. 아라우호와 .005 차라 적합만으로 주전을 정할 수 없다.',
 '공중 지배, 침착한 패스, 전진 차단을 겸한 볼 플레잉 센터백.',
 '강점은 75.5% 공중 경합 승률과 90.4% 패스 성공률, 좌우 유연성. 약점은 어깨 부상으로 시즌 표본이 21경기에 그친 점.',
 '렌 2025/26 21경기. 우측 14경기 평균 7.08·cb_bpd/Aggressive .903, 좌측 7경기 .850. 구단 Opta 요약 클리어 4.9/90·볼 회수 4.14/90.',
 'LOW — 에메리 체제 대상 아님.',
 'LOW — 알론소 체제 대상 아님.',
 'MEDIUM-HIGH — 이라올라 센터백의 전진 배급·선제 차단 요구에 정합, 리버풀 실행은 미검증.',
 'SofaScore player 1445625; https://www.liverpoolfc.com/news/jeremy-jacquet-factfile-aerial-dominance-van-dijk-respect-and-lfc-homework; reports/transfer-watch/2026-08-13.md',
 'HIGH 렌·구단 Opta 데이터 / LOW 리버풀 실행','2026-08-13',NULL);

-- 슈퍼컵 교체 5명. 45분 미만이라 시즌 대표 집계에는 쓰지 않지만 경기 리포트에는 원천 그대로 공개한다.
INSERT OR REPLACE INTO player_matches(
 player_id,event_id,match_id,team_code,season,date,opponent,venue,competition,minutes,rating,started,
 lineup_pos,pos_class,lineup_order,formation,avg_x,avg_y,possession,hit_points,cells,map25,xg,xa,
 key_passes,duels_won,duels_lost,tackles,interceptions,goals,assists,touches,recoveries,stats_json,
 role_note,source,confidence
) VALUES
(17,16260286,68,'AVL','2026-27','2026-08-12','Paris Saint-Germain','A','UEFA Super Cup',11,6.6,0,'D','LB',12,'4-2-3-1',35.51,81.81,39,15,'2,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,3,1,0,0,4,2,0,0,0','50000300003000038300X5000',NULL,NULL,0,0,0,0,0,0,0,12,2,'{"minutes":11,"rating":6.6,"key_passes":0,"pass_total":12,"pass_acc":10,"duels_won":0,"duels_lost":0,"tackles":0,"interceptions":0,"goals":0,"assists":0,"touches":12,"recoveries":2,"shots_on":0,"shots_total":0,"clearances":0,"saves":0}','79분 파우 토레스 대신 LCB 투입','SofaScore event 16260286 player heatmap/statistics/average-positions/lineups','HIGH 원천값 / LOW 역할 — 11분'),
(11,16260286,68,'AVL','2026-27','2026-08-12','Paris Saint-Germain','A','UEFA Super Cup',18,6.8,0,'M','RDM',13,'4-2-3-1',45.01,44.14,39,23,'0,0,0,0,0,0,1,3,1,1,0,0,1,5,1,0,4,0,2,0,0,1,1,2,0','0000002622002X20804002240',NULL,NULL,0,2,0,1,0,0,0,18,4,'{"minutes":18,"rating":6.8,"key_passes":0,"pass_total":13,"pass_acc":12,"duels_won":2,"duels_lost":0,"tackles":1,"interceptions":0,"goals":0,"assists":0,"touches":18,"recoveries":4,"shots_on":0,"shots_total":0,"clearances":1,"saves":0}','72분 카마라 대신 RDM 투입','SofaScore event 16260286 player heatmap/statistics/average-positions/lineups','HIGH 원천값 / LOW 역할 — 18분'),
(21,16260286,68,'AVL','2026-27','2026-08-12','Paris Saint-Germain','A','UEFA Super Cup',11,6.8,0,'M','LDM',14,'4-2-3-1',59.61,61.11,39,19,'0,2,0,0,0,1,5,2,0,0,0,1,0,3,1,2,0,2,0,0,0,0,0,0,0','040002X400020624040000000',NULL,NULL,0,2,1,1,0,0,0,18,0,'{"minutes":11,"rating":6.8,"key_passes":0,"pass_total":15,"pass_acc":15,"duels_won":2,"duels_lost":1,"tackles":1,"interceptions":0,"goals":0,"assists":0,"touches":18,"recoveries":0,"shots_on":0,"shots_total":0,"clearances":0,"saves":0}','79분 주앙 고메스 대신 LDM 투입','SofaScore event 16260286 player heatmap/statistics/average-positions/lineups','HIGH 원천값 / LOW 역할 — 11분'),
(59,16260286,68,'AVL','2026-27','2026-08-12','Paris Saint-Germain','A','UEFA Super Cup',17,6.2,0,'F','RM',15,'4-2-3-1',62.08,19.31,39,20,'0,0,1,3,2,0,0,0,2,4,0,0,0,2,3,0,0,0,0,1,0,0,0,0,2','003850005X000580000300005',NULL,NULL,0,2,1,1,0,0,0,18,2,'{"minutes":17,"rating":6.2,"key_passes":0,"pass_total":14,"pass_acc":9,"duels_won":2,"duels_lost":1,"tackles":1,"interceptions":0,"goals":0,"assists":0,"touches":18,"recoveries":2,"shots_on":0,"shots_total":0,"clearances":0,"saves":0}','73분 맥긴 대신 RM 투입','SofaScore event 16260286 player heatmap/statistics/average-positions/lineups','HIGH 원천값 / LOW 역할 — 17분'),
(60,16260286,68,'AVL','2026-27','2026-08-12','Paris Saint-Germain','A','UEFA Super Cup',18,6.6,0,'F','ST',16,'4-2-3-1',64.94,40.66,39,9,'0,1,0,0,1,0,1,1,1,0,0,1,0,1,2,0,0,0,0,0,0,0,0,0,0','05005055500505X0000000000',NULL,NULL,0,1,1,0,0,0,0,7,0,'{"minutes":18,"rating":6.6,"key_passes":0,"pass_total":7,"pass_acc":5,"duels_won":1,"duels_lost":1,"tackles":0,"interceptions":0,"goals":0,"assists":0,"touches":7,"recoveries":0,"shots_on":0,"shots_total":0,"clearances":0,"saves":0}','72분 Madjo 대신 ST 투입','SofaScore event 16260286 player heatmap/statistics/average-positions/lineups','HIGH 원천값 / VERY LOW 역할 — 히트포인트 9');

INSERT OR REPLACE INTO match_player_reports VALUES
(1,17,'SUB LCB','79분 파우 토레스 대신 투입된 좌측 센터백','종료 국면에서 좌측 후방과 터치라인 쪽을 커버','11분, 10/12패스, 12터치, 2회수, 평점 6.6. 실점 없이 종료했으나 짧은 표본','종료 XI LCB cb_wideback/Aggressive .794; 히트포인트 15 경계 표본','SofaScore event 16260286; reports/match-watch/2026-08-12-avl-psg-super-cup.md','HIGH 스탯 / LOW 역할 — 11분'),
(1,11,'SUB RDM','72분 카마라 대신 투입된 우측 피벗','열세 추격에서 중앙 순환과 회수를 유지','18분, 12/13패스, 2/2경합, 1태클, 4회수, 평점 6.8','종료 XI RDM dm_dlp/Roaming .722; 대표 처방에는 반영하지 않음','SofaScore event 16260286; reports/match-watch/2026-08-12-avl-psg-super-cup.md','HIGH 스탯 / LOW 역할 — 18분'),
(1,21,'SUB LDM','79분 주앙 고메스 대신 투입된 좌측 피벗','높아진 라인 뒤에서 좌중앙 패스 순환','11분, 15/15패스, 2/3경합, 1태클, 18터치, 평점 6.8','종료 XI LDM dm_dlp/Roaming .466; 짧은 표본이라 유사도 해석 금지','SofaScore event 16260286; reports/match-watch/2026-08-12-avl-psg-super-cup.md','HIGH 스탯 / LOW 역할 — 11분'),
(1,59,'SUB RM','73분 맥긴 대신 투입된 우측 와이드 공격수','우측 폭과 전진 출구를 이어받았으나 창출량은 제한','17분, 9/14패스, 2/3경합, 1태클, 2회수, 평점 6.2','종료 XI RM wm_widemid/Build-Up .765; 공격형 대표 처방으로 승격하지 않음','SofaScore event 16260286; reports/match-watch/2026-08-12-avl-psg-super-cup.md','HIGH 스탯 / LOW 역할 — 17분'),
(1,60,'SUB ST','72분 Madjo 대신 투입된 스트라이커','추격 국면의 중앙 표적과 크로스 도착점','18분, 5/7패스, 1/2경합, 7터치, 슈팅 0, 평점 6.6','종료 XI ST st_false9/Build-Up .493은 히트포인트 9라 표시만 하고 판정에는 사용하지 않음','SofaScore event 16260286; reports/match-watch/2026-08-12-avl-psg-super-cup.md','HIGH 스탯 / VERY LOW 역할 — 히트포인트 9');

ALTER TABLE match_player_prescriptions ADD COLUMN replaced_player_id INTEGER REFERENCES players(id);
ALTER TABLE match_player_prescriptions ADD COLUMN minute_on INTEGER;

INSERT OR REPLACE INTO match_player_prescriptions(
 report_id,player_id,game_version,pos_label,role_id,focus,fit_sim,starter,sort_order,
 rationale,source,confidence,replaced_player_id,minute_on
) VALUES
(1,17,'FC26','LCB','cb_wideback','Aggressive',0.794,0,12,'79분 파우 토레스 교체 후 종료 XI의 좌측 수비 위치를 재현.','SofaScore event 16260286 player heatmap/statistics','LOW 게임 번역 — 11분·히트포인트 15',4,79),
(1,11,'FC26','RDM','dm_dlp','Roaming',0.722,0,13,'72분 카마라 교체 후 중앙 순환·회수 위치를 재현.','SofaScore event 16260286 player heatmap/statistics','LOW 게임 번역 — 18분',12,72),
(1,21,'FC26','LDM','dm_dlp','Roaming',0.466,0,14,'79분 주앙 고메스 교체 후 좌중앙 패스 순환 위치를 재현.','SofaScore event 16260286 player heatmap/statistics','VERY LOW 게임 번역 — 11분',56,79),
(1,59,'FC26','RM','wm_widemid','Build-Up',0.765,0,15,'73분 맥긴 교체 후 우측 폭·전진 출구를 재현.','SofaScore event 16260286 player heatmap/statistics','LOW 게임 번역 — 17분',10,73),
(1,60,'FC26','ST','st_false9','Build-Up',0.493,0,16,'72분 Madjo 교체 후 짧은 연결 위치를 표시. 히트포인트 9라 역할 판정에는 사용하지 않는다.','SofaScore event 16260286 player heatmap/statistics','VERY LOW 게임 번역 — 18분·히트포인트 9',61,72);

UPDATE match_reports
SET tactical_changes=tactical_changes || '|72~79분 Bogarde·Abraham·Alysson·Mings·Barkley 5명을 투입해 종료 XI로 전환',
    game_implications=game_implications || '|교체 5명은 경기 전용 종료 XI에서만 바꿔 볼 수 있으며 45분 미만 표본을 시즌 대표 처방에 합산하지 않음',
    updated_at='2026-08-13'
WHERE id=1;

INSERT OR IGNORE INTO _migration_log VALUES(
 '014-player-analysis-provenance-and-supercup-subs','2026-08-13',
 '선수 분석 관찰 기간·표본 범위, 현재 스쿼드 누락 분석/평가, 슈퍼컵 교체 5명 원천·리포트·종료 XI 처방 보강'
);
COMMIT;
