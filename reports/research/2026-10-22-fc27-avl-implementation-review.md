# FC27 기준 아스톤 빌라(에메리) 게임 구현 검토 + 구현용 데이터 충분성 재검토 (2026-10-22)

> 검토 시점 2026-10-22(바이킹전 D+1) · 현행 게임 버전 **FC27**(`core.game_version.current`) · DB 읽기만 했고 아무 행도 바꾸지 않았다.
> 근거 등급은 불변규칙 12(A=EA 1차 · B=데이터마이닝/fut.gg · C=통제 실측 · D=통설). 실측(SofaScore·WhoScored·FotMob)은 등급 축 밖이라 「실측」으로 적는다.
> 대상 자료: `team_tactic_setups` · `slot_canon_roles`(FC27) · `prescriptions opt:*`(FC27) · `fut_tactics`/`fut_tactic_roles`(인게임 pulled) · `match_game_setups`/`match_player_prescriptions` #51~#62 · `observations` #1040~#1113 · `game_system_changes` FC27 44행 · `reproduction_limits` FC27 14행 · docs/10·21·22·50 · core/team_settings.py · gates.py.

## 0. 한 줄 결론

- **팀 설정 3축(4-2-3-1 Wide · Balanced · Balanced · 52)은 인게임과 정본이 일치한다**(pulled `7ZTFKBu$37p7` 10-22 = #32 사용자 결정 10-15 = obs#1081). 다만 **「시즌 정본」을 뜻하는 행이 없다** — FC27 26/27에 `kind='optimal'` 행이 0이고, 「에메리 실축 구현 프리셋」이라는 이름을 단 #42는 Short Passing(폐기된 값)이다. docs/10 「게임 적용 정책」도 Short Passing을 적고 있다(낡은 문서).
- **슬롯 정본(slot_canon_roles FC27) 11칸 중 인게임 코드와 다른 칸이 3개**: LB(정본 att_wb/Support ↔ 인게임 윙백/Balanced) · RDM(정본 홀딩/Defend ↔ 인게임 DLP/Build-Up · obs#1080 테스트 중) · ST·LM 포커스(정본 Support/Balanced ↔ 인게임 Attack/Attack). 셋 다 「사용자 결정 대기」 상태라 **정본이 낡은 게 아니라 결정이 안 닫힌 것**이다.
- ⛔ **선발 처방 층(`prescriptions opt:*` starter=1 · FC27)은 낡았다** — 11칸 중 **7칸이 현재 선발과 다르고**(루헤리·완비사카·만잠비 부상 · 헤밍스 LM 선발 · 음바예 RM · 파우 토레스 비선발) **6칸이 슬롯 정본과 역할/포커스가 다르다**. G8+는 역할군만 보므로 통과한다. 이 층이 export돼 스쿼드 화면의 「선발」로 나간다.
- **인게임 검증 루프는 FC27에서 0회**: `ingame_captures` 75건 전부 FC26(마지막 09-10) · `v_kernel_fidelity` 13행 FC26. FC27 커널은 fut.gg 승계(B)만 있고 C등급 확인이 없다. 게이트 G1·G3·G5도 FC26만 검사한다.
- 데이터는 **팀 3축·슬롯 역할·국면 그리드**는 충분하고, **운반(carries)·비보유 형태 정형·세트피스 키커/타깃·FC27 선수 카드 축(PlayStyle·Role+ · 로스터 09-10 출시 전)·국면 분(5경기 결손)**이 부족하다. 이 PC에는 바이킹전 D+2·D+3 예약이 없어 **G34가 실패 중**이다.

---

## Part 1 — 구현 검토

### 1.1 팀 설정 3축 + 포메이션

| 축 | 슬롯 정본/시즌 행 | 인게임(pulled 10-22 `7ZTFKBu$37p7`) | 실측(FC27 시대 경기 프리셋 #51·55·56·62) | 판정 | 근거 |
|---|---|---|---|---|---|
| 포메이션 | 4-2-3-1 Wide(#32·#33·#42) | 4-2-3-1 (2) (EA id 4) | 4경기 전부 4-2-3-1 Wide | **잘 반영** | 실측 · ⚠️ 「Wide」↔「(2)」 대응이 코드(`core/classify.py:67` 축약)와 산문에만 있고 표로 없다 |
| 빌드업 | **Balanced**(#32 사용자 10-15 · obs#1081 10-20) · ⚠️ #42 「에메리 실축 구현 프리셋」은 Short Passing | Balanced | Counter(#51 브렌트퍼드) · Balanced ×3 · 시즌 중앙값 규칙 Balanced(점유 42%·롱볼 10.4%) | **잘 반영**(값) / **정본 표기 괴리**(#42 이름·docs/10) | 실측 + `core.team_settings` 규칙 |
| 수비 접근 | Balanced | Balanced | 4/4 Balanced · 규칙 일치 | **잘 반영** | 실측 · EA 정의(A, game_tactic_params) |
| 라인 | 52 | 52 | 55·50·48(DIVERGE: 뉴캐슬 압박 초반 한정)·52 · 규칙 48~58 | **잘 반영** | 실측 · ⚠️ 000⑷⑸ 미해결 — FC27 슬라이더 구간이 EA 1–30/31–60과 어긋남(HANDOFF P1) |
| 상대 유형 프리셋 | `optimal:low-possession-2026-10-15`(#33 · LB만 윙백 Balanced) | 코드 1개만 pulled — **어느 프리셋인지 연결 없음** | 점유 ≤45% 7/11경기에서 LB att_wb 1위 0회(obs#1042) | **부분 반영** — 인게임 LB=윙백 Balanced는 #33과 같지만 「저점유용」으로 쓰고 있는지 알 수 없다 | 실측 |
| 리드 국면 프리셋 | FC26엔 `optimal:lead` 있음 · **FC27 26/27 없음** | 없음 | 리드 뒤 def_x 하강·PPDA 상승이 4경기 전부 반복(#56 77′+ 31.5 · #62 62–70′ 26.7) | **미반영**(재현 한계 #26 「단일 정적 프리셋」) | 실측 |

**팀 3축 요약**: 값은 맞다. 문제는 **「정본」이라는 라벨이 어디에도 없다는 것** — 시즌 정본 역할을 하는 행이 `ingame:user-2026-10-15`(사용자 입력 기록)이고, 이름이 「실축 구현 프리셋」인 #42는 폐기된 값을 들고 있다. docs/10 게임 적용 정책 「기본 전술 1개 = `kind='optimal'`」을 FC27 26/27이 지키지 않는다.

### 1.2 슬롯 11칸 — 정본 ↔ 인게임 ↔ 실측

실측 열은 FC27 시대 AVL 경기 전용 처방(`match_player_prescriptions` starter · #51 브렌트퍼드 · #55 페네르바흐체 · #56 뉴캐슬 · #62 바이킹)의 커널 1위 분포와 평균 fit.

| 칸 | slot_canon_roles FC27 | 인게임 `7ZTFKBu$37p7` | 실측 4경기 1위 분포(평균 fit) | 판정 | 비고·등급 |
|---|---|---|---|---|---|
| GK | gk_ballplaying/Build-Up | Ball Playing Keeper/Build-Up | gk_goalkeeper/Defend 4/4(.963) — 히트맵은 희소 행동을 못 담음 | **잘 반영**(사용자 결정 10-15 · 재검토 조건 「3경기 중 2경기 KeeperSweeper」) | 실측 무결정 · 역할 설명 B |
| LB | fb_att_wb/Support | **Wingback/Balanced** | wingback/Balanced 2 · wingback/Support 1(밍스) · att_wb/Support 1(완비사카 뉴캐슬 .929) | **괴리(설명 가능)** — 인게임은 #33 저점유 프리셋 값. 정본 유지 결정(obs#1042)과 「어느 프리셋을 켰는지」 기록이 없어 괴리인지 의도인지 판별 불가 | 실측 · EA #45(풀백 조기 하강 미수정 · A) — 게임이 att_wb를 과하게 내리는 상태라 Balanced가 결과적으로 비슷해질 수 있음(해석) |
| LCB | cb_bpd/Build-Up | BPD/Build-Up | cb_bpd/Aggressive 3(.896) · Defend 1 | **잘 반영**(포커스는 실측이 Aggressive 쪽 — 1위 포커스 Build-Up 0/4) | 실측 · Δ는 .05 안팎이라 무결정 처리 타당 |
| RCB | cb_bpd/Aggressive | BPD/Aggressive | cb_bpd/Aggressive 3(.823) · Build-Up 1 | **잘 반영** | 실측 |
| RB | fb_wingback/Balanced | Wingback/Balanced | wingback/Balanced 2(캐시 .883) · att_wb/Support 1(캐시 #51) · **fb_inverted/Build-Up 1(고메스 #62 .812)** | **잘 반영**(정본 = 캐시형) · 고메스 RB는 부상 강제 1경기 — 일반화 금지(#62 §7) | 실측 |
| LDM | dm_dlp/Roaming | DLP/Roaming | dm_dlp/Roaming 4/4(.773) | **잘 반영** | 실측 |
| RDM | **dm_holding/Defend** | **DLP/Build-Up**(테스트) | boxcrasher/Balanced 2(.69 · 카마라 #55·맥긴 #62) · dlp/Build-Up 1(.719) · dlp/Roaming 1(.636) · 시즌 평균 Roaming .730 > Build-Up .660 > 홀딩 .608(obs#1080) | **괴리 — 정본이 실측 최하위**. 인게임 테스트 결과 대기(HANDOFF P1) | 실측 · ⚠️ 커널 1위가 경기마다 갈림(무결정 3/4) — 「홀딩 Defend가 아니다」까지는 실측, 「DLP Build-Up이다」는 아직 아님 |
| LM | wm_insidefwd/Balanced | **Inside Forward/Attack**(10-22 포커스 변경) | **wm_winger/Attack 2(음바예 .878·.786)** · insidefwd/Balanced 1(부엔디아 .625) · widemid/Support 1 | **괴리 2중** — ⑴ 인게임 포커스 Attack ≠ 정본 Balanced(변경 기록·사유 없음) ⑵ 실측은 음바예에게 winger/Attack(IF .389 기각 · 대조표 20) | 실측 · 쟁점 #7(음바예 윙어 vs IF) |
| CAM | cam_playmaker/Roaming | Playmaker/Roaming | cam_playmaker/Roaming 4/4(**.674** · 부엔디아 .592) | **잘 반영**(역할) · fit이 낮은 칸 — 에메리 10번이 커널보다 넓게 움직임(만잠비 프리롤 obs#1050) | 실측 · EA #10/#19 Attacking Spatial Awareness(A)로 FC27은 역할 구속이 더 풀림 → 낮은 fit의 일부는 구조적 |
| RM | wm_winger/Attack | Winger/Attack(10-22 Wide Playmaker→Winger) | wm_winger/Attack 3(.789) · Balanced 1 | **잘 반영**(10-22 변경으로 정렬됨) | 실측 |
| ST | st_advanced/**Support** | Advanced Forward/**Attack** | st_advanced/Support 2(잭슨 .633) · false9/Attack 1(.649) · target/Balanced 1(.601) — **전부 .65 이하** | **괴리 3중** — 정본 Support · 인게임 Attack · `opt:ST` 처방 **st_false9/Attack .724(n=28)**. 세 층이 세 값 | 실측 · 쟁점 #4·#5 · EA #11 Triggered Runs 거리 제한(A)으로 「배후 침투」 재현이 FC27에서 짧아짐 |

### 1.3 선발 처방 층(`prescriptions kind='opt:*' starter=1` · FC27 · 26/27)

| 칸 | opt 선발(행 id) | 역할/포커스 | 슬롯 정본 | 현재 실제 선발(#56·#62) | 문제 |
|---|---|---|---|---|---|
| GK | 스즈키(939) | gk_goalkeeper/Defend .975 n=29 | gk_ballplaying/Build-Up | 스즈키 | **역할 ≠ 정본**(사용자 10-15 결정 미반영) |
| LB | 루헤리(870) | fb_att_wb/Support .931 n=45 | 같음 | 밍스(#62)·완비사카(#56) | **부상 약 2개월**(obs#1082) |
| LCB | 밍스(942) | cb_bpd/Aggressive | cb_bpd/Build-Up | 파우 토레스 | 포커스 ≠ 정본 · **파우 토레스(746)가 starter=0** |
| RCB | 린델뢰프(749) | cb_bpd/Aggressive | 같음 | 린델뢰프 | — |
| RB | 완비사카(931) | **fb_att_wb/Support** .932 n=25 | fb_wingback/Balanced | 고메스(#62)·캐시 | **역할 ≠ 정본**(같은 역할군이라 G8+ 통과) · 햄스트링 3~4주 |
| LDM | 바클리(943) | dm_dlp/Roaming | 같음 | 바클리 | — |
| RDM | 카마라(753) | dm_holding/Defend | 같음(테스트 중) | 카마라·맥긴 | obs#1080 결과 대기 |
| LM | **헤밍스(944)** | wm_widemid/Support .662 n=5 | wm_insidefwd/Balanced | 음바예 | **선발 표기 오류 수준** — OVR 65 진화 중 카드 · 역할 ≠ 정본 |
| CAM | 만잠비(765) | cam_halfwinger/Balanced | cam_playmaker/Roaming | 부엔디아 | **역할 ≠ 정본** · 종아리 타박 결장(obs#1082) |
| RM | **음바예(938)** | wm_widemid/Build-Up .878 n=16 | wm_winger/Attack | 알리송(760은 starter=0 · wm_winger/Attack .812 n=6) | 좌우가 뒤집힘(09-19 statfit 흔적) · 역할·포커스 ≠ 정본 |
| ST | 잭슨(940) | st_false9/Attack .724 n=28 | st_advanced/Support | 잭슨 | 역할·포커스 ≠ 정본 |

⇒ **11칸 중 정본과 역할/포커스가 다른 칸 7(GK·LCB·RB·LM·CAM·RM·ST), 현 가용 인원과 다른 칸 4(LB·RB·LM·CAM)**. 이 층은 export(`AVL.json prescriptions` 285행 전부 FC27)되어 스쿼드·히트맵 화면의 「선발 처방」으로 보인다. **FC26→FC27 승계(82b0e50)가 낡은 선발을 그대로 옮긴 것**이 원인이고, 승계 자체는 규칙대로였다(행 보존).

### 1.4 역할 커널·게이트·버전 누수

| 항목 | 상태 | 판정 |
|---|---|---|
| `kernels/FC27.json` | roles 37 · focus 85 · variants 217 · role_key_attrs 292 · system_changes 44 · **role_ingame 0** | 익스포트 정상 · 인게임 대조 0 |
| `core/kernel.py EXPECTED['FC27']` | (37,85,217) 등재 | 정상 |
| G1 커널 정합 | `Kernel("FC26")`만 — FC27은 Kernel 생성 자체가 안 됨(gates.py:479) | **FC27 미검사** |
| G3 커널 앵커 6항 | FC26 저장 그리드로만 재현 | **FC27 앵커 없음**(역할표가 전항 일치라 수치는 같을 것이나 「같다」를 검사하지 않음) |
| G5 JS 커널 동치 | `kernels/FC26.json`만(gates.py:527) | **FC27.json 미검사** — `site/assets/kernel.js:35`도 FC26일 때만 카운트 assert |
| G40 버전 정합 | 신설 · 통과 | 정상 |
| 화면 커널 로드 | `squad.html:34` `compare.html:31` `heatmap.html:33` `game.html:146` `evolutions.html:166` 전부 `loadKernels('FC26')` 하드코딩 · `manual.html` 제목 「FC26 구현 매뉴얼」 · `index.html` 「FC26 → FC27」 | **FC26 누수** — 처방(FC27)과 커널(FC26) 버전이 화면에서 어긋남(값은 같아 보이나 구조상 틀림 · `core/game_version.py` 머리말이 금지한 형태) |
| 규칙 모듈 | `core/team_settings.py` 머리말 「FC26 팀 설정 제안」 · 임계값은 FC27 `game_tactic_params` 9행과 동일 정의 | 값 정상 · 문서 낡음 |
| docs/10 「게임 적용 정책」 | 「빌드업 Short Passing / 라인 ~52」 | **낡음**(10-15 Balanced 결정 미반영) |
| docs/22 §3 PlayStyle 카탈로그 | FC26 기준 35종 · §6 표가 FC27 차이 | 규약상 §6 우선 — 정상 |
| `reproduction_limits` FC27 | 14행 = FC26 문구 그대로 승계(#15~#28) | 정상 · 단 FC27 신규 한계(#11 Triggered Runs 거리 제한 · #45 풀백 조기 하강)가 한계 표에 없음 |
| 인게임 캡처 | `ingame_captures` 75건 전부 FC26 · 마지막 2026-09-10 · `v_kernel_fidelity` 13행 FC26 | **FC27 C등급 0** — docs/50 루프가 FC27에서 시작되지 않음 |

### 1.5 FC27 시스템 변화 중 빌라 재현에 직접 걸리는 것(`game_system_changes` · 등급)

| id | 내용 | 빌라 구현 함의 | 등급 |
|---|---|---|---|
| #45 | EA가 **풀백 조기 하강(라인 깨짐)** 을 최다 피드백으로 인정 · 미수정 | C2 풀백 비대칭(LB 전진측)의 게임 내 재현이 **엔진 결함에 덮여** 있음 → LB att_wb vs 윙백 A/B는 수정 전까지 결론 유보 | A |
| #11 | Triggered Runs 거리 제한 | st_advanced/Support · wm_winger/Attack의 배후 침투가 짧아짐 — 알리송 「뒷공간 침투」 재현 손실 | A |
| #10·#19 | Attacking Spatial Awareness — 역할은 유지되나 구속 완화 | 커널 fit 하한이 구조적으로 내려감(CAM .67 · ST .63) — Δ≤.05 무결정 기준 유지 타당 | A |
| #14·#20 | Team Press 수비 3분의 1 무효 · 수비수 압박 효율 낮음 | 미드블록 재현엔 유리(docs/10) — 뉴캐슬전 0–15′ 맞압박(PPDA 4.1) 같은 국면은 재현 불가 | A |
| #22 | 패서 PlayStyle의 리시버 트랩 보정 제거 | 「패서를 좋게 해 리시버를 덮는」 처방 폐기 — 6.1 규약 반영됨 | A |
| #21·#13 | 프로모 카드 Role++ 기본 · PlayStyle+ 상한 3 | 역할 숙련은 판정 층에서 제외(6.1) — 반영됨 | A/B |

### 1.6 제안 — DB 변경은 **새 행만**

**㉠ 지금 반영 가능(근거·사용자 결정이 이미 있음)**
1. `team_tactic_setups` 새 행 `kind='optimal'`(FC27 · 2026-27 · 4-2-3-1 Wide · Balanced/Balanced/52 · ingame_formation 4-2-3-1 Wide) — 근거 #32(사용자 10-15) · obs#1081(10-20) · pulled 7ZTFKBu$37p7 일치. `tactic_changes.py --reason` 필수(G19).
2. `observations` 새 행 — 「선발 처방 층 7/11 낡음」 실물 기록(위 1.3 표 · 승계 커밋 82b0e50 원인) + 「인게임 LM 포커스 Balanced→Attack · RM Wide PM→Winger 변경(10-22 pulled)의 사유 미기록」.
3. `prescriptions opt:*` 새 행(기존 행 starter만 바꾸지 않는다 — starter 플래그 갱신은 편집이 정상 작업인 표이므로 허용되나, 역할/포커스 변경은 새 행): 현 가용 선발로 재생성 — GK 스즈키 gk_ballplaying/Build-Up · LB 밍스(루헤리 복귀 전) · LCB 파우 토레스 cb_bpd/Build-Up · RCB 린델뢰프 · RB 캐시 fb_wingback/Balanced · LDM 바클리 · RDM 카마라 · LM 음바예 · CAM 부엔디아 cam_playmaker/Roaming · RM 알리송 wm_winger/Attack · ST 잭슨 — **정본 역할로**. fit_sim은 `refresh_eval_samples.py --apply`(T1)로 산출.
4. docs/10 「게임 적용 정책」 빌드업 문구 정정(문서) · 화면 `loadKernels('FC26')` 5곳 → `current` 버전 사용(코드 · 구조 ①) · gates G1/G3/G5에 FC27 추가(③).

**㉡ 사용자 판단 대기(⛔ slot_canon_roles 변경 사안)**
5. RDM `dm_holding/Defend` → `dm_dlp/Build-Up`(obs#1080 인게임 테스트 결과 + 다음 2경기 실측). 현재 실측 근거는 「홀딩이 아니다」까지.
6. ST 포커스 Support ↔ Attack ↔ `opt:ST` false9/Attack — 세 층 통일. 실측은 4경기 전부 .65 이하라 역할 자체가 무결정(쟁점 #4·#5).
7. LM 포커스 Balanced ↔ 인게임 Attack · 역할 insidefwd ↔ 음바예 실측 winger(쟁점 #7).
8. LB — 인게임이 #33(저점유) 값으로 고정돼 있는데 「경기마다 바꾸는가」 운용 결정. 바꾸지 않을 거면 정본을 윙백 Balanced로, 바꿀 거면 `fut_tactics`에 어느 프리셋인지 연결(아래 2.3 ③).
9. FC27 `optimal:lead`(리드 국면 프리셋) 신설 여부 — FC26엔 있었고 실측은 4/4 리드 뒤 하강.

**㉢ 추가 실측 필요(경기 수)**
10. 고메스 RB(1경기) · 밍스 LB 잔류(1경기) · GK 스위핑 재검토 조건(3경기 중 2) · 양 풀백 역전(obs#449 · 버킷당 2경기).

---

## Part 2 — 게임 구현에 필요한 데이터 충분성

### 2.1 게임이 받는 입력 ↔ 우리 공급원 (AVL 26/27 · FC27)

| 게임 입력 | 공급 표·컬럼 | AVL 26/27 표본 | 최신 | 상태 |
|---|---|---|---|---|
| 포메이션 | `team_tactic_setups.formation/ingame_formation` · `match_game_setups.formation` · `slots`(4-2-3-1 Wide 11 · 4-4-2 11) | 경기 프리셋 6(#43~#62) · 공식전 12 | 10-22 | **충분** |
| 빌드업·수비접근·라인 | `matches.possession` · `team_match_stats` passes/long_att/ppda/def_x → `core.team_settings.suggest` → `match_game_setups` + `rule_note`(G15) | 공식전 12 · xG/PPDA FotMob·WS 동일 조건 11(08-23~) | 10-22 | **충분** |
| 11칸 역할·포커스(시즌) | `slot_canon_roles` FC27 11행 · `prescriptions opt:*` | 정본 11 · opt 선발 11(+교체 36) | 정본 10-22 · **opt 선발은 낡음**(1.3) | 정본 충분 / **선발 층 부족** |
| 11칸 역할·포커스(경기) | `match_player_prescriptions`(fit_sim·fit_delta·alt_role) | 경기당 16 × 6경기 | 10-22 | **충분** |
| 역할 커널(히트맵 기대값) | `game_roles/focus/variants` FC27 · `kernels/FC27.json` | 37/85/217 | 10-22(fut.gg B · FC26 승계) | 충분(B) / **C 0** |
| 선수 위치 실측 | `player_matches.map25/cells` + 국면 그리드 `cells_poss/def`(WS) | 278행 · 국면 그리드 207/278 | 10-22 | 충분 · 국면 그리드 결손 2경기(08-23·08-31) |
| 스코어 국면 분(@lead/@trail) | `player_matches.stats_json.phase_*` | **118/278** — 08-31·09-08·09-19·10-10·10-14 5경기 0 | — | **부족**(5경기 incidents 미병합 → 국면 집계 표본 반토막) |
| 구간 지표 | `match_phase_metrics`(def_x·ppda·own_half_pass_pct) · `match_tactical_changes` | #62 59행 · 변화 6행 | 10-22 | 충분(#56 이후) |
| 선수 카드 스탯(6대·29속성·키·몸무게·AcceleRATE) | `player_game_stats` FC27 | AVL 122행 · **roster_date 2026-09-10(출시 전)** | 09-10 | **낡음** — 출시 후 fut.gg 재수집 필요(`fill_futgg_fc27_detail.py`) |
| PlayStyle(실축 선수) | `player_game_stats.playstyles` FC27 | **24/122 채움** | 09-10 | **부족** |
| Role+/++(실축 선수) | `player_game_stats.role_familiarity` FC27 | **0/122**(대응표 `fc_role_familiarity_map` 98행은 있음) | — | **없음**(HANDOFF 0-2) |
| PlayStyle·Role+(내 FUT 카드) | `fut_club_players.current_playstyles/current_roles_plus` | 보유 161 중 132/141 | 10-22 | 충분(FUT 축) |
| 세트피스 키커·타깃 | `manager_profiles.set_pieces`(산문 09-18) · `match_shots.situation`(corner 7·FK 1·PK 1) · `match_events`에 코너 kind 없음 | 산문 1 · 슈팅 상황별 xG | 09-18 | **부족** — 게임 입력(키커 지정)에 쓸 정형 없음 |
| 교체 패턴 | `match_player_prescriptions.minute_on/replaced_player_id` · `match_events kind='sub'` | 경기당 5 × 6 | 10-22 | 충분(집계는 쿼리로 가능 · 정형 요약 없음) |
| 비보유 형태(4-4-2 등) | **없음** — `match_hypotheses`·리포트 산문·`reproduction_limits #20` | — | — | **없음**(정형 필드) |
| rest-defense(볼 뒤 잔류 수) | 산문(#62 §2 「3+2=5」) · limit #28(게임 축 없음) | — | — | 없음(게임 입력 아님 · 기록 축 부재) |
| 압박 트리거 | `video_impl_claims axis=instruction` 150행 · limit #17(게임 슬라이더 없음) | — | — | 충분(한계 명시 · 게임 입력 아님) |
| 운반(progressive carries) | **없음** — Opta 이벤트에 캐리 없음 · SS/FM 경기 단위 없음 · `fotmob_detail_stats`는 dribbles만(시즌 단위) | — | — | **없음**(#62 대조표 10행은 추정) |
| GK 배급 | `team_match_stats.long_att_v`(팀) · GK `stats_json` pass_total/acc만 | — | — | **부족** — GK 롱 비중이 obs#1081에서 손계산 · `PHASE_METRICS`엔 정의돼 있으나 #62에 미적재 |
| 상대 유형 프리셋 | `team_tactic_setups optimal:low-possession`(LB 1칸) · obs#1081(고압박 Counter 기각) | 1 | 10-15 | 충분(사용자 결정) |
| 리드 국면 프리셋 | FC26 `optimal:lead` · FC27 없음 | 0 | — | **없음**(1.6 ㉡9) |
| 인게임 검증(캡처·A/B) | `ingame_captures` · `v_kernel_fidelity` · `team_tactic_setups ingame:*` | FC26 75건 · **FC27 0** · ingame:* FC27 4행(코드만) | 09-10 | **없음(FC27)** |
| 선수 상태(부상·징계) | `player_status` | 1065행 | **10-22** | 충분 |
| 서사·영상 주장 | `video_impl_claims` | APPLIED 39 · HELD 184 · PENDING 83 · NA 142 · none 137 | #62 영상 3편(UTV·1874·Terrace View 미전사) | 충분(규약) · #62 얕음 |
| 관전 가설 판정 | `match_hypotheses` #62 | match 12 · partial 13 · mismatch 4 · pending 1 | 10-22 | 충분 |
| D+N 추적 예약 | `~/.claude/scheduled-tasks`(이 PC AL02359162.local) | **mw-avl-viking-d2/d3 없음** | — | **G34 실패 중**(이 PC 폴더가 있어 「다른 PC」 건너뜀이 안 걸림) |

### 2.2 결손 표

| 필요 데이터 | 현재 공급원 | 상태 | 부족 사유 | 추가 수집 제안 | 우선 |
|---|---|---|---|---|---|
| 선발 처방 층(현 가용 XI · 정본 역할) | `prescriptions opt:*` | 부족 | FC26 승계가 7-9월 선발을 그대로 옮김 · 부상 미반영 | T1(`refresh_eval_samples.py`) 뒤 opt:* 새 행 생성 절차를 match-watch §4-1에 묶기 · **게이트 신설**: opt 선발 ≠ slot_canon 역할/포커스 또는 `player_status` 장기 부상이면 실패(G8+ 확장) | **P1** |
| 스코어 국면 분(5경기) | `stats_json.phase_*` | 부족 | SS incidents 병합이 회차에 따라 빠짐 | `load_sofascore_json.py`에 incidents 병합을 필수 단계로(④) + **G23 확장**: 공식전 player_matches에 phase_* 없으면 결손 | P1 |
| FC27 선수 카드 축(29속성·PlayStyle·Role+/++) | `player_game_stats` FC27(09-10) | 낡음/없음 | 출시 전 수집 뒤 재수집 없음 · 0-2 백로그 | `fill_futgg_fc27_detail.py` + `migrate_fc27.py --roles` 재실행 → roster_date ≥ 2026-09-25 · **G21 감시 표에 player_game_stats FC27 추가** | P1 |
| D+N 예약(이 PC) | scheduled-tasks | 없음 | 예약이 iMac에만 있음 | 바이킹전 D+2(10-23 20:00)·D+3(10-24 20:00) 예약 재생성 또는 D+2 절을 오늘 쓰고 D+3만 예약 — G34가 막는다 | P1 |
| 비보유 형태 정형 | 없음 | 없음 | 리포트 산문에만 | `match_game_setups`에 `shape_in_possession`·`shape_out_possession` 컬럼(nullable · 어휘 고정 「4-4-2」「3-2-5」…) + G37에 AVL 리포트 필수 | P2 |
| 세트피스 키커·타깃 | 산문 | 부족 | 정형 없음 · 게임 입력은 키커 지정뿐 | `match_set_pieces`(match_id·kind·taker_id·target_id·side·outcome·source) 신설 — 코너 8·FK는 WS 이벤트 qualifier(코너·크로스)로 키커 자동 추출 가능 | P2 |
| GK 배급 비중 | 손계산 | 부족 | PHASE_METRICS 정의만 있고 미적재 | `match_phase_metrics` metric `gk_long_share`를 AVL 경기 필수로(G37 확장) | P2 |
| 인게임 검증 FC27 | `ingame_captures` | 없음 | 09-10 이후 캡처 중단 · FC27 시작 안 함 | docs/50 절차로 `ingame:user-2026-10-15`(또는 현 코드 7ZTFKBu$37p7) 비조작 3경기 캡처 → G3 FC27 앵커 | P2(사용자 플레이 필요) |
| 운반(carries) | 없음 | 없음 | 공개 제공사에 경기 단위 캐리 없음 | 대안 ①「수신 좌표→다음 볼 이벤트 좌표」 추정을 `core.whoscored`에 함수로 올려 **추정임을 컬럼명에 박음**(`carry_est_10plus`) ② FotMob `playerStats` 경기 단위에 Carries가 있는지 1회 확인 | P3 |
| 리드 국면 프리셋 | 없음(FC27) | 없음 | 사용자 결정 미요청 | 1.6 ㉡9 — 결정 후 새 행 | P3 |
| 커널 게이트 FC27 | G1/G3/G5 | 없음 | FC26 하드코딩 | gates.py에 현행 버전 루프(`core.game_version.current`) — G1 Kernel(gv) · G5 kernels/{gv}.json · G3 앵커는 FC26 수치 그대로 FC27에도 기대(전항 일치 승계이므로 같아야 함) | P2 |
| 화면 커널 버전 | `loadKernels('FC26')` 5곳 | 누수 | 하드코딩 | `index.json`의 현행 버전을 data.js가 읽어 `loadKernels(current)` — G22 정적 검사에 `loadKernels('FC2` 리터럴 금지 추가(구조 ①+③) | P2 |
| 「정본」 라벨 | `team_tactic_setups` | 없음 | kind='optimal' FC27 행 0 | 1.6 ㉠1 | P1 |
| 인게임 코드 ↔ 프리셋 연결 | `fut_tactics` | 없음 | pulled 행이 어느 `team_tactic_setups.kind`인지 모름 | `fut_tactics.setup_kind` 컬럼(club-sync가 11칸 역할·3축 일치로 자동 판정 · 불일치면 NULL+보고) | P2 |
| FC27 신규 재현 한계 | `reproduction_limits` FC27 14행(승계) | 부족 | #11·#45 미반영 | 새 행 2(Triggered Runs 거리 · 풀백 조기 하강) · game_system_changes id 인용 | P3 |

### 2.3 우선 조치 10건

| # | 할 일 | 바꿀 곳 | 표 | 합격 기준 |
|---|---|---|---|---|
| 1 | FC27 `kind='optimal'` 시즌 정본 행 추가(Balanced/Balanced/52) | `tactic_changes.py --reason "obs#1081·#32"` | `team_tactic_setups` | `SELECT count(*) FROM team_tactic_setups WHERE regime_id=1 AND season='2026-27' AND game_version='FC27' AND kind='optimal'` = 1 · G19 통과 |
| 2 | 선발 처방 opt:* 재생성(현 가용 · 정본 역할) + 게이트 | match-watch SKILL §4-1 완료 절차에 「opt 선발 ≠ 정본 또는 장기 부상 → 재생성」 · `gates.py` G8+ 확장 | `prescriptions` | G8+: opt starter 11행이 slot_canon 역할/포커스와 일치 · `player_status` 장기 부상 0 |
| 3 | 바이킹전 D+2·D+3 예약 재생성(이 PC) 또는 D+2 절 작성 | `mcp__scheduled-tasks` | — | `gates.py` G34 ✅ |
| 4 | 국면 분 결손 5경기 백필 + G23 확장 | `load_sofascore_json.py`(incidents 필수) · `gates.py` G23 | `player_matches.stats_json` | 공식전 player_matches 중 phase_* 결손 0 |
| 5 | FC27 선수 카드 재수집(29속성·PlayStyle·Role+) | `fill_futgg_fc27_detail.py` · `migrate_fc27.py --roles` · G21 감시 표 | `player_game_stats` | AVL FC27 roster_date ≥ 2026-09-25 · playstyles 채움 ≥ 90% · role_familiarity > 0 |
| 6 | 게이트·화면의 FC26 하드코딩 제거 | `gates.py`(G1/G3/G5 현행 버전 루프) · `site/assets/data.js`(현행 버전) · `squad/compare/heatmap/game/evolutions.html` · G22 리터럴 금지 | — | `grep -c "loadKernels('FC26')" site/*.html` = 0 · G1 FC27 ✅ · G5 FC27.json ✅ |
| 7 | 비보유 형태 정형 2컬럼 + G37 필수 | migration(번호는 부모 배정) · `load_match_extras.py` · G37 | `match_game_setups` | AVL 리포트(≥10-14) shape_out_possession NOT NULL |
| 8 | GK 배급 비중을 구간 지표 필수로 | `match_phase_metrics.py` · G37 | `match_phase_metrics` | AVL 리포트마다 metric='gk_long_share' ≥ 1행 |
| 9 | 세트피스 키커·타깃 표 신설(WS qualifier 자동 추출) | migration · `load_whoscored.py` | `match_set_pieces`(신설) | #62 코너 8행 taker_id 채움 |
| 10 | 인게임 코드 ↔ 프리셋 연결 + LM/ST 포커스 변경 사유 기록 | `club_sync.py` §3-3 · `observations` 새 행 | `fut_tactics.setup_kind` · `observations` | pulled 최신 행 setup_kind NOT NULL 또는 보고 1행 · obs 1행 |

> 적용 순서 제안: 3 → 1 → 2 → 4 → 5 → 6(코드) → 7~10. 2·7·9는 migration 번호가 필요하므로 부모 세션이 배정한다. 5~9 중 사용자 플레이가 필요한 것은 인게임 검증(2.2 표)뿐이다.
