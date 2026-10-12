# 2026-10-10 AVL vs Brentford — 2-2

> 수집일 2026-10-11 · SofaScore event `16363872` · 프리미어리그 6R · 홈(Villa Park) · 기본 포메이션 4-2-3-1 (상대 4-2-3-1)
> FotMob matchId `5795466` · WhoScored matchId `1983592`(Opta · scope=full · 이벤트 1,458건)
> ⭐ 이 회차는 **사용자 라이브 시청 관찰 18건**(obs#963~980)을 실측과 대조했다 — 「현장 관찰 대조」 절(§4-1) 참조.

## 1. 경기 개요와 원천 수치

| 항목 | AVL | BRE |
|---|---|---|
| 점유 | 52% (1H 50 · 2H 54) | 48% |
| xG (FotMob = SofaScore) | **1.76** (오픈플레이 1.72 · 세트 0.05) | 1.25 (오픈플레이 1.04 · 세트 0.21) |
| xGOT | 2.25 | 0.56 |
| 슈팅 / 유효 / 블록 | 20 / 7 / 7 | 14 / 4 / 3 |
| 빅찬스 | 2 | 2 |
| 패스 (정확) | 407 (321 · 79%) | 358 (284 · 79%) |
| 롱볼 | 26/61 (43%) | 17/39 (44%) |
| 크로스 | **0/4** | 5/18 |
| 경합 · 공중볼 | 56% · 20/36 | 44% · 16/36 |
| 파울 · 경고 | 7 · 2 | **24 · 5** |
| PPDA (WhoScored) | **11.2** (280/25) | 6.68 (294/44) |
| def_x (라인 높이 프록시) | **34.9** (n=185) | 42.8 (n=179) |
| 실점으로 이어진 실수 | **1** (9′ 밍스) | 0 |
| GK 실점 방지(SofaScore goals prevented) | 스즈키 **−1.44** | 켈러허 +0.25 |

**하프별** (FotMob 동일 스냅샷): 1H xG **1.24 – 0.53** · 슈팅 10–5 / 2H xG **0.52 – 0.72** · 슈팅 10–9. 전반 우세 → 후반 역전된 흐름.

**타임라인** (SofaScore incidents)
- 10′ 야르몰류크 0-1 — 9′ 빌드업 중 **밍스 패스 실수(Opta `Error`)** → 샤데 회수 → 티아구 → 린델뢰프 걷어내기 → 야르몰류크
- 12′ **잭슨 1-1**
- 45+3′ 부엔디아 경고
- 46′ **루제리 → 완비사카(LB) — SofaScore `incidentClass=injury`(부상 교체)**
- 64′ 부엔디아 → 음바예
- 72′ 캐시 경고
- 77′ **맥긴 2-1 (도움 만잠비)**
- 79′ 아예르 2-2 — 켈러허 롱볼부터 이어진 브렌트포드 왼쪽(빌라 오른쪽) 전개, 앤서니 크로스
- 86′ **만잠비 → 알리송 · 고메스 → 바클리**

**수집 한계**: SofaScore 히트맵은 **터치 기반**이다(docs/50) — 공 없는 위치(오프더볼)는 덜 잡힌다. 교체 출전 4명은 hp 9~33으로 짧은 표본(대표 히트맵 기준 hp15 미달: 바클리 9·알리송 10).

## 2. 전술 설명

### 점유 구조·빌드업
- **GK가 빌드업의 3번째 패서**: 스즈키 패스 46개(WhoScored) — 캐시 51·밍스 47에 이어 팀 3위. 평균 출발 x 9.8, 박스 밖에서 시작한 패스 7개.
- **첫 실점이 이 구조에서 나왔다**: 9′ 스즈키 → 밍스 → 밍스의 박스 앞 패스가 끊김(x18) → 10′ 실점. 「짧게 시작하는 빌드업 + 높은 GK 관여」의 비용이 직접 드러난 장면.
- **피벗 비대칭(현장 관찰 obs#965)**: 고메스 터치 평균 x 45.8(0~64′)로 카마라 43.2보다 2.6 높고 왼쪽(y 61.9 vs 38.1). 단일 경기 적합 **dm_dlp/Roaming .875(Δ.154)** — 오늘 바꾼 정본 LDM과 일치. ⚠️ 「2선 높이」는 터치 평균상으론 아니다(2선 x 56~66) — 터치 기반 한계를 감안.

### 비점유 구조·압박
- PPDA 11.2 · def_x 34.9 — 직전 토트넘전(13.24 · 30.6)보다 약간 높고 적극적이지만 여전히 중·저블록. 브렌트포드는 PPDA 6.68로 훨씬 강하게 압박했다.
- **잭슨의 압박(obs#963)**: 단일 경기 적합 **st_advanced/Support .516(Δ.146 · 2위 포처 Versatile .370)** — EA 정의상 Support의 강화 특성이 「압박」이다. 터치 평균 y 59.5로 왼쪽 쏠림(0~64′) 재현.

### 전환·rest-defense·세트피스
- 두 번째 실점(79′)은 켈러허 롱볼 → 카요데 → 디우프(빌라 오른쪽 측면 y94) → 앤서니 → 아예르로 **빌라 오른쪽**을 따라 내려왔다. 64~86′ 구간 맥긴(y 34.7)·음바예(y 35.7)가 **둘 다 오른쪽에 몰려 있던** 시점이다(WhoScored 터치 평균).
- 세트피스 xG 0.05 대 0.21.

## 3. 전술적 특성
- **강점**: 전반 xG 1.24로 전반 장악 · 만잠비 키패스 3·도움 1 · 맥긴 평점 8.2(골 1·키패스 2) · 잭슨 8.1.
- **취약점**: ⑴ 짧은 빌드업 실수 실점(9′) ⑵ 크로스 0/4 — 측면 마무리 루트 부재 ⑶ 후반 xG 역전(0.52–0.72) ⑷ 스즈키 goals prevented −1.44.
- **직전 경기와 다른 점**: 토트넘 원정은 점유 36%의 저블록 역습이었고, 이 경기는 점유 52%로 공을 더 쥐었다.

## 4. 경기 중 변화

1. 0′~10′: 0-0 → 9′ 빌드업 실수 실점.
2. 12′ 잭슨 동점 — 이후 전반 내내 우세(전반 xG 1.24).
3. 46′ 루제리 부상 교체 — **완비사카를 왼쪽 풀백**으로(본래 RB). 터치 평균 y 84.5(왼쪽)로 실제 왼쪽 수행. 단일 경기 적합 fb_att_wb/Support .791 — 루제리 fb_wingback/Balanced .920보다 전진형.
4. 64′ 부엔디아 → 음바예: 2선 재배치. 77′ 맥긴 득점(도움 만잠비).
5. 79′ 실점 후 86′ 만잠비 → 알리송 · 고메스 → 바클리.

### 4-1. ⭐ 현장 관찰 대조 (사용자 라이브 시청 18건 → 실측)

| obs | 관찰 | 실측 대조 | 판정 |
|---|---|---|---|
| #963 | 잭슨 압박 많음 · 왼쪽 이탈 | st_advanced/Support .516 Δ.146 · 0~64′ 터치 y 59.5(왼쪽) | ✅ 일치 |
| #964 | 만잠비 반응형 측면 교환 → 플레이메이커 Roaming | cam_playmaker/Roaming .751 Δ.106(하프윙어 .560) | ✅ 일치 |
| #965 | 고메스 LDM 높은 위치 · 카마라 아래 | dm_dlp/Roaming .875 Δ.154 · 고메스 x +2.6 · 좌측 | ✅ 역할 일치 · ⚠️ 「2선 높이」는 터치 평균상 미확인 |
| #966·#975 | 스즈키 높은 빌드업 · 박스 밖 러시 | 패스 46(팀 3위) · KeeperSweeper 2회(80′ x19 · **96′ x47**) · 박스 밖 회수 2회(2′·6′) · 히트맵 적합은 gk_goalkeeper/Defend .939 | ✅ 이벤트로 일치 — 히트맵(위치)은 박스 안 중심이라 희소 행동을 못 담는다 |
| #967 | 루제리 HT 교체 사유 미상 | **SofaScore 부상 교체** | ✅ 사유 확정(부상) |
| #968·#971·#974 | 2선 3인(만잠비·맥긴·음바예) 순환 | 64~86′ 터치 평균: 만잠비 y52(중앙) · 맥긴 34.7 · 음바예 35.7(둘 다 오른쪽 안쪽) | ⚠️ 평균은 순환을 지운다 — 장면 단위는 영상 확인 필요 |
| #969·#970 | 음바예 안쪽 이동 · Balanced 추정 | wm_insidefwd/Attack .444 > Balanced .350(hp21 · 26′) | ⚠️ 역할(IF)은 일치 · 포커스는 실측이 Attack 쪽(짧은 표본) |
| #972 | 맥긴 IF 느낌 | wm_winger/Attack .772(IF Balanced .528) · 터치 y 22.2(0~64′, 오른쪽) | ❌ 실측은 윙어 — 득점 장면의 안쪽 침투는 순간 행동일 수 있음 |
| #973 | 맥긴 만잠비 합류 후 안쪽 증가 가설 | 이 경기 5열(터치라인) **.52** — 만잠비 없던 경기 평균 .51과 같음 | ⚠️ 반대 방향 1건 · 판정 보류 유지 |
| #976 | 바클리 → 고메스 자리 | 86′ 고메스 → 바클리 확인 | ✅ |
| #977 | 에메리 자리별 역할 고정 | LDM 고메스 dlp Roaming .875 · 바클리 hp9로 판정 불가 | 정황 유지 |
| #978 | 알리송 투입 후 알리송 우 · 맥긴 중 · **만잠비 좌** | ⛔ **알리송은 86′ 만잠비 대신 투입** — 86′ 이후 터치 평균: 알리송 y20(오른쪽) · 맥긴 45(중앙) · **음바예 y86(왼쪽)** | ⛔ 충돌 — 왼쪽은 만잠비가 아니라 **음바예**(실측 채택 · 불변규칙 3) |
| #979 | 알리송 윙어 가설 검증 계획 | 86′ 이후 잭슨 터치 x 50.6·y 54(중앙·깊게 · n=4) | 표본 4로 판정 불가 |
| #980 | 알리송 오프더볼 안쪽 · 캐리는 윙어 | 단일 경기 적합 wm_wideplm/Attack .732 > IF Balanced .683 > winger .502 (hp10 무효) | 판정 불가(표본) |

## 5. 선수별 분석 — 출전 선수 전원

| 선수 | 위치·실제 역할(단일 경기 적합 1위 · Δ) | 분/평점·핵심 스탯 | 평균 위치(SofaScore)·히트맵 | 특성·수행 | FC 역할/포커스 함의 |
|---|---|---|---|---|---|
| 스즈키 | GK · gk_goalkeeper/Defend .939 (Δ.008 무결정 · 2위 Balanced) | 90′ 5.8 · 패스 26/42 · 세이브 3 · 회수 8 · 걷어내기 5 · goals prevented −1.44 | (10.6, 51.4) · hp67 | 빌드업 3번째 패서 · 스위퍼 액션 2회(96′ x47) | 히트맵은 Defend, 이벤트는 Build-Up+러시 — **GK 정본 재결정 사안**(§7) |
| 캐시 | RB · fb_att_wb/Support .895 (Δ.004 무결정 · 2위 fb_wingback/Balanced) | 90′ 6.6 · 패스 35/40 · 태클 5 · 경고 72′ | (46.2, 12.6) · hp74 | 우측 전진·수비 겸장, WhoScored 패스 1위(51) | 시즌 정본 fb_wingback/Balanced와 무결정 동률 — 유지 |
| 린델뢰프 | RCB · cb_bpd/Aggressive .857 (Δ.029 무결정) | 90′ 6.9 · 패스 41/46 · 걷어내기 13 | (28.3, 31.1) · hp73 | 걷어내기 13으로 후방 정리 | 정본 유지 |
| 밍스 | LCB · cb_bpd/Aggressive .905 (Δ.001 무결정 · 2위 Build-Up .904) | 90′ 6.0 · 패스 36/47 · **9′ 실점 이어진 실수** | (33.7, 65.1) · hp67 | 패스량 팀 1위(SofaScore 47) | 정본 유지 · 빌드업 실수 1건 기록 |
| 루제리 | LB · fb_wingback/Balanced .920 (Δ.064) | 45′ 6.4 · 패스 11/13 · 키패스 1 | (35.8, 86.0) · hp28 | **부상으로 HT 교체** | 시즌 measured 갱신(n 3) — fb_wingback/Balanced .899 |
| 완비사카 | LB(본래 RB) · fb_att_wb/Support .791 (Δ.040 무결정) | 45′ 6.6 · 태클 2 · 인터셉트 1 | (44.6, 82.4) · hp33 | 반대발 왼쪽 수행, 루제리보다 전진 | 교체 표본 — 시즌 집계 제외 |
| 카마라 | RDM · dm_dlp/Roaming .636 (Δ.021 무결정 · 2위 dm_dlp/Build-Up) | 90′ **7.3** · 패스 36/44 · 키패스 1 · 경합 9-4 | (46.5, 34.3) · hp81 | 앵커 · 경합 우위 | 정본 RDM holding/Defend 유지(적합도 낮고 무결정) |
| 고메스 | LDM · **dm_dlp/Roaming .875 (Δ.154)** | 86′ 6.9 · 패스 36/40 | (44.6, 55.0) · hp62 | 좌측 피벗, 카마라보다 약간 높음 | **오늘 바꾼 정본과 일치** · 시즌 measured argmax도 dm_dlp/Roaming(.812)으로 변경 |
| 맥긴 | RM · wm_winger/Attack .772 (Δ.048 무결정 · 2위 winger/Balanced) | 90′ **8.2** · **골 77′** · 키패스 2 · 슈팅 3/3 | (58.3, 26.1) · RAM · hp56 | 득점 · 경합 7-6 | 정본 RM wm_winger/Attack과 일치 — 「IF 느낌」(obs#972)은 실측과 불일치 |
| 만잠비 | CAM · **cam_playmaker/Roaming .751 (Δ.106)** | 86′ 7.1 · **도움 77′** · 키패스 3 · 슈팅 1/7 · 패스 20/21 | (63.8, 51.6) · hp49 | 반응형 이동 · 슈팅 7개(팀 최다) | 정본 CAM과 일치 — 중거리 슛 성향(박스 밖) 재확인 |
| 부엔디아 | LM · wm_insidefwd/Balanced .625 (Δ.009 무결정 · 2위 wm_widemid/Defend) | 64′ 6.3 · 키패스 2 · 슈팅 0/4 · 태클 3 · 경고 | (52.7, 68.4) · LAM · hp61 | 안쪽형(윙어 .223) | 정본 LM wm_widemid/Support와 무결정권 — 유지 |
| 잭슨 | ST · **st_advanced/Support .516 (Δ.146)** | 90′ **8.1** · **골 12′** · 키패스 2 · 경합 5-8 | (63.5, 57.3) · LAM으로 분류 · hp43 | 압박·왼쪽 이탈 | ST 정본(st_advanced/Versatile)과 다름 — **잭슨 선발 시 Support**가 실측·관찰 모두 지지 |
| 음바예 | LM(교체) · wm_insidefwd/Attack .444 (Δ.094 · hp21) | 26′ 6.9 · 키패스 1 · 슈팅 1/1 | (64.4, 51.1) · hp21 | 안쪽으로 이동 | 교체 표본 — IF 계열 확인, 포커스 미확정 |
| 바클리 | LDM(교체) · dm_holding/Ball-Winning .583 (hp9 무효) | 11′ 6.7 · 패스 7/7 · 키패스 1 | (40.8, 57.7) · hp9 | 고메스 자리 직행 | 기록만 |
| 알리송 | RM(교체) · wm_wideplm/Attack .732 (hp10 무효) | 11′ 6.4 | (72.8, 21.2) · hp10 | 오른쪽 높게 | 기록만 |

**맥긴 터치라인 비중(obs#973 표본 +1)**: 이 경기 5열(오른쪽 터치라인) 비중 **0.52**(열 분포 .02·.07·.12·.27·.52). 만잠비 **선발** 경기인데 만잠비 없던 26/27 5경기 평균(.51)과 같다 — 「만잠비 합류 후 안쪽 증가」 가설에 **반대 방향 1건**. 만잠비 동반 표본은 4경기(선발 2)로 늘었고 평균 .42. 판정 보류 유지.

## 6. 전술 변화 판정
- **유지**: 4-2-3-1 · 피벗 비대칭(카마라 앵커) · 우측 맥긴 윙어형 · CAM 플레이메이커 Roaming.
- **새로 나타난 것**: ⑴ 루제리 부상 → 완비사카 왼쪽 풀백 ⑵ 음바예 투입 후 2선 순환(현장 관찰) ⑶ GK 빌드업·스위핑 비중.
- **정본 반영(같은 회차 · 사용자 결정 2026-10-11)**: LDM dm_holding/Roaming → **dm_dlp/Roaming**(이 경기 고메스 .875가 추가 지지) · GK gk_goalkeeper/Defend → gk_ballplaying/Build-Up(**재결정 대기** — §7).
- **profile 갱신**: `manager_profiles` buildup·implementation 축에 덧붙임(§9).

## 7. 게임 구현 판정

- 결론: **추가 관찰** — 단, 두 칸은 이번 회차에 정본 근거가 모였다(LDM 반영 완료 · ST 잭슨 선발 시 Support).
- **이 경기 전용 팀 설정**: FC26 / 4-2-3-1 Wide / 빌드업 **Counter** / 수비 접근 **Balanced** / 라인 **55** / tactic_code 없음.
  `core.team_settings.suggest(52, 407, 61, 11.2)` → Counter / Balanced / 55~62(롱볼 15.0%) — **규칙 그대로**(rule_note=RULE). 라인은 def_x 34.9로 하단 55.
- **이 경기 선발 11명**: `match_player_prescriptions` 11행 + 교체 4행(단일 경기 적합 1위를 쓴다. Δ≤.05는 「실측 무결정」 명기).
- **GK 정본 재결정 근거(사용자 판단 대기)**: 이벤트상 스위퍼 행동 2회(하나는 하프라인 근처 x47) + 빌드업 패스 팀 3위 → **gk_sweeper/Build-Up**이 관찰·이벤트 모두에 맞는다. 히트맵(위치)은 박스 안 중심이라 희소 행동을 반영하지 못한다(gk_sweeper/Build-Up .581 · gk_ballplaying/Build-Up .728 · gk_goalkeeper/Defend .939). ⚠️ 첫 실점이 짧은 빌드업 실수에서 나왔다 — 높은 GK 관여의 비용도 같이 본다.
- **ST**: 잭슨 선발 경기의 실측(.516 Δ.146)과 관찰이 st_advanced/Support로 모인다. 정본 ST(st_advanced/Versatile)는 슬롯 정본이고, **잭슨 선발 시 처방**으로 Support를 쓰는 것이 맞다 — 정본 변경은 사용자 판단.
- `prescriptions` 변경: measured 4행 재집계(맥긴·밍스·루제리·고메스 — 고메스 argmax holding→dlp Roaming · Δ.027 무결정).
- **다음 경기 재검증**: 2선 순환 장면(영상) · 음바예 포커스 · 알리송 국면별 움직임 · 맥긴 터치라인 비중 추이.

⚠️ 이 설정은 `match_game_setups`·`match_player_prescriptions`의 `MATCH ONLY` 프리셋이다.

### 7-1. 재판정 — claim #167 「카마라·고메스 어느 쪽도 배급을 지배하지 않는다」
카마라·고메스 **동시 선발** 경기. 패스량 순위(SofaScore `pass_total` — 이전 회차와 같은 원천):
**밍스 47 · 린델뢰프 46**(CB 듀오 1·2위) · 카마라 44 · 스즈키 42 · 고메스·캐시 40.

| 경기 | 패스량 1·2위 | 카마라·고메스 순위 |
|---|---|---|
| 08-12 슈퍼컵 | 부엔디아·캐시 | 8위·9위 |
| 09-08 UCL | **파우 토레스·린델뢰프(CB)** ✓ | 3위·5위 |
| 09-19 PL | 밍스(CB)·카마라 | 2위·순위 밖 |
| **10-10 PL(이 경기)** | **밍스·린델뢰프(CB)** ✓ | **3위·5위** |

⇒ 「CB 1·2위」가 **2경기째**(조건 3경기 중 2/3 · 패스 집계 가능한 동시 선발 4경기 중 2). **PENDING 유지** — 다음 동시 선발 경기에서 한 번 더 나오면 APPLIED.
⚠️ WhoScored 이벤트 집계로는 캐시 51·밍스 47·스즈키 46·린델뢰프 46으로 순위가 다르다(스로인 등 집계 정의 차이) — 판정은 **이전 회차와 같은 SofaScore** 기준으로 했다.

### 7-2. claim #169 「맥긴이 침투를 놓친다」
이 경기에서 같은 지적은 서사 조사 결과(§8)로 판정한다.

## 8. 영상·기사·감독 발언 (D+0 · 2026-10-11 01:40 KST 기준)

### 8-1. 에메리 경기 후 회견 — **미확보(게시 전)**
종료 45분 뒤 시점에 회견 원문·전사가 아직 없었다(avfc.co.uk·BBC·Birmingham Mail). 구단 공식 「VILLA 2-2 BRENTFORD || POST-MATCH LIVE」(https://www.youtube.com/watch?v=0G-3rgIq77o · 10-10 16:04Z 라이브 · **설명만 확인 · 자막 없음**)에 인터뷰가 들어 있을 가능성이 높다 — **D+1에서 확보**한다. 브렌트퍼드 키스 앤드루스 감독 발언도 동일.

### 8-2. Jacob Tanswell(The Athletic) — Bluesky 26건 (분 = UTC−14:00 · 후반은 45+(UTC−15:03) 추정)
- 경기 전: 에메리는 만잠비가 「to play free」(자유롭게 뛰도록) 해야 한다고 말했다 — **obs#964 플레이메이커 Roaming의 감독 측 근거**.
- ~5′: 「Johan Manzambi largely operating as a right 10 … has freedom to drift across」(만잠비는 주로 오른쪽 10번으로 뛰지만 가로질러 떠다닐 자유가 있다).
- ~14′: 「Brentford's goal had come from them showing the ball to Mings since the first goal kick」(브렌트퍼드의 골은 첫 골킥부터 밍스에게 공을 내주도록 유도한 결과였다) — **9′ 실수는 상대의 설계된 압박 함정**이었다.
- ~21′: 「Brentford's full-backs not comfortable in following Buendia and McGinn when they move inside」(부엔디아·맥긴이 안으로 들어올 때 브렌트퍼드 풀백이 따라가기 불편해한다) — 에메리 원칙 「와이드는 안으로」가 작동한 장면.
- HT: 「not sure if he can do that with Gomes & Kamara, who love duels」(경합을 좋아하는 고메스·카마라로 통제가 가능할지 확신이 없다) — claim #167(배급 비지배)과 같은 방향의 기자 판단.
- ~54′: 「Wan-Bissaka now tasked with providing high width outside of Buendia, which doesn't tend to come naturally」(완비사카는 부엔디아 바깥에서 높은 폭을 대는 임무 — 그에게 자연스럽지 않다) — 실측 fb_att_wb/Support .791과 일치.
- ~63′: 「Matteo Ruggeri has just come out of the tunnel and has some strapping on his left leg. Hamstring area.」(루제리가 왼쪽 다리 햄스트링 부위에 테이핑을 하고 터널에서 나왔다) — SofaScore 부상 교체 분류와 함께 **부상 교체 확정에 가깝다**(공식 진단은 미발표).
- ~68′: 「Manzambi moves to the left, McGinn as the 10, Mbaye on the right」(만잠비 왼쪽, 맥긴 10번, 음바예 오른쪽) — **현장 관찰 obs#968과 정확히 일치**.
- ~74′: 「Manzambi and Jackson finding success when they peel off to the left」(만잠비와 잭슨이 왼쪽으로 빠질 때 성과를 낸다) — obs#963 잭슨 좌측 이탈 확인.
- ~84′: 「#AVFC switch off and don't track Ajer」(빌라가 집중을 놓쳐 아예르를 추적하지 않았다) — 79′ 실점.
- 종료 후: 「Villa not really controlling games this season」(빌라는 이번 시즌 경기를 통제하지 못하고 있다).

### 8-3. 다국어 기사
- 🇯🇵 스즈키 — 게키사카(Yahoo! 재게재): 「ラストプレーでハーフウェーライン付近まで飛び出す好カバー」(라스트 플레이에서 하프라인 부근까지 뛰쳐나간 좋은 커버) · 사커다이제스트: 「間一髪でクリア」(간발의 차로 클리어) — **WhoScored 96′ KeeperSweeper x47과 같은 장면**. obs#975 확인.
- 🇪🇸 EFE 결과 기사(인용 없음) · 🇧🇷 경기 흐름만 · 🇨🇭 만잠비 도움만 · 🇮🇹 루제리 관련 0건.

### 8-4. 팬 채널
- 1874 「MATCH REACTION: Aston Villa v Brentford」(예약 라이브 17:45Z · 제목만) · UTV·The Villans 경기 후 영상 미게시(16:40Z 기준). ⇒ **D+1에서 전사·요약·구현 주장(G17)**.

### 8-5. claim #169 「맥긴이 침투를 놓친다」
이 경기에서 같은 지적은 없다 — 79′ 「don't track Ajer」는 팀 단위 지적이고 맥긴 특정이 아니다. **HELD 유지**(독립 2소스 또는 2경기 누적 조건 불변).

### 8-6. 소스 커버리지
| 소스 | 상태 |
|---|---|
| 감독 회견(양 팀) | ❌ 게시 전 — D+1 |
| Tanswell | ✅ Bluesky 26건 · X 미조회 |
| 팬 채널 3곳 | ❌ 경기 후 영상 게시 전 — D+1 |
| 다국어 기사 | 영 7 · 일 3 · 서 1 · 포 1 · 불 1 · 이 0 · 브렌트퍼드 측 0 |

## 9. 데이터 반영과 한계
- 추가: `matches` 1행(id 115) · `player_matches` 15행(국면 그리드 15행 포함) · `team_match_stats` 1행(xG 4종 FotMob 동일 스냅샷 · PPDA·def_x) · `match_events` 21행 · `match_shots` 34행 · `match_period_stats` 2행.
- 갱신: `prescriptions` measured 4행 재집계(G18).
- 한계: 터치 기반 히트맵 · 교체 4명 짧은 표본 · 2선 순환은 평균 위치가 지운다(영상 필요).

## D+1 추적 (2026-10-11)

> 수집 시각 2026-10-11 KST · 회차: 스케줄 `mw-avl-brentford-d1` · 당일 절(§1~9)은 수정하지 않았다.

### D1-1. 에메리 경기 후 발언 — ✅ 확보(정식 회견 전문은 미확보 · 매체 발췌 + 구단 플래시 인터뷰)
- **루제리 HT 교체 = 햄스트링 부상 확정**: 원문 「Ruggeri is hamstring」(루제리는 햄스트링이다 — Hayters TV, 10-10 19:44, 1차 확인) · 「It's his hamstring. We will check tomorrow.」(햄스트링이다. 내일 검사한다 — RotoWire). PA(Express & Star 등 · **원문 403, 검색 스니펫만**): 일요일 스캔 · 「I will try to keep our structure without our two left-footed full-backs in Maatsen and Ruggeri」(왼발 풀백 마트선·루제리 없이도 구조를 바꾸지 않고 유지하겠다) · 완비사카가 왼쪽 풀백을 이어 맡을 전망. ⇒ §4-1 obs#967 「부상」 판정 **확증**(obs#983).
- **자기 진단 = 통제 부족**(BBC MOTD 발췌, Yahoo 재게재): 「We must try to control the match and structure better with possession and positioning」(점유와 포지셔닝으로 경기와 구조를 더 잘 통제해야 한다) · 「We were sometimes in a hurry and losing the ball」(때때로 서두르다 공을 잃었다) · ESPN/PA: 「We were expecting to try and dominate the ball more than we did」(실제보다 공을 더 지배하길 기대했다) → obs#986. ⚠️ 팀 빌드업 정본 Counter를 바꿀 근거는 아니다(감독 목표 ≠ 이 경기 실측 스타일) — 추가 관찰.
- 구단 플래시 인터뷰(gxU0HMfb3Nk · auto-caption · VAVEL 정리본과 문구 일치): 「more or less I think the result is fair in 90 minutes … we conceded more than I expected」(대체로 결과는 공정, 하지만 기대보다 많이 실점) · 「Nicolas Jackson … understanding everything tactically and everything with his power in our structure better」(잭슨은 자기 힘을 우리 구조 안에서 점점 더 잘 이해하고 있다) · 「like Johan Manzambi – it's his second match playing in the starting 11」(만잠비처럼 선발 두 번째 경기인 선수도 있다).
- ❌ **미확보**: 부엔디아→음바예·알리송·바클리 교체 의도, 2선 순환, 만잠비 「play free」 후속, 스즈키 빌드업, 고메스·카마라 언급 — 확인한 어느 매체 발췌에도 없다. 구단 「POST-MATCH LIVE」(0G-3rgIq77o)는 **해설진 토크만 있고 회견은 들어 있지 않다**(전사로 확인).
- 🇪🇸 스페인어: EFE 「2-2. El Aston Villa de Emery, estancado」(에메리의 빌라, 정체) — **인용 없음**. AS·Marca·Mundo Deportivo·El Correo·Noticias de Gipuzkoa 0건(검색어: 「Unai Emery Brentford empate declaraciones Aston Villa」 · 「Emery Brentford rueda de prensa Villa Park Ruggeri」).

### D1-2. 키스 앤드루스(브렌트퍼드) — ✅ 확보 · 빌라 구조 언급 0
- Sky 회견: 「We could've won it, could've lost it」(이길 수도, 질 수도 있었다) · beIN/MOTD: 「Torn to be honest … we're also up against a team who I thought were just starting to click before the international break」(솔직히 복잡하다 … 대표팀 휴식기 직전 막 맞아 들어가던 팀을 상대했다).
- ⚠️ **밍스·골킥 압박 계획 언급 없음.** 브렌트퍼드 구단 리포트는 장면만 서술: 「Tyrone Mings was put under pressure by two Bees players」(밍스가 브렌트퍼드 선수 2명에게 압박받았다). ⇒ 「설계된 압박 함정」(Tanswell 14′)은 기자·팬·구단 리포트 판단이고 **상대 감독 확인은 없다**(obs#984).

### D1-3. 팬 채널·구단 영상 — 전사 4편 · 요약 + 구현 주장 9행(G17)
| 영상 | 게시 | 종류 | 핵심 | impl_claims |
|---|---|---|---|---|
| AVFC 「Unai Emery post match reaction」 gxU0HMfb3Nk | 10-10 | 플래시 인터뷰 | 위 D1-1 | none 1 |
| AVFC 「POST-MATCH LIVE」 0G-3rgIq77o | 10-10 | 해설진 토크 | 만잠비 「10 position … with Jackson most of the time」(대부분 잭슨 바로 뒤 10번) · 「unai system … wants them to try and play through」(에메리 시스템은 뒤에서 풀어 나오길 원한다) · 음바예·알리송 투입 후 「who's on the right, who's on the left」(누가 오른쪽이고 왼쪽인지 계속 바뀌었다) | 만잠비 cam_playmaker APPLIED · 골킥 빌드업 NA |
| UTV 「SOME OF THIS DOESN'T MAKE SENSE!」 HKPnsNlcdEQ | 10-10 | 경기 반응+복스팝 | 「we're still so narrow … so easy to be jumped on」(여전히 너무 좁아 압박당하기 쉽다) · 밍스 표적 압박 · 카마라 고립 · 고메스 견실 | 폭 limit HELD · 밍스 limit PENDING · 카마라 limit HELD |
| 1874 「Plenty Of Positives」 aEKmZ70siXA | 10-11 | 경기 반응 라이브 | 고메스 사실상 MOTM · 골킥 때 고메스 집중 압박 · 루제리 HT 이탈로 왼쪽 자연 폭 상실 · 음바예 좌우 위협 · 만잠비 후반 체력 저하 | 고메스 dm_dlp APPLIED · 골킥 수신 HELD · 음바예 IF PENDING |

- The Villans: 경기 후 영상 **미게시**(최신은 10-08 프리뷰 「Dismantling Keith Andrews…」) → D+2 재확인.
- 1874: 월요일(10-12) 「five things」 후속 쇼 예고 → D+2·D+3 대상.
- ⚠️ UTV 복스팝 전사에 26/27 스쿼드에 없는 이름(Partey·El Ghazi·Maguire·Digne 등)이 섞여 있다 — 자동 자막 오인식 또는 팬 착오. 인물명은 실측으로만 확정했다.
- ⚠️ UTV의 「너무 좁다」는 **실측과 일부 충돌**: 오른쪽은 맥긴 터치라인 .52·wm_winger/Attack로 폭이 있었다. 좁았던 쪽은 왼쪽(부엔디아 IF .625) — HELD.

### D1-4. Tanswell · 다국어 추가분
- **Bluesky**: D+0 수집(26건) 이후 신규 **0건**(마지막 16:48Z — 앤드루스의 3면 경기장 발언 관련). 종료 직후분은 D+0 §8-2에 이미 반영. 추가 확인한 문장: 「Lack of control means defence is exposed more, broken upon more & feel slightly more fragile」(통제가 없으니 수비가 더 노출되고 더 자주 뚫리며 조금 더 취약해 보인다). X는 접근 불가. The Athletic 기사 0건.
- 🇯🇵 스즈키: Football Zone·Goal JP·도쿄스포츠·닛칸·Soccer King·풋볼채널 — 첫 실점 「ほとんど不可能だった」(거의 불가능했다 · Birmingham Live 재인용) · 「ビルドアップにも何度も関わった」(빌드업에도 여러 번 관여했다 · Soccer King) · 「ハーフウェーライン手前まで飛び出してクリア」(하프라인 바로 앞까지 나와 걷어냈다 · 닛칸) — **GK 정본 gk_sweeper/Build-Up(f0c29e0)과 같은 방향**. 실점 실수는 전부 밍스 「つなぎのミス」(연결 실수)로 서술 · 스즈키 빌드업 비판 0.
- 🇨🇭/🇫🇷 만잠비: Bluewin(Keystone-SDA, 영문판만 확보) 「Manzambi provided the final pass for the second goal」(두 번째 골의 마지막 패스) · 24heures 스니펫 — 전술 서술 0. Blick·RTS·Le Matin·L'Équipe 0건.
- 🇮🇹 루제리: **0건**(「Ruggeri infortunio Aston Villa Brentford」 · 「bicipite femorale」 · 「problema muscolare … esami」). 터키어 매체(페네르바체전 프레임)만 다룸 — 미열람.
- 🇧🇷 고메스·알리송: ge.globo·UOL·Lance **0건**(「João Gomes Aston Villa Brentford empate」 · 「Alysson Aston Villa Brentford ge.globo」 · 「Aston Villa empata com Brentford João Gomes Alysson」).
- 전술 블로그: Aston Villa Review(서브스택) 평점 — 「Aston Villa don't always have the answer to being systematically interrupted」(빌라는 체계적으로 끊기는 경기에 늘 답을 갖고 있진 않다 · 브렌트퍼드 파울 24) · 완비사카 「Every weakness he has in possession was amplified on his left foot」(소유 시 약점이 왼발에서 증폭됐다 — §4 완비사카 왼쪽 수행의 비용) · 음바예 「Came in on the right, with McGinn moving more central」. 「match conclusions」 본편은 유료·10-11 게시 예정 → D+2. 7500 to Holte·Coaches' Voice·TFA 0건.

### D1-5. 중점 검증 판정
| 항목 | D+0 | D+1 판정 |
|---|---|---|
| 루제리 부상(obs#967) | SofaScore 부상 교체 + Tanswell 테이핑 | ✅ **확정** — 감독 「hamstring」(obs#983) |
| 2선 순환(obs#968·971·974) | 평균 위치가 순환을 지움 | ✅ 64′ 배치 독립 2소스 확인 · 이후 좌우 교대는 1874·구단 해설 정황(obs#985). 장면 빈도는 영상 미확인 |
| 알리송 국면별 움직임(obs#980) | 표본 무효 | 신규 근거 0 — UTV 복스팝(두 번째 실점 때 캐시가 알리송에게 나가라 지시) 1건뿐, 판정 불가 유지 |
| claim #167 | 2/4(최근 3경기 2/3) · 사용자 결정: 다음 동시 선발 대기 | **PENDING 유지** — 새 패스 증거 없음. 정황: 1874 「골킥 때 고메스 집중 압박」 |
| claim #169 | HELD | **HELD 유지** — 79′ 지적은 전부 팀 단위, 맥긴 특정 0건 |
| 밍스 표적 압박 | Tanswell 1소스 | 독립 3소스 일치 · 상대 감독 확인 없음(obs#984) · 처방 변경은 사용자 판단 |

### D1-6. 상태
- `match_reports` #51은 **draft 유지**: 감독 발언은 확보했지만 **정식 회견 전문이 없고**(매체 발췌만) D+2·D+3 추적이 남았다. G12 데이터 조건 자체는 D+0에서 충족.
- 반영: `observations` #983~986 · `player_duties` 4행에 덧붙임(고메스 #22 · 음바예 #245 · 밍스 #160 · 루제리 #223) · `match_videos` 4행(요약·key_points) · `video_impl_claims` 9행 · claim #167·#169 verdict_note 덧붙임.
- 다음 회차(D+2) 우선: 1874 「five things」 · The Villans 경기 후 영상 · Aston Villa Review 「match conclusions」 · 루제리 스캔 결과 · 에메리 페네르바체전 사전 회견(10-14 예상, 루제리·완비사카 왼쪽 언급 가능).

## D+2 추적 (2026-10-12)

> 수집 시각 2026-10-12 KST · 회차: 스케줄 `mw-avl-brentford-d2` · 당일 절(§1~9)과 D+1 절은 수정하지 않았다. 중점: 지연 게시 전술 분석 영상·전술 블로그(다국어 · 상대팀 관점 포함).

### D2-1. 전술 분석 영상 — 신규 2편 전사 · 요약 + 구현 주장 6행(G17)
| 영상 | 게시 | 종류 | 핵심 | impl_claims |
|---|---|---|---|---|
| UTV 「THE REAL REASON WHY WE CAN'T WIN AT VILLA PARK」 YV8GaXrtRpo (33:13) | 10-11 | **전술 리뷰**(장면 클립·패스맵·네트워크) | 아래 D2-2 | 캐시 추적 limit HELD · 밍스 빌드업 limit PENDING · 고메스 허브 instruction PENDING · 전환 고립 limit HELD · 스즈키 스위핑 맥락 limit HELD |
| 1874 「Plenty to Like, But Villa Still Have Work to Do! … Matchday Experience」 OKn4DXxl54A (21:46) | 10-11 | 현장 브이로그 | 「Xiao Gomez was exceptionally good」(고메스가 특출났다) · 「Suzuki good」 · 2-1 직후 실점 「naive」(순진했다) | none 1 |

- UTV 영상은 yt-dlp가 **HTTP 429**로 막혀 브라우저 pot 경로(`yt_transcript_json3.py`)로 전사했다. 전사 중 아예르가 「Ya」로 오인식 — 인물은 SofaScore incidents로 확정.
- ⭐ UTV가 인용한 패스 성공률은 우리 SofaScore 실측과 거의 일치한다: 밍스 78↔**77** · 카마라 84↔**82** · 고메스 90↔**90** · 만잠비 95↔**95** · 잭슨 72↔**72** · 캐시 93↔**88**. 패스 수(밍스35·린델뢰프36·카마라37)는 원천이 달라(영상 속 xG 사이트) 판정에 쓰지 않았다.
- **미전사**: Justin Talks Villa 「THE WARM DOWN | ASTON VILLA 2–2 BRENTFORD」 TMWv33q3T64(10-10 · 13:04) — **자막 없음**(yt-dlp `has no subtitles`). 서브스택 본문도 영상 링크뿐.
- **미게시**: The Villans 경기 후 영상(최신 여전히 10-08 프리뷰) · 1874 월요일 「five things」 후속 쇼(10-12 회차 시점 업로드 목록에 없음) → D+3 재확인.

### D2-2. UTV 전술 리뷰 핵심 (auto-caption)
- 진단: 「we lacked control. Now control is one of the biggest fundamentals within an Unai team」(통제가 없었다. 통제는 에메리 팀의 가장 큰 기본이다) — 에메리 자기 진단(obs#986)과 같은 방향.
- **9′**: 「Tyrone Mings has got a clear option now to roll this ball onto his left foot and play into Ruggeri」(왼발로 굴려 루제리에게 줄 명확한 옵션이 있었다) → 첫 터치가 발밑에 걸림 → 안쪽 카마라에게 느슨한 패스(「Kamara doesn't want this ball. He's pointing towards Gomez」 카마라는 이 공을 원하지 않고 고메스를 가리킨다) → 샤데 회수 → 박스 앞 빈자리에서 야르몰류크. 평가: 「we weren't under any pressure」(압박받지 않았다).
- **79′**: 켈러허 → 빌라 오른쪽 2대1 과부하 → 「Matty Cash here for some reason completely switches off and doesn't track the run」(캐시가 완전히 집중을 놓고 침투를 따라가지 않는다) · 「Maybe Gomez can shuffle across a little bit more」(고메스가 조금 더 좁힐 수도 있었다).
- **전환 수비**: 「Your defense is isolated … The midfield is chasing shadows」(수비가 고립되고 미드필드는 그림자만 쫓는다) — 반복 장면 4~5개 클립.
- **스즈키 막판 스위핑**: 「Why in the last minute of the game is our keeper having to steam out to the halfway line … I'm thankful he did」(왜 마지막 순간 키퍼가 하프라인까지 나가야 하나 — 해 줘서 다행이지만) — 행동은 인정, 원인은 통제 부족.
- **네트워크**: 「everything's kind of going into Gomez … spider web off him」(모든 것이 고메스에게 모인다) · 카마라–고메스 간격 넓음 · 폭은 풀백 2명뿐 「still quite narrow」(여전히 좁다) · 음바예 투입 후 「creative option where he can go out wide and he can attack centrally」(바깥으로도 안으로도 갈 수 있는 창의적 옵션).

### D2-3. 기사·방송 해설 (다국어 · 서브에이전트 위임 + 1차 소스 재확인)
- 🇬🇧 **BBC MOTD 시어러**(Aston Villa News 10-11 06:40 · 원문 직접 확인): 「Matty Cash gets caught ball watching. Ajer give and go, (Joao) Gomes certainly doesn't help Cash out at all.」(캐시가 공만 보다 놓쳤다. 아예르의 원투에 고메스는 캐시를 전혀 돕지 않았다) · 「That is exactly what John McGinn was on about」(맥긴이 말한 게 바로 이것이다 — 맥긴의 「오프더볼에서 배울 게 많다」 취지 발언을 받는 말이나 **맥긴 원문은 미확보**).
- 🇬🇧 PA/Evening Standard 「Tyrone Mings' stray pass」(밍스의 빗나간 패스) · 만잠비 「caused problems for the Bees all afternoon」(오후 내내 브렌트퍼드를 괴롭혔다) · SofaScore 뉴스 맥긴 「two key passes from clever pockets in the right half-space」(오른쪽 하프스페이스에서 키패스 2) · Sky(Adam Bate) — 구조 서술 없음.
- 🇬🇧 **브렌트퍼드 관점**: 앤드루스 VAVEL 「The boys aren't robots. It takes some time」(선수들은 로봇이 아니다 — 시간이 걸린다) · 「I felt we could've nicked it」(이길 수도 있었다) — **밍스·골킥 압박 계획 언급 0**(VAVEL·Irish Examiner 원문 확인). Beesotted·Bees United·Ealing Road 경기 후 리뷰·브렌트퍼드 팬 유튜브 **0건**(Ealing Road는 프리뷰만).
- 🇯🇵 스즈키 — **東スポWEB**(10-11) 「ハーフウェーライン手前まで飛び出してクリアしてピンチの芽をつんだ」(하프라인 앞까지 뛰쳐나와 걷어내 위기의 싹을 잘랐다) · **フットボールチャンネル**(10-11) 「ハーフウェーライン近くまで飛び出してクリアするなどチームのピンチを救った」(하프라인 근처까지 나와 걷어내는 등 위기를 구했다) · GOAL JP 「先制点はどうすることもできなかった」(선제골은 어쩔 도리가 없었다). 빌드업(스즈키→밍스) 서술은 기확보 게키사카 계열 외 0.
- 🇩🇪/🇨🇭 만잠비 — watson.ch 「Aston Villa mit Johan Manzambi kommt weiterhin nicht richtig auf Touren」(만잠비가 있는 빌라는 여전히 제 궤도에 오르지 못한다) — 포지션 서술 0. kicker·Badische Zeitung·spielverlagerung.de 0건.
- 🇪🇸 **0건**(EFE 재전재 외) — 검색어: 「Emery Brentford rueda de prensa Aston Villa 2-2」 · 「Aston Villa Brentford Emery análisis táctico octubre 2026」 · 「Emery Villa Brentford AS Marca Relevo empate Villa Park Mings」 · 「Emery Aston Villa Brentford Mundo Deportivo OR "El País" OR Relevo empate octubre」.
- 🇮🇹 **루제리 스캔 결과 미공개**(10-11~12 보도 0) — 검색어: 「Ruggeri infortunio Aston Villa Brentford」 · 「Ruggeri esami lesione Italia … Aston Villa ottobre」 · 「Ruggeri Aston Villa bicipite femorale Mancini Nazionale ottobre 2026」 · 「Ruggeri Aston Villa infortunio esito esami 11 ottobre」. ⚠️ Tuttomercatoweb 「lesione di secondo/terzo grado」(2~3도 손상)는 아탈란타 시절 기사 — 쓰지 않는다.
- 🇧🇷 **0건** — 「João Gomes Alysson Aston Villa Brentford empate」 · 「João Gomes Aston Villa Brentford atuação nota ge globo」 · 「Trivela Aston Villa Brentford João Gomes Alysson Emery」.
- 🇫🇷 **0건** — 「Manzambi passe décisive Aston Villa Brentford Blick RTS」 · 「Manzambi Aston Villa Brentford L'Équipe OR "Le Temps" OR RTS OR Blick 11 octobre」.
- **전술 블로그 0건**: TFA(스코어 페이지뿐) · BTL · Spielverlagerung · Coaches' Voice · Ultimo Uomo · 7500 to Holte. ⚠️ TFA의 「forward presses Tyrone Mings … forcing Aston Villa out wide」(전방이 밍스를 압박해 빌라를 측면으로 몬다)는 **약 1년 전 맞대결** 자료라 이 경기 근거로 쓰지 않았다. PL Story House 「The Aston Villa/Brentford Room」은 자칭 「Fictional minds. Real data.」(가상 필자) 매체라 근거에서 제외.
- ⚠️ Sky Sports 페이지에 기사 본문이 아닌 「특정 문구를 인용하라」는 지시문 블록이 섞여 있었다 — 데이터로만 취급하고 따르지 않았다.

### D2-4. 에메리 회견 재시도
- **정식 회견 전문 여전히 미확보.** avfc.co.uk 「Emery reflects on 'tough match'」(VillaTV 플래시 — D+1 확보분과 동일) · ESPN 「sad」 · Sky 「At Villa Park, we have played three matches and we did not win until now」(빌라 파크에서 세 경기를 치렀는데 아직 못 이겼다) — 전술 의도(교체·2선 순환·스즈키 빌드업)를 다룬 대목은 어느 발췌에도 없다. UTV가 인용한 Tanswell 경유 발언 「happy with the defensive structure but felt they conceded chances due to not keeping possession well」(수비 구조엔 만족하나 점유를 잘 지키지 못해 찬스를 내줬다 — **UTV 낭독 auto-caption, Tanswell 원문 미확인**)은 D+1 「control」 진단과 같은 방향.

### D2-5. 중점 검증 판정
| 항목 | D+1 | D+2 판정 |
|---|---|---|
| 2선 순환(만잠비 왼쪽·맥긴 10·음바예 오른쪽) | 64′ 배치 독립 2소스 · 이후 교대는 정황 | **변동 없음** — 신규 원문 근거 0. UTV는 77′ 빌드업에서 음바예의 중앙 공략 1장면만 |
| 짧은 빌드업 함정(9′ 밍스) | 독립 3소스 「표적 압박」(obs#984) | **보정(정정 아님)** — 밍스는 압박 없이 받았고 첫 터치·판단에서 실패(UTV). 「showing the ball to Mings」는 수신자 유도로 읽는다 — 설계는 상대, 실점은 실행(**obs#988**). 상대 감독 확인은 여전히 0 |
| 79′ 빌라 오른쪽 실점 | 「don't track Ajer」 팀 단위 | ✅ **귀속 특정** — 캐시 볼 와칭 + 고메스 커버 부재, 독립 2소스(시어러·UTV) · 고메스는 AVR 포함 3소스(**obs#987**) |
| 스즈키 스위퍼(정본 gk_sweeper/Build-Up) | 일본 매체·이벤트 일치 | **유지** — 일본 2매체 추가 확인. 단 UTV는 「통제 부족이 강제한 장면」으로 해석 → 성향/상황 분리는 3경기 누적(**obs#989**) |
| claim #167 | PENDING(2/3) | **PENDING 유지** — 새 패스 실측 0. UTV 네트워크상 고메스 허브는 반대 방향 정황이나 물량 지표와 다른 축(**obs#990**) |
| claim #169 | HELD | **HELD 유지 · 반례 1건** — 79′을 맥긴으로 특정한 소스 0, 두 소스 모두 캐시·고메스 |

⇒ **당일 판정 정정 없음.** §2의 「9′ 실수는 상대의 설계된 압박 함정」은 뒤집히지 않았고 obs#988로 해석 범위만 좁혔다.

### D2-6. 게임 구현 함의
- 79′ 귀속은 **집중력 축**이라 FC 역할·포커스로 옮기지 않는다(캐시 RB 정본 유지 · claim HELD — 재판정: 2경기째 독립 2소스).
- 밍스 9′은 「표적 압박」보다 「수신 후 실행」 쪽 근거가 늘었다 — 밍스 선발 시 처방(빌드업 관여를 줄이는 역할) 변경은 claim #210·#216 **PENDING · 사용자 판단**.
- 결론은 §7과 같다: **추가 관찰**.

### D2-7. 상태
- `match_reports` #51 **draft 유지** — 정식 회견 전문 미확보 · D+3 남음.
- 반영: `observations` #987~990 · `player_duties` 4행 덧붙임(캐시 #30 · 고메스 #22 · 밍스 #160 · 스즈키 #121) · `match_videos` 2행(요약·key_points) · `video_impl_claims` 6행(#215~220) · claim #167·#169·#210 verdict_note 덧붙임.
- D+3 우선: The Villans 경기 후 영상 · 1874 「five things」 · Aston Villa Review 「match conclusions」(유료) · 루제리 스캔 결과 · 에메리 페네르바체전 사전 회견(10-13~14 예상 — 루제리·완비사카 왼쪽, 밍스 언급 가능) · 맥긴 「off the ball」 원문.
