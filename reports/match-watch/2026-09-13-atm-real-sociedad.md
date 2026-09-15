# 2026-09-13 Real Sociedad 0-3 Atlético Madrid — 라리가 J5 (원정, 아노에타)

> 수집일 2026-09-14 · SofaScore event `16416332` · FotMob matchId `5868058` · WhoScored matchId `1994164` ·
> 라리가 2026/27 J5 · 원정 · ATM 3-4-2-1 / Real Sociedad 4-2-3-1

## 1. 경기 개요와 원천 수치

| 항목 | ATM | Real Sociedad |
|---|---|---|
| 점유율 | **46%** | 54% |
| xG | **2.05** | 0.27 |
| xG 오픈플레이 | **1.05** | 0.08 |
| xG 세트피스 | 0.22 | 0.19 |
| xG 논PK | 1.26 | 0.27 |
| xGOT | **1.95** | 0.49 |
| 슈팅 / 유효 | 13 / 5 | 8 / 3 |
| 박스 안 슈팅 | **9** | 2 |
| 빅찬스 / 놓침 | 3 / 0 | 1 / 1 |
| 상대 박스 터치 | 22 | 17 |
| 패스 / 정확 | 462 / 373 (81%) | 524 / 450 (86%) |
| 상대 진영 패스 | 163 | **269** |
| 롱볼 (성공/시도) | 32 / 64 (50%) | 23 / 39 (59%) |
| 크로스 (성공/시도) | 4 / 8 (50%) | 3 / 20 (15%) |
| 코너 | 3 | **9** |
| 태클 / 인터셉트 / 클리어 / 블록 | 13 / 8 / 24 / 4 | 17 / 7 / 22 / 2 |
| 공중경합 | 13/23 (57%) | 10/23 (43%) |
| 드리블 성공 | 8/12 (67%) | 11/15 (73%) |
| 파울 / 옐로 | 9 / 1 | 13 / 2 |
| **PPDA** | **15.14** (333/22) | 11.35 (352/31) |
| **def_x (라인 프록시)** | **36.0** (n=145) | 41.8 (n=150) |

- **득점**: 84′ 그리말도(PK) · 90′ 조나단 데이비드(도움 그리말도) · 90+5′ 줄리아노 시메오네(도움 한츠코).
- **스코어 국면**: `level` **84분** · `lead` 12분(추가시간 포함) · `trail` **0분**.
  **0-3이라는 스코어는 경기 내용의 요약이 아니다 — 경기의 93%가 0-0이었다.**
- **교체**(전부 ATM 59~76분): 59′ 카르도소←바에나 · 60′ 코케←이강인 · 60′ 조나단 데이비드←마르코스 요렌테 · 76′ 아르나우 오르티스←루크먼.
- **국면별 압박·라인**(WhoScored 이벤트 구간 분할):

| 구간 | ATM PPDA | ATM def_x | RSO PPDA | RSO def_x |
|---|---|---|---|---|
| 전반 0–45 | 16.40 (164/10) | 39.5 | 11.28 (203/18) | 40.0 |
| 후반 45–84 (0-0) | **9.64** (106/11) | 35.9 | 9.31 (121/13) | 43.0 |
| 84–종료 (리드) | 57.00 (57/1) | **27.0** | — (28/0) | 47.9 |

- **수집 엔드포인트**: SofaScore `lineups`·`average-positions`·`heatmap`·`incidents`·`event`(event 16416332,
  `scripts/collect_event.py` Playwright) / FotMob `matchDetails?matchId=5868058`(xG 4종 **동일 스냅샷**) /
  WhoScored `matchCentreData` matchId=1994164(이벤트 1,612건 → `core.whoscored`).
- **정합 검증**: xG 2.05 − 논PK 1.26 = **0.79** ≈ PK 1개 × ~0.79 ✅ / 오픈플레이 1.05 + 세트 0.22 = 1.27 ≈ 논PK 1.26 ✅.
  `xg_source='FotMob'` — 4종 전부 한 응답에서 왔다.
- **결손·한계**: 롱볼·크로스 **시도**는 FotMob의 「성공(성공률)」 표기에서 역산했다(반올림 오차 ±1 가능).
  `def_x`는 ATM 전체 표본이 **이 경기 포함 2건**뿐이라(안필드 34.1) 절대 수준 해석은 아직 못 한다.
- **유효 히트맵**: 출전 15명 전원 수집. 시즌 집계 기준(45분+·hit_points 15+) 통과는 **11명**(선발 전원);
  교체 4명(코케 30분/hp27 · 카르도소 31분/hp22 · 데이비드 30분/hp14 · 오르티스 14분/hp14)은 리포트 전용이다.

## 2. 전술 설명

### 점유 구조·빌드업

3-4-2-1의 **좌우 비대칭이 이 경기의 구조 그 자체다.** 평균 위치를 툴 좌표(x=100−소파y, 0=왼쪽)로 놓으면:

| 구역 | 선수 (툴x) |
|---|---|
| 좌측 | 그리말도 **18.3** · 루크먼 24.8 · 바에나 36.3 · 한츠코 20.6 |
| 중앙 | 율만 54.0 · 로메로 59.1 · 오블락 50.8 |
| 우측 | 마르코스 요렌테 **78.5** · 이강인 78.6 · 줄리아노 시메오네 79.6 · 푸빌 81.2 |

**툴x 59와 78 사이에 아무도 없다.** 우측에는 네 명(RCB·RWB·RCM·RAM)이 폭 3 안에 겹쳐 서 있고,
좌측은 그리말도가 터치라인에 붙어 혼자 폭을 만들었다. 즉 명목상 대칭인 3-4-2-1이
**「우측 4인 과밀 + 좌측 1인 고립」** 으로 운용됐다.

빌드업은 짧지 않았다. 롱볼 비율 **13.9%**(64/462)에 자기 진영 패스 210 대 상대 진영 163 —
상대(181/269)와 정반대다. 전방 압박을 걸지 않고 공을 내준 뒤 **되찾으면 곧장 앞으로 보내는** 형태다.
정확도 81%(상대 86%)와 크로스 성공률 50%(8회 시도로 적다)가 같은 이야기를 한다:
**적게 만들고 좋은 것만 만들었다**(박스 안 슈팅 9 대 2 · xGOT 1.95 대 0.49).

### 비점유 구조·압박

PPDA **15.14**는 시메오네 체제의 서사와 정면으로 충돌하는 값이 아니라, **9월 들어 세 번째로 반복된 값**이다
(09-05 아틀레틱 15.13 · 09-09 리버풀 12.52 · 09-13 15.14). 8월의 7.77·8.26과 대역이 다르다.

⭐ 그리고 이 경기에서 **시즌 처음으로 상대 PPDA가 우리보다 낮았다**(ATM 15.14 vs RSO 11.35).
직전 5경기는 전부 ATM 쪽이 낮았다(더 압박했다). **압박 주도권을 내준 첫 경기다.**

def_x 36.0은 수비 액션의 무게중심이 자기 진영 쪽이라는 뜻이고, 구간을 쪼개면 더 분명하다 —
전반 39.5 → 후반(0-0) 35.9 → 리드 후 **27.0**. 리드를 잡자마자 통째로 내려앉았다.

후반 0-0 구간의 PPDA 9.64는 「압박을 올렸다」로 읽히기 쉽지만 **분모(수비 액션)는 10→11로 거의 그대로였고
분자(상대의 자기 진영 패스)가 164→106으로 줄었다.** 즉 ATM이 더 강하게 누른 것이 아니라
**상대가 자기 진영에서 돌리기를 그만두고 앞으로 보내기 시작했다.** 압박 지표의 개선분은 상대 행동 변화의 반영이다.

### 전환·rest-defense·세트피스

- 클리어 24 · 블록 4 · 공중경합 57%(13/23) — 박스 앞에서 처리하는 양이 많았고 그것을 이겼다.
- 상대 코너 **9개**를 내주고 세트피스 실점 0(RSO 세트 xG 0.19). 백3 + 율만/로메로의 제공권이 버텼다.
- 상대 크로스 20회 시도 중 성공 3회(15%) — **폭은 내주되 안에서 이기는** 전형적 저블록 처리다.
- rest-defense는 백3 + 율만 단독 피벗. 마르코스 요렌테가 우측 높은 자리로 나가 있는 동안
  중앙 커버가 율만 한 명으로 줄어드는 구간이 반복됐다(상대 빅찬스 1개가 여기서 나왔다).

## 3. 전술적 특성

**반복된 강점**
- **효율의 극단.** 슈팅 13개로 xG 2.05 — 슈팅당 0.158. 박스 안 슈팅 비율 9/13(69%).
  시즌 직전 최고 xG는 1.02(09-05 아틀레틱)였다. **이번이 2배다.**
- 저블록에서 상대 크로스 20개를 15% 성공률로 눌렀다.
- 교체 후 20분에 경기를 끝냈다 — 조나달 데이비드 30분 만에 xG 0.26·1골, 평점 7.9(팀 내 교체 최고).

**반복된 취약점**
- **좌측 고립.** 루크먼(툴x 24.8)은 명목상 최전방 1번인데 왼쪽으로 흘렀고, 터치 26·패스 16·경합 2승7패·
  키패스 3에 평점 6.2(팀 최저)로 76분 교체됐다. 그리말도 한 명이 좌측 폭·전진·마무리를 전부 떠안았다.
- **우측 과밀.** 요렌테·이강인·시메오네·푸빌이 같은 3폭 안에 있어 요렌테의 커널 적합이 .541로 내려앉는다
  (명목 RCM인데 실측은 윙 폭). 이강인(터치 34·패스 22)과 바에나(터치 36)는 둘 다 볼을 거의 못 만졌다.
- ⭐ **백3 자체의 구조적 누출 — 우CB 푸빌의 등 뒤.** 현지 분석이 **세 경기 연속 같은 지점**을 지목한다:
  「Marc Pubill, perseguía con agresividad a su marca y generaba a su espalda un goloso agujero,
  deformando la línea de cinco zagueros」(푸빌이 자기 마크를 공격적으로 쫓아가며 **등 뒤에 군침 도는 구멍**을
  만들고 5백 라인을 변형시킨다) — 산 마메스(09-05)·안필드(09-09)·아노에타(09-13) 전부. 마타라초는 게데스로
  이 경로를 표적했고, **시메오네의 42분 5-4-1 전환(요렌테를 그 측면에 내림)이 그 대응**이었다.
  ⇒ 푸빌 `cb_wideback/Support` 적합 .636이 낮은 것은 노이즈가 아니라 **이 행동의 반영**으로 읽힌다.
- **93분간 0-0.** 내용상 우세(xG 2.05 대 0.27)를 84분까지 스코어로 못 바꿨다.
  PK가 없었다면 이 경기는 0-0 또는 1-0 승부였다. 현지 양측 모두 **0-3은 과대 스코어**로 평가했다
  (Gipuzkoa 「marcador claramente excesivo」 — 명백히 과도한 스코어 · 마지막 두 골은 「prácticamente anecdóticos」 사실상 부수적).

**상대가 만든 교란과 분리**
- 소시에다드의 점유 54%·상대 진영 패스 269는 ATM이 눌린 결과가 아니라 **ATM이 내준 것**이다
  (ATM의 PPDA가 이미 15대). 다만 **코너 9개**는 상대가 만든 실질 압력이다.
