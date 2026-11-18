# 본머스 · 브라이턴 · 첼시 — 26/27 전술 개요 · FC27 구현 · 베스트 11 (2026-11-18)

> 사용자 지시 「본머스와 브라이튼 첼시 전술 분석해서 추가해줘 — 아스톤 빌라 수준으로 자세하게는 아니고 전반적인 전술적 특성과 게임내 구현, 베스트 11 정도만」.
> 범위: 개요 수준. DB 정본(팀 설정·슬롯 역할)은 **첼시만** 있다 — 본머스·브라이턴은 관리 팀이 아니라 이 리포트로만 남긴다.
> 근거 등급(불변규칙 12): **C** = 실측 기반 · **D** = 추론(통설·서술 해석). 게임 구현안은 대부분 D다.

## 한눈에 보기

| 팀 | 감독 | 순위(11월 중순) | 기본 형태 | 핵심 성격 | FC27 팀 설정 (빌드업 · 수비 접근 · 라인) |
|---|---|---|---|---|---|
| 본머스 | 마르코 로제(신임) | 7위 · 공식전 8연승 | 4-2-3-1 → 비보유 4-4-2 | 공간 지향 고압박 · 탈취 뒤 직선 공격 | Balanced · Balanced · 60 |
| 브라이턴 | 파비안 휘르첼러 | **2위**(7승 1무 2패) | 4-2-3-1(유동·비대칭) | 짧은 빌드업으로 압박 유인 · 리그 최강 대인 압박 | Short Passing · Aggressive · 75 |
| 첼시 | 사비 알론소 | — | 4-2-3-1 Wide(초반 3-4-2-1) | 상대 따라 빌드업을 바꾸는 중간 블록 | Balanced · Balanced · 52 (DB 정본) |

---

## 1. 본머스 — 마르코 로제

### 전술 특성

- **감독**: 이라올라가 리버풀로 떠난 뒤 로제가 3년 계약으로 부임했다(2026-04-20 발표). 첫 6경기 3무 3패(18위)에서 첼시전 1-5 패배 뒤 리그 4연승으로 7위.
- **형태**: 보유 시 4-2-3-1, 비보유 시 10번 클라위버르트가 올라가 **좁은 4-4-2(4-2-2-2)**.
- **압박**: 높되 사람보다 공간을 지킨다 — TFA 「Bournemouth pressed the ball but defended the space around it.」(본머스는 볼을 압박하되 그 주변 공간을 지켰다). 신호는 상대 6번으로 가는 패스, 애덤스+크리스티 협공.
  - 상대 실수 유도 득점 8(리그 2위의 두 배) · 높은 지역 탈취 뒤 득점 4(1위) — Opta Analyst 11-04.
  - 우리 실측 PPDA 9.89(빌라전 10-28) · 11.27(리버풀전 09-20) — Balanced 구간(C).
- **빌드업·전환**: 골킥부터 짧게 풀되 막히면 직선. 로제 「Da muss man den Ball vielleicht ab und zu schnörkellos in des Gegners Hälfte bringen.」(때로는 군더더기 없이 볼을 상대 진영으로 보내야 한다). 탈취 즉시 배후 직선 패스.
- **비대칭(빌라전 실측)**: 오른쪽에 3명을 몰아 과부하, 왼쪽은 풀백 혼자 폭(C · 1경기).

### FC27 구현안

| 항목 | 값 | 등급 |
|---|---|---|
| 포메이션 | 4-2-3-1 Wide | C(선발 실측) |
| 빌드업 | Balanced (대안 Counter — 탈취 뒤 직선 성향) | C/D |
| 수비 접근 · 라인 | Balanced · 60 — 「압박 괴물」 서술로 High를 주면 PPDA 실측과 어긋난다 | C |

| 슬롯 | 역할 · 포커스 | 등급 |
|---|---|---|
| GK | 스위퍼 키퍼 · Balanced | D |
| RB | 풀백 · Balanced | D |
| RCB | 센터백 · Defend | D |
| LCB | 볼 플레잉 센터백 · Build-Up | D |
| LB | 윙백 · Support (왼쪽 폭 단독) | C/D |
| RDM | 홀딩 · Ball-Winning (협공 압박) | C |
| LDM | 박스 크래셔 · Balanced | D |
| CAM | 섀도 스트라이커 · Attack (비보유 시 투톱) | C/D |
| RM | 인사이드 포워드 · Attack (라얀) | D |
| LM | 인사이드 포워드 · Balanced (타버니어 하프스페이스) | C |
| ST | 어드밴스드 포워드 · Attack | D |

