#!/bin/sh
# dump 스탬프 — 「이 PC의 DB가 git의 dump와 같은 회차인가」를 가른다 (2026-10-12 · .db 추적 중단과 함께 신설).
#
#   db/dump/_stamp.txt  (git 추적) = 마지막으로 dump를 만든 회차의 지문(dump *.sql 전체의 sha256)
#   db/.dump_stamp      (로컬 전용) = 이 PC의 DB가 마지막으로 dump와 맞춰진 회차의 지문
# 둘이 다르면 = pull로 남의 dump가 들어왔는데 DB는 아직 옛것 → 이 상태에서 dump하면 **남의 데이터를 지운다**.
#
#   db_stamp.sh check  → 같으면 0, 다르면 메시지와 함께 1
#   db_stamp.sh sync   → 지금 dump의 지문을 두 곳에 쓴다(db_dump.sh·db_restore.sh 끝에서 부른다)
set -e
cd "$(dirname "$0")/.."
fp() { cat db/dump/*.sql | shasum -a 256 | cut -d' ' -f1; }
case "$1" in
  check)
    [ -f db/dump/_stamp.txt ] || exit 0          # 스탬프 도입 전 dump — 비교할 것이 없다
    if [ ! -f db/tactics.db ] || [ ! -f db/.dump_stamp ] || ! cmp -s db/dump/_stamp.txt db/.dump_stamp; then
      echo "⛔ 이 PC의 DB가 git의 dump보다 낡았다(새 클론이거나 pull로 다른 PC의 dump가 들어왔다)."
      echo "   ⇒ scripts/db_restore.sh 로 dump에서 DB를 다시 만든 뒤 진행할 것."
      echo "   ⚠️ 그대로 dump하면 다른 PC에서 들어온 데이터를 옛 DB로 덮어 지운다."
      exit 1
    fi ;;
  sync)
    fp > db/dump/_stamp.txt
    cp db/dump/_stamp.txt db/.dump_stamp ;;
  *) echo "usage: db_stamp.sh check|sync"; exit 2 ;;
esac
