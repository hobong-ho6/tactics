---
name: transfer-watch
description: 아스톤 빌라 이적 루머 정기 감시 — 스캔·크로스체크는 서브에이전트에 위임하고, 메인 세션이 추가 기사 검사·등급 확정·실측·transfer_targets 반영을 맡는다. 스케줄(매일 09/21시) 또는 수동(/transfer-watch)으로 실행.
---

# 빌라 이적 루머 감시 파이프라인

작업 디렉터리: `/Users/user/Documents/tactics`. 규칙은 CLAUDE.md와 docs/30-data-rules.md를 따른다.

## 0. 실행 구조 — 스캔은 서브에이전트, 판정·실측·DB는 메인 세션 (2026-07-30 확정)

§1~2(소스 스캔 + 티어 크로스체크)는 **`Agent` 툴로 서브에이전트에 위임**한다. 검색·페이지 읽기가
대량 토큰을 쓰는 데 반해 산출물은 "이름·등급·URL" 목록뿐이라, 메인 세션의 컨텍스트를 §3 이후
(실측·커널 계산·DB 쓰기·리포트)에 남겨두는 편이 낫다.

- **서브에이전트 범위**: §1 스캔 + §2 크로스체크. `subagent_type: general-purpose`.
  프롬프트에 반드시 포함할 것:
  ① 오늘 날짜, ② **DB 쓰기·파일 편집·git·`scripts/` 실행 금지(읽기·검색 전용)**,
  ③ `reports/transfer-watch/<오늘>.md`를 먼저 읽고 **같은 날 이미 판정된 건은 새 근거가 있을 때만 보고**,
  ④ 3티어 목록(Fichajes·CaughtOffside·thehardtackle·insidefutbol·givemesport·Yardbarker 등)과
     **애그리게이터가 인용한 원출처를 추적하라**는 지시, ⑤ 아래 4개 절 고정 보고 형식
     (신규 이름 후보 / 기존 행 상태 변화 / 크로스체크 실패 / 변동 없음 확인) +
     **항목마다 URL·보도 발행일 필수**, ⑥ **§2-0 발행일 검증을 티어 판정보다 먼저 하라**는 지시
     (나이 표기·병기된 타 구단 상황으로 교차검증 — 1티어 매체도 1년 전 기사를 실어나른다).
- **메인 세션 범위**: 서브에이전트 보고를 받은 뒤 ⑴ 등급 **최종 판정**(에이전트 제안은 참고값이고
  보존 정책 적용·슬롯 결정은 메인이 한다), ⑵ 애매한 건에 대한 **추가 기사 검사**(1티어 직접 확인,
  원출처 추적, 상충 보도 대조), ⑶ §3 실측·커널 적합도, ⑷ §4 DB 반영, ⑸ §4-2 리포트, ⑹ §5 커밋·푸시.
- 에이전트를 띄운 직후 대기하지 말고, 메인 세션은 그 사이 **실측 백로그(PENDING MEASUREMENT)**나
  전날 미해결 항목을 먼저 처리한다. 보고가 오면 합쳐서 리포트를 쓴다.
- 헤드리스 스케줄 실행에서 `Agent` 툴을 쓸 수 없으면 메인 세션이 §1~2를 직접 수행한다(기존 방식).

## 1. 루머 소스 스캔 *(TransferFeed·WebSearch는 서브에이전트 / Fotmob은 메인 세션)*

- `WebFetch`로 https://www.transferfeed.com/clubs/aston-villa/15 를 읽고
  **영입(incoming) 루머 선수 목록**을 추출한다 (선수명, 소속, 포지션, 루머 요지).
  ⚠️ **TransferFeed의 "Nh ago" 스탬프는 원기사 발행 시각이 아니라 피드 수집 시각이다** (2026-08-03 실증:
  Dobbin "16h 전 임대 이적"의 실제 사실은 07-15 완전이적 완료). "최근 몇 시간 이내" 판별에 단독으로 쓰지 말 것.
