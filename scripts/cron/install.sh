#!/usr/bin/env bash
# 이적 감시 cron 등록 — 매일 09:00 / 21:00 (Claude Code 스케줄 작업과 같은 시각).
# 멱등: 이미 있는 tactics 항목을 지우고 다시 넣는다. 다른 cron 항목은 건드리지 않는다.
#
#   scripts/cron/install.sh          # 등록
#   scripts/cron/install.sh --remove # 해제
#
# ⛔ macOS TCC (2026-08-13 실증): 등록·기동은 되지만 실행이 막힌다 —
#    "bash: .../transfer-watch.sh: Operation not permitted". cron이 ~/Documents 를 못 읽는다.
#    시스템 설정 → 개인정보 보호 및 보안 → 전체 디스크 접근 권한 → /usr/sbin/cron 추가로 풀린다.
#    스크립트 문제가 아니다 — 셸에서 직접 돌리면 정상 완료한다.
#    (이 저장소는 같은 TCC 문제를 이미 겪었다 — .claude/launch.json 주석 참조.)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RUNNER="$ROOT/scripts/cron/transfer-watch.sh"
MARK="# tactics:transfer-watch"

current="$(crontab -l 2>/dev/null || true)"
cleaned="$(printf '%s\n' "$current" | grep -v "$MARK" || true)"

if [ "${1:-}" = "--remove" ]; then
  printf '%s\n' "$cleaned" | grep -v '^$' | crontab - 2>/dev/null || crontab -r 2>/dev/null || true
  echo "해제됨."
  crontab -l 2>/dev/null || echo "(crontab 비어 있음)"
  exit 0
fi

{
  printf '%s\n' "$cleaned" | grep -v '^$' || true
  echo "0 9 * * * $RUNNER $MARK"
  echo "0 21 * * * $RUNNER $MARK"
} | crontab -

echo "등록 완료 — 매일 09:00 / 21:00"
crontab -l
