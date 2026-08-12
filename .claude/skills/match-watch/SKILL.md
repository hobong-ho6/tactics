---
name: match-watch
description: 시즌 중 주간 경기 데이터 수집 — 3팀(AVL·CHE·LIV) 라운드별 선수 실측(히트맵·스탯·평균위치)과 팀 스탯을 v2 DB에 적재하고 집계·적합을 갱신. 매주 또는 경기 다음날 /match-watch로 실행. 슈퍼컵·컵대회 포함.
---

# 주간 경기 수집 파이프라인 (v2 · 3팀)

작업 디렉터리: `/Users/ad03230205/Documents/tactics`. DB `db/tactics.db`. 규칙: CLAUDE.md·docs/00.

## 0. 선행 게이트
`python3 scripts/gates.py` 통과 확인. 실패 시 수집 중단하고 원인부터.

## 1. 라운드 확인 (팀 루프: AVL → CHE → LIV)
- `SELECT code, sofascore_id FROM teams` (AVL 40 · CHE 38 · LIV 44).
- 브라우저를 sofascore.com/robots.txt 오리진에 띄우고 `/api/v1/team/<id>/events/last/0`으로
  직전 경기(들) event_id 확보. 이미 적재된 event는 건너뛴다:
  `SELECT DISTINCT event_id FROM player_matches WHERE event_id IN (...)`.

## 2. 선수 실측 수집
- 라인업 API로 45분+ 출전자 목록 → `core.sofascore.js_collect()` 스니펫으로 일괄 수집
  → `parse_collected()` → `player_matches` INSERT (source·confidence 필수).
- 신입 선수는 `players`에 승격(sofascore_id 컬럼) 후 적재.
- ⭐ **신규 선수는 영상·서사 분석 필수** (docs/30 「영상·서사 소스 절차」): 스카우트 리포트
  수집 → player_duties 가설 기록 → 실측 교차검증 → obs 판정. CHE/LIV 포함 전 팀 공통.
- **pos_class 분류 필수**: `core.classify.pos_class(avg_x, avg_y, lineup_pos)` —
  lineup_pos(G/D/M/F)만으로는 포지션-순수 집계가 안 된다 (2026-08-11 방법론 보강).
- **스코어 국면**: 같은 오리진에서 `/api/v1/event/<eid>/incidents`로 득점 시각을 받아
  stats_json에 `phase_lead/level/trail` 분(分)을 기록 — @lead/@trail 분리 집계의 원료.

## 2-1. ⭐ 서사 수집 — 매 회차 의무 (2026-08-12 신설, 사용자 지시)

**실측만 모으면 절반이다.** 히트맵·스탯이 담는 것은 요구역할의 **36%**뿐이고(obs#121),
관계·타이밍·온더볼은 영상·서사에서만 온다. 정본 규칙은 **docs/30 「정기 수집 규칙」**.

- **대상**: ⓐ 그 라운드 **45분+ 출전 선수 전원**(신규만이 아니다) ⓑ **감독 3인**.
- **소스 4종을 매 회차 확인**하고, 빠뜨린 종류는 리포트에 **"미수행 + 사유"** 를 적는다:
  **유튜브 전술 분석** · **전술 블로그**(TFA·BTL·Spielverlagerung·Coaches' Voice) ·
  **기사**(클럽 전담 기자) · **본인 발언**(기자회견·인터뷰 — 1차 자료라 가장 세다).
- **서브에이전트에 위임한다**(팀당 1개 병렬). 프롬프트에 반드시:
  ① 오늘 날짜 ② 읽기·검색 전용(DB 쓰기·git 금지) ③ **DB 선조회 먼저**(이미 아는 것 반복 금지)
  ④ **발행일·체제 검증**(에메리=비야레알/아스날 · 알론소=레버쿠젠 · 이라올라=본머스/라요 자료가
     대량으로 돈다 — 현 팀 결론처럼 쓰면 안 된다) ⑤ **조회하지 않은 것을 쓰지 마라**
     (근거 없는 'PlayStyles 트릭스터' 허위 기재 사고 전례) ⑥ 영상은 채널·제목·**게시일**·URL 필수이고
     내용을 직접 못 봤으면 **"설명·자막·요약 기사 기준"** 명기.
- **산출**: 선수 → `player_duties` · 감독 → `manager_profiles`(11축) · 판정/충돌 → `observations`.
  게임 설정 함의가 나오면 `team_tactic_setups`·처방에 반영(단 **커널 Δ 산출 전 처방 변경 금지**).
- ⚠️ **위치 주장은 실측이 이긴다.** 서사가 실측과 어긋나면 충돌을 기록하고 실측을 채택한다.

## 3. 팀 스탯
`/api/v1/event/<eid>/statistics` → `team_match_stats` + `matches` 행 추가.
CHE·LIV는 이것이 알론소·이라올라 **체제 첫 실측**이다 — 25/26 데이터와 섞지 말 것(규칙 7).

## 4. 집계·적합 갱신
- 표본이 2경기 이상 쌓인 선수는 `core.aggregate.player_aggregate`(포지션-순수)로
  `prescriptions` kind='measured'(26/27 시즌 행 — 25/26 행을 덮지 않는다, 추가만) 갱신.
- 적합은 `core.kernel.Kernel('FC26').best_fit_slot()`. 노이즈 구간(Δ≤.05)은 인선 변경 금지.

## 5. 완료 절차 (매 실행)
`python3 scripts/export.py` → `scripts/db_dump.sh` →
`git add db/tactics.db db/dump/ site/data/ && git commit -m "data(match-watch): <라운드 요약>" && git push`
종료 보고: 팀별 수집 경기 수 / 신규 선수 / 집계 갱신 행 / 게이트 상태.

## 특별 회차
- **2026-08-12 슈퍼컵(AVL)**: 시즌 첫 실측 — obs#134~136(우측 와이드 선발) 검증을 §2와 함께 수행,
  결과를 observations에 기록.
