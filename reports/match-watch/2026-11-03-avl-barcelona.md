# 2026-11-03 FC Barcelona vs AVL — 3-0 (빌라 원정 패)

> 수집일 2026-11-04(경기 다음 날 오전 · D+1 회차) · SofaScore event `16938783` · FotMob `6106263` · WhoScored `2029135`
> UEFA 챔피언스리그 리그 페이즈 4차전 · 스포티파이 캄프 노우 · 주심 Davide Massa · 빌라 원정 · 양 팀 4-2-3-1
> 감독: 바르셀로나 **한지 플릭(Hans-Dieter Flick)** · 빌라 **우나이 에메리** · 게임 버전 `core.game_version.live_on('2026-11-03')` = **FC27**
> 관전 메모: [notes/2026-11-03-avl-barcelona-user-live.md](notes/2026-11-03-avl-barcelona-user-live.md) — 가설은 §10 대조표

## 요약

- **0-3, 경기 내내 열세.** xG 0.72–1.96(FotMob · PK 0) · 점유 35%(전반 30 · 후반 40) · 슈팅 9–16 · 유효 1–8 · 빅찬스 1–5 · 바르사 PPDA 6.85(빌라 19.86).
- **실점 3개 모두 빌라 실수·측면에서**: 7′ 고메스 자기 박스 앞 패스 실수 → 야말 회수·마무리 · 52′ 토레스 회수 직후 패스 상실 → 베르날 → 페르민 → 하피냐 · 64′ 칸셀루가 맥긴을 제치고 컷백 → 하피냐.
- **3선 좌우가 뒤집혔다**: SS 평균 위치(앞뒤, 좌우 · 0~100 · 좌우 0 = 빌라 오른쪽) 고메스 (45,45) RDM · 카마라 (35,63) LDM — 이번 시즌 둘이 함께 선발된 경기에서 처음이다. 고메스가 10 높고, 경기 중 좌우 교대는 드물었다(15분 창 17개 중 2).
- **야말 쪽 3인 수비**: 야말 근접 수비 동작 마첸 6 · 부엔디아 6 · 카마라 6. 62분 전 카마라 수비 동작의 45%가 빌라 왼쪽 터치라인 열에서 나왔다.
- **R1′ 성립(6/6 + 모호 1)**: 부엔디아 선발 4경기 → 만잠비 CAM 4/4 · 부엔디아 없이 알리송 선발 2경기 → 만잠비 LM 2/2. 이 경기도 부엔디아 LM · 만잠비 CAM이었다.
- **게임 구현: 추가 관찰.** 경기 프리셋 4-2-3-1 Wide · Counter/Deep/38(RULE). 정본 변경 없음 — 3선 좌우·만잠비 자리·잭슨 역할은 사용자 판단 대기.

## 1. 경기 개요와 원천 수치

| 지표 | 바르셀로나 | 빌라 | 출처 |
|---|---|---|---|
| 점유 | 65% | 35% | SofaScore·FotMob 동일 |
| xG(전체 / 오픈플레이 / 세트 / 논PK / xGOT) | 1.96 / 1.93 / 0.03 / 1.96 / 2.93 | 0.72 / 0.48 / 0.24 / 0.72 / 0.53 | FotMob 한 응답(동일 스냅샷) · SofaScore xG도 같은 값 |
| 슈팅(유효) · 빅찬스 | 16(8) · 5 | 9(1) · 1 | SofaScore |
| 패스(성공) | 603(552) | 323(258) | SofaScore |
| 롱볼 | 12/26 | 23/46 | SofaScore |
| 경합 · 공중 · 드리블 | 49% · 7/12 · 15/24 | 51% · 5/12 · 11/17 | SofaScore |
| 코너 · 파울 · 경고 | 4 · 14 · 1 | 8 · 9 · 3 | SofaScore |
| PPDA | **6.85**(274/40) | 19.86(437/22) | core.whoscored.ppda · WS 2029135 |
| 수비 액션 평균 높이(def_x) | 41.2 | 38.1 | core.whoscored.수비 액션 평균 높이(def_x) |
| 실점으로 이어진 실수 | 0 | **1**(7′ 고메스) | SofaScore |

- 하프별(FotMob): 전반 점유 30% · xG 0.42–0.70 · 슈팅 5–5 / 후반 점유 40% · xG 0.29–1.27 · 슈팅 4–11. 하프별 PPDA(빌라·바르사) 전반 27.0·7.11 · 후반 15.79·6.64.
- 득점 국면: 0–7′ 동점 · 7′ 이후 전부 열세(만잠비 기준 동점 7분·열세 55분).
- 교체: 바르사 46′ 베르날↔로드리 · 70′ 제주스↔하피냐 · 가비↔페르민 · 더 용↔페드리 · 82′ 발데↔파리냐스. 빌라 62′ 바클리↔고메스 · 고레츠카↔만잠비 · 음바예↔부엔디아 · 77′ 알리송↔맥긴 · 아브라함↔잭슨.
- 경고: 마첸 11′ · 부엔디아 31′ · 잭슨 45′ · 하피냐 45′.
- 수집: SofaScore `/event/16938783{,/statistics,/incidents,/shotmap,/lineups,/managers,/graph,/average-positions}`(headless 기본 UA 200) · FotMob matchDetails 6106263(페이지 안 fetch) · WhoScored matchCentreData 2029135 **scope=full 1,518건** → `reports/match-watch/data/2026-11-03-avl-ws-2029135.json` 보존. 출전 16명 전원 SofaScore 평균 위치·히트맵 있음.

## 2. 전술 설명

### 점유 구조·빌드업

- 4-2-3-1. WS 볼 소유 평균 위치(앞뒤, 좌우 · 0~100 · 좌우 0 = 빌라 오른쪽): 고메스 (48,45) · 카마라 (42,62) · 마첸 (39,88) · 캐시 (41,14) · 부엔디아 (60,69) · 맥긴 (60,32) · 만잠비 (66,55) · 잭슨 (69,47).
- 후방 순환은 오른쪽 축이었다. 패스 연결 린델뢰프→캐시 12회 · 캐시→린델뢰프 11회 · 캐시→맥긴 7회 · 고메스→캐시 7회. 왼쪽은 마첸→토레스 8회로 되돌림이 많았다.
- 바르사 압박(PPDA 6.85)을 피하려 직접 배급을 늘렸다. 롱볼 56개(WS 기준) 중 28개 실패 · 잭슨 롱볼 수신 2 · 스즈키 패스 39 중 롱패스 14.
- 측면이 비대칭이었다. 부엔디아(CAM형)는 왼쪽 안쪽(볼 소유 1열 40%), 맥긴은 오른쪽 터치라인(4열 42%), 왼쪽 폭은 마첸(0열 81%)이 맡았다.

### 비보유 구조·압박

- 4-4-1-1 깊은 블록 — 빌라 수비 액션 평균 높이(def_x) 38.1, 전반 구간 30~35. 만잠비가 잭슨 옆 2선(수비 동작 평균 높이 55)에 섰다.
- **야말 쪽 3인 수비.** 야말 볼 터치 69개 중 59%가 빌라 왼쪽 터치라인 열, 평균 높이 33(빌라 진영). 야말 근접(±3초 · 거리 15 이내) 수비 동작은 마첸 6 · 부엔디아 6 · 카마라 6 · 만잠비 1 · 토레스 1이다. 야말과 같은 1초 안 듀얼은 부엔디아 태클 4 · 마첸 파울 4 · 카마라 태클 3이었다. 야말 드리블은 4/10 성공으로 억제했다.
- 빌라 왼쪽 2/5 구역 수비 동작(62분 전): 마첸 15 · 부엔디아 11 · 카마라 8 · 토레스 7.
- 0-2 이후 52–60′에만 전방 압박이 나왔다(수비 액션 평균 높이(def_x) 55.0 · PPDA 4.43). 64′ 3실점 뒤 다시 내려앉았다(64–75′ 40.6 · PPDA 47).

### 전환·rest-defense·세트피스

