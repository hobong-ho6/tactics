#!/usr/bin/env bash
# 히트맵·리포트 페이지 로컬 서버 — 에이전트 툴 없이 어느 셸에서든 동일하게 뜬다.
#
# Claude Code의 .claude/launch.json은 preview 데몬이 ~/Documents에 TCC 권한이 없어
# /private/tmp/tactics-preview 미러를 서빙한다. 셸에서 직접 띄울 때는 그 우회가
# 필요 없으므로 site/를 그대로 서빙한다.
#
#   scripts/serve.sh              # http://127.0.0.1:8123 에 site/ 서빙
#   PORT=9000 scripts/serve.sh    # 포트 변경
#   scripts/serve.sh /private/tmp/tactics-preview   # 미러를 서빙(Claude Code와 동일 대상)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIR="${1:-$ROOT/site}"
PORT="${PORT:-8123}"

[ -d "$DIR" ] || { echo "디렉터리 없음: $DIR" >&2; exit 1; }

echo "서빙 $DIR → http://127.0.0.1:$PORT  (Ctrl-C로 종료)"
exec python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$DIR"
