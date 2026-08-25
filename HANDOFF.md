# HANDOFF

## 프로젝트

- 실제 감독 전술을 실측으로 분해해 FC26 전술로 재현한다.
- 대상: Aston Villa/Unai Emery(주), Chelsea/Xabi Alonso, Liverpool/Andoni Iraola, Atlético/Diego Simeone.
- 저장소: `/Users/ad03230205/Documents/tactics`, 브랜치 `main`.
- DB 정본: `db/tactics.db`. `db/dump/`와 `site/data/`는 파생물이다.
- 규약 정본: `CLAUDE.md`, `docs/00-overview.md`, 세부 문서는 `docs/`.
- 정기 작업 런북: `.claude/skills/transfer-watch/SKILL.md`, `.claude/skills/match-watch/SKILL.md`, `.claude/skills/player-collect/SKILL.md`.

## 현재 상태

> 마지막 갱신: **2026-08-25 저녁 KST** · 작업 PC `AD03230205ui-iMac.local` · 브랜치 `main` ·
> 마지막 커밋 `c4805a4`(origin/main과 일치, push 완료). 이 문서 자체의 커밋은 그 다음에 얹힌다.

- DB: players 190 · player_matches **4,074** · team_match_stats **61** · match_reports **25** ·
  match_player_reports **457** · squad_entries **126** · prescriptions **408** · **slots 88** ·
  match_game_setups **10** · match_player_prescriptions **164** · transfer_targets **38** ·
  transfer_outgoing **53** · player_duties **190** · observations **334**(최신 obs#334).
- 회귀: **G1~G12 전항 통과**(2026-08-25 마지막 확인). ⭐ 이날 **게이트 2건 신설** —
  G12 `orphan_preset_slots`(프리셋 pos_label이 그 팀 slots에 없으면 실패) ·
  G9 무버전 JS 임포트 검사(공유 모듈은 `?v=` 필수).
- ⭐ **적합값 드리프트: 차이 20 → 8 → 4**(obs#316 → obs#330). 좌우 이봉 분포 전수 점검 완료 —
  아래 「종결된 항목」 참조.
- ⛔⛔ **`site/assets/*.js`를 고쳤으면 임포트의 `?v=`를 반드시 올려라.** launch.json의 heatmap
  인라인 핸들러는 **HTML/JS에 no-store를 보내지 않는다**(그 파일 상단 주석). 2026-08-25에 이것 때문에
  `decodeMap` 수정이 브라우저에 도달하지 못해 같은 버그를 두 번 보고받았다. 이제 **G9가 막는다**.
- ⛔ **curl·WebFetch로 FotMob·SofaScore API를 치지 말 것** — 페이지 컨텍스트 밖에서 막힌다(404/403).
  **브라우저(Playwright 또는 in-app 브라우저)로 해당 오리진 페이지를 연 뒤 `page.evaluate`/JS 콘솔
  안에서 fetch**하면 200이다. ⭐ 2026-08-25 확인: SofaScore API가 **서브에이전트(WebFetch) 컨텍스트에선
  403**이었지만 **메인 세션 브라우저(sofascore.com 오리진)에선 200**이었다 — 사이트 차단이 아니라
  호출 경로의 문제이므로, 403 보고를 받으면 먼저 브라우저 경로로 재확인한다.

### 2026-08-23 PL Round 1 수집

| 팀 | 경기 | 핵심 실측 | 상태/리포트 |
|---|---|---|---|
| AVL | Brighton 4–0 Aston Villa | 점유 27%, xG 0.31–3.67, 슛 6–21, PPDA 24.69. João Gomes 40′ 퇴장 | `draft` · `reports/match-watch/2026-08-23-avl-brighton.md` |
| LIV | Newcastle 2–2 Liverpool | 점유 61%, xG 2.98–1.58, 슛 27–13, PPDA 5.95. Gakpo 52′, Szoboszlai 90+9′ PK | **`complete`** · `reports/match-watch/2026-08-23-liv-newcastle.md` |
| CHE | Fulham 2–3 Chelsea | 점유 38%, xG 1.70–1.34, 슛 18–14, PPDA 20.18. Palmer 1G1A | `draft` · `reports/match-watch/2026-08-24-che-fulham.md` |
| ATM | 비야레알 2-2 (라리가 R2, 홈) | xG 0.78–3.60, 76′ DOGSO 퇴장, 주전 첫 가동 4-4-2 | **`complete`** · `reports/match-watch/2026-08-23-atm-villarreal.md` |

✅ **CHE 풀럼전(matchId 5795372) 전체 적재 완료.** FotMob 팀·선수 실측 + WhoScored/Opta 1,659 이벤트로
출전 16명 좌표/map25와 PPDA를 만들었다. 실제 3-4-2-1에서 Palmer–João Pedro–Rogers 전원이 득점에 관여했고,
Lacroix는 CCB에서 박스까지 올라가 도움을 기록했다. 다만 공식 전체 회견·지연 전술 영상은 아직 없어 `draft`다.
다음은 08-27 EFL컵(루턴 홈, id 6005665) · 08-30 브라이턴 홈.

**D+N 창 정정** — 경기일이 08-23이므로 D+1은 **08-24**(완료)다. 본문에 08-25로 적혀 있던 것은
오기이며 AVL 리포트에서 이미 정정됐다. 남은 창은 **D+3 = 08-25~26**.
D+2는 **08-24 21시에 조기 실시 완료**, 08-25에 D+3 정기 검색도 완료했다.

### 이번 경기 판정

- AVL: 50분간 10명이어서 PPDA 24.69와 Deep/38은 감독 의도보다 경기 국면의 영향이 크다.
  Buendía ST는 공백을 메운 응급 배치이며 시즌 처방으로 병합하지 않는다.
- LIV: 61% 점유·27슛에도 오픈플레이 xG는 0.96, 막힌 슛은 16개다. 공격량과 박스 공략의 질을 분리한다.
- LIV 두 실점은 모두 공격 진영 소유권 상실 뒤 전환에서 발생했다. 이라올라 이식의 잔여수비 리스크는 유지한다.
- Víctor Muñoz는 교체 27분에 마지막 PK를 유도했다. Rio Ngumoha와 RM 선발 경쟁을 다시 연다.
  ⭐ **D+2에서 「직접 맞교체」로 확정됐다** — 63분 무뇨스 IN ↔ 응구모하 OUT(FotMob 이벤트 원본).
  같은 슬롯 수행 대비라는 간접 근거가 **감독이 그 자리에서 바꿨다**는 직접 근거가 됐다.
- Ryan Gravenberch는 Gakpo 골을 도왔지만 두 실점 전 소유권 상실에도 관여했다. Roaming 피벗의 양면성 표본이다.
- ⭐ **LIV D+3에서 Coaches' Voice 전술 보드와 Between The Posts 초록을 확보했다(obs#321).**
  Wirtz·Szoboszlai가 뉴캐슬의 선수지향 마커를 바깥으로 끌고 Gakpo가 중앙으로 들어간 동점골 구조가 확정됐다.
  지연 전문 분석·공식 회견·전 선수 처방이 갖춰져 `complete`로 승격했다.
- **AVL D+3은 팟캐스트 4건의 공개 설명을 수확했지만 전술 영상·전문 블로그 0건**(obs#322).
  오디오를 듣거나 전사하지 않았으므로 새 전술 문장은 채택하지 않았고 `draft`를 유지했다.
- **CHE**: 38% 점유에도 xG 1.70·18슛·박스 터치 37로 전환 효율이 높았다(obs#323).
  반면 Fulham 620패스·Sánchez goals prevented -0.78로 중원/GK 리스크가 남았다(obs#325).

## 자동화

- Codex heartbeat **id=3 「프리미어리그 3팀 경기 수집」**, 매일 08:00 KST.
- 매 회차 순서: 기존 draft 리포트 D+1~D+3 점검 → 새 종료 경기 확인 → match-watch 전체 파이프라인.
- 새 경기/후속 근거가 없으면 저장소를 변경하지 않는다.
- 이적 감시는 cron `transfer-watch.sh`가 09:00/21:00 각 1행. macOS TCC/marker probe 검증 완료.

## 종결된 항목

### 2026-08-25 세션 (transfer-watch 09시 + Dutch 스윕, match-watch 사이드 이봉 점검)

- ✅ **transfer-watch 09시 회차 — 신규 2 · 강등 1 · 원장 결함 1건 삭제 · 실측 1건.**
  `reports/transfer-watch/2026-08-25.md` 참조. 커밋 `d427b8d`.
  - **AVL 하파엘 레앙 신규(MEDIUM-HIGH)** — 1티어 2곳(Sky Italia·Di Marzio) 「trattativa in corso」,
    단 오퍼 0건(Moretto가 같은 날 「단순 아이디어」로 적음)이라 HIGH 미승격.
    **SofaScore 실측 완결**: 세리에A 6경기(404분) → 커널 최적 **wm_insidefwd/Balanced 0.834**(LM),
    LST 0.747·ST 0.549·RM 0.280으로 좌측 전용 프로필. 커널 회귀 검증 통과.
  - **LIV 코디 각포 신규 유출(MEDIUM-HIGH)** — 맨시티가 08-25 접촉(Romano/Di Marzio),
    조건부(리버풀은 윙어 2명 영입 성사 시에만 매각, 1순위 바르콜라). 08-24 리포트의
    「매수측 입찰 0건」 오류를 정정(토트넘 £60m가 08-15에 이미 거절당함).
  - ⭐⭐ **원장 결함 삭제**: ATM `transfer_outgoing` 그린우드(player_id=180) 행이
    **우리 자체 `player_tenures`로 직접 반증**됐다(ATM 시즌 없음, 실제는 마르세유→페네르바흐체).
    ATM은 매수 후보였다가 07월에 철수한 것이었다 — 삭제.
  - ATM 파르도 MEDIUM 강등(뉴캐슬·라이프치히가 ATM보다 앞섬), 알바레스 「잔류 수렴」 부분 철회
    (ESPN 1티어가 아스날 마감주 실행 의사 명시).
  - ⭐ **사용자 요청으로 각포 축 네덜란드어 추가 스윕** — 원발굴자 Mounir Boualin(Soccernews.nl) 확인,
    club-to-club 접촉 0건 재확인, AD.nl/Elfrink가 접촉 시점을 「vorige week」로 적어 Romano
    「today」와 **시점 불일치**(다음 회차 대조 과제로 남김). 리포트에 「추가 스윕」 절로 추가.
- ✅ **좌우 이봉(bimodal) 분포 전수 점검(obs#328·#329)** — 확정 고정 40명 점검, 7명 이봉·4명은
  전체 집계가 사이드 능력을 심각히 과소평가. **린델뢰프**(AVL CB) 전체집계 0.75 → 사이드분리
  **LCB .952 / RCB .929**(둘 다 최상급, obs#316의 NULL 보류가 정답이었음을 확인). 무뇨스·오나나·
  바클리·맥알리스터·자케도 사이드 전용값으로 갱신. `squad_entries` 6행 갱신 + `prescriptions`에
  `measured:side:L/R` 12행 신설(UNIQUE 제약상 squad_entries에 좌우 두 행을 넣을 수 없어 분리).
  ⭐ **무뇨스는 이후 사용자 지시로 재판정 완료(obs#330)** — 분량(좌 22경기)보다 최근 기용(이라올라
  체제는 우측, 08-23 응구모하와 직접 맞교체)을 우선해 주 사이드를 **LM(.771) → RM(.834)** 로 전환.
  좌측 값은 `measured:side:L`에 보존. **파생 발견**: LIV 좌측(LM)이 학포 1명뿐으로 비어 — 학포가
  맨시티/토트넘 이적으로 이탈하면 LM 후보 0명. 커밋 `a626c77`·`a24d0ad`·`f6c5116`.
- ✅ **응구모하(pid=114) `squad_entries` 결손 채움(obs#331)** — 개막전(08-23 뉴캐슬) RM 선발인데
  행이 없었다. 같은 좌우 이봉 패턴(친선 4경기+PL 1경기, hp≥15)이나 무뇨스보다 판단이 단순했다 —
  분량(우측 170분>좌측 90분)·최근기용·유일한 공식전 표본이 전부 우측을 가리켜 **RM wm_winger/Attack
  .812**를 그대로 채택. 좌측(LM .837·n=2·프리시즌뿐)은 `measured:side:L`에 보존. 커밋 `9e1a262`.
- ✅ **경기 재현 프리셋 칩이 한 자리에 겹치던 버그 — 원인 3개 전부 수정(obs#332)** 커밋 `b72b778`·`79c158e`.
  증상은 하나였다: 좌표 JOIN이 실패하면 `left:undefined%`가 되고 CSS가 무시해 11명이 겹친다(조용히 깨진다).
  ⑴ **formation 문자열 불일치**(AVL 22 · LIV 3·20·23) — `'4-2-3-1'` vs slots `'4-2-3-1 Wide'`. 표기만 정합.
  ⑵ **그 팀에 해당 포메이션이 없음**(ATM 24) — 실제 4-4-2인데 slots는 4-1-4-1뿐. formation을 고치면
  기록 왜곡이므로 `core/export.py`에 **기하 폴백** 추가(커널이 이미 formation을 무시하고 첫 행을 쓰는 것과 같은 규칙).
  ⑶ ⭐ **존재하지 않는 슬롯으로 산출**(CHE 2) — 피벗이 LDM/RDM인데 CHE엔 그 슬롯이 없다. 역산으로
  저장값이 **LDM 50·RDM 61**(어느 팀 slots에도 없는 값)에서 나온 것을 특정했다. 경위: 그 리포트는
  CHE slots가 백4뿐이던 2026-08-16 작성이고 3-4-2-1 슬롯 추가 시 이관되지 않았다. LCM/RCM으로 재산출
  (카이세도 .896→.807 · 라비아 .913→.831, 역할 `dm_dlp`→`cm_holding`은 슬롯 유형이 CM이기 때문).
  ⇒ **G12에 `orphan_preset_slots` 신설**(폴백이 ⑴은 흡수하지만 ⑶은 못 잡는다). 회귀 주입으로 발화 확인.
- ✅ **ATM 4-4-2 슬롯 신설(obs#333)** 커밋 `e1a720b`. 근거: R1 Opta formations가 4141(0~61분)→**442(61~96분)**,
  R2는 선발부터 4-4-2. 기하는 ATM 자체 실측만 사용(불변규칙 7). ⭐ **원 저자의 「단일 포메이션만 등록해
  CHE 비결정 결함을 재현하지 않는다」를 만족시켰다** — CHE 결함의 원인은 포메이션이 둘인 게 아니라
  **8개 pos에서 x가 달랐다**는 것이라, 공유 pos 7개의 x를 4-1-4-1과 **완전히 동일**하게 넣어 커널이
  여전히 결정적이다(전수 확인). 저장 fit 전량 재산출 **불일치 0**.
  ⛔ **report 24 처방은 이관하지 않았다** — 측정이 반대를 가리킨다(이강인 ST Δ1.8 vs LST Δ9.2 등
  3명 악화·2명 동일, 전방 3명 툴y가 62~64로 같은 높이). 「명목 4-4-2 / 실측 4-1-4-1 기하」다.
- ✅ **경기 히트맵이 '전체 출전자'에서 안 나오던 버그(obs#334)** 커밋 `e1a720b`·`c4805a4`.
  ⑴ 1차 원인은 **`decodeMap(null)`이 TypeError를 던진 것** — 호출부가 `.filter(Boolean)`로 이미
  falsy를 걸러내게 쓰여 있었는데 `map()`에서 던져 `renderPitch` 전체가 중단됐다. AVL 브라이턴전은
  **16명 중 15명이 유효 히트맵을 갖고도 0명분이 그려졌다.**
  ⑵ ⛔ 고쳤는데도 계속 비었다 — **브라우저가 구 kernel.js를 캐시**하고 있었다(위 「현재 상태」 경고 참조).
  `?v=` 추가 + **G9 검사 신설**로 닫았다. 진단 단서는 **캡션이 셀렉터와 어긋난 것**(「선발 합성 11/11」
  ↔ 선택은 '전체 출전자')이었다 — 캡션이 맨 끝줄이라 중간에서 던지면 직전 상태로 남는다.
  ⇒ 캡션을 **그리기 전에** 쓰도록 순서를 바꿔 재발 시에도 사실과 다른 표시가 남지 않게 했다.
  ⑶ **교체 선수 히트맵 8건 신규 수집**(SofaScore, G2 회귀 3,031행 불일치 0). 나머지 결손은
  `event_id`가 **음수(FotMob 합성 키)**라 수집 불가, 가르나초는 4분 출전 **hp=0 확정 결손**.
  ⑷ 출전자 범위 기본값 **'선발 11명'**, 경기 드롭다운 **공식전/프리시즌 optgroup 분리**.

### 2026-08-24 세션 (압축)

- 드리프트 6건 전량 데이터 오류 0건(원인은 `check_fit_drift.py`의 `pos_only`/포메이션 혼입) —
  스크립트 수정으로 차이 20→8. NULL fit 13행은 최초 시드 누락으로 정체 확정, 8행 백필.
  AVL/LIV D+2 조기 실시(교체 상대 확정, 2025년 기사 혼입 차단).

## 다음 할 일

### match-watch
1. ⭐ **CHE 풀럼전 D+2(08-26)·D+3(08-27)** — 알론소 공식 전체 회견, 클럽 전술 영상,
   Palmer/Rogers/João Pedro 선수별 분석, 지연 전술 블로그를 재검색한다. 0건도 리포트에 기록한다.
2. **AVL Brighton전은 비정기 재시도 조건부 draft** — 공식 전체 회견/클럽 전술 영상,
   경기 전용 전문 분석 또는 팟캐스트 공식 전사가 나오면 다시 연다. 정기 D+1~D+3은 완료.
3. **PL 다음 라운드**: AVL/LIV/CHE 실제 경기마다 동일 파이프라인을 반복한다.
   가장 가까운 CHE 08-30 Brighton 홈에 앞서 08-27 Luton EFL컵도 match-watch 범위 여부를 확인한다.
4. Atlético 이후 경기는 별도 match-watch 일정. 그리말도 실측이 채워지면 2경기 슬롯 기하·fit·sort_order 연쇄 재검증.
5. ⭐ **LIV 좌측(LM) 영입 공백** — 무뇨스·응구모하 둘 다 RM으로 확정되며 LM은 학포 1명뿐임이
   드러났다(obs#330·#331). 학포가 이적(맨시티/토트넘 2파, MEDIUM-HIGH)하면 LM 후보 0명 — 영입 축 검토 필요.
6. **전후(x축, 라인 높이) 이봉 점검은 아직 안 했다** — obs#328~331은 좌우(y축)만 봤다.

### transfer-watch (마감 2026-09-01, D-7)
1. ⭐⭐⭐ **레앙(AVL) — 정식 오퍼 제출 여부.** Di Marzio(협상 중) ↔ Moretto(단순 아이디어) 상충은
   오퍼 하나로 갈린다. 밀란 재개선선 €50m.
2. ⭐⭐⭐ **고레츠카(AVL)·디사시(CHE) 구단 공식 발표** — 둘 다 Romano HWG+메디컬 완료 단계에서
   구단 공식만 미발화. 발화 즉시 CONFIRMED 승격.
3. ⭐⭐ **각포(LIV 유출) — Elfrink 「vorige week」 vs Romano 「today」 시점 대조** + 시티/토트넘 중
   구단 간 대화로 올라가는 쪽 확인.
4. **민테(LIV) 3차 입찰**·**바르콜라(LIV) 2차 서면 오퍼** — 둘 다 여러 회차 미발화이며 각포 매각의
    선행조건이다.
5. **왓킨스 이적 정황을 계속 추적한다** — 개막전 20인 제외가 부상이 아니고 에메리가 사유 답변을
    3회 거부했다. 08-24 훈련 복귀로 방향이 갈렸다. 이적 확정 시 `squad_entries` ST 행(fit 0.722)과
    9번 처방 전체가 재판정 대상이다.
6. Minteh는 2026-09-02에 개선 오퍼 0건이면 등급 재판정한다.
7. **FIFA art.10 국제 임대 쿼터 1차 규정문 확인** — CHE 임대 정리 축(잭슨·에수구·무드리크·워싱턴·
    켈리먼) 전체가 「6칸 중 4칸」↔「스트라스부르 마지막 1칸」 수치 충돌 상태다.

## 데이터 수집 상태와 결손

- 대량 수집: `collect_fotmob_players.py`, `collect_understat_shots.py`; `check_fit_drift.py`는 읽기 전용.
- ⛔⛔ **검색엔진 연도 혼입에 주의.** 2026-08-24 실측 사례 — 스웨덴어 검색 요약이 뉴캐슬–리버풀 2-2를
  「**Slots** radikala högalinje」로 설명했는데 26/27 리버풀 감독은 **이라올라**다. 원문 fetch 결과
  검색엔진이 **2025-08-25 동일 카드**(슬롯 체제, 응구모하 막판골) 기사를 섞은 것이었다.
  **같은 상대·같은 8월·유사 스코어의 전년도 경기는 반드시 발행일을 확인하고 쓴다.**
- ⚠️ **verbatim 인용은 요약 경유 시 열화된다.** 같은 기자회견 답변이 매체별로 3종(에메리·왓킨스 건),
  같은 「PL 매치센터」 성명이 2종(고메스 죄목)으로 갈렸다. **실질만 채택하고 인용문은 원문 확보 전까지 쓰지 않는다.**
- Understat은 빅5(+RFPL) 슛/창조 대체 원천이나 챔피언십·에레디비시·리가2는 없다.
- SofaScore 403이면 축2 실측/R2 그리드를 억지로 채우지 않는다. WhoScored 접근을 먼저 재프로브한다.
- Sofifa 35속성/playstyles, FBref 12축은 403 결손 상태다.
- 결손과 0을 구분한다. API 키 생략은 확정 0일 수 있으므로 `docs/30-data-rules.md` 규약을 따른다.

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

## 참고 문서

- `docs/20-fc-game-system.md`: 슬롯 x, 역할·포커스, 게임 구현 규칙.
- `docs/30-data-rules.md`: 수집, 좌표, 그리드, 표본·결손 규칙.
- `docs/40-pipeline.md`: DB/export/dump/git 파이프라인.
- `docs/50-transfer-policy.md`: 이적 등급·보존 정책.
- `docs/60-research-methods.md`: 새 축 검증과 통계 기준.