- 상대 빅찬스 1개를 놓쳤다(빅찬스 놓침 1:0) — 스코어 0-3은 그 한 장면의 결과에도 기대고 있다.

## 4. 경기 중 변화

1. **0-0 (0~59분)** — 3-4-2-1 그대로. 전반 PPDA 16.4·def_x 39.5로 완전히 물러섰다. 0-0 유지가 목적인 배치.
2. **첫 3중 교체 (59~60분)** — 바에나→카르도소, 이강인→코케, 요렌테→조나단 데이비드.
   **연결고리 3인(바에나·이강인·요렌테)을 한꺼번에 뺐다.** WhoScored 포지션으로는
   율만이 RCM으로, 카르도소가 LCM으로 이동하고 **루크먼이 최전방에서 좌측 AM(LAM)으로 내려가며 데이비드가 9번**에 들어갔다.
3. **76~77분** — 오르티스←루크먼(LAM). 좌측 인원을 한 번 더 갈았다.
4. **마지막 국면 (84~90+5)** — 84′ PK 선제 직후 def_x가 **27.0**으로 급락(완전 후퇴)했는데도
   90′·90+5′ 두 골이 더 나왔다. 후퇴 + 역습이 동시에 성립한 드문 구간이다.

⭐ **WhoScored 포메이션 라벨은 95분 내내 `3421` 단일이었다**(formation 블록 4개 전부 동일).
직전 안필드전은 3-5-2(0~74) → 3-4-2-1(74~78) → 4-4-2(78~)로 라벨이 세 번 바뀌었다.

⚠️ **그러나 라벨 불변 ≠ 구조 불변이다.** 바스크 현지 전술 분석(Noticias de Gipuzkoa, 2026-09-14)은
같은 경기에서 **세 단계의 구조 변형**을 서술한다 — 라벨 분류기가 잡지 못하는 층이다:

1. **킥오프~약 30분**: 수비 시 **5-3-2**(1선 2명 = 루크먼 + 이강인). 보유 시 3CB + 2카릴레로.
2. **약 42분(전반 중) — 시메오네의 첫 조정**: **5-4-1**로 변경.
   「Con un nuevo 5-4-1 que dejaba solo en punta a Kang-in Lee, Cholo logró que Lookman y sobre todo
   Marcos Llorente (ubicado este en el costado sobre el que más volcaban sus ofensivas los txuri-urdin)
   pudieran trabajar en la banda」
   (이강인을 최전방에 홀로 두는 새로운 5-4-1로, 촐로는 루크먼과 특히 **마르코스 요렌테**(소시에다드가
   공격을 가장 많이 쏟던 측면에 배치)가 측면에서 일할 수 있게 만들었다).
3. **후반 개시~60분 교체**: **보유 국면에서 4-3-3으로 전환**.
   「Estos abandonaron el esquema de tres centrales y dos carrileros … para actuar con el balón mediante
   un 4-3-3, dibujo reforzado a posteriori con las sustituciones」
   (이들은 3센터백+2카릴레로 체계를 버리고 … 볼을 가진 상태에서 4-3-3으로 움직였고, 이 그림은 이후 교체로 강화됐다).
   영어권 ATM 전담(Into the Calderón)도 독립적으로 같은 판정 — 「the team reverted to a more recognisable 4-3-3」
   (팀이 더 알아보기 쉬운 4-3-3으로 되돌아갔다).

⇒ **판정: 「95분 단일 포메이션」은 WhoScored 라벨 수준에서만 참이다.** 실제로는 보유/비보유가 갈리고
전반 중 1선 인원이 2→1로 줄었다. ⚠️ 단 **42분 5-4-1 전환 시각은 1차 실측이 아니라 현지 분석의 서술**이고,
우리 이벤트 데이터로는 아직 그 시각을 독립 확인하지 못했다(§9 한계).

## 5. 선수별 분석 — 출전 선수 전원

툴 좌표 = (100−소파y, 소파x). 슬롯 Δx는 안필드전 실측으로 등재된 ATM 3-4-2-1 슬롯 기하 대비 차이다.

| 선수 | 위치·실제 역할 | 분/평점·핵심 스탯 | 평균 위치(툴)·슬롯 Δx | 특성·수행 | FC 역할/포커스 함의 |
|---|---|---|---|---|---|
| 얀 오블락 | GK | 90′ · **7.7** · 세이브 3 · 패스 34/24 · 회수 10 | (50.8, 8.4) · Δ−2.2 | 유효슈팅 3개를 전부 막아 무실점. 회수 10은 뒤 공간 정리를 GK가 했다는 뜻 | `gk_goalkeeper/Defend` **.957** — 정본 유지 |
| 크리스티안 로메로 | CCB (백3 중앙) | 90′ · **7.9** · 클리어 **11** · 경합 5승1패 · 터치 72 · 패스 54/49 | (59.1, 31.6) · Δ**+8.1** | 백3 한가운데에서 전진 수비. 클리어 11은 팀 최다 — 상대 크로스 20개의 종착점이 그였다. 중앙인데 우측으로 8 치우쳤다 | `cb_bpd/Aggressive` **.930** — 이번에 처음 measured 처방 등재(n=2) |
| 다비드 한츠코 | LCB | 90′ · 7.1 · 클리어 3 · 경합 1승3패 · 패스 53/45 · **도움 1**(90+5′) | (20.6, 32.7) · Δ−0.4 | 슬롯과 거의 정확히 일치. 마지막 골 어시스트는 좌측에서 나온 전진 패스 | `cb_wideback/Aggressive` **.770** — 안필드전과 같은 역할 |
| 마르크 푸빌 | RCB | 90′ · 7.3 · 경합 5승2패 · 태클 2 · 패스 40/36 | (81.2, 35.7) · Δ−2.8 | 툴x 81은 CB가 아니라 사실상 우측 풀백 폭. 우측 4인 과밀의 맨 뒤 | `cb_wideback/Support` **.636** — 적합이 낮은 것은 CB 역할군으로 이 폭을 설명 못 하기 때문 |
| 모르텐 율만 | LCM (단독 피벗) | 90′ · 7.3 · xG 0.15 · 인터셉트 2 · 경합 5승3패 · 터치 67 | (54.0, 44.9) · Δ+5.0 | 중앙을 혼자 지켰다. 요렌테가 우측으로 빠져 있는 동안 rest-defense의 유일한 6번 | `cm_b2b/Ball-Winning` **.792** — 안필드 .529에서 크게 올랐다(단독 피벗이 역할과 맞는다) |
| 줄리아노 시메오네 | RM (우측 윙백) | 90′ · **8.0**(팀 최고) · **xG 0.64** · **골 1**(90+5′) · 경합 8승5패 · 회수 8 · 태클 3 | (79.6, 47.7) · Δ+2.6 | 90분 내내 우측 전 구간을 오르내렸다. xG 0.64는 팀 2위 — 윙백인데 박스 안에 반복해 들어갔다 | `wm_widemid/Support` **.724** (안필드는 `wm_winger/Balanced`) — 시즌 measured는 `wm_winger/Balanced` .789(n=4) 유지 |
| 마르코스 요렌테 | RCM (명목) → **지시된** 우측 커버 | 60′ · 6.8 · 키패스 2 · 경합 3승4패 · 회수 5 | (78.5, 49.3) · Δ**+22.5** | **이 경기 최대 실측-명목 괴리인데, 표류가 아니라 설계였다.** 현지 분석: 42분 5-4-1 전환 때 「소시에다드가 공격을 가장 많이 쏟던 측면」에 의도적으로 배치됐고, 도해 캡션은 「Llorente vigila muy de cerca de Soler e impide así que el valenciano busque una carrera de Sergio a la espalda del propio Pubill」(요렌테가 솔레르를 아주 밀착 감시해 **푸빌 등 뒤로의 침투**를 막는다)로 기능을 특정한다. 즉 **푸빌의 구조적 누출을 막는 보정 장치**였다. 60분 교체, 교체 후 불만 표출(ItC) | `cm_halfwinger/Support` **.541** — 낮은 적합은 「중앙 역할군으로 윙 폭을 설명 못 함」의 신호. 시즌 measured(RB `fb_wingback/Balanced` .912)는 **변경하지 않았다** |
| 알렉스 바에나 | LAM | 59′ · **6.4** · xG 0.05 · 경합 3승**8**패 · 터치 36 · 패스 27/24 | (36.3, 49.8) · Δ−5.7 | 경합 8패는 팀 최다. 좌측 하프스페이스에서 고립됐고 볼 관여가 거의 없었다. 59분 첫 교체 대상 | `cam_playmaker/Build-Up` **.457** — 적합 최저. 역할이 실제로 수행되지 않았다는 뜻으로 읽는다 |
| 알레한드로 그리말도 | LM (좌측 카릴레로) | 90′ · 7.3 · **xG 0.84**(팀 최고) · **골 1(PK)·도움 1** · 키패스 1 · 터치 70 | (18.3, 52.0) · Δ**−21.7** | ⭐ **전진은 무조건이 아니라 조건부였다.** 상대 좌윙 바레네체아에게 맨마킹으로 묶여 71분(바레네체아 교체 아웃)까지 수비에 붙잡혔고, 그 뒤부터 전방 진출이 열렸다 — 득점·도움이 전부 84분 이후인 것과 정합한다. 크로스 배급 질은 현지 혹평 | `wm_widemid/Support` **.769** — 시즌 measured는 아직 `LB fb_att_wb/Support` .898(백4 표본)이다. **백3 좌WB 표본 2경기째**. ⭐ FC 함의: 상시 오버래핑이 아니라 **같은 쪽 상대 윙어 유무에 종속**되는 전진 |
| 이강인 🇰🇷 | RAM | 60′ · 6.6 · xG 0.04 · xA 0.053 · 키패스 1 · 터치 **34** · 패스 22/15 | (78.6, 54.3) · Δ+6.6 | 우측 10번 자리인데 툴x 78.6으로 윙에 붙었다. 터치 34는 선발 필드플레이어 최저. ⚠️ **위치 서술 3중 충돌**: 한국 매체는 「좌측 미드필드/윙어」, 바스크 분석은 「5-4-1의 단독 최전방」, 실측은 **우측 넓게**다 — **실측 채택**. 시메오네 진단: 「La Real Sociedad trabajó muy bien sobre el juego asociativo de Kang-In Lee y Baena, lo que nos hizo no tener profundidad」(소시에다드가 이강인·바에나의 연계에 아주 잘 대응했고, 그래서 우리는 종심을 갖지 못했다) | `cam_halfwinger/Balanced` **.665** — 안필드(.597)와 같은 역할로 두 경기 연속 |
| 아데몰라 루크먼 | ST (명목 최전방) | 76′ · **6.2**(팀 최저) · 슈팅 **0** · 키패스 3 · 터치 **26** · 경합 2승**7**패 | (24.8, 63.1) · Δ**−12.2** | 9번으로 적혔지만 좌측으로 흘렀고 **슈팅 0개**. 지시는 「고립된 9번」(Infobae 「Lookman como '9' aislado」)이었고 좌측 표류는 본인 성향이다. 현지 평가 만장일치 미스캐스팅 — El Desmarque 4점 「Sigue demostrando que no sabe jugar como delantero centro. Desubicado」(계속해서 중앙 공격수로 뛸 줄 모른다는 것을 증명한다. 자리를 못 잡았다). ItC는 60분 4-3-3 복귀 후 편해졌고 **그리말도와의 좌측 조합**에 가능성이 있다고 봤다 | `st_advanced/Support` **.603** — 안필드 9번(알바레스)은 `st_false9/Build-Up`이었다. **9번 유형이 바뀌었다**. ⭐ 서사·실측 합치: 9번이 아니라 **좌측 인사이드 포워드**로 재현해야 한다 |
| 조니 카르도소 | 교체 59′(←바에나) · LAM→LCM | 31′ · 6.5 · xG 0.05 · 터치 17 · 옐로(75′) | (31.3, 56.8) | 60분부터 좌측 중앙으로 내려 중원을 메웠다. 짧은 표본 | `cm_playmaker/Roaming` .508 — hp22, 참고값 |
| 코케 | 교체 60′(←이강인) · RAM | 30′ · 6.8 · 터치 24 · 패스 21/19 | (59.7, 56.2) | 이강인 자리에 들어갔으나 **훨씬 안쪽**(툴x 59.7 vs 78.6)에 섰다 — 우측 과밀을 교체로 푼 셈 | `cam_classic10/Versatile` .677 — hp27, 참고값 |
| 조나단 데이비드 | 교체 60′(←요렌테) · ST | 30′ · **7.9** · **xG 0.26 · 골 1**(90′) · 슈팅 2 | (54.8, 64.1) | **ATM 데뷔 이후 첫 골.** 30분에 슈팅 2·xG 0.26으로 루크먼의 76분(슈팅 0)을 뒤집었다 | `st_poacher/Attack` .354 — **hp14로 임계 미달**, 그리드 근거로 쓰지 않는다 |
| 아르나우 오르티스 | 교체 76′(←루크먼) · LAM | 14′ · 6.7 · 키패스 1 · 터치 10 | (18.8, 57.6) | 좌측 끝에서 폭 유지 | `cam_halfwinger/Balanced` .608 — **hp14로 임계 미달**, 참고값 |