- ✅ **Fotmob은 2026-08-03에 복구됐다 — 브라우저 경유로 계속 사용한다** (`/rumours?teamIds=10252`).
  - **수집 주체는 메인 세션이다.** 브라우저 창(pane)은 세션당 하나뿐이라 서브에이전트와 동시 사용하면 충돌한다.
    §0대로 스캔 에이전트를 띄운 **직후 대기 시간에** 메인 세션이 다음을 실행한다:
    `preview_start {url: "https://www.fotmob.com/rumours?teamIds=10252"}` → `get_page_text`.
    루머 테이블 30행이 완전히 렌더링되고 `teamIds` 필터도 정상 적용된다.
  - 왜 이게 되는가: 07-23~07-31 전건 실패의 원인은 레이트리밋이 아니라 **CSR vs 정적 GET의 구조적 불일치**였다
    (`WebFetch`는 셸/헤더만 받는다). 렌더링하는 클라이언트를 쓰면 그대로 풀린다. → **`WebFetch`로는 여전히 불가.**
  - **고유 가치**: 루머마다 **출처 매체와 날짜를 라벨링**한다(예: `ST Nicolas Jackson / Jul 21 / Fabrizio Romano`).
    TransferFeed에 없는 정보이고, TransferFeed가 놓치는 이름을 실제로 잡아낸다(2026-08-03: Scienza·Ferrán
    Torres·Bowen·Woltemade·Gakpo 등).
  - ⛔ **그러나 라벨을 티어 근거로 쓰지 말 것.** Fotmob은 `Watkins → Fenerbahce`를 "Sky Sports"로 표시하지만
    실제 원출처는 전부 터키 매체(Sabah·Fotomac·Sercan Hamzaoglu)였고 Sky 보도는 확인되지 않았다. 게다가 루머
    행은 기사 URL이 아니라 **선수 페이지로만 링크**돼 라벨을 원문으로 검증할 수 없다.
    → **이름·날짜 발굴용 리드 소스로만 쓰고, 티어 판정은 §2 원문 추적으로 별도 수행한다.**
  - Fotmob에서만 나온 이름은 **메인 세션이 직접 §2 크로스체크**한다(에이전트는 이미 실행 중이라 전달 불가).
- ⚠️ `WebSearch`로 공백을 메운다 — 예: `"Aston Villa" transfer news <날짜>` ·
  `"Aston Villa" signing agreed` · `"Aston Villa" exit transfer`.
  ⛔ **Sky Sports 빌라 라이브 블로그는 2026-08-02~03에 누적 5회 이상 접근 실패**("blog currently unavailable") —
  "당일 1티어 확인" 경로가 막혀 있다. 대체 소스 1곳 확보가 최우선 백로그.
- 이미 `transfer_targets`에 있는 선수는 상태 변화(협상 단계 진전/무산)만 확인.
  `sqlite3 data/avl_analysis.db "SELECT name, slot, likelihood FROM transfer_targets WHERE window='2026-summer'"`

## 2. 1~2티어 기자 크로스체크 *(서브에이전트 담당 — 최종 판정은 메인 세션)*

새 이름 또는 상태 변화 후보마다 `WebSearch`로 확인한다:
`"Aston Villa" "<선수명>" transfer` (+필요시 기자명).

- **1티어**: Fabrizio Romano, David Ornstein(The Athletic), Sky Sports 공식,
  BBC Sport, The Athletic 클럽 담당(Jacob Tanswell 등).
- **2티어**: Telegraph, Times, Guardian, Birmingham Mail(빌라 전담 John Townley 등),
  Football Insider 수준의 전국지·전담 기자.
- 그 외(어그리게이터, 팬사이트 단독)는 **3티어 — 크로스체크 실패로 간주**.

등급 규칙:
| likelihood | 조건 |
|---|---|
| HIGH | 1티어가 협상/합의 단계를 보도 ("advanced talks", "agreement", "here we go") |
| MEDIUM-HIGH | 1티어 관심 보도 또는 2티어 복수가 협상 보도 |
| MEDIUM | 2티어 1곳 이상이 구체적 관심 보도 |
| 크로스체크 실패 | DB에 추가하지 않음 (다음 실행에서 재확인만) |

### 2-0. 발행일 검증을 티어 판정보다 **먼저** 하라 (2026-08-03 추가)

