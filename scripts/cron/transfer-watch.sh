#!/usr/bin/env bash
# 이적 감시 정기 실행 — cron에서 비대화형으로 돈다 (Claude Code 스케줄 작업의 대응물).
#
# 두 단계로 나눈 이유: ⑴ Fotmob 수집은 기계적이라 LLM 없이도 되고, 실패해도 나머지를
# 막으면 안 된다. ⑵ 티어 판정·DB 쓰기·리포트·커밋은 판단이 필요해 codex가 있어야 한다.
# codex가 없으면 ⑴만 남기고 그 사실을 로그에 명시한다 — 조용히 성공한 척하지 않는다.
#
# crontab 등록: scripts/cron/install.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 1

# cron의 PATH는 최소라 npm 전역 bin과 시스템 경로를 명시한다.
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

STAMP="$(date +%Y%m%d-%H%M)"
mkdir -p "$ROOT/logs"
LOG="$ROOT/logs/transfer-watch-$STAMP.log"
exec >>"$LOG" 2>&1

echo "═══ 이적 감시 $STAMP 시작 (호스트 $(hostname)) ═══"

echo "--- 1/2 Fotmob 리드 수집 (3팀) ---"
if [ -x "$ROOT/.venv/bin/python" ]; then
  "$ROOT/.venv/bin/python" scripts/fetch_fotmob.py AVL CHE LIV \
    > "$ROOT/logs/fotmob-$STAMP.txt" 2>>"$LOG" \
    && echo "OK → logs/fotmob-$STAMP.txt" \
    || echo "⚠️ Fotmob 수집 실패 (다음 단계는 계속 진행)"
else
  echo "⚠️ .venv 없음 — AGENTS.md §0 세팅 필요. Fotmob 건너뜀"
fi

echo "--- 2/2 판정·DB·리포트·커밋 ---"
codex_rc=0
CODEX_BIN="$(command -v codex 2>/dev/null || true)"
if [ -z "$CODEX_BIN" ] && [ -x "/Applications/ChatGPT.app/Contents/Resources/codex" ]; then
  CODEX_BIN="/Applications/ChatGPT.app/Contents/Resources/codex"
fi

if [ -n "$CODEX_BIN" ]; then
  # --full-auto는 공식 문서상 deprecated이고 현재 앱 번들 CLI에서는 제거됐다.
  # --approve-for-me가 workspace-write 샌드박스 안에서 승인 요청을 자동 검토한다.
  "$CODEX_BIN" exec --ephemeral --approve-for-me -C "$ROOT" \
    "$(cat "$ROOT/scripts/cron/transfer-watch-prompt.txt")"
  rc=$?
  echo "codex exec 종료 코드: $rc"
  if [ "$rc" -ne 0 ]; then
    echo "⛔ 판정 단계 실패 — 위 codex 로그를 확인할 것"
    codex_rc="$rc"
  fi
else
  echo "⛔ codex 미설치 — 판정 단계를 건너뛴다. 수집분만 logs/fotmob-$STAMP.txt에 남았다."
  echo "   ChatGPT 앱 또는 @openai/codex CLI 설치 필요"
fi

echo "═══ 종료 $(date +%H:%M:%S) ═══"
exit "$codex_rc"
