# 2026-09-06 CHE vs Arsenal — 1-2 (패)

> 수집일 2026-09-07 · SofaScore event `16363257` · 프리미어리그 3라운드 · **원정** · 3-4-2-1
> FotMob matchId `5795435` · WhoScored matchId `1983568` · matches id 98

---

## 1. 경기 개요와 원천 수치

**아스날 2-1 첼시** (HT 1-1). 첼시가 2분 만에 앞서고 88분을 쫓아간 경기다.

| 항목 | 첼시(v) | 아스날(o) |
|---|---|---|
| 점유율 | **45%** | 55% |
| xG (FotMob) | **0.39** | 2.05 |
| xG 오픈플레이 | 0.32 | 1.44 |
| xG 세트피스 | 0.07 | 0.61 |
| xGOT | 0.35 | 2.00 |
| 슈팅 / 유효 | 13 / 5 | 16 / 9 |
| 블록당함 | 2 | 6 |
| 박스 안 슈팅 | 5 | 13 |
| 빅찬스 (SofaScore) | 1 | 4 |
| 패스 (성공률) | 384 (82%) | 461 (85%) |
| 롱볼 | 18/49 (37%) | 18/45 (40%) |
| 크로스 | **1/14 (7%)** | 4/16 (25%) |
| 상대 박스 터치 | 26 | 44 |
| 파이널서드 진입 | 47 | 61 |
| 코너 | 3 | 5 |
| 공중전 | 16/29 (55%) | 13/29 (45%) |
| 태클 / 인터셉트 / 클리어 | 12 / 7 / 23 | 10 / 9 / 24 |
| 세이브 | **8** | 4 |
| 경고 | 4 | 2 |
| **PPDA** | **9.58** | 7.58 |

- **xG 원천은 FotMob 단일 스냅샷**(`xg_source='FotMob'`, §3 규칙). 이번 경기는 드물게 **SofaScore와 FotMob 전체 xG가 2.05/0.39로 완전히 일치**했다. 정합 검산도 통과: `0.39 − 0.32 = 0.07` = FotMob xG set play 0.07 ✅ / 상대 `2.05 − 1.44 = 0.61` = set play 0.61 ✅. PK 0개.
- **득점·국면**
  - 2' 모건 로저스 (어시스트 요럴 하토) → 첼시 **lead**
  - 25' 카이 하베르츠 (어시스트 데클란 라이스) → **level**
  - 50' 마르틴 외데고르 (어시스트 흐리스토스 촐리스) → 첼시 **trail**
  - 선발 기준 국면 분: `lead 23분 · level 27분 · trail 40분`. 즉 **경기의 44%를 지고 있었고, 앞선 시간은 23분뿐이다.**
- **교체**: 60' 구스토↔라비아 · 60' 차바리아↔하토 · 81' 에스테방↔페드루 네투 · 87' 웰벡↔로저스.
- **경고 4장**: 14' 조앙 페드루 · 45' 콜 파머 · 58' 라크루아 · 83' 모건 로저스. 주심 Chris Kavanagh.
- **수집 엔드포인트**: SofaScore `/api/v1/event/16363257/{lineups, average-positions, incidents, statistics}` + 선수별 `/heatmap`. FotMob `/api/data/matchDetails?matchId=5795435`. WhoScored `matchCentreData` matchId=1983568(이벤트 1425건, PPDA 산출).
- **결손·한계**: 출전 15명 전원 수집(결손 0). 히트맵 유효 기준(hit_points≥15) 미달은 **웰벡(hp=2, 8분) · 에스테방(hp=8, 9분)** 2명 — 이 둘은 대표 그리드·시즌 집계에서 제외되고 리포트 근거로만 쓴다. 아체암퐁은 hp=28로 기준은 넘겼으나 90분 출전치고 극단적으로 적다(터치 21회).

---

## 2. 전술 설명

### 점유 구조·빌드업

기본형은 **3-4-2-1**이고, 실측 평균 위치(툴 좌표 = 100 − 소파y, 좌 0 ↔ 우 100)는 이렇다.

| 슬롯 | 선수 | 툴x | 소파 avg_x(전진도) |
|---|---|---|---|
| GK | E. 마르티네스 | 50.4 | 10.5 |
| LCB | 포파나 | 37.3 | 38.4 |
| CCB | 라크루아 | 62.0 | 38.3 |
| RCB | 아체암퐁 | 76.0 | **50.0** |
| LWB | 하토 | 20.5 | 39.0 |
| LCM | 리스 제임스 | 44.2 | 48.9 |
| RCM | 라비아 | 49.2 | 40.4 |
| RWB | 페드루 네투 | 83.7 | **62.2** |
| LAM | 로저스 | 27.3 | 58.8 |
| ST | 조앙 페드루 | 45.0 | 62.1 |
| RAM | 파머 | 53.9 | 62.7 |

세 가지가 눈에 띈다.

1. **좌우 윙백의 전진도가 완전히 비대칭이다.** 우측 네투 62.2 vs 좌측 하토 39.0 — **23의 격차**다. 좌측은 로저스(58.8/툴x 27.3)가 이미 높고 넓게 서서 폭을 담당했고, 하토는 그 뒤를 받치는 실질 백4의 좌측이었다. 우측은 네투 혼자 폭과 높이를 다 맡았다.
2. **아체암퐁이 백3의 우측인데 avg_x 50.0으로 라크루아·포파나(38)보다 12 높다.** 백3가 평평하지 않고 우측이 밀려 올라간 형태였다. 그런데 터치 21회·패스 13회로 **볼에는 거의 관여하지 않았다** — 위치는 전진했으나 빌드업 경로가 아니었다는 뜻이다.
3. **파머와 조앙 페드루가 사실상 같은 높이의 2인 전방**이었다(avg_x 62.7 / 62.1, 툴x 53.9 / 45.0). 3-4-2-1의 「2」와 「1」이 수직으로 분리되지 않았다. 파머는 RAM 앵커(툴x 68)보다 14 안쪽으로 들어와 중앙에서 뛰었다.

빌드업 통계는 **저볼륨·저정확도**다. 패스 384회(82%)로 아스날 461회(85%)에 밀렸고, 롱볼 성공률 37%, **크로스는 14회 중 1회 성공(7%)** 이다. 파이널서드 패스도 91/130(70%)로 아스날 166/205(81%)에 크게 뒤졌다. 마르티네스가 패스 37회 중 19회만 성공(51%)한 것도 롱볼 의존을 보여준다.

### 비점유 구조·압박