- 자기 진영 볼 상실이 실점으로 바로 이어졌다: 7′ 고메스 패스 실수(높이 17 · Opta Error) → 야말 2초 뒤 득점 · 52′ 토레스가 자기 박스 앞에서 회수 직후 패스를 잃고 베르날 회수 → 페르민 → 하피냐(13초).
- 64′는 빌라 오른쪽 1대1이었다. 칸셀루가 맥긴의 챌린지를 제치고(드리블 성공) 컷백 → 하피냐.
- 빌라 역습 위협은 적었다 — 박스 터치 26(바르사 36), 슈팅 9 중 유효 1.
- 세트피스: 빌라 코너 8(맥긴 3 · 부엔디아 1 · 음바예 4) → 슈팅 3(8′·9′·68′) · 세트 xG 0.24(빌라 xG의 33%). 바르사 코너 4 · 세트피스 실점 0. 상세는 [세트피스 리서치 덧붙임](../research/2026-11-04-avl-set-pieces.md).

## 3. 전술적 특성

- **강점**: 야말 개인 돌파 억제(드리블 4/10 · 3인 수비) · 카마라 수비(태클 4 · 인터셉트 4 · 빌라 최고 평점 6.9) · 스즈키 선방 5 · UCL 세트피스 창구 유지(세트 xG 0.24).
- **약점**: 자기 진영 볼 처리 실수 2건이 실점(7′·52′) · 압박 회피 실패(롱볼 절반 실패 · 잭슨 경합 1-5 고립) · 빌라 오른쪽 1대1(칸셀루 vs 맥긴·캐시) · 유효 슈팅 1.
- **상대가 만든 교란**: 플릭의 바르사가 PPDA 6.85로 높게 눌러 빌라의 짧은 빌드업을 끊었다. 칸셀루가 빌라 오른쪽을 공략했고, 야말은 빌라 왼쪽에서 3명을 끌어당겼다.
- **기존 프로필·직전 경기와 비교**: 풀럼전(10-31)은 고레츠카 LDM · 카마라 RDM이었다. 이번 경기는 고메스·카마라 조합이 처음으로 좌우를 바꿨다(관전 메모 R3: 이전 5경기 카마라 왼쪽 기준 폭(툴x) 61.6 · 고메스 40.9 = 카마라 오른쪽). 깊은 블록과 직접 배급은 강팀 원정(맨시티 10-24)과 같은 계열이다.

## 4. 경기 중 변화

1. **0–7′ 동점**: 바르사 압박 속 짧은 배급 시도(빌라 수비 액션 평균 높이(def_x) 33.6). 7′ 고메스 실수 → 0-1.
2. **7–45′ 열세 · 깊은 블록**: 점유 30% · 전반 xG 0.42–0.70. 빌라 코너 3개 중 2개(8′·9′)가 슈팅. 30′ 이후 고메스가 오른쪽으로 더 넓어졌다(15분 창 볼 터치 좌우: 고메스 왼쪽 기준 폭(툴x) 59.6→63.1 · 카마라 31.3→32.6).
3. **46–62′ 후반 출발**: 바르사 46′ 베르날↔로드리. 52′ 0-2 뒤 빌라가 처음으로 높게 압박(52–60′ 수비 액션 평균 높이(def_x) 55.0).
4. **62′ 3명 교체**: 바클리(위치상 CAM · SS 평균 위치(앞뒤, 좌우 · 0~100 · 좌우 0 = 빌라 오른쪽) (62,62)) · 고레츠카(위치상 RDM (54,43)) · 음바예(LM (73,79)). 교체 짝은 고메스↔바클리 · 만잠비↔고레츠카지만 자리는 바클리가 만잠비 자리, 고레츠카가 고메스 자리였다. 카마라는 LDM을 지키며 중앙 쪽으로 옮겼다(62분 뒤 수비 동작 평균 좌우 59 → 41 — 좌우 0 = 빌라 오른쪽).
5. **64′ 0-3 → 77′ 알리송·아브라함**: 블록 재하강. 음바예가 키패스 2 · xA 0.20으로 마지막 공격을 이끌었지만 결과는 그대로였다.

## 5. 선수별 분석 — 출전 선수 전원

좌표: SS 평균 위치(앞뒤, 좌우 · 0~100 · 좌우 0 = 빌라 오른쪽). 볼 소유·수비 그리드 열은 왼쪽→오른쪽 비중.

| 선수 | 위치·실제 역할 | 분/평점·핵심 스탯 | 평균 위치·히트맵 | 특성·수행 | FC 역할/포커스 함의 |
|---|---|---|---|---|---|
| 스즈키 | GK · 배급 혼합 | 90 · 6.3 · 선방 5 · 패스 27/36 · 롱볼 6/14 | SS 평균 위치 (8,52) | 3실점 모두 근거리. 압박 아래 롱패스 비중 구간별 25~67% | 1위 gk_goalkeeper/Defend(Δ.034 무결정) · 정본 gk_ballplaying/Build-Up |
| 캐시 | RB · 수비 우선 | 90 · 5.8(팀 최저) · 경합 1-3 · 패스 29/37 | SS 평균 위치 (41,14) | 칸셀루·고든 상대. 오른쪽 순환 축(린델뢰프↔캐시 23회) | 1위 fb_wingback/Balanced(Δ.098) = 정본 |
| 린델뢰프 | RCB | 90 · 6.4 · 패스 35/37 | SS 평균 위치 (23,33) | 가장 깊은 위치에서 오른쪽 출구로 순환 | 1위 cb_bpd/Build-Up(Δ.020 무결정) · 정본 cb_bpd/Aggressive |
| 파우 토레스 | LCB · 야말 쪽 커버 | 90 · 6.4 · 패스 43/48 · 롱볼 5/8 | SS 평균 위치 (32,69) | 왼쪽 2/5 수비 동작 11. 52′ 회수 직후 패스 상실이 2실점 출발 | 1위 cb_bpd/Aggressive(Δ.021 무결정) · 정본 cb_bpd/Build-Up |
| 마첸 | LB · 야말 1차 수비 + 왼쪽 폭 | 90 · 6.2 · 11′ 경고 · 경합 10-7 · 리커버리 11 · 드리블 4/5 | SS 평균 위치 (39,87) · 볼 소유 0열 81%→78%(62′ 전→후) | 야말 근접 수비 동작 6 · 같은 1초 파울 4. 음바예 투입 뒤에도 터치라인을 지킴(H3 불일치) | 1위 fb_wingback/Balanced(Δ.096) · 정본 fb_att_wb/Support — 인버티드 근거 없음 |
| 주앙 고메스 | **RDM** · 카마라보다 높게 | 62 · 6.4 · 태클 4 · 경합 4-1 · 패스 14/17 · xG 0.11 | SS 평균 위치 (45,45) · 수비 동작 열 12/0/38/12/38(n=8) | 7′ 실수 → 실점(Opta Error). 좌우 교대 창 2/17 | 1위 dm_dlp/Roaming 0.694 · 2위 dm_holding/Roaming(Δ.047 무결정) · RDM 정본 dm_holding/Defend 0.580 |
| 카마라 | **LDM** · 깊은 홀딩 + 야말 쪽 | 90 · **6.9** · 태클 4 · 인터셉트 4 · 경합 7-6 · 패스 22/25 | SS 평균 위치 (35,63) · 62′ 전 수비 동작 0열 45% · 가장 깊은 줄 55% | 야말 근접 수비 동작 6 · 같은 1초 태클 3 · 인터셉트 1 | 1위 dm_dlp/Roaming 0.636(Δ.034 무결정 · LDM 정본과 같음) · dm_holding/Defend 0.539 |
| 맥긴 | RM · 수비형 측면 | 77 · 6.0 · 패스 11/20 · 볼 손실 16 · 코너 3 | SS 평균 위치 (56,28) · 수비 동작 4열 64% | 64′ 칸셀루에게 제쳐짐 → 3실점 | 1위 wm_widemid/Defend(Δ.084) · 정본 wm_winger/Attack 0.514 |
| 만잠비 | CAM · 수비 시 2선 | 62 · 6.4 · xG 0.23(빅찬스 미스 1) · 드리블 2/3 · 경합 2-6 · 패스 7/10 | SS 평균 위치 (63,54) · 볼 소유 열 16/26/37/16/5 | 21터치로 고립. R1′ 패턴대로 부엔디아 선발 = CAM | 1위 cam_playmaker/Build-Up(Δ.030 무결정) · 정본 cam_playmaker/Roaming |
| 부엔디아 | LM(CAM형) · 야말 2차 수비 | 62 · 6.8 · 태클 5 · 경합 7-5 · 31′ 경고 | SS 평균 위치 (55,72) · 볼 소유 1열 40% · 수비 0열 43% | 야말 근접 수비 동작 6 · 같은 1초 태클 4 | 1위 wm_widemid/Defend(Δ.028 무결정) · 정본 wm_insidefwd/Balanced |
| 잭슨 | ST · 채널·터치라인 수신 | 77 · 6.6 · 드리블 1/4 · 경합 1-5 · 45′ 경고 · 오프사이드 2 | SS 평균 위치 (63,46) · 볼 소유 열 26/0/26/37/11 · 행 32/37/21/11/0 | 양 터치라인 37%(시즌 29%) · 내려옴 11%(시즌 9%) · 롱볼 수신 2 | 1위 st_advanced/Support(Δ.099) = 정본 |
| 바클리 | 62′ · 위치상 CAM | 28 · 6.2 · xG 0.10 | SS 평균 위치 (62,62) | 교체 짝은 고메스지만 만잠비 자리 | 45분 미만 — 리포트용 |
| 고레츠카 | 62′ · 위치상 RDM | 28 · 6.5 · 패스 9/10 | SS 평균 위치 (54,43) | 고메스 자리. 카마라는 LDM 유지 | 45분 미만 |
| 음바예 | 62′ · LM 윙어 | 28 · 7.0 · 키패스 2 · xA 0.20 · 코너 4 | SS 평균 위치 (73,79) | 볼 소유 맨 앞 줄 50% — 야말 쪽 수비보다 전진 | 45분 미만 |
| 알리송 | 77′ · RM | 13 · 6.7 · 드리블 2/2 | SS 평균 위치 (63,24) | 오른쪽 터치라인 | 45분 미만 |
| 아브라함 | 77′ · ST | 13 · 6.5 · 볼 소유 3 | SS 평균 위치 (75,39) | H2 이어받기 판정 불가(표본) | 45분 미만 |