### 베스트 11 (10~11월 리그 선발)

| 위치 | 선수 | 메모 |
|---|---|---|
| GK | 페트로비치 | |
| RB | 애덤 스미스(주장) | |
| RCB | 제임스 힐 | 풀백 출신 기동형 |
| LCB | 안토니우 실바 | 벤피카 영입 · 세네시 대체 |
| LB | 트뤼페르 | 왼쪽 폭 |
| RDM | 타일러 애덤스 | 압박 신호·탈취 |
| LDM | 크리스티 | 협공 + 2선 득점 |
| CAM | 클라위버르트 | 3골 2도움 · 비보유 투톱 |
| RM | **라얀** | 왼발 오른쪽 윙어 · 맨유전 골·MVP |
| LM | 타버니어 | 리그 5골 · 슈팅당 npxG 1위 |
| ST | 에바니우송 | 리그 5경기 연속골 |

- 변수: 스콧(허벅지) 벤치 복귀 · 아라우호·토트 부상 · 에바니우송 입스위치전 43′ 교체(사유 미확인).

---

## 2. 브라이턴 — 파비안 휘르첼러

### 전술 특성

- **감독**: 휘르첼러 유임(2026-05-07 2029년까지 재계약). 리그 10경기 7승 1무 2패 26득점 7실점 · **2위**(선두 아스널과 5점 차, 11-08 기준). 에티하드 원정 첫 승(10-31 맨시티 1-0).
- **형태**: 표기는 4-2-3-1이지만 자리 이동이 많아 「not always a true representation」(늘 실제 모습은 아니다). **비대칭** — 왼쪽이 공격 측면, 오른쪽은 「more about control」(통제 쪽).
  - 레프트백 출신 데 카위퍼를 왼쪽 2선에, 센터백 출신 보스칼리를 레프트백에 둔다.
- **빌드업**: 그라운드 위주 짧은 패스로 상대 압박을 유인. 그로스가 센터백 왼쪽으로 내려오면 보스칼리가 전진.
- **압박**: 공간이 아니라 **사람**을 따라가는 대인 압박. 신호는 백패스·GK 패스. PPDA 8.6 **1위**, 공격 진영 탈취 1위(LiveScore · 7경기 기준).
- **라인**: 리그 3번째로 높다(검색 요약만 확인). 라인 뒤 공간이 약점.
- **강팀 원정**: 맨시티전 점유 39%로 버팀 — 휘르첼러 「It was a completely defensive performance where everyone had the mindset 'I need to defend'」(완전히 수비적인 경기였다, 모두가 '나는 수비해야 한다'는 생각이었다).
- **득점원**: 세트피스·중거리슛 비중이 크다(xG 19.3에 26골). 휘르첼러 「The set-piece is getting so important in the Premier League at the moment」(지금 프리미어리그에서 세트피스가 아주 중요해지고 있다).

### FC27 구현안 (전부 D)

| 항목 | 값 |
|---|---|
| 포메이션 | 4-2-3-1 Wide |
| 빌드업 | Short Passing (강팀 원정은 Balanced) |
| 수비 접근 · 라인 | Aggressive · 75 (PPDA 1위 · 높은 탈취 1위 · 최상단은 피함) |

| 슬롯 | 역할 · 포커스 | 메모 |
|---|---|---|
| GK | 스위퍼 키퍼 · Build-Up | 높은 라인 뒤 커버 + 빌드업 |
| RB | 풀백 · Balanced | 오른쪽 = 통제 측면 |
| RCB | 볼 플레잉 센터백 · Aggressive | 운반·전진 수비 |
| LCB | 볼 플레잉 센터백 · Build-Up | 던크 = 패스 축 |
| LB | 폴스백 · Balanced | 센터백형 레프트백(대안 풀백 · Defend) |
| RDM | 홀딩 · Defend | 체마 안드레스 「6번」 |
| LDM | 딥라잉 플레이메이커 · Roaming | 그로스 하강·전진 |
| CAM | 섀도 스트라이커 · Attack | 아야리 침투·압박 |
| RM | 윙어 · Balanced | 고메스 폭 유지 |
| LM | 윙어 · Attack | 공격 측면 |
| ST | 어드밴스드 포워드 · Attack | 배후 침투·역습 |

