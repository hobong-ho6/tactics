#!/bin/sh
# Regenerate diffable SQL dumps from db/tactics.db (v2).
# Run after ANY DB change, before committing (see docs/00-overview.md).
# v1 dumps (data/dump/)는 아카이브와 함께 동결 — 여기서는 건드리지 않는다.
# ⭐ 2026-10-12부터 git에는 .db가 아니라 이 dump가 실린다 — 다른 PC는 scripts/db_restore.sh로 DB를 만든다.
set -e
cd "$(dirname "$0")/.."
db=db/tactics.db
# ⛔ pull로 들어온 남의 dump를 옛 DB로 덮어 지우지 않게 먼저 막는다(db_stamp.sh 참조).
scripts/db_stamp.sh check
# ⭐ 형식은 scripts/db_dump_sql.py가 정한다 — sqlite3 CLI는 버전마다 출력이 달라 PC가 바뀔 때마다
#    내용이 같은 dump가 수만 줄 바뀌었다(2026-11-02 · 2회째 · 불변규칙 13). ⛔ 여기서 CLI로 다시 쓰지 않는다.
python3 scripts/db_dump_sql.py
scripts/db_stamp.sh sync
echo "dumped $(ls db/dump | wc -l | tr -d ' ') files to db/dump/"
