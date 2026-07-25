-- 2026-07-24 왓킨스+잭슨 투톱 4-2-2-2 예측 세팅 (team_tactic_setups 백킹)
-- 툴 프리셋 '아스톤 빌라 26/27 (투톱)'의 DB 근거. 실측 아님 = 예측(what-if).
BEGIN;
INSERT INTO team_tactic_setups(season,game_version,kind,formation,build_up_style,defensive_approach,line_height,tactic_code,rationale,confidence) VALUES
('2026-27','FC26','projected:2up-4222','4-2-2-2','Short Passing','Balanced',52,'',
 '왓킨스+잭슨 투톱 예측(실측 아님). 26/27 projected 셸 유지 + 2번째 스트라이커 수용. 포메이션 근거: 빌라 포메이션 상수(4-2-3-1 41/45)의 투톱 예외가 4-2-2-2 ×1(번리 H)·4-4-2 ×3(본머스H·리즈A·첼시A) — 더블 피봇(고메스·카마라 dm_holding)을 보존하려면 4-2-2-2, 두 줄 4 뱅크/리드관리엔 4-4-2. 역할 스태거(핵심): 왓킨스 st_advanced/Attack(최전방 박스 피니셔+좌채널 배후, measured x41 좌편향·xg1.33·xa.03) / 잭슨 st_advanced/Support(하강 링크·양채널·전방압박, transfer_targets id123 실측 fit .752·x48). 2선=가르나초 wm_insidefwd/Attack(좌 내향)+로저스 cam_playmaker/Roaming(중앙 공급). 폭=풀백 전담(에메리 한 번에 한 명, 캐시 Balanced rest-defense/에스투피냔 Support), 배후 리스크는 파우 스텝업+마르티네스 스위퍼로 상쇄. 수비 국면은 4-4-2 미드블록으로 회귀(기존 셸 정합). 툴 에메리구조 87(vs 4-2-3-1 예상 93)=구조 이탈 정량화. 대안 프리셋: 4-4-2(맥긴 RM·가르나초 LM wm_widemid/Support + 카마라·로저스 중앙 페어).',
 'QUALITATIVE — 예측(what-if) 세팅. 포메이션 상수 예외·에메리 커리어 4-4-2 DNA·잭슨 실측 st_advanced/Support(.752)·왓킨스 measured st_advanced에 근거. 리스크: 두 스트라이커 동시 드롭 시 박스 공동화, 무윙어 폭 부재. 시즌 실측으로 검증 예정.');
COMMIT;
