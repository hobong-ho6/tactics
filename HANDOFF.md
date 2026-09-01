# HANDOFF

## 프로젝트

- 실제 감독 전술을 실측으로 분해해 FC26 전술로 재현한다.
- 대상: Aston Villa/Unai Emery(주), Chelsea/Xabi Alonso, Liverpool/Andoni Iraola, Atlético/Diego Simeone.
- 저장소: `/Users/ad03230205/Documents/tactics`, 브랜치 `main`.
- DB 정본: `db/tactics.db`. `db/dump/`와 `site/data/`는 파생물이다.
- 규약 정본: `CLAUDE.md`, `docs/00-overview.md`, 세부 문서는 `docs/`.
- 정기 작업 런북: `.claude/skills/transfer-watch/SKILL.md`, `.claude/skills/match-watch/SKILL.md`, `.claude/skills/player-collect/SKILL.md`.

## 현재 상태

> 마지막 갱신: **2026-09-01 KST** · 작업 PC `AD03230205ui-iMac.local` · 브랜치 `main` ·
> 마지막 **데이터** 커밋 `4eb0e0d` · 이 문서의 갱신 커밋 `740a268`(그 위에 얹혀 있다).
> 해시 표기 커밋은 그 다음에 하나 더 붙는다 — HEAD가 여기서 1커밋 앞서 있으면 정상이다.
> ⚠️ **직전 갱신은 08-25(`f05010f`)였다** — 08-26~09-01 사이 24개 커밋이 문서에 반영되지 않은 채 쌓여 있었고,
> 이번 갱신이 그 공백을 git log 기준으로 복원한 것이다.

- DB: players **200** · player_matches **4,175** · team_match_stats **65** · match_reports **29**
  (**complete 14 · draft 15**) · match_player_reports **521** · squad_entries **131** ·
  prescriptions **429** · slots **88** · match_game_setups **14** · match_player_prescriptions **228** ·
  transfer_targets **44** · transfer_outgoing **67** · player_duties **194** ·
  **player_shirt_numbers 26**(신설) · understat_player_matches **5,634** · observations **372**.
  (players −1 · fotmob_season_stats −8 · fotmob_traits −6 · player_tenures −6 = 에수구 병합분 ·
   player_matches −79 = 에수구 1 + **이중기록 77+1쌍 정리분**. 아래 참조.)
- ⏰⏰ **2026-27 여름 이적창이 2026-09-01 23:00 BST(= 09-02 00:00 CEST)에 닫혔다.**
  **사용자 지시로 `transfer-watch` 정기 루틴은 종료한다** — 남은 것은 **09-02 09:00 KST 마감 정산 1회뿐**이고,
  그 회차가 스스로 스케줄을 삭제한다(아래 「자동화」 참조).
- 회귀: G1~G12 전항 통과. 커널 회귀검증 **14/14 소수점 3자리 재현**(08-31, 빌라 영입 전수 수집 시).
- ⛔⛔ **xG 계열은 한 회차에 같은 스냅샷으로 수집한다** — 따로 채우면 Opta 사후 개정 때문에
  「오픈플레이 > 전체」라는 불가능한 값이 된다. FotMob matchDetails 한 응답에 전부 있다.
  검산: `xg − xg_op` = 세트피스+PK이고 **PK 개수 × ~0.79**와 대조. 정본은 `match-watch/SKILL.md` §3.
- ⛔⛔ **`site/assets/*.js`를 고쳤으면 임포트의 `?v=`를 반드시 올려라.** heatmap 인라인 핸들러는
  HTML/JS에 no-store를 보내지 않는다. **G9가 막는다.**
- ⛔ **curl·WebFetch로 FotMob·SofaScore API를 치지 말 것** — 페이지 컨텍스트 밖에서 막힌다(404/403).
  브라우저로 해당 오리진을 연 뒤 JS 안에서 fetch하면 200이다. **403 보고를 받으면 먼저 브라우저 경로로 재확인한다.**
  ✅ SofaScore는 08-19 이후 재개통 상태이며 08-31 빌라 영입 수집에서도 정상 작동했다.
