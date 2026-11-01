# 2026-10-31 AVL vs Fulham — 1-1 (홈 · 빌라 1 풀럼 1)

> 수집일 2026-11-01(예약 `mw-avl-fulham-collect` 10:00 회차) · SofaScore event `16363901` · FotMob `5795496` · WhoScored `1983627` · **프리미어리그 9라운드** · 홈(빌라 파크 · 관중 34,649) · 주심 Samuel Barrott · 빌라 4-2-3-1 vs 풀럼 4-2-3-1 · 풀럼 감독 **Álvaro Arbeloa**(SS managers · 풀럼 공식 회견 · PA 3원 확인) · 게임 버전 `core.game_version.live_on('2026-10-31')` = **FC27**
> DB: `matches` #129 · `match_reports` #65(draft) · 이 경기 관전 메모: `reports/match-watch/notes/`에 **2026-10-31-avl-fulham\* 없음** → 본머스전 사용자 메모(음바예 → 오른쪽 공백) 가설을 이 경기 실측으로 다시 대조했다(아래 표).

## 요약

- **1-1, 전반 지배·후반 붕괴.** xG **1.71–2.21**(FotMob · 빌라 PK 0.79 포함 → 논PK **0.92–2.21**) · 전반 xG 1.20–0.60 → 후반 **0.51–1.61** · 점유 45%(전반 47·후반 43) · 슈팅 16–14 · 유효 3–5 · 빅찬스 4–4 · 상대 박스 터치 **24–40**.
- **득점·실점**: 39′ 잭슨(만잠비 스루패스 · 알리송 흘려주기 · 카스타뉴·아펜그루버 제치고 마무리) · 16′ 맥긴 PK 크로스바(13′ 고레츠카 코너 헤더 → 베르게 핸드볼 VAR) · 64′ 이워비 코너를 스즈키가 놓친 **자책골**.
- **압박이 후반에 사라졌다**: PPDA 빌라 전반 15.58 → 후반 **31.67**(풀럼 경기 12.84) · 0–15′ 수비 액션 평균 높이(def_x) 62.8로 높게 출발했지만 리드 뒤(39–64′) **19.6~24.8**로 하강 · 에메리 「They were breaking our press and we needed our goalkeeper, Zion Suzuki, saving some actions.」(그들이 우리 압박을 깨고 나왔고 골키퍼 스즈키의 선방이 필요했다 · avfc.co.uk).
- **빌라 오른쪽이 풀럼의 주 공격로였다 — 단 「전환 공백」이 아니라 「상대 LB의 배후 침투」로.** 66′ 전 풀럼 오픈플레이 크로스 **빌라 오른쪽 9 : 왼쪽 2**(로빈슨 5·이워비 4) · WLS 「He constantly got in behind Matty Cash」(계속 캐시 뒤를 파고들었다). 상대 진영 볼 상실 뒤 10초 전환 진입은 오른쪽 2·왼쪽 3(본머스전 H2′ 판정과 같은 방향).
- **배치**: 고레츠카 **LDM**(첫 PL 선발 · 쟁점 #25 2/2 → 더블 피벗 확정) · 맥긴 10번이 오른쪽 하프스페이스로 기울고(볼 터치 62% 오른쪽) 잭슨이 왼쪽으로 내려와(SS 평균 54,60) 만잠비와 연결 · 66′ 3명 동시 교체(위치상 알리송→음바예 · 고레츠카→고메스 · 만잠비→부엔디아 — SofaScore·클럽 기록의 짝은 다르다, 아래).
- **게임 구현: 추가 관찰.** 경기 프리셋 4-2-3-1 Wide · Balanced/Deep/40(RULE). 정본 변경 없음 — **슬롯 정본 보류 5건 재판정 표(맨시티·본머스·풀럼 3경기)**는 끝 절 · 사용자 판단 대기.

## ⭐ 본머스전 사용자 관전 메모 재대조 (H1′·H2′·H2·H3 → 풀럼전)

원료: WS matchCentreData 1,580건(scope=full · `data/2026-10-31-avl-ws-1983627.json`). 좌표는 WS(각 팀 자기 공격 방향 x · y 0 = 그 팀 오른쪽). **빌라 오른쪽 = 풀럼 왼쪽(풀럼 y>66.7)**. 국면은 셋으로 갈랐다 — ⑴ **보유**(빌라 볼 터치 레인) ⑵ **비보유**(풀럼 파이널서드 터치·크로스 출발·수비 액션 좌표) ⑶ **볼 상실 직후 10초**(빌라 터치 → 다음 터치가 풀럼 → 10초 안 풀럼이 x>66.7 진입한 레인). 평균 위치 하나로 판정하지 않는다(obs#879). 66′ 전(알리송 RM)과 뒤(음바예 RM)를 나눴다. ⚠️ 이 경기 음바예는 **교체 24분**이라 선발 기준 쟁점(#6·#7·#48)에 안 세진다.

| # | 사용자 가설(본머스전 메모) | 본머스전 판정(10-28 · 음바예 선발 58′) | 풀럼전 실측(알리송 0–66′ / 음바예 66′–) | 풀럼전 판정 |
|---|---|---|---|---|
| H1′ | RM 기본 위치는 오른쪽 넓게, 중앙 진입은 공격 국면에서만 | **부분 일치**(기본 폭 일치 · 중앙 볼 소유 2/22) | ⑴ 보유: 알리송 볼 터치 24 중 **오른쪽 폭 20(83%)**·중앙 4 · 보유 그리드 1위 wm_winger/Attack .733(**Δ.194 결정**) · 음바예 21 중 **19(90%)** 오른쪽 · 안쪽 칸은 **맥긴(10번)이 오른쪽 하프스페이스로 기울어** 채움(볼 터치 62% 오른쪽 · (70,25)) · BirmLive 「Alysson has a natural ability to glide infield from the right wing」(알리송은 오른쪽 윙에서 안으로 미끄러져 들어온다)은 볼 소유 위치로는 드묾 | **부분 일치** — 기본 폭 = 일치(2경기 연속). RM의 중앙 진입은 두 경기 모두 드물고, 안쪽은 10번(본머스 부엔디아 · 풀럼 맥긴)이 채운다 |
| H2′ | 오른쪽 공백은 공격→수비 **전환 순간**에 생긴다 | **불일치**(상대 진영 상실 34 → 오른쪽 0·왼쪽 2) | ⑶ 상대 진영 상실 0–66′ **68건 → 오른쪽 2·왼쪽 3** · 66′– 32건 → 오른쪽 1·왼쪽 0 · 자기 진영 상실 0–66′ 59건 → 오른쪽 10·중앙 13·왼쪽 12. **예외 1건**: 30′58″ 알리송이 오른쪽 높은 곳(78,10) 드리블 상실 → 로빈슨이 빌라 오른쪽으로 끌고 간 역습 → 32′ 보브 빅찬스(xG 0.21 · 스즈키 선방) — 풀럼 공식 「A blistering counter attack spearheaded by Antonee Robinson」(로빈슨이 이끈 맹렬한 역습) · 실점은 코너 자책골(전환 실점 0) | **부분 일치** — 빈도로는 불일치(2 vs 3), 결정적 장면 1건은 일치. 단 RM이 **중앙에 있어서가 아니라 오른쪽 폭에서 볼을 잃은 뒤** RM·RB 뒤 공간을 상대 LB가 쳤다 |
| H2 | 빌라 오른쪽이 비고 오른쪽 라인이 자주 뚫린다 | **부분 일치**(양은 왼쪽 · 결정적 장면 오른쪽) | ⑵ 풀럼 파이널서드 터치 0–66′ 빌라 **오른쪽 62 · 중앙 30 · 왼쪽 60**(양은 대칭) · 오픈플레이 크로스 출발 **오른쪽 9 : 왼쪽 2** · 로빈슨 볼 터치 (48,86) · 이워비 (65,74) · 빌라 오른쪽 수비 액션 캐시 13건 (38,30) · 알리송 12건 **(49,22)**(하프라인 부근) · WLS 「He constantly got in behind Matty Cash」(계속 캐시 뒤를 파고들었다) · Fulhamish 「using his pace to evade Cash and the backtracking Alysson」(속도로 캐시와 뒤따라 내려오던 알리송을 따돌렸다) · **66′ 음바예 투입 뒤 풀럼 오픈플레이 크로스 0** · 파이널서드 터치 오른쪽 12·왼쪽 7·중앙 7 | **부분 일치** — 양은 대칭, 크로스·배후 침투의 질은 오른쪽 집중. 원인은 **상대 LB 로빈슨의 오버래핑 vs 캐시+알리송 2인 대응**(본머스전 원인은 임시 RB 보가르드의 배후 대응) |
| H3 | 상대는 반대 전환으로 빌라 오른쪽을 공략한다 | **부분 일치**(오른쪽 효율 높음 · 빈도는 왼쪽) | 풀럼 긴 측면 전환(가로 Δy≥50) 0–66′: 빌라 오른쪽으로 **5(성공 5)** · 왼쪽으로 5(성공 2) · 66′–: 오른쪽 1 · 왼쪽 4 · 풀럼 슈팅 직전 패스 출발: 빌라 오른쪽 5(코너·프리킥 포함) · 왼쪽 4 · 중앙 5 | **부분 일치** — 오른쪽으로 보낸 전환은 정확했다(5/5). 주 경로는 전환보다 **같은 쪽 로빈슨 전진** |

⇒ **두 경기 종합(판정 뒤 · 사용자 판단 대기)**: 「RM이 안쪽으로 들어가 전환 때 오른쪽이 빈다」는 두 경기 모두 이벤트로는 약하다(전환 진입 오른쪽 0/34 · 2/68). 반복된 것은 **빌라 오른쪽 배후가 상대 측면 자원(본머스 솔레르 · 풀럼 로빈슨)에게 뚫리는 것** — RB(보가르드 → 캐시)와 RM(음바예 → 알리송)의 2인 대응이 상대 LB/LW 오버로드를 못 받는다. 게임 함의 후보: RM 역할을 바꾸기보다 **RB 포커스(캐시 정본 fb_wingback/Balanced)를 더 보수적으로** 또는 RDM(카마라) 오른쪽 커버 — 근거 등급: 실측(이벤트) · 「포커스를 낮추면 복귀가 늘어난다」는 **D(통설)**. 쟁점 #13(풀백 비대칭)·#14(알리송 측면 기용) 표본으로 기록.

## ⭐ 이월 확인 대조표 (본머스전 D+3 → 이 경기)

| # | 이월 항목 | 실측 | 판정 |
|---|---|---|---|
| C1 | 가르나초 소집·교체 서열(obs#1135·#1136) | **소집 · 87′ 다섯 번째(마지막) 교체**(맥긴 아웃 · LM, 부엔디아 CAM 이동) · Tanswell 「Alejandro Garnacho is #AVFC's fifth sub. He replaces John McGinn. Three minutes of normal time remaining.」(가르나초가 다섯 번째 교체로 맥긴 대신 투입. 정규시간 3분 남음) · 9′ 볼 터치 4 · 슈팅 블록 1(xG 0.10) · 66′ 첫 묶음은 음바예·부엔디아·고메스 | **일치(리그 하위 서열)** — 본머스전(컵) 58′ 1순위 교체와 갈린다 → 컵/리그 서열 분리. 팬 채널은 투입이 늦었다고 지적(UTV) |
| C2 | 본머스전 중점 5인 중 출전자 | **고레츠카 LDM 66′(첫 PL 선발)** · **음바예 66′ 교체 RM 24′** · 마조·하우드-벨리스 **벤치 미출전** · 헤밍스 명단 밖 | 아래 「중점 5인 출전 맥락」 |
| C3 | 만잠비 복귀(본머스전 「not only rest」(휴식만은 아니다) · obs#1152) | **LM 선발 66′ · 39′ 도움** · AVN 8 「the real MVP」(진짜 MVP) | 일치(주전 복귀) |

### 중점 5인 출전 맥락 (본머스전 → 풀럼전)
- **고레츠카**: 로테이션 컵 선발(LDM) → **리그 첫 선발도 LDM**(카마라와 짝 · avfc 「The German begins alongside Boubacar Kamara in midfield」(카마라와 나란히 중원에 선다) · 스니펫). 볼 터치 (49,57) · 패스 16/19 · 슈팅 3 블록 · 13′ 헤더가 PK 유도 · 66′ 교체. **쟁점 #25 2/2 → 판정(아래)**. 팬 채널 「he didn't do anything wrong, but what did he do right?」(잘못한 건 없지만 잘한 건 뭐였나 · UTV auto-caption).
- **음바예**: 컵 선발 RM 58′ → **리그 교체 RM 24′**(로테이션 복귀 아님 · 66′ 첫 묶음). 볼 터치 21 중 19 오른쪽 · 경합 3/3 · AVR 「Looked Villa's only route to a winner」(빌라의 유일한 결승골 경로로 보였다). 선발이 아니라 #6(2/3)·#7(1/2)·#48(1/2) 진행도 불변.
- **하우드-벨리스**: 벤치 미출전 — RCB 린델뢰프 · LCB 토레스가 PL 주전. #24(0/2)·#58(0/2) 불변.
- **마조**: 벤치 미출전(잭슨 90′). #80(0/2) 불변.
- **헤밍스**: 명단 밖(SS 라인업·결장 목록 모두 없음 · 사유 1차 소스 0 → D+1).

## 1. 경기 개요와 원천 수치

| 항목 | 빌라 | 풀럼 |
|---|---|---|
| 점유(전반/후반) | 45(47/43) | **55**(53/57) |
| xG(FotMob · 오픈/세트/PK) | 1.71(0.54/0.38/0.79) | **2.21**(1.39/0.82/0) |
| 논PK xG · xGOT | 0.92 · 0.48 | 2.21 · 1.72 |
| 슈팅(유효 · 블록) | 16(3 · 6) | 14(5 · 3) |
| 빅찬스(득점) | 4(1) | 4(0) |
| 패스(정확) | 433(373) | 535(473) |
| 롱볼 | 20/36 | 27/41 |
| 크로스 | 6/17 | 6/18 |
| 코너 | 7 | 7 |
| 경합 % · 지상 · 공중 | 52 · 35/63 · 9/21 | 48 · 28/63 · 12/21 |
| 후반 지상 · 공중 | 12/28 · **3/13** | 16/28 · 10/13 |
| 드리블 | 7/16 | 7/16 |
| 태클 · 가로채기 · 클리어 | 17 · 5 · 15 | 15 · 13 · 27 |
| 상대 박스 터치 | 24 | **40** |
| 오프사이드 | 2 | 4 |
| GK 세이브 · goalsPrevented(SS) | 4 · +0.72 | 2 · −0.52 |
| PPDA(WS) | **20.94**(전반 15.58 · 후반 31.67) | 12.84(13.75 · 12.0) |
| 수비 액션 평균 높이(def_x)(WS) | 40.3 | 36.4 |

- **득점 국면**: 0-0 0–39′ · 1-0 39–64′ · 1-1 64′– → `phase_level 65 · phase_lead 25 · phase_trail 0`(분).
- **교체**(SS incidents): 빌라 66′ 고메스·부엔디아·음바예(만잠비·알리송·고레츠카 아웃) · 79′ 바클리(카마라) · 87′ 가르나초(맥긴) / 풀럼 75′ 캐어니(이워비) · 79′ 팔라시오스(킹)·테테(보브) · 87′ 라르손(카스타뉴)·무니스(가르시아). ⚠️ **66′ 교체 짝이 갈린다** — SS·클럽 기록은 고레츠카→음바예 · 알리송→부엔디아 · 만잠비→고메스, **WS formation 슬롯(위치)**은 알리송→음바예(슬롯 7) · 고레츠카→고메스(슬롯 4) · 만잠비→부엔디아(슬롯 11). 처방·분석은 위치 짝을 쓴다(BirmLive·AVR 서술과 일치).
- **경고**: 빌라 캐시 76′(**시즌 5장 → 11-08 맨유전 출장 정지**) / 풀럼 아펜그루버 30′ · 바시 45+4′ · 캐어니 77′.
- **결장**: 완비사카(햄스트링 · 에메리 「Maybe Wan-Bissaka is coming back next week」(완비사카가 다음 주 돌아올 수도 있다)) · 오나나(시즌 아웃 · Read Aston Villa 프리뷰) · 루게리(햄스트링 한 달+). 벤치 미출전: 비조 · 하우드-벨리스 · 밍스 · 마조. 명단 밖: 헤밍스(사유 미확인).
- **수집**: SS `/event/16363901/{,statistics,incidents,shotmap,lineups,managers,graph,average-positions}` + 선수 히트맵·평균 위치(collect_event.py headless — 403 없음) · FotMob 5795496(xG 4종 동시 스냅샷 · 하프별) · WS 1983627 headful 전체 JSON(1,580건). PL이라 슛 xG는 SS(`match_shots` provider=SofaScore · 31). 히트맵 기준(45분+ · hit_points 15+) 통과: 선발 11명 전원(잭슨 35·알리송 34 · 교체 5명은 45분 미만).

## 2. 전술 설명

### 점유 구조·빌드업
- 4-2-3-1 · 양 풀백 폭(마첸 볼 터치 (49,85) · 캐시 (51,20)) · 피벗 카마라 오른쪽 (47,34) · 고레츠카 왼쪽 (49,57).
- 후방 순환 축은 **토레스→린델뢰프 27 · 린델뢰프→토레스 20** → **린델뢰프→캐시 21** · 캐시→맥긴 9 — 오른쪽 출구(본머스전 밍스–마트센 왼쪽 축과 반대). 볼 소유 레인(x≥33) 전반 왼쪽 37·중앙 26·오른쪽 38% → 후반 30/27/**43%**.
- **맥긴 10번이 오른쪽 하프스페이스로 기울고**(볼 터치 29 · 오른쪽 62% · (70,25)) 알리송이 폭 — 오른쪽 2인. 왼쪽은 **잭슨이 내려와**(SS 평균 54,60 · 볼 터치 (60,65)) 만잠비 (57,75)와 연결 — 선제골이 이 경로.
- 스즈키 패스 36(롱 8 · 성공 5) · 스위핑(KeeperSweeper) 0 · 박스 밖 비패스 행동 1.
- 상대 시각: Fulhamish 「Villa's main strategy was aerial attacks to their pacey forwards」(빌라의 주 전략은 빠른 전방으로 보내는 공중볼이었다).

### 비점유 구조·압박
- 4-4-1-1. 0–15′ 수비 액션 평균 높이(def_x) **62.8** · PPDA 9.71로 높게 출발 — Fulhamish 「Berge and Charles moving amongst the backline to try and help the team wriggle away from a high press」(베르게·찰스가 백라인 사이로 내려와 하이프레스를 벗어나려 했다).
- 16–30′ 수비 액션 평균 높이(def_x) 48.5 → 30–39′ 32.0 → **리드 뒤 39–45′ 19.6 · 45–60′ 24.8** · 후반 PPDA 31.67. 에메리 「we were not keeping the same consistency with ball possession」(전반 같은 점유의 일관성을 유지하지 못했다) · 「I want to watch the game to understand better why we couldn't in the second half… Why? I can't understand now」(후반에 왜 안 됐는지 경기를 다시 봐야겠다… 왜인지 지금은 모르겠다 · BirmLive 전문).
- 오른쪽: 캐시 수비 액션 13 (38,30) · 알리송 12 (49,22) · 카마라 14 (33,43) — 로빈슨·이워비 2인을 캐시·알리송이 받고 카마라가 안쪽에서 커버.

### 전환·rest-defense·세트피스
- 상대 진영 볼 상실 100건 뒤 10초 안 풀럼의 빌라 수비 3분의 1 진입 **6건**(오른쪽 3·왼쪽 3) — rest-defense 자체는 버텼다. 예외 32′ 보브 빅찬스(위 H2′).
- 빌라 역습 득점: 38′43″ 카스타뉴 볼 처리 실수 → 만잠비 (55,41)→(72,72) 스루패스 → 잭슨 드리블 2회 → 38′49″ 득점(6초).
- **세트피스**: 풀럼 세트 xG **0.82** · 33′ 코너 헤더 2 · 54′ 찰스 코너 빅찬스(xG 0.64 · 라인 위 블록) · 60′ 아펜그루버 헤더 · **64′ 코너 → 스즈키 자책** · 77′ 프리킥 헤더. 빌라 세트 xG 0.38(고레츠카 코너 헤더 2 · 막판 토레스 헤더 2) + PK 0.79. `match_set_pieces` 23행.

## 3. 전술적 특성

- **강점**: ⑴ 전반 통제(xG 1.20–0.60 · 지상 경합 23/35 · 공중 6/8) ⑵ 잭슨 개인 마무리(드리블 3/3 · 박스 안 2명 제침) ⑶ 스즈키 선방 4(goalsPrevented +0.72) ⑷ 마첸 왼쪽 폭 출구(깊은 수신 13 · 팬 채널 「our best attacking outlet in the second half was maybe Maatsen」(후반 최고의 공격 출구는 마트센이었다 · 1874 auto-caption)).
- **약점**: ⑴ **후반 압박·강도 소멸**(PPDA 31.67 · 후반 공중 3/13) — Tanswell 「Fulham had almost double the number of touches in the attacking box, more big chances, higher xG & completed over 100 more passes, despite setting up to let Villa have the ball. Lack of intensity in decision-making」(풀럼은 빌라에 공을 내주는 셋업이었는데도 박스 터치가 거의 두 배, 빅찬스·xG가 더 많았고 패스를 100개 넘게 더 성공했다. 판단에 강도가 없었다) ⑵ **빌라 오른쪽 배후(로빈슨)** ⑶ PK 실축(키커 = 에메리 「We have our analysis about penalty shooters, and it was McGinn who was the taker today.」(키커 분석이 있고 오늘의 키커는 맥긴이었다)) ⑷ 세트피스 실점(자책).
- **상대가 만든 교란**: 아르벨로아 하프타임 지시 「We have to be more aggressive… especially when you go man to man.」(더 공격적이어야 한다… 특히 대인 대결에서 · 풀럼 공식) → 후반 경합 역전. 「'Jedi' was fantastic tonight.」('제다이'(로빈슨)는 오늘 환상적이었다 · WLS).
- **직전 경기 대비**: 4-2-3-1·4-4-1-1 같음. 빌드업 출구가 왼쪽(밍스–마트센) → **오른쪽(린델뢰프–캐시)**. 「후반 첫 15분 강도」 약점은 본머스전(「the first 15 minutes of the first and second half」(전반·후반 첫 15분))과 **같은 패턴 2경기 연속**(팬 채널은 포레스트전까지 묶어 3번째로 서술).

## 4. 경기 중 변화

1. **0–15′ 높은 출발**: 수비 액션 평균 높이(def_x) 62.8 · PPDA 9.71. 5′ 이워비 역습 슈팅(xG 0.30).
2. **13–16′ VAR PK → 맥긴 크로스바**(xG 0.79).
3. **16–39′ 통제 속 풀럼 역습·세트**: 32′ 보브 빅찬스(로빈슨 역습 · 스즈키 선방) · 33′ 코너 헤더 2 → **39′ 잭슨 1-0**.
4. **39–64′ 리드 뒤 블록 하강**: 수비 액션 평균 높이(def_x) 19.6~24.8 · 모멘텀 51–59′ −38.0 · 54′ 찰스 코너 빅찬스 · 60′대 이워비 헤더·가르시아 슈팅 연속 선방 → **64′ 코너 자책 1-1**.
5. **66′ 3명 동시 교체**(음바예 RM · 부엔디아 LM · 고메스 LDM) → 66–82′ 모멘텀 −26.1 · 79′ 바클리(고메스 RDM) · 87′ 가르나초 LM(부엔디아 CAM) · 83–90′ 모멘텀 +25.4. 형태 4-2-3-1 유지 · 음바예 쪽 크로스 허용 0 · 빌라 후반 xG 0.51.

## 5. 선수별 분석 — 출전 선수 전원

| 선수 | 위치·실제 역할 | 분/평점·핵심 스탯 | 평균 위치(SS)·볼 터치(WS) | 특성·수행 | FC 역할/포커스 함의(FC27 커널 · 단일 경기) |
|---|---|---|---|---|---|
| 스즈키 | GK | 90′ SS 9.1 · FM 7.69 · 패스 30/33 · 롱 5/8 · 세이브 4 · 스위핑 0 | (9,50) | 32′ 보브·45′ 킹 1대1 전진·63′ 이워비 헤더 선방 · ⚠️ 64′ 자책 | gk_goalkeeper/Defend .939(Δ.008 무결정) · 정본 gk_ballplaying/Build-Up .728 |
| 캐시 | RB · 잔류측 | 90′ SS 7.2 · FM 7.3 · 패스 47/57 · 태클 3 · 76′ 경고(5장) | (46,20) · 볼 터치 오른쪽 87% · 수비 (38,30) | 로빈슨 배후 침투 허용(WLS) | fb_wingback/Support .839(Δ.000 무결정 · 2위 att_wb/Support) · 정본 wingback/Balanced .803 |
| 린델뢰프 | RCB · 순환 축 | 90′ SS 7.2 · 패스 **74/77** · 롱 5/5 · 운반 44회 282m | (34,37) · 수비 (29,40) | 63′ 가르시아 슈팅 블록 | cb_bpd/Aggressive .954(**Δ.131 결정**) = 정본 |
| 파우 토레스 | LCB · 전개측 | 90′ SS 6.5 · 패스 62/69 · 운반 추정 전진 188m · 헤더 2 빗나감 | (36,68) | 풀럼이 시간을 줌(AVR) | cb_bpd/Aggressive .892(Δ.090) · 정본 bpd/Build-Up .802 |
| 마첸 | LB · 왼쪽 폭 | 90′ SS 6.8 · FM 7.3 · 패스 29/34 · 공중 2/2 · 상실 12 | (51,81) · 깊은 수신 13 | 후반 공격 출구 | fb_att_wb/Support .902(**Δ.133 결정**) = 정본 |
| 카마라 | RDM · 앵커 | 79′ SS 7.1 · FM 7.24 · 지상 8/10 · 태클 4 | (44,36) · 수비 (33,43) | 30야드 탈취 → 고레츠카 슈팅(AVR) | dm_dlp/Roaming .588(Δ.005 무결정 · 2위 boxcrasher/Balanced) · 정본 holding/Defend .541 |
| 고레츠카 | LDM · 첫 PL 선발 | 66′ SS 6.5 · FM 6.25 · 패스 16/19 · 슈팅 3(블록) | (52,58) · 볼 터치 중앙 61%·왼쪽 32% | 13′ 헤더 → PK | dm_dlp/Roaming .542(Δ.020 무결정) = 정본 · 보유 1위 dlp/Build-Up .652 |
| 알리송 | RM · 폭 | 66′ SS 6.5 · FM 6.67 · 패스 **4/6** · 스프린트 23(팀 최다) · 상실 11 | (62,22) · 오른쪽 83% · 수비 (49,22) | 39′ 흘려주기 · 후반 존재감 소멸(BirmLive) | wm_winger/Attack .599(Δ.023 무결정) = 정본 · 보유 .733(Δ.194 결정) |
| 맥긴 | CAM → 오른쪽 하프스페이스 | 87′ SS 6.2 · FM 6.77 · **16′ PK 크로스바** · 키패스 4 · 크로스 2/8 · 상실 14 | (71,23) · 오른쪽 62% | 어수선한 경기에서 존재감 부족(AVR) | cam_halfwinger/Attack .670(Δ.001 무결정) · 정본 playmaker/Roaming **.255** |
| 만잠비 | LM · 안쪽 연결 | 66′ SS 6.9 · FM 7.51 · **39′ 도움** · 경합 5/12 · 상실 12 | (55,76) · 왼쪽 82% · 전진 수신 12 | AVN 8 「the real MVP」(진짜 MVP) | wm_wideplm/Attack .718(Δ.056) · 정본 insidefwd/Balanced .662 |
| 잭슨 | ST → 왼쪽 하강 | 90′ **SS 8.5** · FM 7.92 · **39′ 득점** · 드리블 3/3 · 경합 7/9 | (54,60) | 등지는 터치(AVR) · 시즌 8호 | st_advanced/Versatile .467(Δ.026 무결정) · 정본 Support .419 |
| 주앙 고메스 | LDM → 79′ RDM | 24′ SS 6.6 · 패스 13/16 | (55,41) | 기동력·에너지(BirmLive) | 리포트용 — 보유 1위 dm_dlp/Roaming |
| 음바예 | RM(66′~) · 폭 | 24′ SS 6.8 · 경합 3/3 · 드리블 1/1 | (63,13) · 오른쪽 90% · 수비 (52,11) | 「only route to a winner」(유일한 결승골 경로 · AVR) | 리포트용 — 보유 1위 wm_winger/Balanced .895 |
| 부엔디아 | LM(66′~) → 87′ CAM | 24′ SS 6.6 · 크로스 2/2 · 키패스 2 | (61,56) 안쪽 | 토레스 헤더 프리킥 | 리포트용 — 보유 1위 wm_wideplm/Attack |
| 바클리 | LDM(79′~) | 11′ SS 6.5 · 패스 6/7 | (58,57) | 팬은 더 일찍 투입 요구 | 리포트용 |
| 가르나초 | LM(87′~) | 9′ SS 6.7 · 슈팅 1 블록 · 크로스 1/1 | (79,69) | 다섯 번째 교체 | 리포트용 |

45분 미만 교체 5명은 리포트 근거로만 쓰고 대표 그리드·처방 집계에는 넣지 않는다. 평점(10점): 만잠비 AVN 8 · 잭슨 dave.sport 8 · 스즈키 AVN 4 ~ 4thOfficial 7(가장 갈림).

## 6. 전술 변화 판정

- **유지**: 4-2-3-1 · 비보유 4-4-1-1 · 양 풀백 폭 · 더블 피벗(카마라 + 1).
- **새로 나타난 것**: 고레츠카 리그 LDM(#25 확정) · 맥긴 10번의 오른쪽 기울기 + 잭슨 왼쪽 하강(왼쪽 연결 경로) · 빌드업 출구 오른쪽(린델뢰프–캐시).
- **반복된 약점**: 하프 시작 강도(본머스전에 이어) · 빌라 오른쪽 배후.
- **`manager_profiles` 반영**: **pressing 축 덧붙임** — 리드 뒤 블록 하강·후반 압박 소멸이 맨시티(리드 수비 액션 평균 높이(def_x) 20.4~32.2)에 이어 2번째 리드 경기에서 재현(39–64′ 수비 액션 평균 높이(def_x) 19.6~24.8). 의도(리드 보호)인지 실패인지는 에메리 자신도 「Why? I can't understand now」(왜인지 지금은 모르겠다) — 성향으로 단정하지 않고 사실만 덧붙였다. 나머지 축 갱신 불필요(단일 경기).

## 7. 게임 구현 판정

- 결론: **추가 관찰**.
- **이 경기 전용 팀 설정**(`match_game_setups` #65 · match_only): FC27 · 4-2-3-1 Wide · 빌드업 **Balanced** · 수비 접근 **Deep** · 라인 **40** · `core.team_settings.suggest(45, 433, 36, 20.94)` → Balanced/Deep/0~45 · `compare()` 차이 0 → rule_note **RULE** · 보유 4-2-3-1 / 비보유 4-4-1-1. ⚠️ Deep은 후반 압박 실패를 재현한 값이지 처방 근거가 아니다(전반 0–30′은 High에 가까웠다).
- **선발 11명**(`match_player_prescriptions` · FC27 커널 1위 · 무결정은 2위 병기 · 보유/비보유 분리 적합은 `load_fit_poss.py`):

| 칸 | 선수 | 역할/포커스 | fit | Δ | 2위 | 보유 1위 | 정본과 |
|---|---|---|---|---|---|---|---|
| GK | 스즈키 | gk_goalkeeper/Defend | .939 | .008 무결정 | goalkeeper/Balanced | 같음 | 다름(정본 BPK .728) |
| RB | 캐시 | fb_wingback/Support | .839 | .000 무결정 | att_wb/Support | att_wb/Support .884 | 다름(정본 wingback/Balanced .803) |
| RCB | 린델뢰프 | cb_bpd/Aggressive | .954 | **.131** | stopper/Aggressive | 같음 | 같음 |
| LCB | 파우 토레스 | cb_bpd/Aggressive | .892 | .090 | bpd/Build-Up | 같음 | 다름(정본 Build-Up .802) |
| LB | 마첸 | fb_att_wb/Support | .902 | **.133** | wingback/Balanced | 같음 | 같음 |
| RDM | 카마라 | dm_dlp/Roaming | .588 | .005 무결정 | boxcrasher/Balanced | boxcrasher/Balanced .521 | 다름(정본 holding/Defend .541) |
| LDM | 고레츠카 | dm_dlp/Roaming | .542 | .020 무결정 | dlp/Build-Up | dlp/Build-Up .652 | 같음 |
| RM | 알리송 | wm_winger/Attack | .599 | .023 무결정 | insidefwd/Attack | 같음 .733(Δ.194) | 같음 |
| CAM | 맥긴 | cam_halfwinger/Attack | .670 | .001 무결정 | halfwinger/Roaming | halfwinger/Roaming | 다름(정본 playmaker/Roaming **.255**) |
| LM | 만잠비 | wm_wideplm/Attack | .718 | .056 | insidefwd/Balanced(정본) | 같음 .783 | 다름(정본 .662) |
| ST | 잭슨 | st_advanced/Versatile | .467 | .026 무결정 | target/Balanced | 같음 | 다름(정본 Support .419) |

- `prescriptions`·`slot_canon_roles`·`team_tactic_setups` 변경 **없음** — 단일 경기 · 무결정 7칸. 등급: 커널 적합 = 실측(우리 계산) · 「Defend/Support 포커스 = 덜 올라간다」류 해석은 **D**. FC26 사실 전용 없음.
- 다음 경기 재검증: ⑴ 바르사(11-03 UCL) RM 선발과 오른쪽 배후 대응 ⑵ 맨유(11-08) **캐시 출장 정지** — RB 대체(에메리 「he will decide on who replaces Matty Cash after Barcelona」(바르사전 뒤 캐시 대체를 정하겠다 · Tanswell)) ⑶ 리드 국면 블록 높이 3번째 표본.

## 8. 영상·기사·감독 발언

### 감독 1차 발언
- **에메리 — avfc.co.uk 「Emery's thoughts on Fulham's draw」(10-31 · 직접 열람)**: 「It's a disappointing result, a fair result.」(실망스러운 결과지만 공정한 결과다) · 「Sometimes we conceded some transitions and some actions… They were breaking our press and we needed our goalkeeper, Zion Suzuki, saving some actions.」(가끔 전환과 몇몇 장면을 허용했고… 그들이 우리 압박을 깨고 나왔으며 스즈키의 선방이 필요했다) · 「The second half in the first 20 minutes, they were pushing, they were dominating… we were not keeping the same consistency with ball possession」(후반 첫 20분은 그들이 밀어붙이며 지배했다… 우리는 같은 점유의 일관성을 유지하지 못했다) · 「It's one stop in our progression… still being in the middle of the table.」(성장 과정의 한 정거장이다… 아직 중위권이다).
- **에메리 — Birmingham Live 회견 전문(John Townley · 10-31 22:59 GMT · 직접)**: 캐시 대체 「Maybe Wan-Bissaka is coming back next week… we have five days until Sunday to prepare and identify how we can replace Wan-Bissaka if he is not available.」(완비사카가 다음 주 돌아올 수도 있다… 안 되면 일요일까지 닷새 동안 대체 방법을 찾겠다 — 문맥상 캐시 대체) · PK 「We have our analysis about penalty shooters, and it was McGinn who was the taker today.」(키커 분석이 있고 오늘의 키커는 맥긴이었다) · 「I want to watch the game to understand better why we couldn't in the second half… Why? I can't understand now」(후반에 왜 안 됐는지 다시 봐야겠다… 왜인지 지금은 모르겠다) · 일정 「It is not an excuse… We have players to rotate」(핑계가 아니다… 로테이션할 선수가 있다).
- **에메리 — PA(Irish News·E&S 동일 · 직접)**: 「It's part of football… I prefer to speak about the save he did.」(축구의 일부다… 그의 선방을 얘기하고 싶다) · 「We are understanding the team better, the players in our structure. We are adapting, but still work to do.」(우리 구조 속 선수들을 더 잘 이해해 가고 있다. 적응 중이지만 할 일이 남았다).
- **에메리 — Sky(직접)**: 「they dominated more in the second half, they created chances and they scored a goal.」(후반엔 그들이 더 지배했고 기회를 만들어 골을 넣었다).
- **아르벨로아 — 풀럼 공식 회견(Geoff Pruce · 10-31 · 직접)**: 「We have to be more aggressive… especially when you go man to man.」(더 공격적이어야 한다… 특히 대인 대결에서) · 「we are a team that wants to control the game with the ball」(우리는 공으로 경기를 통제하려는 팀이다) · 「we need to be a little bit lucky – we were today with the goal」(조금은 운이 필요하다 — 오늘 골은 운이 따랐다) · PA 「since the first minute of the second half, we saw that we can beat anyone」(후반 첫 1분부터 누구든 이길 수 있다는 걸 봤다) · Sports Mole 「It was a Champions League team in front of us.」(챔스 팀이 앞에 있었다).
- 66′ 3명 교체 사유 · 고레츠카·만잠비·알리송·음바예·가르나초 개별 언급: 4개 출처 모두 **0**.

### Jacob Tanswell (X @J_Tanswell · 브라우저 직접 열람 · 비로그인 최신 5건)
- FT 총평(11-01 06:57 KST · status 2116650682615021946): 「A dire second half. Villa looked in control early on but then it felt complacent. … Lack of intensity in decision-making… Cash suspended for Man United, too」(끔찍한 후반. 초반엔 통제했지만 이후 안이했다 … 판단에 강도가 없었다… 캐시는 맨유전 징계).
- 가르나초 다섯 번째 교체(…2116648458849493345 · 위 C1) · 스즈키 회견 인용(…2116663319054676197) · 완비사카(…2116663575737680038): 「Emery says Aaron Wan-Bissaka may be available for next week at Old Trafford, but if not, he will decide on who replaces Matty Cash after Barcelona.」(완비사카가 다음 주 올드 트래퍼드전에 가능할 수 있고, 아니면 바르사전 뒤 캐시 대체를 정하겠다).
- 미수행: The Athletic 기사(도메인 차단) · nitter(서비스 중단 공지).

### 기사·평점
- PA(Jonathan Veal · AOL/Irish News 직접) · Guardian(Peter Lansley · AOL 직접) · Sky(직접) · 풀럼 공식 리포트 · Fulhamish(Owen Macdonald · 직접) · WLS 리포트·평점(직접) · 평점 BirmLive(Townley)·AVN(Carr)·AVR(Nee)·dave.sport(Chettle)·4thOfficial(스니펫)·Mecze24. avfc 리포트·프리매치는 **스니펫**(CloudFront 오류).
- 자책골 서술 충돌: 영어권 「completely uncontested」(완전히 경합 없음 · BBC 계열 스니펫) vs FOOTBALL ZONE(일본어 · 직접) 「相手選手と接触して落球」(상대 선수와 접촉해 공을 떨어뜨렸다) — 접촉 서술은 1곳뿐 · 영상 확인은 D+1.

### 다국어 (불변규칙 10)
- **스페인어(에메리 필수)**: 에메리 스페인어 발언 **0** — 영어 회견만 존재 · Marca·AS·Relevo·El País·MD 도메인이 검색 도구에서 차단(미수행 사유) · EFE(Unitel 전재)는 PK를 「segunda mitad」(후반)로, 스즈키가 「Kevin」(케빈 · 실제 벤치)을 막았다고 써 신뢰도 낮음. FDP Radio(직접) 「con un cabezazo de Pau Torres cerca del palo」(골대 옆을 스친 파우 토레스의 헤더로). ⚠️ 스페인어 검색에 에메리 발언으로 붙은 「este es el equipo que queremos ser」(이게 우리가 되고 싶은 팀이다)는 원문 확인 결과 **아르벨로아** 발언 — 쓰지 않는다. 아르벨로아 스페인어 원문 0.
- **일본어(스즈키)**: フットボールチャンネル(직접) 「鈴木が好セーブで阻止」(스즈키가 선방으로 막았다) · FOOTBALL ZONE 「鋭い飛び出し」(날카로운 전진 · 45′ 킹) · 닛칸 마트센 발언 「彩艶は素晴らしいGKです。今回の経験から学び、彼をサポートして次の試合に臨む」(사이언은 훌륭한 GK다. 이번 경험에서 배우고 그를 지지하며 다음 경기에 임하겠다 · 영어 원문 미확보). 이탈리아어(파르마) 0.
- **독일어**: LAOLA1(아펜그루버 · 직접) 「Allerdings überquert der Ball bei dieser versuchten Abwehraktion die Torlinie - ein Geschenk für Fulham.」(그 처리 과정에서 공이 골라인을 넘었다 — 풀럼에 준 선물) · 고레츠카 kicker·Bild·Sport1·tz·AZ·Sky DE **0**.
- **프랑스어**: ATS/bluewin(만잠비 · 직접) 「l'international helvétique a vu son ballon en profondeur être sublimé par son attaquant Nicolas Jackson」(스위스 대표의 침투 패스를 잭슨이 빛나게 마무리했다) · wiwsport(잭슨 · 직접) 「Jackson s'est joué de la défense de Fulham en réalisant un joli enchaînement avant de battre le gardien adverse.」(잭슨이 멋진 연속 동작으로 풀럼 수비를 농락한 뒤 골키퍼를 꺾었다) · 카마라 L'Équipe 제목만(스니펫) · 음바예 Dsports 「entré à la 67e」(67분 투입) 행동 서술 없음.
- **폴란드어(캐시)**: Sportowefakty(직접) 「Matty Cash pozostał na murawie do końca spotkania.」(캐시는 끝까지 그라운드에 남았다) — 후반 수비 부담 서술.
- **0건**: 스웨덴어(린델뢰프 3종) · 네덜란드어(마트센 VI·AD·Telegraaf) · 포르투갈어(알리송 ge.globo·UOL·Lance · Placar 1건은 알리송 언급 0) · 아르헨티나(가르나초 Olé·TyC) · 스코틀랜드(맥긴 Daily Record).

### 영상 (필수 채널 3곳)
- UTV 「SECOND HALF HORROR SHOW FROM ASTON VILLA」(6bwxQlWU3bk · 11-01 · 18:00 · yt-dlp 429 → **브라우저 pot 경로 · 뮤트**) → `match_videos` #464.
- 1874 「Aston Villa v Fulham | Suzuki OWN GOAL Halts Villa's Home Winning Run」(ZPtfGsSLb94 · 11-01 · 30:28 · yt-dlp 자막) → #465.
- 건너뜀: 프리뷰 3(UTV weXKU3b6L1M · The Villans EUhuiiN4cJA · 1874 FhbYRUQRi_8) · UTV 쇼츠 2(1VHGVzTp3TM · QnnNeNRY-9k). **The Villans 경기 후 영상 0**(영상·라이브·쇼츠 탭 확인) → D+1.
- 다른 채널(제목·설명 기준 · 미전사): All Villa No Filler B_VjoBqVn8A · Villa in NOIR 7Dx2zNHRq_A · 풀럼 쪽 Fulhamish UOsofuOP5B8 · talkSPORT f9c_RxiSWBE · 일본어 ロスタイムズ 3xl4TCp716U · TOTAL FOOTBALL ZwvnXUvYl74 → D+1~D+2 후보.

### 영상 요약 (전사 2편 · `match_videos` #464·#465 · 구현 주장 8행 · auto-caption)
- **#464 UTV 리액션**: 「전반 지배·후반 붕괴」가 포레스트전과 같은 패턴 · 후반 문제 ⑴ 경합 열세 ⑵ 「the two wide players in Manzambi and Allison weren't protecting the fullbacks at all」(두 측면 만잠비·알리송이 풀백을 전혀 보호하지 않았다) · 팬 「Manzambi and Allison had a really tough night tracking those runners … fullbacks isolated」(만잠비·알리송이 그 러너들을 따라가는 데 애먹었고 풀백이 고립됐다) · PK 키커를 잭슨으로 고정하자는 주장. ⇒ 실측: 알리송(오른쪽) 쪽은 크로스 9로 **같은 방향**(주장 HELD #14), 만잠비(왼쪽) 쪽은 크로스 2로 **불일치**(REJECTED).
- **#465 1874 리액션 라이브**: 맥긴 부진 = 팀 부진 패턴 · 2선 3명 후반 부진 · 늦은 교체 · 스즈키 옹호 · 최고 선수 마첸 · 알리송이 오히려 캐시 앞 RB 높이까지 내려앉았다(UTV와 **반대 서술** · 실측 수비 액션 (49,22)은 어느 쪽과도 딱 맞지 않음 → HELD #16) · 만잠비 왼쪽 채널이 맞다(HELD #49).
- 주장 8행: HELD 6(#14 · #59 · #16 · #47 · #49 · #5) · REJECTED 1 · NA 1(PK 키커 — 설정 축 밖).

## 9. 데이터 반영과 한계

- DB(행 추가): `matches` #129 · `player_matches` 16(국면 그리드·phase 분·SS 운반·FotMob 경기 스탯·WS 운반 추정/수신 · pulled=2026-11-01 scope=full) · `team_match_stats` 1(xG 4종 FotMob 동일 스냅샷 · PPDA·수비 액션 평균 높이(def_x)) · `match_events` 18 · `match_shots` 31(SofaScore) · `match_period_stats` 2 · `match_momentum` 92 · `match_set_pieces` 23 · `match_reports` #65(draft) · `match_player_reports` 16 · `match_game_setups` 1 · `match_player_prescriptions` 16(선발 11 + 교체 5) · `match_phase_metrics` 80 · 가설 판정 5행 · `match_videos` 2 · `video_impl_claims` 8.
- 선수 상태(§0-1): `collect_fotmob_players.py --team AVL`만 실행(CHE·LIV·ATM 수집 보류).
- 집계(§4 · G18): measured #919(맥긴 RM) n=12→**13** — 풀럼전 명목 CAM 선발이 pos_class RAM으로 분류돼 RM 집계에 들어간다(G18 어휘표 RM←RAM) · FC27 wm_winger/Attack .7542(종전 .7454 · 2위 wideplm/Attack .726 · Δ.028 무결정) — argmax 불변 · T2 아님. T1 `refresh_eval_samples --apply` 17행 · `refresh_duty_applied` 상태 변경 0.
- **선발 처방 층 자동 산출**(export · `core.opt_starters` · obs#1148 — 손으로 고르지 않는다): 최근 공식전 5경기 슬롯 선발 최다로 CAM 부엔디아→**맥긴** · LDM 고메스→**고레츠카** · LM 음바예→**만잠비**(`tactic_change_log` #263~#265). 역할·포커스(슬롯 정본)는 불변.
- 판정 쟁점: **#25 APPLIED**(고레츠카 선발 2/2 더블 피벗 · 주장 8행 종결) · **#3 재판정 HELD**(KeeperSweeper 바이킹·맨시티·풀럼 0 → gk_ballplaying 유지 · 다음 스즈키 선발 3경기) · **#49 재판정 HELD**(만잠비 LM에서도 정본 insidefwd/Balanced가 2위권 · 다음 비CAM 선발 2경기). #6·#7·#48(음바예 선발 아님)·#24·#58(하우드-벨리스 미출전)·#80(마조 미출전) 진행도 불변. `claim_issues --due` AVL 판정할 차례 0.
- 한계: ⑴ 이벤트는 볼이 있는 순간만 — 오프더볼 복귀 속도(UTV 「tracking back sort of a slow pace」(느린 속도로 복귀))는 직접 측정 불가 ⑵ 음바예 24분 표본 ⑶ 66′ 교체 짝 출처 충돌(위치 짝 채택) ⑷ SofaScore VAR incident는 「penaltyNotAwarded」로 표기 — PA·WS(PK 실행)와 충돌, 실측·기사 채택(`match_events` note) ⑸ 스즈키 SS 9.1은 SofaScore 표시값 그대로.
- `match_reports.status` = **draft** — D+1~D+3 추적 뒤 complete 판정.

## ⭐ 슬롯 정본 보류 5건 — 재판정 표 (맨시티 10-24 · 본머스 10-28 · **풀럼 10-31** · 리서치 §1.2 형식)

obs#1123 재판정의 세 번째 열. 실측 열은 경기 프리셋(`match_player_prescriptions` #63·#64·#65)의 FC27 커널 1위·Δ·보유 그리드. ⛔ **정본(`slot_canon_roles`·`team_tactic_setups` #46)과 인게임 코드 `7ZTFKBu$37p7`는 바꾸지 않았다 — 사용자 판단 대기.**

| # | 칸·쟁점 | 정본 FC27 | 맨시티(#63 · 37% · 리드 76분) | 본머스(#64 · 51% · 로테이션 · 열세 83분) | **풀럼(#65 · 45% · 리드 25분 · PL 주전)** | 3경기 판정(제안) | 비고·등급 |
|---|---|---|---|---|---|---|---|
| ⑴ | **RDM** dm_holding/Defend vs dm_dlp/Build-Up | dm_holding/Defend | 카마라 1위 holding/Defend .779(Δ.013 무결정) · 보유 1위 dm_dlp/Defend .863 · dlp/Build-Up .673(보유 .762) | 고메스 1위 dlp/Roaming .807(Δ.206) · 보유 dlp/Roaming .855 · 정본 .437 · dlp/Build-Up .601(보유 .685) | 카마라 1위 **dlp/Roaming .588**(Δ.005 무결정 · 2위 boxcrasher/Balanced) · 보유 1위 boxcrasher/Balanced .521 · 정본 holding/Defend **.541** · dlp/Build-Up .534(보유 .471) | **여전히 갈림** — 합산 1위 DLP 계열 2/3(고메스·풀럼 카마라), 정본 holding 1/3. 풀럼전 카마라는 전 조합이 .60 아래 무결정 — 표본 약함 | ⭐ 인게임 테스트 obs#1149 카마라 RDM DLP/Build-Up 「좋았다 — 유지」(사용자 · 10-29) · 보유 그리드 DLP 우세는 풀럼전에서 깨짐(boxcrasher) · 실측 |
| ⑵ | **ST 포커스** Support vs Attack | st_advanced/Support | 잭슨 advanced/Support .375 vs Attack .267 · 보유 1위 false9/Attack .436 | 마조 advanced/Support .351 vs Attack .332(Δ.019) | 잭슨 1위 **advanced/Versatile .467** · Support .419 · Attack **.400** · 보유 Versatile .527 ≈ Support .523 > Attack .466 | **Support ≥ Attack 3/3 — 단 셋 다 fit <.50 무결정** · 풀럼전은 Versatile이 근소 1위(잭슨 왼쪽 하강) | ST 커널 적합 구조적 저조(리서치 §1.2) · 인게임 Attack 유지 여부는 사용자 판단 · 에메리 「we need him more running in behind」(더 배후로 뛰길 원한다 · 맨시티전)와 실측(내려옴)이 계속 긴장 · 실측 |
| ⑶ | **LM 역할·포커스** | wm_insidefwd/Balanced | 만잠비 1위 widemid/Defend .538(Δ.007) · 보유 1위 insidefwd/Balanced .741 · 정본 .504 | 헤밍스 1위 widemid/Support .723(Δ.060) · 정본 .369 | 만잠비 1위 **wm_wideplm/Attack .718**(Δ.056) · 2위 **정본 insidefwd/Balanced .662** · 보유 wideplm/Attack .783 vs 정본 .701 | **선수 따라 갈림** — 만잠비는 정본이 1·2위권(보유 기준 맨시티 1위 · 풀럼 2위), 헤밍스는 정반대 | 루게리 여전히 부상(한 달+ · 에메리 「more than one month」(한 달 이상)) → LM은 만잠비 주전 · 정본 유지 근거가 가장 강한 칸 · 실측 |
| ⑷ | **LB 저점유 프리셋 운용** | fb_att_wb/Support(인게임 Wingback/Balanced) | 마첸 1위 wingback/Balanced .869(Δ.069) · 정본 .687 | 마첸 1위 fullback/Balanced .756 · 보유 1위 wingback/Balanced .799 · 정본 .672 | 마첸 1위 **att_wb/Support .902(Δ.133 결정) = 정본** · wingback/Balanced .769 | **뒤집힘 — 2/3 wingback/Balanced → 풀럼에서 정본 att_wb/Support 결정** | 점유 37%·51%는 wingback, 45%는 att_wb — 점유와 단조 관계 아님 · 경기 상대 구조(풀럼 RW 보브 · 오른쪽 과부하 없음)가 변수일 가능성 · 「인게임 값으로 정렬」 제안은 **보류 쪽으로 약해짐** · 실측 |
| ⑸ | **FC27 optimal:lead 신설** | 없음(#46 optimal만) | 리드 76분 · 리드 구간 수비 액션 평균 높이(def_x) 31.8~32.2 · 20.4(60–66′) | 리드 0분 | **리드 25분(39–64′)** · 수비 액션 평균 높이(def_x) **19.6(39–45′) · 24.8(45–60′) · 38.2(60–64′)** · 후반 PPDA 31.67 · 리드 중 풀럼 xG 대부분(후반 1.61) | **리드 표본 2경기 도달 — 둘 다 「리드 시 블록 20~32로 하강」** · 단 풀럼전은 하강 뒤 실점·지배를 허용 | 조건(리드 2경기) 충족 → 사용자 판단 차례. ⚠️ 풀럼전 하강은 에메리도 원인 미상(의도 아닐 수 있음) — 「리드 = 블록 하강」을 프리셋으로 굳히면 **실패를 재현**할 위험 · 실측 |

⇒ **사용자 판단 요청 목록**(종료 보고에 올림): ⑴ RDM — DLP 2/3이지만 풀럼전 무결정 · 인게임 테스트 「좋았다」 → 정본 변경 여부 ⑵ ST 인게임 Attack vs 정본 Support(3/3 Support ≥ Attack · 전부 무결정) ⑶ LM 정본 유지(만잠비 주전 · 정본 1~2위권) ⑷ LB — 풀럼전이 정본 쪽으로 뒤집어 「wingback 정렬」 근거 약화 ⑸ lead 프리셋 — 2경기 조건 충족 · 단 풀럼전 하강은 실패 사례라 신설 시 라인 하한을 둘지.

## D+1 추적

- 예약 `mw-avl-fulham-collect-1400`(11-01 14:00 보강 · 이 PC) — 이 파일에 「D+1 보강」 절로 덧붙인다. 대상: The Villans 경기 후 영상 · Tanswell 추가분 · 자책골 접촉 여부(FOOTBALL ZONE vs 영어권) · 헤밍스 명단 제외 사유 · 스페인어 에메리 원어(차단 도메인 재시도) · 아르벨로아 스페인어 원문 · 풀럼 관점 영상(Fulhamish).

## D+2 추적

- 예약 `mw-avl-fulham-d2`(11-02 20:00) — 지연 전술 분석(TFA·BTL·Spielverlagerung·The Athletic) · 상대 관점 · 1874 먼데이 리뷰류 · 당일 판정 정정 여부.

## D+3 추적

- 예약 `mw-avl-fulham-d3`(11-03 20:00) — 3일 추적 종결 · 바르사전(11-03 UCL) 명단으로 RB·RM 대응 확인 · complete 판정.

## D+1 보강 (2026-11-01 14:00)

> 예약 `mw-avl-fulham-collect-1400` · 10:00 회차가 리포트·`match_reports` #65를 이미 만들었으므로 **보강만** 했다. DB 행 변경 없음(리포트 md만 덧붙임).

### ⑴ 감독 회견 — 10:00 이후 추가분
- **아르벨로아 — Sports Mole(Ben Sully · 11-01 00:39 GMT · 직접 · 인용 출처 표기 없음)**: 「This is what I want to see from my team, that character, that ambition.」(이게 내 팀에게서 보고 싶은 것, 그 성격과 야망이다) · 「We needed to be aggressive against a team like Villa. It was a Champions League team in front of us.」(빌라 같은 팀을 상대로는 공격적이어야 했다. 앞에 있던 건 챔피언스리그 팀이었다) · 「I think maybe we deserved a little bit more, but the performance was really great.」(조금 더 가져갈 자격이 있었을지도 모르지만 경기력은 정말 훌륭했다) · 「I think we are a very difficult team to beat, and I think we can beat anyone.」(우리는 이기기 매우 어려운 팀이고 누구든 이길 수 있다고 생각한다). ⇒ 10:00 회차의 「더 공격적이어야 한다… 대인 대결에서」와 같은 축 — **후반 풀럼의 대인 압박 강화가 의도된 하프타임 조정**이라는 서술을 보강(빌라 후반 PPDA 31.67·풀럼 12.84 실측과 정합).
- **에메리 — 새 원문 0.** 10:00 회차 4개 출처(avfc · BirmLive 전문 · PA · Sky) 밖의 추가 회견 전사 없음. PA 기사에 붙은 「one point in a difficult stadium」(어려운 원정에서 승점 1) · 「so happy with the second half」(후반에 매우 만족) 류 문장은 **홈 감독 발언으로 성립하지 않아 상대 감독 발언 혼입으로 판단 · 인용 제외**(검색 요약 단계에서 확인 · 원문 미검증).
- 66′ 3명 교체 사유 · 헤밍스 명단 제외: 여전히 **1차 소스 0**.

### ⑵ Jacob Tanswell X
- 브라우저 직접 열람(비로그인 · 14:0x KST): 고정 글 다음 최신이 10:00 회차에 이미 기록한 4건(…2116663575737680038 · …2116663319054676197 · …2116650682615021946 · …2116648458849493345) 그대로 — **추가분 0**.

### ⑶ 필수 채널 3곳 (`/videos` + `/streams` 2탭 · yt-dlp 목록)
- UTV: 새 영상 0(최신 6bwxQlWU3bk = #464 기수집). The Villans: **경기 후 영상 여전히 0**(최신 EUhuiiN4cJA는 프리뷰 · `/streams` 최신은 UCL 랭킹 aF2xltKwKmE). 1874: 새 영상 0(최신 스트림 ZPtfGsSLb94 = #465 기수집).
- ⇒ 전사·요약·구현 주장 **신규 0편**(G17 대상 없음). 뮤트 규칙 해당 재생 없음.

### ⑷ 다국어 기사
- **스페인어(필수)**: Marca 직접 열람 차단(도구 거부) · 검색에 아르벨로아 스페인어 회견 원문 **0**(검색 결과는 맨유전 심판 발언·벌금 건뿐). Flashscore/Soccerway ES 「Emery, más centrado en Arbeloa que en Flick」(직접 · 날짜 표기 없음 · 문맥상 경기 전날) — 에메리 「Así que mañana, Fulham. Hay que dar prioridad claramente a la Premier League, y ese es el mensaje」(그러니 내일은 풀럼이다. 프리미어리그를 분명히 우선해야 하고, 그게 메시지다) · 「En la Premier League nos faltan puntos.」(프리미어리그에서 우리는 승점이 모자란다). ⚠️ 영어 회견의 스페인어 번역 전재로 보인다(에메리 스페인어 원어 여부 불명) — 불변규칙 12의 「번역 복제」 주의 대상이라 **독립 교차검증으로 세지 않는다**. 바르사전 앞 로테이션 대신 리그 우선 → 풀럼전 PL 주전 선발(고레츠카 첫 PL 선발 포함)과 정합.
- **자책골 접촉 여부**: 영어권 3곳 추가 — Sky 「unforced error」(강요되지 않은 실수) · AllFootball 「completely uncontested」(완전히 경합 없음) · Telegraph(Yahoo 전재) 「backpedals towards his own line」(골라인 쪽으로 뒷걸음질쳤다) · 판정 확인은 골라인 기술뿐(파울 VAR 검토 보도 0). ⇒ **접촉 서술은 FOOTBALL ZONE(일본어) 1곳뿐 · 「경합 없음」 채택**, 충돌은 기록으로 남긴다(영상 확인은 여전히 미수행 — 하이라이트 직접 시청 경로 없음).
- 헤밍스: Villa News(Declan Carr · 10-30 · 직접) 「Emery simply can't afford to start him next time out.」(에메리는 다음 경기에 그를 선발로 쓸 여유가 없다) — 선발 제외 전망일 뿐 **명단 밖 사유는 아님**. 무릎 부상은 10-20 훈련 복귀(Rotowire · 스니펫)·본머스전 선발로 회복 확인. 포레스트전 하우드-벨리스 전례(PL 명단 인원 제한)와 같은 원인일 가능성은 **D(추정)** — 확인 전 판정에 쓰지 않는다.
- 다른 언어권: 10:00 회차(일본어·독일어·프랑스어·폴란드어 · 0건 6개 언어)에서 새로 붙은 기사 0.

### ⑸ 10:00 회차 결손 점검
- `match_player_reports` #65 16명: tactical_role·characteristics·performance·game_implication 빈칸 **0**.
- `player_matches` match 129 AVL 16명: 국면 그리드(cells_poss·cells_def) 16/16 · 운반 키 16/16 · phase_source `scope=full`.
- `gates.py` 전항 통과(G21 필수 3종 · G17 · G37 · G42 포함) → **채울 결손 없음**.

### ⑹·⑺ 확인
- 본머스전 관전 가설(H1′·H2′·H2·H3) 풀럼전 판정: 리포트 앞 「사용자 관전 메모 재대조」 절에 있음 → 추가 작업 없음.
- 보류 5건 재판정 표(맨시티·본머스·풀럼 3열): 리포트 끝 절에 있음 → 추가 작업 없음 · 정본 불변.

### D+2로 넘김
- 지연 전술 분석(TFA·BTL·The Athletic) · The Villans 경기 후 영상 재확인 · 풀럼 관점(Fulhamish UOsofuOP5B8 등 — 필수 채널 밖, 전사 판단은 D+2) · 아르벨로아 스페인어 원문(스페인 매체 직접 열람 경로) · 헤밍스 명단 밖 사유 · 66′ 교체 사유.