## 6. 전술 변화 판정

- **유지된 것**: 4-2-3-1 · 강팀 원정 깊은 블록 + 직접 배급(맨시티전과 같은 계열) · 오른쪽 순환 축(린델뢰프↔캐시) · UCL 세트피스 창구.
- **새로 나타난 것**: ⑴ 고메스 RDM · 카마라 LDM(이번 시즌 둘이 함께 선발된 6번째 경기에서 처음) ⑵ 부엔디아가 LM(CAM형 측면) · 만잠비 CAM ⑶ 음바예가 왼쪽 코너 키커(4개).
- **직전 경기 대비**: 풀럼전 고레츠카 LDM → 이번 경기 고메스(벤치에서 선발 복귀) · 마첸 LB(풀럼전도 마첸). 비보유 형태 4-4-1-1은 같다.
- **`manager_profiles`·`observations` 반영**: profile 갱신 불필요 — 3선 좌우 교대는 1경기 현상이라 formation·role_demands 축에 덧붙이지 않고 D+3 종결 때 재판정한다(서사로 설계 의도가 확인되면 role_demands에 덧붙임).

## 7. 게임 구현 판정

- 결론: **추가 관찰**
- **이 경기 전용 팀 설정**: FC27 · 4-2-3-1 Wide · **Counter / Deep / 38** · tactic_code 없음 · rule_note RULE — `core.team_settings.suggest(점유 35, 패스 323, 롱볼 시도 46, PPDA 19.86)` → Counter/Deep/0~45(롱볼 14.2%) · compare() 차이 0. 보유 4-2-3-1 · 비보유 4-4-1-1.
- **이 경기 선발 11명**(단일 경기 커널 1위 · SofaScore 히트맵 · 무결정 = Δ≤.05):

| 슬롯 | 선수 | 역할/포커스 | fit | Δ | 2위 | 시즌 정본 |
|---|---|---|---|---|---|---|
| GK | 스즈키 | gk_goalkeeper/Defend | .943 | .034 무결정 | gk_goalkeeper/Balanced | gk_ballplaying/Build-Up |
| RB | 캐시 | fb_wingback/Balanced | .876 | .098 | fb_fullback/Balanced | 같음 |
| RCB | 린델뢰프 | cb_bpd/Build-Up | .914 | .020 무결정 | cb_bpd/Aggressive | cb_bpd/Aggressive |
| LCB | 토레스 | cb_bpd/Aggressive | .917 | .021 무결정 | cb_bpd/Build-Up | cb_bpd/Build-Up |
| LB | 마첸 | fb_wingback/Balanced | .902 | .096 | fb_fullback/Balanced | fb_att_wb/Support |
| RDM | 고메스 | dm_dlp/Roaming | .694 | .047 무결정 | dm_holding/Roaming | dm_holding/Defend |
| LDM | 카마라 | dm_dlp/Roaming | .636 | .034 무결정 | dm_dlp/Build-Up | 같음 |
| RM | 맥긴 | wm_widemid/Defend | .684 | .084 | wm_widemid/Support | wm_winger/Attack |
| CAM | 만잠비 | cam_playmaker/Build-Up | .885 | .030 무결정 | cam_playmaker/Roaming | cam_playmaker/Roaming |
| LM | 부엔디아 | wm_widemid/Defend | .598 | .028 무결정 | wm_insidefwd/Balanced | wm_insidefwd/Balanced |
| ST | 잭슨 | st_advanced/Support | .604 | .099 | st_poacher/Versatile | 같음 |

