# 파이프라인 & DB·git 운영

## 시즌 파이프라인 (시즌/버전마다 반복)

```
1. research  — 경기·평점·히트맵 수집 (docs/30-data-rules.md 절차)
2. ingest    — matches/appearances/streaks 적재      → 검증: 행 수·중복·규약 준수
3. analyze   — 포지션별 평점×결과 집계, 3층위 분석    → 검증: rationale에 수치 근거
4. map       — player_role_map 작성 (kind별)          → 검증: 11명 완전한 XI 쿼리 가능
5. export    — 프리셋 JSON 생성 → data/exports/       → 검증: 툴에서 로드·렌더 확인
6. commit    — db_dump.sh 실행 후 git 커밋
```

## DB 관리

- `data/avl_analysis.db` 원본을 git으로 관리한다 (수 MB 이하인 동안은 그대로 커밋).
- SQLite는 바이너리라 diff가 안 보이므로, **DB를 변경한 커밋에는 반드시
  `scripts/db_dump.sh`를 돌려 `data/dump/`(schema.sql + 테이블별 INSERT 덤프)를
  함께 갱신**한다. 리뷰·이력 추적은 dump의 텍스트 diff로 한다.
- 복구: git 히스토리의 .db를 체크아웃하거나, dump로 재구성
  (`cat data/dump/schema.sql data/dump/*.sql | sqlite3 new.db` 순서 주의).
- 스키마 변경은 additive만 (컬럼·테이블 추가). 파괴적 변경이 불가피하면
  변경 전 커밋을 만들어 두고 DESIGN.md에 마이그레이션 내역을 적는다.

## git 규칙

- 커밋은 성격별로 분리: `data:`(DB+dump), `tool:`(fc26-heatmap.html), `docs:`(문서).
- 프리셋 JSON export는 `data/exports/`에 두고 커밋한다.
- `.DS_Store` 등 OS 파일은 .gitignore.
- 원격(remote)이 아직 없음 — GitHub private repo에 push해 백업하는 것을 권장 (백로그).

## 정기 자동화

- **transfer-watch** (매일 09:00/21:00, 로컬 스케줄러 `villa-transfer-watch`):
  TransferFeed 빌라 페이지 스캔 → 1~2티어 기자 크로스체크 → MEDIUM 이상 신규 루머만
  실측 분석 후 `transfer_targets`에 추가(`short_label` 컬럼 필수 — 툴 표시용 한글/영문
  짧은 이름). 절차 정의는
  [.claude/skills/transfer-watch/SKILL.md](../.claude/skills/transfer-watch/SKILL.md).
  Chrome 미연결 실행은 `PENDING MEASUREMENT`로 표시 — 다음 대화 세션에서 측정 보완.
  앱이 꺼져 있으면 다음 실행 시점으로 밀린다.
  이적료가 확정·변경되는 건은 **`transfer_ledger` 테이블(가계부: in/deduct/out/pending)도
  함께 갱신** — 이적 탭 상단 예산 가계부가 여기서 파생된다.
  **DB 갱신 후 반드시 `python3 scripts/sync_transfer_ui.py` 실행** — fc26-heatmap.html의
  `TRANSFER_TARGETS`/`TRANSFER_OUTGOING`/`TRANSFER_LEDGER`/`XI_OWNED` 미러 배열을 DB로 재생성한다.
  - 영입 후보 옵션(SQUAD_SLOTS/PLAYER_BEST/CMP_SLOTS/XI_POOL)은 `injectTransferCandidates()`가
    미러에서 런타임 파생 (2026-07-14 리팩터).
  - **베스트 11(XI_POOL)** = 보유 선수(`squad_positions` DB → XI_OWNED) + 확정 영입만
    (`transfer_targets.likelihood='CONFIRMED'`). 루머 후보(MEDIUM-HIGH·HIGH)는 Best 11에서 제외
    — 이적 탭·선수 비교·빌라 스쿼드에만 노출 (2026-07-21).
  - **보유 선수의 뛸 수 있는 포지션**은 `squad_positions` 테이블이 단일 소스 — 다포지션 선수는
    (label, slot_type)로 여러 행(예: 맥긴 WM+DM, 부엔디아 WM+CAM, 보가르드 DM+FB). 새 포지션
    실측이 생기면 이 테이블에 행 추가 후 sync — XI_POOL이 자동 갱신된다.
  순서: DB 갱신 → `sync_transfer_ui.py` → `db_dump.sh` → 커밋.

## 백로그 (알려진 정리 과제)

- [x] `matches.competition` 표기 정규화 완료 (2026-07-02) — 표준 명칭 2종 + 신설 `stage` 컬럼으로
      스테이지/매치위크 분리 (MW5, R16 1st leg, Final 등)
- [x] result 접두 표기(`W 4-0` 등) 10건 → 홈-원정 원문 스코어로 정규화; venue 장식 제거,
      구단명 표기 통일 (AFC Bournemouth→Bournemouth 등) (2026-07-02)
- [x] `(실측)` 프리셋 역이관 — player_role_map kind='measured' 16행, API 정밀 그리드로 교체 (2026-07-02)
- [x] `(역할)` 프리셋 재도출 완료 (2026-07-02) — 표본 보강된 포지션-순수 그리드로 전 포지션
      스캔 후 kind='role' 11행 확정 + 툴 (역할) 프리셋 갱신 (평균 유사도 ~0.82).
      kind='role'은 "실측 움직임과 가장 닮은 역할"(기술적), kind='optimal'은 "게임에서 택할
      역할"(처방적)로 구분 유지 — 예: GK 실측 최근접은 gk_goalkeeper/Defend(0.96)지만
      빌드업 임무 때문에 optimal은 gk_sweeper 유지.
- [ ] 툴의 MAPS 커널·프리셋을 DB/JSON 로딩으로 전환 (DESIGN.md 로드맵)
- [ ] 팀 전술 설정(빌드업/수비라인) 모델링 — `game_tactics` 테이블 설계
- [x] matches 중복 정리 완료 (2026-07-02) — 리버풀 홈전 43(5/16)을 26(5/15, API 날짜)으로 병합,
      로저스 중복 행은 정밀본(그리드 보유)만 보존
- [ ] `@dom`/`@tight` 분리 그리드를 툴 변형 프리셋(지배/접전)으로 노출
- [x] 부엔디아 좌측 편향 → player_duties에 반영: 자유 10번은 "좌편향 프리롤"로 해석,
      우측 매핑 금지 (2026-07-02)
- [x] 카마라 깊이 재검토 완료 (2026-07-02) — 첼시 원정·리버풀 원정(2-0 패) 그리드를 추가한
      탈편향 표본에서도 dm_dlp/Roaming 0.83 > dm_holding 0.58: "딥 앵커" 프레임 기각.
      부가 발견: 피봇 좌우가 10월 중순(스퍼스 원정)을 기점으로 좌→우 전환, 이후 연승기 내내 우측.
      optimal의 dm_holding은 처방적 안전 선택으로 유지 → 숙련 타이브레이커로 최종 확정(2026-07-05, 검증 게이트 폐기)
- [x] 가변 포지션 5명 player_duties 작성 — 포지션별 행 분리, player_match_positions
      전수 수집(226행) + v_position_profile 집계 기반 (2026-07-02)
