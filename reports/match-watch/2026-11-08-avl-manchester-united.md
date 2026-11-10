# 2026-11-08 Manchester United vs AVL — 4-4 (빌라 원정 무)

> 수집일 2026-11-09(경기 다음 날 · 주간 예약 회차 `match-watch-weekly` · D+1) · SofaScore event `16363918` · FotMob `5795512` · WhoScored `1983850`
> 프리미어리그 10라운드 · 올드 트래퍼드 · 빌라 원정 · 양 팀 4-2-3-1
> 감독: 맨유 **마이클 캐릭** · 빌라 **우나이 에메리** · 게임 버전 `core.game_version.live_on('2026-11-08')` = **FC27**
> 관전 메모: 없음(`reports/match-watch/notes/`에 이 경기 파일 없음) — 가설 대조표 생략

## 요약

- **4-2로 85분을 앞서다 90+2′·90+6′에 실점해 4-4.** xG 2.88–3.55(FotMob · PK 각 1) · 점유 44% · 슈팅 12–26 · 유효 6–9 · 맨유 박스 터치 48(빌라 18).
- **빌라 득점은 거의 세트피스·PK였다**: 빌라 xG 2.88 중 오픈플레이 0.38뿐 — 세트 1.71(4′ 잭슨·53′ 고레츠카 모두 맥긴 프리킥 뒤 혼전) + PK 0.79(48′ 맥긴 · 알리송 획득). 오픈플레이 득점은 1′ 알리송(스로인 → 맥긴 키패스) 하나.
- **수비 높이가 이번 시즌 공식전 최저권**: 수비 액션 평균 높이(def_x) 31.2(맨유 43.8) · 비보유 4-4-1-1에 맥긴이 앞줄(수비 동작 평균 높이 52). 맨유 크로스 30개(빌라 왼쪽에서 17 · 오른쪽에서 13).
- **보유 땐 오른쪽 풀백이 남는 3백**: 하우드-벨리스(PL 첫 선발 · 캐시 경고 누적 정지) WS 볼 터치 평균 위치(앞뒤, 좌우 · 0~100 · 좌우 0 = 빌라 오른쪽) (33,18) · 마첸 (47,87). Tanswell 워밍업 관찰 「the RB tucking in and the LB pushing high」(RB가 안으로 좁히고 LB가 높이 올라간다)와 일치.
- **마지막 두 실점은 빌라 오른쪽·GK**: 90+2′ 헤븐이 고메스를 제치고 얻은 프리킥 → 빠른 재개 → 도르구 크로스(빌라 오른쪽) → 지르크제이 · 90+6′ 코너 → 람먼스가 스즈키를 막는 사이 도르구 헤더(Opta: 스즈키 실수). 에메리 「with Dorgu left side, we couldn't defend him good」(도르구 쪽을 잘 막지 못했다).
- **게임 구현: 추가 관찰.** 경기 프리셋 4-2-3-1 Wide · Balanced/Deep/35(DIVERGE — PPDA 13.5는 압박이 아니라 맨유의 빌라 진영 점유 결과). 정본 변경 없음.

## 1. 경기 개요와 원천 수치

| 지표 | 맨유 | 빌라 | 출처 |
|---|---|---|---|
| 점유 | 56% | 44% | SofaScore·FotMob 동일 |
| xG(전체 / 오픈플레이 / 세트 / 논PK / xGOT) | 3.55 / 2.36 / 0.40 / 2.76 / 4.39 | 2.88 / 0.38 / 1.71 / 2.09 / 2.63 | FotMob 한 응답(동일 스냅샷) · SofaScore xG도 같은 값 |
| 슈팅(유효) · 빅찬스 | 26(9) · 6 | 12(6) · 5 | SofaScore |
| 패스(성공) | 502(438) | 410(347) | SofaScore |
| 롱볼 | 19/33 | 19/46 | SofaScore |
| 크로스 | 5/30 | 2/5 | SofaScore |
| 경합 · 공중 · 드리블 | 51% · 9/22 · 8/13 | 49% · 13/22 · 8/21 | SofaScore |
| 태클 · 인터셉트 · 클리어 | 26 · 12 · 12 | 11 · 12 · 36 | SofaScore |
| 코너 · 파울 · 경고 | 8 · 18 · 1 | 1 · 9 · 1 | SofaScore |
| PPDA | 9.21(350/38) | 13.5(297/22) | core.whoscored.ppda · WS 1983850 |
| 수비 액션 평균 높이(def_x) | 43.8 | **31.2** | core.whoscored.수비 액션 평균 높이(def_x) |
| 실점으로 이어진 실수 | 1(요로 53′) | 1(스즈키 90+6′) | SofaScore · Opta Error |

- 하프별(FotMob): 전반 점유 48% · xG 1.25–1.69 · 슈팅 6–12 / 후반 점유 40% · xG 1.63–1.86 · 슈팅 6–14. 하프별 PPDA(빌라·맨유) 전반 16.56·10.25 · 후반 11.38·8.06.
- 득점 국면(SofaScore 국면 분): 빌라 리드 85분 · 동점 5분 · 열세 0분.
- 교체: 맨유 46′ 매과이어→헤븐 · 66′ 아마드→라시 · 달롯→도르구 · 틸레만스→마운트 · 83′ 음뵈모→지르크제이. 빌라 71′ 알리송→바클리(CAM) · 맥긴→헤밍스(RM) · 78′ 고레츠카→고메스(LDM) · 만잠비→음바예(LM) · 86′ 잭슨→마조. (교체 짝은 SofaScore incidents · 들어간 자리는 WS formations.)
- 경고: 헤븐 57′ · 스즈키 90+7′(항의).
- 결장: 캐시(경고 5장 누적 1경기 정지 · AVFC 「in place of the suspended Matty Cash」) · 완비사카(허벅지 · 출전 불투명) · 오나나(십자인대) · 루제리(햄스트링).
- 수집: SofaScore `/event/16363918{,/statistics,/incidents,/shotmap,/lineups,/managers,/graph,/average-positions}`(headless 기본 UA 200) · FotMob matchDetails 5795512(페이지 안 fetch) · WhoScored matchCentreData 1983850 **scope=full 1,567건** → `reports/match-watch/data/2026-11-08-avl-ws-1983850.json` 보존. 출전 16명 전원 SofaScore 평균 위치·히트맵 있음.

## 2. 전술 설명

### 점유 구조·빌드업

