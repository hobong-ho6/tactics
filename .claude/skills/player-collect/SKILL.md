---
name: player-collect
description: 한 선수의 모든 데이터 축을 빠짐없이 수집한다 — 실측·게임스탯·상세지표·서사·판정까지 14축 체크리스트. 사용자가 "<선수> 데이터 수집", "<선수> 자료 수집해줘", "<선수> 전부 수집", "선수 데이터 업데이트", "<선수> 분석 자료 모아줘"라고 할 때 반드시 사용한다. 영입 후보·신규 영입·기존 스쿼드 누구에게나 적용한다. 특정 축 하나만 요청받아도 이 목록으로 결손을 먼저 점검한 뒤 시작한다.
---

# 선수 데이터 전수 수집

작업 디렉터리는 저장소 루트. 규칙은 CLAUDE.md·docs/00. **DB `db/tactics.db`가 정본.**

## 0. 원칙 4개

1. **결손과 0은 다르다**(obs#132). 소스가 값을 주지 않으면 **NULL**로 둔다. 0으로 채우면 집계가 조용히 망가진다.
2. **팀 축을 섞지 마라**(불변규칙 7). 영입 후보의 지표는 **원소속 팀 시스템의 값**이다.
   `regime_id`가 필요한 테이블(`player_duties`·`player_evaluations`)에 **우리 팀 체제로 넣지 말 것** —
   아직 우리 선수가 아니면 `regime_id=NULL` 또는 미등재.
3. **추가만, 재작성 금지**(불변규칙 2). 기존 행은 **비어 있는 칸만** 채운다.
4. **수집 못 한 축은 리포트에 "미수집 + 사유"를 남긴다.** 조용히 빠뜨리면 다음 세션이 있는 줄 안다.

## 1. 먼저 결손을 센다 (웹으로 나가기 전)

```bash
sqlite3 db/tactics.db "SELECT id,name,name_kr,sofascore_id,fotmob_id,sofifa_id FROM players WHERE name LIKE '%<이름>%'"
```
`player_id`를 확보한 뒤 아래를 돌려 **어느 축이 비었는지** 먼저 표로 만든다.

```bash
PID=<player_id>
for t in player_game_stats player_matches fotmob_detail_stats fotmob_season_stats fotmob_traits \
         player_duties player_tenures player_evaluations prescriptions squad_entries \
         transfer_targets transfer_outgoing player_shot_profile fbref_percentiles match_player_reports; do
  printf '%-28s %s\n' "$t" "$(sqlite3 db/tactics.db "SELECT COUNT(*) FROM $t WHERE player_id=$PID")"
done
```

⭐ **이 표가 이번 수집의 작업 목록이다.** 0인 축을 채우는 것이 과제다.

⛔⭐ **선수를 특정할 때는 이름과 함께 소속팀·국적·포지션 3요소를 반드시 대조한다**(docs/30 「선수 동일성 확인 규약」이 정본).
이름 표기는 소스마다 다르고(`Miloš Kerkez` ↔ `Milos Kerkez`), 동명이인은 국적까지 같을 수 있다
(`Alysson` 빌라·브라질·**RM** ↔ `Alisson Becker` 리버풀·브라질·**GK**). **`name_kr`이 충돌하면 행이 조용히 사라진다.**

⚠️ **이 카운트는 두 가지를 놓친다**(obs#234 실증 — 이 함정에 실제로 빠졌다):
1. **`player_id`가 NULL인 외부 후보 행**. `player_game_stats`·`transfer_targets`는 우리 선수가 아닌 사람도
   담으므로 `WHERE player_id=<id>`가 0을 보고할 수 있다. **`sofifa_id`·이름으로도 함께 세라**:
   `sqlite3 db/tactics.db "SELECT id,roster_date,player_id,playstyles FROM player_game_stats WHERE sofifa_id=<sofifa_id>"`
   찾으면 그 행에 `player_id`를 링크해 구멍을 닫는다.
2. **카운트가 1 이상이어도 그 행의 빈 칸**. '축이 있다'와 '축이 채워졌다'는 다르다 —
   0이 아닌 축도 **행을 열어 어느 컬럼이 비었는지 봐라**. obs#234는 이걸 안 해서
   이미 DB에 있던 PlayStyles를 "근거 0건"이라고 적었다.

## 2. 14축 체크리스트

| # | 축 | 테이블 | 소스·경로 | 필수? |
|---|---|---|---|---|
| 1 | **선수 기본** | `players` | 이름·`name_kr`·생년·주포지션 + **id 3종**(`sofascore_id`·`fotmob_id`·`sofifa_id`) | ✅ |
| 2 | **경기별 실측** | `player_matches` | SofaScore `core.sofascore.js_collect` → `parse_collected` | ✅ |
| 3 | **대표 그리드·적합** | `transfer_targets` / `prescriptions` | `core.aggregate` → `core.kernel.best_fit_slot` | ✅ |
| 4 | **FC 게임스탯** | `player_game_stats` | sofifa | ✅ |
| 5 | **상세 지표·백분위** | `fotmob_detail_stats` | FotMob `playerStats` | ✅ |
| 6 | **시즌 요약** | `fotmob_season_stats` | FotMob `playerData` | ✅ |
| 7 | **포지션군 백분위** | `fotmob_traits` | FotMob `playerData.traits` | ✅ |
| 8 | **커리어 이력** | `player_tenures` | FotMob `playerData.careerHistory` | ✅ |
| 9 | **서사·듀티** | `player_duties` | 영상·전술블로그·기사·1차발언 4종 | ✅ |
| 10 | **종합 평가** | `player_evaluations` | 위 전부의 종합 + 3감독 전술핏 | 스쿼드만 |
| 11 | **슛 프로파일** | `player_shot_profile` | SofaScore 슛맵 | 공격수 |
| 12 | **FBref 백분위** | `fbref_percentiles` | FBref | ⛔ 차단 중 |
| 13 | **경기별 리포트** | `match_player_reports` | match-watch 스킬 | 출전 시 |
| 14 | **판정 기록** | `observations` | 새 사실·충돌·정정 | ✅ |

### 축별 수집 경로 상세

**① id 3종** — 없으면 나머지가 전부 막힌다. 가장 먼저 확보한다.
- SofaScore: `/api/v1/search/all?q=<name>` → `results[].entity.id`
- FotMob: 팀 스쿼드에서 — `/api/data/teams?id=<fotmob_team_id>` → `squad[].members[]`
  (팀 id는 리그 테이블에서: `/api/data/leagues?id=<league>&season=<YYYY%2FYYYY>`)
  ⚠️ FotMob **검색 API는 404**다(2026-08-16). 팀 경유로 찾을 것.
- sofifa: `https://sofifa.com/players?keyword=<name>` → 결과 행의 `/player/<id>/` 링크

**② 경기별 실측** — `core/` 모듈만 쓴다. 세션 내 재구현 금지.
브라우저를 `https://www.sofascore.com/robots.txt` 오리진에 띄우고 `js_collect` 스니펫 실행.
⚠️ 홈페이지에서 돌리면 렌더러가 얼어 CDP 타임아웃(레이트리밋 아님).

**④ FC 게임스탯 (sofifa)**
⭐ **선수 상세 페이지는 로그인 세션이면 열린다**(2026-08-17 실증, obs#234) — `https://sofifa.com/player/<id>/`.
로그인 상태면 **playstyles·특산품(traits)·역할 숙련·AcceleRATE·체형**이 전부 나온다(비로그인은 로그인 페이지로
리다이렉트 · WebFetch는 403). ⚠️ **상세 페이지 제목의 로스터 날짜를 기존 행의 `roster_date`와 대조**하고,
같을 때만 그 행의 빈 칸을 채운다. 로그인이 없을 때는 **검색 페이지 컬럼 스크레이프**를 쓴다:
`https://sofifa.com/players?keyword=<name>&showCol%5B%5D=<코드>&…`
확인된 코드: `ae`나이 `oa`OVR `pt`POT `bp`베스트포지션 `hi`키 `pf`주발 `vl`가치 `wg`주급 `tt`총합
`ir`국제인지도 · 능력치 `cr fi he vo cu fk sh lo bl ac sp ag ba so ju st sr ln aa in po pe ma sa sl vi cm re dp`
· GK `gd gh gc gp gr`
⭐⭐ **[2026-08-19 정정] 6대 스탯(PAC/SHO/PAS/DRI/DEF/PHY)은 검색 페이지에서 그대로 받아진다** —
`showCol[]=pac,sho,pas,dri,def,phy`. 종전의 「스크레이프되지 않는다」는 틀렸다.
마르티네스 83/81/82/85/56/85가 기존 행과 일치해 재현 검증됐다 ⇒ **GK 원능력치 매핑 규칙은 불필요**하다
(과거 규칙 `DEF칸 = SPD = (가속+질주)/2`도 옳았음이 함께 확인됐다).
⭐ **팀 단위 수집**: `?tm[]=<팀id>` (AVL 2 · CHE 5 · LIV 9). ⚠️ 여러 팀을 묶으면 **60행에서 잘린다** — 팀별로 받을 것.
국적·풀네임·sofifa_id는 행 DOM에서: `img.flag[title]` · `a[data-tippy-content]` · `href=/player/<id>/`.
⛔ **프리킥 정확도·공격성은 컬럼 코드가 없다**(`fk`·`aa` 무시됨) — 상세 페이지 전용.
⚠️ **playstyles·traits·role_familiarity·AcceleRATE·body_type은 상세 페이지 전용**이다 —
검색 컬럼으로는 안 나오니 **로그인 후 상세로 가라**(위 참조). ⛔ traits 공란은 결손이 아니라 '없음'일 수 있다 —
상세의 **특산품 블록이 존재하고 비어 있으면 실측 0**이다(obs#132의 결손/0 구분).
⚠️ sofifa 나이 필드가 **1년 뒤처질 수 있다**(스즈키 실제 23세 ↔ 표기 22세). 나이 판단에 그대로 쓰지 말 것.

**⑤ 상세 지표 (FotMob = Opta 원자료)** — ⭐ 이 프로젝트에서 **가장 수확이 큰 경로**다.
1. `/api/data/playerData?id=<fotmob_id>` → `statSeasons[]`에서 **`entryId`** 를 얻는다(예: `1-0`).
2. `/api/data/playerStats?playerId=<id>&seasonId=<entryId>` → 지표·백분위.
   ⚠️ `seasonId`에 `2025/2026-55` 같은 형식을 넣으면 **null**이 온다. **반드시 `entryId`**를 쓸 것.
3. `localizedTitleId`가 우리 `metric_key`와 **1:1로 일치**한다. 그대로 쓴다.
4. ⭐ **여러 시즌·여러 클럽을 전부 받아라** — 같은 선수의 팀별 대비가 obs#223의 근거였다.
5. ⭐ **`keeperShotmap`/`shotmap`에 `situation`·`shotType`·`expectedGoalsOnTarget`이 있다** →
   **세트피스 vs 오픈플레이 분리 방어 지표**를 직접 계산할 수 있다(FBref 없이).
   ⚠️ 이렇게 계산한 PSxG−실점 합계는 공표된 `goals_prevented`와 **정확히 일치하지 않는다**(모델 차이).
   **상황 간 상대 비교에만 쓰고 절대값을 공표값처럼 인용하지 말 것.**

**⑨ 서사·듀티 (= 영상 분석·기사·스카우팅 리포트)** — docs/30 「영상·서사 소스 절차」.
⭐ **실측이 담는 것은 요구역할의 36%뿐이다**(obs#121). 관계·타이밍·온더볼은 여기서만 온다.
**4종을 전부 시도**하고 빠뜨린 것은 **"미수행 + 사유"** 를 적는다:

| 종류 | 무엇을 찾나 | 기록 필수 항목 |
|---|---|---|
| **유튜브 전술 분석** | 역할·움직임 해설 영상 | 채널·제목·**게시일**·URL + **직접 시청/자막/요약 중 무엇인지** |
| **전술 블로그** | 스카우팅 리포트 | TFA · Breaking The Lines · Spielverlagerung · Coaches' Voice · **현지 분석가 협회**(예: 이탈리아 `assoanalisti.it`) |
| **기사** | 클럽 전담 기자 | 매체·기자명·발행일 |
| **1차 발언** | 본인·감독·GK코치·**동료** | ⭐ 가장 세다. 전언(경유 보도)과 원인터뷰를 구분할 것 |

- **서브에이전트에 위임한다**(브라우저 금지·읽기 전용·DB 선조회 먼저·이미 아는 것 반복 금지).
- ⚠️ **체제 검증 필수** — 선수가 거쳐온 **클럽 × 감독**을 먼저 나열하고 각 자료가 어느 체제인지 명기하게 한다.
  실증: 스즈키는 3체제로 갈렸다(신트트라위던 / 파르마 페키아·키부 / 파르마 쿠에스타) — 섞으면 결론이 무효다.
- ⭐ **영어 검색만으로 끝내면 절반을 놓친다.** **모국어 + 현 리그 언어**로 각도를 바꿔라.
  실증: 스즈키 통솔 근거는 **일본어 기사(Sportiva)** 에서만 나왔고, 스위퍼 기각 근거는 **이탈리아어(AIAPC)** 에서만 나왔다.
- ⚠️ **"근거 0건"도 유효한 결과다.** 못 찾았으면 못 찾았다고 쓰고 **어떤 검색을 시도했는지** 남긴다 —
  다음 회차가 같은 검색을 반복하지 않는다.
- ⛔ **콘텐츠팜 블록리스트**(출처 없이 그럴듯한 문장을 생산 — 근거로 쓰지 말 것):
  `footballkit.lazada.com.ph` · `milan-kakanista22.com` · `syumatsusekai-football.com` ·
  `soccer-players-db.com` · `samurai-football.com` · `note.com` 개인 블로그 · 나무위키
- ⛔ **접근 차단 도메인**(2026-08-16 확인, 재시도 전 참고): FBref(403→CAPTCHA) · thisisanfield(403) ·
  liverpool.com(402 페이월) · forzaparma.it · ultimouomo.com · parmatoday.it · sofifa 상세(로그인) ·
  nikkei.com(회원) · The Athletic(페이월)
- `player_duties`는 **G10이 검사한다**: `source`(URL/obs#/리포트 경로 포함)·`sample_scope`·`sample_note` **필수**.
  ⚠️ 우리 선수가 아니면 `regime_id=NULL`.

## 3. 교차검증 — 수집으로 끝내지 않는다

⭐ **실측과 서사가 어긋나면 그 자체가 결과다.** 충돌을 지우지 말고 기록한다(불변규칙 3).
- 서사가 위치를 주장하면 **실측이 이긴다.**
- 단 **같은 것을 재고 있는지 먼저 확인하라** — obs#223의 교훈: 평균 위치(깊이)와
  Opta `Acted as sweeper`(빈도)는 **다른 것을 재는 지표**라 어긋나도 모순이 아니다.
- 지표가 팀 시스템의 함수일 수 있다 — 같은 선수의 **다른 클럽 시즌**이 최고의 통제군이다.

## 4. 완료 기준

- §1 결손 표의 0이 **채워졌거나, 사유가 적혔다.**
- 새 사실은 `source`·`confidence`를 채워 기록했다. **결손은 NULL.**
- 판정·충돌·정정은 `observations`에 남겼다.
- `python3 scripts/gates.py` 통과 → `python3 scripts/export.py` → `scripts/db_dump.sh`
- 명시 스테이징 커밋(⛔ `git add -A` 금지):
  ```
  git add db/tactics.db db/dump/ site/data/ reports/
  git commit -m "data(<선수>): <수집 축 요약>"
  git push
  ```
- 종료 보고: **축별 수집/미수집 표** + 새 obs 번호 + 미수집 사유.
