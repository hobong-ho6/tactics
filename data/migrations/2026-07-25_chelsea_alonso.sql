-- 2026-07-25 첼시 26/27 (알론소) — 레버쿠젠 블루프린트 이식 (참조 구현, 최종 5-4-1)
-- 툴 프리셋 '첼시 26/27 (알론소)'의 DB 백킹 + 빌라 투톱 프리셋 로저스 정합성 수정.
BEGIN;

-- 1) team_tactic_setups — 알론소 첼시 참조 세팅 (인게임 5-4-1 최종)
INSERT INTO team_tactic_setups(season,game_version,kind,formation,build_up_style,defensive_approach,line_height,tactic_code,rationale,confidence) VALUES
('2026-27','FC26','reference:chelsea-alonso','5-4-1','Short Passing','High',64,'',
 '알론소 레버쿠젠 블루프린트의 첼시 이식(참조 구현, 실측 아님). 부임 2026-05-17 발표·07-01 4년(첼시 공식/ESPN). 개념 골격: 3-4-2-1 스캐폴드 → 공격 3-2-5(5채널 오버로드)·수비 백5. ★FC26 슬롯 제약으로 인게임 포메이션은 5-4-1 채택: 3-4-2-1은 와이드=WM(윙백 역할 선택 불가)·중앙 2미들=CM이라 그리말도/프림퐁 윙백 역할 재현 불가 → 백5(FB 슬롯, fb_inverted/fb_att_wb 사용 가능)+4미드+1톱인 5-4-1이 정확 매핑(수비 국면 백5와도 일치, 공격 3-2-5 전개는 역할 커널 담당). 택티컬 비전=포제션(구 티키타카 — 볼 통제·중앙 지향 빌드업 정합; High Pressing 비전은 다이렉트 지향이라 부적합, 카운터프레스는 수비접근 High+라인 64로 구현). XI(스쿼드 2026-07-25 — 로저스£117m·팔레스트라£43m·퀜다£40m·에메가£22m IN / 쿠쿠레야·A.산투스·T.조지·가르나초(빌라 임대) OUT): 산체스 gk_ballplaying/Build-Up — 콜윌(LCB) cb_bpd/Aggressive(인카피에: 좌 전진 스텝) · 아다라비오요(CB) cb_bpd/Build-Up(타: 중앙 지휘·롱 대각) · 포파나(RCB) cb_wideback/Support(탑소바/코수누: 빌드업 시 와이드 이탈+볼캐리) — 아토(LWB) fb_inverted/Build-Up(그리말도: 딥→대각 내향 플레이메이커) · 팔레스트라(RWB) fb_att_wb/Attack(프림퐁: 터치라인 하이 윙어) — 엔소(LCM) cm_dlp/Build-Up(샤카 오케스트레이터) · 카이세도(RCM) cm_holding/Ball-Winning(팔라시오스 볼위너) — 로저스(LM) wm_wideplm/Attack(비르츠: 좌 하프스페이스 창조 — 빌라 실측 roaming 창조성 승계) · 팔머(RM) wm_insidefwd/Attack(호프만: 우 하프스페이스 득점 커넥터) — 주앙 페드루(ST) st_advanced/Support(보니페이스: 드롭 링크+카운터프레스 선봉). 비대칭 윙백=시스템 축(그리말도 yin/프림퐁 yang). 구조 리스크: 쿠쿠레야 매각으로 그리말도 롤 적임자 아토뿐(백3 좌측 겸직 불가), 중앙 상실 시 취약(레버쿠젠 동일). 로테이션: 제임스 RWB/RCB·에스테방/퀜다 RM·RWB·라비아/에수구 피봇·델랍/에메가 st_target·지튼스 LM·잭슨(빌라行 HIGH, XI 제외). 에메리 빌라(4-2-3-1 Balanced/52)와 대비: 5-4-1 High/64. 툴 프리셋 첼시 26/27 (알론소)와 계약.',
 'QUALITATIVE — 블루프린트 이식(첼시 실전 실측 아님). 레버쿠젠 전술은 themastermindsite·ac3lab·soccertutor·managingmadrid·bulinews 교차(2026-07-25 수집), 스쿼드는 Wikipedia 2026-27 Chelsea season + 첼시 공식 이적 페이지, FC26 슬롯 제약·비전 목록은 EA 커뮤니티 가이드(dexerto/beebom) 확인. 알론소가 첼시에서 레버쿠젠 골격을 그대로 쓸지는 미확인 — 시즌 개막 후 실측 검증 예정.');

