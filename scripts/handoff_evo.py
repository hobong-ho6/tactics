#!/usr/bin/env python3
"""HANDOFF.md의 「진화 원장」 블록을 DB에서 다시 쓴다 (2026-11-07 신설 · 불변규칙 13).

왜 (사용자 「핸드오프에 진화 기록이나 db에 안남기는거야? 내역을 잘 모르네 세션들이」):
  진화 기록은 DB(`fut_evolution_log`)에 다 있었지만 HANDOFF는 손으로 써서 낡았다
  (시세 완주·운명의 실 2명·알리송 Marksman이 빠지고 「시세 1단계 진행 중」으로 남아 있었다).
  세션은 시작할 때 HANDOFF만 읽는다 ⇒ 블록을 DB에서 만들어 `ship.py`가 커밋마다 갱신한다.

블록 = 마커 사이(<!-- evo-ledger:start --> … <!-- evo-ledger:end -->). 마커 밖은 건드리지 않는다.
반환(종료 코드): 0 = 바뀜 · 1 = 그대로 · 2 = 마커 없음
"""
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core.db import connect  # noqa: E402  ⭐ DB 연결 정본(G36)
HANDOFF = ROOT / "HANDOFF.md"
START, END = "<!-- evo-ledger:start -->", "<!-- evo-ledger:end -->"
DAYS = 14


def block(con):
    since = (date.today() - timedelta(days=DAYS)).isoformat()
    rows = con.execute("""
        SELECT cp.name, l.evo_name, MAX(l.level) lv, MIN(l.ovr_before) ob, MAX(l.ovr_after) oa,
               MIN(l.applied_at) st, MAX(l.completed_at) done, MAX(l.removed_at) rm,
               SUM(l.completed_at IS NULL) open_n
          FROM v_evo_log l JOIN fut_club_players cp ON cp.id = l.club_player_id
         WHERE l.applied_at >= ? OR l.completed_at IS NULL
         GROUP BY l.club_player_id, l.evo_id ORDER BY MIN(l.applied_at) DESC, MIN(l.id) DESC""", (since,)).fetchall()
    out = [START, f"**진화 원장 (자동 · 최근 {DAYS}일 + 진행 중 · 정본 DB `fut_evolution_log` · `ship.py`가 갱신)**", ""]
    if not rows:
        out.append("- (없음)")
    for name, evo, lv, ob, oa, st, done, rm, open_n in rows:
        state = f"제거 {rm}" if rm else ("진행 중" if open_n else f"완료 {done}")
        out.append(f"- {st} · {name} ← {evo} {lv}단계 · OVR {ob}→{oa} · {state}")
    out.append(END)
    return "\n".join(out)


def main():
    text = HANDOFF.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print("⚠️ HANDOFF.md에 진화 원장 마커가 없다 — 건너뜀")
        return 2
    con = connect()
    head, rest = text.split(START, 1)
    new = head + block(con) + rest.split(END, 1)[1]
    if new == text:
        return 1
    HANDOFF.write_text(new, encoding="utf-8")
    print("   HANDOFF.md 진화 원장 블록 갱신")
    return 0


if __name__ == "__main__":
    sys.exit(main())
