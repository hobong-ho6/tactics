#!/usr/bin/env python3
"""GG Club 역할 숙련 신규/갱신 회귀 검사."""
import contextlib
import io
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

import fut_club_sync as sync


def main():
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "club.db"
        payload = Path(tmp) / "ggclub.json"
        con = sqlite3.connect(db)
        con.executescript("""
            CREATE TABLE fut_accounts(id INTEGER PRIMARY KEY, name TEXT);
            CREATE TABLE fc_chemistry_styles(ea_id INTEGER, name TEXT);
            CREATE TABLE player_card_items(ea_item_id INTEGER, player_id INTEGER,
                name_kr TEXT, best_pos TEXT, game_version TEXT);
            CREATE TABLE fut_evolution_log(club_player_id INTEGER, is_void INTEGER,
                evo_name TEXT, ovr_after INTEGER, completed_at TEXT,
                confidence TEXT, applied_at TEXT);
            CREATE TABLE fut_club_players(
                id INTEGER PRIMARY KEY, account_id INTEGER, player_id INTEGER,
                ea_item_id INTEGER, name TEXT, acquired TEXT, acquired_how TEXT,
                status TEXT DEFAULT 'owned', current_ovr INTEGER, current_six TEXT,
                current_attrs TEXT, current_roles_plus TEXT, current_roles_plus_plus TEXT,
                chem_style_ea INTEGER, chem_points INTEGER, gg_player_id TEXT,
                synced_at TEXT, notes TEXT, updated TEXT, evo_count INTEGER DEFAULT 0);
            INSERT INTO fut_accounts VALUES(1, 'main');
            INSERT INTO fut_club_players(account_id, ea_item_id, name, status,
                current_ovr, current_six, current_roles_plus, current_roles_plus_plus,
                updated, chem_points) VALUES(1, 101, '기존', 'owned', 80,
                '{"PAC": 80, "SHO": 70, "PAS": 70, "DRI": 70, "DEF": 70, "PHY": 70}',
                '[5]', '[]', '2026-09-01', 0);
        """)
        con.commit()
        con.close()
        six = [80, 70, 70, 70, 70, 70]
        payload.write_text(json.dumps([
            {"ea": 101, "n": "기존", "ovr": 80, "six": six, "cp": 0,
             "rp": [5], "rpp": [7]},
            {"ea": 102, "n": "신규", "ovr": 80, "six": six, "cp": 0,
             "attrs": {"pace": 80}, "rp": [5], "rpp": [7]},
        ]), encoding="utf-8")
        old_db, old_argv = sync.DB, sys.argv
        try:
            sync.DB = db
            sys.argv = ["fut_club_sync.py", str(payload), "--account", "main"]
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                sync.main()
        finally:
            sync.DB, sys.argv = old_db, old_argv
        assert "신규 1 · 갱신 1" in out.getvalue(), out.getvalue()
        con = sqlite3.connect(db)
        rows = con.execute("""SELECT ea_item_id, current_attrs, current_roles_plus,
                                    current_roles_plus_plus, updated
                             FROM fut_club_players ORDER BY ea_item_id""").fetchall()
        con.close()
        assert rows[0][3] == "[7]" and rows[0][4] == sync.TODAY, rows[0]
        assert json.loads(rows[1][1]) == {"pace": 80}, rows[1]
        assert rows[1][2:4] == ("[5]", "[7]"), rows[1]
    print("GG Club 신규 속성·역할 숙련 / Role++ 단독 변경: ✅")


if __name__ == "__main__":
    main()