⚠️ **티어가 높아도 기사가 1년 전 것이면 아무 의미가 없다.** 2026-08-03 하루에만 **10건**을 이 검사로 걸러냈고,
그중 **Sancho/Lammens 건은 BBC Sport 본체 + Romano 원트윗**이었다 — 즉 **매체 티어 검사로는 원리적으로
잡히지 않는다.** 여름 이적창은 매년 같은 시기에 같은 구단·같은 포지션 루머가 돌기 때문에 **정확히 1년 오차**가
가장 흔한 형태다(같은 날 Yılmaz 건도 발행일이 정확히 1년 전이었다).

**신뢰하면 안 되는 지표** — 오늘 전부 실패했다:
URL 슬러그의 연도 · 검색 결과 노출 순서 · 애그리게이터 피드의 "Nh ago" 스탬프 ·
"최신"이라는 페이지 문구 · 트윗이 검색에 걸렸다는 사실 자체.

**실제로 함정을 잡아낸 지표 2개 — 이 둘을 먼저 본다**:
1. **본문 내 선수 나이 표기.** 현재 나이와 1살 이상 어긋나면 그 기사는 과거 것이다.
   (실증: 같은 칼럼에 "Jackson, 24"·"Sancho, 25" — 2026-08 기준 각각 25·26이다.)
2. **동시 병기된 타 구단·타 선수 상황.** 이미 결론이 난 사건이 "진행 중"으로 쓰여 있으면 과거 기사다.
   (실증: "맨유가 디부 두고 빌라와 회담 중"·"바이에른이 잭슨 입찰 철회"·"자니올로 대체자를 찾는 갈라타사라이".)

보조 수단: 트윗은 **status ID로 발행 시점을 확정**할 수 있다(예: `1962141760139759699` = 2025-08-31).
ID 자릿수·크기가 최근 트윗과 확연히 다르면 과거 것이다.

**판정 순서**: ⑴ 발행일 확정 → ⑵ 원출처 추적(애그리게이터면 인용 원문까지) → ⑶ 티어 판정 → ⑷ 등급.
발행일을 확정하지 못한 건은 `confidence`에 **"발행일 확인 실패"** 를 명기하고 등급 근거로 쓰지 않는다.

## 2-1. 경쟁 링크 강도 비교 (2026-07-30 추가) — 등급의 두 번째 축

§2의 등급표는 **"빌라 관련 보도의 티어"** 만 본다. 여기에 **경쟁 구도**를 더해 보정한다. 같은 선수를
두고 빌라보다 더 진전된 클럽이 있으면 빌라 성사 확률은 낮고, 빌라가 단독·최유력이면 높다.

- 전담 서브에이전트에 위임한다(§0과 동일 구조, 선수 6~7명씩 나눠 병렬). 선수별로 확인할 것:
  ① 빌라 링크의 **최신 단계**(관심<접촉<협상<개인합의<메디컬<합의) + 보도 기자·티어·날짜
  ② **경쟁 클럽별 단계·티어·날짜** ③ 선수 측 선호·거부 정황 ④ 셀링클럽 기조(잔류·블록·호가)
  ⑤ 구조적 제약(이적료 갭, 임대 vs 완전, PL 동일구단 임대 2명 불가 등)
- **강도 비교 순서**: 단계 → 티어 → 최신성. 판정은 `빌라 우위 / 대등 / 경쟁 클럽 우위(어디)` 3값.
- **등급 보정 규칙**:
  | 상황 | 처리 |
  |---|---|
  | 경쟁 클럽이 합의·메디컬 단계 | `DEAD (…행 확정)` 후보 → 삭제 검토 |
  | 경쟁 클럽 우위(협상 단계 앞섬) | 한 단계 하향 (HIGH→MEDIUM-HIGH 등) |
  | 대등 | 등급 유지 + rationale에 경쟁 구도 명기 |
  | 빌라 우위·단독 | 등급 유지, 상향은 §2 티어 요건을 별도로 충족할 때만 |
- 스키마는 바꾸지 않는다 — 비교 결과는 `rationale`에 `[경쟁구도]` 문장으로, 한계는 `confidence`에 남긴다.
- 리포트(§4-2)에는 `## 경쟁 링크 강도` 절을 만들어 선수별 우위 판정과 URL을 기록한다.

