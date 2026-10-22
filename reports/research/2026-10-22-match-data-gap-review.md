# 경기 분석용 선수·경기 데이터 결손 검토 (2026-10-22)

> 범위: **경기 단위 분석**(리포트 §5 선수별 · 대조표 가설 판정 · 역할 커널 fit · 팀 설정 규칙)에 지금 쓰는 데이터와, 같은 무료 제공사에서 **더 받을 수 있는데 안 받는 것**.
> 방법: DB 읽기만(AVL 26/27 공식전 12경기 · `matches.date ≥ 2026-08-12` · 친선 2경기 제외) + 수집기 필드 목록(`core/sofascore.py STAT_FIELDS` · `core/whoscored.py` · `scripts/collect_fotmob_players.py`) + 바이킹전 리포트의 「추정·미수집·손계산」 지점.
> 유료 데이터(Opta xT/EPV · StatsBomb 360 · Wyscout)는 제안하지 않는다. 무료 이벤트 데이터로 **답할 수 없는 질문**은 §4에 따로 적고 대체 프록시를 명시한다.

## 0. 한 줄 결론

- **경기 단위 기본 축은 충분하다** — SofaScore 19필드·그리드·평균 위치(출전 전원), FotMob xG 4종·슈팅맵, WhoScored 국면 그리드·PPDA·def_x·세트피스·운반(추정)이 10-14 이후 경기 전부에 있다.
- **구조적 결손은 「회차마다 범위가 달랐다」는 것이다.** FotMob 경기별 선수 스탯(상대 박스 터치·라인 브레이킹 패스·기회 창출·거리·스프린트)은 **브라이튼전(#86) 1경기만**, WhoScored 선수 보유 x(`ws_poss_x`)는 **브뤼허전(#99) 1경기만** 들어갔다. 바이킹전은 둘 다 없다 — 같은 제공사 같은 호출인데 런북에 「필수」로 안 박혀 회차마다 빠졌다.
- **가설 판정이 「부분 일치·판정 불가」로 멈춘 자리(바이킹전 partial 13 · undecided/pending 2)는 대부분 「수신 좌표·압박 받는 상황·오프볼」 신호 부재**다. 수신 좌표는 WS 이벤트의 `PassEndX/Y`(이미 받은 JSON 안에 있다)로 지금 당장 채울 수 있고, 오프볼·압박 의도는 무료 데이터로는 끝내 못 잰다(프록시만).
- 역할 커널 fit의 「무결정 Δ≤.05」(FC27 4경기 선발 44칸 중 **25칸**)는 **입력이 터치 히트맵 한 장**(`map25`)인 구조 때문이다. 보유/비보유 분리 그리드(`map25_poss/def`)가 이미 있는데 커널 fit은 합산 그리드만 쓴다 — 수집이 아니라 **활용** 결손.

## 1. 지금 저장하는 것 (AVL 26/27 공식전 12경기 · 189 선수행)

| 층 | 표·컬럼 | 공급원·호출 | 채움 | 비고 |
|---|---|---|---|---|
| 선수 기본 스탯 | `player_matches` rating·minutes·xg/xa·key_passes·pass_total/acc·duels·tackles·interceptions·touches·recoveries·shots·clearances·saves | SofaScore `/event/{id}/player/{pid}/statistics` (STAT_FIELDS 19) | 142/189 (교체 짧은 출전·GK 제외 사실상 전원) | `xg` 49행은 슈터만 |
| 선수 위치 | `avg_x/avg_y` · `map25`·`cells`(hit_points) | SofaScore `average-positions` · `player/heatmap` | 188/189 | 유효 기준 45분+·15점 |
| 국면 그리드 | `map25_poss/map25_def`·`cells_poss/def`·`phase_source` | WhoScored matchCentreData → `core.whoscored.phase_cells` | 142/189 (#68 PSG·#94 아스널 0) | 10-14 이후 전부 |
| 스코어 국면 분 | `stats_json.phase_lead/level/trail` | `match_events` → `core.phase_minutes` | 189/189 (10-22 백필) | G23 |
| 운반(추정) | `stats_json.carry_est_*` | WS 이벤트 → `core.whoscored.carry_est` | 32/189 (#56·#62만) | 10-22 신설 · 추정 명기 |
| FotMob 경기별 선수 | `stats_json.touches_opp_box·chances_created·line_breaking_passes·aerials·dispossessed·dribbled_past·shot_blocks·distance_covered·sprints·topspeed·passes_final_third·dribbles` | FotMob `__NEXT_DATA__ content.playerStats` | **15/189 (#86 브라이튼만)** · 거리·스프린트 10 | ⛔ 회차 의존 |
| WS 선수 보유 x | `stats_json.ws_poss_x·ws_min_poss_x·ws_def_x·opta_position` | WS 이벤트 | **15/189 (#99 브뤼허만)** | ⛔ 회차 의존 |
| 팀 경기 스탯 | `team_match_stats` xG 4종(FotMob 동일 스냅샷)·슈팅·빅찬스·패스·롱볼·크로스·코너·듀얼·파울·공중·드리블·태클·인터셉트·클리어·블록·PPDA(분자/분모)·def_x | SofaScore `statistics` + FotMob + WS | 12~13/13 · def_x 9/13 | def_x는 WS 있는 경기만 |
| 하프별 | `match_period_stats` 점유·xG·슈팅·PPDA | 위 조합 | 2행/경기 | |
| 구간 지표 | `match_phase_metrics` def_x·ppda·own_half_pass_pct·gk_long_share(+ box_touches_p10·own_third_losses·shots_p10 3행뿐) | WS → `segment_metrics` | #56·#62 전 구간 | 10-20 신설 · 이전 경기 없음 |
| 사건 | `match_events` goal·own_goal·penalty_goal·sub·yellow·red·var·gk_change | SofaScore `incidents` | 전 경기 | 코너·FK·오프사이드 kind 없음 |
| 슈팅 | `match_shots` xg·xgot·outcome·situation·body_part·x/y | FotMob shotmap(UCL) · SofaScore shotmap(PL) | 전 경기 | 제공사가 대회별로 갈림 |
| 세트피스 | `match_set_pieces` kind·taker·target·flank·outcome | WS qualifier → `set_pieces` | #56·#62 | 10-22 신설 |
| 가설·변화·형태 | `match_hypotheses`·`match_tactical_changes`·`match_game_setups.shape_*` | 리포트 JSON | #56·#62(G37) | |
| 시즌 축(선수 리포트) | `fotmob_detail_stats` 25지표(10-22) · `fotmob_season_stats` · `fotmob_traits` · `player_market_values` · `player_status`(10-22) · `understat_player_matches` 6,178행 | FotMob playerStats · Understat | 10-22 신선 | match-watch §0-1이 주간 갱신 |

## 2. 분석이 실제로 막힌 자리 (바이킹전 리포트 기준)

| 리포트 위치 | 무엇을 쓰려 했나 | 지금 상태 | 왜 막혔나 |
|---|---|---|---|
| 대조표 #10 고메스 볼 캐리 | 전진 운반 수·거리 | **추정**(`carry_est` · 수신→다음 이벤트) | Opta 이벤트에 Carry 타입 없음 |
| 대조표 #13·#19 부엔디아·맥긴 「내려와 받는다」 | **수신 위치**(어디서 받았나) | 추정(다음 이벤트 위치로 역산) | WS `PassEndX/Y`를 받는 사람에게 귀속시키는 함수가 없다 — **JSON엔 있다** |
| 대조표 #15 잭슨↔음바예 교환 | 같은 시각 두 선수의 **오프볼 위치** | 판정 불가(볼 소유 이벤트만) | 이벤트 데이터는 볼 가진 사람만 찍는다 — 무료로는 불가 |
| 대조표 #16 알리송 뒷공간 침투 | 침투 런·오프사이드·스루패스 수신 | 부분(수신 좌표 추정·오프사이드는 incidents 없음) | SofaScore incidents에 offside 없음 · WS `Throughball` qualifier는 받은 JSON에 있다 |
| 대조표 #11·#22 고메스 횡단·「벌려 수비」 | 비보유 위치 분포 | 레인 비중(보유 이벤트)·수비 액션 평균 | `cells_def`는 있으나 레인 통계로 안 쓴다 — 활용 결손 |
| §2 비점유 압박 | 압박 트리거·강도 | PPDA·def_x 구간치만 | 압박 「의도」는 무료 데이터에 없음 — PPDA+def_x+상대 자기 진영 패스 성공률이 프록시 |
| §2 rest-defense 「3+2=5」 | 슈팅 순간 볼 뒤 인원 | 산문(눈대중) | 슈팅 순간 전 선수 좌표 없음 — 불가 · 프록시는 상대 슈팅 직전 10초 보유 이벤트 분포 |
| §5 GK 스즈키 | 스위핑·롱 배급 비중·박스 밖 액션 | `gk_long_share`는 생김 · 스위핑 0건은 **「없다」가 아니라 「안 쟀다」** | SofaScore GK 필드(runsOut·successfulRunsOut·highClaims·punches·goalsPrevented·savedShotsFromInsideTheBox)를 **STAT_FIELDS에 안 넣었다** |
| §5 측면·CB | 크로스 시도/성공·롱볼 시도/성공·드리블 시도/성공·공중 듀얼·실수(errorLeadToShot)·피파울 | 팀 단위만(`team_match_stats`) · 선수 단위 5~7행 | SofaScore 선수 statistics에 **다 있는데** STAT_FIELDS 19개만 받는다 |
| §7 커널 fit 무결정 25/44 | 역할 식별 신호 | 합산 `map25` 한 장 | `map25_poss/def` 분리 그리드를 fit에 안 쓴다 · 역할 커널(fut.gg 히트맵)도 보유/비보유 구분 없음 |
| 평점 교차 | SS·FM·WS 평점 | SS·FM만 | WS rating은 JSON에 있음(`ratings`) — 사소 |

## 3. 제공사가 주는데 안 받는 것

### 3-1. SofaScore `/event/{id}/player/{pid}/statistics` — 선수 statistics 전체 (공개·무료 · 이미 쓰는 호출 · **필드만 추가**)

| 필드 | 쓰임 | 가치 |
|---|---|---|
| `accurateLongBalls/totalLongBalls` | CB·GK·DM 배급형 판정(cb_bpd Build-Up vs Defend · dm_dlp) | 높 |
| `accurateCross/totalCross` | 윙어·풀백 크로스 공급원(세트피스 표와 교차) | 높 |
| `totalContest/wonContest` (드리블) · `dispossessed` · `possessionLostCtrl` | 탈압박·운반 판정(carry_est 보강) | 높 |
| `aerialWon/aerialLost` · `groundDuels` | ST target vs advanced · CB 공중 | 높 |
| `bigChanceCreated/bigChanceMissed` · `expectedAssists`(이미) | 결정력·창출 | 중 |
| `errorLeadToAShot/Goal` · `penaltyConceded` · `wasFouled` · `fouls` | 리스크 축 | 중 |
| `outfielderBlock` · `totalClearance`(이미) · `challengeLost` · `dribbledPast` | 수비 역할(홀딩 vs box-crasher) | 중 |
| GK: `goalsPrevented` · `savedShotsFromInsideTheBox` · `punches` · `highClaims` · `runsOut/successfulRunsOut` · `goodHighClaim` | **스위핑 판정**(gk_ballplaying 재검토 조건 「3경기 중 2경기 KeeperSweeper」가 지금은 잴 수 없다) | **높** |
| `touches`(이미) · `minutesPlayed`(이미) · `ratingVersions` | — | 하 |

접근: `core/sofascore.py STAT_FIELDS`에 튜플 추가 → `js_collect`/`js_event_collect`가 그대로 직렬화 → `parse_collected`가 `stats_json`에 넣는다. 브라우저(sofascore 오리진)는 이미 필요한 경로. 소급: 12경기 × 출전 선수 — 같은 스니펫으로 재호출 가능(평균 위치·히트맵은 재수집 불필요).

### 3-2. SofaScore 그 밖의 경기 엔드포인트

| 호출 | 내용 | 현재 | 가치 |
|---|---|---|---|
| `/event/{id}/graph` | 분 단위 **모멘텀**(−100~100) | 없음 | 중 — 경기 흐름 3묶음·전술 변화 분 경계를 수치로(지금은 득점·교체 분만) |
| `/event/{id}/incidents` | `offside`·`injuryTime`·`varDecision` 포함 | goal·sub·card·var만 적재 | 중 — 오프사이드 kind 추가(알리송 침투 판정) · 어휘 고정 필요 |
| `/event/{id}/lineups` `missingPlayers` | 결장자·사유 | `player_status`가 담당 | 하 |
| `/event/{id}/player/{pid}/heatmap` | 이미 | — | — |
| `/event/{id}/average-positions` | 전·후반 분리 없음(전체만) | 이미 | — |
| `/event/{id}/team/{tid}/heatmap`? | 팀 히트맵(제공 불확실) | 미확인 | 하 |

### 3-3. FotMob `matchDetails` (`__NEXT_DATA__` · 공개 · 이미 받는 응답 안)

| 필드 | 현재 | 가치 |
|---|---|---|
| `content.playerStats[pid].stats[*]` — 「Touches in opposition box」·「Chances created」·「Line-breaking passes」·「Passes into final third」·「Successful dribbles」·「Aerials won」·「Dispossessed」·「Dribbled past」·「Recoveries」·「Fouls won」·「Distance covered」·「Sprints」·「Top speed」·(시즌별로 「Carries」·「Progressive carries」가 **뜨는 대회가 있다** — UCL은 2026-27부터 physical+carry 제공 보고 있음 · 바이킹전 JSON으로 확인 필요) | **#86만** | **높** — 운반 추정을 실측으로 대체할 유일한 무료 후보 · 라인 브레이킹·파이널서드 패스는 「경기를 푼다」 가설의 직접 지표 |
| `content.momentum` | 없음 | 중 (SS graph와 중복 — 하나만) |
| `content.matchFacts.playerOfTheMatch`·`highlights` | 없음 | 하 |
| `content.lineup.*.performance.substitutionEvents` | 교체 사유 아님 | 하 |

접근: `scripts/fetch_fotmob.py`/match-watch §3이 이미 `__NEXT_DATA__`를 받는다 — `playerStats` 파싱을 **필수 단계**로 올리고 `stats_json` 키 어휘를 `collect_fotmob_players.py`의 metric map과 **같은 정본**으로 묶는다(지금은 경기별 키와 시즌별 키가 따로 산다).

### 3-4. WhoScored matchCentreData (받은 JSON 2경기 — 이미 저장)

| 요소 | 현재 | 가치 |
|---|---|---|
| `PassEndX/PassEndY`(패스 끝 좌표) → **수신자 귀속**(같은 팀 다음 이벤트 주체) | 운반 추정에만 간접 사용 | **높** — 수신 위치·수신 압박(수신 직후 Dispossessed/Tackled 비율)·깊은 수신 수가 전부 여기서 나온다 (대조표 #13·#16·#19) |
| qualifier `Throughball`·`KeyPass`·`BigChance`·`Chipped`·`HeadPass`·`Longball`·`Cross`·`Zone`·`Angle`·`Length` | `Longball`·코너·FK·크로스만 | 중 — 스루패스 수신 = 뒷공간 침투 직접 지표 |
| `OffsideGiven`·`OffsideProvoked` 이벤트 | 안 씀 | 중 (SS incidents 보완) |
| `BallRecovery` 위치 분포 | PPDA·def_x에 포함 | 중 — 압박 회수 높이 |
| `ratings`·`position` 분 단위 | 안 씀 | 하 |
| **보존 규칙**: 런북 §2-2a에 저장 규칙은 넣었으나 **G37이 파일 존재를 검사하지 않는다** | — | 높(구조) |

### 3-5. Understat
`understat_player_matches` 6,178행(선수별 경기 xG/xA/npxG/xGChain/xGBuildup)이 있다 — **xGChain·xGBuildup은 「경기를 푸는 축」 가설(맥긴·고메스)의 직접 지표**인데 리포트가 안 쓴다. PL만 제공(UCL 없음). 활용 결손.

## 4. 결손 표

| 분석 질문(리포트 절/가설) | 필요 신호 | 현재 | 공급원·필드 | 수집 방법 | 가치 | 비용 | 우선 |
|---|---|---|---|---|---|---|---|
| 「경기를 푸는 축」(#26 맥긴·고메스) · 부엔디아 하강 수신(#13·#19) | 수신 위치·깊은 수신·수신 후 탈압박 | 추정 | WS `PassEndX/Y` + 다음 이벤트 주체 | `core.whoscored.receptions(events, pid)` 신설 → `stats_json.recv_n·recv_avg_x·recv_deep_n·recv_pressed_pct` · `load_carry_est.py`에 합류 | 높 | 낮(JSON 보유) | **1** |
| GK 역할(gk_ballplaying 재검토 「3경기 중 2경기 스위핑」) · CB/윙어/풀백 세부 역할 | 롱볼·크로스·드리블·공중·GK 러닝아웃/하이클레임 | 없음 | SofaScore statistics 확장 필드(3-1) | `STAT_FIELDS` +18 · 12경기 소급(브라우저 스니펫) | 높 | 중(브라우저 1회) | **2** |
| 운반(#10) · 라인 브레이킹·파이널서드 패스 · 박스 터치 · 거리/스프린트 | FotMob 경기별 선수 스탯 | #86만 | FotMob `playerStats` | match-watch §3에 필수 단계 + `stats_json` 키 정본 통일 + 11경기 소급(JSON 재호출) | 높 | 중 | **3** |
| 회차마다 범위 다름(구조) | — | — | — | **G21 확장**: 공식전 `player_matches`(10-14 이후)에 FotMob 키·`recv_*`·WS JSON 파일 없으면 실패 | 높(구조) | 낮 | **4** |
| 역할 커널 무결정 25/44 | 보유/비보유 분리 fit | 그리드는 있음 · fit 미사용 | `map25_poss` | `core.kernel.fit` 입력을 보유 그리드로 하는 변형 `fit_poss` + 경기 프리셋에 두 값 병기(Δ가 갈리는 칸 보고) | 높 | 낮 | **5** |
| 경기 흐름 경계·전술 변화 분 | 모멘텀 | 없음 | SS `/graph` 또는 FM `momentum` | `match_period_stats`에 분 단위 표 신설(`match_momentum` · migration) | 중 | 낮 | 6 |
| 뒷공간 침투(#16) · 오프사이드 | 스루패스 수신·오프사이드 | 없음 | WS `Throughball` qualifier · `OffsideGiven` · SS incidents offside | `match_events` kind 어휘 +offside · `recv_*`에 through 수신 | 중 | 낮 | 7 |
| 압박 트리거·강도 | 회수 위치 분포·상대 자기 진영 패스 성공률(이미) | 프록시만 | WS BallRecovery x 분포 | `segment_metrics`에 `recovery_x` | 중 | 낮 | 8 |
| 평점 3원 교차 | WS rating | 없음 | WS `ratings` | `stats_json.ws_rating` | 하 | 낮 | 9 |
| 오프볼 교환(#15) · rest-defense 인원 · 압박 의도 | 전 선수 추적 좌표 | **불가** | 없음(유료 추적 데이터만) | 프록시: 두 선수 보유 이벤트의 시간창 교차(같은 5분 창에서 레인 바뀜 횟수) · 상대 슈팅 직전 10초 우리 보유 이벤트 분포 | — | — | 프록시만 |
| 선수 리포트 신선도 | FotMob 시즌 25지표·부상·시세 | 10-22 신선 | §0-1 주간 | 유지 · 단 **`fotmob_detail_stats`는 PL만**이라 UCL 포함 합산이 없다(FotMob 한계) | — | — | 유지 |

## 5. 우선 조치 8건

| # | 할 일 | 바꿀 곳 | 표 | 합격 기준 |
|---|---|---|---|---|
| 1 | 수신 귀속 함수 `receptions()` + `stats_json.recv_*` 4키 + #56·#62 적재 · 대조표 #13·#19 D2 재판정 | `core/whoscored.py` · `scripts/load_carry_est.py`(이름을 `load_ws_player_extras.py`로) | `player_matches` | `SELECT count(*) FROM player_matches WHERE json_extract(stats_json,'$.recv_n') IS NOT NULL AND match_id IN (120,126)` = 32 |
| 2 | SofaScore `STAT_FIELDS` 확장(롱볼·크로스·드리블·공중·GK 6종 등 +18) + 12경기 소급 | `core/sofascore.py` · match-watch §2 | `player_matches.stats_json` | 공식전 10-14 이후 선수행에 `long_att`·`aerial_won`·GK행 `runs_out` NOT NULL |
| 3 | FotMob `playerStats` 경기별 적재를 필수 단계로 + 키 정본 통일 + 11경기 소급 · **Carries/Progressive carries 제공 여부 1회 확인**(바이킹전 JSON) | `scripts/fetch_fotmob.py` · `collect_fotmob_players.py` metric map 공유 | `player_matches.stats_json` | `touches_opp_box` 채움 경기 ≥ 11/12 · carries 제공이면 `carry_est_*` 옆에 `carries_fm` 병기 |
| 4 | G21 확장 — 공식전 선수행 필수 키(FotMob·recv·확장 SS) + `reports/match-watch/data/*-ws-*.json` 존재 | `scripts/gates.py` | — | gates ✅ · 바이킹전 이후 경기에 결손 0 |
| 5 | 보유 그리드 fit(`fit_poss`) 병기 — 경기 프리셋 16행에 `fit_sim_poss` 컬럼(migration) | `core/kernel.py` · `match_player_prescriptions` | migration | 4경기 44칸 중 Δ≤.05가 몇 칸 줄었는지 리포트 |
| 6 | 모멘텀 표 신설(`match_momentum` minute·value·source) + 경기 흐름 3묶음 경계 자동 제안 | migration · match-watch §3 | 신설 | #62 90행 · `match_tactical_changes` 분과 대조 |
| 7 | `match_events` kind +`offside` · WS `Throughball` 수신을 `recv_through_n`으로 | `load_sofascore_json.py` · `core/whoscored.py` | `match_events`·`stats_json` | 어휘 게이트에 kind 추가 · #62 알리송 `recv_through_n` ≥ 0 |
| 8 | Understat `xGChain/xGBuildup`을 선수 리포트·경기 리포트 §5(PL 경기)에 표기 | `export.py`(선수 JSON) · 리포트 템플릿 | 없음(활용) | 뉴캐슬전 §5 맥긴·고메스 행에 xGChain 표기 |

## 6. 무료 데이터로 답할 수 없는 질문(명시)

- **오프볼 움직임·위치 교환**(잭슨↔음바예 · 알리송 교차 「횟수」): 이벤트 데이터는 볼 가진 순간만 찍는다. 프록시 = 두 선수 보유 이벤트의 5분 창 레인 교차 횟수 + 팬·분석 영상 서술(D등급).
- **압박 의도·트리거**: PPDA·def_x·회수 높이·상대 자기 진영 패스 성공률의 조합이 상한. 「백패스 때 뛰었다」는 영상 주장(`video_impl_claims axis=instruction`)으로만.
- **rest-defense 인원·라인 간격·블록 폭**: 추적 데이터 필요. 프록시 = 상대 슈팅 직전 10초 우리 보유 이벤트 x 분포(「볼 뒤에 몇 명」이 아니라 「얼마나 앞에 있었나」).
- **GK 스위핑의 질**: 러닝아웃 횟수(SS)는 받을 수 있으나 「나왔어야 했는데 안 나온」 장면은 없다.
