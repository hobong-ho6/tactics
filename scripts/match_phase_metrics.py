#!/usr/bin/env python3
"""WhoScored(Opta) 이벤트 → 경기 구간 지표 적재 (2026-10-20 신설 · migration 109).

경기 분석 화면 「경기 흐름」의 원료다. 계산은 core.whoscored.segment_metrics 하나만 쓴다(불변규칙 4 —
세션마다 콘솔 JS로 다시 짜지 않는다). 수집 회차가 matchCentreData를 받아 둔 JSON 파일을 넘긴다.

구간: 기본 15분 창(0·15·30·45·60·75·종료) + --cuts로 득점·교체 분을 더한다(예: --cuts 36,43,56,77).
⛔ 이미 같은 (report, side, metric, seg_from)이 있으면 멈춘다 — 다른 구간 정의로 다시 넣으려면 먼저 사람이 판단한다.

사용:
    .venv/bin/python scripts/match_phase_metrics.py --report 57 --events /tmp/ws-1983609.json \
        --team-id 15 --opp-id 31 --dry-run
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                   # noqa: E402
from core.db import connect as connect_db             # noqa: E402
from core.whoscored import gk_ids_of, segment_metrics  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", type=int, required=True)
    ap.add_argument("--events", required=True, help="matchCentreData JSON(전체 또는 events 배열)")
    ap.add_argument("--team-id", type=int, required=True, help="리포트 팀의 WhoScored teamId")
    ap.add_argument("--opp-id", type=int, required=True)
    ap.add_argument("--cuts", default="", help="15분 창에 더할 구간 경계 분(쉼표)")
    ap.add_argument("--metrics", default="", help="이 지표만(쉼표 · 예: gk_long_share) — 다른 지표가 이미 적재된 리포트에 한 지표를 보강할 때")
    ap.add_argument("--merge-existing", action="store_true",
                    help="같은 (report, side, metric, seg_from)이 있으면 멈추지 않고 value·n·seg_to를 갱신(구간 재정의 — 사람이 판단한 뒤에만 · note에 남긴다)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    raw = json.loads(Path(a.events).read_text(encoding="utf-8"))
    events = raw.get("events", raw) if isinstance(raw, dict) else raw
    cuts = {15, 30, 45, 60, 75} | {int(x) for x in a.cuts.split(",") if x.strip()}
    # ⭐ GK 롱패스 비중(gk_long_share · G37 ⑹)은 전체 matchCentreData(home/away.players)가 있어야 GK를 안다 —
    #    events 배열만 넘기면 계산되지 않으므로 여기서 멈춘다(조용히 빠지면 G37이 커밋을 막을 때 원인을 모른다).
    gk_ids = gk_ids_of(raw)
    if not gk_ids:
        raise SystemExit("⛔ GK를 알 수 없다(home/away.players 없음) — matchCentreData 전체 JSON을 넘길 것(gk_long_share 계산 불가)")
    rows = segment_metrics(events, a.team_id, a.opp_id, cuts, gk_ids=gk_ids)
    if a.metrics:
        keep = {m.strip() for m in a.metrics.split(",") if m.strip()}
        rows = [r for r in rows if r["metric"] in keep]
    src = f"WhoScored matchCentreData {Path(a.events).name} → core.whoscored.segment_metrics (match_phase_metrics.py)"
    conf = "HIGH — Opta 이벤트 직접 계산. ⚠️ 구간이 짧으면 표본(n)이 작다 — 화면이 흐리게 그린다"
    for r in rows:
        print(f"  {r['side']} {r['metric']:18} {r['seg_from']:>3}–{r['seg_to'] if r['seg_to'] is not None else '끝':>3}  {r['value']:>6}  n={r['n']}")
    if a.dry_run:
        print(f"[dry-run] {len(rows)}행 — 쓰지 않았다")
        return
    con = connect_db(DB)
    try:
        for r in rows:
            if a.merge_existing:
                hit = con.execute("SELECT id, seg_to, value, n FROM match_phase_metrics WHERE report_id=? AND side=? AND metric=? AND seg_from=?",
                                  (a.report, r["side"], r["metric"], r["seg_from"])).fetchone()
                if hit:
                    con.execute("""UPDATE match_phase_metrics SET seg_to=?, value=?, n=?, source=?, confidence=?,
                                   note=COALESCE(note,'') || ? WHERE id=?""",
                                (r["seg_to"], r["value"], r["n"], src, conf,
                                 f" · [구간 재정의 {src.split(' ')[0]}] 종전 {r['seg_from']}–{hit[1] if hit[1] is not None else '끝'} {hit[2]}(n={hit[3]}) → "
                                 f"{r['seg_from']}–{r['seg_to'] if r['seg_to'] is not None else '끝'} (--merge-existing)", hit[0]))
                    continue
            con.execute("""INSERT INTO match_phase_metrics(report_id,side,metric,seg_from,seg_to,value,n,note,source,confidence)
                           VALUES(?,?,?,?,?,?,?,NULL,?,?)""",
                        (a.report, r["side"], r["metric"], r["seg_from"], r["seg_to"], r["value"], r["n"], src, conf))
    except Exception as e:                                 # noqa: BLE001
        con.rollback()
        raise SystemExit(f"⛔ 적재 중단(전부 되돌림): {e}")
    con.commit()
    print(f"✅ #{a.report}: 구간 지표 {len(rows)}행")


if __name__ == "__main__":
    main()