**보존 정책 (2026-07-21 확정)**: `transfer_targets`에는 **MEDIUM-HIGH 이상만 보존**한다.
MEDIUM·MEDIUM-LOW·LOW·DEAD로 판정/강등된 건은 DB에서 삭제하고, 그날의 근거는
리포트 파일(reports/transfer-watch/)에만 남긴다 (DB=실행 가능한 숏리스트, 리포트=전체 로그).
새 루머가 MEDIUM이면 리포트에 기록하되 DB에는 넣지 않는다.

## 3. 강한 루머(MEDIUM 이상) 분석 → DB 추가 *(메인 세션 담당)*

docs/20-fc-game-system.md의 영입 후보 파이프라인 그대로:

1. SofaScore API에서 선수 검색 → 최근 6경기(45분+, 히트포인트 15+) 히트맵 수집.
   **API는 sofascore.com 페이지 컨텍스트에서만 접근 가능** (claude-in-chrome javascript_tool).
   Chrome 연결이 없는 헤드리스 실행이면: transfer_targets에 map25 없이 행을 만들고
   confidence에 `PENDING MEASUREMENT`를 남긴 뒤 종료 보고에 명시한다.
   - 엔드포인트: 히트맵 `/api/v1/event/{eid}/player/{pid}/heatmap`, 스탯 `.../statistics`,
     경기목록 `/api/v1/player/{pid}/events/last/{page}` (역순 `player/{pid}/event/{eid}/...`는 404).
   - **탭 프리즈 주의 (2026-07-30 확인)**: sofascore.com 홈에서 fetch 루프를 돌리면 라이브 스코어
     스크립트가 렌더러를 얼려 CDP가 45초 타임아웃된다 — 레이트리밋이 아니다(7/29 오진).
     **새 탭 + `https://www.sofascore.com/robots.txt`(동일 오리진 경량 페이지) + `Promise.all` 병렬 fetch**로
     8경기 일괄 수집이 안정적이다. 얼면 새 탭을 만들어 재시도. `curl`은 UA/Referer를 붙여도 403.
2. 5×5 툴 그리드(툴x=100−소파y, 툴y=소파x) + 중심좌표 + 평균 평점 계산.
3. 커널 적합도: fc26-heatmap.html의 MAPS를 파싱해 해당 슬롯 x에서 placedMap
   (미러+시프트) 후 코사인 — 기존 세션 스크립트 패턴 재사용.
   - **파싱 함정 (2026-07-30)**: MAPS 블록의 **마지막 항목(`st_false9`)은 뒤에 개행이 없어**
     `\},?\n` 류 정규식이 조용히 놓친다. 파싱 직후 **역할 수가 37인지 확인**하고, 기존 행의
     저장값(**하지무사 .821** / **은디아예 .825** / Jackson .752 / **Quiñones .832=st_false9/Attack** /
     만잠비 .817 / 바투리나 .711 / **가르나초 LM .804=wm_winger/Attack**)이 재현되는지 회귀 검증할 것.
     슬롯 x 버킷: RM 86 · LM 14 · CAM·ST 50 · RB 86.
     > ⚠️ **[2026-08-06 정정]** 하지무사·은디아예 기준값은 원래 .923 / .883으로 적혀 있었는데, 이는
     > **obs#93·#94 커널 교체(placedMap 미러+시프트 → EA 정본 변형 선택) 이전** 값이다. obs#100이
     > 각각 .821 / .825로 재산출했고 DB도 그 값이다. 낡은 값을 게이트로 쓰면 **회귀 검증이 항상
     > 실패**한다. 나머지 4개(Jackson·Quiñones·만잠비·바투리나)는 2026-08-06 전수 재산출에서
     > 소수점 3자리까지 그대로 재현됐다 — 커널 교체의 영향은 wide 역할(RM/LM)에만 있었다.
     > 파이썬으로 `decodeMap`/`placedMap`/`cmpCos`를 재현해 검증해도 되고(브라우저 불필요),
     > 툴 함수를 브라우저에서 직접 호출해도 된다.
4. `transfer_targets`에 INSERT OR REPLACE (window='2026-summer', 근거 URL·등급·캐비앗 +
   **`short_label` 필수** — 툴에 쓸 짧은 한글/영문 이름, 예: `Matías Soulé` → `소울레`).
   실측상 부적합 슬롯(예: 적합도 <0.4)은 애초에 그 슬롯 행을 만들지 않는 것으로 대신한다.
