# 실축 → FC 구현 플랫폼 (v2, 2026-08-11 재설계)

실제 감독·팀 페어의 전술을 데이터로 분석해 FC26·FC27+에 재현하는 프로젝트.
**대상**: 에메리·아스톤 빌라(AVL, 주) / 알론소·첼시(CHE) / 이라올라·리버풀(LIV).
시스템 설계·규약·진행 상태의 정본은 **[docs/00-overview.md](docs/00-overview.md)**.

## 세션 핸드오프
- 세션 시작 시 HANDOFF.md를 먼저 읽고 한 줄 브리핑 후 시작.
- 종료 전 또는 "handoff" 지시 시 HANDOFF.md 내부 규칙대로 갱신.

## 문서 맵

| 작업 | 문서 |
|---|---|
| 시스템 구조·게이트·규약·진행 상태 | [docs/00-overview.md](docs/00-overview.md) ⭐정본 |
| 감독 분석 (에메리/알론소/이라올라 — PPDA 정본은 12) | docs/10 · 11 · 12 |
| FC 게임 시스템 (v1 기준 — 게이트 표는 scripts/gates.py가 정본) | docs/20 |
| 데이터 수집 규칙 (좌표·함정 7종·SofaScore) | docs/30 |
| 새 분석 축 사전등록 양식 | docs/60 |
| v1 아카이브 (구 툴·구 DB — 읽기 전용) | archive/v1/ · data/ |

## 불변 규칙

1. **`db/tactics.db`가 single source of truth.** 페이지(site/)는 export 산출물만 소비한다 —
   손편집 지점 0. 구 v1 DB(data/avl_analysis.db)는 동결 아카이브(읽기 전용).
2. **추가만, 재작성 금지.** 새 시즌/버전/팀 = 행 추가. 기존 행을 덮어쓰지 않는다.
3. **실측 > 서사.** 기사와 실측이 충돌하면 실측 채택, 충돌 사실을 `confidence`에 기록.
4. **게이트 우선.** DB 쓰기 전 `python3 scripts/gates.py` 통과 필수 (export.py는 자동 강제).
   인코딩·집계·커널 로직은 `core/`만 쓴다 — 세션 내 재구현 금지.
5. **DB 변경 후 고정 절차**: `python3 scripts/export.py`(site/data 재생성 + 프리뷰 미러)
   → `scripts/db_dump.sh`(db/dump 재생성) → **.db + dump + site/data 함께 커밋**.
   ⚠️ `git add -A` 금지 — 커밋 금지 파일이 있어 푸시가 차단된다. 명시 스테이징만.
6. **조인 규칙**: 사람은 `player_id`, 팀은 `team_code`, 판단 테이블은 `regime_id`.
   라벨 문자열 조인 금지.
7. **팀 축을 섞지 말 것.** 타 팀 실측을 근거로 쓸 때 `rationale`에 출처 팀·체제 명기.
   25/26 첼시·리버풀 팀 전술은 알론소·이라올라 것이 아니다.
8. **히트맵은 시각화해서 보여준다.** 대화에서 5×5 그리드는 위젯으로(열0=좌측, 행0=공격 방향,
   X=1.0·숫자/10, 단일색 램프). 수치 결론은 본문에.
9. **좌표 규약**: SofaScore x=공격 방향, y 낮음=오른쪽. 툴x=100−소파y, 툴y=소파x (docs/30).
10. **⭐ 서사 수집은 다국어로 한다.** 선수·팀·감독 자료를 모을 때 영어로 끝내지 않는다 —
    **대상의 모국어 + 그가 거쳐온 리그의 언어**로 검색어를 새로 짜서 다시 훑는다.
    현지 전술 매체가 영어권 종합지보다 밀도가 높다. 규칙 정본은 docs/30 「다국어 검색 규칙」.
    실증(2026-08-16): 스즈키 결정적 근거 3건이 **전부 일본어·이탈리아어에서만** 나왔다.

## 작업 완료 기준 (data 작업의 DoD)

- 새 사실은 `player_matches`/해당 테이블에 `source`·`confidence`를 채워 기록했다.
- **서사 자료는 다국어로 훑었다**(불변규칙 10) — 쓰지 않은 언어권이 있으면 사유를 남겼다.
- 새 경기 수집은 `match_reports`·`match_player_reports`와 `reports/match-watch/` 원문까지 작성해
  출전 선수 전원·전술 변화·게임 구현 판단을 닫고, 경기 전용 `match_game_setups`와 선발 11명의
  `match_player_prescriptions`를 시즌 정본과 분리해 기록했다(G12).
- 파생 결론은 `prescriptions`(정형 필드: fit_sim/sample_n/avg_rating 컬럼)에 기록했다 —
  값을 rationale 산문에 묻지 않는다.
- 불변규칙 5의 고정 절차(export → dump → 커밋)를 실행했다.
