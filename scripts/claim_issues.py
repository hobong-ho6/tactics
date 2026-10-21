#!/usr/bin/env python3
"""판정 쟁점 관리 — 영상 구현 주장을 쟁점 단위로 열고·세고·판정하고·감시한다 (2026-10-21 · migration 114·115).

왜: 판정 조건·재판정 조건이 산문에만 있어 PENDING 165건·HELD 185건이 아무도 다시 보지 않은 채 쌓였다
  (사용자 「판정대기는 언제 판정완료되는거야?」 · 「보류 판정도 이후에 업데이트 되는거야?」).
  트리거 판정 정본은 core/claim_issues.py — 여기는 그걸 부르는 손잡이다. G39가 기한 초과·미연결을 막는다.

단계:
  decide(판정 대기) — 묶인 주장 PENDING · 트리거 = 판정 조건
  watch(감시)       — HELD로 판정한 뒤 · 묶인 주장 HELD · 트리거 = 재판정 조건
  closed            — APPLIED·REJECTED, 또는 HELD --final(재판정 조건 없음 · 사유 필수)

사용:
    python3 scripts/claim_issues.py                 # 열린 쟁점 + 진행도
    python3 scripts/claim_issues.py --due           # 판정·재판정할 차례만 + 묶인 주장
    python3 scripts/claim_issues.py --load F.json   # {"issues":[{…spec…, "claim_ids":[…]}]} 판정 대기 쟁점 생성
    python3 scripts/claim_issues.py --apply-watch F.json   # {"rearm":[…], "issues":[…], "attach":[…]} 감시 쟁점 일괄
    python3 scripts/claim_issues.py --attach ISSUE CLAIM_ID…
    python3 scripts/claim_issues.py --close ISSUE --verdict REJECTED --note "실측 근거…"         # 종결
    python3 scripts/claim_issues.py --close ISSUE --verdict HELD --note "…" --w-kind matches --w-n 5 --w-comp league --w-since 2026-10-21
        → 정본 유지 + 재판정 트리거(감시 단계로 남는다) · 감시 중인 쟁점이면 같은 명령으로 다시 건다
    python3 scripts/claim_issues.py --close ISSUE --verdict HELD --final --note "재판정 조건이 없는 이유"
    python3 scripts/claim_issues.py --close-claims CLAIM_ID… --verdict REJECTED|HELD --final --note "조건 소멸·이미 충족 사유"
        → 쟁점 전체가 아니라 주장 몇 개만 종결(종결 쟁점으로 떼어 낸다)
    python3 scripts/claim_issues.py --extend ISSUE --since 2026-10-21 --n 3 --note "아직 결정적이지 않은 이유·수치"   # 판정 대기만
⛔ 판정(--close)은 사람이 실측을 보고 내린다 — 이 스크립트는 판정을 만들지 않는다. 정본을 바꾸는 APPLIED는 사용자 승인 후.
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
from core.claim_issues import progress, trigger_kr, insert_issue, overdue, arm_watch   # noqa: E402

TODAY = dt.date.today().isoformat()
CLAIM_VERDICT = {"decide": "PENDING", "watch": "HELD"}     # 단계별로 묶이는 주장의 판정


def show(con, only_due):
    rows = con.execute("SELECT * FROM claim_issues WHERE status='open' ORDER BY hold, phase, team_code, id").fetchall()
    n_due = {"decide": 0, "watch": 0}
    for r in rows:
        p = progress(con, r)
        if only_due and not p["due"]:
            continue
        n_due[r["phase"]] += p["due"]
        cl = con.execute("SELECT id FROM video_impl_claims WHERE issue_id=? AND verdict=?",
                         (r["id"], CLAIM_VERDICT[r["phase"]])).fetchall()
        what = "재판정할 차례" if r["phase"] == "watch" else "판정할 차례"
        flag = "⛔ 기한 초과" if overdue(con, r) else (f"⭐ {what}" if p["due"] else "")
        tag = "유지·감시" if r["phase"] == "watch" else "판정 대기"
        print(f"#{r['id']:<3} {r['team_code']}{' [보류]' if r['hold'] else ''} [{tag}] {r['title_kr']} — "
              f"{trigger_kr(con, r)} · 주장 {len(cl)} {flag}")
        if only_due:
            print(f"     질문: {r['question_kr']}\n     실측: {r['measure_kr']}\n     주장: {', '.join(str(c['id']) for c in cl)}")
    print(f"\n열린 쟁점 {len(rows)} · 판정할 차례 {n_due['decide']} · 재판정할 차례 {n_due['watch']}")


def attach(con, issue_id, claim_ids):
    r = con.execute("SELECT phase FROM claim_issues WHERE id=? AND status='open'", (issue_id,)).fetchone()
    if not r:
        raise SystemExit(f"⛔ 열린 쟁점 #{issue_id}이 없다")
    want = CLAIM_VERDICT[r["phase"]]
    for cid in claim_ids:
        c = con.execute("SELECT verdict, issue_id FROM video_impl_claims WHERE id=?", (cid,)).fetchone()
        if not c:
            raise SystemExit(f"⛔ 주장 #{cid} 없음")
        if c["verdict"] != want:
            raise SystemExit(f"⛔ 주장 #{cid}은 {c['verdict']}다 — {r['phase']} 쟁점은 {want} 주장만 묶는다")
        if c["issue_id"] not in (None, issue_id):
            raise SystemExit(f"⛔ 주장 #{cid}은 이미 쟁점 #{c['issue_id']}에 묶여 있다")
        con.execute("UPDATE video_impl_claims SET issue_id=? WHERE id=?", (issue_id, cid))


def watch_trigger(a):
    return {k: v for k, v in {"trigger_kind": a.w_kind, "trigger_n": a.w_n, "trigger_comp": a.w_comp,
                              "trigger_player": a.w_player, "trigger_pos": a.w_pos, "trigger_date": a.w_date,
                              "since": a.w_since, "measure_kr": a.w_measure}.items() if v is not None}


def close(con, a):
    r = con.execute("SELECT * FROM claim_issues WHERE id=?", (a.close,)).fetchone()
    if not r:
        raise SystemExit(f"⛔ 쟁점 #{a.close} 없음")
    reopen = r["status"] == "closed" and r["resolution"] == "HELD" and a.verdict == "HELD" and a.w_kind
    if r["status"] != "open" and not reopen:
        raise SystemExit(f"⛔ 쟁점 #{a.close}은 이미 닫혔다({r['resolution']})")
    if not progress(con, r)["due"] and r["status"] == "open":
        print(f"⚠️ 트리거 전 판정이다({trigger_kr(con, r)}) — 실측이 이미 결정적일 때만 쓴다")
    tag = f" [쟁점 #{a.close} {'재판정' if r['phase'] == 'watch' else '판정'} {TODAY} → {a.verdict}] {a.note}"
    targets = ("PENDING", "HELD")
    if a.verdict == "HELD" and not a.final:
        if not a.w_kind:
            raise SystemExit("⛔ HELD는 재판정 트리거(--w-kind …)가 필수다 — 재판정 조건이 정말 없으면 --final과 사유")
        arm_watch(con, a.close, watch_trigger(a), a.note, TODAY)
        n = con.execute(f"""UPDATE video_impl_claims SET verdict='HELD', verdict_note=COALESCE(verdict_note,'')||?
                            WHERE issue_id=? AND verdict IN ({','.join('?' * len(targets))})""",
                        (tag, a.close, *targets)).rowcount
        r2 = con.execute("SELECT * FROM claim_issues WHERE id=?", (a.close,)).fetchone()
        return f"쟁점 #{a.close} 「{r['title_kr']}」 → 유지 · 감시 {trigger_kr(con, r2)} · 주장 {n}행"
    con.execute("UPDATE claim_issues SET status='closed', resolution=?, resolution_note=COALESCE(resolution_note||' · ','')||?, closed=? WHERE id=?",
                (a.verdict, f"[{a.verdict}{' final' if a.final else ''} {TODAY}] {a.note}", TODAY, a.close))
    n = con.execute(f"""UPDATE video_impl_claims SET verdict=?, verdict_note=COALESCE(verdict_note,'')||?
                        WHERE issue_id=? AND verdict IN ({','.join('?' * len(targets))})""",
                    (a.verdict, tag, a.close, *targets)).rowcount
    return f"쟁점 #{a.close} 「{r['title_kr']}」 → {a.verdict}{' (종결)' if a.final else ''} · 주장 {n}행"


def close_claims(con, a):
    """주장 몇 개만 종결 — 원 쟁점에서 떼어 종결 쟁점 1행(trigger date=오늘)에 묶고 닫는다(이력은 양쪽에 남는다).
    ⛔ 원 쟁점의 마지막 주장이면 거부한다 — 그때는 쟁점 자체를 --close한다."""
    if not (a.verdict and (a.note or "").strip()):
        raise SystemExit("⛔ --close-claims는 --verdict와 --note(사유)가 필수다")
    if a.verdict == "HELD" and not a.final:
        raise SystemExit("⛔ 주장 단위 HELD 종결은 --final(재판정 조건이 없는 이유)만 허용 — 감시를 이어갈 거면 쟁점에 남겨 둔다")
    rows = [con.execute("SELECT * FROM video_impl_claims WHERE id=?", (c,)).fetchone() for c in a.close_claims]
    if not all(rows):
        raise SystemExit("⛔ 없는 주장 id가 있다")
    src = {r["issue_id"] for r in rows}
    if len(src) != 1 or None in src:
        raise SystemExit("⛔ 같은 쟁점에 묶인 주장만 한 번에 종결한다")
    parent = con.execute("SELECT * FROM claim_issues WHERE id=?", (src.pop(),)).fetchone()
    left = con.execute(f"SELECT COUNT(*) FROM video_impl_claims WHERE issue_id=? AND id NOT IN ({','.join('?' * len(rows))})",
                       (parent["id"], *a.close_claims)).fetchone()[0]
    if parent["status"] == "open" and left == 0:
        raise SystemExit(f"⛔ 쟁점 #{parent['id']}의 마지막 주장이다 — 쟁점 자체를 --close로 닫는다")
    ids = ", ".join(f"#{c}" for c in a.close_claims)
    iid = insert_issue(con, {"team_code": parent["team_code"], "title_kr": f"개별 종결 {ids} (쟁점 #{parent['id']}에서)"[:40],
                             "question_kr": f"쟁점 #{parent['id']} 「{parent['title_kr']}」에서 떼어 낸 주장 {ids}의 종결",
                             "measure_kr": a.note, "trigger_kind": "date", "trigger_date": TODAY},
                       f"scripts/claim_issues.py --close-claims, {TODAY}")
    con.execute("UPDATE claim_issues SET status='closed', resolution=?, resolution_note=?, closed=? WHERE id=?",
                (a.verdict, f"[{a.verdict}{' final' if a.final else ''} {TODAY}] {a.note}", TODAY, iid))
    tag = f" [쟁점 #{parent['id']}→#{iid} 개별 종결 {TODAY} → {a.verdict}] {a.note}"
    con.executemany("UPDATE video_impl_claims SET issue_id=?, verdict=?, verdict_note=COALESCE(verdict_note,'')||? WHERE id=?",
                    [(iid, a.verdict, tag, c) for c in a.close_claims])
    con.execute("UPDATE claim_issues SET source=COALESCE(source,'')||? WHERE id=?",
                (f" · [{TODAY} 주장 {ids} → 쟁점 #{iid}로 개별 종결({a.verdict})]", parent["id"]))
    return f"주장 {ids} → {a.verdict} 종결(쟁점 #{iid} · 원 쟁점 #{parent['id']} 남은 주장 {left})"


def apply_watch(con, path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    src = f"scripts/claim_issues.py --apply-watch {Path(path).name}, {TODAY}"
    for x in d.get("rearm", []):
        r = con.execute("SELECT status, resolution FROM claim_issues WHERE id=?", (x["issue_id"],)).fetchone()
        if not r or r["resolution"] != "HELD":
            raise SystemExit(f"⛔ rearm #{x['issue_id']}: HELD로 판정된 쟁점이 아니다")
        arm_watch(con, x["issue_id"], x, "기존 HELD 판정의 재판정 조건을 트리거로 옮김(migration 115 백필)", TODAY)
    for s in d.get("issues", []):
        iid = insert_issue(con, {**s, "phase": "watch",
                                 "resolution_note": "[유지] 기존 HELD 판정 묶음 — 재판정 조건을 트리거로 옮김(migration 115 백필)"}, src)
        attach(con, iid, s.get("claim_ids", []))
    for x in d.get("attach", []):
        attach(con, x["issue_id"], x["claim_ids"])
    return (f"감시 재설정 {len(d.get('rearm', []))} · 새 감시 쟁점 {len(d.get('issues', []))} · "
            f"기존 쟁점 연결 {sum(len(x['claim_ids']) for x in d.get('attach', []))}행")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--due", action="store_true")
    ap.add_argument("--load")
    ap.add_argument("--apply-watch")
    ap.add_argument("--attach", nargs="+", type=int, metavar="N")
    ap.add_argument("--close", type=int)
    ap.add_argument("--verdict", choices=("APPLIED", "HELD", "REJECTED"))
    ap.add_argument("--final", action="store_true", help="HELD 종결 — 재판정 조건 없음(사유를 --note에)")
    ap.add_argument("--note")
    for k in ("kind", "comp", "player", "pos", "date", "since", "measure"):
        ap.add_argument(f"--w-{k}")
    ap.add_argument("--w-n", type=int)
    ap.add_argument("--close-claims", nargs="+", type=int, metavar="CLAIM_ID",
                    help="쟁점 전체가 아니라 주장 몇 개만 종결(조건 소멸·이미 충족) — 종결 쟁점 1행으로 떼어 낸다")
    ap.add_argument("--extend", type=int, help="판정 대기 쟁점의 트리거를 다시 건다(--since·--n)")
    ap.add_argument("--since")
    ap.add_argument("--n", type=int)
    a = ap.parse_args()
    con = connect_db(DB)
    con.row_factory = sqlite3.Row
    if not any((a.load, a.apply_watch, a.attach, a.close, a.extend, a.close_claims)):
        return show(con, a.due)
    con.execute("BEGIN IMMEDIATE")
    if a.load:
        specs = json.loads(Path(a.load).read_text(encoding="utf-8"))["issues"]
        for s in specs:
            iid = insert_issue(con, s, f"scripts/claim_issues.py --load {Path(a.load).name}, {TODAY}")
            attach(con, iid, s.get("claim_ids", []))
        msg = f"쟁점 {len(specs)}개 생성 · 주장 {sum(len(s.get('claim_ids', [])) for s in specs)}행 연결"
    elif a.apply_watch:
        msg = apply_watch(con, a.apply_watch)
    elif a.attach:
        attach(con, a.attach[0], a.attach[1:])
        msg = f"쟁점 #{a.attach[0]}에 주장 {len(a.attach) - 1}행 연결"
    elif a.close_claims:
        msg = close_claims(con, a)
    elif a.extend:
        if not ((a.note or "").strip() and (a.since or a.n)):
            raise SystemExit("⛔ --extend는 --note(왜 아직 판정 못 하나 · 실측 수치)와 --since/--n이 필수다")
        r = con.execute("SELECT * FROM claim_issues WHERE id=? AND status='open' AND phase='decide'", (a.extend,)).fetchone()
        if not r or r["trigger_kind"] == "date":
            raise SystemExit(f"⛔ 연장할 수 있는 판정 대기(경기 트리거) 쟁점 #{a.extend}이 없다")
        log = f" · [연장 {TODAY}: since {r['since']}→{a.since or r['since']} · n {r['trigger_n']}→{a.n or r['trigger_n']} — {a.note}]"
        con.execute("UPDATE claim_issues SET since=?, trigger_n=?, armed=?, source=COALESCE(source,'')||? WHERE id=?",
                    (a.since or r["since"], a.n or r["trigger_n"], TODAY, log, a.extend))
        msg = f"쟁점 #{a.extend} 연장"
    else:
        if not (a.verdict and (a.note or "").strip()):
            raise SystemExit("⛔ --close는 --verdict와 --note(실측 근거)가 필수다")
        msg = close(con, a)
    con.commit()
    print(msg)


if __name__ == "__main__":
    main()
