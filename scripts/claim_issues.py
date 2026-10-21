#!/usr/bin/env python3
"""판정 쟁점 관리 — 영상 구현 주장 PENDING을 쟁점 단위로 열고·세고·닫는다 (2026-10-21 · migration 114).

왜: PENDING의 판정 조건이 산문에만 있어 165건이 아무도 닫지 않은 채 쌓였다(사용자 「판정대기는 언제 판정완료되는거야?」).
  트리거 판정 정본은 core/claim_issues.py — 여기는 그걸 부르는 손잡이다. G39가 기한 초과·미연결을 막는다.

사용:
    python3 scripts/claim_issues.py                 # 열린 쟁점 + 진행도
    python3 scripts/claim_issues.py --due           # 트리거가 찬 쟁점만(판정할 차례) + 묶인 주장
    python3 scripts/claim_issues.py --load F.json   # {"issues":[{…spec…, "claim_ids":[…]}]} 쟁점 생성 + 주장 연결
    python3 scripts/claim_issues.py --attach ISSUE CLAIM_ID…      # 새 PENDING 주장을 기존 쟁점에 묶는다
    python3 scripts/claim_issues.py --close ISSUE --verdict HELD --note "실측 근거…"
        → 쟁점을 닫고 묶인 PENDING 주장의 verdict를 한 번에 바꾼다(verdict_note에 판정 이력을 **덧붙인다**)
⛔ 판정(--close)은 사람이 실측을 보고 내린다 — 이 스크립트는 판정을 만들지 않는다.
"""
import argparse
import datetime as dt
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                        # noqa: E402
from core.db import connect as connect_db                  # noqa: E402
from core.claim_issues import progress, trigger_kr, insert_issue, overdue   # noqa: E402

TODAY = dt.date.today().isoformat()


def show(con, only_due):
    rows = con.execute("SELECT * FROM claim_issues WHERE status='open' ORDER BY hold, team_code, id").fetchall()
    n_due = 0
    for r in rows:
        p = progress(con, r)
        if only_due and not p["due"]:
            continue
        n_due += p["due"]
        cl = con.execute("SELECT id, video_id FROM video_impl_claims WHERE issue_id=? AND verdict='PENDING'", (r["id"],)).fetchall()
        flag = "⛔ 기한 초과" if overdue(con, r) else ("⭐ 판정할 차례" if p["due"] else "")
        print(f"#{r['id']:<3} {r['team_code']}{' [보류]' if r['hold'] else ''} {r['title_kr']} — {trigger_kr(con, r)} · 주장 {len(cl)} {flag}")
        if only_due:
            print(f"     판정: {r['question_kr']}\n     실측: {r['measure_kr']}\n     주장: {', '.join(str(c['id']) for c in cl)}")
    print(f"\n열린 쟁점 {len(rows)} · 판정할 차례 {n_due}")


def attach(con, issue_id, claim_ids):
    if not con.execute("SELECT 1 FROM claim_issues WHERE id=? AND status='open'", (issue_id,)).fetchone():
        raise SystemExit(f"⛔ 열린 쟁점 #{issue_id}이 없다")
    for cid in claim_ids:
        r = con.execute("SELECT verdict, issue_id FROM video_impl_claims WHERE id=?", (cid,)).fetchone()
        if not r:
            raise SystemExit(f"⛔ 주장 #{cid} 없음")
        if r["verdict"] != "PENDING":
            raise SystemExit(f"⛔ 주장 #{cid}은 PENDING이 아니다({r['verdict']}) — 쟁점은 판정 대기 주장만 묶는다")
        if r["issue_id"] not in (None, issue_id):
            raise SystemExit(f"⛔ 주장 #{cid}은 이미 쟁점 #{r['issue_id']}에 묶여 있다")
        con.execute("UPDATE video_impl_claims SET issue_id=? WHERE id=?", (issue_id, cid))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--due", action="store_true")
    ap.add_argument("--load")
    ap.add_argument("--attach", nargs="+", type=int, metavar="N")
    ap.add_argument("--close", type=int)
    ap.add_argument("--verdict", choices=("APPLIED", "HELD", "REJECTED"))
    ap.add_argument("--note")
    a = ap.parse_args()
    con = connect_db(DB)
    con.row_factory = sqlite3.Row
    if a.load:
        con.execute("BEGIN IMMEDIATE")
        specs = json.loads(Path(a.load).read_text(encoding="utf-8"))["issues"]
        for s in specs:
            iid = insert_issue(con, s, f"scripts/claim_issues.py --load {Path(a.load).name}, {TODAY}")
            attach(con, iid, s.get("claim_ids", []))
        con.commit()
        print(f"쟁점 {len(specs)}개 생성 · 주장 {sum(len(s.get('claim_ids', [])) for s in specs)}행 연결")
    elif a.attach:
        con.execute("BEGIN IMMEDIATE")
        attach(con, a.attach[0], a.attach[1:])
        con.commit()
        print(f"쟁점 #{a.attach[0]}에 주장 {len(a.attach) - 1}행 연결")
    elif a.close:
        if not (a.verdict and (a.note or "").strip()):
            raise SystemExit("⛔ --close는 --verdict와 --note(실측 근거)가 필수다")
        con.execute("BEGIN IMMEDIATE")
        r = con.execute("SELECT * FROM claim_issues WHERE id=? AND status='open'", (a.close,)).fetchone()
        if not r:
            raise SystemExit(f"⛔ 열린 쟁점 #{a.close}이 없다")
        if not progress(con, r)["due"]:
            print(f"⚠️ 트리거 전 판정이다({trigger_kr(con, r)}) — 실측이 이미 결정적일 때만 쓴다")
        con.execute("UPDATE claim_issues SET status='closed', resolution=?, resolution_note=?, closed=? WHERE id=?",
                    (a.verdict, a.note, TODAY, a.close))
        tag = f" [쟁점 #{a.close} 판정 {TODAY} → {a.verdict}] {a.note}"
        n = con.execute("""UPDATE video_impl_claims SET verdict=?, verdict_note=COALESCE(verdict_note,'')||?
                           WHERE issue_id=? AND verdict='PENDING'""", (a.verdict, tag, a.close)).rowcount
        con.commit()
        print(f"쟁점 #{a.close} 「{r['title_kr']}」 → {a.verdict} · 주장 {n}행 갱신")
    else:
        show(con, a.due)


if __name__ == "__main__":
    main()