## 6. 전술 변화 판정

**유지된 것**
- **백3(3-4-2-1)** — 안필드(09-09)에 이어 **2경기 연속**. 원정 · 상대 4-2-3-1도 동일.
- 낮은 라인(def_x 34.1 → 36.0)과 저블록 처리(클리어·공중경합 우위).
- 우측 과밀 기하 — 안필드 슬롯 등재 당시 이미 「RCB(푸빌) x84는 사실상 RWB 폭, RM(요렌테 x77)과 겹친다」로
  캐비앗을 달았는데 **이번에 그대로 재현됐고 더 심해졌다**(요렌테가 RCM 명목으로 x78.5).

**새로 나타난 것**
- ⭐ **백3가 임기응변이 아니라 설계라는 두 번째·더 강한 증거.** WhoScored 라벨은 95분 내내 `3421`이었다
  (안필드는 라벨이 세 번 바뀌었다). ⚠️ 단 라벨 불변이 구조 불변은 아니다 — 현지 분석은 5-3-2 → 5-4-1(≈42′)
  → 보유 시 4-3-3의 3단 변형을 서술한다(§4). **변한 것은 앞선 인원이고 백3 자체는 끝까지 유지됐다.**
- ⭐⭐ **「유럽 원정 한정 조정」 가설은 기각된다.** 바스크 전술 분석이 안필드전을 「수비 시 명확한 5-3-2」로 규정하고,
  **이번 백3를 그 연속으로, 그리고 상대 4-2-3-1에 대한 맞춤으로** 설명한다 —
  「el Atlético se ajustó al 4-2-3-1 del Liverpool (sobre el papel el mismo dibujo de la Real) defendiendo
  con el mencionado 5-3-2」(아틀레티코는 리버풀의 4-2-3-1 — 서류상 레알 소시에다드와 같은 그림 — 에 맞춰
  앞서 말한 5-3-2로 수비했다). ⚠️ **그러나 이것은 「상대 맞춤」의 근거이지 「체제 전환」의 근거가 아니다.**
  시메오네 본인은 백3 지속 여부 질문에 「Well, time will tell」(글쎄, 시간이 말해줄 것이다)로 확약을 피하고
  CB 3인 영입 경쟁 서사로 답을 돌렸다 — **현 단계는 「보유 CB 3인을 동시에 쓰기 위한 구조 실험」으로 읽는 것이 소스에 충실하다.**
- ⭐ **압박 주도권 역전.** 시즌 처음으로 상대 PPDA(11.35)가 우리(15.14)보다 낮았다.
  8월(7.77·8.26)과 9월(15.13·12.52·15.14)은 대역이 다르다 — obs#350~352의 「시메오네 압박 상수 8.26」은
  **8월 한정 값으로 다시 좁혀야 한다.**
- ⭐ **9번 유형 교체.** 안필드 알바레스 `st_false9/Build-Up`(하강 연계형) → 이번 루크먼 `st_advanced/Support`(전방 고정형).
  같은 3-4-2-1 안에서 9번 유형이 바뀌었고, 루크먼 쪽 결과가 훨씬 나빴다(슈팅 0·평점 6.2).
- **시즌 최고 xG 2.05**(직전 최고 1.02). 점유 46%에서 나왔다.

**직전 경기(안필드) 대비 변화**
- 결과 역전(1-2 패 → 3-0 승)인데 **구조는 더 수동적**이었다(PPDA 12.52→15.14, def_x 34.1→36.0은 사실상 동일).
- 안필드 D+3에서 관측된 「연결고리 3인 전원 제거 → equipo plano」 패턴이 **이번에도 59~60분에 반복**됐다
  (바에나·이강인·요렌테 동시 교체). 다만 이번엔 그 뒤 3골이 났다 — 같은 조치, 반대 결과다.
  ⚠️ 두 경기로 「이 교체가 효과적이다」라고 결론 낼 수 없다. **다음 표본에서 재검증 항목으로 남긴다.**

