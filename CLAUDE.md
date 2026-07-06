# Aston Villa → FC 전술 구현 프로젝트

실제 아스톤 빌라(에메리)의 전술을 데이터로 분석해서, FC26 및 이후 시리즈(FC27…)의
게임 내 전술(포메이션·역할·포커스)로 재현하는 프로젝트.

## 문서 맵 — 작업 전에 해당 문서를 먼저 읽을 것

| 작업 | 문서 |
|---|---|
| 시스템 전체 구조(레이어, 테이블 관계) | [data/DESIGN.md](data/DESIGN.md) |
| 실제 전술 분석 (에메리 철학, 포지션 요구, 선수 분석) | [docs/10-emery-tactics.md](docs/10-emery-tactics.md) |
| FC 게임 시스템 분석·매핑 (역할/포커스, 버전 관리, 툴) | [docs/20-fc-game-system.md](docs/20-fc-game-system.md) |
| 데이터 수집·기록 규칙 (스키마, 좌표 규약, 신뢰도, SofaScore 수집법) | [docs/30-data-rules.md](docs/30-data-rules.md) |
| 파이프라인, DB·git 운영 | [docs/40-pipeline.md](docs/40-pipeline.md) |
| 게임 내 검증 루프 (플레이 체크리스트, ingame_checks) | [docs/50-ingame-validation.md](docs/50-ingame-validation.md) |

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
6. 툴 프리셋 네이밍: `아스톤 빌라 <시즌> (<종류>)` — 예: `아스톤 빌라 25/26 (최적)`.

## 작업 완료 기준 (data 작업의 Definition of Done)

- 새 사실은 `appearances`(또는 해당 테이블)에 `source`(URL/API 엔드포인트)와
  `confidence`(등급+근거)를 채워서 기록했다.
- 파생 결론은 `player_role_map`에 `kind`와 `rationale`을 채워서 기록했다.
- `scripts/db_dump.sh`를 실행했고, .db + dump를 커밋했다.