- 보유 형태는 **3-2-5에 가까웠다.** WS 볼 터치 평균 위치(앞뒤, 좌우 · 0~100 · 좌우 0 = 빌라 오른쪽): 하우드-벨리스 (33,18) · 린델뢰프 (28,37) · 토레스 (28,73) · 카마라 (37,39) · 고레츠카 (40,52) · 마첸 (47,87) · 만잠비 (52,68) · 맥긴 (54,35) · 알리송 (54,21) · 잭슨 (61,69).
- 오른쪽 풀백이 남고 왼쪽 풀백이 올라갔다. 하우드-벨리스는 마첸보다 14 낮고 터치라인에서 5 더 안쪽이다. Tanswell 워밍업 관찰(3백 · 오른쪽 하우드-벨리스)과 맞는다.
- 후방 순환은 GK–왼쪽 CB 축. 패스 연결 스즈키→토레스 18회 · 토레스→스즈키 18회 · 린델뢰프→하우드-벨리스 12회 · 토레스→린델뢰프 10회 · 마첸→토레스 10회.
- 잭슨은 왼쪽 채널에서 받았다(WS 볼 터치 좌우 69 · SofaScore 포지션 분류 LAM). 볼 터치 30개로 고립됐고 경합 1-4.
- 롱볼은 후반에 늘었다(전반 패스 243 중 22 → 후반 189 중 31). 스즈키 롱볼 10/23.

### 비보유 구조·압박

- **4-4-1-1 깊은 블록.** 수비 동작 평균 높이(71분 전): 맥긴 52 · 만잠비 43 · 알리송 40 · 고레츠카 31 · 카마라 28 · 하우드-벨리스 23 · 린델뢰프 18 · 토레스 13. 잭슨은 수비 동작 2개.
- 수비 액션 평균 높이(def_x) 31.2는 이번 시즌 공식전 최저권이다(바르셀로나 원정 38.1 · 맨시티 리드 구간 31.8~32.2와 같은 층).
- 맨유는 전반 빌라 왼쪽을 팠다. 빌라 진영 3분의 1 맨유 볼 터치(66분 전): 빌라 왼쪽 91 · 중앙 29 · 오른쪽 60. 44′ 동점골도 마즈라위–아마드가 빌라 왼쪽에서 만든 컷백이었다.
- 66′ 교체 뒤 방향이 바뀌었다(66분 뒤: 왼쪽 26 · 중앙 21 · 오른쪽 32). 도르구·라시가 들어와 빌라 오른쪽(하우드-벨리스·헤밍스 쪽)을 공략했고, 마지막 두 골 모두 그 흐름에서 나왔다.

### 전환·rest-defense·세트피스

- 16′ PK는 빌라 빌드업 볼 상실에서 시작했다: 토레스 패스가 중원에서 끊김(요로 인터셉트) → 틸레만스 → 마이누 → 쿠냐가 하우드-벨리스를 제치고 박스 진입 → 카마라 파울.
- 빌라 공격 세트피스가 경기를 결정할 뻔했다. 맥긴 프리킥 2개(3′·52′)가 각각 리바운드 골(잭슨·고레츠카)로 이어졌다. 세트 xG 1.71.
- 세트 수비는 무너졌다. 맨유 코너 8개 · 마지막 실점은 코너 → GK 앞 블로킹. 에메리 「if we were focusing on how the 'keeper needs protecting, we would defend it」(키퍼 보호에 집중했다면 막았을 것).

## 3. 전술적 특성

- **강점**: 세트피스 공격(맥긴 킥 → 2골) · 이른 리드(4′ 2-0) · 하프타임 뒤 재정비(46–53′ 2골 · 에메리 「control the game like we planned … in the dressing room」(라커룸에서 계획한 대로 통제했다)) · 공중 경합 13/22.
- **약점**: 오픈플레이 창출 부족(xG 0.38) · 깊은 블록 지속(맨유 슈팅 26 · 크로스 30) · 세트 수비와 GK 보호 · 리드 막판 관리(각 하프 마지막 10분 실점 — 맥긴 「In the last 10 minutes of each half, we have to manage better.」(각 하프 마지막 10분을 더 잘 관리해야 한다)).
- **상대가 만든 교란**: 캐릭의 맨유가 PPDA 9.21로 빌라 빌드업을 압박했고(16′ PK 출발점), 66′ 3명 교체로 공략 방향을 빌라 왼쪽 → 오른쪽으로 옮겼다.
- **기존 프로필·직전 경기와 비교**: 선발은 풀럼전(10-31)과 같은 구성에 RB만 캐시 → 하우드-벨리스. 리드 뒤 실점은 이번 시즌 PL 세 번째(브렌트포드 2-1→2-2 · 풀럼 1-0→1-1 · 이번 4-2→4-4)이고, 토트넘전(3-0→3-2)까지 넣으면 리드 막판 실점은 네 경기째다.

## 4. 경기 중 변화

1. **0–4′ 빌라 2골**: 1′ 마첸 스로인 → 고레츠카·만잠비 짧은 연결 → 맥긴 키패스 → 알리송 · 3′ 맥긴 프리킥 → 리바운드 → 알리송 슈팅 선방 → 잭슨.
2. **5–44′ 맨유 압박 · 빌라 하강**: 16′ PK(카마라) · 빌라 수비 액션 평균 높이(def_x) 16–30분 15.6. 맨유가 빌라 왼쪽에서 크로스·컷백을 반복 → 44′ 틸레만스.
3. **45–53′ 후반 출발 · 빌라 2골**: 하프타임 뒤 빌라가 후방 10패스 빌드업 → 하우드-벨리스 롱패스 → 알리송 PK 획득(48′ 맥긴) · 52′ 맥긴 프리킥 → 요로 실수 → 고레츠카.
4. **54–70′ 맨유 반격**: 66′ 맨유 3명 교체(라시·도르구·마운트). 모멘텀 59–81′ 맨유 우세(SofaScore 그래프). 빌라 볼 점유 15분 창 60–75′ 36%.
5. **71–86′ 빌라 교체**: 71′ 바클리 CAM·헤밍스 RM · 78′ 고메스 LDM·음바예 LM(만잠비는 73′ 요로 태클 뒤 통증 — watson.ch) · 86′ 마조 ST. 75–90′ 빌라 볼 점유 54%로 오히려 공을 더 가졌다.
6. **90+2′·90+6′ 실점**: 헤븐 돌파(고메스 챌린지 실패) → 하우드-벨리스 파울 → 브루노 빠른 프리킥 → 도르구 크로스 → 지르크제이 · 라시 크로스 → 마운트 헤더 → 하우드-벨리스 클리어로 코너 → 브루노 코너 → 도르구 헤더.

## 5. 선수별 분석 — 출전 선수 전원