-- 2) tactic_observations — 알론소 블루프린트 참조 기록 (래시포드 선례와 동일 scope=reference 형식)
INSERT INTO tactic_observations(season,scope,claim,evidence,source,confidence) VALUES
('2026-27','reference',
 '알론소 첼시 부임(2026-07-01) — 레버쿠젠 3-4-2-1 블루프린트의 첼시 이식 참조 분석(인게임 5-4-1). 빌라 상대 분석·이적 평가(로저스 매각처, 가르나초 임대 원클럽, 잭슨 협상 상대)의 컨텍스트.',
 '레버쿠젠 핵심(23/24 무패 더블): ①3-4-2-1→공격 3-2-5·수비 백5 ②중앙 지향 빌드업+비대칭 윙백(그리말도 딥 인버트/프림퐁 하이 윙어, 코수누 와이드 이탈로 4-2-4화) ③샤카 오케스트레이터(빌드업 관여 145회 1위)+팔라시오스 볼위너 ④2×10 비르츠(좌 로머)+호프만(우 커넥터) ⑤보니페이스 압박 선봉+링크 ⑥하이라인+즉시 카운터프레스(22/23 미드블록에서 진화) ⑦third-man 콤비네이션·좌측 삼각. 첼시 매핑(최종): 팔레스트라=프림퐁(RWB fb_att_wb/Attack), 아토=그리말도(LWB fb_inverted/Build-Up — 쿠쿠레야 매각으로 유일 적임=구조 최약 슬롯), 엔소=샤카(LCM cm_dlp), 카이세도=팔라시오스(RCM cm_holding), 로저스=비르츠(LM wm_wideplm/Attack), 팔머=호프만(RM wm_insidefwd/Attack), 주앙 페드루=보니페이스(st_advanced/Support). FC26 제약: 3-4-2-1 와이드=WM 슬롯이라 윙백 역할 불가 → 인게임 5-4-1 채택. 첼시 25/26 10위→마레스카·로제니어 경질 후 부임.',
 'https://www.chelseafc.com/en/news/article/xabi-alonso-appointed-chelsea-manager ; https://en.wikipedia.org/wiki/2026%E2%80%9327_Chelsea_F.C._season ; https://themastermindsite.com/2023/09/08/xabi-alonso-bayer-leverkusen-tactical-analysis-2023-24/ ; https://ac3lab.github.io/blog/2024/post_leverkusen_1_en/ ; https://www.soccertutor.com/blogs/inside-football-coaching/xabi-alonso-tactics-bayer-leverkusen-3-2-5-attacking-shape-wing-back-threat ; https://www.managingmadrid.com/2025/5/26/24436704/xabi-alonsos-leverkusen-his-tactical-masterpiece-explained-before-the-madrid-era-begins (2026-07-25 수집)',
 'HIGH(레버쿠젠 전술 — 다수 분석 교차)·HIGH(부임·스쿼드 — 공식/위키) / QUALITATIVE(첼시 이식 예측 자체)');

-- 3) 빌라 투톱 프리셋 정합성 수정 — 로저스는 첼시 매각(£117m)이므로 2선 공급책=만잠비로 교체
UPDATE team_tactic_setups
SET rationale = REPLACE(rationale,
  '2선=가르나초 wm_insidefwd/Attack(좌 내향)+로저스 cam_playmaker/Roaming(중앙 공급)',
  '2선=가르나초 wm_insidefwd/Attack(좌 내향)+만잠비 cam_halfwinger/Balanced(중앙 공급 — 로저스는 첼시 매각 £117m, 2026-07-25 정정)')
WHERE kind='projected:2up-4222' AND season='2026-27';

COMMIT;
