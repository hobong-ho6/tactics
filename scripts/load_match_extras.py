#!/usr/bin/env python3
"""경기 리포트의 가설 판정·구간 지표·요약 포인트 적재 (2026-10-20 신설 · migration 109).

왜 (사용자 지시 2026-10-20 「경기 흐름이나 선수 포인트, 관전 메모 가설 판정, 부상 등에 대해서도 경기 분석에서 항상 제공」):
  이 셋은 리포트 원문(markdown)에만 있어 화면이 「원문 펼치기」로만 보여줬다. 수집 회차가 판정을 쓰면
  같은 내용을 JSON 한 장으로 만들어 이 스크립트로 넣는다 — 화면은 export만 읽는다(불변규칙 1).

JSON 형식:
  {"report_id": 56, "key_points": "<markdown 불릿>", "source": "...", "confidence": "...",
   "hypotheses":  [{"seq", "tag", "round": "D0", "claim", "measured", "evidence", "verdict", "verdict_note", "obs_id"}],
   "corrections": [{"seq", "round": "D1|D2|D3", "measured", "evidence", "verdict", "verdict_note", "obs_id"}],
   "phase_metrics": [{"side": "v|o", "metric", "seg_from", "seg_to", "value", "n", "note"}],
   ⭐ migration 111(전술 분석 4칸 · 2026-10-20):
   "tactics": {"tac_possession", "tac_defense", "tac_transition" (markdown 불릿), "strengths": [..], "weaknesses": [..],
               "opp_disruption", "impl_verdict": "유지|추가 관찰|시험 프리셋|정본 변경", "recheck_items": [..]},
   "changes": [{"seq", "minute", "minute_to", "title", "detail"}],          # 경기 중 변화 단계(분 축)
   "prescriptions": [{"pos_label", "fit_delta", "alt_role"}]}                # 선발 처방의 1·2위 격차(무결정 Δ 막대)
  verdict ∈ match · partial · mismatch · undecided · pending.  metric ⊆ core.whoscored.PHASE_METRICS.

⛔ 추가만(불변규칙 2): 정정은 원래 행을 고치지 않는다 — 같은 seq의 **최신 행**을 supersedes_id로 가리키는
   새 행을 넣는다. 이미 있는 (report, seq, round)·(report, side, metric, seg_from)를 만나면 **멈춘다**
   (조용히 건너뛰면 다시 돌린 회차가 무엇을 넣었는지 모른다). key_points는 「현재 요약」이라 갱신한다.

사용:
    .venv/bin/python scripts/load_match_extras.py --json /tmp/r56.json --dry-run
    .venv/bin/python scripts/load_match_extras.py --json /tmp/r56.json
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                   # noqa: E402
from core.db import connect as connect_db             # noqa: E402  ⭐ DB 연결 정본(대기·작성 중 표시)
from core.whoscored import PHASE_METRICS              # noqa: E402  ⭐ 지표 목록 정본

VERDICTS = {"match", "partial", "mismatch", "undecided", "pending"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    d = json.loads(Path(a.json).read_text(encoding="utf-8"))
    rid = int(d["report_id"])
    src = d.get("source") or f"{a.json} (load_match_extras.py)"
    conf = d.get("confidence") or "리포트 판정 그대로 — 근거 등급은 각 행 evidence 참조"
    now = dt.datetime.now().isoformat(timespec="seconds")

    bad = [h.get("seq") for h in d.get("hypotheses", []) + d.get("corrections", []) if h.get("verdict") not in VERDICTS]
    bad_m = sorted({m["metric"] for m in d.get("phase_metrics", []) if m["metric"] not in PHASE_METRICS})
    if bad or bad_m:
        raise SystemExit(f"⛔ 모르는 판정값 seq {bad} · 모르는 지표 {bad_m} — PHASE_METRICS/VERDICTS를 먼저 넓힐 것")

    con = connect_db(DB)
    if not con.execute("SELECT 1 FROM match_reports WHERE id=?", (rid,)).fetchone():
        raise SystemExit(f"⛔ match_reports #{rid} 없음")
    n_h = n_c = n_p = n_t = 0
    try:
        for h in d.get("hypotheses", []):
            con.execute("""INSERT INTO match_hypotheses(report_id,seq,tag,round,claim,measured,evidence,verdict,
                             verdict_note,supersedes_id,obs_id,source,confidence,created_at)
                           VALUES(?,?,?,?,?,?,?,?,?,NULL,?,?,?,?)""",
                        (rid, h["seq"], h.get("tag"), h.get("round") or "D0", h["claim"], h["measured"],
                         h.get("evidence"), h["verdict"], h.get("verdict_note"), h.get("obs_id"), src, conf, now))
            n_h += 1
        # 정정은 회차 순서대로 — D1 정정 위에 D2 정정이 얹힌다
        for c in sorted(d.get("corrections", []), key=lambda c: c["round"]):
            prev = con.execute("""SELECT id, tag, claim FROM match_hypotheses WHERE report_id=? AND seq=?
                                  ORDER BY round DESC, id DESC LIMIT 1""", (rid, c["seq"])).fetchone()
            if not prev:
                raise SystemExit(f"⛔ 정정 대상 seq {c['seq']}의 원래 판정이 없다")
            con.execute("""INSERT INTO match_hypotheses(report_id,seq,tag,round,claim,measured,evidence,verdict,
                             verdict_note,supersedes_id,obs_id,source,confidence,created_at)
                           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (rid, c["seq"], prev[1], c["round"], prev[2], c["measured"], c.get("evidence"),
                         c["verdict"], c.get("verdict_note"), prev[0], c.get("obs_id"), src, conf, now))
            n_c += 1
        for m in d.get("phase_metrics", []):
            con.execute("""INSERT INTO match_phase_metrics(report_id,side,metric,seg_from,seg_to,value,n,note,source,confidence)
                           VALUES(?,?,?,?,?,?,?,?,?,?)""",
                        (rid, m["side"], m["metric"], m["seg_from"], m.get("seg_to"), m["value"], m.get("n"),
                         m.get("note"), src, conf))
            n_p += 1
        if d.get("key_points"):
            con.execute("UPDATE match_reports SET key_points=? WHERE id=?", (d["key_points"], rid))
        t = d.get("tactics") or {}
        TCOLS = ["tac_possession", "tac_defense", "tac_transition", "strengths", "weaknesses",
                 "opp_disruption", "impl_verdict", "recheck_items"]
        if set(t) - set(TCOLS):
            raise ValueError(f"모르는 tactics 키 {sorted(set(t) - set(TCOLS))}")
        for k in TCOLS:                     # 「현재 판단」 칸이라 갱신한다(key_points와 같은 규약)
            if k in t:
                v = t[k]
                con.execute(f"UPDATE match_reports SET {k}=? WHERE id=?",
                            (json.dumps(v, ensure_ascii=False) if isinstance(v, list) else v, rid))
        n_t = sum(1 for k in TCOLS if k in t)
        for c in d.get("changes", []):
            con.execute("""INSERT INTO match_tactical_changes(report_id,seq,minute,minute_to,title,detail,source,confidence)
                           VALUES(?,?,?,?,?,?,?,?)""",
                        (rid, c["seq"], c["minute"], c.get("minute_to"), c["title"], c.get("detail"), src, conf))
        for x in d.get("prescriptions", []):
            n = con.execute("""UPDATE match_player_prescriptions SET fit_delta=?, alt_role=?
                               WHERE report_id=? AND pos_label=? AND starter=1""",
                            (x["fit_delta"], x.get("alt_role"), rid, x["pos_label"])).rowcount
            if n != 1:
                raise ValueError(f"선발 처방 {x['pos_label']} {n}행 — 정확히 1행이어야 한다")
    except Exception as e:                                 # noqa: BLE001 — UNIQUE 충돌 포함 전부 되돌린다
        con.rollback()
        raise SystemExit(f"⛔ 적재 중단(전부 되돌림): {e}")
    if a.dry_run:
        con.rollback()
        print(f"[dry-run] #{rid}: 판정 {n_h} · 정정 {n_c} · 구간 지표 {n_p} · 요약 {'있음' if d.get('key_points') else '없음'}"
              f" · 전술 칸 {n_t} · 변화 단계 {len(d.get('changes', []))} · 처방 Δ {len(d.get('prescriptions', []))} — 쓰지 않았다")
        return
    con.commit()
    print(f"✅ #{rid}: 판정 {n_h} · 정정 {n_c} · 구간 지표 {n_p} · 요약 {'갱신' if d.get('key_points') else '없음'}"
          f" · 전술 칸 {n_t} · 변화 단계 {len(d.get('changes', []))} · 처방 Δ {len(d.get('prescriptions', []))}")
    print("다음: python3 scripts/gates.py && python3 scripts/export.py")


if __name__ == "__main__":
    main()