**`manager_profiles`·`observations` 반영**
- `formation`·`pressing`·`role_demands` 3축에 덧붙임(내용은 §9).
- 미해결 「ATM 포메이션 4-4-2 vs 백3」(HANDOFF 미해결 #1)은 **백3 쪽으로 한 걸음 더 갔다** —
  다만 2경기 모두 **원정 + 상대 4-2-3-1**이라 교란이 분리되지 않았다. 홈 경기 또는 다른 상대 포메이션에서
  백3가 나와야 확정된다.

## 7. 게임 구현 판정

- **결론: 추가 관찰.**
  단일 경기이고 커널 Δ는 전부 노이즈 구간(≤.05)이다. 시즌 `team_tactic_setups`·`slot_canon_roles`는 **변경하지 않는다.**
- **이 경기 전용 팀 설정**(`match_game_setups`, `match_only=1`):
  FC26 / **3-4-2-1** / 빌드업 **Counter** / 수비 접근 **Balanced** / 라인 **48** / tactic_code 없음.
  - 규칙 대조(`core.team_settings.suggest(점유 46, 패스 462, 롱볼시도 64, PPDA 15.14)`):
    `Counter` / `Balanced` / 라인 48~58 · 롱볼 13.9%. `compare()` **편차 없음 → `rule_note='RULE'`**.
  - 라인은 제안 구간의 **하단(48)** 을 택했다 — 실측 def_x 36.0과 리드 후 27.0이 구간 상단과 맞지 않는다.
    (구간 안이라 편차로 잡히지 않는다.)
- **이 경기 선발 11명**(`match_player_prescriptions`, FC26, `match_only`):

| 슬롯 | 선수 | 역할 | 포커스 | 단일 경기 fit |
|---|---|---|---|---|
| GK | 오블락 | `gk_goalkeeper` | Defend | .957 |
| LCB | 한츠코 | `cb_wideback` | Aggressive | .770 |
| CCB | 로메로 | `cb_bpd` | Aggressive | .930 |
| RCB | 푸빌 | `cb_wideback` | Support | .636 |
| LM | 그리말도 | `wm_widemid` | Support | .769 |
| LCM | 율만 | `cm_b2b` | Ball-Winning | .792 |
| RCM | 마르코스 요렌테 | `cm_halfwinger` | Support | .541 |
| RM | 줄리아노 시메오네 | `wm_widemid` | Support | .724 |
| LAM | 바에나 | `cam_playmaker` | Build-Up | .457 |
| RAM | 이강인 | `cam_halfwinger` | Balanced | .665 |
| ST | 루크먼 | `st_advanced` | Support | .603 |

  교체 4명도 같은 표에 `starter=0`으로 기록했다(카르도소 LCM `cm_playmaker/Roaming` .508 · 코케 RAM
  `cam_classic10/Versatile` .677 · 조나단 데이비드 ST `st_poacher/Attack` .354 · 오르티스 LAM
  `cam_halfwinger/Balanced` .608). ⚠️ 데이비드·오르티스는 hit_points 14로 **그리드 임계 미달**이다.

- **`prescriptions` 변경**: 포지션-순수가 유지된 5명만 갱신했다 — 오블락 GK .970(n5→6) · 한츠코 LCB .885→**.863**(n5) ·
  푸빌 RCB .884→**.877**(n3) · 줄리아노 시메오네 RM .808→**.789**(n3→4) · **로메로 CCB .930 신규(n2)**.
  전부 Δ≤.05 노이즈 구간이라 **인선 변경은 없다.**
  ⛔ 그 외 선수(요렌테·이강인·그리말도·율만·바에나·루크먼)는 백3 전환으로 `pos_class`가 바뀌어
  기존 measured 행의 `pos_label`과 어긋난다. **표본을 섞지 않기 위해 갱신하지 않았다** — §9의 관측 항목으로 남긴다.

- **다음 경기 재검증 항목**
  1. **백3가 홈·다른 상대 포메이션에서도 나오는가**(현재 2경기 모두 원정 + 상대 4-2-3-1).
  2. **9월 PPDA 15 대역이 유지되는가** — 3경기째면 「압박 상수 8.26」을 시즌 축에서 분리한다.
  3. **9번 유형**(루크먼 advanced vs 알바레스 false9) 중 무엇이 정착하는가.
  4. 59~60분 3중 교체가 반복되는가, 그리고 그 전후 효과.
  5. 요렌테의 RCM 명목 / 윙 폭 실측 괴리(Δx +22.5)가 재현되면 **ATM 3-4-2-1 슬롯 기하를 2경기 중앙값으로 재산출**한다.

⚠️ 이 설정은 `match_game_setups`·`match_player_prescriptions`의 `MATCH ONLY` 프리셋이다.
전체 시즌 전술이나 대표 선수 역할에 자동 병합하지 않는다.

## 8. 영상·기사·감독 발언 (D+1, 2026-09-14)

⭐ 인용은 전부 **원문 + 한국어 번역 병기**다(불변규칙 11). 영역 경유분은 그 사실을 명기한다.

### 8-1. 소스 인벤토리

| 언어 | 매체 | 제목 | 게시일 | 확인 방식 |
|---|---|---|---|---|
| ES | **Noticias de Gipuzkoa** (바스크) ⭐ **이번 회차 최고 소스** | Por qué Simeone (padre) fue el mejor del Atlético ante la Real | 2026-09-14 | 브라우저 직접(전문+도해 캡션) |
| EN | Into the Calderón | Diego Simeone praises impact players after Atleti thrash Real Sociedad | 2026-09-14 | 브라우저 직접(회견 영역 전문) |
| EN | Into the Calderón | Real Sociedad 0-3 Atlético Madrid: Player Ratings | 2026-09-14 | 브라우저 직접 |
| ES | El Desmarque | El uno por uno del Atlético… cuatro notables y tres suspensos | 2026-09-13 | WebFetch 직접 |
| ES | Infobae(EFE) | Simeone: "El partido dura 90 minutos y los cambios nos han dado fuerza" | 2026-09-13 | WebFetch 직접 |
| ES | Infobae(EFE) | Crónica del Real Sociedad - Atlético de Madrid: 0-3 | 2026-09-13 | WebFetch 직접 |
| ES | Infobae(EFE) | Matarazzo: "Llevamos tres partidos con acciones rigurosas en contra" | 2026-09-13 | WebFetch 직접 |
| ES | VAVEL España | Simeone: "Aprovechamos los pasajes del partido que nos fueron favorables" | 2026-09-14 | WebFetch 직접 |
| ES | Futeros | Simeone explica su decisión con Grimaldo: "Charlamos un montón" | 2026-09-14 | WebFetch 직접 |
| EN | Football España | Atlético Madrid vs Real Sociedad: 3-0 away win | 2026-09-14 | WebFetch 직접 |
| KO 🇰🇷 | 머니투데이 | 교체 후 표정까지 굳은 이강인, 현지 저격성 혹평에 최저 평점까지 | 2026-09-14 | WebFetch 직접 |
| JA 🇯🇵 | フットボールチャンネル | 久保建英、2戦連続で先発落ち 71分から途中出場も… | 2026-09-14 | WebFetch 직접 |
| ES | YouTube / **Atlético Stats** | REAL SOCIEDAD 0-3 ATLETI: DESPEGUE A TIEMPO EN ANOETA (`RDHt-dGo644`) | 2026-09-13~14 | ⚠️ **채널·제목·설명만. 미시청 — 근거로 쓰지 않았다** |
| ES | YouTube / Atlético Stats | VICTORIA DE INFLEXIÓN EN ANOETA \| LAS NOTAS… EL FACTOR JONATHAN DAVID (`_fKMMU1kcxM`) | **2026-09-14 23:00 공개 예정** | 예약 상태만 확인 → **D+2 재확인 대상** |
| ES | Sphera Sports | El Atleti sale victorioso de Anoeta y toma aire | **게시일 미노출** | WebFetch — **발행일 불명, 보조 근거 등급** |
| IT | Virgilio Sport | Atletico Madrid, Lookman timido e involuto… | **2026-03-07** | WebFetch → **다른 경기라 기각** |

**4종 집계**: 유튜브 **2건**(1 미시청 · 1 미공개) · 전술 블로그/분석 **3건** · 기사 **9건** ·
감독 1차 발언 **2인 4건**(시메오네 3 · 마타라초 1). 403 차단 후 브라우저 경로로 회수 3건.

### 8-2. 감독 발언

**디에고 시메오네 (ATM, 경기 후 회견 2026-09-13)**

- 백3 지속 여부 질문에 — 「Well, time will tell.」 (글쎄, 시간이 말해줄 것이다.)
  이어 CB 영입 경쟁으로 화제를 돌렸다: 「El trabajo nuestro tanto con el Cuti y con Hancko… El club hizo
  un gran esfuerzo para traer al Cuti. Pubill se lo ganó con su trabajo.」
  (쿠티(로메로)와 한츠코 양쪽에 대한 우리의 작업이… 구단은 쿠티를 데려오려 큰 노력을 했다. 푸빌은 자기 노력으로 그 자리를 얻었다.)
  ⚠️ 영문 부분은 Into the Calderón **영역 경유**.
- 「Fuimos contundentes en defensa.」 (우리는 수비에서 단호했다.)
- **전반 부진의 자체 진단** — 「La Real Sociedad trabajó muy bien sobre el juego asociativo de Kang-In Lee
  y Baena, lo que nos hizo no tener profundidad.」
  (레알 소시에다드가 이강인과 바에나의 연계 플레이에 아주 잘 대응했고, 그 때문에 우리는 종심을 갖지 못했다.)
- **교체 설명** — 「El partido dura 90 minutos y los cambios nos han dado fuerza. Koke nos dio calma,
  Cardoso fuerza y Arnau pólvora.」
  (경기는 90분간 계속되고 교체가 우리에게 힘을 줬다. 코케는 침착함을, 카르도소는 힘을, 아르나우는 화력을 줬다.)
- **바에나·이강인 교체의 결과론 방어** — 「If the game had ended with a different result, people would have
  asked why I took out Álex Baena and Kang-in Lee. But it's part of your job, and part of mine, to stick
  with what you believe in.」 (경기가 다른 결과로 끝났다면 사람들은 내가 왜 알렉스 바에나와 이강인을
  뺐냐고 물었을 것이다. 하지만 자기가 믿는 것을 밀고 나가는 게 당신 일의 일부이자 내 일의 일부다.)
  ⚠️ 영역 경유. **교체 사유 자체는 끝내 말하지 않았다.**
- **그리말도** — 「No arrancó bien, pero parece que necesitaba un partido así. Charlamos un montón antes
  del partido, tiene una personalidad muy buena… Por suerte salió el partido que él quería y nosotros, también.」
  (시즌 출발이 좋지 않았지만 이런 경기가 필요했던 것 같다. 경기 전에 아주 많이 이야기했다. 그는 대단히 좋은
  성격을 가졌다… 다행히 그가 원하던 경기가, 그리고 우리가 원하던 경기가 나왔다.)
- **루크먼·이강인 선발 이유를 데이비드에게 설명했다** — 「obviously explaining why Kang-in Lee and Ademola
  Lookman were starting, because they've obviously been playing more often and he's only been here a short time.」
  (이강인과 아데몰라 루크먼이 왜 선발인지 분명히 설명했다. 그 둘은 더 자주 뛰어왔고 그는 여기 온 지 얼마 안 됐기 때문이다.)
  ⚠️ 영역 경유. ⭐ **서열 근거가 「경기력」이 아니라 「누적 출전」이라고 감독이 직접 말했다.**

**펠레그리노 마타라초 (Real Sociedad, 경기 후 회견 2026-09-13)**

- ⭐ **전술적으로 가장 중요한 한 줄** — 「No hemos conseguido generar lo suficiente con la pelota ante
  una defensa tan baja como la del Atlético.」
  (아틀레티코처럼 **그렇게 낮은 수비**를 상대로 우리는 볼을 갖고 충분히 만들어내지 못했다.)
  ⇒ 상대 감독이 ATM의 **저블록**을 1차 증언했다 — 우리 def_x 36.0 실측과 정합한다.
- 판정 불만(PK) — 「Está claro que no es penalti. Es el tercer partido así.」
  (페널티가 아닌 게 명백하다. 이런 경기가 세 번째다.) / 「Llevamos tres partidos con acciones rigurosas
  en contra… y eso al final significan puntos.」 (세 경기 연속 가혹한 판정을 겪고 있다… 그건 결국 승점을 의미한다.)
  ⚠️ 자기 방어로 보고 **인과 설명에서는 배제**했다.

### 8-3. 미수행 소스와 사유

| 언어축 | 결과 |
|---|---|
| 스페인어 | 다수 확보. ⚠️ **Marca·AS·Relevo·COPE·SER 자체 URL은 검색에 노출되지 않아 직접 열지 못했다** — El Desmarque·VAVEL·Infobae(EFE)·Futeros로 대체 |
| 바스크 | **Noticias de Gipuzkoa 전술분석 1건 확보(최고 소스)**. `diariovasco.com`·EITB·Berria **0건**. **순수 에우스케라 검색어 미수행 — 시간 배분** |
| 한국어 🇰🇷 | 1건(머니투데이) |
| 일본어 🇯🇵 | 1건(フットボールチャンネル — 쿠보 2경기 연속 선발 제외, 71분 투입, 「"主力"の肩書き失う」 '주전' 타이틀을 잃었다) |
| 이탈리아어 | **이 경기 다룬 기사 개봉 0건**. 열어본 Virgilio 기사는 2026-03-07자 다른 경기 → 기각 |
| 프랑스어 | 조나단 데이비드 — **L'Équipe 0건**, 소규모 매체만 노출·미개봉 |
| 덴마크어 | 율만 — **0건**(BT·Bold.dk·Tipsbladet 미노출) |
| 슬로바키아어 | 한츠코 — **미수행(시간 배분)** → D+2 과제 |
| 포르투갈어 | 카르도소 — **미수행**(미국 국적·59분 투입으로 우선순위 하위) |
| 독일어 | 마타라초 — **미수행(시간 배분)**. 회견은 스페인어로 충분히 회수됨 → D+2 과제(Kicker·Sport1) |
| 유튜브 사이트 내부검색 | `sp=EgIIAw%3D%3D`(이번 주) 필터로 스윕 — 전술분석 채널 **1개(Atlético Stats)**, 나머지는 하이라이트·쇼츠. **D+2~D+3 재확인 필수**(지연 게시 규칙) |

### 8-4. 소스 충돌과 신뢰도 경고

1. ⛔ **교체 짝 불일치.** AS 계열은 `Koke ← Llorente(59)` / `J.David ← Kang-in(59)`로, SofaScore(`Koke ← 이강인`,
   `David ← 요렌테`)와 반대다. **SofaScore 실측 채택** — WhoScored 포지션 블록(60~77분)에서 코케가 이강인이
   있던 RAM 좌표(vert 7.5 / horiz 3.5)에, 데이비드가 최전방(vert 9)에 들어간 것이 SofaScore 짝짓기를 지지한다.
2. ⛔ **이강인 위치 3중 충돌**(한국 매체 좌측 / 바스크 분석 단독 최전방 / 실측 우측 넓게) → **실측 채택**.
3. ⚠️ **Marca·AS 평점 코멘트는 한국어 중역만 확보**(「볼 터치가 너무 많다」·「그리즈만의 원터치를 그리워한다」).
   **원문 미확보이므로 불변규칙 11에 따라 DB에 인용하지 않았다.**
4. ⚠️ **득점 시각이 소스마다 다르다**(PK 81′/82′/84′ · 2번째 89′/90′ · 3번째 90+5′/94′/95′) → **SofaScore 정본 채택**.
5. ⚠️ **율만 평가가 정반대다** — El Desmarque 7 「Fue el dueño y señor」(주인이자 지배자) vs Into the Calderón 5
   「failed to demonstrate any connection with players further forward」(전방 선수들과 어떤 연결도 보여주지 못했다).
   **어느 쪽도 단독 채택하지 않았다** — 커널 적합 .792와 전진 패스 실측으로 판정할 항목으로 남긴다.
6. ⚠️ **바스크 매체 편향 보정**: 자국 팀 패배를 「명백히 과도한 스코어」로 완화하는 경향이 있으나,
   **도해 캡션의 구체 행동 서술**(푸빌 추격 · 요렌테의 솔레르 밀착 · 카르도소 프리)은 형용사가 아니라
   검증 가능한 행동 기술이므로 채택했다(불변규칙 10 운영 지침).
7. ⚠️ **유튜브 영상 2건 모두 미시청** — 내용을 근거로 쓰지 않았다. 자막 전사 인용 없음(auto-caption 경고 해당 없음).
8. ⚠️ **Into the Calderón 회견 인용은 영역본**이다. 스페인어 원문은 Infobae·VAVEL 부분만 대조 확보했다.

## 9. 데이터 반영과 한계

**DB에 추가한 행**
- `matches` 1행(id 106, event 16416332) · `player_matches` **15행**(출전 전원, `match_id` 연결) ·
  `team_match_stats` 1행(`xg_source='FotMob'` · `ppda_method`·`def_x_method` = `core.whoscored` 정본).
- 국면 분리 그리드: 15명 전원에 `cells_poss`/`cells_def`/`map25_poss`/`map25_def`/`phase_source` 기록
  (WhoScored matchId=1994164 이벤트 기준). `possession=46.0`, `stats_json`에 `phase_level/lead/trail` 기록.
- `prescriptions` measured 갱신 4행 + 신규 1행(로메로).
- `match_reports` 1행 + `match_player_reports` 15행 + `match_game_setups` 1행 + `match_player_prescriptions` 15행.

**한계**
- **단일 경기**다. 커널 Δ≤.05는 정본 처방 변경 근거가 아니다.
- **교란이 분리되지 않았다**: 원정 · 상대 4-2-3-1 · 84분까지 0-0 · 마지막 6분 3골.
  스코어 국면이 `lead` 12분뿐이라 @lead/@trail 분리 집계에는 거의 기여하지 못한다.
- `def_x` ATM 표본 2건 — 절대 수준 해석 불가, 경기 간 비교만 가능.
- 롱볼·크로스 시도는 역산값(§1).
- ⚠️ **§4의 3단 변형(5-3-2 → 5-4-1 ≈42′ → 보유 시 4-3-3)은 현지 분석의 서술이지 우리 1차 실측이 아니다.**
  WhoScored 라벨은 `3421` 단일이었고, 전환 시각을 이벤트 데이터로 독립 확인하지 못했다.
  ⭐ 가능한 검증법(HANDOFF 「다음 할 일 6」과 같은 방법): WhoScored 이벤트 타임라인으로 이강인·루크먼의
  **평균 위치 변화 시점을 역산**한다 — 다음 회차 과제로 남긴다.
- ⚠️ 서사 축 미수행 언어권 4개(슬로바키아어·포르투갈어·독일어·순수 에우스케라)와
  이탈리아어·프랑스어·덴마크어 0건은 §8-3에 검색어와 함께 기록했다. **D+2~D+3에서 재시도한다.**
- ⭐ **`pos_class` 불안정 관측**: 백3 전환으로 여러 선수의 `pos_class`가 기존 measured `pos_label`과 어긋난다
  (이강인 RM 4경기 vs 처방 RST · 요렌테 RM 2경기 vs 처방 RB · 그리말도 LM vs 처방 LB ·
  율만 RCM vs 처방 LDM · 바에나/루크먼 ST vs 처방 LST/LM). **이번 회차에서는 고치지 않았다** —
  백3 표본이 2경기뿐이라 지금 pos_label을 바꾸면 백4 표본과 섞인다. 표본 3경기에서 재판정한다.
- `match_reports.status`: 필수 섹션·출전 전원 선수 행·경기 전용 팀 설정·11명 역할이 모두 있어 **complete**.

---

## D+2 추적 (2026-09-15)

> 회차 범위는 **이 경기 한정**이다. 가중치는 런북 §2-1a대로 **유튜브 전술 분석·전술 블로그**에 뒀다 —
> D+1에 빈손이었던 두 종이 이번 회차에 **전부 열렸다**. 인용은 전부 원문 + 한국어 번역 병기(불변규칙 11).
> ⚠️ 유튜브 전사는 **auto-caption**이다(오인식 가능) — 인용마다 명기한다.

### D+2-1. 이월 과제 처리 결과

| # | D+1 과제 | 결과 |
|---|---|---|
| 1 | 예약 영상 `_fKMMU1kcxM` 공개 확인·전사 | ✅ **공개됨**(2026-09-14 23:00 라이브, 22시간 전). 전사 **1,982 cue** 확보 |
| 2 | `RDHt-dGo644` 전사 확보 | ✅ 전사 **685 cue** 확보. D+1의 「미시청」 해소 |
| 3 | 유튜브 사이트 내부 검색 스윕 | ✅ 2개 축으로 실행 → **신규 2채널**(상대팀 관점 1 포함) |
| 4 | 미수행 언어축 4개 | 독일어 **0건** · 슬로바키아어 **0건(403)** · 포르투갈어 **0건** · 에우스케라 **1건 확보** |
| 5 | 0건이었던 언어축 재시도 | 이탈리아어 **0건(재확인·기각 확정)** · 프랑스어 **0건(403)** · 덴마크어 **1건 확보** |
| 6 | Marca·AS 원문 URL | **Marca 확보 ✅**(uno a uno 전문 + D+2 신규 분석) · **AS 미확보**(경로 4종 전부 실패) |
| 7 | diariovasco·EITB·Berria 브라우저 직접 | ✅ **diariovasco 해소**(D+2 전술 분석 확보, 이번 회차 최고 소스 중 하나) · **Berria 해소**(에우스케라 1건) |

### D+2-2. 신규 소스 인벤토리

**유튜브 전술 분석 — 4건(전부 전사 확보, auto-caption)**

| 채널 | 제목 | 게시일 | video_id | 확인 방식 |
|---|---|---|---|---|
| **Atlético Stats** ⭐ 이번 회차 최고 소스 | VICTORIA DE INFLEXIÓN EN ANOETA \| LAS NOTAS… EL FACTOR JONATHAN DAVID | **2026-09-14** (라이브) | `_fKMMU1kcxM` | **전사 전문**(1,982 cue) |
| Atlético Stats | REAL SOCIEDAD 0-3 ATLETI: DESPEGUE A TIEMPO EN ANOETA | **2026-09-13**(경기 직후) | `RDHt-dGo644` | **전사 전문**(685 cue) |
| **El Rincón de la Real** ⭐⭐ **상대팀 관점** | GOLEADA ENGAÑOSA \| Resumen y notas 1x1 Real Sociedad 0-3 Atlético | 2026-09-14 | `uGlZbUGrHZs` | **전사 전문**(615 cue) |
| Espíritu del Manzanares | REAL SOCIEDAD 0-3 ATLETI — La efectividad salva al Atleti \|#3 | 2026-09-14 | `UBaPgLg4kKI` | **전사 전문**(1,885 cue) |

- 예약 확인: **Atlético Stats `zFvDU2SSXMo`** 「¿ONCE DE ROTACIONES DEL ATLETI VS OSASUNA? \| **EL MOMENTO JONATHAN DAVID**」
  — **2026-09-15 23:00 공개 예정** → **D+3 대상**. 같은 채널이 「mañana tenemos vídeo de Lookman」(내일 루크먼 영상이 있다)로
  예고한 **루크먼 전용 분석**도 D+3에서 찾는다.

**전술 블로그·기사 — 신규 5건**

| 언어 | 매체 | 제목 | 게시일 | 확인 방식 |
|---|---|---|---|---|
| **ES** | **El Diario Vasco** ⭐⭐ (Imanol Troyano) | Un accidente que no debe echar todo por tierra | **2026-09-15 (D+2)** | 브라우저 직접(전문) |
| ES | **Marca** (Isaac Suárez) | Uno a uno del Atlético: Grimaldo y Jonathan David encuentran el gol que necesitaban | 2026-09-13 23:09 | 브라우저 직접(**전문 — D+1 미확보분 해소**) |
| ES | **Marca** (Isaac Suárez) | Un Atlético de arreones | **2026-09-15 13:23 (D+2)** | 브라우저 직접(전문) |
| **EU** 🏴 | **Berria.eus** (Julen Urrestarazu) — **순수 에우스케라** | Realak azken minutuetan galdu du Atletico Madrilen aurka | 2026-09-14 07:40 | 브라우저 직접(전문) |
| **DA** 🇩🇰 | **bold.dk** | Sene scoringer bag Atlético-sejr | 2026-09-13 | WebFetch 직접 |
| EN | tacticalfootballanalysis.com (Mohamed Ouni) | Real Sociedad vs Atlético Madrid [0-3] Tactical Analysis | **2026-09-15 (D+2)** | WebFetch — ⚠️ **실측 충돌로 등급 강등**(D+2-6) |
| EN | Pulse Sports Nigeria | Simeone must apologise to Lookman again as new system propels… | 2026-09-13 | WebFetch — 보조 등급 |

**4종 집계(D+2 신규분)**: 유튜브 전술분석 **4건(전부 전사)** · 전술 블로그 **2건**(Diario Vasco · tacticalfootballanalysis) ·
기사 **5건** · 감독 1차 발언 **0건 신규**(회견은 D+1에 회수 완료, 이후 새 발언 미발생).

### D+2-3. ⭐⭐ 가장 큰 수확 — 포메이션 3단 변형이 **5단**으로 확장되고 전환 시각이 좁혀졌다

D+1 §4는 Noticias de Gipuzkoa 단독으로 **5-3-2 → 5-4-1(≈42′) → 보유 시 4-3-3**의 3단을 적었고,
「42분은 1차 실측이 아니다」를 한계로 남겼다(§9). **D+2에 독립 소스 2건이 더 나왔고 단계가 늘었다.**

**Atlético Stats `_fKMMU1kcxM`가 화면 도해와 함께 제시한 순서**(auto-caption):

1. **0~10분 — 고압박 시도.** 「Giuliano al principio, aunque luego acabó como carrilero, intentó el Atleti
   mantener el 442, presionar arriba, estuvo cerca de causar varias pérdidas peligrosas de la Real」
   (줄리아노가 초반에, 비록 나중엔 카릴레로로 끝났지만, 아틀레티코는 **4-4-2를 유지하며 위에서 압박**하려 했고
   레알의 위험한 실책을 여러 번 유발할 뻔했다.)
   ⚠️ **같은 방송 안에서 이견이 있다** — 다른 출연자는 「Yo no comparto mucho lo del inicio en el 442…
   creo que más o menos estábamos así también 3 4 2 1」(초반 4-4-2라는 데는 별로 동의하지 않는다…
   내 생각엔 초반에도 대략 3-4-2-1이었다)로 반박한다. **라벨은 합의되지 않았고, 「초반엔 높게 압박했다」만 합의된다.**
2. **≈15분 — 고블록 → 저블록.** 「El siguiente paso fue bajar para atrás. Yo no entendí pasar de bloque alto
   a bloque bajo y además es clarísimo minuto 15」 (다음 단계는 뒤로 내려가는 것이었다. 고블록에서 저블록으로
   가는 걸 이해하지 못했고 게다가 **15분이라는 게 아주 명확하다**.)
   원인 특정: 「se ajusta muy mal la presión desde el sector izquierdo con Lookman, que no la hace a la
   intensidad que realmente toca」 (**좌측에서 루크먼과 함께 압박 조절이 아주 잘못됐고**, 그는 실제로
   필요한 강도로 하지 않는다.)
3. **중간 — 이강인이 눌리며 세컨드 스트라이커/우측 미디어푼타로.** 「acabamos aculando un poquito a Kang-in Lee
   que estaba de **segundo punta, media punta diestro**, segundo delantero」 (이강인을 조금 뒤로 몰아붙이게
   됐는데 그는 **세컨드 스트라이커, 우측 미디어푼타**, 두 번째 공격수였다.)
4. **5-4-1 — 이강인 최전방, 루크먼 좌측.** 「el siguiente paso fue ya este, es decir, **Kang-in en punta,
   Lookman izquierda, nos reordenamos en un 541**」 (다음 단계는 바로 이것, 즉 **이강인이 최전방, 루크먼이 좌측,
   우리는 5-4-1로 재배열했다**.)
5. ⭐ **5-5-0 — 아무도 앞에 없는 구간.** 「Hubo momentos que la presión era un 5, es decir, no había nadie…
   lo que vemos ahí al final después de ese 541, que era el 55」 (압박이 5였던, 즉 **아무도 없던** 순간들이
   있었다… 그 5-4-1 뒤에 마지막에 보이는 것, 그게 **5-5**였다.) 비교 대상으로 챔스 맨시티 원정을 든다.

**전환 시각 — 세 소스의 수렴**: Gipuzkoa 「≈42분」 / Atlético Stats `RDHt-dGo644` 「desde el 35 más o menos
se ha ido Lookman a izquierda y 541」(**35분 즈음부터** 루크먼이 좌측으로 갔고 5-4-1) / Atlético Stats
`_fKMMU1kcxM` 「15분 저블록 전환 → 그 뒤 5-4-1」.
⇒ **저블록 전환은 ≈15분, 5-4-1 재배열은 35~42분 구간**으로 좁혀진다. ⚠️ **여전히 우리 1차 실측이 아니다**
(WhoScored 라벨은 95분 내내 `3421`). 단 **소스 3종·독립 2진영(ATM 팬 분석 + 바스크 매체)** 으로 격상됐다.

⭐ **루크먼의 좌측 표류가 이 전환의 구성 요소로 서술된다.** D+1 §5는 「지시는 고립된 9번, 좌측 표류는 본인 성향」으로
적었는데, 두 영상은 **5-4-1 재배열 때 루크먼을 좌측으로 보낸 것이 배치였다**고 말한다 → D+2-7의 판정 정정 참조.

### D+2-4. ⭐⭐⭐ 「저블록은 설계인가 강제인가」 — 양 팀 관점이 정확히 반대다

D+1에는 마타라초의 「defensa tan baja」(그렇게 낮은 수비) 증언만 있었고 **원인**은 열려 있었다. D+2에 정면 충돌이 생겼다.

- **ATM 팬 전술 채널(Atlético Stats) — 「우리가 선택했다」**: 「ayer creo que **fue decisión del Atleti** y
  para mí fue una decisión excesivamente extrema… hay un tramo del Liverpool en Anfield que evidentemente
  ves el partido y dices, es el Liverpool el que te hace recular… **ayer no**」
  (어제는 **아틀레티코의 결정**이었다고 생각하고 내겐 지나치게 극단적인 결정이었다… 안필드의 리버풀전에는
  분명히 경기를 보면 **리버풀이 너를 물러나게 만든** 구간이 있다… **어제는 아니다**.) auto-caption.
  근거로 상대 무위협을 든다: 「la Real tuvo una posesión estéril en todo momento, prácticamente no remató
  a puerta hasta la segunda parte」(레알은 내내 **불임의 점유**를 했고 후반까지 사실상 유효슛이 없었다.)
- **상대 매체(El Diario Vasco, D+2) — 「우리가 밀어냈다」**: 「El Atlético se vio muy incómodo en la primera
  hora de juego por la incapacidad que tuvo de combinar por dentro y lo bien sujetado que estuvo por fuera,
  por lo que **no le quedó otra opción que** replegar rápido tras pérdida y situarse en bloque bajo」
  (아틀레티코는 첫 한 시간 동안 **안쪽으로 조합하지 못하는 무능**과 **바깥에서 잘 묶인 것** 때문에 매우 불편했고,
  그래서 볼을 잃은 뒤 빠르게 물러나 저블록에 자리 잡는 것 **외에 선택지가 없었다**.)

⛔ **실측 판정 — 「선택」 쪽이 이긴다.** 상대 xG **0.27** · 유효슛 3 · 박스 안 슈팅 **2** · 빅찬스 1(놓침).
「선택지가 없었다」고 할 만큼 상대가 압도한 흔적이 우리 이벤트에 없다. 또한 저블록 전환 시각으로 지목된 **≈15분**은
상대가 위협을 만들기 **전**이다. ⇒ **자발적 후퇴로 판정**하고, Diario Vasco 서술은 **상대팀 자기서사 편향**으로 분류한다.
⚠️ 단 Diario Vasco가 지목한 **원인 중 절반**(「안쪽으로 조합하지 못했다」)은 우리 실측과 정합한다 — 상대 진영 패스 163 대 269,
이강인 터치 34·바에나 터치 36. **「상대가 밀어냈다」는 기각하되 「안쪽 조합 실패」는 채택**한다.

⭐ **FC 함의**: 이 판정이 `match_game_setups`의 수비 접근을 지지한다. 실측이 「눌려서 내려갔다」가 아니라
「내려가기로 했다」이므로 라인 **48**(제안 구간 하단)과 `Balanced`는 그대로 둔다 — **변경 없음**.

### D+2-5. ⭐⭐⭐ 9번 유형 판정 — 양 진영이 독립적으로 같은 결론에 도달했다

D+1 §7의 「다음 경기 재검증 항목 3」(루크먼 `st_advanced` vs 알바레스 `st_false9` 중 무엇이 정착하는가)에
**D+2가 한 걸음 답을 줬다.** 두 진영이 서로 모르는 채 같은 말을 한다.

- **상대 CB 2인에 대한 상대 매체의 평가(El Diario Vasco)**: 「Se mostraron **cómodos** enfrentándose a
  atacantes móviles como Kang In Lee o Lookman **en vez de a un nueve de referencia**.」
  (그들은 **기준점 9번 대신** 이강인이나 루크먼 같은 **이동형 공격수**를 상대하는 것을 **편안해했다**.)
- **ATM 팬 채널(Atlético Stats)**: 「lo que te cambia a nivel estructural tener un nueve, porque los centrales
  de la Real… estuvieron muy cómodos todo el partido y **fue salir Jonathan David y empezaron a empeorar**
  porque lo que te fija y lo que te condiciona un nueve suele beneficiar a los jugadores de segunda línea」
  (**9번을 두는 것이 구조 차원에서 바꾸는 것** — 레알의 센터백들은… 경기 내내 아주 편안했고
  **조나단 데이비드가 나오자 나빠지기 시작했다**. 9번이 고정시키고 제약하는 것은 보통 **2선 선수들을 이롭게** 하기 때문이다.)

⇒ **판정: 이 경기의 9번 부재는 개인 부진이 아니라 구조 결손이다.** 상대가 「편했다」고 말하고 우리 쪽이
「9번이 들어가자 상대가 나빠졌다」고 말하며, 실측이 그것을 뒷받침한다 — 루크먼 76분 **슈팅 0** vs 데이비드 30분 **슈팅 2·xG 0.26·1골**.
⭐ **FC 함의**: 루크먼의 `st_advanced/Support` .603은 **역할 선택 오류의 기록**으로 읽는다. 시즌 정본은 아직 바꾸지 않되
(단일 경기), **다음 표본에서 「기준점형 9번(`st_target`/`st_poacher` 계열) + 2선 활성화」 가설을 우선 검증 항목으로 올린다.**

**루크먼 배치에 대한 Marca의 1차 판정**(D+1엔 원문이 없어 쓰지 못했다):
「Primero como hombre más adelantado y más tarde **en una banda en la que se sintió mucho más natural**,
no paró de intentarlo, pero con muy poco acierto, **siendo incapaz de superar alguna vez a Aramburu**.」
(처음에는 가장 전진한 선수로, 나중에는 **훨씬 더 자연스럽게 느낀 측면**에서 시도를 멈추지 않았지만
정확성이 거의 없었고, **아람부루를 한 번도 제치지 못했다**.) NOTA **5**.
⇒ ⭐ D+1 §5의 「9번이 아니라 **좌측 인사이드 포워드**로 재현해야 한다」가 **스페인 전국지 1차 원문으로 지지**된다.

⭐ **아람부루 맨마킹 — 두 진영 독립 수렴.** 상대팀 채널: 「estaba bien Aramburu… **secó a Lukman** con el que
estuvo **pegado todo el partido**」(아람부루는 좋았다… **루크먼을 말려버렸고** 경기 내내 **붙어 있었다**) /
Marca: 「siendo incapaz de superar alguna vez a Aramburu」 / 「**Arnau Ortiz** … logró ser una pesadilla para
Aramburu **como no había logrado Lookman**」(아르나우 오르티스는… **루크먼이 해내지 못한** 아람부루의 악몽이 되는 데 성공했다).
⇒ **루크먼의 좌측 무력화에는 상대 우측 풀백의 전담 마킹이라는 외부 원인이 있었다** — 「본인 성향」 단독 설명은 부족하다.

### D+2-6. ⭐⭐ 「푸빌 등 뒤」 계열 — 지지 1건, **방향 반대 서술 1건**

- **지지**: tacticalfootballanalysis(2026-09-15)가 「**Pubill:** tracked back to fill defensive spaces;
  **followed Sučić's dropping movements**」(푸빌: 수비 공간을 메우러 내려왔고, **수치치의 하강 움직임을 따라갔다**)로
  **추격 행동 자체는 3번째 독립 서술**이다.
- ⛔ **방향 반대**: Atlético Stats `RDHt-dGo644`는 구멍을 만든 사람을 **요렌테**로 지목한다 —
  「no solo Kang-in, varias veces ha tenido que salir **Llorente a los centrales**, dejando **un hueco enorme**」
  (이강인뿐 아니라 여러 번 **요렌테가 센터백들에게까지 나가야 했고**, **거대한 구멍**을 남겼다.) auto-caption.
  그리고 위험 경로를 **좌측**으로 특정한다: 「las cuatro veces que ha salido la Real Sociedad, el peligro
  **lo ha creado por ese lado**(=izquierda) porque no tenía a los jugadores bien posicionados」
  (레알 소시에다드가 나온 네 번, 위험은 **그 쪽(좌측)에서** 만들어졌다. 선수들이 제대로 배치돼 있지 않았기 때문이다.)
- ⚠️ **Gipuzkoa(D+1)는 요렌테를 「푸빌 등 뒤를 메우는 보정 장치」로, Atlético Stats는 「요렌테가 나가서 구멍을 만든다」로
  적는다 — 정반대다.** 두 서술은 **시간대가 다를 수 있다**(5-4-1 전환 **전** = 요렌테가 앞으로 나감 / 전환 **후** =
  요렌테를 그 측면에 내림). 현재 자료로는 분리되지 않는다. **미해결로 남기고 D+3·다음 경기 이벤트 타임라인 역산 과제로 넘긴다.**
- ⭐ **obs#775(「흔들리는 건 요렌테가 아니라 푸빌이다」)의 독립 지지 1건 추가** — Espíritu del Manzanares:
  「Llorente tiraba para arriba o se ponía más tirando para el medio, **Pubill se quedaba como lateral y
  jugábamos con una línea de cuatro**」(요렌테는 위로 나가거나 더 중앙 쪽으로 섰고, **푸빌은 풀백으로 남아
  우리는 백4로 뛰었다**.) auto-caption. ⇒ 백3가 국면에 따라 **실질 백4**가 된다는 **4번째 서술**이다.

⛔ **tacticalfootballanalysis는 보조 등급으로 강등한다.** 같은 글이 「Atlético employed **man-to-man marking
high up the pitch**」(아틀레티코는 **높은 위치에서 맨투맨 마킹**을 구사했다)라고 쓰는데, **우리 PPDA 15.14 ·
상대 PPDA 11.35 · 스페인어 1차 소스 3종의 「저블록」 서술과 정면 충돌**한다. 또 상대 xG를 **0.75**로 적어
FotMob 0.27과 어긋난다. **위치·압박 주장은 실측이 이긴다** — 이 글의 압박 서술은 **채택하지 않고**,
푸빌–수치치 추격 서술만 보조 근거로 쓴다.

### D+2-7. ⭐ 당일(D+1) 판정 정정 — 2건

불변규칙 2·G14에 따라 **당일 절을 수정하지 않는다.** 아래를 정정으로 적고 `observations`에 정정 행을 새로 만들었다.

**정정 ①: 상대 빅찬스 1개의 발생 경로 — 오픈플레이 rest-defense 누출이 아니라 「세트피스 클리어 실패, 좌측 박스」다.**
D+1 §2는 「rest-defense는 백3 + 율만 단독 피벗. 요렌테가 우측 높은 자리로 나가 있는 동안 중앙 커버가 율만 한 명으로
줄어드는 구간이 반복됐다(**상대 빅찬스 1개가 여기서 나왔다**)」로 적었다. **D+2에 소스 3종이 다른 경로를 말한다.**
- **Berria(에우스케라)**: 「Realaren aukerarik garbiena Sucicek izan zuen **korner batean**: Beitiak buruz jo
  ostean, baloia erdilari kroaziarrari iritsi zitzaion **area txikian**」 (레알의 가장 확실한 기회는 수치치가
  **코너에서** 가졌다: 베이티아가 헤딩한 뒤 볼이 **골 에어리어에서** 크로아티아 미드필더에게 갔다.)
- **Marca**: 그리말도 항목 「una **indecisión en el área** que permitió a Sucic gozar de la mejor ocasión de la
  Real」(**박스 안에서의 주저함**이 수치치에게 레알 최고의 기회를 허용했다) / 율만 항목 「estuvo blando en la acción
  en la que **junto a Grimaldo** dejó rematar a Sucic」(**그리말도와 함께** 수치치에게 슛을 허용한 장면에서 무르게 대응했다).
- **Atlético Stats**: 「aquella concesión entre Grimaldo y Julman, que no acaban despejando **balón parado**
  y acaban tirando」(그리말도와 율만 사이의 그 허용 — **세트피스**를 끝내 걷어내지 못하고 슛을 내줬다.) auto-caption.
⇒ **판정: 세트피스(코너/프리킥) 후 2차볼 클리어 실패, 지점은 좌측 박스(그리말도·율만).**
오픈플레이 우측 rest-defense 설명은 **3소스가 반박**한다. **정정 채택.**
⭐ FC 함의 변경: 이 실점 위기는 **rest-defense 구조**가 아니라 **세트피스 수비 2차볼 처리**의 문제다 —
D+1이 rest-defense 쪽에 달았던 취약점 무게를 **세트피스 쪽으로 옮긴다**. (§1 실측 「상대 코너 9개」와 정합한다.)

**정정 ②: 루크먼의 좌측 표류는 「본인 성향」이 아니라 상당 부분 「배치 + 상대 맨마킹」이다.**
D+1 §5는 「지시는 「고립된 9번」이었고 **좌측 표류는 본인 성향이다**」로 적었다. D+2에 세 갈래 반증이 나왔다.
(ⓐ) 두 영상이 **5-4-1 재배열 시 루크먼을 좌측으로 보낸 것을 배치 단계로 서술**한다(D+2-3의 4단계).
(ⓑ) Marca가 **측면을 「훨씬 더 자연스럽게 느낀」 자리**로 판정한다 — 표류가 아니라 적합이다.
(ⓒ) 상대팀 채널과 Marca가 **아람부루의 90분 전담 마킹**을 독립 서술한다.
⇒ **판정: 「본인 성향」 단독 귀속을 철회한다.** 좌측 이동은 **전환 배치의 일부**이고, 그 자리에서의 무력화는
**상대 전담 마킹**이 큰 몫이다. ⚠️ 단 **실측 툴x 24.8(좌측)·슈팅 0은 그대로**이며, 「9번으로 재현하면 안 된다」는
D+1 결론은 **유지·강화**된다(D+2-5).

### D+2-8. 율만 평가 정면 충돌 — 제3~제5 소스로 판정 종결

D+1 §8-4 ⑤는 El Desmarque **7** 「Fue el dueño y señor」(주인이자 지배자) vs Into the Calderón **5**
「failed to demonstrate any connection with players further forward」(전방 선수들과 어떤 연결도 보여주지 못했다)를
**어느 쪽도 단독 채택하지 않고** 남겨뒀다. D+2에 3소스가 추가됐다.

| 소스 | 평점 | 원문 · 번역 |
|---|---|---|
| **Marca** | **6** | 「firmó una actuación **solvente**, merodeando con el gol tras dos cabezazos en el área rival」(**견실한** 활약을 펼쳤고, 상대 박스에서 헤딩 두 번으로 골 근처까지 갔다) — 단 「estuvo **blando**」(무르게 대응했다)로 수치치 장면을 감점 |
| **Atlético Stats** | **6** | 「no fue su mejor partido, pero no quiere decir que fuera un mal partido… estuvo un poquito **errático**, a veces un poco **superado** por la Real Sociedad」(그의 최고 경기는 아니었지만 나쁜 경기였다는 뜻은 아니다… 조금 **불규칙**했고, 때로 레알 소시에다드에게 **밀렸다**) auto-caption |
| Atlético Stats 커뮤니티 투표 | **6.6**(441표) | — |

⇒ ⭐ **판정 종결: 「견실했으나 지배하지는 않았다」 — 6 대역.** El Desmarque의 「dueño y señor」는 **과대**,
Into the Calderón의 5 「연결 전무」는 **과소**다. 우리 커널 적합 `cm_b2b/Ball-Winning` **.792**(안필드 .529 → 크게 상승)와
이 대역이 정합한다 — **단독 피벗 배치가 역할과 맞는다**는 D+1 판정은 **유지**한다.

⭐ **Atlético Stats가 제시한 메커니즘 하나 추가**: 「la entrada tan jerarca del Cuti Romero… **le quita también
trabajo a Hjulmand**. ¿Por qué? porque defiende tanto hacia delante que hubo muchas acciones en centro del
campo que… en otros partidos sale ganador ahí el danés」(쿠티 로메로의 그 지배적인 등장이… **율만의 일까지
빼앗는다**. 왜냐하면 그가 워낙 앞으로 나가 수비해서 중원의 많은 장면이… 다른 경기였다면 그 덴마크인이 이겼을
장면이었기 때문이다.) auto-caption.
⇒ ⭐ **로메로(CCB, 클리어 11·툴x 59.1로 중앙에서 우측으로 Δ+8.1 전진)의 전진 수비가 율만의 수비 관여를 잠식한다** —
**백3 중앙 CB와 단독 피벗의 역할 간섭**이라는 구조적 관측. FC 함의: `cb_bpd/Aggressive`(로메로)와
`cm_b2b/Ball-Winning`(율만)을 **동시에 쓰면 중앙 수비 액션이 겹친다** — 다음 표본에서 율만의 태클·인터셉트 추이로 검증한다.

### D+2-9. 그 밖의 새 근거

- ⭐ **빌드업 붕괴의 인적 원인 지목 — 바리오스(Pablo Barrios) 결장.** 두 Atlético Stats 영상이 반복한다:
  「se notaba que **faltaba Pablo Barrios** para recibir ese primer balón y desatascar un poquito las jugadas
  porque **ni Baena, ni Marcos Llorente, ni el propio Kang-in Lee** te dan las soluciones que te da Pablo Barrios.
  ¿Cuál era la solución? Pues pegarle para arriba y que se sacen」(그 첫 볼을 받아 플레이를 풀어줄 **파블로 바리오스가
  없다는 게** 티가 났다. **바에나도, 마르코스 요렌테도, 이강인 본인도** 바리오스가 주는 해법을 주지 못하기 때문이다.
  해법이 뭐였나? 위로 뻥 차서 알아서 하게 두는 것.) auto-caption.
  ⇒ **실측 정합**: 롱볼 시도 **64회(13.9%)** · 상대 진영 패스 163 대 269 · 이강인 터치 34 · 바에나 터치 36.
  ⭐ **FC 함의**: 백3 빌드업의 실패는 구조가 아니라 **1차 탈압박 패서의 부재**로 설명될 수 있다 — 바리오스 복귀 경기에서
  같은 3-4-2-1이 나오면 **롱볼 비율·상대 진영 패스**를 비교해 분리한다. **다음 경기 재검증 항목에 추가.**
- ⭐ **롱볼 64회의 목적지가 특정됐다(상대 매체 증언).** El Diario Vasco: 「[Remiro] se le vio muy atento…
  para abandonar decidido el área en varias ocasiones y despejar **los envíos largos del cuadro colchonero
  a la espalda de los centrales blanquiazules**」(레미로는 아주 집중한 모습이었고… 여러 차례 결단력 있게 박스를
  떠나 **아틀레티코가 소시에다드 센터백들 등 뒤로 보낸 롱볼**을 걷어냈다.)
  ⇒ **ATM의 롱볼은 무작정 걷어내기가 아니라 「상대 CB 등 뒤」를 겨냥한 설계된 전달이었다.** 성공률 50%(32/64)의 의미가 바뀐다.
  ⭐ 그리고 상대 좌CB 사르의 취약이 그 표적과 맞물린다 — 상대팀 채널: 「Mamadou Sarr… **le buscaron la espalda**,
  se sentía incómodo en el posicionamiento… **no es un especialista para jugar en la izquierda**」
  (마마두 사르… **그의 등 뒤를 노렸고**, 위치 선정에서 불편해했다… **왼쪽에서 뛰는 스페셜리스트가 아니다**.)
  ⇒ 우리 우측 과밀(요렌테·이강인·줄리아노·푸빌)이 겨냥한 곳이 **상대의 가장 약한 CB 쪽**이었다.
  줄리아노 **xG 0.64**(팀 2위)가 이 경로의 산물로 읽힌다.
- ⭐ **59~60분 3중 교체의 재해석 — 「연결고리 제거」만이 아니라 「폭 → 중앙 재배치」다.**
  El Diario Vasco(상대 관점): 「**La acumulación de hombres por dentro en el Atlético** complicó aún más las
  cosas al cuadro txuri-urdin, sobre todo a Kubo」(**아틀레티코의 안쪽 인원 누적**이 소시에다드를, 특히 쿠보를
  더 어렵게 만들었다.) ⇒ **우리 실측과 정합**: 코케가 이강인 자리에 들어가며 툴x **78.6 → 59.7**(−18.9).
  D+1 §6의 「연결고리 3인 전원 제거 → equipo plano」 서술은 **유지하되**, 그 조치가 동시에 **우측 과밀을 해소하고
  중앙을 채운 재배치**였다는 축을 추가한다. ⭐ 이것이 「같은 조치, 반대 결과」(안필드 vs 아노에타)의 후보 설명이다.
- **그리말도의 후반 개선 — 경쟁 설명 2개.** D+1 §5는 「바레네체아 71분 교체 아웃 이후 전진이 열렸다」로 적었다.
  Atlético Stats는 다른 원인을 든다: 「a Grimaldo le has puesto un tío que te da **la amplitud**, que te
  ensancha el campo y… desde que ha salido Arnau, le hemos empezado a ver **media punteando**… porque tiene
  un tío que ocupa los espacios que Grimaldo no sabe ocupar」(그리말도에게 **폭을 만들어주는** 선수, 경기장을
  넓혀주는 선수를 붙여줬고… **아르나우가 들어온 뒤부터** 그가 **미디어푼타처럼 뛰는 것**을 보기 시작했다…
  그리말도가 점유할 줄 모르는 공간을 점유하는 선수가 있기 때문이다.) auto-caption.
  ⚠️ **두 사건이 71분·76분으로 붙어 있어 분리되지 않는다.** 실측(득점·도움 전부 84분 이후)은 **둘 다와 정합**한다.
  ⭐ **FC 함의는 오히려 선명해진다**: 그리말도의 전진은 **무조건이 아니라 조건부**이며, 조건은
  「같은 쪽 상대 윙어의 부재」**또는**「같은 쪽 폭 제공자의 존재」다 — D+1 결론을 **약화가 아니라 일반화**한다.
- **Marca의 시즌 축 관측(D+2)**: 「su producción va **por arreones**」(그들의 생산은 **발작적으로** 간다) —
  3승이 전부 짧은 구간에 몰렸다(레알전 84′~, 세비야전 30분, 말라가전 15분). 이 경기의 「93분간 0-0 → 마지막 6분 3골」이
  **고립된 사건이 아니라 시즌 패턴의 네 번째 사례**다. ⚠️ 시즌 축이라 이 회차 범위를 넘지만, **이 경기 해석에 한해** 기록한다.
- **상대 감독 평가(상대팀 관점)**: El Rincón de la Real은 마타라초에게 **4점**을 주며 교체 타이밍을 지적한다 —
  「**el cambio táctico del Cholo es bastante más temprano que el ajuste** que hizo él… le pilló un poquito
  el toro porque **le ganó ahí en la batalla** a Simeone」(**촐로의 전술 변경이 그가 한 조정보다 상당히 이르다**…
  그가 조금 늦었다. **시메오네가 그 싸움에서 이겼기** 때문이다.) auto-caption.
  ⇒ ⭐ **상대팀 관점이 「시메오네가 먼저 조정했다」를 독립 확인** — D+2-3의 「≈15분 / 35~42분 전환」 서술과 정합한다.
- **에우스케라 소스의 저블록 3차 증언**: 「eroso zegoen Reala, **espainiarrak atzean baitzeuden** eta ez
  baitzuten ia arriskurik sortu」(레알은 편안했는데, **스페인 팀(아틀레티코)이 뒤에 있었고** 거의 위험을 만들지
  않았기 때문이다.)
- **덴마크어 축**: bold.dk는 전술 서술 없이 사실 보도만 — 「Morten Hjulmand havde et **godt forsøg efter 25
  minutter**, men bolden strøg forbi mål」(모르텐 율만은 **25분에 좋은 시도**를 했지만 볼은 골문을 스쳐 지나갔다) ·
  「Morten Hjulmand **spillede fuld tid**」(율만은 **풀타임을 뛰었다**). **전술 근거로는 쓰지 않는다.**

### D+2-10. 언어축별 시도 기록 (「0건」도 결과다)

| 언어축 | 결과 | 이번 회차에 실제로 쓴 검색어·경로 |
|---|---|---|
| 스페인어 | ✅ **Marca 원문 해소** · Diario Vasco D+2 확보 | marca.com `/futbol/atletico.html` 섹션 직접 크롤 · diariovasco.com `/real-sociedad/` 직접 크롤 |
| 스페인어(AS) | ⛔ **여전히 0건** | `as.com/futbol/primera/atletico_de_madrid/`(404) · `as.com/futbol/equipos/atletico-de-madrid/`(404) · `as.com/buscador/?q=…`(JS 미렌더) · `as.com/futbol/` 링크 스캔(atlético 링크 1개, 시즌 프리뷰뿐). **쿠키 배너는 「Rechazar」로 거절 처리**(비필수 거부 원칙). → **D+3 과제: `as.com/futbol/primera/` 또는 라리가 경기 페이지 경유** |
| 바스크(ES) | ✅ **해소** | diariovasco.com 직접 방문 — D+1의 「0건」은 **검색엔진 미노출 탓**이었다(브라우저 경로 규칙의 4번째 실증) |
| **순수 에우스케라** 🏴 | ✅ **0건 → 1건** | berria.eus `/bilaketa?bilatu=Reala+Atletico`(404) → **`berria.eus/kirola` 섹션 직접 크롤로 회수**. EITB는 미시도(시간 배분) → D+3 |
| **독일어** 🇩🇪 | ⛔ **0건** | 「Matarazzo Real Sociedad Atlético 0:3 Trainer Kicker」 · 「Matarazzo Real Sociedad Trainer Bericht September 2026 Sport1 Spox」 · kicker.de `/suche?q=Matarazzo`(빈 렌더). **이 경기를 다룬 독일어 1차 매체 없음** — 노출된 Sky Sport DE 자료는 **2026-04 코파 결승** 건이다. ⇒ 마타라초의 독일 시절 연고는 **현 전술 보도로 이어지지 않는다**. **D+3 이후 이 축은 우선순위 하향 권고.** |
| **슬로바키아어** 🇸🇰 | ⛔ **0건** | 「Hancko Atlético Madrid Real Sociedad zápas hodnotenie」 → dennikn.sk 개별 URL **HTTP 403**. sportnet.sme.sk는 **25/26 시즌 27라운드** 기사(다른 경기) → 기각. **D+3: sme.sk 브라우저 직접 방문** |
| **포르투갈어** 🇵🇹🇧🇷 | ⛔ **0건** | 「Johnny Cardoso Atlético Real Sociedad português análise setembro 2026」 → 프로필·이적 자료만. **이 경기 다룬 포르투갈어 기사 없음**(카르도소 31분 출전). **D+3 이후 우선순위 하향 권고.** |
| 이탈리아어 🇮🇹 | ⛔ **0건 — 기각 확정** | 「Lookman Atletico Real Sociedad pagelle Gazzetta 14 settembre 2026」 → virgilio 기사가 **다시 이 경기 맥락으로 노출**됐으나 브라우저 실물 확인 결과 **게시일 `07/03/26 22:10`**, 25/26 메트로폴리타노 **3-2** 경기(소를로트 선발·그리즈만 교체 투입·알바레스 멀티골)였다. ⭐ **「검색 스니펫은 근거 불가」 규칙의 실증 사례 — 같은 오탐이 두 회차 연속 노출됐다.** |
| 프랑스어 🇫🇷 | ⛔ **0건** | 「Jonathan David premier but Atlético Real Sociedad L'Équipe」 → **L'Équipe 여전히 미노출**. calciomio.fr 1건 노출됐으나 **HTTP 403**으로 실물 확인 불가 → **채택하지 않음** |
| 덴마크어 🇩🇰 | ✅ **0건 → 1건** | 「Morten Frendrup Julmand Atlético Real Sociedad dansk Bold.dk」 → ⚠️ **선수명 오기 교정**: 이 선수는 **Morten Hjulmand**다(Frendrup은 제노아의 다른 덴마크 선수). bold.dk 확보 — **전술 서술 없음** |
| 한국어 🇰🇷 | 미수행(D+1 1건 보유) | — |
| 일본어 🇯🇵 | 미수행(D+1 1건 보유·쿠보 축) | — |
| 유튜브 사이트 내부검색 | ✅ **2축 스윕 · 신규 2채널** | `search_query=Real+Sociedad+Atletico+analisis+tactico&sp=EgIIAw%3D%3D` (20건 회수) · `search_query=Real+Sociedad+analisis+Matarazzo+Atletico+Anoeta&sp=EgIIAw%3D%3D` (**상대팀 채널 1건 — 이 검색어가 결정적이었다**) |

⭐ **다음 회차를 위한 검색어 권고**: 상대팀 관점은 **상대 감독 이름 + 상대 팀명 + 구장명** 조합이 팬 분석 채널을 끌어낸다
(`analisis <상대감독> <상대팀> <구장>`). 우리 팀 이름만 넣은 스윕에서는 이 채널이 **한 건도 나오지 않았다.**

### D+2-11. 이 회차의 DB 반영

- `observations` **신규 9행**(regime_id=4, season='2026-27') — 판정 6 · 정정 2 · 충돌 1.
- `player_duties` **6행**에 `[2026-09-15 D+2 …]` 덧붙임 — 루크먼·그리말도·율만·요렌테·푸빌·로메로.
- `match_reports.id=42`의 `tactical_description`·`tactical_changes`·`game_implications`에 `[2026-09-15 D+2 …]` 덧붙임.
- `match_videos` **4행 신규**(report_id=42) — 전사 경로 포함.
- `manager_profiles`: **갱신함**(`formation` 축 — 5단 변형과 전환 시각 수렴). 사유는 D+2-3.
- ⛔ **`prescriptions`·`team_tactic_setups`·`slot_canon_roles`·`match_game_setups`·`match_player_prescriptions`는 변경하지 않았다** —
  D+2가 더한 것은 **서사 근거**이고 커널 값을 움직일 새 실측은 없다. 게임 구현 판정은 **「추가 관찰」 유지**.

### D+2-12. 다음 회차(D+3, 2026-09-16) 과제

1. **Atlético Stats `zFvDU2SSXMo`**(2026-09-15 23:00 예정) 공개 확인 + 전사 — 「EL MOMENTO JONATHAN DAVID」.
2. 같은 채널 예고 **루크먼 전용 분석 영상**을 찾는다(「mañana tenemos vídeo de Lookman」).
3. **AS 원문** — `as.com/futbol/primera/` 또는 라리가 경기 페이지 경유로 재시도(경로 4종 실패 기록은 D+2-10).
4. **EITB**(에우스케라/ES) 브라우저 직접 방문 — 이번 회차 미시도.
5. **슬로바키아어** sme.sk 브라우저 직접(403 우회).
6. **요렌테 방향 충돌 해소**(D+2-6) — 「구멍을 메웠나 / 만들었나」를 **WhoScored 이벤트 타임라인의 요렌테 평균 위치
   시점별 역산**으로 분리한다(§9의 미해결 검증법과 같은 도구).