5. **fc26-heatmap.html은 손으로 고치지 않는다.** DB 갱신 후
   `python3 scripts/sync_transfer_ui.py`를 실행하면 `TRANSFER_TARGETS`/`TRANSFER_OUTGOING`
   미러 배열이 재생성되고, 툴의 `injectTransferCandidates()`가 런타임에 SQUAD_SLOTS/
   PLAYER_BEST/XI_POOL로 자동 주입한다 (2026-07-14 리팩터, docs/20-fc-game-system.md 참조).

## 4. 상태 변화 처리

- 무산/타클럽 이적 확정: likelihood를 `DEAD (사유)`로 갱신 — `sync_transfer_ui.py` 재실행 후
  자동으로 SQUAD_SLOTS/XI_POOL 후보에서 빠진다(injectTransferCandidates가 DEAD 필터).
- 빌라 이적 확정: likelihood `CONFIRMED`로 갱신. 라벨 `(합류확정)`은 툴이 런타임에 자동
  붙이므로 손으로 안 바꿔도 됨. 시즌 데이터가 쌓이면 players로 승격 (docs/20 규칙).

## 4-3. 정체(STALE) 관리 — 2주 무소식은 DEAD로 숨기고, 새 보도가 나오면 복원 (2026-07-30 확정)

명단을 **컴팩트하게** 유지하기 위한 규칙. 툴에 뜨는 후보는 "지금 살아 있는 링크"만 남긴다.

- **판정 기준**: `last_news_date`(**빌라 링크**를 다룬 최신 보도의 날짜 — 그 선수의 타클럽 이적설
  보도는 갱신으로 세지 않는다)로부터 **14일 초과** 경과 →
  `likelihood='DEAD (STALE — 최신 보도 YYYY-MM-DD 이후 2주+ 무소식)'`.
  `transfer_targets`·`transfer_outgoing` 양쪽에 같은 기준을 적용한다.
- **적용 제외**: `CONFIRMED`(합류/이적 확정)와 `OWNED`(보유 선수)는 정체 판정 대상이 아니다 —
  이미 결론이 난 행이라 무소식이 정상이고, 숨기면 스쿼드·XI에서 확정 선수가 사라진다.
  즉 STALE은 **진행 중인 루머 등급(HIGH·MEDIUM-HIGH·MEDIUM…)에만** 적용한다.
- **⚠️ 함정 — 재확인 날짜를 쓰지 말 것**: `rationale`에는 매 실행이 `[2026-07-29 재확인 — 유지]` 식으로
  **우리가 확인한 날짜**를 남긴다. 이건 기사 갱신일이 아니다. 그것으로 판정하면 **어떤 행도 절대 정체되지 않는다**.
  반드시 **보도 자체의 날짜**를 `last_news_date`(TEXT, `YYYY-MM-DD`)에 따로 기록한다.
  (이 컬럼은 2026-07-30 추가. NULL = 아직 미확정 → 다음 실행에서 채운다. 값이 NULL이면 정체 판정을 보류한다.)
- **왜 삭제가 아니라 DEAD인가**: 툴의 `injectTransferCandidates()`가 `/^DEAD/i`인 행을 건너뛰므로
  (fc26-heatmap.html) **DEAD만으로 히트맵·SQUAD_SLOTS·XI_POOL에서 사라진다**. 행을 지우면 어렵게 얻은
  `map25`·`fit_sim`·실측 표본까지 잃고 부활 시 재측정이 필요하다 → **정체 건은 지우지 않는다.**
  (§2 보존 정책의 "DEAD는 삭제"는 **등급 강등·무산 확정** 건에 적용되는 규칙이고, 정체는 별개다.)
- **복원**: 새 보도가 확인되면 §2 등급표로 재판정해 `likelihood`를 되돌리고 `last_news_date`를 갱신한다.
  `sync_transfer_ui.py` 재실행만으로 툴에 다시 노출된다. rationale에 `[STALE 해제 YYYY-MM-DD]`를 남긴다.
