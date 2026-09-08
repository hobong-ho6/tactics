#!/usr/bin/env python3
"""migration 027 후속 — match_game_setups.rule_note 백필 (2026-09-08).

core.team_settings 규칙을 기존 경기 프리셋 19행에 적용해 일치/편차를 **기록만** 한다.
⛔ 기록된 설정값은 하나도 바꾸지 않는다 — 편차는 「규칙과 다르게 골랐고 당시 산문 근거만 있다」는
사실이며, 재판정은 사용자 판단이다. 새 행은 세션이 직접 rule_note를 채운다(match-watch SKILL §2-2).
재실행 안전: rule_note가 이미 있으면 건너뛴다.
"""
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                     # noqa: E402
from core.team_settings import suggest, compare         # noqa: E402

con = sqlite3.connect(DB)
rows = con.execute("""
    SELECT mgs.report_id, mgs.build_up_style, mgs.defensive_approach, mgs.line_height,
           (SELECT MAX(possession) FROM player_matches pm
             WHERE pm.event_id=mr.event_id AND pm.team_code=mr.team_code) poss,
           ts.ppda_v, ts.passes_v, ts.long_att_v
    FROM match_game_setups mgs JOIN match_reports mr ON mr.id=mgs.report_id
    LEFT JOIN team_match_stats ts ON ts.event_id=mr.event_id AND ts.team_code=mr.team_code
    WHERE mgs.rule_note IS NULL ORDER BY mgs.report_id""").fetchall()
n_rule = n_div = n_nostats = 0
for rid, bu, da, lh, poss, ppda, passes, long_att in rows:
    sug = suggest(poss, passes, long_att, ppda)
    missing = [k for k, v in (("점유", poss), ("PPDA", ppda), ("롱볼", long_att)) if v is None]
    diff = compare(sug, bu, da, lh)
    if diff:
        note = ("DIVERGE (backfill 2026-09-08): " + " · ".join(diff)
                + " — 기록 당시 산문 근거 유지, 규칙 사전등록 전 판정이라 재판정 미실시")
        n_div += 1
    elif missing and not (sug["build_up_style"] and sug["defensive_approach"]):
        note = "NO-STATS (backfill 2026-09-08): " + "·".join(missing) + " 결손으로 규칙 적용 불가"
        n_nostats += 1
    else:
        note = "RULE (backfill 2026-09-08)" + (f" — {'·'.join(missing)} 결손 축은 비교 생략" if missing else "")
        n_rule += 1
    con.execute("UPDATE match_game_setups SET rule_note=? WHERE report_id=?", (note, rid))
    print(f"  report {rid:>3}: {note[:110]}")
con.commit()
print(f"rule_note 백필: RULE {n_rule} · DIVERGE {n_div} · NO-STATS {n_nostats} (총 {len(rows)})")