좌표: SS 평균 위치(앞뒤, 좌우 · 0~100 · 좌우 0 = 빌라 오른쪽).

| 선수 | 위치·실제 역할 | 분/평점·핵심 스탯 | 평균 위치 | 특성·수행 | FC 역할/포커스 함의 |
|---|---|---|---|---|---|
| 스즈키 | GK · 롱볼 혼합 | 90 · 7.8 · 선방 5 · 패스 37/50 · 롱볼 10/23 · 90+7′ 경고 | SS 평균 위치 (8,50) | 선방은 많았지만 90+6′ 코너에서 람먼스 블로킹 속 실수(Opta Error). 에메리 「adaptation for Suzuki」(스즈키의 적응 문제) | 1위 gk_goalkeeper/Defend(Δ.009 무결정) · 정본 gk_ballplaying/Build-Up |
| 하우드-벨리스 | RB · 보유 땐 3백 오른쪽 | 90 · 6.6 · 클리어 7 · 패스 38/42 · 라인 브레이킹 패스 10 | SS 평균 위치 (31,20) | PL 첫 선발. 16′ 쿠냐에게 제쳐짐 · 90+2′ 실점 프리킥 허용 | 1위 fb_fullback/Balanced(Δ.020 무결정) · 정본 fb_wingback/Balanced .743 |
| 린델뢰프 | RCB | 90 · 6.1 · 인터셉트 5 · 클리어 8 · 패스 46/52 | SS 평균 위치 (27,37) | 친정 경기. 뒤에서 오른쪽 순환 | 1위 cb_bpd/Aggressive(Δ.025 무결정) = 정본 |
| 파우 토레스 | LCB · 순환 축 | 90 · 6.5 · 클리어 11 · 패스 54/64 · 라인 브레이킹 15 | SS 평균 위치 (28,72) | 스즈키와 36회 주고받음. 16′ 중원 패스 차단이 PK 출발 | 1위 cb_bpd/Aggressive(Δ.012 무결정) · 정본 cb_bpd/Build-Up |
| 마첸 | LB · 왼쪽 폭 · 높게 | 90 · 6.2 · 태클 3 · 패스 22/24 | SS 평균 위치 (44,86) | 아마드·마즈라위 상대로 고전(AVN). 1′ 스로인이 선제골 시작 | 1위 fb_att_wb/Support(Δ.043 무결정) = 정본 |
| 카마라 | RDM · 깊은 홀딩 | 90 · 5.9 · 경합 8-8 · 태클 3 · 돌파 허용 2 · PK 허용 | SS 평균 위치 (36,39) | 16′ 쿠냐에게 PK. 수비 동작 평균 높이 28 | 1위 dm_holding/Defend(Δ.064) = 정본 |
| 고레츠카 | LDM · 연결 + 늦은 침투 | 78 · 6.5 · 골 1 · 패스 36/37 · 경합 1-5 · 파울 4 | SS 평균 위치 (38,54) | 빌라 8경기 만의 첫 골(세트피스 리바운드) | 1위 dm_holding/Defend(Δ.001 무결정) · 정본 dm_dlp/Roaming .759 |
| 알리송 | RM · 터치라인 + 박스 침투 | 71 · 7.9 · 골 1 · PK 획득 · 슈팅 3 · 박스 터치 6 | SS 평균 위치 (52,21) | 1′ 골 · 4′ 잭슨 골 기점 슈팅 · 48′ PK 획득 | 1위 wm_widemid/Support(Δ.018 무결정) · 정본 wm_winger/Attack .499 |
| 맥긴 | CAM · 압박 선봉 + 킥 | 71 · 7.6 · 골 1(PK) · 도움 1 · 키패스 2 · 볼 손실 12 | SS 평균 위치 (52,37) | 1′ 도움 · 프리킥 2개가 2골 · 비보유 앞줄(수비 동작 평균 높이 52) | 1위 cam_playmaker/Balanced(Δ.053) · 정본 cam_playmaker/Roaming .559 |
| 만잠비 | LM · 왼쪽 안쪽 | 78 · 7.6 · 경합 13-5 · 드리블 3/5 · xA 0.29 · 패스 19/20 | SS 평균 위치 (49,66) | 왼쪽 수비 가담(수비 동작 19). 73′ 요로 태클 뒤 통증 → 78′ 교체 | 1위 wm_wideplm/Build-Up(Δ.014 무결정) · 정본 wm_insidefwd/Balanced .450 |
| 잭슨 | ST · 왼쪽 채널 수신 | 86 · 6.7 · 골 1 · 도움 1 · xG 1.30 · 경합 1-4 | SS 평균 위치 (60,69) | 4′ 리바운드 골 · 53′ 고레츠카 골 기점 슈팅. 오픈플레이 고립 | 1위 st_advanced/Support(Δ.077) = 정본 |
| 바클리 | 71′ · CAM | 19 · 6.5 · 슈팅 2 | SS 평균 위치 (66,58) | 맥긴 자리 | 45분 미만 — 리포트용 |
| 헤밍스 | 71′ · RM | 19 · 6.3 · 경합 2-6 · 공중 0-3 | SS 평균 위치 (54,21) | 알리송 자리. BBC 「Came on to shore things up but move didn't work」(굳히려 들어왔지만 통하지 않았다) | 45분 미만 |
| 고메스 | 78′ · LDM | 12 · 6.5 | SS 평균 위치 (55,51) | 90+2′ 헤븐 돌파 허용(실점 출발) | 45분 미만 |
| 음바예 | 78′ · LM | 12 · 6.5 · 키패스 1 | SS 평균 위치 (70,71) | 만잠비 자리 | 45분 미만 |
| 마조 | 86′ · ST | 13 · 6.4 | SS 평균 위치 (64,28) | 잭슨 자리 | 45분 미만 |

## 6. 전술 변화 판정

- **유지된 것**: 4-2-3-1 · 카마라 RDM/고레츠카 LDM(풀럼전과 같은 짝) · 알리송 선발 = 만잠비 LM(R1′ 패턴 · 부엔디아 없이 알리송 선발 3/3) · 맥긴 10번 · 세트피스 공격 창구.
- **새로 나타난 것**: ⑴ 하우드-벨리스 RB — 보유 땐 3백 오른쪽에 남았다(캐시 정지 대응) ⑵ 수비 액션 평균 높이(def_x) 31.2 — 시즌 최저권 깊이.
- **반복된 것(누적)**: 리드 막판 실점 — 이번 시즌 PL 세 번째 승점 손실(브렌트포드·풀럼·맨유). 맥긴이 「each half」를 짚었다.
- **`manager_profiles` 반영**: situational 축에 덧붙임(리드 막판 관리 · 세트 수비 GK 보호 — 감독 1차 발언). 나머지 축은 갱신 불필요(형태·역할 변화 없음).

