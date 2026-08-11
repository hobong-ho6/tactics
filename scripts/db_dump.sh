#!/bin/sh
# Regenerate diffable SQL dumps from db/tactics.db (v2).
# Run after ANY DB change, before committing (see docs/00-overview.md).
# v1 dumps (data/dump/)는 아카이브와 함께 동결 — 여기서는 건드리지 않는다.
set -e
cd "$(dirname "$0")/.."
db=db/tactics.db
mkdir -p db/dump
sqlite3 "$db" .schema > db/dump/schema.sql
for t in $(sqlite3 "$db" "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"); do
  sqlite3 "$db" ".mode insert $t" "SELECT * FROM $t;" > "db/dump/$t.sql"
done
echo "dumped $(ls db/dump | wc -l | tr -d ' ') files to db/dump/"
