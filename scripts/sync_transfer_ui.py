#!/usr/bin/env python3
"""Regenerate the AUTOGEN blocks in fc26-heatmap.html from data/avl_analysis.db.

Run this after any transfer_targets/transfer_outgoing change (transfer-watch
runs, manual DB edits), before scripts/db_dump.sh + commit. See docs/40-pipeline.md.

Rewrites two blocks only, between marker comments:
  AUTOGEN:TRANSFER_TARGETS   <- transfer_targets rows (window=2026-summer, likelihood != 'OWNED')
  AUTOGEN:TRANSFER_OUTGOING  <- transfer_outgoing rows joined with players.name

Everything else in the file (SQUAD_SLOTS owned-player opts, PLAYER_BEST for
nailed-on starters, XI_POOL owned rows, etc.) is untouched — incoming-candidate
entries for those three are derived at runtime from TRANSFER_TARGETS by
injectTransferCandidates() (see fc26-heatmap.html), not generated here.
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "avl_analysis.db"
HTML = ROOT / "fc26-heatmap.html"
WINDOW = "2026-summer"


def js_obj(fields):
    """Render an ordered dict of Python values as a compact JS object literal.
    None -> JS null (valid JS, keeps falsy semantics for e.g. `if(row.map25)`)."""
    parts = [f"{k}:{json.dumps(v, ensure_ascii=False)}" for k, v in fields.items()]
    return "{" + ",".join(parts) + "}"


def gen_transfer_targets(conn):
    rows = conn.execute(
        """SELECT name,name_kr,slot,club,position,likelihood,confidence,
                  fit_sim,opt_role,opt_focus,fit_role,fit_focus,source,
                  map25,tool_x,tool_y,sample_n,avg_rating,short_label
           FROM transfer_targets
           WHERE window=? AND likelihood!='OWNED'
           ORDER BY id""",
        (WINDOW,),
    ).fetchall()
    lines = []
    for row in rows:
        r = dict(row)
        obj = js_obj(
            {
                "name": r["name"],
                "name_kr": r["name_kr"],
                "slot": r["slot"],
                "club": r["club"],
                "position": r["position"],
                "likelihood": r["likelihood"],
                "confidence": r["confidence"],
                "fit_sim": r["fit_sim"],
                "opt_role": r["opt_role"],
                "opt_focus": r["opt_focus"],
                "fit_role": r["fit_role"],
                "fit_focus": r["fit_focus"],
                "source": r["source"],
                "map25": r["map25"],
                "avg_rating": r["avg_rating"],
                "sample_n": r["sample_n"],
                "short_label": r["short_label"],
            }
        )
        lines.append(obj + ",")
    return "const TRANSFER_TARGETS=[\n" + "\n".join(lines) + "\n];", len(rows)


def gen_transfer_outgoing(conn):
    rows = conn.execute(
        """SELECT p.name,t.dest_club,t.likelihood,t.confidence,t.source
           FROM transfer_outgoing t JOIN players p ON p.id=t.player_id
           WHERE t.window=?
           ORDER BY t.player_id""",
        (WINDOW,),
    ).fetchall()
    lines = []
    for name, dest_club, likelihood, confidence, source in rows:
        obj = js_obj(
            {
                "player": name,
                "dest_club": dest_club,
                "likelihood": likelihood,
                "confidence": confidence,
                "source": source,
            }
        )
        lines.append(obj + ",")
    return "const TRANSFER_OUTGOING=[\n" + "\n".join(lines) + "\n];", len(rows)


def gen_transfer_ledger(conn):
    rows = conn.execute(
        """SELECT kind,label,amount_m,note,confidence
           FROM transfer_ledger WHERE window=?
           ORDER BY CASE kind WHEN 'in' THEN 0 WHEN 'deduct' THEN 1 WHEN 'out' THEN 2 ELSE 3 END,
                    amount_m DESC""",
        (WINDOW,),
    ).fetchall()
    lines = []
    for r in rows:
        obj = js_obj(
            {
                "kind": r["kind"],
                "label": r["label"],
                "amount": r["amount_m"],
                "note": r["note"],
                "confidence": r["confidence"],
            }
        )
        lines.append(obj + ",")
    return "const TRANSFER_LEDGER=[\n" + "\n".join(lines) + "\n];", len(rows)


def replace_block(html, marker, new_body):
    start = f"/* AUTOGEN:{marker}:START */"
    end = f"/* AUTOGEN:{marker}:END */"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(html):
        sys.exit(f"marker block {marker} not found in {HTML}")
    replacement = f"{start}\n{new_body}\n{end}"
    return pattern.sub(lambda _m: replacement, html, count=1)


def main():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    html = HTML.read_text(encoding="utf-8")
    targets_body, n_targets = gen_transfer_targets(conn)
    outgoing_body, n_outgoing = gen_transfer_outgoing(conn)
    ledger_body, n_ledger = gen_transfer_ledger(conn)
    html = replace_block(html, "TRANSFER_TARGETS", targets_body)
    html = replace_block(html, "TRANSFER_OUTGOING", outgoing_body)
    html = replace_block(html, "TRANSFER_LEDGER", ledger_body)
    HTML.write_text(html, encoding="utf-8")
    print(f"synced {n_targets} TRANSFER_TARGETS + {n_outgoing} TRANSFER_OUTGOING + {n_ledger} TRANSFER_LEDGER rows into {HTML.name}")


if __name__ == "__main__":
    main()
