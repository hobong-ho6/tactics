# HANDOFF

## 프로젝트

- 실제 감독 전술을 실측으로 분해해 FC26 전술로 재현한다.
- 대상: Aston Villa/Unai Emery(주), Chelsea/Xabi Alonso, Liverpool/Andoni Iraola, Atlético/Diego Simeone.
- 저장소: `/Users/ad03230205/Documents/tactics`, 브랜치 `main`.
- DB 정본: `db/tactics.db`. `db/dump/`와 `site/data/`는 파생물이다.
- 규약 정본: `CLAUDE.md`, `docs/00-overview.md`, 세부 문서는 `docs/`.
- 정기 작업 런북: `.claude/skills/transfer-watch/SKILL.md`, `.claude/skills/match-watch/SKILL.md`, `.claude/skills/player-collect/SKILL.md`.

## 현재 상태

> 마지막 갱신: **2026-08-25 08시 KST** · 작업 PC `AD03230205ui-iMac.local` · 브랜치 `main` ·
> 시작 기준 커밋 `9d0295e`(origin/main과 일치). 이번 match-watch 커밋은 아래 완료 후 기록한다.

- DB: players 190 · player_matches **4,074** · team_match_stats **61** · match_reports **25** ·
  match_player_reports **457** · squad_entries 125 · prescriptions 394 ·
  match_game_setups **10** · match_player_prescriptions **164** · transfer_targets 37 ·
  player_duties **190** · observations **325**(최신 obs#325).
- 회귀: **G1~G12 전항 통과**. G2 **3,007** 그리드 불일치 0, G6 고아 FK 0,
  G7 appearances 앵커 `(14,6,4,93)`, G12 경기 리포트 결손 0.
- ⭐ **적합값 드리프트: 차이 20 → 8, 일치 88 → 100**(obs#316). 아래 「종결된 항목」 참조.
- ⛔ **curl·WebFetch로 FotMob API를 치지 말 것** — 페이지 컨텍스트 밖에서 막힌다(404/셸).
  **Playwright로 페이지를 연 뒤 `page.evaluate` 안에서 fetch**하면 200이다. 이번 세션에서
  `matchDetails`(교체 이벤트)·`teams` 일정을 이 방식으로 받았다.

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

## 종결된 항목 (2026-08-24 세션)

- ✅ **드리프트 6건 판정 완료(obs#316) — 실제 오류는 0건이었다.** 원인은 데이터가 아니라 대조 도구다.
  `check_fit_drift.py`가 ⑴ `pos_only`를 무시하고 ⑵ 포메이션을 섞어 argmax를 잡고 있었다.
  라크루아(CCB 고정)·로저스(LW 고정, 우측은 duties가 **금지**)는 사이드 오탐,
  에수구는 3-4-2-1 RCM(x=55) ↔ 3-4-3 RCM(x=60) **앵커 혼입**(불변규칙 7 위반 비교),
  니콜자줄리는 사이드 고정이 미기록이라 오탐 → `pos_only='RAM'` 기록으로 해소.
  보가르드 +.022·부엔디아 +.014·맥긴 +.007은 노이즈 구간이거나 문서화된 역할 선택.
  **스크립트를 고쳤다** — 차이 20 → 8, 일치 88 → 100.
- ✅ **NULL fit 13행의 정체 확정 = 최초 시드 행의 누락**(판단에 의한 NULL이 아니다).
  전부 `squad_entries.id ≤ 17` · 날짜 스탬프 없는 `appearances measured`/`OWNED`이고,
  2026-07-21에 추가된 **2차 슬롯** 행만 값을 갖고 있었다(맥긴: 주 포지션 WM은 NULL, 2차 DM·CAM은 값 있음).
  **8행 백필 · 4행 보류 · 1행 대상 외.**
- ✅ **AVL/LIV D+2 조기 실시(obs#317)** — LIV 63분 교체 상대 확정(맥알리스터 ← 비르츠),
  스웨덴어 개척, 2025년 동일 카드 기사 혼입 차단, AVL 고메스 정지 대상 경기 일정 검증.

## 다음 할 일

1. ⭐ **CHE 풀럼전 D+2(08-26)·D+3(08-27)** — 알론소 공식 전체 회견, 클럽 전술 영상,
   Palmer/Rogers/João Pedro 선수별 분석, 지연 전술 블로그를 재검색한다. 0건도 리포트에 기록한다.
2. **AVL Brighton전은 비정기 재시도 조건부 draft** — 공식 전체 회견/클럽 전술 영상,
   경기 전용 전문 분석 또는 팟캐스트 공식 전사가 나오면 다시 연다. 정기 D+1~D+3은 완료.
3. **PL 다음 라운드**: AVL/LIV/CHE 실제 경기마다 동일 파이프라인을 반복한다.
   가장 가까운 CHE 08-30 Brighton 홈에 앞서 08-27 Luton EFL컵도 match-watch 범위 여부를 확인한다.
4. Atlético 이후 경기는 별도 match-watch 일정. 그리말도 실측이 채워지면 2경기 슬롯 기하·fit·sort_order 연쇄 재검증.
5. **왓킨스 이적 정황을 계속 추적한다** — 개막전 20인 제외가 부상이 아니고 에메리가 사유 답변을 3회 거부했다.
   이적 확정 시 `squad_entries` ST 행(fit 0.722)과 9번 처방 전체가 재판정 대상이다.
6. Minteh는 2026-09-02에 개선 오퍼 0건이면 등급 재판정한다.

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