- **매 실행 절차**: ⑴ 그날 확인된 보도로 `last_news_date` 갱신 → ⑵ 14일 초과 행을 DEAD(STALE) 전환 →
  ⑶ 리포트에 `## STALE 전환/해제` 절로 기록. 정체 전환도 "변동"이므로 sync+dump+커밋 대상이다.

## 4-1. 빌라 선수 유출(outgoing) 루머 확인

영입 스캔과 별도로, 빌라 기존 선수(`players` 테이블)의 이적설도 확인한다.

- `WebSearch`로 `"Aston Villa" "<선수명>" transfer` 또는 일반적으로
  "Aston Villa outgoing/exit rumours"를 스캔해 주전급 선수 유출 루머를 찾는다.
- 1~2티어 크로스체크는 §2와 동일 기준 적용.
- 통과한 건은 `transfer_outgoing(window, player_id, dest_club, likelihood, rationale,
  source, confidence)`에 INSERT OR REPLACE (player_id는 `players.id` FK).
  히트맵/커널 적합도 분석은 하지 않는다 — 이 테이블은 역할 적합성이 아니라 유출 위험을 추적한다.
- 이적 확정 시 likelihood `CONFIRMED`로 갱신 (player_seasons 등 승격은 별도 판단).

## 4-2. 일일 리포트 생성 (매 실행 필수)

DB 갱신과 별도로, **그날 수집한 기사·업데이트를 모은 리포트를 파일로 남긴다.**
`reports/transfer-watch/<YYYY-MM-DD>.md`에 작성한다(`<YYYY-MM-DD>`는 실행일).
같은 날 재실행이면 같은 파일을 **덮어쓰지 않고**, 파일 안에 `## <HH>시 실행` 섹션을 추가한다.

리포트는 스크립트가 아니라 이 실행이 직접 쓴다 — 원문 기사 서술은 WebSearch 결과에만
있고 DB 필드로는 복원되지 않기 때문. DB의 `rationale`/`source`와 그날 검색한 기사 내용을
결합해 아래 템플릿을 채운다.

```markdown
# 빌라 이적 감시 리포트 — <YYYY-MM-DD>

## 요약
- 스캔: 영입 ~N건 / 유출 ~M건 (소스: TransferFeed)
- 오늘 변동: 신규 X · 갱신 Y · 무산/DEAD Z

## 신규·갱신 (선수별)
### <선수> (<현소속>, <슬롯>) — <등급 old→new>
- 기사 요지: <그날 기사 1~3줄, 이적료·단계·경쟁 클럽>
- 출처: <기자/매체 (티어)>, <URL>
  (유출 건도 같은 형식으로. 실측 미수행 시 `실측 PENDING` 명시)

## 크로스체크 실패·보류
- <이름>: <사유 — 팬사이트 단독 / 미크로스체크 / 링크 소멸>

## 기존 행 재확인 (변동 없음)
- 영입: <등급 유지 요약>
- 유출: <등급 유지 요약>

## PENDING MEASUREMENT
- <이름(슬롯)> …
```

변동이 전혀 없는 날도 리포트는 남긴다(그날의 기사 로그·재확인 기록 보존).

## 5. 완료 기준 (매 실행)

- **DB 변경이 있으면**: `python3 scripts/sync_transfer_ui.py`(fc26-heatmap.html 미러 갱신)
  → `scripts/db_dump.sh`(dump 재생성) 실행. DB 변경이 없으면 이 둘은 건너뛴다.
- **리포트는 매 실행 작성**(§4-2) 후, 아래처럼 **파일을 명시 스테이징**해서 커밋한다.
  `git add -A`는 쓰지 않는다 — 저장소에 `.claude/settings.json`(Figma PAT 등) 등 커밋 금지
  파일이 있어 푸시가 차단된다:
  ```
  git add reports/transfer-watch/ data/avl_analysis.db data/dump/ fc26-heatmap.html
  git commit -m "data(transfer-watch): <요약> (<YYYY-MM-DD>)"
  git push
  ```
  (DB 변동이 없어 리포트만 있는 날도 리포트 파일만 스테이징해 커밋한다.)
- 종료 보고(터미널): 스캔된 이름 수 / 크로스체크 통과·실패 / 추가·갱신된 행 / PENDING 여부
  + **리포트 파일 경로**.