- ⭐ **유튜브 자동 생성 자막은 회수 가능하다** — `python3 scripts/yt_transcript.py VIDEO_ID LANG [메모]`
  → `reports/transcripts/`. 영상·음성 자체는 여전히 시청 불가(화면 전술보드는 자막에 없다).
  인용 시 confidence에 **auto-caption** 명기. ⏰ docs/30 「듣지 않은 영상은 인용 금지」에서
  **「전사를 읽은 영상」의 지위는 아직 미정의** — 규약 갱신은 사용자 판단 대기.

### 2026-08-30~31 PL Round 3 (수집 완료 · 커밋 `e175143`)

| 팀 | 경기 | 핵심 실측 |
|---|---|---|
| CHE | Chelsea 4–3 Brighton | **PL 사상 최저 점유 26%인데 xG 2.93:1.41** · PPDA 22.67 |
| CHE | Luton 0–2 Chelsea (EFL컵) | 백4 전환 66% · PPDA 13.13 |
| LIV | Liverpool 2–2 Nottm Forest | **69% 점유에 빅찬스 1:5 — 이라올라 이식의 첫 반증** · PPDA 5.76 |
| ATM | Sevilla 1–3 Atlético | 바에나 falso nueve · **33분 안에 3–0** · PPDA 8.26 |

- player_matches +64 · team_match_stats +4(xG 4종 동일 스냅샷) · 스코어국면 phase 적재 ·
  26/27 measured 처방 20행 갱신 · 완료 리포트 4건 + 경기전용 프리셋 4 + 선수처방 64.
