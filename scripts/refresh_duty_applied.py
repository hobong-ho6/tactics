#!/usr/bin/env python3
"""영상·스카우트 분석의 **반영 상태 재계산** — 자동 판정분만 (2026-09-14 신설, 09-15 정밀화).

왜:
  `player_duties.applied_status`는 「이 분석이 처방에 닿았는가」를 담는다(migration 031, G16).
  처방·분석이 늘어날 때마다 다시 계산해야 하므로 **재실행 가능한 스크립트**로 뺐다.
  match-watch 회차마다 실측·처방을 갱신한 뒤 이 스크립트를 돌린다.

⛔ **사람이 내린 판정(APPLIED/HELD/REJECTED)은 건드리지 않는다** — 자동 4종만 재계산한다.

⭐ **슬롯 계열(`w_` 윙 ↔ `wm_` 와이드 미드)은 같은 역할로 본다** (09-15 정정).
   둘은 **역할이 아니라 슬롯이 다른 것**이고 슬롯은 `slots` 표가 정한다 —
   바르콜라 `w_wideplm`(LW 분석) ↔ 우리 `wm_wideplm`(LM 슬롯)을 충돌로 세면 오탐이다.

사용:
    .venv/bin/python scripts/refresh_duty_applied.py --dry-run
    .venv/bin/python scripts/refresh_duty_applied.py
"""
import argparse
import datetime as dt
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                     # noqa: E402

AUTO = ("MATCH", "CONFLICT", "NO_RX", "PROSE")


def canon(role):
    """슬롯 계열을 지우고 역할 어간만 남긴다 — `w_wideplm`·`wm_wideplm` → `wide_wideplm`."""
    return re.sub(r"^wm?_", "wide_", role or "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    roles = {r[0] for r in con.execute("SELECT DISTINCT role_id FROM game_role_focus")}
    have = defaultdict(set)
    for q, c in (("SELECT player_id, role_id FROM prescriptions WHERE role_id IS NOT NULL", "role_id"),
                 ("SELECT player_id, role_id FROM match_player_prescriptions WHERE role_id IS NOT NULL", "role_id"),
                 ("SELECT player_id, fit_role FROM squad_entries WHERE fit_role IS NOT NULL", "fit_role")):
        for r in con.execute(q):
            have[r["player_id"]].add(r[c])

    note0 = f"[{a.pulled} 자동 재계산] 사람 승인 아님 — 분석이 명시한 역할 코드 ↔ prescriptions·match_player_prescriptions·squad_entries.fit_role 전량 대조(슬롯 계열 w_/wm_는 동일 역할로 봄)."
    changed, counts = [], defaultdict(int)
    for d in con.execute("""SELECT id, player_id, game_role_implication imp, applied_status
                            FROM player_duties
                            WHERE applied_status IS NULL OR applied_status IN (%s)"""
                         % ",".join("?" * len(AUTO)), AUTO):
        found = {x for x in roles if x in (d["imp"] or "")}
        mine = have.get(d["player_id"], set())
        hit = {x for x in found if canon(x) in {canon(y) for y in mine}}
        if not found:
            st, extra = "PROSE", " 역할 코드가 없어 기계 판정 불가 — 반영 여부는 사람이 적어야 한다."
        elif not mine:
            st, extra = "NO_RX", " 이 선수의 처방 행이 아직 없다."
        elif hit:
            st, extra = "MATCH", f" 일치 역할: {', '.join(sorted(hit))}."
            slot_only = [x for x in hit if x not in mine]
            if slot_only:
                extra += f" ⭐ 슬롯 계열만 다르다({', '.join(sorted(slot_only))} ↔ 보유 {', '.join(sorted(mine))}) — 역할은 같다."
        else:
            st, extra = "CONFLICT", f" 분석 {', '.join(sorted(found))} ↔ 보유 처방 {', '.join(sorted(mine))} — 사람 판정 대기."
        counts[st] += 1
        if st != d["applied_status"]:
            changed.append((d["id"], d["applied_status"], st))
        if not a.dry_run:
            con.execute("UPDATE player_duties SET applied_status=?, applied_note=? WHERE id=?",
                        (st, note0 + extra, d["id"]))
    if not a.dry_run:
        con.commit()
    print(f"자동 판정 {sum(counts.values())}행:", dict(counts))
    print(f"상태 변경 {len(changed)}행:", changed[:20])
    held = con.execute("""SELECT applied_status, COUNT(*) FROM player_duties
                          WHERE applied_status NOT IN (%s) GROUP BY 1""" % ",".join("?" * len(AUTO)), AUTO).fetchall()
    print("사람 판정(건드리지 않음):", {r[0]: r[1] for r in held})
    print("다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
