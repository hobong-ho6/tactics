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
mkdir -p db/dump
sqlite3 "$db" .schema > db/dump/schema.sql
for t in $(sqlite3 "$db" "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"); do
  sqlite3 "$db" ".mode insert $t" "SELECT * FROM $t;" > "db/dump/$t.sql"
done
scripts/db_stamp.sh sync
echo "dumped $(ls db/dump | wc -l | tr -d ' ') files to db/dump/"
