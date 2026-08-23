# HANDOFF

## 프로젝트

- 실제 감독 전술을 실측으로 분해해 FC26 전술로 재현한다.
- 대상: Aston Villa/Unai Emery(주), Chelsea/Xabi Alonso, Liverpool/Andoni Iraola, Atlético/Diego Simeone.
- 저장소: `/Users/ad03230205/Documents/tactics`, 브랜치 `main`.
- DB 정본: `db/tactics.db`. `db/dump/`와 `site/data/`는 파생물이다.
- 규약 정본: `CLAUDE.md`, `docs/00-overview.md`, 세부 문서는 `docs/`.
- 정기 작업 런북: `.claude/skills/transfer-watch/SKILL.md`, `.claude/skills/match-watch/SKILL.md`, `.claude/skills/player-collect/SKILL.md`.

## 현재 상태

> 마지막 갱신: **2026-08-24 09시 KST 전후** · 작업 PC `AD03230205ui-iMac.local` ·
> 시작 기준 HEAD/origin `11a407e` · 이번 작업은 AVL/LIV PL 개막전을 함께 커밋·푸시한다.

- DB: players 190 · player_matches **4,032** · team_match_stats **59** · match_reports **23** ·
  player_duties **176** · observations **309**(최신 obs#309).
- 회귀: **G1~G12 전항 통과**. G2 2,991 그리드 불일치 0, G6 고아 FK 0,
  G7 appearances 앵커 `(14,6,4,93)`, G12 경기 리포트 결손 0.
- SofaScore는 현재 403이나 WhoScored는 인앱 브라우저에서 열렸고, FotMob API도 200으로 회복됐다.
  이번 두 경기에서 FotMob(팀·선수 스탯/xG/물리량) + WhoScored/Opta(이벤트·좌표·PPDA)를 사용했다.

### 2026-08-23 PL Round 1 수집

| 팀 | 경기 | 핵심 실측 | 상태/리포트 |
|---|---|---|---|
| AVL | Brighton 4–0 Aston Villa | 점유 27%, xG 0.31–3.67, 슛 6–21, PPDA 24.69. João Gomes 40′ 퇴장 | `draft` · `reports/match-watch/2026-08-23-avl-brighton.md` |
| LIV | Newcastle 2–2 Liverpool | 점유 61%, xG 2.98–1.58, 슛 27–13, PPDA 5.95. Gakpo 55′, Szoboszlai 90+9′ PK | `draft` · `reports/match-watch/2026-08-23-liv-newcastle.md` |
| CHE | Fulham 원정 2026-08-25 04:00 KST | 아직 경기 전 | heartbeat id=3이 다음 완료 회차에 수집 |

두 보고서가 `draft`인 이유는 경기 종료 직후라 지연 전술 영상·전문 블로그가 아직 없기 때문이다.
매일 08:00 KST heartbeat id=3이 새 경기보다 먼저 D+1/D+2/D+3 보강 여부를 확인하도록 프롬프트를 갱신했다.
이번 두 경기의 후속일은 **08-25 / 08-26 / 08-27 08:00 KST**다. 0건이어도 보고서에 검색 범위를 기록한다.

### 이번 경기 판정

- AVL: 50분간 10명이어서 PPDA 24.69와 Deep/38은 감독 의도보다 경기 국면의 영향이 크다.
  Buendía ST는 공백을 메운 응급 배치이며 시즌 처방으로 병합하지 않는다.
- LIV: 61% 점유·27슛에도 오픈플레이 xG는 0.96, 막힌 슛은 16개다. 공격량과 박스 공략의 질을 분리한다.
- LIV 두 실점은 모두 공격 진영 소유권 상실 뒤 전환에서 발생했다. 이라올라 이식의 잔여수비 리스크는 유지한다.
- Víctor Muñoz는 교체 27분에 마지막 PK를 유도했다. Rio Ngumoha와 RM 선발 경쟁을 다시 연다.
- Ryan Gravenberch는 Gakpo 골을 도왔지만 두 실점 전 소유권 상실에도 관여했다. Roaming 피벗의 양면성 표본이다.

## 자동화

- Codex heartbeat **id=3 「프리미어리그 3팀 경기 수집」**, 매일 08:00 KST.
- 매 회차 순서: 기존 draft 리포트 D+1~D+3 점검 → 새 종료 경기 확인 → match-watch 전체 파이프라인.
- 새 경기/후속 근거가 없으면 저장소를 변경하지 않는다.
- 이적 감시는 cron `transfer-watch.sh`가 09:00/21:00 각 1행. macOS TCC/marker probe 검증 완료.

## 다음 할 일

1. **08-25 08:00**: AVL/LIV D+1 보강 + 종료된 Fulham–Chelsea가 있으면 전체 수집.
2. **08-26, 08-27 08:00**: AVL/LIV D+2/D+3. D+3 뒤 근거가 충분하면 `complete`, 아니면 결손을 유지한다.
3. **PL 다음 라운드**: AVL/LIV/CHE 실제 경기마다 동일 파이프라인을 반복한다.
4. Atlético R2 및 이후 경기는 별도 match-watch 일정에서 처리. 그리말도 실측이 채워지면 2경기 슬롯 기하·fit·sort_order 연쇄 재검증.
5. 적합값 드리프트 6건을 행별 판정: Esugo +.231, Nico Paz +.224, Rogers +.136,
   Lacroix +.057, Bogarde +.022, Buendía +.014. duty 제약이면 저장값을 유지하고 confidence에 명시한다.
6. 저장값 NULL인 AVL 주전 fit 13행의 의도를 확인한다.
7. Minteh는 2026-09-02에 개선 오퍼 0건이면 등급 재판정한다.

## 데이터 수집 상태와 결손

- 대량 수집: `collect_fotmob_players.py`, `collect_understat_shots.py`; `check_fit_drift.py`는 읽기 전용.
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