**PPDA 9.58** — 직전 브라이턴전 22.67에서 **2.4배 공격적으로** 바뀌었다(obs#469). 전·후반 분해하면 첼시는 9.46 → 9.69로 거의 일정했고, **변한 쪽은 아스날**이다(6.19 → 8.88). 즉 첼시는 90분 내내 같은 강도로 압박했고, 아스날이 2-1로 앞선 뒤 압박을 풀었다.

수비 액션은 태클 12 · 인터셉트 7 · 클리어 23으로 아스날(10/9/24)과 대등하다. 그런데 **박스 안 슈팅을 5:13으로 내줬고 상대 박스 터치가 26:44**다 — 라인 앞에서는 버텼으나 박스 진입 자체를 막지 못했다.

공중전은 첼시가 16/29(55%)로 이겼다. 포파나 혼자 클리어 10회·경합 13회(6승 7패)로 수비 부하의 대부분을 감당했다.

### 전환·rest-defense·세트피스

- **선제골이 전환에서 나왔다**: 2분, 하토의 헤더 경합 승리 → 낙하볼을 로저스가 마무리. 첼시가 이 경기에서 만든 유일한 빅찬스이자 유일한 득점이다.
- **rest-defense가 우측에서 무너졌다**: 네투가 툴x 83.7·avg_x 62.2로 나가 있는 동안 그 뒤를 아체암퐁(avg_x 50.0)이 덮어야 했는데, 아체암퐁의 히트맵 포인트는 28개뿐이고 평점 5.7로 팀 최저다. 아스날의 한쪽 오버로드가 이 지점을 겨냥했다 — 알론소 본인이 회견에서 인정했다(§8).
- **세트피스는 xG 0.07 대 0.61로 완패**다. 코너 3:5. 공격 세트피스에서 사실상 아무것도 만들지 못했다(맥피 코치 영입 축, obs#37과 대조 필요).

---

## 3. 전술적 특성

**반복된 강점**

- **초반 득점 패턴이 3경기 연속이다.** 첼시는 시즌 첫 3경기 모두 전반 5분 이내에 득점했다(로저스 2분 골 포함) — PL 최초 기록.
- **공중전·박스 안 버티기**: 공중전 55%, 클리어 23회. 포파나가 축이다(평점 7.2, 팀 필드플레이어 최고 중 하나).
- **하토의 온더볼 기여**: 60분 출전으로 어시스트 1·키패스 1·태클 2·경합 4승, 평점 7.1. 실측 툴x 20.5로 명백한 좌 윙백이다.

**반복된 취약점**

- ⭐ **리드한 직후 통제력을 잃는다 — 브라이턴전과 같은 구조다.** 2분에 앞선 뒤 23분간 xG를 거의 만들지 못하고 25분에 동점을 내줬다. 알론소 본인 진단과 정확히 일치한다(§8).
- **크로스가 작동하지 않는다**: 14회 중 1회. 네투가 우측에서 혼자 폭을 담당했지만 박스 안에 받을 사람이 없었다 — 파머와 조앙 페드루가 같은 높이로 붙어 있었기 때문이다.
- **총 xG 0.39.** 90분 동안 만든 기대득점이 0.39이고 그 중 0.11이 파머의 슛 3개다. 득점은 xG 0.0755짜리 마무리였다.
- **골키퍼가 팀을 지탱했다**: 마르티네스 8세이브·평점 8.4. 필드 10명 중 7.2를 넘긴 선수가 없다.

**감독 프로필·직전 경기와의 관계**

- **유지**: 백3(3라운드 연속) · 윙백 폭 의존 · 「시스템은 사진 한 장일 뿐」이라는 가변 선언과 정합하는 슬롯 내 역할 이동.
- **변화**: 압박 강도(PPDA 22.67 → 9.58) · 점유율(26% → 45%). 두 값이 라운드마다 크게 흔들린다.
- **결원의 결과**: 리스 제임스의 피벗 기용은 전술 설계가 아니라 **엔소 페르난데스 이적(맨시티, 2026-09-01 CONFIRMED, `transfer_outgoing` id=25) + 카이세도 결장**의 산물이다.

---

## 4. 경기 중 변화

1. **0-0 (0~2분)**: 첼시가 곧바로 전환에서 앞섰다. 하토의 경합 → 로저스 마무리.
2. **리드 (2~25분)**: 첼시가 물러섰다. 이 23분 동안 아스날이 박스를 잠식했고 25분 하베르츠가 라이스의 패스를 받아 라크루아 앞에서 동점을 만들었다. 알론소: 「득점 후 15~20분 동안 우리는 너무 많이 수비해야 했다」.
3. **후반 개시 5분 만에 열세 (50분)**: 촐리스 → 외데고르. 첼시 좌측(하토·로저스 뒤)이 다시 열렸다.
4. **60분 이중 교체**: **구스토↔라비아 · 차바리아↔하토**. 라비아는 60분까지 경합 5승 0패에 평점 6.8로 잘하고 있었고, 이 교체는 현지 매체에서도 의문시됐다. 구스토는 툴x 53.0(중앙)으로 들어왔고 `pos_class`는 RCB로 찍혔지만 **커널은 미드필드를 지지한다**(RCM 0.5661 > CCB 0.3802 > RCB 0.3221) — 백3 재편이 아니라 **라비아 자리의 피벗 교체**다. 차바리아는 하토보다 10 높게(avg_x 49.8) 서서 추격 국면을 반영했다.
5. **81·87분**: 에스테방(→네투), 웰벡(→로저스). 에스테방은 9분 만에 슈팅 1개·유효 1개(xG 0.041)로 라야의 선방에 막혔다 — 이 경기 후반 첼시의 가장 위협적인 장면.
6. **마지막 국면**: trail 40분 동안 첼시가 만든 총 xG는 0.39의 일부에 불과하다. 크로스 14회 중 13회 실패가 이 구간에 집중됐다.

---

## 5. 선수별 분석 — 출전 선수 전원 (15명)

좌표는 소파 `avg_x`(전진도) / `avg_y`, 툴x는 100−avg_y(좌 0 ↔ 우 100). 단일 경기 fit은 3-4-2-1 슬롯 기하 기준.

| 선수 | 위치·실제 역할 | 분/평점·핵심 스탯 | 평균 위치·히트맵 | 특성·수행 | FC 역할/포커스 함의 |
|---|---|---|---|---|---|
| **E. 마르티네스** | GK — 실질 MOM | 90' **8.4** / 세이브 **8**, 패스 37(성공 19·51%), 리커버리 8 | x=10.5 y=49.6 (툴x 50.4) hp=58 | 8세이브로 2실점에 막았다. 다만 배급 정확도 51%로 롱볼 의존 | `gk_goalkeeper/Defend` fit **0.9388** — 이견 없음 |
| **웨슬리 포파나** | LCB — 백3 좌, 수비 부하 집중 | 90' **7.2** / 클리어 **10**, 경합 6승7패, 태클 3, 인터셉트 2, 키패스 2, 패스 48(92%) | x=38.4 y=62.7 (툴x 37.3) hp=**87**(팀 최다) | 활동량·커버 범위 모두 팀 최고. 백3에서 유일하게 안정적 | `cb_bpd/Aggressive` fit **0.8413** |
| **막상스 라크루아** | CCB — 백3 중앙 | 90' 6.6 / 패스 48(90%), 클리어 6, 경합 5승3패, 태클 2, **경고 58'** | x=38.3 y=38.0 (툴x 62.0) hp=71 | 배급은 깔끔했으나 25분 하베르츠 동점골 장면에서 직접 지목됐다(프랑스어 매체) | `cb_bpd/Aggressive` fit 0.7065 — 2위(cb_stopper 0.539)와 격차 큼 |
| **조시 아체암퐁** | RCB — 백3 우, 밀려 올라감 | 90' **5.7(팀 최저)** / 터치 **21**, 패스 13, 경합 0승2패, 클리어 1 | x=**50.0** y=24.0 (툴x 76.0) hp=**28** | ⚠️ 90분 출전에 터치 21회. 위치는 높았으나 볼 관여·수비 기여 모두 결손. 네투가 비운 우측 뒤를 덮지 못했다 | `cb_bpd/Aggressive` fit **0.4556** — 팀 최저. 이 슬롯 배치 자체가 실측과 안 맞는다 |
| **요럴 하토** | LWB — 좌 윙백(pos_class는 LDM) | 60' **7.1** / **어시스트 1**, 키패스 1, 태클 2, 경합 4승3패, 클리어 2 | x=39.0 y=79.5 (툴x **20.5**) hp=37 | 2분 결승 어시스트(헤더 경합 승리). 60분 교체는 부상 아닌 구조 조정으로 보인다 | 슬롯 LM 기준 `wm_widemid/Defend` 0.6593이지만 ⭐ **커널 그룹을 FB로 바꾸면 `fb_att_wb/Support` 0.7717** — obs#467 |
| **리스 제임스** | LCM — 임시 피벗 | 90' 7.1 / 패스 46(93%), 슈팅 3(유효 1), 리커버리 6, 경합 3승3패, 태클 0 | x=48.9 y=55.8 (툴x 44.2) hp=75 | 원 포지션이 아니다(엔소 이적+카이세도 결장). 배급은 안정적이었으나 수비 액션 0/0 | `cm_playmaker/Roaming` 0.7612 — 2위 `cm_holding/Defend` 0.753과 **Δ0.008(노이즈)**. 판정 보류 |
| **로메오 라비아** | RCM — 피벗 | 60' 6.8 / 경합 **5승 0패**, 패스 27(89%), 태클 1, 인터셉트 1 | x=40.4 y=50.8 (툴x 49.2) hp=46 | 60분까지 경합 무패. 외데고르 결승골 장면에서 촐리스를 커버하러 중앙을 비웠다는 지적 있음 | `cm_b2b/Ball-Winning` fit **0.8709** — 이 경기 필드 최고 적합 |
| **페드루 네투** | RWB — 우 윙백(pos_class는 RDM) | 81' 6.3 / 키패스 2, 인터셉트 2, 경합 3승5패, 터치 39, 슈팅 1 | x=**62.2** y=16.3 (툴x **83.7**) hp=49 | 우측 폭을 혼자 담당. 전반 추가시간 포스트 강타. 크로스 성공률 붕괴의 당사자 | 슬롯 RM 기준 `wm_winger/Attack` 0.8032 · ⭐ FB 그룹이면 `fb_att_wb/Support` **0.8144** — obs#467 |
| **모건 로저스** | LAM — 좌 전방, 폭 담당 | 87' **7.2** / **골 1**, 슈팅 3(유효 1), xG 0.076, 키패스 1, 리커버리 5, 경합 2승7패, **경고 83'** | x=58.8 y=72.7 (툴x 27.3) hp=51 | 2분 결승... 이 아니라 선제골. 이후 경합 2승7패로 고전 | `cam_playmaker/Roaming` 0.8194 ⚠️ `cam_classic10/Wide`와 **동률 0.8194**. 시즌 집계(LM, n=3)는 `wm_wideplm/Attack` 0.8468 |
| **조앙 페드루** | ST — 파머와 나란한 전방 | 90' 6.5 / 경합 **10승 7패(팀 최다)**, 키패스 2, 슈팅 1, xG 0.018, 패스 19(68%), **경고 14'** | x=62.1 y=55.0 (툴x 45.0) hp=49 | 밀착 마크에도 경합 10승. 결정적 기회 2회 실축(칩샷 포함) | 단일 경기 `st_false9/Build-Up` 0.6849 · ⭐ **시즌 4경기 집계는 `st_advanced/Support` 0.7693으로 뒤집혔다** — obs#468 |
| **콜 파머** | RAM — 중앙으로 좁혀 뜀 | 90' 6.5 / 슈팅 3(유효 **2**), xG **0.112(팀 최다)**, 키패스 1, 패스 47(83%), 경합 1승4패, **경고 45'** | x=62.7 y=46.1 (툴x **53.9**) hp=61 | RAM 앵커(툴x 68)보다 14 안쪽. 조앙 페드루와 겹쳤다 | `cam_playmaker/Roaming` 0.8366 ⚠️ 시즌 표본이 ST n=2 / RM n=2로 갈려 대표 위치 미확정(fit 0.5576) |
| **말로 구스토** | 교체 60' (→라비아) · RCM | 30' 6.9 / 태클 2, 경합 3승 0패, 패스 18(89%), 슈팅 1 | x=56.4 y=47.0 (툴x 53.0) hp=32 | 라비아 자리의 피벗 교체 — 커널도 RCM(0.566) > CCB(0.380) > RCB(0.322)로 미드필드를 지지한다 | 단일 경기 표본. 시즌 처방 미변경 |
| **펩 차바리아** | 교체 60' (→하토) · 좌 윙백 | 30' 6.6 / 태클 1, 인터셉트 1, 패스 10(70%), 경합 1승1패 | x=49.8 y=81.6 (툴x 18.4) hp=21 | 하토보다 10 높게(avg_x 49.8) 섰다 — 추격 국면 반영 | 단일 경기 표본 |
| **에스테방** | 교체 81' (→네투) · 우 전방 | 9' 6.5 / 슈팅 1(유효 1), xG 0.041, 터치 6 | x=59.0 y=29.4 (툴x 70.6) hp=**8** | 9분 만에 개인 돌파 후 유효슛 — 라야 선방. 후반 최대 위협 | ⚠️ hp<15로 그리드 무효. 집계 제외 |
| **대니 웰벡** | 교체 87' (→로저스) | 8' 6.4 / 터치 **2**, 패스 1 | x=78.6 y=44.8 (툴x 55.3) hp=**2** | 사실상 표본 없음 | ⚠️ hp<15로 그리드 무효. 집계 제외 |

---

## 6. 전술 변화 판정

**유지된 것**
- 백3(3-4-2-1) — PL 1·2·3라운드 연속. **이번 포메이션은 「전환」이 아니라 연속이다**(obs#470). 스페인어 매체도 「알론소가 시즌 내내 써온 3-4-2-1」로 서술한다.
- 윙백 폭 의존, 전방 2인의 자유 이동, 초반 득점.

**새로 나타난 것**
- ⭐ **좌우 윙백 전진도 비대칭**(네투 62.2 vs 하토 39.0, Δ23). 1경기 근거다 — 재검증 대상.
- ⭐ **백3 우측(아체암퐁)이 12 밀려 올라간 비평면 백3**. 볼 관여는 최소(터치 21).
- **파머·조앙 페드루가 수직 분리 없이 같은 높이**. 3-4-2-1의 「2-1」이 사실상 「front 2 + wide 1」로 작동했다.

**직전 경기(브라이턴 4-3 W) 대비 변화**
| 지표 | 브라이턴(08-30, H) | 아스날(09-06, A) |
|---|---|---|
| 점유율 | 26% | **45%** |
| PPDA | 22.67 | **9.58** |
| xG | 2.93 | **0.39** |
| 패스 | 227 | 384 |
- 압박·점유가 라운드 사이에서 2배 이상 흔들린다 → **시즌 정본에 단일 라인높이·압박강도를 박으면 안 된다**(obs#469).

**`manager_profiles`·`observations` 반영**
- 신규 obs **#467**(pos_class가 3-4-2-1 윙백을 오분류) · **#468**(주앙 페드루 st_false9 → st_advanced 역전) · **#469**(압박 강도 2.4배 요동) · **#470**(3-4-2-1은 연속·윙백 비대칭) · **#471**(event_id 이중 규약 — 데이터 위생).
- `manager_profiles`는 이번 회차에 수정하지 않았다 — 3경기 표본이고 변동 폭이 커서 축 갱신 근거가 서지 않는다.

---

## 7. 게임 구현 판정

### 결론: **추가 관찰**

단일 경기이고, 커널 Δ가 역할 경계를 가로지른 건 주앙 페드루 1건뿐이며 그마저 n=4다. **시즌 정본(`team_tactic_setups`·`fc26:opt:*`·`slot_canon_roles`)은 변경하지 않았다.**

### 이 경기 전용 팀 설정 (`match_game_setups`, MATCH ONLY)

| 항목 | 값 |
|---|---|
| game_version | FC26 |
| formation | 3-4-2-1 |
| build_up_style | Counter |
| defensive_approach | Balanced |
| line_height | 55 |

근거: 점유 45%인데 xG 0.39·크로스 1/14로 지공은 작동하지 않았고, 유일한 득점과 유일한 빅찬스가 2분 전환에서 나왔다 → **Counter**. PPDA 9.58은 직전 경기(22.67)보다 훨씬 공격적이지만 아스날(7.58)보다는 무르고, 박스 안 슈팅을 5:13으로 내줬다 → 라인 높이 **55**(중간보다 약간 높게), 접근은 **Balanced**.

### 이 경기 선발 11명 (`match_player_prescriptions`, MATCH ONLY)

| 슬롯 | 선수 | 역할 | 포커스 | 단일경기 fit | 비고 |
|---|---|---|---|---|---|
| GK | E. 마르티네스 | gk_goalkeeper | Defend | 0.9388 | |
| LCB | 포파나 | cb_bpd | Aggressive | 0.8413 | |
| CCB | 라크루아 | cb_bpd | Aggressive | 0.7065 | |
| RCB | 아체암퐁 | cb_bpd | Aggressive | **0.4556** | ⚠️ 최저 적합 — 실측이 슬롯과 안 맞는다 |
| LM(LWB) | 하토 | wm_widemid | Defend | 0.6593 | ⚠️ FB 그룹이면 fb_att_wb/Support 0.7717 |
| LCM | 리스 제임스 | cm_playmaker | Roaming | 0.7612 | ⚠️ 2위와 Δ0.008 (노이즈) |
| RCM | 라비아 | cm_b2b | Ball-Winning | **0.8709** | 필드 최고 |
| RM(RWB) | 페드루 네투 | wm_winger | Attack | 0.8032 | ⚠️ FB 그룹이면 fb_att_wb/Support 0.8144 |
| LAM | 로저스 | cam_playmaker | Roaming | 0.8194 | ⚠️ cam_classic10/Wide와 동률 |
| ST | 조앙 페드루 | st_false9 | Build-Up | 0.6849 | 시즌 4경기는 st_advanced/Support |
| RAM | 파머 | cam_playmaker | Roaming | 0.8366 | |

### 교체 4명 (`match_player_prescriptions`, starter=0)

| 투입 | 선수 | 슬롯 | 역할 | 포커스 | fit | 비고 |
|---|---|---|---|---|---|---|
| 60' (→라비아) | 구스토 | RCM | cm_playmaker | Roaming | 0.5661 | ⭐ pos_class는 RCB지만 커널은 CM 지지(RCM 0.566 > CCB 0.380 > RCB 0.322) — 피벗 교체다 |
| 60' (→하토) | 차바리아 | LM | wm_widemid | **Support** | 0.6796 | 하토(Defend)와 같은 슬롯인데 포커스가 갈린다 — avg_x 10 높음 |
| 81' (→네투) | 에스테방 | RM | wm_winger | Attack | **NULL** | ⚠️ hp=8로 그리드 무효 — fit 미산출, 슬롯 승계 판단 |
| 87' (→로저스) | 웰벡 | ST | st_advanced | Support | **NULL** | ⚠️ hp=2·터치 2 — fit 미산출, 배치만 기록 |

### 시즌 처방 변경 여부

- `prescriptions` kind='measured' (regime 2 · 2026-27 · FC26) **6행 갱신/신설** — 이건 *측정 기록*이지 정본 처방이 아니다:
  - **갱신** 로저스 LM `wm_wideplm/Attack` 0.8011(n2) → **0.8468(n3)** — 역할 불변
  - **갱신** 조앙 페드루 ST `st_false9/Build-Up` 0.7396(n2) → **`st_advanced/Support` 0.7693(n4)** — ⭐ 역할 역전
  - **신설** 하토 `LWB(3-4-2-1)` fb_att_wb/Support 0.7717 (n2, 150')
  - **신설** 네투 `RWB(3-4-2-1)` fb_att_wb/Support 0.8144 (n2, 127')
  - **신설** 라비아 `LDM` cm_dlp/Build-Up 0.7460 (n3, 218')
  - **신설** 파머 `ST` st_false9/Build-Up **0.5576** (n2, 180') ⚠️ 낮음 — 인선 근거로 쓰지 말 것
- **미기록**: 아체암퐁(FB 0.6953 / CB 0.7043 / WM 0.7056 — **Δ0.011로 판정 불가**), E. 마르티네스(GK — 커널 변별력 없음).
- `fc26:opt:*`·`slot_canon_roles`·`team_tactic_setups` **변경 0**.

### 다음 경기 재검증 항목

1. **주앙 페드루 st_advanced vs st_false9** — 점유율이 다시 낮은 경기(예: 강팀 원정)에서 false9로 돌아가는가? obs#446(잭슨)과 같은 「국면 반응」인지 판별.
2. **윙백 좌우 비대칭**(네투 62 vs 하토 39)이 상대 무관하게 반복되는가.
3. **아체암퐁 RCB 적합 0.4556** — 다음 백3 경기에서도 볼 관여가 이 수준이면 슬롯 배치 자체를 재검토.
4. **PPDA** — 3경기 값이 22.67 / 9.58 / (풀럼전 미산출)이다. 4번째 값으로 분산 폭 확정.
5. **크로스 1/14** — 우측 단독 폭 구조에서 반복되는가, 아니면 이 경기 한정인가.

---

## 8. 영상·기사·감독 발언

**⚠️ 이 경기는 D+1이다.** 유튜브 전술 분석·전술 블로그는 D+1~D+3에 게시된다(SKILL §2-1a) — 아래는 당일~D+1 회차 결과이고, **D+1·D+2·D+3 후속 수집을 예약했다.**

| 종류 | 결과 |
|---|---|
| 유튜브 전술 분석 | **사실상 0건.** 검색에 잡힌 것은 경기 전 프리뷰(「THIERRY HENRY BREAKS DOWN XABI ALONSO'S CHELSEA TACTICS」, 「ARTETA and ALONSO」)와 [알론소 사전 기자회견 영상(2026-09-04)](https://www.youtube.com/watch?v=dIv7o0BfHDI)뿐이다. **직접 시청하지 않았고 채널명도 확정하지 못했다 — 검색 결과 제목 기준.** 인용 불가. |
| 전술 블로그 | **0건.** TFA · Spielverlagerung · Between the Lines · Coaches' Voice 전부 이 경기 대상 발행물 없음. 시도 검색어: `Spielverlagerung Chelsea Arsenal Alonso Analyse 2026`, `"Between the Lines" OR "Football Analyst" Chelsea Arsenal Alonso tactics`. (브라이턴전 D+3 회차에서도 이 3매체는 「4회 연속 0건」으로 이미 기록됨) |
| 기사 | [Yardbarker — "Alonso struck first, but he fell into Arteta's trap of gambles"](https://www.yardbarker.com/soccer/articles/alonso_struck_first_but_he_fell_into_artetas_trap_of_gambles/s1_17790_44267014) · [SI — Four Takeaways](https://www.si.com/soccer/four-takeaways-chelsea-defeat-xabi-alonso-9-6-26) · [football365 — Neville 비판](https://www.football365.com/news/gary-neville-133m-chelsea-transfer-deals-arsenal-loss-xabi-alonso) · [The Chelsea Chronicle 평점](https://www.thechelseachronicle.com/match-coverage/chelsea-player-ratings-vs-arsenal-morgan-rogers-a-9-but-blues-duo-get-5-10-in-enthralling-battle/) · [Arseblog 프리뷰(D-1)](https://arseblog.com/2026/09/can-arteta-take-advantage-of-early-days-alonso-as-chelsea-visit/) |
| 감독 1차 발언 | [NBC Sports — Alonso 회견](https://www.nbcsports.com/soccer/news/xabi-alonso-reaction-chelsea-manager-speaks-after-tight-derby-at-arsenal) · [ESPN — Alonso, 수비 문제 언급](https://www.espn.com/soccer/story/_/id/49851013/xabi-alonso-chelsea-address-defensive-issues-arsenal-defeat) · [Goal.com — "It hurts"](https://www.goal.com/en/lists/xabi-alonso-chelsea-defeat-arsenal-premier-league/blta32a83e3ffe54696) |

### 사비 알론소 — 경기 후 (Sky Sports 경유)

> "It hurts. It hurts because a defeat has to hurt. It has been a very intense game with different moments for everything. We had chances to equalise."
> (아프다. 패배는 아파야 하는 것이니까 아프다. 여러 국면이 있었던 매우 치열한 경기였다. 동점 기회들이 있었다.)

> ⭐ "After we scored, there were 15-20 minutes where we had to defend too much and we were struggling a bit to get control."
> (득점 후 15~20분 동안 우리는 너무 많이 수비해야 했고 통제력을 되찾는 데 조금 힘들어했다.)

> "We could do better with the second goal — we conceded too early."
> (두 번째 실점은 더 잘 처리할 수 있었다 — 너무 일찍 내줬다.)

> ⭐ "Arsenal do very good, interesting things. They overload on one side with 5-6 players. It's part of the game to have these actions and we continue."
> (아스날은 좋고 흥미로운 것들을 한다. 한쪽에 5~6명을 오버로드시킨다. 그런 상황도 경기의 일부이고 우리는 계속 나아간다.)

> "This is a process. It's still early days for us. We want to start having clean-sheets. They will come."
> (이것은 과정이다. 아직 초기 단계다. 클린시트를 시작하고 싶다. 곧 올 것이다.)

**실측 대조**: 「득점 후 15~20분」 진단은 실측 `phase_lead 23분`과 정확히 겹친다. 「한쪽 5~6명 오버로드」는 아체암퐁·네투가 있던 첼시 우측이 열린 것과 정합한다.

### 미켈 아르테타 — 경기 후 (Arsenal.com)

> "Against Chelsea, you know exactly the game that you're going to play. They have so much quality, and you have to adapt so much to what they do."
> (첼시를 상대하면 어떤 경기가 펼쳐질지 정확히 알게 된다. 그들은 매우 뛰어나서 그들이 하는 것에 많이 적응해야 한다.)

> "The way they use the keeper as an extra player, the courage that they show, how they get out from tight situations, it's unbelievable."
> (골키퍼를 여분의 선수처럼 쓰는 방식, 그들이 보여주는 용기, 좁은 상황에서 빠져나오는 방식은 믿기지 않는다.)

⚠️ 이 인용은 페이지 전체 대조를 마치지 못했다. 같은 회견 발췌에서 **아스날과 무관한 선수(브루누 기마랑이스) 언급이 혼입**돼 있어 인접 문장의 신뢰도를 낮춰 취급한다. D+1 추적에서 원문 재확인 대상.

### 선수 1차 발언

> 하토(경기 전, [Yahoo](https://ca.sports.yahoo.com/news/jorrel-hato-issues-dangerous-warning-091855879.html)): 첼시 수비가 「아직 그 수준이 아니다」(직전 3경기 5실점 자인).

### 다국어 커버리지

| 언어 | 성과 | 주요 검색어 |
|---|---|---|
| 영어 | ⭐⭐⭐ 회견 원문·평점·전술 기사 확보 | `Arsenal Chelsea 2-1 tactical analysis`, `Xabi Alonso press conference Arsenal Chelsea` |
| 스페인어 | ⭐⭐ 포메이션 연속성 확인(el nacional 등) | `Alonso Arsenal Chelsea 3-4-2-1 análisis táctico` |
| 네덜란드어 | ⭐ NOS 원문으로 득점자·어시스트 검증, 하토 서술 | `Jorrel Hato Arsenal Chelsea wedstrijd analyse` |
| 포르투갈어 | ⭐ 조앙 페드루·에스테방 개인 서술(abola.pt, dgabc) | `João Pedro Estêvão Chelsea Arsenal derby análise` |
| 프랑스어 | ⭐ 라크루아 실책 장면 상세(footmercato) | `Lacroix Chelsea Arsenal défaite analyse tactique` |
| 독일어 | ⚠️ **0건** — kicker·Spielverlagerung 원문 없음. 검색 결과는 영어 소스의 재서술이라 부가가치 없음으로 종결 | `Xabi Alonso Chelsea Arsenal Niederlage Taktik Analyse` |

### 미수행 소스와 사유

- **유튜브 전술 분석 직접 시청 0건** — 게시 지연(D+1~D+3). 후속 수집 예약됨.
- **전술 블로그 0건** — 동일 사유 + 이 3매체는 첼시를 반복적으로 다루지 않음(브라이턴전에서 확인).
- **아체암퐁 전용 네덜란드어 자료 0건** — 첼시 유스 출신 수비 자원에 대한 현지어 심층 취재가 이 시점에 존재하지 않음.
- **아르테타 회견 원문 완독 미완** — 위 ⚠️ 참조.

### 기각한 주장

- ⛔ 검색 요약이 「칼라피오리가 동점골」이라 서술했으나 **NOS 원문 직접 확인 결과 하베르츠가 맞다**. 검색 도구의 합성 오류로 판정, 폐기.
- ⛔ 아르테타 회견 발췌에 브루누 기마랑이스(뉴캐슬) 언급 혼입 — 명백한 오류로 기각.
- ⚠️ 「첼시가 이미 세트피스에서 2골 실점」이라는 수치는 검색 요약 경유(원문 미확인) — **MEDIUM 이하로 취급**, D+1 추적에서 재검증.

---

## 9. 데이터 반영과 한계

**DB에 추가한 행**

| 테이블 | 내용 |
|---|---|
| `matches` | id=98 · event 16363257 · CHE · 2026-27 · A · 1-2 · 점유 45.0 |
| `player_matches` | **15행**(출전 전원). pos_class·map25·국면 분(lead/level/trail) 포함 |
| `team_match_stats` | 1행 · **`xg_source='FotMob'`** · PPDA 9.58/7.58(WhoScored Opta) |
| `prescriptions` | kind='measured' **2행 갱신 + 4행 신설**(§7) |
| `observations` | **#467~#471** 5건 |
| `match_reports` | 1행 · status **complete** |
| `match_player_reports` | **15행** |
| `match_game_setups` | 1행 (match_only=1) |
| `match_player_prescriptions` | **15행** (선발 11 + 교체 4, match_only) |

**한계**

- **단일 경기·원정·상대 아스날**이다. xG 0.39는 시즌 대표값이 아니라 이 상대·이 국면의 값이다.
- **스코어 효과가 크다**: 경기의 44%(40분)를 지고 있었다. 후반 수치는 추격 국면에 오염돼 있다.
- **포지션 혼입**: 알론소 로테이션 탓에 26/27 첼시 표본은 선수당 pos_class가 2~5개로 갈린다. 파머(ST n=2 / RM n=2)·라크루아(RCB·RB·LCB·CCB 각 1)는 포지션-순수 집계가 아직 서지 않는다.
- **결손값**: 웰벡(hp=2)·에스테방(hp=8)은 그리드 무효. 아체암퐁(hp=28)은 기준은 넘겼으나 90분치고 비정상적으로 얕다 — fit 0.4556은 이 얕음의 결과일 수 있다.
- ⚠️ **`pos_class` 오분류**(obs#467): 하토·네투가 LDM/RDM으로 찍힌다. 이번 회차는 core 산출값을 그대로 두고 `prescriptions.pos_label`에서만 교정했다.
- ⚠️ **`event_id` 이중 규약**(obs#471): 저장소의 PL 5경기가 FotMob id로 적재돼 있어 중복 적재 방지 절차가 그 5경기에는 작동하지 않는다. 이번 경기는 SofaScore id로 적재했다. **수정 미실시 — 사용자 판단 대기.**
- **D+1~D+3 추적 미완**: 전술 블로그·유튜브 분석이 아직 없다. 후속 3회 수집이 예약돼 있고, 결과는 이 파일의 `## D+N 추적` 절에 **덧붙인다**(덮어쓰지 않는다).

**G12**: 이번 회차 종료 시점 전항 통과(불완전 0 · 선수행0 0 · 선수누락 0 · 원문누락 0 · 경기프리셋누락 0 · 선수처방누락 0 · xG원천결손 0 · xG스냅샷혼합 3/3 유지).

---

## D+2 추적 (2026-09-08)

> 이 절은 **덧붙임**이다(불변규칙 2). 위 당일 절은 고치지 않았고, 뒤집힌 판정은 아래 「당일 판정 정정」에 적는다.
> ⭐ **당일 회차가 「사실상 0건」으로 닫았던 유튜브 전술 분석이 D+2에 4편 확보됐다** — 검색엔진 질의가 아니라
> **유튜브 사이트 내부 검색**(`&sp=EgIIAw%3D%3D`, 업로드=이번 주)으로 훑은 결과다(obs#516 규약 적용, 두 번째 실증).

### 확보한 1차 자료

| # | 종류 | 채널·매체 | 제목 | 게시 | 확인 방식 |
|---|---|---|---|---|---|
| 1 | 전술 분석 | Football Made Simple | Arteta Found The Flaw In Alonso's System | 09-07 (D+1 심야) | **자동 자막 전사** `reports/transcripts/URlf-04YYLk.en.md` |
| 2 | 전술 분석 | Zekko Football | Why Alonso's New Chelsea Tactics FAILED Against Arsenal | 09-08 새벽 | **자동 자막 전사** `fvy4fhYn8Bc.en.md` |
| 3 | 펀딧 분석 | Sky Sports PL (캐러거·라이트·스터리지) | FULL Super Sunday post-match analysis | 09-07 | **자동 자막 전사** `6RuIVhy2X2M.en.md` |
| 4 | 팬 채널(3티어) | George Benson Football Chelsea | 아스널 2-1 첼시에서 배운 6가지 | 09-07 | **자동 자막 전사** `pS8z69CMjCQ.en.md` |
| 5 | **감독 회견 원문** | MightyBluesNews / BeanymanSports | 알론소 경기 후 회견 **전체** | 09-07 | **자동 자막 전사** `lqUvVPp4A1w.en.md` |
| 6 | **감독 회견 원문** | HaytersTV | 아르테타 경기 후 회견 **전체** | 09-07 | **자동 자막 전사** `ipGsi40qJKM.en.md` |
| 7 | 감독 회견 원문 | Arsenal 공식 | 아르테타 **경기 전** 회견(09-05) — 인용 출처 검증용 | 09-05 | **자동 자막 전사** `XJsTW81j9M8.en.md` |

⚠️ 1~7 전부 **유튜브 자동 생성 자막**이다(영상·음성 미시청). 인명 오인식이 있다(「Chabby Alonzo」·「Califury」·「Achapong」·「Hatau」) —
인용 시 confidence에 **auto-caption** 명기. 회견 전사는 발언자 귀속을 문맥으로 재확인했다.

### ⭐⭐ 알론소 경기 후 회견 — 전문 확보 (당일 절은 Sky 요약 경유 5문장뿐이었다)

> **"They overload a lot on the left side with many players."**
> (그들은 **왼쪽**에 많은 선수로 크게 오버로드를 건다.)
> ⭐ 당일 절의 Sky 판본은 「한쪽에 5~6명」이었다. 원문은 **어느 쪽인지 특정**한다 — 첼시 기준 좌측, 즉 **하토 쪽**이다.
> 전술 분석 2편이 독립적으로 「아스날의 우측(사카·화이트) 오버로드」라고 서술해 방향이 일치한다.

> ⭐⭐ **"We didn't want from the first minute to sit deep and to wait and to make a long game. We wanted it to be active. We wanted to be protagonist in the pressing, sometimes to go higher, sometimes lower, to have good possessions."**
> (첫 분부터 깊이 앉아 기다리며 경기를 길게 끌 생각은 없었다. 능동적이길 원했다. **압박에서 주도자**이길 원했다 — 때로는 더 높게, 때로는 더 낮게 — 그리고 좋은 점유를 갖길 원했다.)
> ⭐ **obs#469(PPDA 22.67→9.58, 라운드 사이 2.4배 요동)의 감독 1차 근거다.** 요동은 표본 잡음이나 상대 반응이 아니라 **설계된 가변성**이라고 감독 본인이 말한다.

> (기자: 「이번 시즌 벌써 7실점이다. 그것을 바로잡는 것이 최우선 과제인가?」)
> **"My priority is to win games. And for that normally it's easier when you don't concede many. So for sure this is something that we need to address. We want to be tighter, to be more clinical, more balanced. But this takes time as well."**
> (내 최우선 과제는 경기를 이기는 것이다. 그러려면 보통 많이 실점하지 않는 편이 쉽다. 그러니 분명 이것은 우리가 다뤄야 할 문제다. 더 조밀하고, 더 결정적이고, 더 균형 잡히길 원한다. 하지만 이것도 시간이 걸린다.)

> **"We wanted to compete. We wanted to win here. We came to win. We knew that we were not that far, but it went that way."**
> (경쟁하고 싶었다. 여기서 이기고 싶었다. 이기러 왔다. 우리가 그렇게 멀지 않다는 걸 알았지만, 그렇게 흘러갔다.)

> **"It's about assessing the risk. Probably last week we took him too early and I don't want to make the same mistake again."**
> (리스크를 평가하는 문제다. 아마 지난주 우리는 그를 **너무 일찍 투입했고**, 같은 실수를 반복하고 싶지 않다.)
> ⚠️ 부상 복귀 판단에 대한 발언이다. 영상 제목·채널 설명은 **모이세스 카이세도**를 지목하지만, 전사 본문에서는 이름이 나오는 대목이
> 잘려 있어 **대상 선수를 전사만으로는 확정할 수 없다**. 카이세도는 이 경기 명단에 없다. ⇒ **미확정으로 남긴다.**

> **"I'm happy with the players we have. For sure you need to deal with injuries… but we need them because they are top players and with them we are a better team."**
> (있는 선수들에게 만족한다. 부상은 감당해야 하는 것이다… 하지만 그들이 필요하다. 톱 플레이어들이고 그들이 있으면 우리는 더 나은 팀이다.)

**실측 대조**: 「득점 후 15분」 진단(당일 절)이 원문에서도 반복된다(`the next 15 minutes they were really pushing us hard… we were defending low`). 실측 `phase_lead 23분`과 정합.

### ⭐ 아르테타 경기 후 회견 — 원문 확보, **당일 절의 인용 2건은 검증 실패**

경기 후 회견 전사(#6)와 **경기 전** 회견 전사(#7) **어디에도** 당일 절이 Arsenal.com 경유로 인용한 두 문장
(「you know exactly the game that you're going to play」·「The way they use the keeper as an extra player… it's unbelievable」)이 **없다**.
당일 절이 이미 같은 페이지의 브루누 기마랑이스(뉴캐슬) 혼입을 이유로 신뢰도를 낮춰 뒀는데, 회견 원문 대조로 **출처 미확정**이 확인됐다.
⛔ **이 인용 2건은 근거로 쓰지 않는다**(폐기가 아니라 보류 — 정확한 Arsenal.com URL이 확인되면 복원한다).
⭐ 게다가 「GK를 여분의 선수로 쓴다」는 서술은 **이 경기의 전술 분석과 어긋난다** — 아래 「당일 판정 정정 ③」 참조.

회견 원문에서 실제로 확인된 것(이 경기 관련):

> **"I think it was an exceptional performance… the beginning was tough, but I enjoyed it because the team reacted in a spectacular way."**
> (예외적인 경기력이었다고 생각한다… 시작은 힘들었지만, 팀이 굉장한 방식으로 반응했기 때문에 즐겼다.)

> (로저스 실점 국면에 대해) **"There are something that we do badly in that goal that we discussed before, but credit to them as well — from that ball in the air, somebody's able to put the ball very close to the post and score against David, which is not easy."**
> (그 실점에서 우리가 잘못한 것이 있고 전에 이야기했던 것이다. 다만 상대에게도 공을 돌려야 한다 — 그 공중볼에서 누군가 포스트에 아주 가깝게 공을 넣어 데이비드를 상대로 득점했고, 그건 쉬운 일이 아니다.)

> ⭐⭐ (교체 투입 선수에 대해) **"I think he played 11 minutes. He had five or six training sessions. The way he played tonight against this opponent, playing man-to-man against João Pedro — he was phenomenal."**
> (11분을 뛰었다고 본다. 훈련 세션을 대여섯 번 했다. 오늘 밤 이 상대를 맞아 뛴 방식, **주앙 페드루를 맨투맨으로 잡은 것** — 경이로웠다.)
> ⭐ **아스날이 주앙 페드루에게 맨마킹을 붙였다**는 감독 1차 확인이다. 첼시 최전방 고립의 상대측 설계 근거.
> ⚠️ 자동 자막이 질문과 답변의 선수 이름을 뒤섞어 **해당 아스날 선수의 이름은 특정하지 못했다**(신입, 훈련 5~6회).

### ⭐⭐ 전술 분석 2편 + 펀딧이 수렴한 것 — 「백3」가 아니라 **백4↔백5 하이브리드**

세 소스가 **독립적으로 같은 것**을 말한다.

> Football Made Simple: **"because the Italian [Calafiori] was inverting high, deep, and all over the place, when Neto followed him, Acheampong was isolated wide and in effect, Chelsea were forced to defend in a back four with a massive gap appearing in this half space."**
> (칼라피오리가 높게·깊게·사방으로 인버트했기 때문에, 네투가 그를 따라가면 아체암퐁이 와이드에 고립됐고, 사실상 첼시는 **이 하프스페이스에 거대한 틈이 생긴 백4로 수비하도록 강요당했다**.)

> Zekko Football: **"They played a back five and a back four simultaneously, changing all the time depending on… positions of the opposition players [and] the actual game state."**
> (그들은 백5와 백4를 **동시에** 썼고, 상대 선수들의 위치와 실제 게임 상태에 따라 계속 바꿨다.)

> ⭐ Sky Sports 캐러거: **"Chelsea today, even if you think about the first half, Achapong was actually making overlapping runs. He was getting into the box. A center back in a back three would not make those runs. So in the main that was a back four today, but it was basically Neto follow Calafiori wherever he goes."**
> (오늘 첼시는, 전반만 생각해도 아체암퐁이 실제로 **오버래핑 런**을 하고 있었다. 박스 안까지 들어갔다. **백3의 센터백은 그런 런을 하지 않는다.** 그러니 오늘은 주로 백4였고, 기본적으로 **네투가 칼라피오리를 어디든 따라가는** 것이었다.)

**⭐⭐ 실측이 이 서사를 독립적으로 지지한다** (당일 수집한 평균 위치, 이번 회차에서 새로 대조):

| 선수 | avg_x(깊이) | avg_y(y 낮음=우측) | 읽기 |
|---|---|---|---|
| 라크루아 | **38.3** | 38.0 | 후방 라인 |
| 포파나 | **38.4** | 62.7 | 후방 라인 |
| **하토**(LWB) | **39.0** | 79.5 | ⭐ **CB 둘과 같은 깊이** — 좌측은 윙백이 아니라 **레프트백** |
| 리스 제임스 | 48.9 | 55.8 | 피벗 |
| **아체암퐁**(RCB) | **50.0** | 24.0 | ⭐⭐ CB 둘보다 **11.7 높다** · 우측 하프스페이스 |
| 네투(RWB) | 62.2 | 16.3 | 우측 최대 폭 |

⇒ 후방 3인(하토·포파나·라크루아)이 x≈38로 **평평한 라인**을 이루고, **아체암퐁 혼자 50까지 전진**해 있다.
**교과서적 백3가 아니라 「비대칭 백4 + 전진한 우측 수비수」**다. 서사와 실측이 같은 결론을 가리킨다.

### 당일 판정 정정

**① 「3-4-2-1은 변화가 아니라 연속」(obs#470)은 유지하되, 국면 층위를 분리해야 한다.**
명목 라인업이 3-4-2-1인 것은 맞다. 그러나 **온볼에서는 비대칭 백4(전진 RCB), 무공에서는 상대 와이드 진출에 따라 4-4-2↔5-4-1을 오간다.**
「백3 연속」을 구조 결론으로 쓰면 이 경기에 대해서는 오독이다. 정정은 새 obs로 기록한다(덮어쓰지 않는다).

**② 「아체암퐁 hp=28은 비정상적으로 얕다 → fit 0.4556은 그 얕음의 결과」(당일 §9 한계·재검증 항목 3)는 원인 진단이 틀렸다.**
얕은 것이 아니라 **전진해 있었다**(avg_x 50.0). 터치 21회는 **볼 관여가 없는 오프더볼 전진**의 결과다 —
Football Made Simple: **"the right center back more often than not marched forward into the half space to allow Neto to stay wide"**
(우측 센터백은 대개 하프스페이스로 전진해 네투가 넓게 남을 수 있게 했다). ⇒ **재검증 항목 3을 「볼 관여 얕음」에서
「전진 CB 임무의 반복 여부 + 오프더볼 전진 대비 볼 관여 괴리」로 교체**한다.

**③ 「첼시가 GK를 여분의 선수로 쓴다」(아르테타 인용 경유)는 이 경기에 대해서는 반증됐다.**
Football Made Simple: **"Like Arsenal, they were willing to go long from their goalkeeper with Palmer and Rogers ready to fight for the second balls."**
(아스날처럼 그들도 골키퍼에서 **길게 갈** 의향이 있었고, 파머와 로저스가 세컨볼을 다툴 준비를 했다.)
실측 롱볼 18/49(37%)와 정합한다. ⇒ 인용 자체가 출처 미확정(위)인 데다 내용도 이 경기와 어긋난다 — **근거 사용 보류**.

**④ 「윙백 좌우 비대칭(네투 62 vs 하토 39)」(재검증 항목 2)의 원인이 규명됐다.**
감독 선호나 선수 성향이 아니라 **칼라피오리 대응**이다. 네투가 칼라피오리를 사람 기준으로 추종했고(캐러거), 그 결과
우측만 폭이 살고 좌측은 평평한 백4가 됐다. ⇒ 재검증 질문을 **「상대 인버티드 풀백이 없는 경기에서도 이 비대칭이 재현되는가」**로 좁힌다.

### ⭐⭐ 2실점의 메커니즘 — 두 소스가 같은 장면을 분해했다

**동점골(25', 하베르츠)** — Zekko Football:
> **"One small movement from Havertz really starts to unlock this. He moves from that central role, vacating one of the Chelsea center backs, and begins to help Saka. This creates a 2v1 situation onto Hato… Fofana is following the run, but he's not close enough because of the distance between himself and Lacroix."**
> (하베르츠의 작은 움직임 하나가 이것을 푼다. 그는 중앙 역할에서 벗어나 **첼시 센터백 하나를 비워내고** 사카를 도우러 간다. 이것이 **하토에게 2v1**을 만든다… 포파나가 그 런을 따라가지만, **라크루아와의 거리 때문에** 충분히 가깝지 못하다.)
> 이어서 **"because of the position of Odegaard, he stops Lacroix from being aggressive"**(외데고르의 위치 때문에 라크루아가 적극적으로 나가지 못한다) → 하베르츠 얼리 슛 → **"As Havertz takes the shot, Martinez isn't set."**(하베르츠가 슛할 때 마르티네스는 자세가 잡히지 않았다.)

**결승골(50', 외데고르)** — Football Made Simple:
> ⭐⭐ **"Chelsea only had a double pivot. So when we saw those wide overloads, a Chelsea pivot was often being dragged across… while it would help to cope with the wide overload, it left the remaining pivot with acres to defend if the center backs were not pushing up to assist. And for Odegaard's winner, we even see shades of this."**
> (첼시는 **더블 피벗밖에 없었다**. 그래서 와이드 오버로드가 나오면 첼시 피벗 하나가 그쪽으로 끌려갔고… 그것이 와이드 오버로드에는 도움이 되지만, **센터백들이 올라와 돕지 않으면 남은 피벗 하나가 광활한 지역을 혼자 수비하게 남는다**. 외데고르의 결승골에서도 그 그림자가 보인다.)

⇒ **구조 판정**: 이 경기 2실점은 개인 실책의 합이 아니라 **「더블 피벗 + 와이드 오버로드」의 산술**에서 나왔다.
좌측(하토)에서는 수적 2v1, 중앙에서는 피벗 1명 잔류. 알론소 본인의 「왼쪽 오버로드」 진단과 같은 곳을 가리킨다.

### ⭐ 라운드를 가로질러 반복되는 구조 — 파머·로저스의 「중앙 공격 / 와이드 수비」 부하

> Football Made Simple: **"In our first analysis of Alonso's Chelsea against Fulham, we talked about the disadvantages of having players like Palmer and Rogers being expected to attack centrally but then defend wide, as the workload and their natural attacking instincts would leave them vulnerable, which Fulham made them pay for. Well, even though Rogers was wide in this match… Arsenal could still have success running off of him."**
> (알론소 첼시에 대한 우리의 첫 분석인 풀럼전에서, 파머와 로저스 같은 선수들이 **중앙으로 공격하고 와이드로 수비하도록** 요구받는 것의 단점을 이야기했다 — 그 작업량과 타고난 공격 본능이 그들을 취약하게 만든다는 것이고, 풀럼이 그 대가를 치르게 했다. 이번 경기에서 로저스가 와이드에 있었음에도… 아스날은 여전히 그를 등지고 달려 성과를 냈다.)

> Sky Sports 캐러거(파머에 대해): **"Palmer, we know he's a wonderful player, but would he do enough for the team defensively?"**
> (파머, 우리는 그가 훌륭한 선수임을 안다. 그러나 그가 팀을 위해 수비적으로 충분히 해줄까?)

⇒ **동일 채널이 풀럼전에서 이미 같은 지적을 했고 아스날전에서 재현됐다**는 점에서, 이것은 경기 한정이 아니라 **체제 형질 후보**다.
다만 두 경기 모두 같은 분석자의 관찰이라 **독립 소스 1건이 더 필요**하다 — 다음 회차 재검증 항목으로 올린다.

### 아스날의 대응 방식 — 상대팀 관점

> Zekko Football: **"Instead of dropping into a back five and simply creating that numerical equality, what they actually did was be far more aggressive, working on 2v1 situations between wingers and fullbacks onto opposition players."**
> (백5로 내려앉아 단순히 수적 동등을 만드는 대신, 그들이 실제로 한 것은 훨씬 더 공격적으로 나서서 **윙어와 풀백이 상대 선수에게 2v1을 거는 것**이었다.)

⇒ 같은 문제(상대의 폭·인버티드 풀백)에 대해 **첼시는 「수적 동등」, 아스날은 「국지적 수적 우위」**로 답했다.
알론소 본인의 원칙 서술("it's not about formation")과 맞물리는 대비다. 캐러거는 이 원칙 주장에 유보를 달았다:
> **"He would argue, as he has done already, it's not about formation — but isn't it always the ones who play five at the back who say that?"**
> (그는 이미 그래왔듯 포메이션의 문제가 아니라고 주장할 것이다 — 그런데 **백5를 쓰는 사람들이 늘 그렇게 말하지 않나?**)

### 팬 채널(3티어) — 사실 항목만 채택

- 라비아 60분 교체 배경: **"Lavia was decent on the ball, but he looked gassed out after 40 minutes."**(라비아는 볼을 다룰 때 괜찮았지만 40분 뒤에는 방전돼 보였다.) — 3티어 관찰이라 **체력 결론으로 쓰지 않는다**. 교체 시점(60')과 정합한다는 사실만 기록.
- 콜윌이 아체암퐁에게 밀려 제외됐다는 서술 — 선발 선택 배경으로만 기록(1차 확인 미완).
- 마르티네스 첫 실점 관여 비판(라크루아 다리 사이 통과). **Zekko·팬 채널 모두 「셋 되지 않은 상태의 얼리 슛」**을 말한다.
- 가브리엘의 마르티네스 머리 가격에 VAR 체크가 없었다는 주장 — **판정 논란은 이 리포트 범위 밖**, 기록만.

### 0건과 미수행 (D+2 시점)

| 항목 | 결과 | 시도 |
|---|---|---|
| 스페인어 전술 분석 영상 | **0건**(경기 후) | 유튜브 내부검색 `Xabi Alonso Chelsea análisis táctico Arsenal`(업로드=이번 주) — 잡힌 것은 전부 영어 채널 |
| 아르테타 회견의 문제 인용 원출처 | **미확인** | 경기 전·후 회견 전사 2건 대조 실패. Arsenal.com 정확한 URL 필요 |
| 알론소 「너무 일찍 투입」 대상 선수 | **미확정** | 전사에 이름 대목 결손. 카이세도 지목은 영상 제목 기준이라 채택 불가 |
| 전술 블로그 | 별도 서브에이전트 회차에서 확인 | 아래 「서브에이전트 회차」 절 |

### ⛔⛔ 당일 판정 정정 ⑤ — 아르테타 인용 2건은 **다른 시즌 경기**의 것이다 (날짜 혼입 함정)

원인이 규명됐다. Arsenal.com에 **제목이 거의 같은 회견 기사 두 개**가 있다.

| URL 슬러그 | 실제 경기 | 판정 |
|---|---|---|
| `every-word-artetas-post-chelsea-press-conference-apV972X6joGN` | **이 경기**(로저스 선제 → 하베르츠·외데고르 역전, 모스케라 부상) | ✅ 채택 |
| `every-word-from-artetas-post-chelsea-presser-a1kW85x3e3jV` | **다른 경기** — 라이스 부상 교체 · **첼시 퇴장** · **「5점 차 선두 회복」** | ⛔ 배제 |

⭐ 메인 세션이 두 번째 URL을 **직접 열어 확인**했다: 문제의 문장 「The way they use the keeper as an extra player…」가
**그 페이지에 있고**, 같은 페이지가 **첼시 퇴장**과 **5점 차 선두 회복**을 말한다. 이 경기는 3라운드로 아스날이 3전 전승 시점이고
퇴장은 없었다(경고 첼시 4·아스날 2). ⇒ **이 경기가 아니다.** 서브에이전트 판정은 25/26 시즌 28라운드(2026-03-01)다.

⛔⛔ **함정의 구조**: 같은 대진·**같은 스코어(Arsenal 2-1 Chelsea)**가 시즌을 건너뛰어 반복됐다. 매체 티어(공식 구단 사이트)로도,
URL 슬러그로도, 검색 순위로도 잡히지 않는다. 잡아낸 지표는 **본문에 병기된 사건의 정합성**(퇴장·순위·부상자)뿐이다 —
transfer-watch §2-0의 「동시 병기된 타 구단·타 선수 상황」 지표가 **경기 리포트 축에서도 동일하게 작동**한다.
⇒ 이 경기 절에서 그 인용 2건에 근거한 서술은 모두 **철회**한다. 대신 확인된 이 경기 발언은 위 「아르테타 경기 후 회견」 절에 있다.

### ⭐⭐ Coaches' Voice — 「0건」이 또 뒤집혔다 (세 번째)

당일 회차가 「0건」으로 닫았으나 **2026-09-07자 이 경기 분석이 존재**했다
([learning.coachesvoice.com](https://learning.coachesvoice.com/cv/arsenal-chelsea-tactics-sep-2026/), 메인 세션 직접 확인).
헐전 D+2에서 같은 일이 있었고(obs#502), 이번이 **세 번째**다. ⇒ **Coaches' Voice는 「검색 0건」으로 닫지 말고 사이트를 직접 훑는다.**

- 무공 **5-4-1 로우블록** — 중앙 침투 제한 + 미드필드 압축.
- **네투**: "Neto dropped from his higher, more advanced position into a **right wing-back role on the defensive line**."
  (네투는 더 높고 전진된 위치에서 **수비 라인의 오른쪽 윙백 역할로** 내려왔다.) · **하토**는 좌측 수비 라인으로 접혔다.
- **아체암퐁**: 네투가 볼을 잡으면 공격을 지원하러 전진했고, **그것이 역습 시 수비 취약을 만들었다**.
- ⭐⭐ **라크루아**: "Maxence Lacroix was drawn out wider to engage Havertz, leaving **big horizontal distances** between Chelsea's defensive line."
  (라크루아가 하베르츠를 상대하러 더 넓게 끌려 나갔고, 첼시 수비 라인 사이에 **큰 수평 간격**을 남겼다.)
- **동점골**: 하베르츠가 외데고르·사카 옆 우측으로 드리프트해 첼시 좌측에 **3v2 오버로드**를 만들고, 하베르츠가 우측 넓은 위치에서 볼을 잡았다.
- **결승골**: 아스날이 좌측으로 순환한 뒤 **칼라피오리의 하프스페이스 침투가 복수의 수비수를 끌어당겨** 외데고르가 중앙에서 받아 마무리.

⇒ **Football Made Simple·Zekko·Sky 캐러거·Coaches' Voice 네 소스가 서로 다른 각도에서 같은 인과를 말한다**:
칼라피오리·하베르츠의 우측(첼시 좌측) 이동 → 네투·라크루아가 사람 기준으로 끌려감 → 수평 간격 → 하프스페이스·중앙 개방.

### ⭐ 선발 배경 — 아체암퐁 기용은 **전술 선택이 아니라 대체**였다

알론소 경기 전 회견(chelseafc.com 공식, 1차 소스):
> **"Fitness. Levi [Colwill] had a little thing during the week, so we wanted not to take a risk at this stage of the season."**
> (컨디션 문제다. 레비가 주중에 약간의 문제가 있어서 시즌 이 시점에 위험을 감수하고 싶지 않았다.)

⇒ 당일 절이 다루지 않았던 배경이다. **「전진하는 우측 CB」라는 임무 자체는 유지하되, 그 임무를 맡은 사람은 대체 자원**이었다.
게임 구현 판정에서 아체암퐁 개인 특성으로 역할을 고정하면 안 된다 — **슬롯의 임무가 먼저이고 사람은 가변**이다.
⚠️ 60분 라비아↔귀스토 · 하토↔차바리아 **교체 의도에 대한 알론소 직접 발언은 1차 소스 0건**이다(chelseafc.com·ESPN·Yahoo 전수 조회).

### ⭐ 「세트피스 2실점」 주장 판정 — **확인, 단 이 경기가 아니다**

Arsenal.com 경기 **프리뷰**(경기 전 발행) 원문:
> **"Conceding twice from set pieces already and looking quite nervy from balls sent into the box, there is a sense that Alonso's men have some work to do on their defensive game."**
> (이미 세트피스에서 두 번 실점했고 박스로 들어오는 볼에 상당히 불안해 보이는 만큼, 알론소의 팀은 수비에서 할 일이 남았다는 인상이다.)

⇒ **경기 전 시점의 누적치**(풀럼·브라이턴 2경기)이고 이 경기 실점 2골과는 무관하다. 당일 절의 「MEDIUM 이하 취급」 판정을
**「확인됐으나 시점이 다르다」로 정정**한다. ⭐ 부수 확인: **이 경기 첼시 선제골(2' 로저스)도 세트피스였고 하토가 배급했다** —
세트피스는 이 팀에게 양날이다.

### 아스날 관점 — 상대측 서술

- **Arseblog** 「Gunners too strong for work-in-progress Chelsea」(09-07): 첼시를 **「work-in-progress」**로 규정. 첼시 3-4-2-1 구조 분해나 60분 교체 언급은 **없다**.
- ⭐ **Yardbarker/Goal** 「Two right-backs in midfield?!」(Yosua Arya, 09-07): **60분 라비아↔귀스토 이후 천연 라이트백 2명(제임스·귀스토)이 중원**을 이룬 구조를 비판.
  결승골에서 **제임스가 외데고르를 놓쳤다**고 지목한다. ⚠️ 우리 실측은 결승골이 50분이라 **교체(60분) 이전**이다 —
  기사의 인과 연결은 시점이 어긋난다. **「두 라이트백 중원」 지적 자체는 60~90분 구간에만 적용**해야 한다.
  애슐리 영 인용: **"Teams will be seeing that Chelsea will sit in there and get men behind the ball, but there's still spaces through the lines."**
  (팀들은 첼시가 물러서서 볼 뒤에 사람을 모으지만 **라인 사이 공간은 여전히 열려 있다**는 걸 알게 될 것이다.)
- **The Athletic 아스날 담당: 0건**(검색 미노출).

### 선수 1차 발언 (신규)

> 라크루아([VAVEL](https://www.vavel.com/en/football/2026/09/07/chelsea-fc/1270533-lacroix-i-think-it-s-not-easy-to-play-there.html), 09-07):
> **"I think it's not easy to play there but we did good. I think it was a good start but once they scored it got more and more difficult. We deserved more."**
> (거기서 뛰는 건 쉽지 않지만 우리는 잘했다. 시작은 좋았지만 그들이 득점한 뒤로 점점 더 어려워졌다. 우리는 더 받을 자격이 있었다.)

### 전술 블로그 — 사이트별 결과 (D+2)

| 사이트 | 결과 |
|---|---|
| **Coaches' Voice** | ✅ **1건**(09-07) — 이번 회차 최대 수확. 「0건」 3회 연속 오판 종결 |
| TheMastermindSite | ❌ 이 경기 없음(09-07자 외데고르 글은 3경기 종합, 첼시 언급 0) |
| Total Football Analysis | ❌ Arsenal 카테고리 최신 2026-02. ⚠️ 검색에 걸리는 「Arsenal 2-1 Chelsea」는 **25/26 28R** — 배제 |
| Spielverlagerung | ❌ 최신글 2026-07-19 |
| Between the Lines | ❌ 0건 |

### 다국어 커버리지 (D+2 · 당일 절 대비 증분만)

| 언어 | 증분 | 비고 |
|---|---|---|
| 스페인어 | ⛔ **주요 매체 6곳 검색 차단**(marca·as·elpais·relevo·mundodeportivo·sport — API 400). 알론소 **스페인어 회견 원문 0건** | **브라우저 경로 재시도 필요** — 다음 회차 이월 |
| 독일어 | **0건 유지**(2회 연속) | kicker·Sky DE 이 경기 자료 없음 |
| 네덜란드어 | 직접 기사 **0건** | 하토 관련은 영어·Coaches' Voice 경유뿐 |
| 포르투갈어 | ⭐ 에스테방 **3경기 연속 벤치**, 81분 투입 | 원문 2곳 **403·402 페이월** — 브라우저 재시도 이월 |
| 프랑스어 | L'Équipe는 **이적 보도만**(€55m·2032년까지) | 이 경기 분석 0건 |

### 선수별 서술 (D+2 · 1차 소스 확인분)

**조시 아체암퐁 (전진형 우측 CB)** — 당일 절의 「비정상적으로 얕다」 해석을 대체한다.
> Coaches' Voice: **"When Chelsea won possession he [Neto] was advanced on to the last line on the right-hand side, supported by advancing right centre-back Josh Acheampong."**
> (첼시가 볼을 회수하면 네투는 우측 최전선까지 전진했고, **전진하는 우측 센터백 조시 아체암퐁이 이를 지원**했다.)
> Evening Standard(5/10): **"A couple of nice runs on the overlap and did use his pace. Some good long-throw deliveries too."**
> (오버랩으로 좋은 런을 두어 차례 했고 스피드를 활용했다. 좋은 롱스로인 배급도 있었다.) — ⭐ **롱스로인 담당**은 신규 정보.
> Sports Illustrated(5.6): **"With Arsenal purring down their right, we didn't see much of Acheampong defensively. The young defender was also seldom involved."**
> (아스날이 자기 우측으로 매끄럽게 흐르는 동안 아체암퐁을 수비적으로 볼 일이 별로 없었다. 이 어린 수비수는 관여 자체가 드물었다.)

⇒ **터치 21회·hp 28은 임무의 결과다.** 볼 회로에서 벗어난 높이에 있었기 때문이지 부진이나 결손이 아니다.

**⭐⭐ 결승골은 아체암퐁이 비운 자리에서 나왔다** — 인과 사슬이 닫혔다.
> Coaches' Voice: **"Acheampong engaging — Calafiori made a half-space run. The latter attracted Lacroix and Neto — who had filled in for Acheampong."**
> (아체암퐁이 나가 붙자 칼라피오리가 하프스페이스로 침투했다. 이 움직임이 라크루아와, **아체암퐁 자리를 메우고 있던 네투**를 끌어당겼다.)
> 이어 **"With James unable to recover into a more central position to track the run in behind by Ødegaard"**
> (제임스가 외데고르의 배후 침투를 추적하러 더 중앙으로 복귀하지 못한 채) → 외데고르 결승골.

⇒ **동점골은 첼시 좌측(하토), 결승골은 첼시 우측(아체암퐁이 비운 쪽)**이다. 두 골이 **같은 설계의 양쪽 대가**다.
결승골 책임의 주류 귀속은 **리스 제임스**(Coaches' Voice·NBC·football.london 3중 일치)이고, 구조적으로는
「피벗이 촐리스·외데고르에게 횡으로 끌려난 뒤 중앙 복귀 실패」다.

**요럴 하토 (좌측 윙백, 60분)** — 🇳🇱 네덜란드어 1차 확인.
> VoetbalPrimeur(09-06): **"Na een vrije trap van Reece James won Jorrel Hato het kopduel, waarna de bal voor de voeten van Morgan Rogers viel."**
> (리스 제임스의 프리킥에서 **하토가 헤더 경합을 이겼고**, 그 뒤 볼이 모건 로저스의 발 앞에 떨어졌다.) ⇒ 선제골 어시스트의 실제 형태.
> football.london(6/10): **"The Dutchman was faced with the tough task of marking Saka but he stuck to it really well."**
> (이 네덜란드 선수는 사카를 마크하는 힘든 임무를 맡았지만 정말 잘 버텨냈다.)
> Sports Illustrated(7): **"Certainly not the long-term solution at wing back."** (좌측 윙백으로서 장기적 해답은 분명 아니다.)

⭐ **60분 교체는 부진·부상이 아니다.** 하토·라비아 **동시 2장**이었고 사유는 「중원 통제 회복」이다(chelseafc.com·VoetbalPrimeur 일치).
개인 사유 서술은 **어떤 언어권에서도 0건**. 오히려 라비아 교체 쪽에 의문이 제기됐다 —
SI: **"A curious choice on the hour from Alonso to remove Lavia."**(라비아를 빼는 것은 알론소의 기이한 선택이었다.)
⚠️ 팬 채널의 「라비아가 40분 만에 방전」 서술(3티어)과 매체의 「기이한 선택」이 갈린다. **미해결로 남긴다.**

**⭐ 주앙 페드루 — 「고정 9번 + 등지고 받는 연결형」. false 9 근거는 불충분** (재검증 항목 1에 대한 답).
> Coaches' Voice(수비 국면): **"João Pedro often screened the central pivot and was ready to release, while Cole Palmer and Morgan Rogers dropped either side of the midfield four."**
> (주앙 페드루는 자주 **중앙 피벗을 차단**하며 튀어나갈 준비를 했고, 파머와 로저스가 미드필드 4의 양옆으로 내려왔다.)
> SI/NBC(공격 국면): **"released Pedro Neto with a back-to-goal chop of over 50 yards."**
> (**골대를 등진 채 50야드가 넘는** 전환 패스로 네투를 풀어줬다.)
> 🇧🇷 포르투갈어 매체는 일관되게 **`centroavante`(고정 9번)**로 기술하고, **`falso nove`를 쓴 포르투갈어 1차 소스는 0건**이다.

⇒ **obs#468(주앙 페드루 최적합 st_false9 → st_advanced 역전, n 2→4)을 서사가 독립적으로 지지한다.**
수비 시 최전방 잔류(피벗 차단)는 false 9의 하강 패턴과 양립하지 않는다. **재검증 항목 1은 이 회차에서 「st_advanced 지지」로 진전**시킨다
(단일 경기이므로 정본 변경은 아니다).

**콜 파머 · 모건 로저스** — 수비 국면 분담은 **비대칭이 아니라 대칭**이었다.
> Coaches' Voice: **"Cole Palmer and Morgan Rogers dropped either side of the midfield four."**
> (파머와 로저스는 **미드필드 4의 양옆으로** 내려왔다.)
⇒ 「한 명은 안쪽 포켓, 한 명은 하강」이라는 비대칭 분담을 지지하는 1차 서술은 **0건**이다. 공격 국면 분담 서술도 못 찾았다 —
**다음 회차 수집 축으로 이월**한다.
- 로저스: 전 매체 7점 이상(SI 7.7 첼시 최고), 선제골. ⚠️ **Foot Mercato 실측 경합 0/7 승**과 평점이 어긋난다 — 게임 판단 시 유의.
- 파머: 전 매체 5~6.5로 혹평 일치. Evening Standard **"Saw plenty of the ball but no telling impact."**(볼은 많이 만졌지만 결정적 영향은 없었다.)
  Foot Mercato: **최종 3선 패스 20회 성공 · 빅찬스 창출 1**. ⇒ 「조용했다」보다 **「관여는 많았고 산출이 없었다」**가 실측에 맞다.

**에스테방** — 🇧🇷 **3경기 연속 벤치**, 81분 네투와 교체 투입.
> dgabc(PT): **"ficou pela terceira vez seguida na reserva. Restando apenas 10 minutos, Alonso finalmente recorreu ao brasileiro."**
> (3경기 연속 벤치에 머물렀다. 10분만 남기고서야 알론소는 마침내 이 브라질 선수를 꺼내 들었다.)
> football.london(7/10, 교체 선수 최고): **"The Brazilian made Chelsea much more threatening after his introduction."**
> (이 브라질 선수는 투입 후 첼시를 훨씬 더 위협적으로 만들었다.) — 더 일찍 투입했어야 한다는 문제 제기 동반.

**에밀리아노 마르티네스** — ⛔ **빌드업 가담 서술은 어느 언어권에서도 0건**이다.
🇪🇸 Infobae 원문(fetch 확인)은 세이브와 5분경 가브리에우의 안면 가격만 다루고 **배급·후방 빌드업 언급이 없다**. Coaches' Voice에도 없다.
스페인어 검색에 걸리는 「발밑이 좋다」류는 전부 **빌라 시절 이적 프리뷰**라 배제했다(불변규칙 7).
⭐ **아르테타의 이 경기 GK 관련 발언은 자기 팀 GK 라야에 대한 것**(「심장이 멎을 뻔했다」)이지 마르티네스가 아니다.
⇒ 당일 절 정정 ③을 보강한다 — 「첼시가 GK를 빌드업 여분으로 쓴다」는 **이 경기에 대해 어떤 1차 소스도 지지하지 않는다.**
- 동점골 책임은 매체가 갈린다: Evening Standard 4점(**"a suspect one to concede"** 내주기에 미심쩍은 실점) · football.london 5점(니어 포스트 포지셔닝) ↔ SI 7.5 · Foot Mercato 알고리즘 평점 **8.0(첼시 최고)**. **미해결로 기록.**

**막상스 라크루아** — ⛔ 「실책」 특정 실패.
🇫🇷 L'Équipe·RMC는 이 경기 기사 **0건**, Foot Mercato는 스탯 페이지만 있다. 「하베르츠 슛이 라크루아 다리 사이로 통과했다」는
**3티어 팬 채널 서술이고 1차 소스로 확인되지 않았다 — 채택하지 않는다.**
1차 소스가 말하는 것은 개인 실책이 아니라 구조다:
> Coaches' Voice: **"Maxence Lacroix was drawn out wider to engage Havertz, leaving big horizontal distances between Chelsea's defensive line."**
> (라크루아가 하베르츠를 상대하러 더 넓게 끌려 나갔고, 첼시 수비 라인 사이에 **큰 수평 간격**을 남겼다.)
⚠️ 평점 분산이 이 경기 최대다: Evening Standard **4** ↔ football.london 6 ↔ NBC 6.5 ↔ SI 6.5.

### ⛔ 새로 확인된 소스 충돌 (해소하지 않고 기록)

| # | 항목 | 채택 | 충돌 주장 |
|---|---|---|---|
| 1 | **포메이션** | 3-4-2-1(실측·Coaches' Voice·🇳🇱·Foot Mercato) | ⭐ **chelseafc.com 공식 리포트가 4-2-3-1 · 아체암퐁 「우측 풀백」**으로 기술. 네덜란드 매체가 이 불일치를 명시 지적. ⇒ **구단 공식 리포트의 포메이션 기술은 신뢰하지 않는다.** ⚠️ 다만 이 「오기」가 캐러거의 「사실상 백4」 관찰과 **같은 방향**이라는 점은 우연이 아닐 수 있다 |
| 2 | **교체 대응** | **네투 OUT 81' / 로저스 OUT 87'**(실측 출전시간·AOL·dgabc 일치) | chelseafc.com은 **반대로** 기술(로저스 81'·네투 87') |
| 3 | **선제골 헤더 승자** | **하토**(🇳🇱 상세 서술 + 공식 어시스트 기록) | SI는 **라크루아**가 가브리에우를 공중에서 눌렀다고 서술 |
| 4 | **선제골 마무리 형태** | 미확정 | 「박스 밖 첫 터치」(chelseafc·🇳🇱) ↔ 「volley」(SI·Standard) ↔ 「박스 안」(Playmaker Brasil) ↔ 「낮은 오른발 땅볼」(La Nación) — **4가지로 갈린다** |
| 5 | **아체암퐁 × 촐리스** | 결승골 주책임은 **제임스**(3중 일치) | NBC 「촐리스에게 제쳐져 결승골로 이어짐」 ↔ football.london·Chronicle 「촐리스를 이겼다」 |

### 막힌 URL (다음 회차 브라우저 재시도)

`readchelsea.com` 평점(403) · `observador.pt`(402 페이월) · `mundiario.com`(403) ·
🇪🇸 marca·as·elpais·relevo·mundodeportivo·sport(**WebSearch 도메인 차단** — 알론소 스페인어 회견 원문 미확보) ·
`elobservador.com.uy` 「마르티네스의 중대한 실책」(미시도 — 동점골 책임 규명에 필요) · `portaldemocrata.com.br`(403)

### D+2 회차 DB 반영

| 테이블 | 내용 |
|---|---|
| `observations` | **#519~526 신규 8건** — ⑲ 백4↔백5 하이브리드(구조 정정) · ⑳ 아체암퐁 「얕음」 원인 정정 · ㉑ 2실점 구조 · ㉒ ⛔아르테타 인용 시즌 혼입 · ㉓ 0건 판정 2축 전복 · ㉔ 주앙 페드루 st_advanced 지지 · ㉕ 압박 높이 가변은 설계(obs#469 감독 근거) · ㉖ 선발·교체 배경 |
| `player_duties` | **10행 addendum**(덧붙임, 덮어쓰기 없음) — 아체암퐁 32 · 하토 62 · 주앙 페드루 67 · 네투 65 · 파머 66 · 로저스 91 · 라크루아 122 · 제임스 68 · 마르티네스 193 · 에스테방 69 |
| `reports/transcripts/` | 신규 7편 — `URlf-04YYLk` · `fvy4fhYn8Bc` · `6RuIVhy2X2M` · `pS8z69CMjCQ` · `lqUvVPp4A1w`(알론소 회견) · `ipGsi40qJKM`(아르테타 회견) · `XJsTW81j9M8`(아르테타 경기 전 회견) |

⛔ **당일 절·실측·`match_game_setups`·`prescriptions`는 고치지 않았다.** 이 회차는 **해석과 서사만** 갱신한다 —
단일 경기이고 커널 Δ 산출을 하지 않았으므로 처방 변경 근거가 아니다(§4 노이즈 규칙).

### D+3(09-09)로 넘기는 것

1. ⛔ **스페인어 주요 6개 매체 검색 차단**(marca·as·elpais·relevo·mundodeportivo·sport) — **브라우저 경로로 재시도**. 알론소 **스페인어 회견 원문** 미확보.
2. 막힌 URL 재시도: `elobservador.com.uy`(「마르티네스의 중대한 실책」 — 동점골 책임 규명) · `readchelsea.com` 평점(403) · `observador.pt`(402) · `mundiario.com`(403).
3. **파머·로저스의 공격 국면 분담** 서술 — 이 회차 0건. 무공 대칭 하강만 확인됐다.
4. 알론소 「too early」 발언의 **대상 선수 확정**(ESPN은 카이세도로 특정하나 그는 명단 외).
5. 「중앙 공격 / 와이드 수비」 부하 논점의 **독립 소스 1건** — 현재 근거 2건이 같은 분석 채널(풀럼전·아스날전)이다.
6. 선제골 마무리 형태 4중 충돌(발리 / 박스 밖 첫 터치 / 박스 안 / 낮은 오른발) — 영상 확인 필요.

## D+3 추적 (2026-09-09)

> 이 절도 **덧붙임**이다(불변규칙 2). 당일 절·D+2 절은 고치지 않았다.
> ⭐ **D+2가 넘긴 6건 중 5건이 닫혔다.** 결정적 전환은 두 가지다 —
> ⑴ **스페인 매체 브라우저 경로가 열렸다**(WebSearch API 차단 ≠ 접근 불가). marca·sport.es·relevo를 직접 읽었다.
> ⑵ **D+2의 「Between the Lines 0건」은 사이트명 오기였다** — 실제 이름은 **Between the Posts**이고, 이 경기 전문 분석이 있었다.

### 확보한 1차 자료 (D+3 신규)

| # | 종류 | 매체 | 언어 | 확인 방식 |
|---|---|---|---|---|
| 1 | ⭐⭐ 전술 분석 | **Between the Posts**(Josh Manley, 09-07) | 🇬🇧 | 브라우저 직접 — 패스맵 포함 |
| 2 | ⭐⭐ 전술 분석 | **tacticalfootballanalysis**(Joana Freitas, 09-08) | 🇬🇧 | 브라우저(후반 유료벽) |
| 3 | ⭐ 전술 분석 | **Chelsea FC Online**(Nnanna Mba, 09-08) | 🇬🇧 | 브라우저 |
| 4 | ⭐⭐ 경기 리포트 | **marca.com** 크로니카(Alberto Rubio, 09-06) | 🇪🇸 | **브라우저 — D+2 차단 돌파** |
| 5 | ⭐⭐ 경기 리포트 | **sport.es**(Clàudia Espinosa, 09-06) | 🇪🇸 | **브라우저 — D+2 차단 돌파** |
| 6 | 선수 프로필 | **relevo.com** 차바리아론(Miguel Ruiz, 08-27) | 🇪🇸 | 브라우저 |
| 7 | ⭐ 매치 리포트·피처 3편 | **readchelsea.com**(James Chettle, 09-06·07) | 🇬🇧 | **브라우저 — D+2 403 돌파** |
| 8 | ⭐ 상대팀 관점 | **readarsenal.com**(09-06·07) | 🇬🇧 | 브라우저 |
| 9 | ⭐ 경기 리포트 | **vi.nl**(09-06) | 🇳🇱 | 브라우저 — 신규 |
| 10 | 평점 종합 | **voetbalprimeur.nl**(09-07) | 🇳🇱 | 브라우저 — 신규 |
| 11 | ⭐ 전 선수 평점 | **hommedumatch.fr**(Romain Mazzotti, 09-07) | 🇫🇷 | 브라우저 — **프랑스어 이 경기 첫 1차 소스** |
| 12 | 감독 발언 | **NBC Sports** 알론소 반응 | 🇬🇧 | WebFetch |

### ⭐⭐ D+3 과제 ① — 선제골(2' 로저스) 마무리 형태 **확정**. 4중 충돌은 대부분 **가짜 충돌**이었다

**여섯 개 소스가 같은 것을 말한다**(그중 셋이 D+2에 없던 언어권이다).

> 🇪🇸 marca: **"Morgan Rogers … empaló desde la frontal un balón peinado por Jorrel Hato."**
> (모건 로저스가 **하토가 스친 볼**을 **박스 정면 밖에서 첫 터치로 내리찍었다**.)
> 🇪🇸 sport.es: **"El ex del Villa empaló un balón en la frontal tras una falta lateral."**
> (빌라 출신은 **측면 프리킥** 뒤 **박스 정면 밖에서 첫 터치로 때렸다**.)
> 🇬🇧 Between the Posts: **"Rogers' volley from the edge of the box found the bottom corner."**
> (로저스의 **박스 외곽 발리**가 **골대 아래 구석**으로 들어갔다.)
> 🇬🇧 tacticalfootballanalysis: **"the ball fell to Rogers after a rebound, and he finished with a first-touch shot from outside the box."**
> (**리바운드** 뒤 볼이 로저스에게 떨어졌고 그는 **박스 밖에서 첫 터치 슛**으로 마무리했다.)
> 🇬🇧 ReadChelsea: **"before it dropped towards Rogers outside the area. The summer signing swept a first-time effort beyond David Raya."**
> (볼이 **박스 밖** 로저스 쪽으로 떨어졌다. 이 여름 영입생은 **첫 터치 슛**을 라야 너머로 밀어 넣었다.)
> 🇫🇷 HommeDuMatch: **"Morgan Rogers avait ouvert le score d'une reprise de volée sur coup de pied arrêté."**
> (로저스가 **세트피스에서 발리**로 선제골을 넣었다.)

⇒ **확정: 세트피스 → 박스 밖(프론탈) → 첫 터치 발리 → 골대 아래 구석.**
⭐⭐ **D+2가 「4가지로 갈린다」고 본 것 중 3가지는 같은 사건의 다른 해상도였다.**
「발리」(SI·Standard)·「박스 밖 첫 터치」(chelseafc·🇳🇱)·「낮은 오른발 땅볼」(La Nación)은 **서로 모순이 아니다** —
발리 = 첫 터치, 프론탈 = 박스 밖, 낮은 땅볼 = bottom corner. **실제 오류는 「박스 안」(Playmaker Brasil) 하나뿐**이고 6:1로 반증됐다.
⇒ **규약 교훈**: 소스 충돌표를 만들 때 **서술 해상도 차이를 사실 충돌로 계상하지 말 것.** 같은 사건을
「동작」·「위치」·「궤적」 축으로 분해하면 충돌인지 보완인지 갈린다.

**부수 성과 — D+2 충돌 #3(선제골 헤더 승자: 하토 ↔ 라크루아)도 해소됐다. 둘 다 맞다.**
> ReadChelsea: **"James delivered a free-kick into the Arsenal penalty area and Maxence Lacroix won the initial aerial challenge. Jorrel Hato kept the second ball alive before it dropped towards Rogers."**
> (제임스가 프리킥을 넣었고 **라크루아가 최초 공중 경합을 이겼다**. **하토가 세컨볼을 살려** 로저스 쪽으로 떨어뜨렸다.)
⇒ **순차적인 두 사건**이다. SI(라크루아)는 1차 경합을, 🇳🇱 VoetbalPrimeur·vi.nl(하토)은 2차 경합을 서술했다.
🇳🇱 vi.nl: **"Hato de bal voor de voeten van Morgan Rogers kon koppen."**(하토가 볼을 로저스의 발 앞으로 **헤더로** 보낼 수 있었다.)
공식 어시스트가 하토인 것과도 정합한다. ⇒ **충돌 #3 폐기.**

### ⭐⭐ D+3 과제 ③·⑤ — 파머·로저스 분담: **압박 높이에 따라 역할이 뒤바뀐다**

D+2는 「무공 대칭 하강(Coaches' Voice)」만 확보했고 「비대칭 지지 0건 · 공격 국면 0건」으로 닫았다.
**두 축 모두 뒤집힌다.** 그리고 D+2가 본 「대칭」은 **틀린 게 아니라 국면 한정**이었다.

**⒜ 높은 압박 국면 = 4-4-2, 완전 비대칭**
> tacticalfootballanalysis: **"Chelsea pressed in a 4-4-2 formation, with Palmer joining João Pedro in the front two, Rogers dropping into the midfield line and Hato dropping into the defensive line to form a back four."**
> (첼시는 **4-4-2로 압박**했다 — **파머가 주앙 페드루와 함께 전방 2인**을 이루고, **로저스는 미드필드 라인으로 내려오고**, **하토는 수비 라인으로 내려와 백4를 만들었다**.)

**⒝ 로우블록 국면 = 5-4-1, 대칭**(D+2 확보분, Coaches' Voice)
> **"João Pedro screened the central pivot, while Cole Palmer and Morgan Rogers dropped either side of the midfield four."**

⇒ ⭐⭐ **판정: 파머·로저스의 무공 역할은 고정 분담이 아니라 「압박 높이의 함수」다.**
높게 갈 때 **파머는 올라가고 로저스는 내려온다**(비대칭). 낮게 앉을 때 **둘 다 미드필드 4의 양옆**(대칭).
이것은 알론소 본인의 회견 발언과 정확히 맞물린다 — *"sometimes to go higher, sometimes lower"*(D+2 확보).
**obs#525(압박 높이 가변은 설계)의 구체적 실행 형태가 이것이다.**
⇒ D+2의 「비대칭 분담 지지 0건」은 **국면을 분리하지 않아서 생긴 결론**이었다. 정정 obs를 만든다.

**⒞ 공격 국면 = 비대칭, 좌우 임무가 다르다** (D+2 0건 → 확보)
> Between the Posts: **"All of this helped clear space for Palmer to drop deeper in the right halfspace, although he also had freedom to roam into central areas too. With the freedom given to him by Alonso, Palmer becomes something of a catalyst for Chelsea's attacks, drifting into deeper areas to pick up the ball and try to change the picture using his creativity."**
> (이 모든 것이 **파머가 우측 하프스페이스에서 더 깊이 내려올** 공간을 열었고, 중앙으로 배회할 자유도 있었다. 알론소가 준 자유 덕에 **파머는 첼시 공격의 촉매**가 된다 — 더 깊은 지역으로 흘러 들어가 볼을 잡고 창의로 그림을 바꾸려 한다.)
> Between the Posts: **"on the left side Hato and Rogers would rotate between left halfspace and left wing. Rogers and João Pedro were both key outlets for Chelsea with their ability to receive long balls and hold defenders off physically."**
> (좌측에서는 **하토와 로저스가 좌측 하프스페이스와 좌측 윙을 로테이션**했다. **로저스와 주앙 페드루는 롱볼을 받아 수비수를 몸으로 버텨내는 능력**으로 첼시의 핵심 출구였다.)

⇒ **공격 국면 분담 확정**:
| | 파머(우) | 로저스(좌) |
|---|---|---|
| 기준 위치 | 우측 하프스페이스 | 좌측 하프스페이스↔좌측 윙 |
| 이동 방향 | **하강**(딥으로 내려와 볼 픽업) | **하토와 수직 로테이션** |
| 기능 | 촉매·창작(자유 부여) | **롱볼 타깃·등지고 버티기** |
| 게임 함의 | 하강형 크리에이터 슬롯 | 물리형 와이드 리시버 슬롯 |

⭐ **로저스의 「롱볼 받아 버티기」는 주앙 페드루와 같은 기능으로 묶인다** — obs#524(주앙 페드루 st_advanced 지지)와
**같은 방향**이다. 첼시의 전진 경로는 「후방에서 길게 → 등지고 받는 두 명(주앙 페드루·로저스) → 세컨볼」이고,
이는 D+2 정정 ③(GK에서 롱볼, 롱볼 18/49=37%)과도 정합한다.
🇫🇷 HommeDuMatch가 **주앙 페드루의 피파울 6회**를 특기한 것이 이 「몸으로 버티는 출구」 기능의 실측 흔적이다.

### ⭐⭐ D+3 과제 ⑤ — 「중앙 공격 / 와이드 수비」 부하: **독립 소스 2건 확보. 단 부하는 로저스에게 걸렸다**

D+2의 근거 2건은 같은 채널(Football Made Simple의 풀럼전·아스날전)이라 독립성이 없었다. **서로 독립된 2건이 붙었다.**

> ⭐ Between the Posts: **"Chelsea therefore found themselves in 4-4-2-like variations when defending, as Rogers also came back on the left side to track White."**
> (첼시는 수비 시 **4-4-2 변형**에 놓였다 — **로저스도 좌측으로 내려와 화이트를 추적**했기 때문이다.)

> ⭐ Chelsea FC Online: **"The most obvious change from Arteta was to push Havertz out to the right touchline to overload the left side of the Chelsea block. Sharing the turns with Odegaard, Bukayo Saka and Rice, the German constantly created three-on-two superiority against Rogers and Hato, gathering the ball in that very same right wide zone to score the equaliser."**
> (아르테타의 가장 뚜렷한 조정은 **하베르츠를 우측 터치라인으로 밀어내 첼시 블록의 좌측을 오버로드**한 것이었다. 외데고르·사카·라이스와 번갈아 가며 이 독일 선수는 **로저스와 하토를 상대로 3대2 우위를 계속 만들었고**, 바로 그 우측 와이드 존에서 볼을 잡아 동점골을 넣었다.)

⇒ ⭐⭐ **판정: 논점은 성립하되 대상이 바뀐다. 「파머와 로저스 둘 다」가 아니라 「로저스」다.**
- 이 경기에서 **파머는 무공에 와이드로 내려가지 않았다** — 높은 압박에서는 **전방 2인**(TFA), 로우블록에서만 미드4 옆(CV).
- 우측 와이드 수비는 파머가 아니라 **네투(미드필드 라인으로 상승)와 아체암퐁(촐리스 담당)**이 나눠 맡았다.
- **좌측만 공격형 선수(로저스)가 풀백(화이트)을 추적**했고, **정확히 그 지점에서 3v2가 걸려 동점골이 나왔다.**
⇒ **체제 형질 후보로 승격하되, 형질의 서술을 「파머·로저스의 중앙공격/와이드수비」에서
「좌측 인사이드 포워드가 상대 우측 풀백을 추적하는 구조적 부하」로 좁힌다.**
⚠️ 단 **반례가 있다.** ReadChelsea(풀럼전, 08-25)는 파머의 무공 기여를 **긍정 평가**했다 —
Opta 기준 **볼 리커버리 7 · 듀얼 승 10**이고 *"Alonso wants his forwards to create chances without leaving the rest of the team exposed, and Palmer's work without the ball showed an encouraging willingness to meet that demand."*
같은 풀럼전을 Football Made Simple은 「파머·로저스가 대가를 치렀다」고 봤다. **같은 경기에 대한 정반대 평가**다 —
파머 축은 **미해결로 남긴다**(로저스 축만 닫혔다).

### ⭐⭐ D+3 과제 ④ — 알론소 「too early」 대상 **확정: 모이세스 카이세도**. 그리고 「명단 외」는 모순이 아니라 **원인**이었다

D+2는 「카이세도는 이 경기 명단에 없다」를 이유로 미확정 처리했다. **인과가 반대였다.**

> 🇬🇧 NBC Sports(카이세도 부상 질문에 대한 답으로 명시 귀속): **"Not longer term, but we talk about assessing the risk. Probably last week we took him too early, and I don't want to make the same mistake."**
> (장기 부상은 아니다. 다만 **리스크 평가**의 문제다. 아마 **지난주 우리가 그를 너무 일찍 투입했고**, 같은 실수를 반복하고 싶지 않다.)
> 🇬🇧 알론소, Sky Sports 경유(ReadChelsea 인용): **"Caicedo was close but no point taking a risk at this point in the season."**
> (카이세도는 근접했지만 시즌 이 시점에 리스크를 감수할 이유가 없다.)
> 🇬🇧 ReadChelsea 사실 서술: **"Caicedo had returned against Brighton last weekend, only to ask to come off shortly afterwards when he again felt discomfort."**
> (카이세도는 **지난 주말 브라이턴전에 복귀**했으나 곧 다시 불편을 느껴 **스스로 교체를 요청**했다.)

⇒ **사슬이 닫혔다**: 2라운드(브라이턴) 조기 복귀 → 재악화·자진 교체 → **3라운드 명단 제외**.
「너무 일찍 투입했다」의 대상 경기는 **지난주 브라이턴전**이고 대상 선수는 **카이세도**다. ESPN·NBC·Sky 3중 일치.
⇒ **D+2의 「미확정」을 「확정」으로 정정**한다.

**⭐⭐ 그리고 이것이 obs#521(더블 피벗의 산술)의 인적 원인이다.**
> ReadChelsea: **"Caicedo's absence… left Alonso with an unusual midfield partnership. Reece James moved inside alongside Romeo Lavia."**
> (카이세도의 결장이 알론소에게 **이례적인 중원 조합**을 남겼다. **리스 제임스가 안쪽으로 이동해 라비아 옆에 섰다**.)
> Chelsea FC Online: **"Chelsea finished a game against the reigning champions with two natural right-backs in central midfield… That bit of improvisation is a consequence of a manic deadline day."**
> (첼시는 디펜딩 챔피언과의 경기를 **천연 라이트백 2명을 중앙 미드필드에 두고** 끝냈다… 그 즉흥은 **광란의 마감일**의 결과다.)

⇒ ⭐⭐ **판정: 이 경기의 더블 피벗은 설계가 아니라 비상 구성이다.**
엔소 페르난데스 매각(→맨시티) + 라민 카마라 영입 무산(모나코 철회) + 카이세도 부상이 겹쳐,
**본직 라이트백인 주장(제임스)이 피벗을 맡았다.** ⇒ **게임 구현에서 「제임스 = 피벗」을 알론소 체제의 정본 슬롯으로
고정하면 안 된다.** obs#521의 구조 진단은 유지하되, **원인 층위에 「인적 비상」을 분리해 붙인다.**
⚠️ D+2가 기록한 Yardbarker의 「두 라이트백 중원」 지적은 **시점이 60분 이후에 한정된다**는 D+2 판정이 맞고,
여기에 **「제임스 단독으로는 선발부터」**를 덧붙인다.

### ⭐⭐ 결승골(50') 인과 사슬 **완성** — D+2에 통째로 빠진 고리가 있었다: **하베르츠의 더미**

D+2는 Coaches' Voice 경유로 「칼라피오리 하프스페이스 침투 → 라크루아·네투 흡인 → 제임스 복귀 실패」까지 봤다.
**마무리 직전의 한 동작이 누락돼 있었다.** 여섯 소스가 독립적으로 그것을 말한다.

> 🇪🇸 marca: **"Christos Tzolis cortó hacia el medio y filtró un pase que dejó pasar Havertz, magistral, para que Martin Odegaard fusilara al Chelsea."**
> (촐리스가 중앙으로 꺾어 패스를 찔렀고, **하베르츠가 그것을 절묘하게 흘려보내** 외데고르가 첼시를 쏘아 맞혔다.)
> 🇪🇸 sport.es: **"Medio gol fue obra de Havertz, que dejó pasar el balón con inteligencia para que su compañero se plantara solo ante el Dibu."**
> (**골의 절반은 하베르츠의 작품**이었다 — 그가 **영리하게 볼을 흘려보내** 동료가 디부와 **단독으로** 맞서게 했다.)
> 🇳🇱 vi.nl: **"Tzolis gaf een lage voorzet die Havertz bewust aan zich voorbij liet gaan."**
> (촐리스가 **낮은 크로스**를 줬고 하베르츠가 **의도적으로 자기 옆을 지나가게 놔뒀다**.)
> 🇬🇧 ReadChelsea: **"Havertz cleverly allowed a low ball across the penalty area to run beyond him, leaving Ødegaard with the space to finish."**
> 🇬🇧 tacticalfootballanalysis: **"Tzolis broke Chelsea's defensive line with a pass, while Havertz's dummy and Ødegaard's well-timed run created the opportunity."**
> 🇬🇧 ReadArsenal: **"Tzolis fired the ball towards Havertz, whose intelligent dummy opened the space for Ødegaard."**

**전체 사슬**(Chelsea FC Online이 가장 완결된 판본을 준다):
> **"Tzolis received on the left and drove infield, Riccardo Calafiori's half-space run attracted both Lacroix and Neto, and Lavia was drawn across as the ball-side midfielder. James failed to recover centrally to track Odegaard's run and the midfielder arrived unmarked to finish emphatically."**
> (촐리스가 좌측에서 받아 **안쪽으로 몰았고**, **칼라피오리의 하프스페이스 침투가 라크루아와 네투를 함께 끌어당겼으며**, **라비아는 볼사이드 미드필더로 횡으로 끌려 나갔다**. **제임스가 중앙으로 복귀해 외데고르의 침투를 추적하지 못했고** 그는 **무마크로** 도착해 강하게 마무리했다.)

⇒ ⭐⭐ **D+2가 「충돌」로 본 것(촐리스 ↔ 칼라피오리 ↔ 제임스)은 충돌이 아니라 한 사슬의 서로 다른 마디였다.**
`촐리스 좌측 인필드 → 칼라피오리 하프스페이스 런(라크루아+네투 흡인) → 라비아 볼사이드 이동 →
낮은 크로스 → **하베르츠 더미** → 제임스 중앙 복귀 실패 → 외데고르 무마크 마무리`
**어시스트 공식 귀속은 촐리스**다(🇫🇷 HommeDuMatch: *"Tzolis … en délivrant une passe décisive pour le second but"*).

**⭐ 「제임스 단독 책임」은 완화해야 한다.**
> Between the Posts: **"Ødegaard was able to ghost into the box, untracked by Chelsea central midfielders or center-backs."**
> (외데고르는 **첼시 중앙 미드필더들에게도 센터백들에게도 추적받지 않은 채** 박스로 스며들 수 있었다.)
⇒ D+2의 「결승골 책임 주류 귀속은 리스 제임스(3중 일치)」에 **BTP의 「미드필더·센터백 전원 미추적」을 병기**한다.
개인 귀속과 집단 귀속이 갈리며, **BTP가 유일하게 센터백까지 책임에 포함**한다.

### ⭐ 동점골(25') — 어시스트 확정 + **책임의 무게중심이 마르티네스에서 피벗으로 옮겨간다**

**어시스트 = 데클란 라이스**(🇳🇱·🇫🇷 두 언어권 독립 확인, D+2에 없던 사실):
> 🇳🇱 vi.nl: **"De Duitser werd aangespeeld door Rice en schoot de bal daarna fenomenaal binnen."**
> (이 독일 선수는 **라이스에게 패스를 받아** 그 뒤 경이롭게 차 넣었다.)
> 🇫🇷 HommeDuMatch(라이스 7.5): **"il a distribué le jeu avec précision et a offert l'ouverture du score à Havertz."**
> (그는 정확하게 경기를 배급했고 **하베르츠에게 선제 실점 장면을 만들어 줬다**.)

**구조 원인 — 박스 앞 보호 결손**:
> ⭐⭐ Between the Posts: **"The protection in front of the box from James and Lavia was also lacking in key moments, such as in Havertz's equalizing goal in the first half, where he was able to dribble across the edge of the box with insufficient pressure before getting a near-post finish off."**
> (**제임스와 라비아의 박스 앞 보호가 핵심 순간에 결여**돼 있었다 — 전반 하베르츠의 동점골이 그렇다. 그는 **충분한 압박 없이 박스 외곽을 가로질러 드리블**한 뒤 **니어 포스트 마무리**를 만들어냈다.)

**슛 형태**(3개 소스 일치): 박스 **외곽**, **왼발**, **니어 포스트**, 낮게.
> 🇪🇸 marca: **"tiró la diagonal hacia el medio y batió al 'Dibu' con un tiro al palo corto con la zurda."** (안쪽으로 대각 이동 후 **왼발 니어 포스트** 슛)
> 🇬🇧 ReadChelsea: **"beating Martinez with a low left-footed effort from the edge of the penalty area."**

**⭐ 마르티네스 책임 재판정 — D+2의 「미해결」에서 진전.**
D+2가 본 평점 분산은 **실제로는 소수 대 다수**다. 이번 회차에 🇫🇷 평점이 추가되며 우호 쪽이 늘었다.

| 매체 | 평점 | 논조 |
|---|---|---|
| Evening Standard | **4** | *"a suspect one to concede"* |
| football.london | **5** | 니어 포스트 포지셔닝 |
| 🇪🇸 marca | (무평점) | **"batió al 'Dibu' -pudo hacer más-"**(디부를 이겼다 — **더 할 수 있었다**) |
| 🇫🇷 HommeDuMatch | **7** | **"un match exceptionnel avec huit arrêts"**(**8세이브**의 예외적 경기) |
| Sports Illustrated | 7.5 | — |
| Foot Mercato(알고리즘) | **8.0** | 첼시 최고 |

⇒ **판정**: 니어 포스트 비판은 3개 소스(Standard·football.london·marca)로 **실재하되 소수**이고,
**세이브 산출(8회)로 평가하는 다수는 우호적**이다. 그리고 **1차 전술 분석(BTP)은 개인이 아니라 피벗의 박스 앞 보호 결손을 지목**한다.
⇒ **책임 귀속을 「미해결」에서 「구조 우위 · 개인 부차」로 진전**시킨다. 게임 구현에서 GK 실책 특성을 조정할 근거가 아니다.
🇳🇱 vi.nl과 🇪🇸 marca가 각각 **마르티네스의 결정적 선방 2~3회**(18' 사카 근접 슛 · 69' 사카 · 하베르츠의 알 넣기 패스 이후)를 별도로 특기한 것도 같은 방향이다.

### ⭐⭐ obs#519(백4↔백5 하이브리드)에 **직접 1차 근거** — 하토가 수비 라인으로 내려온다

D+2는 이 판정을 실측(하토 avg_x 39.0 = CB와 같은 깊이)과 서사(FMS·Zekko·캐러거)의 **간접 수렴**으로 세웠다.
**메커니즘을 명시한 1차 서술이 나왔다.**

> tacticalfootballanalysis: **"Hato dropping into the defensive line to form a back four."**
> (**하토가 수비 라인으로 내려와 백4를 형성**했다.)
> Between the Posts: **"In defensive phases, Neto was often pushed up into the midfield line to stay close to Calafiori… This left Acheampong as the one who would play against Tzolis on the left, and Chelsea therefore found themselves in 4-4-2-like variations."**
> (수비 국면에서 **네투는 칼라피오리에 붙어 있으려고 자주 미드필드 라인으로 밀려 올라갔다**… 이것이 **아체암퐁을 좌측에서 촐리스를 상대하는 사람**으로 남겼고, 그래서 첼시는 **4-4-2 변형**에 놓였다.)

⇒ **완전한 4-4-2 형성 메커니즘**(D+2는 조각만 갖고 있었다):
`네투 ↑ 미드필드 라인(칼라피오리 추종) + 하토 ↓ 수비 라인 + 아체암퐁 → 우측 풀백 역할(촐리스 담당) + 로저스 ↓ 좌측(화이트 추적)`
⇒ 명목 3-4-2-1이 **무공에서 4-4-2로 접힌다**. **실측 하토 avg_x 39.0의 원인이 이것이다.**

**⭐ 아체암퐁 avg_x 50.0의 원인도 이중이었다** — D+2는 온볼 측면만 봤다.
> Between the Posts(온볼): **"the very active forward movements of Acheampong down the right side, often underlapping Neto who held the width on the right."**
> (**아체암퐁의 매우 활발한 우측 전진 움직임**, 폭을 유지한 **네투를 자주 언더랩**했다.)
> Between the Posts(무공): **"This left Acheampong as the one who would play against Tzolis."**
⇒ **온볼에서는 네투를 언더랩하는 전진 CB, 무공에서는 촐리스를 맡는 우측 풀백.** 두 국면 모두 그를 앞에 둔다.
D+2 정정 ②(「얕음」이 아니라 「전진」)를 유지하면서 **무공 층위를 추가**한다.
🇫🇷 HommeDuMatch(6): *"un match correct en défense, bien que discret dans la construction du jeu"*(수비는 무난, **빌드업에서는 조용**) — 터치 21회와 정합.

### ⭐ 60분 교체(하토→차바리아 · 라비아→귀스토)의 **전술적 의도** — D+2 「1차 소스 0건」에서 진전

감독 직접 발언은 **여전히 0건**이다. 그러나 전술 분석 2건이 **구조적 의도**를 서술한다.

> Between the Posts: **"Gusto became part of Chelsea's right-sided rotations allowing James to take a more consistently deeper role, while Chavarría played on the outside of Rogers as wing-back."**
> (**귀스토가 첼시의 우측 로테이션에 합류**해 **제임스가 더 일관되게 낮은 역할**을 맡을 수 있게 했고, **차바리아는 로저스 바깥에서 윙백으로** 뛰었다.)
> ReadChelsea: **"Chelsea improved following the changes. Cole Palmer began finding more room between Arsenal's lines."**
> (교체 뒤 첼시는 나아졌다. **파머가 아스날의 라인 사이에서 더 많은 공간을 찾기 시작했다**.)

⇒ **의도 재구성**: ⑴ 제임스를 **피벗에 낮게 고정**(우측 전진 임무를 귀스토에게 이관) ⑵ 좌측에 **진짜 윙백을 배치해
로저스를 앞에 풀어줌**. D+2가 확보한 공식 사유 「중원 통제 회복」과 모순되지 않고 **같은 것의 구조적 서술**이다.
⭐ 🇪🇸 relevo의 차바리아 프로필(08-27)이 이 배치의 배경을 준다:
> **"En ese tablero de ajedrez dinámico que suelen ser sus equipos, los carrileros no actúan solo como defensores de banda, sino como auténticos elementos tácticos encargados de estirar la anchura del campo."**
> (그의 팀이 늘 그렇듯 역동적인 체스판에서, **카리예로(윙백)는 측면 수비수로만 기능하지 않고 경기장의 폭을 늘리는 진짜 전술적 요소**다.)
⇒ ⭐ **알론소 체제의 명시된 모델에서 윙백은 폭을 담당한다.** 그렇다면 **하토의 avg_x 39.0(수비 라인 합류)은 모델의 실행이 아니라 모델로부터의 이탈**이고,
60분 교체는 **그 이탈을 되돌리려는 조치**로 읽힌다. ⚠️ relevo 기사는 **경기 전 영입 프로필**이라 이 경기 분석이 아니다 — 배경 근거로만 쓴다.

**⚠️ 라비아 교체 논점(D+2 미해결)에 진전.** 🇫🇷 HommeDuMatch가 라비아에게 **6.5**를 주며
*"A été efficace dans la récupération du ballon"*(볼 회수에서 효율적이었다)고 평했다.
⇒ **매체 2곳(SI 「기이한 선택」 · HommeDuMatch 6.5)이 라비아를 긍정 평가**하고, 「40분 만에 방전」은 **3티어 팬 채널 단독**이다.
⇒ 「체력설 ↔ 기이한 선택」의 대칭 대립을 **「체력설은 3티어 단독, 2티어 이상은 반대」로 비대칭화**한다. 확정은 아니다.

### 상대팀(아스날) 관점 — D+2 대비 실질 증분

D+2는 Arseblog·Yardbarker뿐이었고 The Athletic은 0건이었다. **전용 아스날 매체와 전술 블로그가 붙었다.**

> ReadArsenal, 아르테타 회견(외데고르에 대해): 자신감이 **"one of the highest I have seen him"**이고
> 결장이 길었던 만큼 **"a point to prove"**(증명할 것이 있다)가 있다.
> ⭐ Squawka 실측 인용: 외데고르 **77분 · 65터치 · 패스 48/54 · 라인브레이킹 패스 16 · 파이널서드 패스 6 · 찬스 창출 4 · 빅찬스 창출 2 · 볼 탈취 3 · 1골**.

> Between the Posts: **"In many of Arsenal's second-half possession phases, Ødegaard was playing a deeper role compared to the first half. He also had plenty of positional freedom to drop into Arsenal's second line and provide connections in buildup."**
> (아스날의 후반 점유 국면 다수에서 **외데고르는 전반보다 더 낮은 역할**을 했다. **2선으로 내려와 빌드업 연결을 제공**할 위치 자유도 충분했다.)

> Between the Posts: **"White had the freedom to rotate with Saka and Ødegaard in a right-sided triangle, while Havertz also often drifted into this area. Arsenal's movement around the edges of the box on this side was excellent."**
> (**화이트가 사카·외데고르와 우측 삼각형에서 로테이션**할 자유가 있었고, 하베르츠도 자주 이 지역으로 흘러들었다. **이쪽 박스 모서리 주변의 아스날 움직임은 탁월**했다.)

⇒ **첼시 좌측(하토·로저스)에 걸린 부하는 「하베르츠 한 명의 이동」이 아니라 「화이트·사카·외데고르·하베르츠 4인의 우측 삼각 로테이션」**이다.
D+2의 「알론소가 말한 왼쪽 오버로드」에 **구성원과 메커니즘**이 붙었다.

**⭐⭐ 라운드를 가로지르는 형질 — 「박스 모서리 조합 플레이」에 대한 취약** (item ⑤와 별개 축의 독립 증거)
> Between the Posts: **"The ease with which opponents are able to get into the penalty box with combination play around the corners of the box also cost Chelsea a goal against Fulham. It seems to be a key area of concern for Alonso's team at the moment."**
> (상대가 **박스 모서리 주변 조합 플레이로 페널티 박스에 들어오는 용이함**이 **풀럼전에서도 첼시에 실점을 안겼다**. 현재 알론소 팀의 **핵심 우려 영역**으로 보인다.)
⇒ Football Made Simple과 **완전히 독립된 소스**가, **다른 축으로**, **같은 라운드 교차 반복**을 지적한다.
⇒ **체제 형질 후보 2호**: 「박스 모서리(하프스페이스 코너) 조합 방어 취약」. 풀럼전·아스날전 2경기.

### ⛔⛔ 날짜·시즌 혼입 함정 — **이번 회차에도 1건 적발**(obs#522 유형 재발, 두 번째)

WebSearch가 상위에 올린 **soccerway "The Regista: Chelsea vs Arsenal tactical review — Palmer promising but Blues let lead slip"**를
파머 역할 근거로 채택할 뻔했다. WebFetch로 1차 확인한 결과:

| 지표 | 이 경기 | soccerway 기사 |
|---|---|---|
| 스코어 | Arsenal **2-1** Chelsea | **2-2** 무승부 |
| 첼시 감독 | 사비 알론소 | **마우리시오 포체티노** |
| 득점자 | 로저스 / 하베르츠·외데고르 | 파머(PK)·**무드리크** / 트로사르 |
| 로저스 언급 | 선제골 | **0회**(존재하지 않는 선수) |
| 파머 역할 | 우측 하프스페이스 하강 | **false 9** |

⇒ ⛔ **배제.** 제목의 「Chelsea vs Arsenal tactical review」와 「Palmer」만 보면 이 경기와 구별되지 않는다.
⭐ **이번에 작동한 지표는 obs#522와 동일하다 — 본문에 병기된 사건의 정합성**(감독 이름·득점자·스코어).
특히 **무드리크·포체티노**라는 **이 체제에 존재할 수 없는 고유명사**가 즉시 판별을 줬다.
⇒ **규약 보강**: 전술 리뷰를 채택하기 전 **「이 체제에 존재할 수 없는 고유명사」를 본문에서 먼저 검색**한다
(감독·이적한 선수·직전 시즌 주전). 티어·URL·검색 순위보다 빠르고 확실하다.

**부수 정합성 검증 통과 지표**(이번 회차에 채택한 소스 전부에 적용):
🇳🇱 vi.nl 순위표 `ARS 3경기 9점 · CHE 4위 6점 8득7실` · marca `콜리더 9점, 첼시 4위 6점` ·
Chelsea FC Online `첼시 4위, 아스날 9점` — **모두 26/27 3라운드와 일치**. 3개 언어권에서 교차 확인했다.
⚠️ 🇳🇱 vi.nl이 **"voor het tweede seizoen op een rij met 2-1 gewonnen"**(**2시즌 연속** 2-1 승리)라고 명시한다 —
obs#522의 함정 구조(같은 대진·같은 스코어의 시즌 반복)를 **네덜란드 매체가 직접 증언**한다.

### 신규 사실 (분류 외)

- ⭐ 🇳🇱 vi.nl: **"Nog nooit slaagde een Premier League-club erin om in de eerste drie wedstrijden van het seizoen binnen vijf minuten te scoren."**
  (프리미어리그 역사상 어느 클럽도 **시즌 첫 3경기에서 모두 5분 이내에 득점**한 적이 없었다.)
  ⇒ 알론소 첼시의 「빠른 시작」은 인상이 아니라 **리그 사상 최초 기록**이다. 1' 풀럼 · 4' 브라이턴 · 2' 아스날.
  **obs#525(설계된 압박 가변성)와 함께 「초반 능동성」을 체제 형질로 볼 근거가 된다.**
- 🇳🇱 vi.nl: 첼시의 마지막 아스날전 승리는 **2019-12-29**.
- ⭐ 🇵🇹/🇧🇷: **에스테방이 10번을 원하지만 그 자리에 파머와 로저스가 있어** 윙어로밖에 출전 기회가 없다는 것이
  포르투갈어권의 반복 독법이다. D+2의 「3경기 연속 벤치」에 **구조적 이유**가 붙는다 — 슬롯 경합이지 폼 문제가 아니다.
- 🇪🇸 marca: 아르테타와 알론소는 **안티구오코**(산세바스티안)에서 함께 시작했고 선수로 7번 맞붙어 **알론소가 3승 2무 2패 우세**.
  이 경기가 **감독으로서 첫 대결**이다. ⭐ 🇪🇸 sport.es는 **이라올라도 같은 안티구오코 출신**임을 덧붙인다
  (이 프로젝트의 3개 감독 축이 한 유소년 클럽에서 갈라져 나왔다).
- Arsenal 교체(tacticalfootballanalysis): 66' 칼라피오리→인카피에 · 루이스-스켈리→수비멘디 / 76' 외데고르→메리노 · 하베르츠→교케레시 / 90' 사카→마두에케.
- ⭐ **D+2 충돌 #2(교체 시각) 해소**: tacticalfootballanalysis가 **네투 OUT 81'(→에스테방) · 로저스 OUT 87'(→웰벡)**로
  실측·AOL·dgabc와 **일치**한다. ⇒ **chelseafc.com 공식 리포트가 틀렸다**는 D+2 판정이 4번째 소스로 확증됐다.
  신규: 로저스의 교체 투입 상대는 **대니 웰벡**이다.
- 취소골(11~12') 상세: **라이스 프리킥 → 가브리엘 포스트 강타 → 리바운드 칼라피오리 득점 → 콘사 오프사이드로 취소**(🇳🇱 vi.nl·ReadChelsea 일치).
  ⇒ D+2·당일 절이 「칼라피오리 취소골」로만 적은 것에 **원인(콘사 오프사이드)과 경로**가 붙었다.

### 🇫🇷 프랑스어 — 이 경기 첫 1차 소스 (D+2는 0건이었다)

HommeDuMatch 전 선수 평점(09-07). D+2가 「L'Équipe·RMC 0건, Foot Mercato는 스탯만」으로 닫은 축이 열렸다.

| 첼시 | 평점 | 요지 |
|---|---|---|
| 마르티네스 | **7** | 8세이브, 예외적 경기 |
| 아체암퐁 | 6 | 수비 무난, **빌드업에서 조용** |
| 라크루아 | 6 | 듀얼에서 용감히 싸웠으나 **경고** |
| 포파나 | **6.5** | **수비적으로 가장 활동적** — 인터셉트·듀얼 승 다수 |
| 네투 | 6.5 | (→에스테방 6.5, 유효슛 1) |
| 라비아 | **6.5** | **볼 회수에서 효율적** (→귀스토 6) |
| 제임스 | 6.5 | 공격 가담 시도, 수비적으로도 엄정 |
| 하토 | 6.5 | 초반 빠른 어시스트 (→차바리아 6) |
| 파머 | **6** | 여러 차례 시도했으나 **정확성 부족**, **경고** |
| 로저스 | **7** | 선제골, 위협적 (→웰벡 6) |
| 주앙 페드루 | 6.5 | **피파울 6회로 상대 수비를 압박**, 지연 경고 |

⭐ **포파나가 첼시 수비 최고 평가**인 것은 D+2가 다루지 않은 축이다(D+2는 라크루아·아체암퐁 중심).
⭐ **파머 6 + 경고**는 영어권 5~6.5 혹평과 일치 — **4개 언어권이 파머에 대해 수렴**한다.

### 0건과 미해소 (D+3)

| 항목 | 결과 | 시도한 것 |
|---|---|---|
| 🇩🇪 독일어 | **0건 유지 (3회 연속)** | `Havertz Arsenal Chelsea Tor Analyse Xabi Alonso Taktik September 2026 kicker` — 반환된 것은 전부 영어 소스의 독일어 요약이고 **독일어 1차 매체 URL은 0건**. kicker·Sky DE 이 경기 자료 없음 확인 |
| 🇪🇸 elpais.com | **0건** | 브라우저로 `elpais.com/deportes/futbol/` 직접 훑음 — 첼시·아스날·알론소 링크 **0개** |
| 🇪🇸 mundodeportivo.com | ⛔ **브라우저 정책 차단** | 이 환경에서 열 수 없음 — 미해소로 이월 |
| 🇺🇾 elobservador.com.uy | ⛔ **미해소** | 브라우저 2회 시도, **Cloudflare 봇 검증 페이지**에서 정지. CAPTCHA 우회는 하지 않는다 ⇒ **「마르티네스의 중대한 실책」 원문 미확보** (단 책임 논점 자체는 위에서 다른 6개 소스로 진전시켰다) |
| 🇧🇷 portaldemocrata.com.br | ⛔ **사이트 장애** | 403이 아니라 `Erro ao estabelecer uma conexão com o banco de dados`(DB 연결 실패) |
| 🇵🇹 observador.pt · mundiario.com | **미시도** | 우선순위에서 밀림 — 페이월(402)·403이라 기대 수익 낮다고 판단 |
| 유튜브 전사 | ⛔ **HTTP 429 지속** | `yt-dlp` 자막 다운로드가 **4회 연속 429**(45초·20초 백오프 포함). `--list-subs`는 통과하므로 **자막 엔드포인트 한정 레이트리밋**이다. json3 폴백도 동일 429 |
| The Athletic 아스날 담당 | **0건 유지** | 검색 미노출 |
| 파머의 「와이드 수비 부하」 | **미해결** | 로저스 축은 닫혔으나 파머 축은 **소스가 정반대**(FMS 부정 ↔ ReadChelsea 긍정, 둘 다 풀럼전) |

**⭐ 다음 회차용 유튜브 후보**(사이트 내부 검색으로 확보한 ID, 전사 미완):
`eSNTV-2ve64`(Arsenal 2–1 Chelsea: The Champions' Response — ⚠️ **자막 없음 확인**, 재시도 무의미) ·
`k9YZDKQxsZI`(Arsenal have CHANGED — en·es 자막 있음) · `ZjSmghKwDgU`(알론소 회견, 엔소·로저스·카이세도 — en·es 자막 있음) ·
`9AU-TEjgIGg`(Arsenal swarm vs Chelsea trident — en·es 자막 있음) · `-53yKbte__k`(사비 알론소는 왜 공을 소유하려 하지 않는가).

### D+3 회차 DB 반영

| 테이블 | 내용 |
|---|---|
| `observations` | **신규 10건 (#557~566)** — ㉗ 선제골 형태 확정·가짜충돌 규약 · ㉘ 파머·로저스 무공 역할이 압박높이의 함수(D+2 「대칭」 정정) · ㉙ 공격 국면 비대칭 분담 · ㉚ 와이드수비 부하는 로저스 축(독립 2건) · ㉛ 카이세도 확정 + 더블피벗은 비상구성 · ㉜ 결승골 사슬 완성(하베르츠 더미) · ㉝ 마르티네스 책임 구조우위 · ㉞ 백4 형성 메커니즘 1차근거 · ㉟ 박스모서리 취약 = 체제형질 2호 · ㊱ ⛔ 날짜혼입 2번째 적발 + 고유명사 판별 규약 |
| `player_duties` | **8행 addendum**(`[2026-09-09 D+3 추가]` prefix, 덮어쓰기 없음) — 파머 66 · 로저스 91 · 아체암퐁 32 · 하토 62 · 네투 65 · 제임스 68 · 마르티네스 193 · 에스테방 69 |

⛔ **당일 절·D+2 절·실측·`match_game_setups`·`prescriptions`·`match_player_prescriptions`는 고치지 않았다.**
단일 경기이고 커널 Δ 산출을 하지 않았으므로 처방 변경 근거가 아니다.

### D+4 이후로 넘기는 것

1. **파머의 무공 와이드 부하** — 소스가 정면 충돌(같은 풀럼전에 대해 FMS 부정 ↔ ReadChelsea 긍정). 제3의 1차 소스 필요.
2. **유튜브 전사 4편**(위 ID 목록) — 429 해소 후 재시도. 특히 `-53yKbte__k`(알론소의 점유 회피)는 **체제 철학 축**이다.
3. 🇪🇸 mundodeportivo(정책 차단) · 🇺🇾 elobservador(Cloudflare) — **다른 경로 필요**.
4. **「좌측 인사이드 포워드가 상대 우측 풀백을 추적하는 부하」가 다른 상대에게도 재현되는가** — 체제 형질 승격 조건.
5. **「박스 모서리 조합 방어 취약」(체제 형질 2호)** — 현재 2경기(풀럼·아스날). 3경기째 확인 필요.
6. **카이세도 복귀 후 피벗 구성** — 이 경기 더블 피벗이 비상 구성으로 확정된 이상, **정본 피벗은 아직 실측된 적이 없다.**
