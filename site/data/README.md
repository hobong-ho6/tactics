# site/data — DB 익스포트 (손편집 금지)

`python3 scripts/export.py`가 db/tactics.db에서 생성한다. 값은 DB 컬럼의 1:1 사상이며
게이트(scripts/gates.py) 통과가 생성의 선행 조건이다. DB 무변경이면 diff 0.

| 파일 | 내용 | 소스 테이블 |
|---|---|---|
| index.json | 팀·regime·게임버전 메타 | regimes, teams, game_versions |
| kernels/{GV}.json | 역할 37·포커스 85·위치변형 217·전술 파라미터 | game_roles, game_role_focus, game_role_variants, game_tactic_params |
| teams/{CODE}.json | slots(기하)·squad(XI)·prescriptions·setups·profile·transfer | slots, squad_entries, prescriptions, team_tactic_setups, manager_profiles, transfer_* |

팀 추가 = regimes 행 추가 후 재익스포트 → teams/{CODE}.json 생성.
게임 버전 추가 = game_versions 행 + 커널 수집 → kernels/{GV}.json 생성.