### 베스트 11 (맨시티전·브렌트퍼드전 동일 선발)

| 위치 | 선수 | 메모 |
|---|---|---|
| GK | 페르브뤼헨 | 실점 7 vs 기대실점 11.4 — 리그 최고 |
| RB | 코스티냐 | 카디오글루 부상 대체(카디오글루 11-08 벤치 복귀) |
| RCB | 부슈코비치 | 운반형 |
| LCB | 던크(주장) | 경기당 약 90패스 |
| LB | 보스칼리 | 센터백 출신 · 왼발 전환 패스 |
| RDM | 체마 안드레스 | 위치 고수형 6번 |
| LDM | 그로스 | 6·8·10번 오감 · 7경기 3골 4도움 |
| CAM | 아야리 | 맨시티전 결승골 |
| RM | 디에고 고메스 | 높고 넓게 · 중거리 |
| LM | 데 카위퍼 | 레프트백 출신 윙어 |
| ST | 코스툴라스(19세) | 운반·역습 마무리 |

- 결장: 미토마·지마스(전방십자인대) · 요하나 · 퍼거슨. 주요 교체: 비퍼(세트피스 높이) · 힌셜우드 · 뤼테르 · 얄쿠예.

---

## 3. 첼시 — 사비 알론소 (DB 시즌 정본 · regime 2)

