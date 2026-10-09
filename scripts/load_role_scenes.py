"""역할 장면 해설 적재 — db/seeds/role-scenes-{GV}.json → game_roles·game_role_focus·game_role_groups (migration 103).

⛔ 빈 칸만 채운다(불변규칙 2). 이미 값이 있는데 시드와 다르면 덮지 않고 보고한다.
   해설을 고치려면 시드를 고친 뒤 해당 칸을 사람이 비우고 다시 돌린다.

    python3 scripts/load_role_scenes.py [--gv FC26] [--dry-run]
"""
import argparse
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "tactics.db"


def fill(con, table, keys, cols, vals, stats):
    where = " AND ".join(f"{k}=?" for k in keys)
    cur = con.execute(f"SELECT {', '.join(cols)} FROM {table} WHERE {where}", list(keys.values())).fetchone()
    if cur is None:
        stats["missing"].append(f"{table} {dict(keys)}")
        return
    for c, old, new in zip(cols, cur, vals):
        if old is None:
            con.execute(f"UPDATE {table} SET {c}=? WHERE {where}", [new, *keys.values()])
            stats["filled"] += 1
        elif old != new:
            stats["conflict"].append(f"{table}.{c} {dict(keys)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gv", default="FC26")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    seed = json.loads((ROOT / "db" / "seeds" / f"role-scenes-{a.gv}.json").read_text())
    gv = seed["game_version"]
    con = sqlite3.connect(DB)
    stats = {"filled": 0, "conflict": [], "missing": [], "groups": 0}

    # 시드가 DB 역할·포커스를 빠짐없이 덮는가(양방향)
    db_pairs = set(con.execute("SELECT role_id, focus FROM game_role_focus WHERE game_version=?", (gv,)))
    seed_pairs = {(r, f) for r, v in seed["roles"].items() for f in v["focus"]}
    for p in sorted(db_pairs - seed_pairs):
        stats["missing"].append(f"시드에 없음 {p}")
    for p in sorted(seed_pairs - db_pairs):
        stats["missing"].append(f"DB에 없음 {p}")

    for pt, g in seed["groups"].items():
        n = con.execute("INSERT OR IGNORE INTO game_role_groups VALUES(?,?,?,?,?,?,?)",
                        (gv, pt, g["scene_attack"], g["scene_defend"], g["compare"],
                         seed["source"], seed["confidence"])).rowcount
        stats["groups"] += n
    for rid, r in seed["roles"].items():
        fill(con, "game_roles", {"game_version": gv, "role_id": rid},
             ["identity_kr", "focus_axis_kr"], [r["identity"], r["focus_axis"]], stats)
        for f, (atk, dfn) in r["focus"].items():
            fill(con, "game_role_focus", {"game_version": gv, "role_id": rid, "focus": f},
                 ["scene_attack_kr", "scene_defend_kr"], [atk, dfn], stats)

    print(f"{gv}: 군 {stats['groups']}행 추가 · 칸 {stats['filled']}개 채움 · "
          f"덮지 않은 충돌 {len(stats['conflict'])} · 짝 결손 {len(stats['missing'])}")
    for x in stats["conflict"] + stats["missing"]:
        print("  ⚠️", x)
    if a.dry_run:
        con.rollback()
        print("(dry-run — 쓰지 않았다)")
    else:
        con.commit()
    return 1 if stats["missing"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