- 무결정 7칸 — 1위를 조용히 채택하지 않는다(런북 §2-1). 3선은 두 칸 모두 무결정이라 커널로는 「누가 홀딩인가」를 가를 수 없다.
- `prescriptions`·`slot_canon_roles`·`team_tactic_setups` 변경: **없음**. measured #919(맥긴 RM) 재집계만(n 13→14 · wm_winger/Attack 0.757 · argmax 불변 · G18).
- ⚠️ 등급(불변규칙 12): 이 절은 커널 적합(히트맵 코사인 — 우리 실측 파이프라인)만 썼고 「역할이 무엇을 한다」는 주장을 하지 않았다.
- **사용자 판단 대기(정본은 바꾸지 않는다)**:
  1. **3선 조합(계속 검토 · obs#1080 테스트 대기)** — 시즌 정본은 RDM dm_holding/Defend(카마라) · LDM dm_dlp/Roaming(고메스). 이 경기처럼 좌우가 바뀌면 FC27에서도 **역할을 선수에 붙여 좌우만 바꿀지**(카마라 LDM dm_holding/Defend · 고메스 RDM dm_dlp/Roaming) 판단이 필요하다. 근거는 아직 1경기다.
  2. **만잠비 자리** — R1′ 성립(6/6). 인게임에서 「부엔디아 선발 = 만잠비 CAM / 윙어 선발 = 만잠비 LM·맥긴 CAM」을 프리셋 두 벌로 둘지.
  3. **잭슨 터치라인 수신** — 강팀 상대 보유 그리드 2위가 st_target/Wide(.422). ST 포커스 보류 건(슬롯 정본 보류 ⑵)과 묶어 판단.
- 다음 경기 재검증: 맨유(PL 11-09 예정)에서 3선 좌우 · 만잠비 자리 · 자기 진영 실수.

⚠️ 이 설정은 `match_game_setups`·`match_player_prescriptions`의 `MATCH ONLY` 프리셋이다. 전체 시즌 전술이나 대표 선수 역할에 자동 병합하지 않는다.

## 8. 영상·기사·감독 발언

조회 시각 2026-11-04 00:41 UTC(경기 종료 약 2.5시간 뒤 · 서브에이전트 위임 · 읽기 전용). 「본문」 = 기사 본문 직접 열람, 「요약 기준」 = 검색 요약만.

### 감독 1차 발언

- **에메리 — TNT(영어)** · Sky Sports 경기 리포트(2026-11-03 23:13 · 본문): 「Good experience, bad result. At this level, you must be ruthless and avoid mistakes.」(좋은 경험, 나쁜 결과. 이 수준에선 냉정해야 하고 실수를 피해야 한다.) · BBC 「What Emery and McGinn said」(Yahoo 전재 · 본문): 「If we could score one goal with the chances we had in the first half, maybe it would have been different, but we were not clinical.」(전반 기회에서 한 골만 넣었어도 달랐을지 모른다. 하지만 마무리가 날카롭지 못했다.) — https://sports.yahoo.com/articles/barcelona-3-0-aston-villa-224937852.html
- **에메리 — 회견(영어 · PA/BBC Mashiter 2026-11-04 · 본문)**: 고메스에 대해 「I am not blaming him.」(그를 탓하지 않는다.) · 「3-0 is maybe more than we deserved, but we accept the defeat.」(3-0은 우리가 받을 만한 것보다 클 수 있지만 패배를 받아들인다.) — https://sports.yahoo.com/articles/emery-takes-positives-villa-reach-235944835.html · Express & Star(403 · 요약 기준): 「Gomes started not very confident with the ball. The mistake is part of our style」(고메스는 시작부터 공을 다루는 데 자신감이 없었다. 그 실수는 우리 스타일의 일부다).
- **에메리 — Movistar(스페인어)** · Futeros(본문): 「La clave han sido las pérdidas de balón, que nos han penalizado también en los duelos」(핵심은 볼 손실이었고, 그것이 경합에서도 우리를 불리하게 만들었다.) · 「Somos un equipo en construcción y este partido nos tiene que servir para aprender」(우리는 만들어지는 중인 팀이다. 이 경기에서 배워야 한다.) — https://futeros.com/unai-emery-sobre-la-derrota-del-camp-nou-somos-un-equipo-en-construccion-y-este-partido-nos-tiene-que-servir-para-aprender/ · SocBlaugrana(본문): 「nosotros buscamos atraer a los rivales para tener espacios」(우리는 상대를 끌어내 공간을 얻으려 한다) — 짧은 빌드업 고수가 설계였다는 1차 근거.
- **에메리 — 경기 전(11-02)** · El Nacional(본문): 야말에 대해 「Es un jugador especial y puedes ver que puede acabar siendo el mejor del mundo.」(특별한 선수이고, 세계 최고가 될 수 있다는 게 보인다.) · 「nos exigirán muchísimo y tendremos que jugar con mucha personalidad」(그들은 우리를 아주 강하게 몰아붙일 것이고, 우리는 큰 개성을 갖고 뛰어야 한다.) — 야말 대응법·배치 언급은 없음.
- **플릭** · Goal(Movistar → AS · 본문): 「We faced a big team that defended well. We are happy with our defensive performance,」(수비를 잘하는 큰 팀을 상대했다. 우리 수비 경기력에 만족한다.) · Barça Blaugranes 회견(403 · 요약 기준): 「We try to press them very high, so that they make mistakes.」(상대가 실수하도록 아주 높게 압박한다.) · 독일어 발언은 미검색.

### 기사·전술 서술

- **EFE**(Francisco Ávila · Infobae 전재 · 본문): 「El vasco se apuntó a la táctica 'Mou' de cortocircuitar la creación del Barcelona con marcajes individuales a Rodri y Pedri」(에메리는 로드리와 페드리를 대인 마크해 바르사의 빌드업을 끊는 '무리뉴식' 전술을 택했다.) · 「el Villa jugaba muchos balones en largo para que Nicolas Jackson se la jugara con la pareja de centrales」(빌라는 잭슨이 센터백 둘과 맞붙도록 롱볼을 많이 보냈다.)
- **Goal 「The tactics board」**(Mohamed Saeed · 본문 요약): 캐시·마첸은 측면을 지키라는 지시 · 바르사 전방 4명이 빌라 두 피벗에 대인 압박 · 잭슨은 역습 때 속도로 라인을 늘림 · ⚠️ 「빌라 높은 수비 라인」 서술은 **실측과 충돌** — 빌라 수비 액션 평균 높이(def_x) 38.1(바르사 41.2) · 전반 구간 30~35 ⇒ **실측 채택(깊은 블록)**.
- **VAVEL 평점**(본문): 마첸 5 「Sufrió especialmente con Lamine Yamal. El extremo español le superó repetidamente en el uno contra uno.」(라민 야말에게 특히 고전했다. 1대1에서 거듭 제쳤다.) — 실측 야말 드리블 4/10과 어긋남(VAVEL은 「거듭」) ⇒ 실측 기록, 서술은 인상 평가로 둔다.
- **Ara**(Albert Nadal · 본문): 쿠바르시가 첫 20분에 「ya había cortado tres excursiones del veloz Jackson」(빠른 잭슨의 침투를 이미 세 번 끊었다).
- **PA/Independent**(Jonathan Veal · 본문): 「Nicolas Jackson burst down the right flank to set up Johan Manzambi, who shot wide.」(잭슨이 오른쪽 측면을 돌파해 만잠비에게 연결했지만 슛은 빗나갔다.) — H2′ 장면 근거(19′).
- **CBS**(본문): 「Joao Cancelo was essentially given permission to dance around Villa's defense」(칸셀루는 사실상 빌라 수비 사이를 마음대로 휘저었다).
- **El Debate**(본문): 빌라가 「buscó la inexperiencia en Champions de Brian Fariñas para generar peligro desde el flanco izquierdo」(파리냐스의 챔스 경험 부족을 노려 왼쪽 측면에서 위협을 만들었다).
- **Lance!(포르투갈어 · 본문)**: 고메스가 「falhou na saída de bola」(빌드업에서 실수했다) — 좌우 위치 서술 없음.

### R4 — 고메스 오른쪽(RDM) 배치의 전술적 배경

- **확인된 이유(1차 발언)**: **없음.** 에메리 회견·TNT·Movistar·경기 전 회견 어디에도 좌우 배치 설명이 없다.
- **확인된 사실(실측)**: ⑴ 카마라의 62분 전 수비 동작 주변 상대는 **페르민 5 · 야말 5**(둘 다 바르사 오른쪽 = 빌라 왼쪽), 고메스는 고든 2 · 하피냐 2 · 페드리 2 · 페르민 2로 분산. ⑵ 카마라 수비 동작 45%가 빌라 왼쪽 터치라인 열. ⑶ 바르사 전방이 두 피벗을 대인 압박(Goal) — 7′ 실수는 RDM 고메스에게서 나왔다.
- **추정**: 바르사 공격의 중심(야말·페르민)이 빌라 왼쪽에 몰리므로 수비 검증된 카마라를 그쪽에 두고, 더 높이·넓게 움직이는 고메스를 반대편(고든·칸셀루 쪽 · 페드리 견제)에 둔 설계로 읽힌다(사용자 가설 R4-H와 같은 방향). EFE의 「로드리·페드리 대인 마크」가 어느 피벗 몫인지는 실측(고메스 주변 페드리 2 · 카마라 1)으로도 갈리지 않는다. D+2·D+3에서 영상·전술 글로 재판정.

### 미수행·0건과 사유

- **Jacob Tanswell X**: 402로 접근 불가 — 미수행. The Athletic 경기 후 기사 0건(조회 시점). 경기 전 1874 영상 「Jacob Tanswell Reports From Barcelona」(Ud2cwU17zoU · 11-02)만 확인.
- **유튜브 필수 3채널**: 경기 후 영상 0편(조회 시점 업로드 전). 경기 전 영상만 있음 — UTV 「HOW ASTON VILLA BEAT BARCELONA」(bXXq32QKtUc) · 「EVERYTHING ASTON VILLA FANS NEED TO KNOW ABOUT BARCELONA」(vdNc0R3OPmY) · The Villans 「Can Aston Villa Stop Lamine Yamal…」(Ttk_jjW5KkU) — 경기 전 프리뷰라 전사 대상 아님. 13:30 보강 회차·D+2에서 재조회.
- **전술 블로그**(TFA·BTL·Coaches' Voice·Spielverlagerung): 0건(경기 당일).
- **스페인어**: Mundo Deportivo·Sport·AS·Marca·El Periódico·RAC1는 검색 도구 도메인 차단 · 에메리 스페인어 회견 전문 0. **카탈루냐어**: VilaWeb·CCMA 0 · Ara만. **포르투갈어**: ge.globo 0 · UOL 차단. **독일어**(플릭): 미검색.
- 검색어(다음 회차 중복 방지): "Emery Barcelona 3-0 Aston Villa press conference" · "Emery rueda de prensa Barcelona Aston Villa" · "Emery Movistar postpartido" · "Mourinho marcaje Rodri Pedri" · "Barça Aston Villa crònica"(ara·vilaweb·ccma) · "João Gomes Aston Villa Barcelona erro"(ge·lance·espn.com.br).

## 9. 데이터 반영과 한계

- DB 추가: `matches` #130 · `player_matches` 16(국면 그리드 · SS 확장 필드 · FotMob 경기 스탯 · WS 운반 추정/수신) · `team_match_stats` 1(xG 4종 FotMob · PPDA · 수비 액션 평균 높이(def_x)) · `match_events` 17 · `match_shots` 25(SofaScore) · `match_period_stats` 2 · `match_momentum` 92 · `match_set_pieces` 19(빌라 10) · `match_phase_metrics` 84 · `match_reports` #66 · `match_player_reports` 16 · `match_game_setups` 1 · `match_player_prescriptions` 16 · `match_hypotheses` 10 · `match_tactical_changes` 8 · `prescriptions` #919 재집계.
- 한계: ⑴ 강팀 원정 · 7′부터 열세 — 위치·역할은 스코어 효과가 크다. ⑵ 고메스 수비 그리드 n=8, 교체 5명은 45분 미만. ⑶ 야말 「근접 수비 동작」은 이벤트 시각·거리 근사(±3초 · 거리 15)이지 트래킹 데이터가 아니다. ⑷ R1 비교는 n=4·2.
- 상태 `draft` — 서사(회견·영상)는 D+1~D+3에서 채우고 D+3 회차가 complete를 판정한다.

## 10. 관전 메모 가설 대조표 (D0)

| # | 가설 | 실측 | 판정 |
|---|---|---|---|
| H1 | 수비 시 카마라·고메스 좌우가 자주 바뀐다 | 15분 창 볼 터치에서 고메스가 카마라보다 왼쪽인 창 2/17 · 수비 동작 평균 좌우 고메스 41 · 카마라 59(좌우 0 = 빌라 오른쪽) | **부분 일치** — 교대 장면은 있으나 드묾 |
| H1′ | 고메스는 넓게, 카마라는 홀딩 | 카마라 62′ 전 수비 동작 0열 45% · 가장 깊은 줄 55% · 고메스는 4개 열 분산(n=8) · 시즌 수비 열 비중 고메스 18/22/22/20/19 vs 카마라 1/18/26/34/21 | **부분 일치** — 시즌 단위 일치, 단일 경기는 표본 부족 |
| H1″ | 고메스가 살짝 높게 · 배치 고메스 RDM | SS 평균 위치 고메스 (45,45) · 카마라 (35,63) · 수비 동작 평균 높이 34.8 vs 28.8 | **일치** |
| R4-H | 좌우 교대 = 야말 대응 | 야말 터치 59% 빌라 왼쪽 터치라인 · 근접 수비 동작 마첸 6 · 부엔디아 6 · 카마라 6 · 카마라 주변 상대 페르민 5·야말 5 · 감독 언급 0(§8 R4) | **부분 일치** — 카마라가 야말 수비에 실제 가담(실측). 설계 의도는 1차 발언 확인 전 추정 |
| H2 | 잭슨은 내려오지 않고 채널로 | 아래 두 줄 11%(시즌 9%) · 양 터치라인 37%(시즌 29%) · 롱볼 수신 2 · 오프사이드 2 | **부분 일치** — 넓게 받는 건 시즌보다 많고, 안 내려오는 건 평소 수준 |
| H2′ | 양쪽 터치라인 끝에서 받아준다 | 볼 소유 열 26/0/26/37/11 | **일치** |
| H3 | 음바예 투입 뒤 마첸 인버티드 | 볼 소유 0열 81%→78% · 평균 높이 39→45 · 수비 동작만 1열 71%(n=7) | **불일치** — 실측 채택(높아졌을 뿐 안쪽으로 오지 않음) |
| R1′ | 만잠비 자리는 동료 기용이 정한다 | 부엔디아 선발 4 → CAM 4/4 · 부엔디아 없이 알리송 선발 2 → LM 2/2 · 음바예 선발 1 모호 | **일치**(n=7) |
| R1 | LM vs CAM 어디서 더 잘하나 | CAM 4경기 평점 7.33 · xG+xA 경기당 0.51 vs LM 2경기 6.85 · 0.09 | **판정 불가** — CAM 쪽 경향, 표본·동료·상대 교란 |
| 교체 메모 | 음바예 LM · 바클리 CAM · 고레츠카 RDM | SS 평균 위치 (73,79) · (62,62) · (54,43) | **일치** |

### R1 · R1′ 교차표 — 26/27 빌라 선발 7경기

| 경기 | 만잠비 출발 | SS 왼쪽 기준 폭(툴x) | 동료 측면·10번 | 평점 | xG+xA | 키패스 |
|---|---|---|---|---|---|---|
| 09-19 토트넘(PL) | CAM | 53 | 부엔디아 왼쪽 · 맥긴 오른쪽 | 7.8 | 0.60 | 2 |
| 10-10 브렌트퍼드(PL) | CAM | 48 | 부엔디아 왼쪽 · 맥긴 오른쪽 | 7.1 | 0.58 | 3 |
| 10-14 페네르바흐체(UCL) | 왼쪽 안쪽(모호) | 39 | 음바예 왼쪽 터치라인 · 맥긴 오른쪽 | 8.2 | 0.31 | 2 |
| 10-17 뉴캐슬(PL) | CAM | 57 | 부엔디아 왼쪽 · 알리송 오른쪽 | 8.0 | 0.62 | 2 |
| 10-24 맨시티(PL) | LM(깊게) | 34 | 알리송 오른쪽 · 맥긴 중앙 | 6.8 | 0.07 | 0 |
| 10-31 풀럼(PL) | LM | 24 | 알리송 오른쪽 · 맥긴 10번 | 6.9 | 0.11 | 1 |
| 11-03 바르셀로나(UCL) | CAM | 46 | 부엔디아 왼쪽 · 맥긴 오른쪽 | 6.4 | 0.24 | 0 |

- 읽기: 부엔디아가 서면 부엔디아가 왼쪽을 맡고 만잠비가 가운데로 간다. 알리송이 서면 맥긴이 가운데로 가고 만잠비가 왼쪽으로 빠진다. 사용자 가설 그대로다.
- 뉴캐슬전은 「부엔디아 + 알리송」이 함께 섰고 만잠비 CAM이었다 — 기준은 「윙어가 있느냐」보다 **「부엔디아가 있느냐」**에 더 가깝다.
- ⚠️ 성적 차이에는 동료 효과(부엔디아 동반)와 상대(맨시티 원정)가 섞인다. 경향만 적는다.

## D+1 추적 (2026-11-04)

- 이 회차가 경기 다음 날 오전(D+1) 수집 회차다 — §8이 D+1 결과다. 회견 원문(영어·스페인어)은 확보했고, 영상·전술 블로그·The Athletic은 아직 없다.
- 당일 판정 정정: 없음. 서사가 실측과 충돌한 2건(Goal 「높은 수비 라인」 · VAVEL 「마첸이 야말에게 거듭 제쳐짐」)은 실측을 채택했다(불변규칙 3).
- 다음 회차: 13:30 보강(`mw-avl-barcelona-collect-1330`) → D+2(11-05 20:00 `mw-avl-barcelona-d2`) → D+3(11-06 20:00 `mw-avl-barcelona-d3` · complete 판정). 남은 일: 필수 3채널 경기 후 영상 전사·요약·구현 주장(G17) · Tanswell · 스페인어 원어 회견 전문 · 전술 블로그 · R4 설계 의도 재판정.

## D+1 보강 (2026-11-04 13:30)

예약 회차 `mw-avl-barcelona-collect-1330`. 09:30 회차 산출(리포트 · `match_reports` #66)이 있어 보강만 했다. 조회 2026-11-04 13:00~13:40 KST · 회견·기사는 서브에이전트 위임(읽기 전용) · 영상 전사는 브라우저 패널(뮤트 · 포착 즉시 정지 · 탭 닫음).

### ⑴ 감독 회견 — 새로 확보한 원문

- **에메리 — ESPN**(Tom Hamilton · 11-03 · 본문): 「with how they are pressing. It's so intense.」(그들이 압박하는 방식이 정말 강렬하다.) · 「We have worked over four years together and we've made those mistakes before」(우리는 4년 동안 함께 해왔고 전에도 그런 실수를 했다) · 「The 3-0 is more than we suffered but we accept this defeat」(3-0은 우리가 겪은 것보다 큰 점수지만 이 패배를 받아들인다) — 고메스 실수를 압박 강도와 묶은 대목이 새것이다. https://www.espn.com/soccer/story/_/id/50373199/aston-villa-vs-barcelona-uefa-champions-league-unai-emery
- **에메리 — BBC/TNT**(Yahoo 전재 · 본문): 「after the mistake we made, we were creating chances, facing them with individual duels」(실수 이후 우리는 기회를 만들었고 개인 듀얼로 맞섰다) · 「In this level you must be more ruthless.」(이 수준에서는 더 냉혹해야 한다.)
- **에메리 — EFE**(Infobae · 본문): 「La clave no han sido solo las pérdidas, sino más bien que nos ha costado mucho ganar duelos con sus centrales.」(핵심은 볼 손실만이 아니라 상대 센터백과의 듀얼에서 이기기가 무척 힘들었다는 점이다.) · ⚠️ 09:30 회차의 Futeros 판 「La clave han sido las pérdidas de balón」(핵심은 볼 손실이었다)과 **받아쓰기가 갈린다** — 두 매체 모두 같은 Movistar 인터뷰 전사라 교차검증이 아니다. EFE 판이 더 길고 문맥(센터백 듀얼 = 잭슨 롱볼 표적)과 맞아 우선하되 확정하지 않는다. https://www.infobae.com/espana/agencias/2026/11/03/emery-el-barcelona-ha-merecido-ganar-aunque-hemos-tenido-nuestras-ocasiones/
- **에메리 — Fichajes.com**(본문): 「el Barcelona ha aprovechado algún error nuestro en salida de balón」(바르사가 우리 빌드업 실수를 이용했다) · 「el partido ya se ha enfriado por completo」(경기가 완전히 식어버렸다).
- **에메리 — Europa Press**(Infobae · 본문): 「Barcelona siempre va a ser el Barcelona」(바르셀로나는 언제나 바르셀로나다) · 「ellos al final han merecido ganar」(결국 그들이 이길 자격이 있었다).
- **에메리 — AS**(Corrientes Hoy 전재 · 발췌 한 줄): 「Hemos demostrado en momentos estar al nivel del Barça」(우리는 순간순간 바르사 수준에 있음을 보여줬다).
- 제목만 확인(본문 차단): Mundo Deportivo 「Tenemos que saber competir mejor」(더 잘 경쟁할 줄 알아야 한다) · SPORT 「El Barça ha aprovechado nuestros errores」(바르사가 우리 실수를 이용했다) · MARCA 「Este partido, contra uno de los favoritos, nos da información para ser mejores」(우승 후보 중 하나와의 이 경기가 더 나아질 정보를 준다) · Cadena SER · ABC 회견 기사.
- **플릭 — SB Nation**(Yahoo · 본문): 「we were in the right position and we pressed them well, and they made this mistake and we used it」(올바른 위치에서 잘 압박했고, 그들이 실수했고 우리가 이용했다) · **Europa Press**(Infobae · 본문): 「Hemos estado muy compactos, la última línea ha jugado a un nivel increíble」(아주 콤팩트했고 최종 수비라인이 놀라운 수준이었다). 독일어 Stimmen 0건(laola1·audimax·fussballdaten만 검색됨).
- **물었던 네 가지**: 고메스 오른쪽·카마라 왼쪽 배치 이유 **0** · 야말 대응 언급 **0**(경기 후 발언에 「Lamine」 없음) · 카마라·만잠비·잭슨·부엔디아·마첸 평가 **0** · 62′ 3인 교체 이유 **0**.

### ⑵ Jacob Tanswell

- X 직접 접근 실패(x.com 402 · xcancel 451). 검색 요약으로 10-31 트윗(캐시 대체는 「after Barcelona」(바르셀로나전 뒤에) 결정 — 에메리 전달)만 확인. 경기 후 트윗·The Athletic 경기 후 기사 **0건** — D+2에서 재시도.

### ⑶ 필수 3채널 영상 — 전사 3편 · 요약·구현 주장 적재

| 채널 | 영상 | 게시 | 요약 | 구현 주장 |
|---|---|---|---|---|
| UTV | 「ASTON VILLA LACKED BELIEF AGAINST BARCELONA」 `WaquXcu6cm8` | 11-04 라이브 · 17분 | 패인 = 「lacked belief」(믿음 부족) · 선발이 「conservative」(보수적) · 마첸 8점 「stepped up to the challenge of Lamine」(라민 야말이라는 과제를 감당했다) · 고메스 4점 · 잭슨 「ran the channel well」(채널을 잘 뛰었다) | 2행: 측면 인선(윙어) PENDING #6 · 잭슨 채널 PENDING #4 |
| 1874 | 「Barcelona 3-0 Aston Villa \| Villa Fall Short At The Nou Camp」 `qe6-ojk1MG8` | 11-04 라이브 · 33분 | 7′ 실수는 고메스 「complete brain fade」(완전한 정신줄 놓기) · 짧은 배급은 지시된 방식 · 윙어 없는 선발이 역습 출구를 없앴다 · 최고 카마라·마첸 | 5행: 짧은 골킥 HELD #52 · 측면 인선 PENDING #6 · 만잠비 투톱 압박 HELD #15 · 빌드업 역습 HELD #1 · 바클리 6번 HELD #50 |
| UTV | 「BARCELONA v ASTON VILLA \| LIVE CHAMPIONS LEAGUE WATCHALONG」 `IgwcExm5Xms` | 11-03 라이브 · 2시간 28분 | 라인업 때 만잠비 10번·부엔디아 LM(야말 협력 수비용) 예상 · 4-3-3 압박 → 4-4-2 블록 · 잭슨 채널 침투 6회 언급 · 「These corners are posing them all sorts of problems」(우리 코너가 상대에게 온갖 문제를 일으킨다) | 5행: 비보유 형태 HELD #15 · 2선 배치 HELD #21 · 야말 대응 NA · 잭슨 채널 HELD #5 · 강팀 원정 구상 HELD #2 |

- The Villans: 경기 후 영상 **0편**(조회 13:10 KST · 최신은 경기 전 「Can Aston Villa Stop Lamine Yamal…」 `Ttk_jjW5KkU`) — D+2에서 재조회.
- 경기 귀속은 색인 규칙이 못 잡아 `_video_overrides.json`에 report 66으로 적었다. 전 편 auto-caption — 인용은 confidence에 auto-caption.
- 오인식 대조: 「Matson」= 마첸 · 「Gomez/Xiao Gomez」= 주앙 고메스 · 「Buender/Bender」= 부엔디아 · 「McInn」= 맥긴 · 「And Bay/Embi」= 음바예 · 「Leml/Lamin」= 야말. 1874 [25:24] 「Garnacho」는 출전하지 않은 선수라 요약에서 뺐다.

### ⑷ 다국어 기사 — 새로 확보

- **독일어 · audimax.de**(Christoph Greiner · 11-04 · 본문): 「Villa setzte im Mittelfeld auf dieselbe Manndeckung, mit der bereits Real Madrid und PSG angetreten waren」(빌라는 미드필드에서 레알 마드리드·PSG가 썼던 것과 같은 대인 마크를 택했다) — EFE 「marcajes individuales a Rodri y Pedri」(로드리·페드리 대인 마크)와 같은 방향(독립 매체 2곳).
- **스페인어 · VAVEL España**(11-04 · 본문): 「Las llegadas de Matty Cash, João Gomes y Nicolas Jackson」(캐시·고메스·잭슨의 침투) · 「llegaron a generar acciones peligrosas a balón parado」(세트피스로 위협적인 장면을 만들었다).
- **스페인어 · EFE 크로니카**(Infobae · 요약 기준): 경고 마첸 11′ · 부엔디아 31′ · 잭슨 44′ — 야말 쪽 두 명이 31분 안에 모두 경고(간접 정황).
- **Goal 전술 보드 재게재**(LiveScore 등 · 요약 기준): 「Cash and Maatsen were told to stay home to counter Barcelona's wide men」(캐시와 마첸은 바르사 윙어 대응을 위해 자리를 지키라는 지시를 받았다).
- 제목만(본문 차단): El Periódico 「Un Barça opresivo se recompone en Europa ante el asustadizo Aston Villa」(억압적인 바르사가 겁먹은 빌라를 상대로 유럽에서 회복하다) · La Vanguardia 「Unai Emery: Un camaleón en su templo maldito」(우나이 에메리: 저주받은 신전의 카멜레온).
- **카탈루냐어 0건**: VilaWeb·3Cat/Esport3·RAC1 — 검색어 「crònica Lamine Raphinha Emery Kamara」·「anàlisi tàctica」·「roda de premsa」·「pressió」. Relevo·El País 경기 후 기사 0. MD·SPORT·AS·MARCA·El Periódico는 검색·WebFetch 모두 차단.
- 영어 전술 블로그(TFA·BTL·Coaches' Voice·Spielverlagerung·7500 to Holte) **0건**.

### ⑸ 09:30 회차 결손 점검

- 출전 16명 전원: 국면 그리드(점유·비점유) · SS 운반 `carries_ss` · `match_player_reports` 다섯 칸 모두 채워짐 · G21(SS 확장·FotMob·WS JSON) 통과 — **채울 결손 없음**.

### ⑹ 관전 메모 가설 — D+1 재대조

| # | D0 | D+1 근거 | D+1 판정 |
|---|---|---|---|
| R4-H(고메스 RDM = 야말 대응) | 부분 일치 | 에메리 경기 후 발언 7곳에 배치·야말 언급 0 · 2차 서술은 「부엔디아·마첸 협력 수비」(UTV 워치얼롱)·「캐시·마첸 자리 지키기」(Goal)만 말하고 카마라 배치는 말하지 않는다 · 실측은 카마라 주변 상대 페르민 5·야말 5 | **부분 일치 유지** — 카마라가 야말 쪽 수비에 가담한 것은 실측으로 일치, 설계 의도는 1차 발언 0으로 미확인. 스페인어 회견 기사 본문(MD·SPORT·MARCA·SER·ABC) 미열람 — D+2·D+3 재시도 |
| H2(잭슨 채널 침투) | 부분 일치 | UTV 「ran the channel well」(채널을 잘 뛰었다) · 워치얼롱 채널 침투 6회·내려와 받기 0 · EFE 「muchos balones en largo para que Nicolas Jackson se la jugara con la pareja de centrales」(잭슨이 센터백 둘과 맞붙도록 롱볼을 많이 보냈다) · 에메리 「nos ha costado mucho ganar duelos con sus centrales」(센터백과의 듀얼이 힘들었다) | **부분 일치 유지** — 채널·롱볼 표적은 서사 3곳 일치, 「내려오지 않음」은 시즌 평소 수준(9%→11%) |
| R2(세트피스) | 리서치 덧붙임 | 빌라 코너 8(맥긴 3 · 부엔디아 1 · 음바예 4) → 슈팅 3(8′·9′·68′) · 워치얼롱 「These corners are posing them all sorts of problems」(코너가 상대에게 온갖 문제를 일으킨다) vs 1874 「set piece delivery … really poor」(세트피스 전달이 아주 나빴다 · 초반 이후) | 서사가 갈린다 — 실측은 초반 2개(8′·9′)와 음바예 4개 중 1개만 슈팅. 판정은 [세트피스 리서치](../research/2026-11-04-avl-set-pieces.md) 축에서 |
| H1·H1′·H1″·H3·R1·R1′ | — | 새 1차 근거 없음(영상 3편 모두 좌우 교대·만잠비 LM/CAM 비교를 말하지 않음 · 워치얼롱 [01:26:54] 「Manzambi is the one that's running off Jackson」(만잠비가 잭슨 주변을 도는 쪽) = CAM 정합) | D0 판정 유지 |

- DB: `match_hypotheses` D1 2행(#201 R4-H · #202 H2 · supersedes #194·#195) · `match_videos` 3편 요약 · `video_impl_claims` 12행.
- ⛔ 정본(slot_canon_roles·team_tactic_setups·opt 처방) 변경 없음 — 구현 함의(3선 좌우·잭슨 채널 포커스·측면 인선)는 사용자 판단 대기.
- 다음: D+2(11-05 20:00 `mw-avl-barcelona-d2`) — The Villans 경기 후 영상 · Tanswell · 스페인어 회견 기사 본문 · 전술 블로그 · R4 재판정.

## D+2 추적 (2026-11-05)

> **결론: R4(고메스 오른쪽 배치)의 이유를 에메리 본인이 말했다.** 경기 후 회견에서 The Athletic Jacob Tanswell이 직접 물었고, 답은 「비보유 높이 차 — 고메스는 높게 페드리, 카마라는 낮게 페르민」이다. R4-H 판정(부분 일치)은 유지하되 **감독이 꼽은 짝은 야말이 아니라 페르민**이다.

예약 회차 `mw-avl-barcelona-d2`(iMac). 조회 2026-11-05 KST · 기사·회견 다국어 검색은 서브에이전트 위임(읽기 전용) · 유튜브는 사이트 내부 검색(업로드 = 이번 주) · 전사는 yt-dlp 3편 성공 후 429 → 브라우저 timedtext 경로(뮤트 · 포착 즉시 정지) · 전 편 auto-caption.

### ⑴ 감독 회견 — 새로 확보한 원문

| 화자 · 출처 | 원문 | 번역 |
|---|---|---|
| ⭐ 에메리 · 공식 회견(Mundo Deportivo 영상 [VBYGCVbdxfk](https://www.youtube.com/watch?v=VBYGCVbdxfk) [03:18] · Tanswell 질문) | 「different heights mainly when we were without the ball because we needed to press with Jo higher with Pedri and lower with Kamara with Fermín and after it more or less with the ball they have the same task」 | 주로 볼이 없을 때 높이가 달라서다. 고메스는 더 높이 페드리를, 카마라는 더 낮게 페르민을 압박해야 했다. 볼을 가졌을 때는 임무가 거의 같다 |
| 에메리 · 같은 회견 [03:48] | 「before as well he lost very easy two balls before this mistake」 | 그 실수 전에도 공을 아주 쉽게 두 번 잃었다(고메스) |
| 에메리 · 같은 회견 [04:18] | 「we want to attract them to play for the 10 numbers」 | 상대를 끌어내 10번들에게 주려 한다(짧은 빌드업 의도) |
| 에메리 · 같은 회견 [04:50] | 「we must be ready when we are changing the position right or left」 | 오른쪽·왼쪽으로 자리를 바꿀 때도 준비돼 있어야 한다 |
| 에메리 · 구단 공식 인터뷰([D5LNiRkdSPU](https://www.youtube.com/watch?v=D5LNiRkdSPU) · avfc.co.uk 본문 일치) | 「We played the first half like we planned.」 | 전반은 계획대로 했다 |
| 에메리 · Futbolfrances(Movistar+ 표기 · 재가공 의심 · LOW) | 「La imagen que hemos ofrecido es consecuencia directa de nuestros errores」 | 우리가 보인 모습은 우리 실수의 직접적 결과다 |
| 플릭 · Goal es-mx(Mundo Deportivo 전재 · 검색 요약) | 「Queríamos presionarlos, obligarlos a cometer errores, y de ahí llegaron los goles.」 | 그들을 압박해 실수를 강요하려 했고 골은 거기서 나왔다 |

- 선수 평가(카마라·마첸·부엔디아·잭슨·만잠비)·62′ 3인 교체 이유·야말 대응 발언은 **여전히 0**. 회견 [06:52] 「throwing the young wingers on」(어린 윙어들을 넣은 것) 질문에는 「never give up」(포기하지 않는다) 태도만 답했다.
- 맥긴(TNT · 검색 요약): 「a huge learning curve for us」(우리에게 큰 배움) — 전술 의도 없음.

### ⑵ 유튜브 — 8편 전사·요약·구현 주장 14행

| 채널 | 영상 | 언어 | 핵심 | 구현 주장 |
|---|---|---|---|---|
| Mundo Deportivo | 에메리 회견 `VBYGCVbdxfk` | en | R4 1차 이유(위 표) · 짧은 빌드업 = 10번 연결 의도 | 2행: 3선 좌우 배정 HELD #20 · 짧은 빌드업 의도 HELD #52 |
| AVFC 공식 | 에메리 인터뷰 `D5LNiRkdSPU` | en | 전반 계획대로 · 실수는 스타일의 일부 | 주장 없음 |
| UTV(+The Villans) | 「WHY EVERYONE MUST LEARN FROM THIS BARCELONA DEFEAT」 `Cx3glX3RMvQ` | en | 마첸 최고(지상 경합 10/16 · 야말 상대 우위) · 고메스 터치 25 · 「he was on the opposite side … press resistant to Pedri and Lopez」(반대쪽에 서서 페드리·페르민 상대로 압박을 견뎌야 했다) · 맥긴 터치 30·손실 16 · 빌드업은 방식이 아니라 실행 문제 | 2행: 측면 인선 PENDING #6 · 빌드업 유지 HELD #52 |
| 1874 | 「What Did Aston Villa Really Get Wrong In Barcelona?」 `GJpKfDnl56Q` | en | 7′ 실점이 계획을 무너뜨림 · 「He traded Kamara and Gomez. Jacob wrote about it in The Athletic this morning.」(카마라와 고메스를 맞바꿨다. 제이콥이 오늘 아침 The Athletic에 썼다) · 6대6 돌파 시 수적 이점 · 윙어 0명 선발 비판 | 2행: 좌우 교대 해석 HELD #20 · 측면 인선 PENDING #6 |
| Bains Analysis(비빌라) | 「Aston Villa Lost 3-0… But Emery Got A LOT Right」 `pZNrIGvVouE` | en | 만잠비 = 로드리 담당 · 카마라를 야말 쪽에 둔 미세 조정 · 야말은 비교적 묶였다 · 잭슨 채널·버티기 좋고 판단 아쉬움 | 3행: 비보유 4-4-2·만잠비–로드리 HELD #15 · 좌우 교대 HELD #20 · 잭슨 PENDING #4 |
| Albert Blaya Sensat(바르사 · es) | 「ESTE SÍ es el BARÇA de FLICK」 `7ol9Nnb4VIU` | es | 빌라 계획 = 파리냐스에게 시간을 줘 야말이 등진 채 멀리서 받게 + 1대1 매치업 · 전반 빌라 기회 우위 → 후반 바르사 구조 변화 | 1행: 「고메스–페르민」 매치업 **REJECTED**(감독·실측과 충돌) |
| GOAT理論 切り抜き(ja) | 「【CL分析】バルセロナ戦の鈴木彩艶の評価…」 `a52qNaoJIQE` | ja | 골 기준 존 수비 · 페르민 안쪽 침투 추적·야말 컷인 오프사이드 · 측면이 수비에 묶여 역습 인원 부족 · 와이드 공략 전술 없음 | 1행: 역습 인원 HELD #2 |
| 1874(경기 전) | Tanswell 현지 리포트 `Ud2cwU17zoU` | en | [13:13] 카마라·고메스 교대 예상(적중) · 풀백은 박스 폭 바깥에서 수비하지 않는다 | 2행: 풀백 수비 폭 HELD #15 · 교대 예상 HELD #20 |

- 귀속: `_video_overrides.json`에 report 66으로 8편 추가(Ud2cwU17zoU 메타는 `_meta_backfill.json`). 전 편 auto-caption — confidence 명기.
- ⚠️ 1874 `GJpKfDnl56Q`의 en 자막은 번역 경유로 보인다(어순·인명 「Juan」「Jamal」 오류) — 인용은 뜻 위주. Bains는 야말 상대 풀백을 「Matty Cash」, 고메스를 「Diego Carlos」로 말했다(화자 혼동 — 실측은 마첸·고메스).
- 필수 3채널: UTV 1편(The Villans 공동 게시 — The Villans 단독 경기 후 영상은 0) · 1874 1편 새로 · 1874 프리뷰 적재. 미전사(우선순위 밖): Diario AS 회견 풀영상 `mMDcKjDgnTc`(51분 · 플릭+에메리) · La pizarra del profe `-hnKnJnnNug` · Dibra Táctica `yzD4PG0udZM` · Zona 14 Culer `i0yybsqebjA` · The Claret & Blue `qMhayTq84Gg` · Every Week We Follow `HHfn6Bglk9E`.

### ⑶ 기사 — 새로 확보(서브에이전트 · 본문 열람 여부 표기)

- **Squawka 경기 후 분석**(11-04 · 403 · 검색 발췌만): 「Fermin Lopez's movement kept Boubacar Kamara pinned inside, as his job was to protect the space behind Maatsen incase Lopez made an underlapping run between Torres and Maatsen」(페르민의 움직임이 카마라를 안쪽에 묶었다. 카마라의 임무는 페르민이 토레스와 마첸 사이로 안쪽 침투할 때 마첸 뒷공간을 지키는 것이었다) — 감독 발언(카마라–페르민)과 같은 그림. 만잠비는 로드리를 「main marking reference」(주 마킹 기준)로 맡음.
- **Guardian Barney Ronay**(Irish Times 전재 · 본문): 「Emery picked a team to press and stifle the space」(에메리는 압박하고 공간을 질식시킬 선발을 골랐다).
- **Claret Villans**(LiveScore · 본문): 「They played short from a goal kick, with Barcelona primed and ready to close them down」(골킥을 짧게 찼고 바르사는 덮칠 준비가 돼 있었다).
- **Roundtable/Dan Bardell**(Yahoo · 본문): 「Boubacar Kamara and Ian Maatsen were our two standout performers」(카마라와 마첸이 가장 돋보였다).
- **EFE 「5 claves」**(Infobae · 본문): 「El propio Lamine Yamal presionó como nunca」(야말 자신이 전례 없이 압박했다).
- **평점**: Villa News 고메스 3·카마라 5·마첸 5 / Stadium Rant 고메스 4·카마라 6.5·마첸 4.
- ⚠️ 1874 [06:24]가 말한 **The Athletic Tanswell 11-04 기사**(좌우 교대 다룸)는 nytimes.com 접근 불가로 미열람 — D+3 재시도.

### ⑷ 가설·당일 판정 재판정

| # | 이전 | D+2 근거 | D+2 판정 |
|---|---|---|---|
| R4-H(교대 = 야말 대응) | 부분 일치(D0·D1) | 에메리 1차: 고메스–페드리(높게) · 카마라–페르민(낮게) · Squawka 같은 그림 · Bains·1874는 「야말 쪽」 해석 · 실측 카마라 주변 상대 페르민 5·야말 5 | **부분 일치 유지 — 이유 확정**: 같은 쪽 매치업 설계는 맞고, 감독이 꼽은 짝은 페르민 |
| H1″(고메스가 살짝 높게) | 일치 | 에메리 「press with Jo higher」(고메스를 더 높게) | **일치 — 의도된 배정으로 확인** |
| H2(잭슨 채널) | 부분 일치 | Bains 채널·버티기 · GOAT 투톱 고립 · Squawka 잭슨 오른쪽 치우침 | 부분 일치 유지 |
| H1·H1′·H3·R1·R1′ | — | 새 1차 근거 없음 | 유지 |

- **당일 판정 정정 1건**: §8 R4 「확인된 이유(1차 발언): 없음」과 D+1 「에메리 발언 7곳 배치 언급 0」 → **1차 이유 있음**(위 회견). 판정값은 바뀌지 않는다 — obs#1157 · `match_hypotheses` D2 3행(seq 3·4·5 · supersedes 최신 행).
- 상충 기록: Blaya(바르사 분석가)는 「고메스–페르민」이라 했다 → 감독 발언·실측과 어긋나 기각(구현 주장 REJECTED).
- ⛔ 정본(슬롯 역할·팀 전술·선발 처방) 변경 없음. 정리된 비보유 중원 매치업 **만잠비–로드리 · 고메스–페드리 · 카마라–페르민**은 상대 10번 위치에 맞춘 1경기 배정이다 — 쟁점 #20(피벗 분업) 근거로 쌓고, FC 구현 함의(상대에 따라 높은 쪽 DM을 바꾸는 운용)는 사용자 판단 대기.

### ⑸ 0건·실패와 검색어

- The Athletic 경기 후 기사(Tanswell·Corrigan·Ballús) 미열람 · La Vanguardia 「camaleón」·El Periódico 「Un Barça opresivo」 전재처 0 · Birmingham Mail/Live·7500 to Holte·Blaugranes·Culemanía·Relevo·El País·TFA·Between the Lines·Coaches' Voice·Spielverlagerung 0 · Cadena SER·ABC 회견 전문 0 · 독일어(kicker·Sport1·Bild 「Flick Aston Villa」·「Stimmen」) 0 · 포르투갈어 ge.globo 0 · 카탈루냐어(「anàlisi Barça Aston Villa pressió sortida」·「Emery Lamine pla anàlisi tàctica」) 0.
- 유튜브 검색어(이번 주 필터): 「aston villa barcelona」 · 「1874 aston villa」 · 「UTV aston villa」 · 「the villans aston villa」(0) · 「barcelona aston villa tactical analysis」 · 「barça aston villa análisis táctico」 · 「barça aston villa anàlisi」 · 「emery barcelona press conference」 · 「flick aston villa rueda de prensa」 · 「aston villa barcelona kamara gomes」.
- 기사 검색어: 스페인어 「Emery Lamine Kamara izquierda planteamiento」·「Kamara a la izquierda Gomes derecha」·「rueda de prensa competir mejor」 · 포르투갈어 「João Gomes volante direita」 · 영어 「Kamara Yamal plan」·「Maatsen Yamal Kamara left side」·「Squawka」.
- 다음: D+3(11-06 20:00 `mw-avl-barcelona-d3` · complete 판정) — The Athletic Tanswell 11-04 기사 · Diario AS 회견 풀영상의 스페인어 문답 · 남은 스페인어 분석 영상.
