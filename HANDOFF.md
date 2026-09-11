# HANDOFF

## 프로젝트

- 실제 감독 전술을 실측으로 분해해 FC26 전술로 재현한다.
- 대상: Aston Villa/Unai Emery(주), Chelsea/Xabi Alonso, Liverpool/Andoni Iraola, Atlético/Diego Simeone.
- 저장소: `/Users/ad03230205/Documents/tactics`, 브랜치 `main`. DB 정본 `db/tactics.db`
  (`db/dump/`·`site/data/`는 파생물).
- 규약 정본: `CLAUDE.md`, `docs/00-overview.md`. 런북: `.claude/skills/{transfer-watch,match-watch,player-collect}/SKILL.md`.

## 현재 상태

> **2026-09-12 KST** · PC `AD03230205ui-iMac.local` · `main` · 마지막 커밋 **`1c6241b`** — 직전 `0aa7c79`·`e0f45b1` ·
> **✅ origin 일치**(push 완료) · ⚠️ 미추적 폴더 `reports/ingame/*`(이전 세션 스크린샷, 커밋 여부 사용자 판단).
> **09-12 세션 요약**: ⑴ 스쿼드 결손 축 보강(FotMob 15명, 조나단 데이비드 `fotmob_id` 해결) ⑵ ⭐ **FC25·FC26 출시판 게임스탯 176행 시계열**
> (`scripts/collect_futgg_history.py`, fut.gg 정의 API curl) + `player.html` 「버전별 변화」 표 ⑶ 종합평가 19명 갱신 → **스쿼드 전원 09-10 이후 기준**
> ⑷ ⛔ 리스 제임스 FC27 행 오염(로렌 제임스 값) 정정(obs#616). ✅ 음바예 `team_code` 재점검 → **동일 유형 109행 정정**(음바예 23·HB 12·알랑 72·로저스 2, obs#617). ⚠️ 별건: `player_matches.team_code` **NULL 1,432행**(v1 승계 「PL/EL」 라벨 행 다수) — 판단 대기.
> **09-11 스케줄 태스크(브뤼헤전 D+2 추적)**: `reports/match-watch/2026-09-08-avl-brugge.md`에 D+2 절 추가(obs#609~613·615,
> 결번 #614는 자기 검증 중 되돌림). 상세는 아래 「최근 작업」 참조.
> **09-11 세션 요약**: FC27(EA 공식 확정, 09-10) PlayStyles·키·몸무게·카드이미지를 4팀 전원(AVL·CHE·LIV·ATM) 수집,
> `player.html`을 fut.gg식 카드+메뉴로 재구성, `player_evaluations` 128행(98명 갱신 포함) 리프레시,
> **squad_entries에서 CONFIRMED 이적 완료 선수 32행 삭제**(핵심 정책 변경, 아래 참조).
> ⛔⛔ **정책 변경**: 이전 핸드오프의 "`squad_entries.lh`가 OWNED로 남는 건 정상"은 **더 이상 유지하지 않는다.**
> 이번 세션에 `squad_entries ⋈ transfer_outgoing WHERE likelihood='CONFIRMED'`로 전수 대조해 **32행**(AVL 8·CHE 4·LIV 4·ATM 1,
> 총 17명 — 일부 중복 슬롯 포함)을 찾아 **삭제**했다(마르티네스→첼시, 커티스 존스→인터 등 거물급 포함). FK 참조 없어 안전.
> ⇒ **다음 세션은 새 CONFIRMED 이적이 뜨면 즉시 squad_entries에서 지운다** — "런타임 필터링이 있으니 괜찮다"고 미루지 말 것.

- DB: players **206** · player_matches **4,252** · team_match_stats **70** · match_reports **34**
  (**complete 19 · draft 15**) · match_player_reports **598** · **squad_entries 117**(이적 정리 후) ·
  prescriptions **469** · slots **88** · match_game_setups **19** · match_player_prescriptions **306** ·
  transfer_targets **44** · transfer_outgoing **67** · player_duties **208** ·
  player_shirt_numbers **116** · understat_player_matches **5,634** · **teams 37** · **player_evaluations 128** · **transfer_summary 4** · `game_role_focus.movement_kr` **85/85** ·
  `team_match_stats.xg_source` **62/70** · `game_system_changes` **18** · **reproduction_limits 13** · **ingame_captures 75**(T1 15·T2 14·T3 13·T4 11·SIM 11·T5 11) · team_tactic_setups **24**(ingame 6행) · observations **588** · match_reports **36** · player_matches **4,922** ·
  `match_game_setups.rule_note` **19/19**(재판정 후 RULE 8 · DIVERGE 7(사유 명시) · NO-STATS 4) · `player_matches.cells_def` **0/3,363**(다음 경기부터) ·
  `player_game_stats`(FC27, roster_date=2026-09-10) **131행**(AVL·CHE·LIV 103 + ATM 26 + 완비사카·하우드-벨리스·미겔요렌테 보강 3) —
  **playstyles 87/131 non-empty**(나머지는 EA 확정 0종, NULL 아님) · 신설 컬럼 `weight_kg`·`card_image_url`.
- 회귀: **G1~G15(+G8+) 전항 통과**(이번 세션 매 DB 변경마다 재확인). 회귀 테스트 3종(g13·g14·g8x_g15) 09-08 이후 미재실행(변경 없음).
- **이적창 후속 절차 계속** — 위 정책 변경으로 squad_entries는 이제 매 세션 이적 확정분을 즉시 반영해야 한다. 미결 4건(에메날로·르마르·바르가스·응게상)은 등급 동결 유지.
- ⏰ **보류 확정(사용자 지시 09-11)**: 포파나(CHE, LCB 실측)·귀스토(CHE, RCM 기용)·아라우호(LIV, RB 인버트)는 **단일 경기 표본이라 Δ규칙상 커널 갱신 보류** —
  실제로 갱신하려면 해당 경기 SofaScore 좌표(map25)를 새로 수집해야 한다(현재 없음). 다음 표본이 쌓이면 재검토.

### 반복해서 사고를 냈던 규칙 (지우지 말 것)

- ⛔⛔ **불변규칙 2(추가만·재작성 금지)는 리포트 파일뿐 아니라 DB 행에도 적용된다 — 09-08 실증(obs#517·#518).**
  `1211c43`이 obs#503의 4필드를 **`UPDATE`로 제자리 덮어썼고**, 파생 피해 2건이 실제로 났다: ㉠ `.replace()` 실수로 **텍스트 중복**
  ㉡ **UCL 사실을 `evidence`에만 넣고 `claim`의 PL 서술을 남겨 한 행에 두 대회 축이 섞임**(claim↔evidence 정반대 진술).
  ⇒ **정정은 언제나 새 obs 행으로 한다**(⛔ 위반을 위반으로 고치지 않는다 — obs#503도 되돌려 덮어쓰지 않았다).
  ✅ **이제 G14가 막는다.** 정당한 재작성은 `G14_ALLOW_REWRITE=<table>:<id>`로 통과시킨다. 보호 테이블은
  `observations`·`player_duties`뿐(`transfer_targets`·`prescriptions`·`match_reports`는 편집이 정상 작업 — 근거는 `gates.py` 주석).
- ⛔⛔ **파생 컬럼에 「어휘 정본」이 없으면 세션마다 다른 말을 써 넣는다 — 09-08 실증(obs#527).** `pos_class`는 값이 있는 839행 중
  **450행이 정본 어휘 밖**이었고(core 어휘 + 별도 스크립트 어휘 + 손으로 친 문장), `lineup_pos`도 같은 병이다(G/D/M/F ↔ 슬롯 라벨 ↔ NULL).
  ⇒ **새 파생 컬럼은 허용 값 집합을 먼저 정하고 게이트로 묶어라.** ⭐ **독스트링이 거짓말을 할 수 있다** — 옛 `pos_class`는
  「슬롯 x 정본표로 세분류한다」면서 `slots`를 한 번도 참조하지 않았다. **주석이 아니라 코드를 읽고 확인할 것.**
- ⛔ **팀 설정 3축(빌드업·수비접근·라인)을 산문으로 정하지 말 것 — 09-08 실증(obs#532).** 규칙(docs/20 「팀 설정 매핑 규칙」·`core/team_settings.py`)을
  먼저 돌리고 다르면 `rule_note='DIVERGE: 사유'`. 백필에서 **19행 중 14행이 편차**였다(같은 PPDA 대역에 High/72와 Balanced/55가 공존). G15가 사유 없는 편차를 막는다.
- ⛔ **게임에 입력할 수 없는 처방이 또 있었다 — 09-08 실증(obs#533).** CHE 선발 12명·슬롯 없는 LDM/RDM 4행·교체 6행 역할군 밖. **G8+가 막는다** —
  `prescriptions.kind`는 `KIND_RE` 형태만(새 접두는 게이트+docs/00 동시 수정).
- ⛔⛔ **xG 계열은 한 회차에 같은 스냅샷으로 수집하고 `xg_source`를 함께 채운다**(FotMob matchDetails 한 응답에 전부 있다).
  따로 채우면 Opta 사후 개정 때문에 「오픈플레이 > 전체」라는 불가능한 값이 된다. ⛔⛔ **검산(`xg − xg_op` ≈ PK × ~0.79)은
  스냅샷 동일성을 증명하지 않는다** — 비야레알전이 검산을 통과하면서 제공사가 갈려 있었다. **제공사는 `xg_source`로 확인**하고
  교차 경기 집계는 `WHERE xg_source='FotMob'`으로 고정한다(정본 `docs/30` ⑧ · match-watch SKILL §3).
- ⛔⛔ **지연 발행 자료를 검색엔진 질의로 「0건」 처리하지 말 것**(09-08 실증, obs#516) — 4회 질의해 0건이던 두 영상이 **이미 게시돼 있었다**
  (인덱싱만 늦었다). ⇒ **D+2~D+3엔 유튜브 사이트 내부 검색으로 스윕**: `youtube.com/results?search_query=...&sp=EgIIAw%3D%3D`(업로드=이번 주)
  후 JS로 `watch?v=` href 회수. **매체 기사도 같다 — 403/0건은 브라우저 경로로 재확인**(헐전에서 요크셔포스트·avfc.co.uk 성공).
- ⛔ **`observations.id`를 하드코딩하면 동시 실행 세션과 충돌한다**(09-08 실증, 경합 3번째). `max(id)` 읽고 INSERT 하는 사이에
  다른 세션이 #500~505를 선점해 **트랜잭션 전체가 롤백**됐다. ⇒ **id 생략(자동 배정)하거나 `BEGIN IMMEDIATE` 직후 재확인**하고,
  리포트·상호참조의 obs 번호는 **INSERT 성공 후에 기입**한다.
- ⛔ **동시 세션이 있으면 새 파일도 Write 전에 `git log -- <path>`로 이력을 본다**(09-08 실증). 아침에 미추적(`??`)으로 보인
  `test_g14_regression.py`가 그 사이 다른 세션 커밋에 들어가 있었고, Write로 **덮어썼다가 `git show`로 복원**했다.
- 🔴 **커밋만 하고 푸시 안 함 — 2회 재발.** 세션 시작 시 `git status -sb`의 **`[ahead N]`을 반드시 본다**(obs#382 유형).
- ⛔ **curl·WebFetch로 FotMob·SofaScore API를 치지 말 것** — 페이지 컨텍스트 밖에서 막힌다(404/403). 브라우저로 오리진을 연 뒤
  JS 안에서 fetch하면 200이다(✅ SofaScore는 08-19 이후 재개통 — 차단으로 단정하지 말고 먼저 확인한다).
- ⛔⛔ **`site/assets/*.js`를 고쳤으면 임포트의 `?v=`를 반드시 올려라**(G9가 막는다).
- 🔴 **obs#110 솔버 산출을 인용할 때는 obs#111 이후인지 확인한다** — obs#111이 C6를 하드화해 **정본은 좌측 전진**이다.
- ⭐ **유튜브 자동 자막 회수**: `scripts/yt_transcript.py VIDEO_ID LANG` → `reports/transcripts/`. 봇 차단(「page needs to be reloaded」) 시
  브라우저 pot 경로 `scripts/yt_transcript_json3.py`(정본 docs/30). 영상·음성은 시청 불가 — 인용 시 confidence에 **auto-caption** 명기.
  ⏰ docs/30 「듣지 않은 영상은 인용 금지」에서 **「전사를 읽은 영상」의 지위는 미정의** — 규약 갱신은 사용자 판단 대기.

## 자동화

- Codex heartbeat **id=3 「프리미어리그 3팀 경기 수집」**, 매일 08:00 KST (저장소 밖 · 별도 관리).
- ⚠️ **스케줄 정본은 `mcp__scheduled-tasks__list_scheduled_tasks`다** — `CronList`는 다른 시스템이라 0건으로 보인다(09-03 오판 확정).
- **활성**: `match-watch-weekly`(월 10:06) · `weekly-unifi-now-sync`(월 10:03) ·
  `match-watch-avl-hull-followup-d3`(09-09 11:00, 헐전 마지막 회차) ·
  ⭐⭐ `match-watch-avl-brugge-2026-09-08`(09-09 **13:00**, 브뤼헤전 UCL MD1 수집 — **11:00 헐 d3과 겹치지 않게 13:00**,
  obs id 경합 3건 이력). 브뤼헤 프롬프트: 0단계 종료 확인 · 프리뷰 대조 · ⛔ **CL/PL 축 분리** · 재검증 6항목 ·
  🇰🇷 이한범 포함 언어축 · **D+1~D+3 자기 예약**.
  ⭐⭐ **신설 일회성 `match-watch-dplus-che-arsenal-d3`(09-09 **15:00** KST, 활성)** — 첼시-아스날전 D+3. **11:00 헐 d3·13:00 브뤼헤 수집과 겹치지 않게 15:00**.
  프롬프트에 D+2 미해소 6건(🇪🇸 매체 6곳 브라우저 재시도·알론소 스페인어 회견 원문·막힌 URL 5개·파머/로저스 공격 국면 분담·「too early」 대상 선수·선제골 형태 4중 충돌)을 담았다.
  ⚠️ **당일 회차는 D+1~D+3 예약을 「했다」고 리포트에 적었으나 실제로는 생성되지 않았다** — 예약 문구를 쓰면 태스크 목록으로 실재를 확인할 것.
- ✅ **[09-08] 소진 일회성 태스크를 전부 정리했다** — 삭제 전 **산출 커밋을 전건 확인**했고 소실은 없다. `SKILL.md` 원문은 디스크에 남는다.
  ⚠️ 헐 d2·`-atm-athletic-d3`은 **삭제 전에 이미 목록에서 사라져 있었다**(09-08 09:15 조회에는 있었다). 소멸 경로 미확인, 산출(`ca42991`·`1274101`)은 정상.
  ⇒ ⭐ 「자기를 띄운 태스크는 그 세션에서 못 지운다」 규약에 **반례가 관측됐다. 재확인 필요.**
  삭제분 11건: 헐 d1 · liv-ipswich-d3 · atm-athletic-d2 · `transfer-feed`(69회) · `supercup-collect` · 브라이턴 개막전 ·
  `unifi-p0-…-0828-imac` · R3-followup d1/d2/d3 · 헐 본수집. ⚠️ `unifi-p0-…`만 **타 프로젝트라 이 저장소에서 산출 검증 불가**(실행 기록만 확인).
  ⇒ ⭐ **스케줄이 「활성 5건」으로 정리됐다**: 정기 2(unifi 월 10:03 · match-watch 월 10:06) +
  일회성 3(헐 d3 **09-09 11:00** · 브뤼헤 **13:00** · CHE 아스날 d3 **15:00**). ⚠️ **09-09에 3건이 몰린다 — 규칙 9·obs 번호 경합 주의.**
- ⭐ AVL 영상 회차는 **필수 채널 3곳**(UTV · The Villans · 1874, docs/30 표)을 항상 조회한다.

## 최근 작업

### 2026-09-12 ⑾ — 결손 수집 · FC25→FC27 게임스탯 시계열 · 종합평가 19명 (`0aa7c79`·`1c6241b`, obs#616)

- **FotMob 결손 15명**(`collect_fotmob_players.py --resolve-ids`): detail +144·season +38·traits +12·market +84·status +7. 조나단 데이비드 fotmob 939569
  (Lille→Juventus→ATM 텐유어). 니콜자줄리 포지션 DB CM ↔ FotMob AM 불일치는 덮지 않고 보고만. 유스 6명(도밍게스·카스티요·모레노·라하도·미겔 요렌테·니콜자줄리)은 표본 자체가 없다.
- ⭐⭐ **FC25·FC26 출시판 시계열**: fut.gg `/api/fut/player-item-definitions/{25,26}/{eaId}/`가 **curl 200**(브라우저 불필요) — 34속성·PS(+)·키·몸무게·AcceleRATE·`createdAt`.
  EA id는 FC27 09-10 행 `card_image_url`의 `27-{eaId}`에서 회수(sofifa_id=EA id, 48명 채움). **fut.gg base 아이템 = 출시판 값**(왓킨스 FC26 base 84 = fut.gg Δ 기준 ↔ sofifa 시즌말 82)
  ⇒ `roster_date=createdAt`, 기존 sofifa 라이브판과 공존. 폐지 PS id 24=Trivela(페이지 확인), 4/18/27은 추정+런타임 검증. 카드 없음 20건(유스·비지원 리그)은 결손 유지.
  export `game_stats/history.json`(player_id 키, kind 출시판/라이브판) 신설, `{GV}.json`은 라이브판만(name_kr 가로채기 방지) — FC25.json은 만들지 않는다.
- ⛔ **동일성 사고 1건**: 09-10 리스 제임스 행이 로렌 제임스(첼시 위민, eaId 265249)의 키 175/몸무게 77/PS 7종/카드로 오염 — OVR·6종합·attrs는 리스 본인. 정정 + obs#616.
  ⇒ **fut.gg 이름 검색은 남녀 카드를 섞는다 — EA id·gender로 특정**(스크립트에 gender==1+이름 토큰 검사 내장).
- **종합평가 19명**(AVL 3·CHE 10·LIV 6, 병렬 에이전트 4개 → SQL 검토 후 적용, 덧붙임만). 잠정 등급 변경: 아체암퐁 B+→B · 팔레스트라 A-→B(공식전 5경기 0분, 사유 미수집) ·
  웰벡 C+→B- · 라크루아 A-→B+ · 콜윌 B+→B · 켄다 fit MEDIUM-HIGH→MEDIUM. ⚠️ CHE(a) 5행이 **이중 적용**돼(파일 내 BEGIN/COMMIT + 내 래퍼 충돌) 중복 덧붙임을 자체 검증으로 제거 — 에이전트 SQL은 BEGIN/COMMIT 유무를 먼저 본다.

### 2026-09-11 ⑽ — 브뤼헤전(09-08) D+2 추적, 스케줄 태스크 (`f4bb1cc`)

- D+1이 남긴 미해소 항목을 재작업: **에메리 회견 육성 재구성**으로 「he's not the player with qualities
  to running behind but he tried … fantastic, Emiliano」의 지칭 대상을 **헤밍스**로 특정(부엔디아·잭슨
  둘 다 아니었음, obs#609). 세이스 오버랩/언더랩 소스 충돌은 미해소로 남김(obs#610).
- 🇧🇪 벨기에 3도메인(hln.be·nieuwsblad.be·gva.be)이 브라우저 경로로 다시 열려 VP-Rapport 개별 평점
  확보(obs#613). UEFA.com matchId 확정(2049556, 서술형 리포트 자체가 사이트 구조상 없음, obs#611).
  Coaches' Voice 정본 경로 재확인 — 진짜 0건(obs#612).
- ⛔⛔ **자기 오류 정정 사례**: `cpIZf5nxK-4`(UTV 잭슨 분석 영상)를 D+2 신규 발견으로 오인해
  전사·obs·player_duties에 반영했다가, git log 대조로 **D+1 당일 `§8-3 addendum`에 이미 전사·반영**돼
  있었음을 발견하고 전량 되돌렸다(전사 파일 `git checkout --`, obs 삭제 → 결번 **#614**, player_duties
  중복 문단 제거). **불변규칙 2 위반을 커밋 전에 자체 검증으로 잡은 사례** — 다음 세션도 새 발견을
  DB에 쓰기 전 `git log -- <파일>`로 기존 반영 여부를 먼저 확인할 것.
- 결장자 갱신: 마조(Madjo) 결장 사유가 발목 부상으로 신규 확인(obs#615). 게이트 전항 통과, export·dump·push 완료.

### 2026-09-11 ⑼ — FC27 4팀 전량 수집(PlayStyles·키·몸무게·카드) + player.html 재구성 + 종합평가 98명 + squad_entries 이적정리 32행 (`2205d24`…`4108bba`)

- **FC27 확정 데이터 수집**: EA 공식 09-10 드롭이 실제로 PlayStyles까지 포함해 라이브됨을 fut.gg로 재확인(이전 세션 obs#579의 "여전히 미확정"은 하루 뒤인 09-11에 뒤집혔다).
  fut.gg 벌크 API(`/api/fut/players/v2/27/?club_id=N`)로 AVL(2)·CHE(5)·LIV(9)·ATM(240) 4개 클럽 로스터 전량 + `/all-versions/{eaId}` 개별 조회로 키·몸무게를 수집.
  `player_game_stats`에 `weight_kg`·`card_image_url` 컬럼 신설. `core/export.py` game_stats 쿼리에 반영.
- **player.html 재구성**: fut.gg식 선수 카드(OVR·6스탯·PlayStyles 아이콘+한글 툴팁+실제 카드이미지) 신설. 메뉴를 `카드·종합평가/경기스탯/게임스탯/영상분석` 4탭으로.
  경기스탯 비교기준 기본값=리그 전체, 세부속성 기본 펼침, 영상분석 최신순 정렬. PlayStyle 아이콘·설명은 `site/assets/playstyle-icons.js`(fut.gg 카탈로그 36종, 한글 번역).
  `glossary.js`의 툴팁 위임 선택자를 `abbr.gl`→`.gl`로 확장해 재사용.
- **player_evaluations 98명 갱신**(AVL 32·CHE 15·LIV 19·ATM 32) — 팀별 배경 에이전트를 6개 안팎 병렬 하위그룹으로 나눠 FC27 신규스탯·최신 경기·서사를 반영. AVL은 fit_emery, CHE는 fit_alonso, LIV는 fit_iraola 컬럼 사용·ATM은 3컬럼 모두 미사용(fit_simeone 컬럼 없음 — 시메오네 적합은 overall/strengths 산문에 서술).
- ⭐⭐ **squad_entries 이적 정리 32행**(핵심 발견) — `squad_entries ⋈ transfer_outgoing(likelihood='CONFIRMED')` 전수 대조로 각 팀 현재 스쿼드에
  이적 완료 후에도 남아있던 행을 찾아 삭제. AVL(콘사·왓킨스·산초·게상·네델코비치·**마르티네스**·베일리·일링주니어) · CHE(델랍·로베르트 산체스·아다라비오요·에수구·찰로바·엔소) ·
  LIV(모리슨·엘리엇·은두크웨·**커티스 존스**·코나테·살라) · ATM(히메네스). FK 참조 없어 안전. 이전 핸드오프의 "OWNED로 남아도 정상" 가이드는 **폐기**.
- **데이터 결손 재확인**(AVL→CHE→ATM→LIV 우선순위): 완비사카·하우드-벨리스는 구단 공식 합류 확인되지만 EA FC27 DB가 아직 구소속(웨스트햄·사우샘프턴)으로 표기 —
  스탯은 신뢰, club 필드만 EA 반영 지연으로 수집·보강. 미겔 요렌테(ATM)는 fut.gg가 별명 "Miguel Cubo"로 등재해 최초 이름매칭에서 누락된 것을 eaId 대조로 발견·보강.
  **진짜 결손 확정**(fut.gg 원본 자체에 카드 없음, 재수집 불가): 고레츠카(자유계약 공백기)·니콜자줄리·호르헤 도밍게스·호르헤 카스티요·알바로 모레노·호르헤 라하도(전부 무명 유스)·조나단 데이비드(ATM 실측 0경기).
- 포파나(LCB)·귀스토(RCM)·아라우호(RB 인버트) 실측-커널 불일치는 **단일 경기 표본이라 보류**(Δ규칙, 사용자 확인) — 위 「현재 상태」 참조.
- 매 DB 변경 단계마다 `gates.py`(전항 통과) → `export.py` → `db_dump.sh` → 커밋(6회 분할 커밋, 위 해시 범위).

### 2026-09-09~10 ⑻ — ⭐⭐ 인게임 A/B 3·4·5 · 시뮬 1 · 커널 신뢰도 뷰 (`fadba9d`…`c970189`, obs#538·567·568·587·588, captures 30~85)

- **T3** `?ZWKtKhw6ere`(LM wideplm/A, RB wingback/B, RM 후반 음바예): LM을 wideplm으로 바꾸자 **뱅크 대신 더 높이**(부엔디아 0%·가르나초 0.8%) — 커널 자체가 자기진영 0. 맥긴 widemid 재현 T2↔T3 .94.
- **T4** `6YSGpGdk2ana`(마첸만 att_wb→wingback/B): 마첸 그리드 4경기 .88~.94 동일 — **풀백 라벨 무효**. 군내 최적은 늘 falseback.
- **SIM 1** `9ZVJsJYv5dqd`(커리어 관전, 빌라 2-0 레스터, GK ballplaying/BU): ⭐⭐ **시뮬≈사용자**(잭슨 .72~.94·만잠비 .73~.86·맥긴 .97) ⇒ 조작 오염은 형태를 못 바꾼다.
  스크립트 `--heat white`(커리어 흰 히트맵)·ST 점 기준(GK 화면)·강조선 스케일 폐기(스크롤로 이동). GK 역할 두 종 모두 골라인 고정(goalkeeper/Defend .92).
- **T5** `4YQEnEbi&YS4`(**빌드업 Balanced** 단일 변수, 전술 화면 캡처로 11명 HIGH): **전원 이전 경기와 .77~.97 동일** — 빌드업은 히트맵에 무영향. ⚠️ 패스네트워크 2장 때문에 선수 매핑 한 칸 밀림 → cos 0.0 이상치로 발견·재적재. **처리 전 썸네일에서 이름 대조 필수.**
- **뷰**(029): `v_kernel_fidelity`(역할별 게임↔커널 cos, n≥3 HIGH/MID/LOW) → report.html 「게임검증」 열 · `v_ingame_capture_norm`(팀 평균 대비 자기진영 편차 — 기준선이 27.7~50.4%로 흔들려 절대값 금지).
  현재: dm_dlp/R .78 HIGH · cb_bpd/A .64 HIGH · cb_bpd/BU .60 · wideplm/A .54 · holding/BW .49 · widemid/S .45 MID · **att_wb/S .43 · wingback/B .31 · winger/A .21 LOW**.
- 기타: 전술 코드는 오프라인 해독 불가 — **EA 웹앱에 코드 임포트 → Roles 화면 캡처**로 역할 확정(사용자가 로그인) · compare.html 「합류확정」→「신규」(`f4398cf`, lh 값 보존) ·
  브뤼헤 D+1~3 스케줄 **23:00**으로 이동 · UTV 잭슨 D+1 영상 전사(`cpIZf5nxK-4`, obs#567·568 — 미끼 러닝·백힐 기점, 포레스트 백3 단서) · FC27 PlayStyles **09-10 밤 기준 아직 미공개**(EA 페이지 확인).

### 2026-09-08 ⑺·⑹ — 인게임 캡처 1차(`1aeefa2`·`8a623fd`·`a24217e`, obs#536·537) · 프로젝트 점검 후속 7건(`fb9033b`, obs#531~535, migration 027·028)

- ⑺ Remote Play 캡처 경로 확정·스크립트 정본화 · **FC26 히트맵은 위치 기반** · ⭐⭐ 맥긴 wideplm/A→widemid/S로 자기진영 5.9→38.9% · 재현성 .86~.91 · docs/50 한계 표.
- ⑹ 점검 판정(obs#531): 팀 설정 3축 실측 얇음·국면 분리 0 → ⑴ 인게임 경로(obs#534, `ingame_heatmap_to_grid.py`+`ingame_captures`) ⑵ `core/team_settings.py` 규칙 사전등록 → `rule_note` 백필 → **G15**,
  편차 14행 재판정(규칙 채택 7·유지 7, obs#535) ⑶ `cells_poss/def`·`def_x` 컬럼(다음 경기부터 필수) ⑸ 귀스토 RB 0·CHE LDM/RDM deprecated·mpp 교체 6행 정본화 ⑹ 프로필 20행 ⑺ `reproduction_limits` 12행.
  ⛔ 브라우저 JS PPDA 재구현 금지(불변규칙 4). 문서 docs/00·20·30·50 + `test_g8x_g15_regression.py`.

### 그 이전 (압축)

- **09-08 ⑸ pos_class 재작성**(`ad1296b`, obs#527~530) — 포메이션→11슬롯 표 core 이관, 좌우=`slots.x` 주 신호·깊이 0.15 동점 해소, 얇은 표본 NULL(97행), 적합·처방 불변. obs#467 정정(네투 RM). 국면 어휘 툴팁 9종.
- **09-08 ⑷ CHE**(`387a079`, obs#519~526) — 첼시-아스날 D+2: 유튜브 사이트내검색으로 당일 0건 반전(3번째) · 구조 정정 백4↔백5 하이브리드(아체암퐁만 전진) ·
  아르테타 인용 2건이 전년도 회견 재순환이었음을 정정.
- **09-08 ⑶ G14**(`9ad583e`→`1427b36`, obs#518) — 「원장 정정 규약」게이트 편입: prefix 보존(덧붙임만) 불변식, 델타 검사로 obs#503 보호. 역검증 적발 1=사고 1건.

- **09-08 ⑴ ATM 축**(`1274101`, obs#506~516) — 아틀레틱전 D+3 종결: **obs#452 인과 철회**(하이프레스는 아틀레틱 쪽) · 4-4-2 유지·요렌테 5포지션(obs#508) · 최종 5-4-1 독립 확인(obs#507) ·
  obs#459 ⓒ「진짜 9번 부재」 3가설(obs#510) · 감독 발언 3항 질문 자체 없음(obs#493). 미도달 확정: theobjective·atleticodemadrid.com·El Correo·EITB.
- **09-07**(obs#466·#472~480·#499) — AVL 필수 채널 3곳(UTV·Villans·**1874**) · 전사 26+7편 → `player_duties` 16행 · ⭐⭐ **xG 정책**: 저장값 정본·개정 추종 안 함, 교차 집계는 `xg_source` 필터.
- **09-08 ⑵ AVL 축**(`ca42991`·`1211c43`, obs#500~505) — 헐전 D+2: 요크셔포스트 평점으로 D+1 판정 철회(obs#500) · Coaches' Voice 「0건」 반전 → **캐시 뒤 이음새 구조 결손 승격**(obs#502) ·
  「전진 패스 회피」 형질(obs#503, **obs#517과 함께**) · 잭슨 피패스 ¼(obs#504) · 브뤼헤 프리뷰(감독 **이반 레코**, 하옌 자료 금지).
- **09-05~06 헐전 종결·LIV/ATM 수집·포켓 충돌 정정·migration 025**(obs#446~465) — ⭐⭐ **잭슨 false9는 성향이 아니라 국면 반응**(obs#446) ·
  obs#447 무공 4-4-2 보류 · obs#448 캐시 뒤 이음새 2경기 연속 · obs#449 ⚠️ 4경기 집계 풀백 att_wb 역전(정본 유지) ·
  LIV·ATM **압박 급락**(⭐ 이라올라 「윙어 양쪽 다」 선언) · 「점유 대비 박스 효율」 가설 **기각**(r=+0.23), 대신 **AVL 유효슛 이상치**(obs#462) ·
  ⭐⭐ **포켓 충돌 정정**(obs#464) — 세트 A(insidefwd/B·halfwinger/R) / B(wideplm/A·playmaker/R), **10번 유형이 와이드를 정한다**.
- **09-04**(obs#435~445, gsc #10~18) — **FC27 사전 조사**(상세 docs/21): Attacking Spatial Awareness · Triggered Runs 거리 제한 ·
  AcceleRATE 축소 · PlayStyle 리밸런스 · **Team Press 수비 3분의 1 무효** · 커리어 7포지션. ⛔ **역할·포커스는 미공개**.
  **movement_kr 85조합**(정본은 `description` = EA 원문; 이름과 실제가 갈리는 조합은 ⚠️) · **윙 혼잡 회피**(docs/20 ⑨) —
  ⚠️ **`fb_att_wb`/Support = 복귀 감소, 전진은 Attack**, 대가는 **뱅크 소멸** · 아스날전 D+3(스즈키 롱볼은 **상대 의존 처방**, 🇯🇵).
- **09-03**(obs#422~423) — 잭슨 프리셋 역할 유지(Δ0.30, 온볼 서사는 PlayStyle 층) · **베일리 → 올림피아코스**(추적 3축 전부 빗나감).
  ⭐⭐ 교훈: 「미결」 시한을 열린 창으로 잡지 말 것 · 총평에 예상 행선지 금지 · **현지 매체 활발 ≠ 축 생존**.
- **09-02**(obs#414~421) — `transfer_summary` · `player_evaluations` 120행 · SKILL §2-1a 「감독 회견 원문+번역 필수」 ·
  ⭐⭐ **docs/22 = 온볼 층**, 커널 유사도에 넣지 않는다. ⚠️ 워싱턴(CHE) 이적료 3중 병기 미해소.
- **09-01 무결성 정리 4연쇄**(obs#368~374) — 전부 「FK는 성립하는데 조용히 이중화된」 부류: 에수구 2-id 병합 · 이중 기록 78쌍 ·
  **`team_code` 739행** 재배정 · **G13 신설**. 🔴 파급: **완비사카·잭슨·루제리 소속팀 실측 0**.
  ⭐ **team_code 오류는 게이트를 무력화한다**. ⭐⭐ **아하노르 = 아탈란타발 팰리스 임대 + 첼시 선계약(2027-07-01)**, 완전영입 서술은 오답.
  같은 날 AVL 아스날전 수집 — **SofaScore 403 재발** → WhoScored/Opta `matchCentreData`(인앱 오리진) 대체.
- **08-24~31** — ⭐ 사용자 확정 원칙(obs#348): **개별 경기 구현은 그 경기 전술의 게임 재현이므로 분석을 전부 반영한다**(시즌 정본은 누적으로만) ·
  ⭐ **압박 상수 3건**(obs#350~352): 알론소 22.67 · 이라올라 **5.76(최안정)** · 시메오네 8.26(**저블록 서사와 어긋난다**) ·
  ⭐⭐ **음바예 regime_id 3→1 정정**(불변규칙 7 위반, 적합 0.94→**0.878**) · 좌우 이봉 7명·**전후 이봉 0건**(obs#342).

## 진행 중 작업 (WIP)

**없음.** `fb9033b`+핸드오프 커밋까지 푸시 완료, 워킹트리 깨끗.

## 다음 할 일

0. ⭐⭐ **P1 · 다음 인게임 A/B = 「우측을 안쪽형으로」(사용자 결정 09-10)** — T5 구성에서 **맥긴 RM widemid/Support → wideplm/Attack + 캐시 RB wingback/Balanced → falseback/Balanced**만 바꿔 사용자 플레이 1경기.
   판별: 왼쪽 마첸·부엔디아(또는 가르나초)의 열0(터치라인) 질량이 22~39%·1~18% 대역을 벗어나 **바깥으로 밀리면 「우측 균형 반응」**, 그대로면 **4-2-3-1 Wide 슬롯 기하** → 그 다음 포메이션 A/B(Narrow/4-3-3).
   폴더 `reports/ingame/2026-09-1x-avl-test6/` 생성 후 동봉: 전술 화면(코드·11명 역할) · 히트맵 11장 · 팀 통계 1장 · 조작 선수. ⚠️ 처리 전 썸네일 이름 대조.
   그 뒤 시뮬로 **수비 접근·라인 높이** 단일 변수(팀 설정 3축 중 미검증 2축). ⛔ 캡처 단독으로 처방 변경 금지(docs/50).
0-1. **P1 · 스케줄 세션 산출 검토** — 09-09~10 8커밋(브뤼헤 MD1·D+1, 헐 D+3, CHE 아스날 D+3·리즈, FC27 로스터, player-collect 6명, **CHE 4-2-3-1 Wide 슬롯 신설 `a3acd40`**)을 이 세션이 읽지 않았다.
   특히 `a3acd40`은 CHE 슬롯 어휘가 바뀐 구조 변경 — G8+/slot_canon 정합·docs/11 반영 여부 확인. 브뤼헤전 신규 필수 3항(PPDA·def_x·국면 그리드·rule_note·profile 갱신) 적용 여부도 첫 확인 대상.
0-2. **P2 · FC27 09-18 얼리액세스 후 4팀 역할·숙련도(Role+/++) 수집** — ⭐ **PlayStyles·키·몸무게·카드이미지는 09-11 완료**(4팀 131행, **FC25·FC26 출시판 시계열은 09-12 완료**),
    `2205d24`…`4108bba`). 남은 건 fut.gg `/api/fut/roles/` FC27 응답(역할·포커스 목록, docs/20 ② 타이브레이커의 전제) — 09-18 이전 확정 불가.
1. **P1 · 브뤼헤전 D+2(09-11 23:00)·D+3(09-12 23:00) 회차 확인** — UTV 전술 에피소드(D+1 예고) 회수 · 재검증 7항(report 35 §7)은 **09-12 포레스트전(PL R4 홈)** 에서 판정: 잭슨 국면 반응 ①, 풀백 좌우 복귀 ②, 무공 4-4-2 4번째 표본 ③, def_x 2번째 실측 ⑦. 포레스트 **백3+스텝업 CB** 단서(obs#568) 프리뷰에.
2. ⭐ **P1 · 09-09 안필드(리버풀·UCL, ATM R1) — 아틀레틱전 진단 4건의 직접 판별 경기.** ⑴ **가설 ⓒ 우선**: 알바레스 선발 예상 →
   **박스 터치·빅찬스 회복 여부**(ⓐ장신은 쇠를로트 결장으로 09-13로 밀렸다). ⑵ **obs#514**: PPDA **15 대역+60%대 점유**면 원정 공격 노선,
   **8 대역 복귀**면 부산물. ⑶ **obs#460/#511**: **그리말도 제외 + 한츠코 좌측**이 나오는가(obs#515는 결과 판정에 쓰지 않는다).
   ⑷ **감독 발언 3공란의 마지막 창구**. ⚠️ 확정 결장: 쇠를로트(근육) · 아르나우 오르티스(유럽대회 정지).
4. **P1 · obs#449 ⓐ/ⓑ 판별 — 양 풀백 att_wb 집계 역전이 체제 변화인가 국면 혼입인가.** 필요 조건: 점유 국면별(@dom/@tight)
   분리 집계가 **버킷당 2경기**. 74% 표본은 헐전 1경기뿐 → 다음 우세 경기 후 판정. 그때까지 **obs#443 짝짓기 규칙·정본(좌 전진·우 절제) 유지**.
   사용자 인게임 A/B 체감(윙어 쪽 wingback/B · 반대쪽 att_wb/**Attack**)은 여전히 미수집.
5. **P1 · 미결 이적 4건 개별 처리**(에메날로·르마르·바르가스·응게상) — 실효 시한 도래분부터. 절차는 「현재 상태」 마지막 문단.
6. **P2 · 아틀레틱 5-4-1 전환 시각 미확정** — 2소스 모두 분(分) 미명시로 obs#498·#507이 구간 분할에 못 쓰인다.
   ⭐ 남은 방법: WhoScored 이벤트 타임라인으로 **평균 위치 변화 시점 역산**.
6-1. **P2 · `player_matches.team_code` NULL 1,432행 판정**(obs#617 별건 — 콘사 48·디뉴 44·마첸 44·로저스 25/26 PL 37 등. v1 승계 라벨 「PL/EL」 행이 다수라 09-01 정리(obs#372·373)가 건너뛴 부류인지, 의도된 NULL인지 먼저 확인) · G13에 「선수×시즌 클럽↔클럽 혼입」 검사 사전등록 검토(중간 이적 예외 설계 필요) · 팔레스트라·켄다·기튼스 **공식전 미출전 사유** 미수집.
7. **P2 · 알렉사 푸리치(ATM) `sofascore_id` 재탐색**(obs#416) · **ATM 11명 map25 전량 결손** — `player-collect` 필요,
   값을 발명하지 않기로 확인됨(obs#415).
8. **P2 · obs#353 후속** — 학포 RM 배치로 「검증된 LM이 학포뿐」 리스크 재판정. ⭐ 무뇨스 LIV RM 선발 지정으로 전제가 바뀌었다
   (무뇨스 좌측 표본은 오사수나 — 불변규칙 7 캐비앗 유지).
9. **P2 · 경기 전용 처방 재판정을 match-watch 표준 파이프라인에 넣을지 확정** — R3 4경기에서 반복 적용됐다.
10. **P2 · 완비사카·잭슨·루제리의 소속팀 실측 0** — 클럽 표본이 쌓이면 `avg_positions`가 되살아난다.
   그때까지 이 셋은 **히트맵 A(실측) 칩이 없는 상태**다.
11. **P3** · 병렬 중복 실행 가드 미수립(obs#354, 데이터 재발 감지는 G13) · 겨울창(2027-01) transfer-watch 재개는 사용자 판단
   (런북은 저장소에 있어 스케줄만 만들면 된다) · 그리말도(ATM) 실측 채워지면 슬롯 기하·fit 재검증.

## 미해결 — 판단이 필요한 것

1. ⏰ **ATM 포메이션 표기 충돌 — 4-4-2 쪽으로 기울었으나 미해소 존속.** 비야레알전에서 우리·El Desmarque·COPE는 **4-4-2**,
   **Infobae는 「4-3-3 de Simeone」**이었다(obs#333 전제와 직결). ⭐ **09-08 진전**: ATM 전담 분석이 아틀레틱전 최종 포진을
   **4-4-2로 명시**(obs#508)하고 09-09 예상 XI도 4-4-2 ⇒ obs#454는 **강화 방향**. ⛔ 그러나 **감독 발언은 3일 창 내내 0건**이라
   확정 근거가 없다. ⭐ 실측 기하가 4-1-4-1에 더 가까워 처방 미이관 판단은 여전히 정합적.
   ⚠️ 별건: 「**salidas de tres**+라인 간 3명」은 **보유 국면 별도 축**으로 본다.
2. ⏰ **FC27 커널 대기** — 사전 조사는 09-04 완료(obs#445). **PlayStyles·6대스탯·키·몸무게 EA 확정 트리거는 09-11에 완료**(4팀 전량 수집).
   잔여 트리거: **09-18** fut.gg `/api/fut/roles/` FC27 → `migrate_fc27.py --roles --check` → `EXPECTED["FC27"]`·gates 앵커 **새 행** → `--apply`(승인).
   ⛔ 역할 목록 변화는 **미공개** — 확정 전 커널 행 금지. ⚠️ **고레츠카 FC27 게임스탯 0행은 확정 결손이다**(09-11 재확인 — 이적 전 자유계약 공백기라
   fut.gg 전 버전에도 카드가 없음, all-versions API로 직접 대조 완료) ·
   **35속성은 완비사카·음바예 2명**(obs#364).
## 데이터 수집 상태와 결손

- 대량 수집: `collect_fotmob_players.py` · `collect_understat_shots.py` · `collect_event.py`(이벤트 축).
- 읽기 전용 진단: `check_fit_drift.py` · `check_side_bimodality.py` · `check_height_bimodality.py` — ⚠️ 셋 다 **진단만 한다**
  (그리드 재적재·`pos_only`·처방 변경은 사람이 판단). ⭐ 회귀 테스트 `test_g13_regression.py`·`test_g14_regression.py`·`test_g8x_g15_regression.py`(결함 합성 주입) ·
  ⭐ `db_diff.py`(스냅샷 대비 행 단위 대조 — **NOT NULL→NULL 전이를 따로 센다**. FK 검사는 「값이 조용히 지워졌다」를 못 잡는다).
- ⛔⛔ **검색엔진 연도 혼입 주의.** 같은 상대·같은 달·유사 스코어의 전년도 경기는 발행일을 반드시 확인한다.
  ⭐ **엔진 요약 자체가 오염되는 유형**도 있다(과거 시즌 사건을 현재 확정 사실로 제시) — **엔진 요약은 근거로 채택 불가, 개별 URL 실물 확인만.**
  ⚠️ **verbatim 인용은 요약 경유 시 열화된다.** 실질만 채택하고 인용문은 원문 확보 전까지 쓰지 않는다.
- Understat은 빅5(+RFPL)만(챔피언십·에레디비시·리가2 없음). Sofifa 35속성/playstyles·FBref 12축은 403 결손.
- ⏰ **AVL LM/RM 슬롯 x 재검토는 표본 부족으로 보류**(obs#349). 재시도 조건: 정상 경기 누적 + 해당 경기 `cells` 수집.
- ⭐ **1차 소스 메모**: `laliga.com/clubs/{club}/transfers`는 등록 기준 1차 소스로 유효하나 날짜가 **행정 등록일**이라 구단 발표일과 다를 수 있다
  (`atleticodemadrid.com`은 403). 결손과 0을 구분한다(`docs/30`).

## 고정 작업 규칙

1. 시작 시 `git status --short`. 로컬 변경이 있으면 fetch/pull하지 말고 내용부터 확인한다. 깨끗할 때만 `git fetch && git pull --rebase origin main`.
2. 다른 PC/세션 변경을 버리거나 덮지 않는다. 특히 `db/tactics.db`는 충돌 시 기계 병합 금지.
3. DB 변경 뒤 반드시: `scripts/export.py` → `scripts/db_dump.sh` → `scripts/gates.py`. **`git add -A` 금지** — `db/tactics.db`,
   관련 `db/dump/`, `site/data/`, `reports/`, 문서를 명시 스테이징한다. push 전 `origin/main` 이동 여부를 다시 확인한다.
4. ⛔ **원장 행을 `UPDATE`로 고치지 않는다 — 정정은 새 obs 행으로 한다**(G14가 막는다).
5. 시즌 집계는 45분+·hit_points 15+만 쓰되, 경기 리포트는 짧은 교체 포함 **출전자 전원**을 기록한다.
   match 전용 fit/전술은 시즌 `prescriptions`/`team_tactic_setups`에 **자동 병합하지 않는다**.
6. ⚠️ **스케줄 세션이 돈 뒤에는 `git log`와 `git status`를 함께 본다**(커밋만 하고 푸시 안 한 사례, obs#382). 또 **다른 세션의 미커밋 DB
   변경이 보이면 `db/tactics.db`를 내 커밋에서 빼라** — 그쪽이 export·dump를 안 돌렸다면 dump·site/data가 어긋난다.
7. **파괴적 정리 전에는 `python3 scripts/db_diff.py --snapshot`** — 「새로 NULL 된 행 0」을 증명하는 유일한 수단이다(09-01 실증).
8. HANDOFF는 300줄 이하로 유지한다. 완료된 항목·해소된 미해결은 **지운다**(기록은 커밋과 obs에 남는다).

## 핵심 방법론

- 그리드 인코딩·집계·커널은 `core/`만 쓴다(재구현 금지). 좌표: x는 공격 방향, y가 낮을수록 오른쪽 —
  `cells_from_points` → `encode` → `Kernel.best_fit_slot`. **역할군 argmax 전에 슬롯 유형 필터 필수.**
  적합값 Δ 0.02~0.05는 EA 공개 노이즈 구간이라 그 차이만으로 인선을 바꾸지 않는다.
- 히트맵은 요구 역할의 일부만 설명한다. duties·1차 발언·전술 영상이 명확하면 낮은 fit보다 우선할 수 있다. ⭐ 단 **경기 프리셋의 역할 코드는
  그 경기의 위치 실측을 따른다**(09-03 잭슨) — 서사가 뒤집은 것이 **온볼 기능**이면 PlayStyle 층(docs/22)이고, 커널 Δ가 노이즈(≤0.05) 밖이면
  서사로 역할을 덮지 않는다.
  ⭐ **풀백 전진은 같은 쪽 와이드 역할이 결정한다**(docs/20 ⑨) — 윙어 뒤 풀백은 wingback/B, 전진은 C6 해방 사이드에서만.
  ⭐ **10번 포켓 충돌은 CAM 유형의 함수**(obs#464) — halfwinger 옆엔 insidefwd가 보완(.329), playmaker/classic10 옆엔 wideplm/widemid.
  사이드 스위칭 포커스는 `cam_halfwinger`/Roaming 하나. **와이드는 10번 유형을 먼저 정한 뒤 고른다.**
- 단일 경기·퇴장·저점유 같은 교란은 confidence와 보고서에 함께 쓴다.
- ⭐ **불변규칙 7(팀 축 혼선)은 세 번 터졌다** — 런북 슬롯 x 표 · 음바예 regime_id 오배치(obs#355) · **`team_code` 739행**(obs#372·373).
  **타 팀 실측은 출처 팀·체제를 반드시 명기.**
- ⭐ **불변규칙 10 최고 실증**(09-01): 아하노르 거래 구조는 **이탈리아어에만**, 무드리크 매수옵션은 **우크라이나어에만**, 응게상 선행조건은
  **프랑스어에만** 있었다 — 영어권만 봤으면 **거래 형태를 오독**했을 건이다.
- ⭐⭐ **불변규칙 10의 운영 형식**(obs#441·442) — 「다국어를 했다」는 자평은 믿지 않는다.
  ⑴ **선발 11명의 국적·경유 리그를 체크리스트로** 만들어 언어축을 강제한다(화제성만 따라가면 감독 모국어와 최대 화제 선수 축만 훑는다).
  ⑵ **언어축별로 기대 산출물이 다르다** — 감독 모국어·화제 선수 축은 「경기 분석」, 나머지 국적 축은 **「이적 서사·배경」**이 수확이다.
  ⑶ **「0건」은 구조적 사실일 수 있다** — ⛔ **그러나 당일 「0건」은 네 번 반전됐다**(D+1 유튜브 · D+2·D+3 전술 유튜브 · 헐전 Coaches' Voice).
  ⇒ **경로·검색어를 바꾼 재확인 전에는 종결로 적지 않는다.** ⭐ 유튜브는 **사이트 내부 검색**으로 확인한다(obs#516).
  ⑷ ⭐ **언어권이 저밀도라는 것도 결과다** ⇒ 다음 라운드에서 **우선순위를 내리고 사유를 남긴다**.
  ⛔ **단 「결장자 축」은 내리지 않는다** — 고레츠카는 D+2 당일 결장 확정 발표가 나왔다(09-08 실증).

## 참고 문서

- `docs/20`: 슬롯 x·역할·포커스·게임 구현 규칙(**⑧ movement_kr · ⑨ 윙 혼잡 · 팀 설정 매핑 규칙**) · `docs/30`: 수집·좌표·표본·결손(**⑧ xG 제공사 · 국면 그리드**) ·
  `docs/40`: DB/export/dump/git · `docs/50`: 인게임 경량 검증(캡처·전술 코드) · `docs/60`: 새 축 검증·통계 기준 · `docs/22`: PlayStyles·스탯(온더볼) ·
  `docs/21`: FC27 온보딩·트리거.
