#!/usr/bin/env python3
"""경기 프리셋 선발·교체의 **보유/비보유 분리 그리드 적합** 병기 (2026-10-22 신설 · migration 119).

왜: match_player_prescriptions.fit_sim은 합산 히트맵(map25) 한 장과의 코사인이라 FC27 시대 4경기 선발 44칸 중 25칸이 Δ≤.05 「무결정」이었다
    (경기 데이터 결손 검토 §2). WhoScored 국면 분리 그리드(player_matches.map25_poss/map25_def)는 이미 있다 — 같은 커널·같은 슬롯 x로
    보유 그리드 적합을 옆에 둔다. ⛔ role_id/focus는 바꾸지 않는다(사용자 판단 축) — 숫자 4칸만 채운다(기존 값은 같은 정의의 재계산으로 덮는다).
슬롯 x·역할군은 core.export의 game_players와 같은 규칙(경기 포메이션 slots → 없으면 pos의 첫 slots 행)을 따라 fit_sim과 출처가 일치한다.

사용:
    .venv/bin/python scripts/load_fit_poss.py --report 62 [--report 56 …] [--apply]
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                   # noqa: E402
from core.db import connect as connect_db             # noqa: E402
from core.kernel import Kernel                        # noqa: E402

UNDECIDED = 0.05                                      # 리포트 §7 「무결정 Δ≤.05」와 같은 임계


def rows_for(con, rid):
    return con.execute("""
        SELECT mpp.player_id, COALESCE(p.name_kr,p.name) label, mpp.game_version, mpp.pos_label, mpp.role_id, mpp.focus,
               mpp.fit_sim, mpp.fit_delta, mpp.starter, pm.map25_poss, pm.map25_def, pm.minutes,
               COALESCE(s.x, f.x) x, COALESCE(s.slot_type, f.slot_type) slot_type
        FROM match_player_prescriptions mpp
        JOIN players p ON p.id=mpp.player_id
        JOIN match_reports r ON r.id=mpp.report_id
        LEFT JOIN player_matches pm ON pm.match_id=r.match_id AND pm.player_id=mpp.player_id
        LEFT JOIN match_game_setups mgs ON mgs.report_id=mpp.report_id
        LEFT JOIN slots s ON s.regime_id=r.regime_id AND s.formation=mgs.formation AND s.pos=mpp.pos_label
        LEFT JOIN slots f ON f.rowid=(SELECT MIN(f2.rowid) FROM slots f2 WHERE f2.regime_id=r.regime_id AND f2.pos=mpp.pos_label)
        WHERE mpp.report_id=? ORDER BY mpp.starter DESC, mpp.sort_order""", (rid,)).fetchall()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", type=int, action="append", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    con = connect_db(DB)
    kernels = {}
    tot = dict(rows=0, filled=0, undecided=0, decided_on_poss=0, top1_changed=0)
    for rid in a.report:
        print(f"\n# report {rid}")
        for (pid, label, gv, pos, role, focus, fit, delta, starter, mp, md, minutes, x, st) in rows_for(con, rid):
            tot["rows"] += 1
            if not mp or x is None:
                print(f"  {pos:4} {label:10} — 보유 그리드 없음(분 {minutes}) → 건너뜀")
                continue
            k = kernels.setdefault(gv, Kernel(gv))
            r = k.fit_split(mp, md, role, focus, x, st)
            top = k.top2(mp, x, st)
            changed = bool(top) and (top[0][0], top[0][1]) != (role, focus)
            und = delta is not None and delta <= UNDECIDED
            dec = und and r["fit_delta_poss"] is not None and r["fit_delta_poss"] > UNDECIDED
            tot["filled"] += 1
            tot["undecided"] += und
            tot["decided_on_poss"] += dec
            tot["top1_changed"] += changed and bool(starter)
            flag = ("★1위 변경" if changed else "") + (" ◇무결정→결정" if dec else "")
            fs = f"{fit:.3f}" if fit is not None else "-"
            print(f"  {pos:4} {label:10} {role}/{focus:9} 합산 {fs} Δ{delta if delta is not None else '-':<6} | "
                  f"보유 {r['fit_sim_poss']:.3f} Δ{r['fit_delta_poss']:.3f} 1위 {top[0][0]}/{top[0][1]} {top[0][2]:.3f} · "
                  f"비보유 {r['fit_sim_def'] if r['fit_sim_def'] is not None else '-'} {flag}")
            if a.apply:
                con.execute("""UPDATE match_player_prescriptions SET fit_sim_poss=?, fit_sim_def=?, alt_role_poss=?, fit_delta_poss=?
                               WHERE report_id=? AND player_id=? AND pos_label=?""",
                            (r["fit_sim_poss"], r["fit_sim_def"], r["alt_role_poss"], r["fit_delta_poss"], rid, pid, pos))
    if a.apply:
        con.commit()
    print(f"\n행 {tot['rows']} · 채움 {tot['filled']} · 합산 무결정 {tot['undecided']} → 보유 그리드에서 결정 {tot['decided_on_poss']} · "
          f"선발 1위 조합 변경 {tot['top1_changed']} {'(적용)' if a.apply else '(--apply 없음)'}")


if __name__ == "__main__":
    main()
