# 감독 전술 → FC 전술 구현 프로젝트

실제 감독의 전술을 데이터로 분석해서, FC26 및 이후 시리즈(FC27…)의
게임 내 전술(포메이션·역할·포커스)로 재현하는 프로젝트.

**대상 3팀 (2026-07-30 팀 축 도입)**: 에메리·아스톤 빌라(AVL, 기준 구현) /
알론소·첼시(CHE) / 이라올라·리버풀(LIV). DB 8개 테이블에 `team` 컬럼이 있고
`teams` 테이블이 코드를 관리한다 — 팀별 조회는 항상 `WHERE team='<코드>'`로 좁힐 것.

---
## 세션 핸드오프
- 세션 시작 시 반드시 HANDOFF.md를 먼저 읽고, 현재 상태와 다음 할 일을 한 줄로 브리핑한 뒤 작업을 시작할 것
- 세션 종료 전 또는 사용자가 "handoff"라고 하면 HANDOFF.md 내부 규칙에 따라 파일을 갱신할 것
---
## 문서 맵 — 작업 전에 해당 문서를 먼저 읽을 것

| 작업 | 문서 |
|---|---|
| 시스템 전체 구조(레이어, 테이블 관계) | [data/DESIGN.md](data/DESIGN.md) |
| **에메리·빌라** 전술 분석 (철학, 포지션 요구, 선수 분석) — 기준 구현 | [docs/10-emery-tactics.md](docs/10-emery-tactics.md) |
| **알론소·첼시** 전술 분석 (레버쿠젠 원형, 26/27 처방) | [docs/11-alonso-tactics.md](docs/11-alonso-tactics.md) |
| **이라올라·리버풀** 전술 분석 (본머스 실측, 3자 대조, **PPDA 정의·정본 표**) | [docs/12-iraola-tactics.md](docs/12-iraola-tactics.md) |
| FC 게임 시스템 분석·매핑 (역할/포커스, 버전 관리, 툴) | [docs/20-fc-game-system.md](docs/20-fc-game-system.md) |
| 데이터 수집·기록 규칙 (스키마, 좌표 규약, 신뢰도, SofaScore 수집법) | [docs/30-data-rules.md](docs/30-data-rules.md) |
| 파이프라인, DB·git 운영 | [docs/40-pipeline.md](docs/40-pipeline.md) |
| ~~게임 내 검증 루프~~ ⛔ 폐기 — 데이터가 최종 심판 (참고용 보존) | [docs/50-ingame-validation.md](docs/50-ingame-validation.md) |

> PPDA·압박 강도 수치를 인용할 때는 **docs/12의 「PPDA 정의 차이 표」와 정본 표(obs#80)**를
> 먼저 볼 것. 정의 기준표는 docs/12에만 두고 docs/11은 참조한다(중복 금지).

## 불변 규칙 (모든 세션 공통)

1. **`data/avl_analysis.db`가 single source of truth.** 분석 결과·매핑은 반드시 DB에 먼저
   기록하고, 툴(fc26-heatmap.html)의 하드코딩은 DB에서 파생된 것으로 취급한다.
2. **추가만, 재작성 금지.** 새 시즌 = `seasons`/`player_seasons`/`matches`… 행 추가.
   새 게임 버전 = `game_roles` 행 추가. 기존 시즌·버전 데이터를 덮어쓰지 않는다.
3. **실측 > 서사.** 뉴스 기사 서술과 SofaScore API 실측(평점·좌표)이 충돌하면 실측을
   채택하고, 충돌 사실 자체를 해당 행의 `confidence`에 기록한다.
   (사례: 부엔디아 — 기사 "오른쪽 드리프트" vs 실측 좌측 편향, appearances 75–77 참조)
4. **좌표 규약 준수.** SofaScore 히트맵 0–100: x는 공격 방향, **y 낮음=오른쪽 / y 높음=왼쪽**.
   상세와 검증 근거는 docs/30-data-rules.md.
5. **DB 변경 후에는 반드시 `scripts/db_dump.sh` 실행** → `data/dump/*.sql` 재생성 후
   .db와 dump를 함께 커밋한다 (바이너리 diff 불가 보완).
6. 툴 프리셋 네이밍: `<팀명> <시즌> (<종류>)` — 예: `아스톤 빌라 25/26 (최적)`,
   `첼시 26/27 (알론소)`. 팀명은 `TEAMS` 레지스트리(fc26-heatmap.html)의 `prefix` 값을 쓴다.
7. **팀 축을 섞지 말 것.** 한 팀의 실측을 다른 팀 처방의 근거로 쓸 때는 `rationale`에
   출처 팀·체제를 명기한다 (사례: 로저스 첼시 처방의 그리드는 빌라 25/26 에메리 체제 것).
   특히 **25/26 첼시·리버풀 팀 전술은 알론소·이라올라의 것이 아니다** — 개인 위치 성향의
   기준선으로만 쓰고, 팀 구조 주장의 근거로 쓰지 않는다.

## 작업 완료 기준 (data 작업의 Definition of Done)

- 새 사실은 `appearances`(또는 해당 테이블)에 `source`(URL/API 엔드포인트)와
  `confidence`(등급+근거)를 채워서 기록했다.
- 파생 결론은 `player_role_map`에 `kind`와 `rationale`을 채워서 기록했다.
- `scripts/db_dump.sh`를 실행했고, .db + dump를 커밋했다.
