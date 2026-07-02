#!/bin/sh
# Regenerate diffable SQL dumps from data/avl_analysis.db.
# Run after ANY DB change, before committing (see docs/40-pipeline.md).
set -e
cd "$(dirname "$0")/.."
db=data/avl_analysis.db
mkdir -p data/dump
sqlite3 "$db" .schema > data/dump/schema.sql
for t in $(sqlite3 "$db" "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"); do
  sqlite3 "$db" ".mode insert $t" "SELECT * FROM $t;" > "data/dump/$t.sql"
done
echo "dumped $(ls data/dump | wc -l | tr -d ' ') files to data/dump/"