> 출처는 DB 시즌 정본(team_tactic_setups #50 optimal · slot_canon_roles · 선발 처방, 2026-11-04 반영)과 [시즌 축 검토](2026-11-04-che-season-review.md). ⛔ 첼시 정기 수집은 하지 않는다(사용자 결정 11-04) — 최신 경기는 10-31 맨유전까지.

### 전술 특성

- **형태**: 초반 PL은 3-4-2-1(5경기), **10-17 이후 PL은 전부 4-2-3-1**. 하토·주앙 페드루 등 부상이 겹친 시기라 3-4-2-1 복귀 가능성은 열려 있다. 알론소 「Can be in a 4-4-2, it can be in a 5-2-3 but the distances… how you have a good balance」(4-4-2일 수도 5-2-3일 수도 있다, 간격과 균형이다 · auto-caption).
- **빌드업**: 상대 따라 바뀐다 — 경기 프리셋 Counter 4(아스날·스퍼스·브라이턴 등 강팀) · Balanced 5 · Short Passing 3 → 정본 Balanced.
- **압박**: 레버쿠젠식 고압박이 아니라 **중간 블록** — PPDA 8.38~22.67, High 구간(≤8) 0경기.
- **라인**: 수비 액션 평균 높이(def_x) 7경기 평균 39.5 → 정본 52.
- **패턴**: 백3+더블 피벗으로 후방 수적 우위, 카이세도가 백라인 옆으로 내려와 압박을 유인.

### FC27 구현 (DB 정본 · C)

| 항목 | 값 |
|---|---|
| 포메이션 | 4-2-3-1 Wide |
| 빌드업 · 수비 접근 · 라인 | Balanced · Balanced · 52 |

| 슬롯 | 역할 · 포커스 | 선발 | 적합도(표본) |
|---|---|---|---|
| GK | 골키퍼 · Defend | 펜더스 | .961 (5) |
| LB | 윙백 · Support | 요렐 하토 | .711 (3) |
| LCB | 볼 플레잉 센터백 · Aggressive | 콜윌 | .919 (9) |
| RCB | 볼 플레잉 센터백 · Aggressive | 웨슬리 포파나 | .774 (4) |
| RB | 윙백 · Balanced | 아체암퐁 | .922 (5) |
| LDM | 딥라잉 플레이메이커 · Build-Up | 조던 헨더슨 | .696 (2) |
| RDM | 딥라잉 플레이메이커 · Roaming | 카이세도 | .888 (3) |
| LM | 와이드 플레이메이커 · Attack | 로저스 | .783 (4) |
| CAM | 플레이메이커 · Roaming | 콜 파머 | .686 (4) |
| RM | 윙어 · Attack | 페드루 네투 | .809 (8) |
| ST | 폴스 나인 · Build-Up | 주앙 페드루 | .655 (6) |

- 위 선발 열이 곧 **베스트 11**(DB 선발 처방)이다. 참고: 파머 10-24 스퍼스전 퇴장 · 주앙 페드루·하토·라크루아 부상 이력 — 11월 이후 상태는 수집하지 않았다.

---

## 빌라 관점 한 줄

| 상대 | 빌라가 볼 것 |
|---|---|
| 본머스 | 10-28 리그컵 0-3 패. 6번 패스가 압박 신호 → 빌라 더블 피벗의 첫 패스 방향이 관건. 라얀(오른쪽) vs 빌라 LB(마트센) 1:1 |
| 브라이턴 | 대인 압박 1위 + 높은 라인 → 잭슨·알리송의 배후 침투가 통할 구간. 반대로 세트피스·중거리 대비 |
| 첼시 | 중간 블록이라 빌라 점유가 늘 가능성 · 강팀 상대 Counter 프리셋을 쓴 전례 |

## 출처

**본머스**
- NBC Sports 2026-04-20 — https://www.nbcsports.com/soccer/news/bournemouth-hire-marco-rose-to-replace-andoni-iraola-for-2026-27-premier-league-season
- Goal(영·독) 2026-11-13 수정 — https://www.goal.com/en/news/unstoppable-after-a-horror-start-a-german-manager-has-created-a-feared-pressing-monster-in-the-premier-league/bltac481716ae023c9f · https://goal.com/de/meldungen/acht-siege-am-stueck-deutscher-coach-hat-in-der-premier-league-das-pressing-monster-zum-leben-erweckt/bltac481716ae023c9f
- Tactical Football Analysis 2026-09-19 — https://tacticalfootballanalysis.com/real-sociedad-bournemouth-europa-league-2026-2027-tactical-analysis-tactics/
- Goal 「The tactics board」 2026-10-23 — https://www.goal.com/en-qa/lists/bournemouth-ac-milan-the-tactics-board-marco-rose-europa-league/blt72b85fdb94487c90
- VAVEL 2026-10-25 — https://www.vavel.com/en/football/2026/10/25/manchester-united/1276825-manchester-united-0-3-bournemouth-the-damned-united-suffer-humiliation-again.html
- Last Word on Sports 2026-10-31 — https://lastwordonsports.com/football/2026/10/31/bournemouth-vs-leeds-united/
- Premier League News Now 2026-11-15 — https://premierleaguenewsnow.com/2026/11/15/bournemouth-eight-wins-in-a-row-marco-rose-analysis/
- Sky Sports 2026-11-08 — https://www.skysports.com/football/news/13593217/ipswich-1-2-bournemouth-evanilson-scores-again-as-cherries-make-it-eight-wins-in-a-row
- Opta Analyst 2026-11-04 — https://theanalyst.com/articles/bournemouth-marco-rose-blossoming-stats
- 로컬 실측: reports/match-watch/2026-10-28-avl-bournemouth.md · reports/match-watch/2026-09-20-liv-bournemouth.md

**브라이턴**
- Mastermind 2026-09-19 — https://themastermindsite.com/2026/09/19/fabian-hurzeler-brighton-tactical-analysis/
- Tactical Football Analysis 2026-08-26 — https://tacticalfootballanalysis.com/brighton-aston-villa-premier-league-2026-2027-tactical-analysis-tactics/
- Wikipedia 26/27 시즌(11-08 갱신) — https://en.wikipedia.org/wiki/2026%E2%80%9327_Brighton_%26_Hove_Albion_F.C._season
- LiveScore(날짜 미표기 · 약 10-25) — https://www.livescore.com/en/news/football/team/brighton/liverpool-esque-brighton-can-prove-premier-league-title-credentials-against-reds/
- AOL/BBC 2026-10-31 — https://www.aol.com/articles/man-city-0-1-brighton-174952000.html
- WeAreBrighton 2026-11-16 — https://www.wearebrighton.com/newsopinion/7-takeaways-from-brighton-hove-albions-2026-27-season-so-far/
- Eurosport.de 2026-11-06 — https://www.eurosport.de/fussball/premier-league/2026-2027/fabian-huerzeler-rockt-mit-brighton-in-england-platz-drei-nach-sensationssiegen-gegen-top-teams-der-neue-klopp_sto23352795/story.shtml
- Yahoo/Roundtable 2026-11-15 — https://sports.yahoo.com/articles/brighton-tacticals-evolution-transforming-season-192050438.html
- dave.sport 2026-11-08 — https://dave.sport/news/brighton-vs-brentford-line-ups/

**첼시**
- DB 시즌 정본(regime 2 · 2026-11-04) · reports/research/2026-11-04-che-season-review.md