- ⭐ **압박 상수 3건이 반복 확인됐다**(obs#350~352): 알론소 저압박(20.18→22.67) ·
  이라올라 고압박(5.95→5.76, **부임 후 가장 안정적인 상수**) · 시메오네 하이브리드(7.77→8.26, 3경기째 — 저블록 서사와 어긋난다).
- ⭐⭐ **obs#343의 「검증된 LM이 학포뿐」 리스크는 재검토 대상이다**(obs#353) —
  포레스트전에서 **학포가 RM에 배치되고 좌측은 비토르 무뇨스가 맡았다.**
- ⚠️ **08-31 match-watch가 병렬로 2회 실행돼 같은 4경기를 중복 수집했다**(obs#354) —
  실측 적재는 **선행 세션분이 정본**이고 후행 세션은 PPDA만 보강했다. 재발 방지책은 미수립.

## 자동화

- Codex heartbeat **id=3 「프리미어리그 3팀 경기 수집」**, 매일 08:00 KST.
- `match-watch-weekly` 스케줄: 매주 월 10시. R3 D+1~D+3 추적 일회성 작업 3건이 09-01~09-03에 걸려 있다.
- ⚠️ **`transfer-feed` 스케줄은 반복 cron(09/21시)에서 일회성으로 바꿨다** —
  **2026-09-02 09:00 KST 1회만 실행**하고, 그 회차가 잔여 건 정산 후 **자신을 삭제**한다.
  종료 절차는 `reports/transfer-watch/2026-09-01.md` 맨 아래에 있다.

## 종결된 항목

### 2026-09-01 · ⭐⭐ `player_matches` 「이중 기록」 77쌍 정리 (obs#369 → obs#370, 잔여 0)

- **규칙: SofaScore 행을 정본으로 두고, FotMob 행에만 있는 값을 흡수한 뒤 FotMob 행을 삭제한다.**
- **동일 출전 확정**: 77쌍 전부 `date` 일치 · `minutes` 차이 **±1뿐**(−1이 17·0이 42·+1이 18 = 제공자 반올림) ·
  `competition`은 라벨 변형(「Club Friendly」 55 ↔ 「Club Friendly Games」 22).
- **정본 선택 근거**: SofaScore 쪽이 map25·hit_points·avg_x·cells·goals·assists·touches·duels·tackles·key_passes를
  **각 77/77** 갖는 반면 **FotMob 쪽은 그리드·세부스탯이 전부 0/77**이다.
- ⚠️⚠️ **단순 중복이 아니었다 — 평점이 66/77쌍에서 달랐다.** 오류가 아니라 **두 제공자의 평점 체계가 다른 것**이라
  버리지 않고 **`stats_json`에 `fotmob_rating`/`fotmob_minutes`/`fotmob_event_id`/`fotmob_competition_label`로 보존**했다.
  FotMob 고유 결손도 실재했다 — `opponent` 22행 · `venue` 22행 · `started` 1행을 **백필**했다.
- player_matches **4,253 → 4,176**. 정리 후 77행 전부 opponent·venue·started·map25 결손 0.
- 검증: FK 0 · integrity ok · **G1~G12 전항 통과**(G7 앵커 (14,6,4,93) 불변). `player_matches.id` 참조 FK는 없음을 사전 확인.

### 2026-09-01 · ⭐⭐ `team_code` 클럽 축 333행 정리 (obs#371 → obs#372) · **대표팀 축은 미해소**

- **문제**: `team_code`가 「경기 시점 소속」이 아니라 「수집 시점 현 소속」으로 찍혀 있었다.
  스키마가 이 칸을 「그 경기에서 소속」으로 명시하므로 **정의 위반**이다.
  확정 영입 7명에서 **407행** = **클럽 333 + 대표팀 74**.
- **사용자 결정(09-01): 구 클럽 코드를 `teams`에 추가하는 방향.** 클럽 333행만 처리했다.
- **신규 teams 6행** — `PSG` · `BAY` · `BAR` · `WHU` · `RAY` · `PAR`.
  ⚠️ `note`에 **「분석 대상 팀 아님 — player_matches.team_code 참조 어휘」**를 명기했다.
  **regimes·slots·prescriptions 등 판단 테이블은 여전히 AVL·CHE·LIV·ATM 4팀뿐이다.**
  ⭐ `BAY`는 등재 전에도 팔리냐 1행에서 쓰이던 **고아 코드**였고 정규화됐다 ⇒ **teams 미등재 코드 0**.
  ⚠️ **루제리 25/26은 아탈란타가 아니라 아틀레티코(ATM)였다** — 초기 추정을 `player_tenures`로 교정했다.
- **재배정**: 바르콜라 54→PSG · 잭슨 43→BAY + 5→CHE · 루제리 64→ATM · 아라우호 52→BAR ·
  완비사카 38→WHU · 차바리아 55→RAY · 스즈키 28→PAR.
- ⚠️⭐ **`avg_positions`(export)가 team_code로 필터하므로 사이트 표본이 크게 줄었다 — 오염이 걷힌 것이다**:
  완비사카 AVL 35→**10** · 바르콜라 LIV 46→**8** · 아라우호 LIV 23→**4** · 스즈키 AVL 29→**7** ·
  잭슨 AVL 27→**12** · 차바리아 CHE 40→**1** · **루제리 AVL 45→0**(전부 ATM 시절이었다).
- ⭐⭐ **이 정리가 숨은 결손 2건을 드러냈다**:
  ① **match_id 링크 결손 20행** 봉합 → 그 결과 **1차 77쌍에서 놓친 이중기록 1쌍**이 드러나 정리했다
     (잭슨 08-05 유벤투스 — 한쪽 `match_id`가 NULL이라 키로 짝이 안 잡혔다).
  ② **G12 「선수처방누락」 1건이 터졌다** — 잭슨의 08-08 밀란전(32분) 처방이 **없었는데**,
     그 출전이 `AVL`로 태깅돼 G12 조인에 안 걸려 **결손이 은폐돼 있었다.** 커널로 채웠다(ST·st_false9·Build-Up·0.554).
     ⇒ **team_code 오류는 데이터 오염일 뿐 아니라 게이트를 무력화한다**는 것이 실증됐다.
- 검증: FK 0 · integrity ok · **G1~G12 전항 통과** · 잔여 68행(전부 대표팀).

### 2026-09-01 세션 (transfer-watch 마감 당일 · 커밋 `4eb0e0d`)

- ✅ **각포 유출 무산이 4팀 축을 동시에 움직였다** — Ornstein 「deal is off」(맨시티 £80m 거절).
  ⑴ 리버풀 **사르 DEAD**(필요 소멸형 — 슬롯 소멸 + 팰리스 £75m 벽 + **비홈그로운 17인 한도 도달**)
  ⑵ 맨시티 → **엔소(첼시)로 선회** ⑶ 토트넘 → **무드리크(첼시)로 선회**.
  ⚠️ 자체 정정: 어제 원장의 「£85m package」는 실제 제출액 **£80m**과 달랐다.
- ✅ ⭐⭐ **아하노르 거래 형태 근본 정정** — 「첼시 완전영입 → 팰리스 임대」는 **오답**이었다.
  실제는 **아탈란타 발 팰리스 임대 + 첼시 선계약(2027-07-01 등록)**이고, 사유는
  **PL 「동일 구단에 2명 임대 불가」 규정 우회**다(첼시는 이미 디사시를 팰리스로 보냈다).
  **이탈리아어 5개 매체 단독** 정보였고 영어권은 결과만 운반했다.
- ✅ ⭐ **데이비드(ATM) 구조 5항목 확정**(Di Marzio EXCL): 무상임대 · **diritto=재량**(의무·자동 아님) ·
  €25m · 급여 60:40 · 2031. + 역할이 **「제3 공격수」**로 규정되어 **「알바레스 대체」 프레임 자체가 오류**로 판명.
- ✅ **히메네스 Rui Costa 발언 일자 06-27 확정** = 예산총회에서 슈크리니아르를 확인하는 문답 ⇒
  **어제 예고했던 MEDIUM 강등 사유가 §2-0으로 무효화**됐다(연도·창이 맞는데 주제가 다른 유형).
- ✅ **바르콜라 CONFIRMED + squad_entries 승격**(id=134, regime3/WM/wm_wideplm .751,
  그리드 출처 **PSG 25/26** 명기 — 불변규칙 7) · 바이체티치·피니 CONFIRMED ·
  무드리크·토신 **둘 다 토트넘으로 행선지 전면 교체 + HIGH** · 산체스→코모 신규 HIGH ·
  오라일리→동커스터 신규 HIGH(**players id=206 신설**, 5개 회차 결손 봉합).
- ✅ **자체 정정 3건**: 각포 금액 계보 · 버로스 위건 **디비전 라벨**(챔피언십→League One) ·
  쇠를로트 「회복 임박」(08-31 여전히 결장).
- ✅ ⭐ **마감 프레임 정정** — 포르투갈·터키는 **09-04**, UEFA 등록은 **09-02**다.
  ⇒ **히메네스·르마르는 09-01 통과를 자동 잔류로 처리하면 안 된다.**
- ✅ **부재증명 금지 페이지 2호 확정**(`skysports.com/…done-deals` — 실재 건 전부 누락) ·
  **liverpoolfc.com Media watch 함정 6호** · **검색엔진 요약 오염 신규 유형** · §2-0 화석 20건+.
- ✅ 아라우호 `transfer_targets` **player_id 링크 봉합**.

### 2026-08-31 세션 3건 (avl-signings 2 + match-watch R3 + transfer-watch 3회차)

- ✅ **빌라 확정 영입 9명 + 하우드-벨리스·음바예 17축 전수 수집**(커밋 `334a48b`) —
  FotMob 7축 · Understat 2축(+661행) · SofaScore 재개통 확인 후 완비사카/하우드-벨리스 신규 적재 ·
  **커널 회귀검증 14/14 재현** 후 prescriptions 결손 봉합 · FC27 scan-all +136행 ·
  ⭐ **`player_shirt_numbers` 테이블 신설**(obs#363, 빌라 26/27 스쿼드 26명 — 지흐→시세 48번 승계가 표현된다).
  ⭐⭐ **음바예 regime_id 3(리버풀)→1(빌라) 주소 정정**(obs#355, 불변규칙 7 위반) — 적합 0.94→**0.878**.
  ⭐ 음바예는 실측상 정통 윙어가 아니다(obs#356 — tool_x 74.42로 AVL RM 슬롯 x=85보다 **10.58 안쪽**, 영입 11명 중 최대 이탈).
- ✅ **미해결 3건 종결**(커밋 `00e728c`) — ⑴시세 ÖFB컵 결승 **DM 기용설 반증**(5개 독립 소스 전원 백3 CB) ·
  ⑵**에메리의 완비사카 실명 축어 0건 확정**(회견 3회 전수·17개 검색어·3개 언어) + 「hailed」 헤드라인은 **2019년 아스날 시절 화석** ·
  ⑶롱볼 사건 원문 확정. ⚠️ **자체 정정: 「분노→45분 교체」 인과는 반증**됐다(하프타임 4명 동시 교체 = 정규 로테이션, obs#365).
  롱볼 사건과 온더볼 충돌 판정은 유지하되 **교체 함의는 철회**.
- ✅ **R3 4경기 수집**(커밋 `e175143`) — 위 「Round 3」 표 참조.
- ✅ **transfer-watch 3회차**(11시 `68216be` · 21시 `8219733` · 22시 `0623f4a`) —
  데이비드 Romano HWG · 니코 곤살레스 DEAD 강등 · 응게상·토신·버로스 신규 · 라리가 마감 RFEF 규정 확보.

### 2026-08-26~30 (압축)

- **08-26**: CHE 풀럼전 **영상 축 완결**(obs#347, 3개 언어 8건 전사 — 제임스 백3 하강 4중 수렴·「펜타곤 트랩」) +
  **경기 전용 처방 재판정**(obs#348) — ⭐ 사용자 확정 원칙: **개별 경기 구현은 그 경기 전술의 게임 재현이므로
  분석 내용을 전부 반영한다**(시즌 정본은 경기 누적으로만). 선발 4명 역할 교체.
  ⏰ 이 재판정 단계를 match-watch 표준 파이프라인에 넣을지는 **아직 미확정**.
- **08-27~30**: transfer-watch 정기 다수회차 — 고레츠카·잭슨·왓킨스(알힐랄) CONFIRMED 승격 및
  squad_entries 반영 · 아하노르·카마라·데이비드·음바예·엘리엇 신규 등재 · 토디보 등재 후 DEAD.
  ⭐ `core.sofascore.js_event_collect` + `scripts/collect_event.py` **이벤트 축 수집기 신설**(커밋 `f770dff`).
  ⭐ AVL LM/RM 슬롯 x 재검토는 **표본 부족으로 보류**(obs#349, 커밋 `c5c99cc`).
- **08-24~25(아카이브)**: 적합값 드리프트 20→8→4 · 좌우 이봉 전수 점검(40명 중 7명 이봉, 린델뢰프 .75→LCB .952) ·
  전후(높이) 이봉 **0건**(obs#342 — 사이드는 범주형이라 이봉, 높이는 연속형이라 단봉) ·
  게이트 3건 신설(G12 orphan_preset_slots·xg_openplay_violations, G9 무버전 JS 임포트) ·
  스키마 확장 2건(`overall_assessment`, `xg_op_*`/`blocked_*`) · ATM 4-4-2 슬롯 신설 · 경기 히트맵 렌더 버그 3원인 수정.

## 진행 중 작업 (WIP)

**없음.** 워킹트리 깨끗하고 origin/main과 일치한다.

## 다음 할 일

### transfer-watch — ⏰ **종료 절차만 남았다**

1. **P1 · 09-02 09:00 마감 정산(최종 회차)** — 스케줄이 자동 실행한다. 임무:
   ⑴ 잔여 HIGH·MEDIUM-HIGH 전 건을 **결과(CONFIRMED / DEAD)로 확정**
   ⑵ **09-04 마감 리그(포르투갈·터키) 건**은 `confidence`에 「2026-summer 감시 종료 시점 미결」 명기 후 등급 동결
   ⑶ export → dump → 커밋·푸시 ⑷ **`transfer-feed` 스케줄 자기 삭제**.
   ⚠️ **개별 공식 기사 URL 존재 여부로만 판정할 것** — 집계 페이지·Media watch·Sky done-deals는 **전부 부재증명 불가**.
2. **P2 · 겨울창(2027-01) 재개 시** 이 스킬을 다시 켤지 사용자 판단. 런북(`.claude/skills/transfer-watch/SKILL.md`)은
   그대로 저장소에 남아 있어 스케줄만 다시 만들면 된다.
3. **P3 · 이월 감시 대상**: 무소(ATM→나폴리, 겨울창 이월 확정 방향) · 네투(CHE→알힐랄, 사우디 창은 별도 일정).

### match-watch

1. **P1 · PL Round 4** — 동일 파이프라인 반복. R3 D+1~D+3 추적 일회성 작업이 09-01~09-03에 예약돼 있다.
2. **P1 · draft 15건 → complete 승격** — 현재 complete 14 / draft 15다. 프리시즌 친선 draft는
   원문 자체가 얇아 **필드 길이가 근거량에 비례**하므로 억지 보강하지 않는다(08-25 확정).
3. **P2 · obs#353 후속** — 학포 RM 배치로 「검증된 LM이 학포뿐」 리스크 서술을 재판정한다.
   무뇨스 좌측 표본이 오사수나 시절이라는 불변규칙 7 캐비앗은 그대로다.
4. **P2 · 경기 전용 처방 재판정을 표준 파이프라인에 넣을지 확정** — 08-26 이후 R3 4경기에서 반복 적용됐다.
5. **P3 · 병렬 중복 실행 방지**(obs#354) — 08-31에 같은 4경기를 2회 수집했다. 가드 미수립.
   ✅ **「이중 기록」 77쌍은 2026-09-01에 전부 정리했다**(obs#370, 잔여 0).
   ⭐ **다만 재발 감지 게이트 2종은 여전히 없다** —
   ⑴ `players`의 **fotmob_id/sofascore_id 중복 검사**(G6 사각지대 — 두 id가 다 존재하면 통과한다)
   ⑵ `player_matches`의 **같은 (player_id, match_id)에 서로 다른 event_id가 두 행** 있는 경우.
   둘 다 이번에 손으로 셌고 각각 실물 결함을 하나씩 잡아냈다 ⇒ **게이트화 가치가 실증됐다.**
6. **P3 · 그리말도(ATM) 실측**이 채워지면 슬롯 기하·fit 재검증.

## 미해결 — 판단이 필요한 것

1. 🔴⭐ **`team_code` 대표팀 축 — 406행 / 40명이 아직 클럽 코드다**(obs#371 잔여 · 클럽 축은 obs#372로 해소).
   완비사카의 DR콩고 WC예선이 `AVL`, 각 팀 선수의 월드컵·A매치가 소속 클럽 코드로 찍혀 있다.
   내역: FIFA World Cup 142 · International Friendly Games 118 · WC Qual. UEFA 82 · AFCON 28 ·
   WC Qual. CAF 16 · WC Qual. CONMEBOL 12 · 기타 8.
   ⏰ **결정 필요**: 국가대표를 `teams`에 넣을 것인가(40개 코드) / NULL 결손으로 둘 것인가.
   ⚠️ 스키마 주석은 「클럽/대표팀 구분은 competition으로」라 하지만, team_code가 소속을 가리키는 칸인 이상
   대표팀 경기에 클럽 코드를 넣는 것은 정합적이지 않다. **클럽 축과 달리 이건 손대지 않았다.**
2. ⏰ **xG 개정 정책** — 「경기 직후 스냅샷을 정본으로 둘 것인가, 최신 개정을 따라갈 것인가」 규칙이 없다.
   현재는 **draft면 최신, complete면 사용자 판단**으로 운용한다.
3. ⏰ **ATM 비야레알전 포메이션 표기 충돌** — 우리·El Desmarque·COPE는 **4-4-2**, **Infobae 크로니카는 「4-3-3 de Simeone」**.
   obs#333(ATM 4-4-2 슬롯 신설)의 전제와 직결된다. ⭐ 단 실측 기하가 4-1-4-1에 더 가까워 처방을 이관하지 않은 판단은 이 충돌과 정합적이다.
4. ⏰ **FC27 커널 미착수** — `game_roles`/`game_role_focus`/`game_role_variants`의 FC27 행이 **전부 0**이다.
   fut.gg `/api/fut/roles/` 수집은 발매(09-25) 전 역할 데이터 공개 여부가 불확실하다.
   `core/kernel.py` EXPECTED·gates 앵커의 FC27 확장은 커널 행이 생긴 뒤에만 가능하다.
   ⚠️ FC27 게임스탯 잔여 결손: **고레츠카 0행**(무소속이라 fut.gg 클럽 페이지에 없다 — 결손이지 미출시 아님, obs#362) ·
   **35속성은 완비사카·음바예 2명**(obs#364).
5. ⏰ **`transfer_targets` 아하노르 행의 window 표기** — 「2026-summer 완전이적」이 아니라
   **2026-summer 선계약 / 2027-07-01 등록**이다. 스키마상 이를 분리 표현할 자리가 없어 `rationale`에만 적었다.

## 데이터 수집 상태와 결손

- 대량 수집: `collect_fotmob_players.py`, `collect_understat_shots.py`, **`collect_event.py`**(이벤트 축, 08-30 신설).
- 읽기 전용 진단 3종: `check_fit_drift.py` · `check_side_bimodality.py` · `check_height_bimodality.py`.
  ⚠️ 셋 다 **진단만 한다** — 그리드 재적재·`pos_only`·처방 변경은 사람이 판단한다.
- ⛔⛔ **검색엔진 연도 혼입에 주의.** 같은 상대·같은 8월·유사 스코어의 전년도 경기는 반드시 발행일을 확인하고 쓴다.
  ⭐ 2026-09-01에 **검색엔진 요약 자체가 오염되는 신규 유형**을 확인했다 — 요약이 과거 시즌 사건을
  현재 확정 사실로 제시한다. **엔진 요약은 근거로 채택 불가, 개별 URL 실물 확인만 사용한다.**
- ⚠️ **verbatim 인용은 요약 경유 시 열화된다.** **실질만 채택하고 인용문은 원문 확보 전까지 쓰지 않는다.**
- Understat은 빅5(+RFPL)만. 챔피언십·에레디비시·리가2는 없다.
- Sofifa 35속성/playstyles, FBref 12축은 403 결손 상태다.
- ⏰ **AVL LM/RM 슬롯 x 재검토는 표본 부족으로 보류**(obs#349). 재시도 조건: 정상 경기 누적 + 해당 경기 `cells` 수집.
- ⭐ **1차 소스 경로 메모**: `laliga.com/clubs/{club}/transfers`가 **등록 기준 1차 소스로 유효**하다
  (`atleticodemadrid.com`은 403). 단 날짜가 **행정 등록일**이라 구단 발표일과 다를 수 있다.
- 결손과 0을 구분한다. `docs/30-data-rules.md` 규약을 따른다.

## 고정 작업 규칙

1. 시작 시 `git status --short`. 로컬 변경이 있으면 fetch/pull하지 말고 내용부터 확인한다.
2. 깨끗할 때만 `git fetch origin && git pull --rebase origin main`.
3. 다른 PC/세션 변경을 버리거나 덮지 않는다. 특히 `db/tactics.db`는 충돌 시 기계 병합 금지.
4. DB 변경 뒤 반드시:

   ```bash
   .venv/bin/python scripts/export.py
   scripts/db_dump.sh
   .venv/bin/python scripts/gates.py
   ```

5. `git add -A` 금지. `db/tactics.db`, 관련 `db/dump/`, `site/data/`, `reports/`, 문서를 명시 스테이징한다.
6. push 전 `origin/main` 이동 여부를 다시 확인한다.
7. 시즌 집계는 45분+·hit_points 15+만 사용하되, 경기 리포트는 짧은 교체 포함 실제 출전자 전원을 기록한다.
8. match 전용 fit/전술은 시즌 `prescriptions`/`team_tactic_setups`에 자동 병합하지 않는다.
9. HANDOFF는 300줄 이하로 유지한다.

## 핵심 방법론

- 그리드 인코딩·집계·커널은 `core/`만 사용한다. 재구현 금지.
- 좌표: x는 공격 방향, y가 낮을수록 오른쪽. `cells_from_points` → `encode` → `Kernel.best_fit_slot`.
- 역할군 argmax 전에 슬롯 유형 필터가 필수다.
- 적합값 Δ 0.02~0.05는 EA가 공개한 노이즈 구간이므로 그 차이만으로 인선을 바꾸지 않는다.
- 히트맵은 요구 역할의 일부만 설명한다. duties·1차 발언·전술 영상이 명확하면 낮은 fit보다 우선할 수 있다.
- 단일 경기·퇴장·저점유 같은 교란은 confidence와 보고서에 함께 쓴다.
- ⭐ **불변규칙 7(팀 축 혼선)은 실제로 두 번 터졌다** — 런북의 슬롯 x 표(08-14·08-24)와
  음바예 regime_id 오배치(08-31, obs#355). **타 팀 실측을 쓸 때는 출처 팀·체제를 반드시 명기한다.**
- ⭐ **불변규칙 10(다국어)의 최고 실증**: 아하노르 거래 구조는 **이탈리아어에만**, 무드리크 £75m 매수옵션은
  **우크라이나어에만**, 응게상의 미충족 선행조건은 **프랑스어에만** 있었다(2026-09-01).
  영어권만 봤으면 **거래 형태 자체를 오독**했을 건이다.

## 참고 문서

- `docs/20-fc-game-system.md`: 슬롯 x, 역할·포커스, 게임 구현 규칙.
- `docs/30-data-rules.md`: 수집, 좌표, 그리드, 표본·결손 규칙.
- `docs/40-pipeline.md`: DB/export/dump/git 파이프라인.
- `docs/50-transfer-policy.md`: 이적 등급·보존 정책.
- `docs/60-research-methods.md`: 새 축 검증과 통계 기준.
