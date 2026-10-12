#!/bin/sh
# Rebuild db/tactics.db from the committed SQL dumps (db/dump/).
#
# 왜 (2026-10-12 사용자 결정 「①+② 둘 다 진행」): .db 바이너리가 GitHub 100MB 상한을 두 번 넘었다
#   (10-04 103.8MB · 10-12 101.2MB). 그래서 git에는 **dump만** 싣고 .db는 각 PC에서 dump로 다시 만든다.
#   ⭐ 정본은 여전히 로컬의 db/tactics.db다(불변규칙 1) — git이 나르는 형식만 dump로 바뀌었다.
#
# 언제: ⑴ 새로 클론했을 때 ⑵ pull로 다른 PC의 dump가 들어왔을 때 —
#   이때 db_dump.sh·gates.py(G33)가 「DB가 dump보다 낡았다」로 멈추고 이 스크립트를 가리킨다.
# ⚠️ 지금 DB를 덮는다 — 덮기 전에 db/.snapshots/에 사본을 남긴다(dump 안 한 로컬 변경을 잃지 않게).
set -e
cd "$(dirname "$0")/.."
db=db/tactics.db
tmp=db/tactics.db.restore-tmp
[ -f db/dump/schema.sql ] || { echo "⛔ db/dump/schema.sql 없음"; exit 1; }
rm -f "$tmp"
# ⚠️ `.schema`는 뷰마다 `/* 뷰(컬럼…) */;` 주석 줄을 덧붙인다. 그대로 넣으면 다음 객체의 SQL 본문에 섞여
#    dump → 복원을 돌 때마다 쌓인다(2026-10-12 복원 대조에서 확인) — 주석만 지우고 `;`는 남긴다.
#    ⛔ 그 줄 끝의 `;`는 바로 앞 CREATE VIEW의 종결자다 — 줄째 지우면 다음 문장과 붙어 파싱이 깨진다(실측).
sed -E 's#^/\* [A-Za-z0-9_]+\(.*\) \*/;$#;#' db/dump/schema.sql | sqlite3 -bail "$tmp" \
  || { rm -f "$tmp"; echo "⛔ 스키마 복원 실패 — 기존 DB는 그대로다"; exit 1; }
# 한 트랜잭션으로 넣는다(행마다 커밋하면 수십 분 걸린다). 스키마에 있는 표의 dump만 넣는다 —
# 지운 표의 낡은 dump 파일이 남아 있어도 끼어들지 않게. bail=on: 한 줄이라도 실패하면 반쯤 찬 DB를 쓰지 않는다.
tables=$(sqlite3 "$tmp" "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
{ echo ".bail on"; echo "BEGIN;"; for t in $tables; do cat "db/dump/$t.sql"; done; echo "COMMIT;"; } \
  | sqlite3 "$tmp" || { rm -f "$tmp"; echo "⛔ 복원 실패 — 기존 DB는 그대로다"; exit 1; }
if [ -f "$db" ]; then
  mkdir -p db/.snapshots
  bak="db/.snapshots/pre-restore-$(date +%Y%m%d-%H%M%S).db"
  cp "$db" "$bak"
  echo "기존 DB 사본: $bak"
fi
mv "$tmp" "$db"
scripts/db_stamp.sh sync
echo "✅ db/tactics.db를 dump에서 복원했다 ($(sqlite3 "$db" "SELECT COUNT(*) FROM sqlite_master WHERE type='table'") 표)"
