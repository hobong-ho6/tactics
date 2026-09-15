#!/usr/bin/env python3
"""영상·스카우트 분석의 **반영 상태 재계산** — 자동 판정분만 (2026-09-14 신설, 09-15 정밀화).

왜:
  `player_duties.applied_status`는 「이 분석이 처방에 닿았는가」를 담는다(migration 031, G16).
  처방·분석이 늘어날 때마다 다시 계산해야 하므로 **재실행 가능한 스크립트**로 뺐다.
  match-watch 회차마다 실측·처방을 갱신한 뒤 이 스크립트를 돌린다.

⛔ **사람이 내린 판정(APPLIED/HELD/REJECTED)은 건드리지 않는다** — 자동 4종만 재계산한다.

⛔⛔ **「자동 4종만 재계산」은 `applied_status`에만 참이고 `applied_note`에는 거짓이었다**(2026-09-15 사고).
   자동 상태의 **사유에도 사람이 쓴 교정이 들어 있다** — ATM PROSE 9행의 「재판정 조건: map25 수집」이
   틀렸다고 손으로 고쳐놨는데 이 스크립트가 재실행에서 **자동 템플릿으로 통째로 덮었다**.
   G14는 `applied_note`를 보호 목록에 두지 않아 잡지 못했고, dump diff를 직접 읽어서야 발견했다.
   ⇒ 이제 **상태가 실제로 바뀔 때만 사유를 다시 쓴다**(`--force-note`로 강제 가능).
   ⭐ 부류: **「자동 재계산」 스크립트는 자기가 쓴 필드에 사람 손이 섞였는지 먼저 물어야 한다.**

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
    ap.add_argument("--force-note", action="store_true",
                    help="⛔ 자동 상태의 기존 사유까지 템플릿으로 덮어쓴다 — 사람이 쓴 교정이 날아간다(2026-09-15 사고)")
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
    changed, kept, counts = [], [], defaultdict(int)
    for d in con.execute("""SELECT id, player_id, game_role_implication imp, applied_status, applied_note
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
            # ⛔⛔ **상태가 그대로면 사유를 건드리지 않는다**(2026-09-15 사고 후 추가).
            #    자동 상태(PROSE·MATCH·NO_RX·CONFLICT)의 사유에도 **사람이 쓴 교정이 들어 있다** —
            #    09-15에 ATM PROSE 9행의 「재판정 조건: map25 수집」이 틀렸다고 손으로 고쳐놨는데,
            #    이 스크립트가 재실행에서 그걸 **자동 템플릿으로 통째로 덮었다**(G14는 applied_note를
            #    보호 목록에 두지 않아 잡지 못했다). 종전 주석의 「자동 4종만 재계산」은
            #    **상태**에만 참이었고 **사유**에는 거짓이었다.
            #    ⇒ 사유는 **판정이 실제로 바뀔 때만** 다시 쓴다. `--force-note`로 강제 가능.
            if st != d["applied_status"] or a.force_note or not (d["applied_note"] or "").strip():
                con.execute("UPDATE player_duties SET applied_status=?, applied_note=? WHERE id=?",
                            (st, note0 + extra, d["id"]))
                kept.append(None)
            else:
                con.execute("UPDATE player_duties SET applied_status=? WHERE id=?", (st, d["id"]))
                kept.append(d["id"])
    if not a.dry_run:
        con.commit()
    print(f"자동 판정 {sum(counts.values())}행:", dict(counts))
    print(f"상태 변경 {len(changed)}행:", changed[:20])
    if not a.dry_run:
        n_kept = len([x for x in kept if x is not None])
        print(f"⭐ 사유 보존 {n_kept}행(상태 불변 — 사람이 쓴 교정을 덮지 않는다) · 사유 재작성 {len(kept) - n_kept}행")
    held = con.execute("""SELECT applied_status, COUNT(*) FROM player_duties
                          WHERE applied_status NOT IN (%s) GROUP BY 1""" % ",".join("?" * len(AUTO)), AUTO).fetchall()
    print("사람 판정(건드리지 않음):", {r[0]: r[1] for r in held})
    print("다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
