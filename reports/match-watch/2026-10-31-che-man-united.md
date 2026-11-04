# 2026-10-31 CHE vs Manchester United — 2-0 (첼시 홈 승)

> 수집일 2026-11-04(경기 후 D+4 · CHE 수집 보류 해제 첫 회차) · SofaScore event `16363904` · FotMob `5795498` · WhoScored `1983629`
> 프리미어리그 9라운드 · 스탬퍼드 브리지 · 주심 Peter Bankes · 첼시 홈 · 양 팀 4-2-3-1(SofaScore·FotMob·WhoScored 일치)
> 감독: 첼시 **사비 알론소** · 맨유 **마이클 캐릭** · 게임 버전 `core.game_version.live_on('2026-10-31')` = **FC27**
> 관전 메모: 없음

## 요약

- **2-0 홈 승 · 후반에 경기를 뒤집었다.** xG 3.01–1.24(FotMob · PK 1 포함) · 슈팅 19–12 · 유효 10–5 · 점유 58%(전반 50 · 후반 66).
- **전반은 맨유가 더 위험했다.** 전반 xG 0.44–1.15 · 맨유 빅찬스(브루노 19′ · 아마드 43′ 역습) · 34′ 쿠냐 골 VAR 취소.
- **하프타임 메시지 「공으로 이긴다」.** 알론소: 「we said we were going to win this game with the ball」(이 경기를 공을 가지고 이기자고 말했다). 후반 xG 2.57–0.09 · 자기 진영 패스 성공률 90~97%.
- **골은 라비아 회수에서**: 50′ 라비아가 음뵈모 공을 가로채 → 로저스 35야드 운반·칩샷 · 63′ 리산드로 두 번째 경고 퇴장 → 64′ 파머 PK(포파나가 얻음).
- **선발 4자리 변화**: 라비아(헨더슨 병) · 포파나(라크루아 햄스트링) · 팔레스트라(하토 허리) · 에스테방(PL 첫 선발 · 사전 통보) · 네투 임시 9번(주앙 페드루 부상).
- **높은 압박이 처음 실측으로 맞았다.** 첼시 PPDA 8.38 · 0–30′ 6.5~7.1 · 수비 액션 평균 높이(def_x) 43.1.
- **게임 구현: 시험 프리셋.** 4-2-3-1 Wide · Short Passing/Balanced/58(RULE) — 시즌 정본(3-4-2-1)과 달라 사용자 판단 대기(§7).

## 1. 경기 개요와 원천 수치

| 지표 | 첼시 | 맨유 | 출처 |
|---|---|---|---|
| 점유 | 58% | 42% | SofaScore·FotMob 동일 |
| xG(전체 / 오픈플레이 / 세트 / 논PK / xGOT) | 3.01 / 2.01 / 0.21 / 2.22 / 2.53 | 1.24 / 1.18 / 0.06 / 1.24 / 0.30 | FotMob 한 응답(동일 스냅샷) · PK 1(0.79) |
| 슈팅(유효) · 빅찬스 | 19(10) · 4 | 12(5) · 4 | SofaScore · 빅찬스 FotMob |
| 패스(성공) | 561(496) | 396(308) | SofaScore |
| 롱볼 | 17/38 | 14/46 | SofaScore |
| 경합 · 공중 · 드리블 | 59% · 12/21 · 8/19 | 41% · 9/21 · 4/12 | SofaScore |
| 코너 · 파울 · 경고/퇴장 | 8 · 8 · 1/0 | 7 · 20 · 6/1 | SofaScore |
| PPDA | **8.38**(310/37) | 14.71(412/28) | core.whoscored.ppda · WS 1983629 |
| 수비 액션 평균 높이(def_x) | 43.1 | 35.4 | core.whoscored.수비 액션 평균 높이(def_x) |