## 7. 게임 구현 판정

- 결론: **추가 관찰**
- **이 경기 전용 팀 설정**: FC27 · 4-2-3-1 Wide · **Balanced / Deep / 35** · tactic_code 없음 · rule_note DIVERGE — `core.team_settings.suggest(점유 44, 패스 410, 롱볼 시도 46, PPDA 13.5)` → Balanced/Balanced/48~58(롱볼 11.2%). 수비 접근·라인은 수비 액션 평균 높이(def_x) 31.2를 따른다(PPDA 13.5는 맨유의 빌라 진영 점유 결과 · 빌라의 상대 진영 수비 동작 22). 보유 3-2-5 · 비보유 4-4-1-1.
- **이 경기 선발 11명**(단일 경기 커널 1위 · SofaScore 히트맵 · 무결정 = Δ≤.05):

| 슬롯 | 선수 | 역할/포커스 | fit | Δ | 2위 | 시즌 정본 |
|---|---|---|---|---|---|---|
| GK | 스즈키 | gk_goalkeeper/Defend | .962 | .009 무결정 | gk_goalkeeper/Balanced | gk_ballplaying/Build-Up |
| RB | 하우드-벨리스 | fb_fullback/Balanced | .846 | .020 무결정 | fb_fullback/Versatile | fb_wingback/Balanced |
| RCB | 린델뢰프 | cb_bpd/Aggressive | .923 | .025 무결정 | cb_bpd/Build-Up | 같음 |
| LCB | 토레스 | cb_bpd/Aggressive | .820 | .012 무결정 | cb_bpd/Build-Up | cb_bpd/Build-Up |
| LB | 마첸 | fb_att_wb/Support | .844 | .043 무결정 | fb_wingback/Balanced | 같음 |
| RDM | 카마라 | dm_holding/Defend | .905 | .064 | dm_holding/Roaming | 같음 |
| LDM | 고레츠카 | dm_holding/Defend | .801 | .001 무결정 | dm_holding/Roaming | dm_dlp/Roaming |
| RM | 알리송 | wm_widemid/Support | .601 | .018 무결정 | wm_winger/Balanced | wm_winger/Attack |
| CAM | 맥긴 | cam_playmaker/Balanced | .612 | .053 | cam_playmaker/Roaming | cam_playmaker/Roaming |
| LM | 만잠비 | wm_wideplm/Build-Up | .566 | .014 무결정 | wm_wideplm/Attack | wm_insidefwd/Balanced |
| ST | 잭슨 | st_advanced/Support | .442 | .077 | st_false9/Attack | 같음 |

