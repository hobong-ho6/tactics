# FC27 온보딩 체크리스트 (발매 예정 2026-09)

원칙: **버전 추가 = 행 추가** (game_versions에 FC27 행은 이미 있음). 발매일 실행 순서:

1. **Day-1 스냅샷**: EA 피치노트 원문 수집 → `game_system_changes`에 area별 기입
   (FIFA→FC26 소급 요약도 이때 함께). sofifa day-1 로스터 → `player_game_stats`
   (game_version='FC27', roster_date 명기 — 이력 보존이 v2 설계 의도).
2. **역할·커널 수집**: fut.gg `/api/fut/roles/` (키는 id, slug 아님 — obs#92 함정)
   → `game_roles`/`game_role_focus`/`game_role_variants` FC27 행. 좌표 변환은 docs/20 규약.
3. **게이트 확장**: `core/kernel.py`의 EXPECTED에 FC27 정합값 추가, gates.py 앵커는
   FC27 커널로 재산출한 값을 **새 행으로** 기록(FC26 앵커는 유지 — 버전별 병존).
4. **익스포트**: `scripts/export.py`가 kernels/FC27.json을 자동 생성(행만 있으면 됨).
   site/ 페이지는 버전 선택 UI 추가 전까지 FC26 고정 — 필요 시 data.js에 파라미터 추가.
5. **변화 관찰 로그**: FC26 대비 역할 수·커널 diff를 obs로 1건 기록.