- 하프별(FotMob): 전반 점유 50% · xG 0.44–1.15 · 슈팅 8–9 / 후반 점유 66% · xG 2.57–0.09 · 슈팅 11–3. 하프별 PPDA(첼시·맨유) 전반 9.06·10.19 · 후반 7.74·20.75.
- 득점·판정: 34′ 쿠냐 골 VAR 취소(오프사이드) · 50′ 로저스(도움 라비아) · 59′ 리산드로 경고(로저스 역습 셔츠 반칙) · 63′ VAR → 리산드로 두 번째 경고 퇴장 + PK(포파나에게 팔 사용 · 두 반칙 사이 83초) · 64′ 파머 PK(첼시 PL 105경기 50호골) · 71′ 에스테방 골 VAR 취소(오프사이드). SofaScore 사건 분류의 VAR 표기(goalAwarded·penaltyNotAwarded)는 판독 사건 표시이고 결과는 스코어로 판정했다.
- 교체: 맨유 58′ 마이누↔발레바 · 66′ 헤븐·마운트 · 77′ 지르크지↔아마드(부상) · 79′ 5-3-2(WhoScored). 첼시 74′ 차바리아↔팔레스트라 · 87′ 귀스토↔에스테방 · 바르코↔네투 · 웰벡↔카이세도 · 90+7′ 퀜다↔파머.
- 경고: 맨유 6(리산드로 2 · 매과이어 · 마이누 · 음뵈모 · 지르크지) · 첼시 펜더스 90+3′(시간 끌기).
- 수집: SofaScore `/event/16363904{,/statistics,/incidents,/shotmap,/lineups,/managers,/graph,/average-positions}`(headless 200) · FotMob matchDetails 5795498 · WhoScored matchCentreData 1983629 **scope=full** → `reports/match-watch/data/2026-10-31-che-ws-1983629.json` 보존. 출전 16명 중 15명 SofaScore 평균 위치·히트맵 있음(퀜다 1분은 히트맵 없음).

## 2. 전술 설명

### 점유 구조·빌드업