- 무결정 8칸(Δ≤.05). 정본 변경 근거로 쓰지 않는다.
- **구현 함의(사용자 판단 대기 아님 — 관찰 누적)**:
  1. **RB 대체 시 「남는 풀백」** — 캐시가 없을 때 하우드-벨리스 RB는 보유 3백 오른쪽(1위 fb_fullback/Balanced). 쟁점 #13(풀백 비대칭)·#24(하우드-벨리스)에 근거로 쌓는다.
  2. **리드 막판 관리** — `optimal:lead`(라인 45) 프리셋이 있다면 깊은 블록 + 크로스 허용 위험. 쟁점 #16(리드·수세 시 하강 형태)에 근거로 쌓는다. 게임에서 리드 시 「라인 더 내리기」는 이 경기 기준으로는 실점 위험을 키운 쪽이다(1경기 · C 아님 — 실축 관찰).
  3. **세트 수비 GK 보호** — 코너 수비 인원 배치(GK 앞 블로커) 설정 근거. 에메리 1차 발언. 게임 메뉴 「코너 수비 인원」 동작은 `game_system_changes`에 미확인(#83 목록) — 근거 등급 D(통설)로만 둔다.
- 커널 1위·2위·Δ는 `match_player_prescriptions` #70 그대로.

## 8. 서사 수집(§2-1) · 레퍼런스·한계

### 감독 회견(1차)

- 에메리(AVFC 공식 · Sky · Goal · Hayters · PA):
  - 「It's difficult to accept this result because we were winning 4-2 in extra-time and how we conceded two goals is really painful.」(추가시간에 4-2로 이기고 있었기에 받아들이기 어렵고, 두 골을 내준 방식이 정말 고통스럽다)
  - 「The second half, we started very good, scoring two goals, and then we could control the game like we planned in the first half in the dressing room」(후반은 아주 좋게 시작해 두 골을 넣었고, 하프타임 라커룸에서 계획한 대로 경기를 통제할 수 있었다)
  - 「the last six minutes was really getting us upset … it's something we have to try to correct as quick as possible.」(마지막 6분이 정말 우리를 흔들었다 … 최대한 빨리 고쳐야 한다)
  - 「The last moments when we were close to finishing the match, with Dorgu left side, we couldn't defend him good.」(경기를 거의 끝내가던 마지막 순간, 맨유 왼쪽의 도르구를 잘 막지 못했다)
  - 「The last corner, normally, if we were focusing on how the 'keeper needs protecting, we would defend it.」(마지막 코너는, 키퍼를 어떻게 보호할지에 집중했다면 막았을 것이다)
  - 「How we conceded this last goal, it is adaptation for Suzuki. They are pushing and disturbing him.」(마지막 실점은 스즈키의 적응 문제다. 그들이 밀고 방해한다)
  - 「Zion is fantastic how he is performing, but there is still work to do.」(자이온은 지금 활약이 환상적이지만 아직 할 일이 있다)
  - 「We have young talented players, we need to get this mix.」(젊고 재능 있는 선수들이 있고, 이 조합을 만들어야 한다)
  - 교체 의도(71′·78′·86′) 직접 설명: **못 찾음**(AVFC·Sky·Goal·PA·Hayters·BBC).
- 캐릭(Sky): 「you take [out] the moments that are totally avoidable goals that we're giving away, I actually thought we played pretty well and were the better team for the most part」(충분히 피할 수 있었던 실점 장면을 빼면 꽤 잘했고 대부분 더 나은 팀이었다).
- 맥긴(BBC MOTD): 「In the last 10 minutes of each half, we have to manage better.」(각 하프 마지막 10분을 더 잘 관리해야 한다) · 「The third goal was really poor and gave them a lot of encouragement to score.」(세 번째 실점이 정말 형편없었고 그들에게 큰 용기를 줬다).
- 비다가니(빌라 축구운영 디렉터 · X, Sky 전재): 「Lammens did not even look at the ball, went straight to do a contact with the hip over Zion.」(람먼스는 공을 보지도 않고 곧장 엉덩이로 자이온과 접촉했다).

### Jacob Tanswell(필수 기자)

- X는 접근하지 않고 Bluesky 공개 피드로 대체(경기 중 라이브 게시 0건).
  - 「Might be a smokescreen but #AVFC warming up with three centre backs (Harwood-Bellis on the right, Lindelof central and Pau on the left) … the RB tucking in and the LB pushing high」(연막일 수도 있지만 3백으로 워밍업 … RB가 안으로 좁히고 LB가 높이 올라간다) — 실측 보유 3-2-5와 일치.
  - 「Unai Emery says he was angry after leaving the dugout before the final whistle because he "thought the game was done".」(에메리는 경기가 끝난 줄 알고 종료 전 벤치를 떠났다가 화가 났다고 말했다).
- The Athletic 기사(7764790) 본문: **미수행** — nytimes.com이 브라우저·WebFetch 모두에서 막힘.

### 필수 유튜브 3채널

| 채널 | 영상 | 게시 | 처리 |
|---|---|---|---|
| UTV | `xHOUJaTixWI` MATCH REACTION | 11-08 | 전사·요약(auto-caption) |
| 1874 | `ZlDoYo0KCe0` Bardell 경기 후 라이브 | 11-08 | 전사·요약(auto-caption) |
| UTV | `ljUxyRnkUkk` 전술 프리뷰(캐릭 체제 맨유 약점) | 11-06 | 전사·요약(채널 스윕) |
| UTV | `sTIPSGdxIq4` 워치얼롱 | 11-08 | 건너뜀(워치얼롱) |
| 1874 | `qezZkRnbHAY` 프리뷰(Bardell·Sky Reed) | 11-07 | 건너뜀(프리뷰) |
| The Villans | 경기 후 영상 | — | 수집 시점 미게시 → D+1·D+2 추적 |

### 기사·다국어

- 영어: AVFC · BBC(평점) · Sky · Goal(전술 보드 — 사실 오류 섞여 D등급) · Opta Analyst · Hayters · PA · AVN · OneFootball.
- 독일어: t-online(SID — 고레츠카 첫 골) · watson.ch(만잠비 부상 정황 「Nach einer Grätsche von Leny Yoro blieb er in der 73. Minute mit Schmerzen liegen」(73분 요로의 슬라이딩 태클 뒤 통증으로 쓰러졌다)).
- 스웨덴어: Fotbollskanalen(린델뢰프) · 포르투갈어: Placar(알리송) · 일본어: 스포니치·사커킹·풋볼채널(스즈키) · 프랑스어: Blick·Seneweb(만잠비·잭슨).
- 미수행: 에메리 **스페인어** 회견 원문(AS·Marca·EFE·Relevo 검색 결과 없음) · MEN·Guardian·Claret & Blue·7500 to Holte(검색 결과 없음) · 맨유 팬 채널(시간 배분).
- 사실 충돌: 브리프·초기 기록의 「R11」 → SofaScore roundInfo·Opta·Sky 모두 **10라운드** — 정정 반영. 몇몇 사전 XI의 「린델뢰프 RB」는 SofaScore 평균 위치(린델뢰프 오른쪽 기준 폭 37 · 하우드-벨리스 20)로 기각.

### 엔드포인트

- SofaScore `api/v1/event/16363918/*` · FotMob `api/data/matchDetails?matchId=5795512` · WhoScored `matches/1983850/live`(headful Playwright · matchCentreData).

## D+1 추적 (2026-11-09)

- 이 수집 회차가 D+1이다(경기 다음 날) — 내용은 위 §8. 경기 후 영상 2편(UTV `xHOUJaTixWI` · 1874 `ZlDoYo0KCe0`) 전사·요약·구현 주장 10행.
- 남은 것(D+2·D+3로 넘김): The Villans 경기 후 영상(미게시) · 에메리 스페인어 원문 · The Athletic 본문 · 전술 블로그(Claret & Blue 등) · 만잠비 부상 정황 후속.
- ⚠️ D+2·D+3 예약은 이 비대화형 회차에서 `create_scheduled_task`가 **사람 승인 필요**로 거부됐다 → 프롬프트 초안은 [followups/2026-11-09-pending-schedules.md](followups/2026-11-09-pending-schedules.md).

## D+1 재수집 (2026-11-09 저녁) — 유튜브 14편 실제 내용 확인

> 사용자 지시 「영상 제목만 보지 말고 실제 내용을 확인해서 분석 추가」 — 이전 회차는 워치얼롱·프리뷰를 **제목만 보고 건너뛰었다**.
> 이번 회차: 전사 14편을 브라우저 자막(json3 · 항상 뮤트)으로 받아 **처음부터 끝까지 읽고** 요약·구현 주장(23행)을 적재했다. 인용은 전부 auto-caption 전사 기준이다(인명 오인식은 출전 명단으로 교정 — 「Man Zambi」=만잠비 · 「Doggy/Delo」=도르구/달롯).
> 경기 수치 재수집: FotMob matchDetails 다시 받음 — xG 4종(3.55/2.88 · 오픈플레이 2.36/0.38 · 세트 0.40/1.71 · 논PK 2.76/2.09 · xGOT 4.39/2.63)·슈팅·유효·빅찬스·코너·차단 **전부 저장값과 같다(Opta 사후 개정 없음)**.
> D+2·D+3 예약은 11-09 대화 세션에서 등록됐다(위 D+1 절의 followups 링크 파일은 등록 뒤 지웠다).

### 확인한 영상

| 영상 | 채널 · 게시 | 종류 · 귀속 | 한 줄 결론 |
|---|---|---|---|
| `T24bW9RS5QE` | 1874 · Jacob Tanswell 출연 · 11-09 | 경기반응 · #70 | 가장 밀도 높음 — 비보유 백5 하강 부재 · 후반 피벗 추적 · 교체 해석 · 리더 공백 · 스즈키 뒤쪽 포스트 |
| `92CbtLJc1PE` | Sky · 에메리 플래시 인터뷰 · 11-08 | 감독회견 · #70 | §8 인용(기자회견)과 다른 원천 · 새 인용 5 · 교체·RB·스즈키 언급 없음 |
| `I7am7fRYBlU` | UTV 「미드필드 문제」 · 11-09 | 전술분석 · #70 | 실점 장면 화면 분석 · 고레츠카–카마라 연결 부족 |
| `sTIPSGdxIq4` | UTV 워치얼롱(2시간 28분) · 11-08 | 경기반응 · #70 | 경기 장면 약 50행 — 만잠비 부상·10명·교체·막판 오른쪽 |
| `h8szHOHY7y4` | Sky 킨·영 · 11-09 | 상대팀 · #70 | 90% 맨유 이야기 · 빌라는 막판 관리·스즈키만 |
| `wU7pgwotYKw` | Stretford Paddock(맨유 팬) · 11-08 | 상대팀 · #70 | 「높게 압박하지 않고 콤팩트하지 않은 빌라」 · 막판은 박스 투입 반복 |
| `m18IWCKfmy8` | Stephen Howson(맨유 팬) · 11-09 | 상대팀 · #70 | 「파울 → 세트 → 헤더」 · 새 정보 없음(일부 수치 리포트와 다름) |
| `qezZkRnbHAY` | 1874 프리뷰(Bardell·Sky Reed) · 11-07 | 전술분석 · #70 | 사전 예상 대조 근거 |
| `4B1McP3ZYPM` | UTV 프리뷰 · 11-05 | 전술분석 · #70 | 사전 예상 대조 근거(교체 순서 적중) |
| `ToxFiTRmpwc` | The Villans 패널 · 11-05 | 전술분석 · #70 | 제목은 구단주지만 절반이 맨유전 패널 |
| `2BJJVdFELpU` | talkSPORT 2(Bardell·Flex) · 11-06 | 경기반응 · #70 | 전술 핵심 없음 · 스코어 예측만 |
| `LlCsdRMGDNs` | UTV 에메리 야망 · 11-07 | 감독회견 · 미귀속 | 맨유전 내용 없음(구단 야망·캐러거 반박) |
| `NfPgirvAfaU` | The Villans 10R 예측 · 11-06 | 경기반응 · 미귀속 | 맨유전은 스코어 한 줄뿐 |
| `PlkX6YbUUJ8` | NBC 네빌 · 11-08 | 상대팀 · 미귀속 | 맨유 구단 일반론 · 빌라 전술 언급 없음 |

### 열린 질문에 대한 답

**⑴ 교체 의도(71′·78′·86′)** — 에메리 본인 설명은 **여전히 없다**(Sky 플래시에도 없음). 해석만 모였다:
- 만잠비는 **부상 교체 정황이 강해졌다** — UTV 워치얼롱: 72′쯤 스터드 태클 → 「Manzambi is still off the pitch. So, we've got 10 men」(만잠비가 아직 밖에 있다 — 10명이다) → 78′ 교체. 태클한 선수 이름은 말하지 않았다(watson.ch 「73′ 요로」와 시점 일치).
- 71′ 헤밍스: Tanswell은 「도르구 대응 + 볼 지키기」로 이해할 만하다고 봤고 진행자 Bardell은 반대로 「충격적」이라 했다. UTV 워치얼롱은 「Hemmings is a more containing, safer substitution」(헤밍스는 봉쇄형·안전한 교체다)로 읽었다(팬 해석 · 근거 등급 D).
- 고레츠카 78′: UTV 프리뷰(11-05)가 「Goretzka … not above 60 minutes」(고레츠카는 60분 이상은 무리) → 「ends up with Barkley and Gomez in the middle」(끝엔 바클리·고메스가 중앙)을 예상했고 순서가 맞았다 — 체력 관리 정황(1차 확인 아님).

**⑵ 하우드-벨리스 「남는 RB」** — 보유 땐 **킥오프 전부터 예상된 형태**였다. UTV 워치얼롱 진행자: 「not really to bomb on … naturally form into a three at the back … even if Cash is playing」(전진하라는 게 아니라 … 캐시가 뛰어도 원래 3백이 된다). ⇒ 캐시 공백 대응이 아니라 기존 풀백 비대칭의 연장으로 읽힌다(쟁점 #13 감시 유지).
- 비보유 쪽은 Tanswell이 짚었다 — 평소엔 알리송이 내려와 백5 미드블록을 만드는데 이번엔 4-4-2 RB 하우드-벨리스가 바깥까지 맡아 노출됐다. 실측 비보유 4-4-1-1과 일치.
- 경기 전 예상에서 하우드-벨리스 RB 선발을 맞힌 사람은 **0명**(1874·UTV·The Villans 모두 완비사카·고메스·린델뢰프를 거론 · The Villans 패널 「I can't see Bellis coming in」(벨리스가 들어올 것 같지 않다)).

**⑶ 리드 막판 실점 원인** — 영상들은 **블록 높이보다 경기 관리·오른쪽 측면·세트 수비**를 가리킨다:

| 원인 | 근거 영상 | 실측 대조 |
|---|---|---|
| 경기 관리 — 맥긴이 빠진 뒤 리더 공백 · 막판 볼 지키기 실패 | Tanswell · Sky 킨·영(「키퍼로 돌렸다가 다시 넘겨줬다」) | 85′ 이후 스즈키 롱볼 9개 중 6개 실패(WS) |
| 오른쪽 측면 추적 — 헤밍스가 도르구 침투를 놓침 | UTV 「미드필드 문제」 · 워치얼롱 90+5′ 「They're getting out wide on us on their left-hand side」(맨유가 그쪽 왼쪽, 즉 빌라 오른쪽으로 벌려 들어온다) | §4는 90+2′ 출발을 고메스·하우드-벨리스로 적었다 — 둘은 이어지는 장면이라 헤밍스 단독 귀속은 하지 않는다 |
| 마지막 코너 배치 — GK 주변 4대1 · 니어포스트 중복 · 블로커 부재 · 17·18·19세 셋이 함께 섬 | UTV · Tanswell · 에메리(「키퍼 보호에 집중했다면」 · §8) | 세 출처 일치 |

**⑷ 리포트에 없던 관찰**
- **피벗 간격**: 후반 카마라·고레츠카가 하프스페이스 침투를 백라인까지 따라가 컷백 공간이 비었다(Tanswell). WS 실측 둘의 좌우 간격 전반 9.0 → 후반 21.3(UTV 「후반에 벌어졌다」와 일치). 둘 사이 패스 UTV 집계 7회 ↔ WS 근사 12회 — 확정 못 함(쟁점 #87).
- **후반 압박**: UTV 워치얼롱 68′쯤 「Hunting in packs, aggressively winning the ball back」(무리 지어 공격적으로 되찾는다) ↔ 하프별 PPDA 전반 16.56 → 후반 11.38(낮을수록 압박). ⚠️ Tanswell의 「후반엔 물러앉았다」는 이 수치와 **맞지 않는다** — 실측 우선.
- **맨유의 빌드업 대응**: 전반 맨유가 빌라 빌드업에 대인으로 붙었다(워치얼롱 34′쯤 「they've gone man-for-man」(맨투맨으로 붙었다)).
- **에메리 플래시 새 인용**: 「we have to go to good balance」(후반엔 좋은 균형을 잡아야 했다) · 「They did it as well against Roma」(맨유는 로마전에서도 그랬다) · 벤치 조기 퇴장은 「the match was finishing」(경기가 끝나는 줄 알았다).

### 사전 예상 대조(경기 전 영상 5편)

| 예상 | 출처 | 실제 |
|---|---|---|
| 카마라–고레츠카 피벗 · 맥긴 10번 · 만잠비 왼쪽 · 알리송 오른쪽 | 1874 · UTV · The Villans | 대체로 적중 |
| RB = 완비사카/고메스/린델뢰프 | 3편 모두 | 빗나감(하우드-벨리스) |
| 「Villa are one of the most passive sides」(빌라는 가장 수동적인 팀 중 하나) — Sky Reed | 1874 | 재현(수비 액션 평균 높이 31.2) |
| 맨유 모멘텀 경계 · 잭슨 고립 우려 | UTV · The Villans | 재현(막판 2실점 · 잭슨 볼 터치 30) |
| 속도로 벌려라 · 맨유 중원을 뚫어라 | UTV · 1874 | 실현 안 됨(오픈플레이 xG 0.38) |
| 「맨유 압박이 어설프다」 | 1874 | 반박(맨유 PPDA 9.21) |

### 구현 판정

- 구현 주장 23행 적재 — HELD 11(쟁점 #13·#14·#29·#49·#53·#59·#87에 묶음) · 나머지 NA/none. **정본 변경 0** · 게임 구현 판정 「추가 관찰」 유지.
- 남은 것(D+2로): 에메리 교체 의도 1차 발언 · 스페인어 회견 원문 · The Villans 경기 후 영상(11-09 저녁 기준 미게시) · The Athletic 본문.

## D+2 추적 (2026-11-10)

> 결론: **당일 판정은 그대로다(정정 0).** D+1 판정 하나만 고친다 — 만잠비 78′ 교체는 「부상 정황」이 아니었다(구조적 부상 없음 · 대표팀 합류).
> 새 자료: 유튜브 3편(전사·요약·구현 주장 10행) · 전술 글 1(Coaches' Voice) · 다국어 기사 5. 인용은 영상이면 전부 auto-caption 전사 기준이다.

### 새 영상

| 영상 | 채널 · 게시 | 종류 | 한 줄 결론 |
|---|---|---|---|
| `fzuyG4ZUVYc` | The Villans 경기 후 패널(42분) · 11-09 | 경기반응 · #70 | D+1까지 미게시였던 영상. 원인은 블록 높이보다 「리드 뒤 경기 상태 통제 실패」 · 고레츠카–카마라 같은 줄 · 전반 왼쪽 노출 |
| `a94ib5pziPo` | Tactics Exposed(맨유 관점 전술) · 11-09 | 상대팀 · #70 | 캐릭 설계 = 빌라 백4를 좁히고 바깥 침투 · 빌라 빌드업에 대인 마크(마즈라위→만잠비) |
| `UsqgMFZCX_Q` | The Holy Trinity Show(빌라 팬) · 11-09 | 경기반응 · #70 | 막판 스즈키 롱킥 · 90+2′ 헤밍스·고메스 · 시즌 마지막 15분 득실 −4 |

- UTV(@UTVFANCHANNEL)·1874(@The1874Podcast): 11-09 이후 새 경기 영상 **없음**(동영상·라이브 탭 모두 확인 — 이미 D+1에서 처리한 것뿐).
- 건너뜀: XPECTED GOALS `XunbzfrNDC0`(100초) · The Malik Playbook `80f4fFnENeE`(163초) — 길이로 보아 분석 밀도가 낮다(내용 미확인). 맨유 팬 리액션 다수(The United Stand 등)는 캐릭 거취 위주라 제목 단계에서 제외 — ⚠️ 이 판단은 제목 기준이다.

### 실측과 맞춰 본 주장

| 주장 | 출처 | 실측 | 결과 |
|---|---|---|---|
| 고레츠카는 안전하기만 했다 — 「97% passing accuracy with one misplaced pass. Far too safe」(패스 성공률 97%에 실패 1개 — 너무 안전했다) | The Villans | SofaScore 36/37 · 롱볼 0 · 파이널서드 투입 2 | 일치 |
| 전반 맨유가 빌라 왼쪽을 집중 공략 — 「Matson had no support whatsoever」(마첸에게 지원이 전혀 없었다) | The Villans | 맨유 크로스 30 중 빌라 왼쪽 17 | 일치 |
| 알리송에게 볼이 안 갔다(20여 회) | The Villans | 볼 터치 26(71분) | 대체로 일치 |
| 시즌 마지막 15분 득실 −4 | Holy Trinity | PL 76′ 이후 2득점·6실점 | 일치 |
| 막판 스즈키가 짧게 풀지 않고 롱킥 | Holy Trinity | 85′ 이후 스즈키 롱볼 9개 중 6개 실패(WS · D+1) | 일치 |
| 44′ 동점골은 만잠비를 두고 전진한 마즈라위에서 | Tactics Exposed | 틸레만스 골 · 도움 마즈라위(SofaScore) | 일치 |

### 새로 생긴 관찰 — 상대의 「백4 좁히기」

- 맨유는 브루누·음뵈모(후반엔 지르크제이)를 빌라 **센터백과 풀백 사이**에 세워 백4를 좁히고, 쿠냐·아마드·66′ 이후 도르구가 **바깥**을 침투했다. 90+2′ 실점도 같은 패턴이다.
  - Tactics Exposed: 「positioning themselves in between those center backs to drag Villa even narrower and then that opens that space up out wide」(센터백 사이에 서서 빌라를 더 좁히고 바깥 공간을 연다) · auto-caption.
  - Coaches' Voice(11-09 글 · 원문 확인): 「Villa's back four became very narrow, with Taylor Harwood-Bellis at right-back drawn into a narrow position inside」(빌라 백4가 매우 좁아졌고, 라이트백 하우드-벨리스가 안쪽으로 끌려 들어갔다).
- 의미: §요약의 「마지막 두 실점은 빌라 오른쪽」에 **원인 하나가 더해진다** — 측면 미드필더 추적(헤밍스)만이 아니라 백4가 안으로 끌려간 구조. 독립 2소스지만 같은 경기라 쟁점 #53은 「2경기째」 조건을 기다린다. obs#1162.
- 빌라 빌드업 대응(상대 교란): 앞 3명 지역 블록 + 뒤 대인 마크(요로→잭슨 · 마즈라위→만잠비 · 아마드→마첸 · 마이누가 남는 선수 흡수). D+1 UTV 워치얼롱 「they've gone man-for-man」(맨투맨으로 붙었다)과 일치.
- Coaches' Voice는 당일 형태 판정도 지지한다: 「3-2-5 structure when secure in possession」(안정적으로 보유하면 3-2-5) · 「Emery's team dropped into a 4-4-2 low block」(에메리 팀은 4-4-2 로우 블록으로 내려섰다).

### 팬 패널이 갈린 지점

| 쟁점 | The Villans | Holy Trinity | 메모 |
|---|---|---|---|
| 고레츠카 | 「I'll pass back」(백패스만 한다 — 터미네이터 패러디) · 10번이 낫다 | 「extremely composed and assured」(매우 침착하고 확신에 찼다) | 실측 36/37 — 해석만 갈린다(쟁점 #87) |
| 카마라 | 지쳐 보였는데 고레츠카가 먼저 나갔다 · 3경기 연속 출전 관리 필요 | 「Kamara who needed to come off for Gomez」(고메스와 바뀔 선수는 카마라였다) | 둘 다 카마라 교체를 원함 · 에메리 설명 없음 |
| 리드 막판 | 윙어가 백라인으로 내려와 백6 · 마드조에게 넣어 코너로 끌기 | 짧은 빌드업 유지 · 볼 소유 원칙 | 쟁점 #16에 근거로만 쌓음 |

### 만잠비 — D+1 판정 정정

- D+1은 「부상 교체 정황이 강해졌다」고 적었다. **정정**: 스위스 축구협회 미디어 책임자 Adrian Arnold(11-09 회견 · 4-4-2.com 원문 확인):
  - 「Manzambi hat keine Schmerzen im Knöchel und hat grünes Licht gegeben.」(만잠비는 발목 통증이 없고 출전 가능 신호를 줬다)
  - 「Er hat noch ein bisschen Schmerzen in der Wade, aber nicht von diesem Foul am Sonntag」(종아리에 약간 통증이 있지만 일요일 파울 때문은 아니다)
  - 기사 본문: 「Tatsächlich scheint aber keine strukturelle Verletzung vorzuliegen.」(실제로 구조적 부상은 없어 보인다)
- 남는 것: 교체가 부상 대응이었는지 전술 교체였는지는 **여전히 모른다** — 기사는 「kurze Zeit nach einer Behandlung」(치료 직후 얼마 안 돼) 교체됐다고만 적었다. obs#1161.

### 감독 회견 — 원문 상태

- **에메리 스페인어 원문: 없음(이번에도).** 스페인어로 실린 인용(Yahoo Noticias의 Goal 스페인어판 · Futbol Centroamérica)은 모두 **영어 회견을 옮긴 번역**이다 — 원문으로 쓰지 않는다. 그중 §8에 없던 대목 하나(영어 원문 미확인 · 번역 복제):
  - 「Le empujan y le molestan. En otros países no lo permiten. Aquí, sí.」(그를 밀고 방해한다. 다른 나라에선 허용하지 않지만 여기선 허용된다) — 스즈키 관련.
- 일본어(닛칸스포츠 · BBC 인터뷰 번역): 「相手がブロックしてきたときにどう守るか、改善の余地がある。」(상대가 블로킹해 올 때 어떻게 막을지 개선할 여지가 있다) — §8 「키퍼 보호」 발언과 같은 축 · 번역 복제라 교차검증 아님.
- ESPN(11-09): 「We struggled in the first half in some moments after our two goals」(두 골 뒤 전반에 고전한 순간이 있었다).
- 고레츠카(Eurosport.de · Sky 인용): 「Wenn man vier Tore im Old Trafford schießt, sollte man schon den Sieg mitnehmen.」(올드 트래퍼드에서 4골을 넣었으면 승리를 가져가야 한다).
- **교체 의도(71′·78′·86′) 에메리 1차 설명: 여전히 없음.** 영어 회견 전문(AVFC·Birmingham Live)·캐릭 회견 전문도 못 찾음.

### The Athletic · Tanswell

- 기사 7764790 본문: 우회하지 않음(지시대로). 대체 자료는 D+1의 1874 Tanswell 출연분(`T24bW9RS5QE`)이 이미 담고 있다. 11-09 이후 1874 새 출연분은 없다. Bluesky 새 경기 분석 게시: 이번 회차에서 확인 못 함.

### 0건 기록(다음 회차가 반복하지 않도록)

| 언어 | 검색어 | 결과 |
|---|---|---|
| 스페인어 | Emery Manchester United 4-4 rueda de prensa declaraciones · Relevo/Marca/AS/Mundo Deportivo · EFE Dorgu minuto 96 | 원문 0 · 번역 기사만 |
| 영어 | Emery/Carrick press conference full transcript · 7500 to Holte / Claret and Blue / Villa Report 4-4 | 전문 0 · 블로그 0(Coaches' Voice·Goal·Brit Brief만) |
| 독일어 | kicker Goretzka erstes Tor · Bild/Sport1 | kicker 0 · Eurosport만 |
| 네덜란드어 | Zirkzee Lammens Aston Villa 4-4 Voetbal International | VI 0(Sporza·Voetbalzone 미열람) |
| 덴마크어 | Dorgu udligning Aston Villa 4-4 hovedstød | 인용 없음 |
| 포르투갈어 | Alysson gol primeiro minuto | 인용 0 |
| 유튜브 | 「Man Utd 4-4 Aston Villa tactical analysis」 외 2개 검색 | 위 2편 채택 · 나머지 제외 |

- 미열람: MEN·Guardian 분석 · United in Focus(402) · Noticias de Gipuzkoa(406) · Bild·Sport1·SRF.

### 구현 판정

- 구현 주장 10행 적재 — HELD 9(쟁점 #16·#49·#53·#59·#87) · NA 1(상대 대인 마크). **정본 변경 0** · 게임 구현 판정 **「추가 관찰」 유지**.
- 새로 쌓인 근거: 리드 막판 대응(#16)에 「GK 짧은 빌드업 유지」·「윙어 하강 백6」·「템포 낮추기」 세 처방이 팬 소스로 모였다 — 모두 등급 D · 1경기. 실측 근거는 85′ 이후 스즈키 롱볼 실패 6/9와 시즌 마지막 15분 −4.
- D+3로 넘김: 에메리 교체 의도 1차 발언 · 스페인어 원문 · Tanswell Bluesky 경기 분석 · MEN/Guardian.
