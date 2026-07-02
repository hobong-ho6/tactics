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

## 백로그 (알려진 정리 과제)

- [ ] `matches.competition` 표기 정규화 (14가지 혼재 → 표준 명칭)
- [ ] match 35의 result `W 4-0` → `4-0` 정규화
- [x] `(실측)` 프리셋 역이관 — player_role_map kind='measured' 16행, API 정밀 그리드로 교체 (2026-07-02)
- [ ] `(역할)` 프리셋 재도출 — 기존 sim 값은 구(근사) 그리드 기준. 툴의 실측 검증 모드에서
      역할별 유사도를 보고 재선정한 뒤 kind='role'로 기록
- [ ] 툴의 MAPS 커널·프리셋을 DB/JSON 로딩으로 전환 (DESIGN.md 로드맵)
- [ ] 팀 전술 설정(빌드업/수비라인) 모델링 — `game_tactics` 테이블 설계
- [x] 부엔디아 좌측 편향 → player_duties에 반영: 자유 10번은 "좌편향 프리롤"로 해석,
      우측 매핑 금지 (2026-07-02)
- [ ] 카마라 깊이 재검토 — 좌우 문제는 26경기 평균위치로 해결(우측-중앙, RDM으로 교정 완료);
      깊이(dm_holding vs dm_dlp)는 어려운 경기 히트맵 1–2개 추가 수집 후 확정
- [x] 가변 포지션 5명 player_duties 작성 — 포지션별 행 분리, player_match_positions
      전수 수집(226행) + v_position_profile 집계 기반 (2026-07-02)