- 4-2-3-1. WS 볼 소유 평균 위치(앞뒤, 좌우 · 0~100 · 좌우 0 = 첼시 오른쪽): 포파나 (35,29) · 콜윌 (33,64) · 라비아 (46,49) · 카이세도 (49,56) · 아체암퐁 (51,15) · 팔레스트라 (44,86) · 에스테방 (73,23) · 파머 (58,34) · 로저스 (66,62) · 네투 (69,50).
- **후방 3인 순환 + 높은 오른쪽 풀백**: 패스 연결 포파나→콜윌 18회 · 콜윌→포파나 16 · 포파나→아체암퐁 15 · 라비아→카이세도 14. 아체암퐁은 패스 60/65 · 전진 운반 187m · 수신 57로 오른쪽 전진 축이었다.
- 매체 서술 「점유 시 3-2-5」(Goal UK) · 「미드필더가 하프백처럼 내려옴」(Chelsea's Voice)은 **평균 위치로는 확정되지 않는다** — 아체암퐁(51)이 팔레스트라(44)보다 7 높은 비대칭은 실측과 맞는다. 형태 기록은 4-2-3-1로 두고 3-2-5는 서사로 남긴다.
- **라비아·카이세도가 아주 가깝게 섰다**(평균 위치 차 앞뒤 3 · 좌우 7 · Last Word on Football 「레버쿠젠식」과 일치). 라비아 패스 64/72 · 라인 브레이킹 패스 16.
- 오른쪽: 에스테방이 높고 넓게((73,23) · 박스 터치 12 · 크로스 8), 파머는 그 안쪽에서 연결((58,34) · 패스 46/55 · 수신 56). 왼쪽: 로저스가 하프스페이스로 좁혀((66,62)) 왼쪽 폭은 팔레스트라·차바리아.
- 네투 가짜 9번: 볼 소유 평균 위치 (69,50) · 수신 26(깊은 수신 17) · 알론소 「it's not new for him」(그에게 낯선 자리가 아니다).

### 비보유 구조·압박

- **4-4-2 높은 압박**: 첼시 PPDA 8.38(0–15′ 7.12 · 15–30′ 6.5) · 수비 액션 평균 높이(def_x) 43.1(맨유 35.4).
- 전반의 약점(Football365): 첼시 CB 하나가 끌려 나오면 앞선이 따라 나가고, 카이세도·라비아가 브루노·발레바에 붙으면 쿠냐·음뵈모가 수비진에서 바로 받았다 · 아마드가 팔레스트라 쪽 뒷공간을 쳤다.
- 하프타임 수정(Football365): **CB 하나가 음뵈모를 따라가고 공격수 하나가 맨유 미드필더에 붙었다.** 후반 맨유 xG 0.09.

### 전환·rest-defense·세트피스

- 50′ 선제골은 라비아의 중원 회수 → 로저스 운반(전환). 로저스: 「I knew it was a counter-attacking opportunity to drive and Estevao made the run on the outside.」(역습으로 몰고 갈 기회라는 걸 알았고, 에스테방이 바깥으로 뛰어줬다.)
- 전반 맨유 역습 2회(19′ 브루노 · 43′ 아마드 · xG 0.27·0.30) — 높은 압박 뒤 공간.
- 세트피스: 첼시 코너 8 · 세트 xG 0.21 · 63′ PK 장면도 코너 상황(포파나).

## 3. 전술적 특성

- **강점**: 라비아의 회수·연결(리커버리 14 · 태클 5 · 인터셉트 4 · FotMob 8.9 POTM) · 후방 3인 순환(패스 성공률 88%) · 에스테방 오른쪽 1대1·박스 침투 · 로저스 왼쪽 안쪽 운반.
- **약점**: 전반 높은 압박 뒤 공간(맨유 전반 xG 1.15) · 팔레스트라 쪽 수비(아마드 표적) · 포파나 전반 실수 2(ES).
- **상대가 만든 교란**: 캐릭의 맨유는 4-2-3-1 지역·대인 혼합 · 브루노 역습 출발 · 음뵈모·아마드 출구. 63′ 퇴장 뒤 4-4-1 → 79′ 5-3-2로 내려섰다.
- **기존 프로필·직전 경기와 비교**: 스퍼스전(10-24) 대비 9번(로저스→네투) · 3선(헨더슨→라비아) · 오른쪽(퀜다→에스테방) · CB(라크루아→포파나) · LB(하토→팔레스트라). 압박 높이가 PPDA 15.66 → 8.38로 바뀌었다.

## 4. 경기 중 변화

1. **0–29′ 높은 압박 · 주고받기**: PPDA 6.5~7.1 · 모멘텀 4–13′ +19.5 · 16–20′ +16.6. 19′ 브루노 역습 슈팅(xG 0.27).
2. **29–45′ 맨유 우세**: 29–36′ 모멘텀 −53.5(경기 최저) · 30′ 쿠냐 슈팅 골라인 블록 · 34′ 쿠냐 골 취소 · 43′ 아마드 역습(xG 0.30). 첼시 수비 액션 평균 높이(def_x) 31.7로 밀렸다.
3. **46–63′ 하프타임 수정 · 「공으로 이긴다」**: 45–50′ 수비 액션 평균 높이(def_x) 56.6 · 자기 진영 패스 성공률 90~97% · 50′ 로저스 골 · 51′ 네투 역습 슈팅. 알론소 「The first 15 minutes of the second half we were in good control.」(후반 첫 15분은 잘 통제했다.)
4. **63–74′ 수적 우위**: 63′ 퇴장 · 64′ 파머 PK 2-0 · 64–74′ PPDA 4.71로 계속 눌렀다.
5. **74′–종료 관리**: 74′ 차바리아 · 87′ 3명 교체(웰벡 투입으로 투톱 · Goal UK) · 90′ 바르코 슈팅(xG 0.51) 빗나감.

## 5. 선수별 분석 — 출전 선수 전원

좌표: SS 평균 위치(앞뒤, 좌우 · 0~100 · 좌우 0 = 첼시 오른쪽). 평점은 SofaScore.

| 선수 | 위치·실제 역할 | 분/평점·핵심 스탯 | 평균 위치 | 특성·수행 | FC 역할/포커스 함의 |
|---|---|---|---|---|---|
| 펜더스 | GK | 90 · 7.3 · 선방 3 · 패스 19/25 · 롱볼 4/10 | SS 평균 위치 (8,48) | 막판 음뵈모 중거리 크로스바로 쳐냄 · 무실점 · 90+3′ 경고 | 1위 gk_goalkeeper/Defend(Δ.035 무결정) |
| 아체암퐁 | RB · 높은 전진 축 | 90 · 8.3 · 패스 60/65 · 전진 운반 187m · 리커버리 10 | SS 평균 위치 (48,17) | 쿠냐 수비 · 에스테방과 연계 · 「most alert defender」(가장 깨어 있던 수비수 · ES) | 1위 fb_att_wb/Support(Δ.079) |
| 포파나 | RCB | 90 · **8.6** · 패스 67/76 · 인터셉트 5 · 라인 브레이킹 패스 17 | SS 평균 위치 (35,31) | 전반 아마드에게 뚫림(평가 4~8.1로 갈림) · 63′ PK 획득 | 1위 cb_bpd/Aggressive(Δ.085) |
| 콜윌 | LCB | 90 · 7.7 · 패스 61/66 · 공중 4/5 | SS 평균 위치 (31,63) | 크로스 헤더 · 빌드업 축 | 1위 cb_bpd/Aggressive(Δ.027 무결정) |
| 팔레스트라 | LB(오른발) · PL 첫 선발 | 74 · 6.8 · 경합 5-4 | SS 평균 위치 (38,79) | 전반 아마드 표적 · 후반 나아짐 | 1위 fb_wingback/Support(Δ.037 무결정) |
| 라비아 | RDM · 회수·연결 | 90 · 7.9 · 도움 1 · 리커버리 14 · 태클 5 · 인터셉트 4 · 패스 64/72 | SS 평균 위치 (45,50) | POTM(FotMob 8.9) · 50′ 음뵈모 공 가로채 도움 · 알론소 「a top, top performance」(최고 수준의 경기) | 1위 dm_dlp/Roaming(Δ.239) |
| 카이세도 | LDM · 주장 | 87 · 7.5 · 패스 54/57 · 롱볼 4/4 | SS 평균 위치 (49,56) | 패스 94% · 포파나 헤더 굴절 골대 | 1위 dm_dlp/Roaming(Δ.064) |
| 에스테방 | RM · 높고 넓게 · PL 첫 선발 | 87 · 7.9 · xA 0.43 · 키패스 3 · 박스 터치 12 · 크로스 2/8 · 전진 운반 214m | SS 평균 위치 (70,24) | 두 골 오프사이드 취소 · 슈팅 6(9라운드 최다 · FFS) | 1위 wm_winger/Attack(Δ.072) |
| 파머 | CAM · 오른쪽 안쪽 연결자 | 89 · 7.2 · 1골(PK) · 키패스 3 · 수신 56 · 전진 운반 124m | SS 평균 위치 (58,34) | 깊이 내려와 받음(FFS) · 피벗 상시 패스 옵션(LWOF) | 1위 cam_halfwinger/Balanced(Δ.036 무결정) |
| 로저스 | LM · 왼쪽 하프스페이스 | 90 · **8.4** · 1골 · xG 0.65 · 키패스 3 · 박스 터치 7 · 전진 운반 95m | SS 평균 위치 (62,62) | 50′ 35야드 운반·칩샷 · 59′ 리산드로 첫 경고 유도 | 1위 wm_wideplm/Attack(Δ.135) |
| 네투 | ST · 임시 가짜 9번 | 87 · 7.1 · xG 0.42 · 패스 21/22 · 깊은 수신 17 | SS 평균 위치 (68,49) | CB를 묶고 내려와 로저스·파머 관여를 엶 · 박스 존재감 부족 | 1위 st_false9/Build-Up(Δ.024 무결정) |
| 차바리아 | 74′ · LB | 16 · 6.9 · 키패스 1 | SS 평균 위치 (57,87) | 파머 기회 1회 창출(ES) | 45분 미만 |
| 귀스토 | 87′ · 오른쪽 | 13 · 6.8 · 키패스 1 | SS 평균 위치 (61,9) | — | 45분 미만 |
| 바르코 | 87′ · 중앙 | 13 · 6.2 · xG 0.51 | SS 평균 위치 (48,43) | 90′ 빅찬스 빗나감 | 45분 미만 |
| 웰벡 | 87′ · ST(투톱) | 13 · 6.4 | SS 평균 위치 (52,31) | — | 45분 미만 · 히트맵 부족 |
| 퀜다 | 90+7′ | 1 · 평점 없음 | SS 평균 위치 (29,94) | — | 히트맵 없음 · 처방 행 없음 |

## 6. 전술 변화 판정

- **유지된 것**: 4-2-3-1 · 로저스 왼쪽 안쪽 · 오른쪽 풀백 아체암퐁.
- **새로 나타난 것**: ⑴ 라비아·카이세도 가까운 2인 3선 ⑵ 네투 임시 9번 ⑶ 에스테방 오른쪽 폭 ⑷ 높은 압박(PPDA 8.38 · 이번 시즌 브렌트퍼드전과 같은 최저 수준).
- **하프타임 수정**: CB 하나가 음뵈모 대인 · 공격수 하나가 맨유 미드필더에 붙음(Football365) — 알론소는 「We changed some tactical things」(전술적인 것 몇 가지를 바꿨다)라고만 했다.
- **`manager_profiles` 반영**: pressing·role_demands 축에 덧붙임.

## 7. 게임 구현 판정

- 결론: **시험 프리셋**
- **이 경기 전용 팀 설정**: FC27 · 4-2-3-1 Wide · **Short Passing / Balanced / 58** · tactic_code 없음 · rule_note RULE — `core.team_settings.suggest(점유 58, 패스 561, 롱볼 시도 38, PPDA 8.38)` → Short Passing/Balanced/55~62(롱볼 6.8%) · compare() 차이 0. 보유 4-2-3-1 · 비보유 4-4-2.
- **이 경기 선발 11명**(단일 경기 커널 1위 · SofaScore 히트맵 · 무결정 = Δ≤.05):

| 슬롯 | 선수 | 역할/포커스 | fit | Δ | 2위 |
|---|---|---|---|---|---|
| GK | 펜더스 | gk_goalkeeper/Defend | .957 | .035 무결정 | gk_goalkeeper/Balanced |
| RB | 아체암퐁 | fb_att_wb/Support | .901 | .079 | fb_wingback/Balanced |
| RCB | 포파나 | cb_bpd/Aggressive | .921 | .085 | cb_bpd/Build-Up |
| LCB | 콜윌 | cb_bpd/Aggressive | .902 | .027 무결정 | cb_bpd/Build-Up |
| LB | 팔레스트라 | fb_wingback/Support | .902 | .037 무결정 | fb_wingback/Balanced |
| RDM | 라비아 | dm_dlp/Roaming | .891 | .239 | dm_dlp/Defend |
| LDM | 카이세도 | dm_dlp/Roaming | .867 | .064 | dm_dlp/Build-Up |
| RM | 에스테방 | wm_winger/Attack | .771 | .072 | wm_winger/Balanced |
| CAM | 파머 | cam_halfwinger/Balanced | .586 | .036 무결정 | cam_classic10/Versatile |
| LM | 로저스 | wm_wideplm/Attack | .790 | .135 | wm_widemid/Build-Up |
| ST | 네투 | st_false9/Build-Up | .552 | .024 무결정 | st_false9/Attack |

- 무결정 5칸 — 세 경기 중 가장 적다(결정 6칸). 라비아 RDM dm_dlp/Roaming은 Δ.239로 뚜렷하다.
- **왜 「시험 프리셋」인가**: 4-2-3-1 + 짧은 빌드업 + 높은 압박(Short Passing/Balanced/58)이 이번 시즌 첼시에서 처음으로 결과·내용과 함께 맞았다. 시즌 정본(projected #41 · 3-4-2-1 · Short Passing/Balanced/58)과 **팀 설정 3축은 같고 포메이션만 다르다**. 인게임에서 이 프리셋을 시험해 볼 가치가 있다 — 단 1경기라 정본 변경 근거는 아니다(§시즌 축 검토 · 사용자 판단 대기).
- `prescriptions`·`slot_canon_roles`·`team_tactic_setups` 변경: **없음**.
- ⚠️ 등급(불변규칙 12): 커널 적합만 썼고 「역할이 무엇을 한다」는 주장을 하지 않았다.

⚠️ 이 설정은 `match_game_setups`·`match_player_prescriptions`의 `MATCH ONLY` 프리셋이다. 전체 시즌 전술이나 대표 선수 역할에 자동 병합하지 않는다.

## 8. 영상·기사·감독 발언

조회 2026-11-04(경기 후 D+4 · 서브에이전트 위임 · 읽기 전용).

### 감독 1차 발언

- **알론소 — 경기 후(영어)** · NBC 10-31 · MEN 11-01: 「We struggled at times but it feels good to get the three points, to get a serious performance.」(때때로 고전했지만 승점 3점을 진지한 경기력으로 따내서 기분이 좋다.) · 「When we spoke at half-time, we said we were going to win this game with the ball」(하프타임에 이 경기를 공을 가지고 이기자고 말했다) · 「When you feel better with the ball, normally the better you are defending as well.」(공을 가졌을 때 편해지면 보통 수비도 좋아진다.)
- **알론소 — 네투** · Fantasy Football Scout 11-02: 「We need to be sometimes creative, sometimes try to find solutions with the players available and even Pedro, he has worked really hard in that position, it's not new for him.」(때로는 창의적으로 가용 선수로 해법을 찾아야 한다. 페드루도 그 자리에서 열심히 했고 낯선 자리가 아니다.)
- **알론소 — 에스테방**: 「We spoke after Tottenham and he knew that he was going to be playing tonight, today.」(토트넘전 뒤에 얘기했고 그는 오늘 뛸 것을 알았다.) · 포르투갈어(Terra · 번역 보도) 「Vamos precisar dele o ano todo.」(1년 내내 그가 필요할 것이다.)
- **알론소 — 라비아** · ESPN: 「Sometimes the head is more important than the legs and now his head is in a good place.」(때로는 다리보다 머리가 중요하다. 지금 그의 머리는 좋은 상태다.) · 스페인어(Goal es-mx · 번역 기사) 「fue siempre el nexo de unión entre la línea defensiva y los jugadores ofensivos」(그는 늘 수비 라인과 공격 선수 사이의 연결고리였다) — ⚠️ 영어 회견 번역(교차검증 아님).
- **알론소 — 결장 사유**: 라크루아 「Max, he picked up an injury ... he will be a few weeks out」(맥스는 부상을 당했고 몇 주 결장한다) · 하토 「Jorrel, no, but Pep Chavarria is back in the squad」(조렐은 안 되고 펩 차바리아는 명단에 복귀한다).
- **캐릭** · The People's Person(NBC 경유): 「We could've, should've been up really first half.」(전반에 앞서 있었어야 했다.) · 「Bad goal to concede then penalty and we're up against it.」(나쁜 실점 뒤 페널티까지 내주면서 궁지에 몰렸다.)

### 기사·전술 서술

- **Goal UK 전술판**(Mohamed Saeed · 10-31): 유동적인 4-2-3-1 · 점유 시 3-2-5 · 윙어를 높고 넓게 둬 맨유 풀백이 안으로 좁히지 못하게 함 · 맨유 퇴장 뒤 4-4-1.
- **Chelsea's Voice**(Substack · 11-02): 점유 시 미드필더가 하프백처럼 내려옴 · 비점유 4-4-2 미드블록 · 네투는 깊이 내려오는 유동적 CF.
- **Football365**(Dharnish Iqbal · 11-02): 전반 압박 뒤 공간 노출 → 하프타임에 CB 하나가 음뵈모 대인. ⚠️ 「백5·네투 윙백」 표기는 소수(A Bola·NBC 라이브블로그 포함) — 실측(네투 볼 소유 평균 위치 (69,50))과 맞지 않아 **기각**.
- **Last Word on Football**(Alex Richards): 카이세도–라비아를 매우 가깝게(레버쿠젠식).
- **Trivela**(포르투갈어 · Pedro Ramos): 「Estêvão contradiz análise de Alonso」(에스테방이 알론소의 분석을 반박하다) — 강도 적응을 이유로 출전을 아꼈던 알론소 판단을 경기력으로 반박.
- **Calciomercato**(이탈리아어 · 팔레스트라): 「Prima da titolare per l'esterno dei Blues classe 2005」(2005년생 블루스 측면 자원의 첫 선발).

### 미수행·0건과 사유

- The Athletic · Football.London 원문 · 전술 분해 유튜브: **0건**. 회견 영상(`5-TKy3DOGXo`) 자막은 HTTP 429 — 설명란 기준.
- 모국어: 알론소 스페인어 원어 기사 0 · 독일어 0 · ge.globo 0(Trivela·Terra로 대체) · Record 0 · 라비아 프랑스어 0 · 펜더스 네덜란드어 0. 카이세도 에콰도르 스페인어(Primicias 등) 확보.

## 9. 데이터 반영과 한계

- DB 추가: `matches` #133 · `player_matches` 16 · `team_match_stats` 1 · `match_events` 21 · `match_shots` 31(SofaScore) · `match_period_stats` 2 · `match_momentum` 92 · `match_set_pieces` 26 · `match_phase_metrics` 57 · `match_reports` #69 · `match_player_reports` 16 · `match_game_setups` 1 · `match_player_prescriptions` 15(퀜다 1분 제외) · `match_tactical_changes`.
- 한계: ⑴ 63′부터 수적 우위 — 후반 지표는 그 효과를 포함한다. ⑵ 「3-2-5」는 평균 위치로 확정 못 함. ⑶ 웰벡·퀜다는 히트맵이 부족해 적합 계산 없음.
- 상태 `complete`.
