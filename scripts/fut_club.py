#!/usr/bin/env python3
"""내 얼티밋 구단 원장 — 계정·보유 선수·진화 적용 기록 (2026-09-17 신설, migration 036).

왜 (사용자 지시 「내 얼티밋 계정에서 내 구단의 선수들이 어떻게 진화를 적용하고 발전해가는지 기록해나갈거야」):
  페이지는 export 산출물만 읽는다(불변규칙 1 — 손편집 지점 0). 그래서 「내가 오늘 이 선수에게 이 진화를 적용했다」는
  사실은 이 CLI로 DB에 넣고 export가 화면에 내보낸다. ⛔ EA 구단 자동 수집은 승인 파트너(FC Community API) 전용이라
  없다 — 이 원장이 정본이고, 나중에 GG Club 세션 임포터가 붙어도 여기로 들어온다.

  스탯 변화는 **발명하지 않는다**: 적용 후 상태는 `player_evolutions.path_json`(fut.gg가 계산한 단계별 결과 카드)에서
  가져오고, 그 경로가 없으면 `--ovr-after/--six-after`를 사용자가 직접 넘겨야 한다.

사용:
    python3 scripts/fut_club.py account add main --platform PS5 --game FC27
    python3 scripts/fut_club.py player add --account main --name 보가르드 --player-id 11 --ea-item 264209 --acquired 2026-09-26 --how 팩
    python3 scripts/fut_club.py evolve --account main --player 보가르드 --evo 2493 [--level 1] [--date 2026-09-26] [--note …]
    python3 scripts/fut_club.py import /tmp/club.json --account main --source "gg-club 2026-09-26"
    python3 scripts/fut_club.py list --account main
"""
import argparse
import datetime as dt
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                     # noqa: E402

TODAY = dt.date.today().isoformat()


def account(con, name):
    r = con.execute("SELECT * FROM fut_accounts WHERE name=?", (name,)).fetchone()
    if not r:
        raise SystemExit(f"⛔ 계정 '{name}' 없음 — `account add {name}` 먼저")
    return r


def club_player(con, acc_id, key):
    rows = con.execute("SELECT * FROM fut_club_players WHERE account_id=? AND (id=? OR name=?) AND status='owned'",
                       (acc_id, key if str(key).isdigit() else -1, key)).fetchall()
    if len(rows) != 1:
        sys.exit(f"⛔ 보유 선수 '{key}' 특정 실패({len(rows)}건) — id로 지정할 것")
    return rows[0]


def cmd_account(con, a):
    con.execute("INSERT INTO fut_accounts(name, platform, game_version, notes, created) VALUES(?,?,?,?,?)",
                (a.name, a.platform, a.game, a.notes, TODAY))
    print(f"계정 등록: {a.name} ({a.platform or '-'}, {a.game})")


def cmd_player_add(con, a):
    acc = account(con, a.account)
    cur = {}
    if a.ea_item:
        c = con.execute("SELECT * FROM player_card_items WHERE ea_item_id=? AND game_version=?", (a.ea_item, acc["game_version"])).fetchone()
        if c:
            cur = dict(current_ovr=c["ovr"], current_playstyles=c["playstyles"],
                       current_roles_plus=c["roles_plus"], current_roles_plus_plus=c["roles_plus_plus"],
                       current_six=json.dumps({"PAC": c["pac"], "SHO": c["sho"], "PAS": c["pas"],
                                               "DRI": c["dri"], "DEF": c["def"], "PHY": c["phy"]}))
            if not a.player_id:
                a.player_id = c["player_id"]
    con.execute("""INSERT INTO fut_club_players(account_id, player_id, ea_item_id, name, acquired, acquired_how, status,
                     current_ovr, current_six, current_playstyles, current_roles_plus, current_roles_plus_plus, notes, updated)
                   VALUES(?,?,?,?,?,?,'owned',?,?,?,?,?,?,?)""",
                (acc["id"], a.player_id, a.ea_item, a.name, a.acquired, a.how,
                 cur.get("current_ovr"), cur.get("current_six"), cur.get("current_playstyles"),
                 cur.get("current_roles_plus"), cur.get("current_roles_plus_plus"), a.notes, TODAY))
    print(f"보유 등록: {a.name} (player_id={a.player_id}, item={a.ea_item}, OVR {cur.get('current_ovr', '미상')})")


def cmd_evolve(con, a):
    acc = account(con, a.account)
    cp = club_player(con, acc["id"], a.player)
    # 적용 후 상태 — 그 선수의 진화 경로(path_json)에서 이 진화 id가 만드는 단계를 찾는다
    after, evo_name = None, None
    if cp["player_id"]:
        for pe in con.execute("""SELECT evolution_ids, evolution_names, path_json FROM player_evolutions
                                 WHERE player_id=? AND game_version=? ORDER BY steps""", (cp["player_id"], acc["game_version"])):
            ids = json.loads(pe["evolution_ids"])
            if a.evo in ids and pe["path_json"]:
                step = json.loads(pe["path_json"])[ids.index(a.evo) + 1]     # path_json[0]은 적용 전 기준 카드
                after = step
                evo_name = pe["evolution_names"].split(" → ")[ids.index(a.evo)]
                break
    if evo_name is None:
        r = con.execute("SELECT name FROM fc_evolutions WHERE evo_id=? ORDER BY pulled DESC", (a.evo,)).fetchone()
        evo_name = r["name"] if r else f"evo#{a.evo}"
    ovr_after = a.ovr_after or (after or {}).get("ovr")
    six_after = a.six_after or (json.dumps(after["six"]) if after else None)
    if ovr_after is None:
        sys.exit("⛔ 적용 후 OVR을 알 수 없다 — 이 선수·진화의 path_json이 없으니 --ovr-after/--six-after를 직접 넘길 것")
    src = ("player_evolutions.path_json (fut.gg 계산 결과 카드)" if after else "사용자 입력값")
    con.execute("""INSERT INTO fut_evolution_log(club_player_id, evo_id, evo_name, level, applied_at, completed_at,
                     ovr_before, ovr_after, six_before, six_after, playstyles_after, roles_plus_after, roles_plus_plus_after,
                     source, confidence, notes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (cp["id"], a.evo, evo_name, a.level, a.date, a.completed, cp["current_ovr"], ovr_after, cp["current_six"], six_after,
                 json.dumps((after or {}).get("playstyles"), ensure_ascii=False) if after else None,
                 json.dumps((after or {}).get("roles_plus")) if after else None,
                 json.dumps((after or {}).get("roles_plus_plus")) if after else None,
                 f"scripts/fut_club.py evolve ({TODAY} 기록) · 적용 후 값 출처: {src}",
                 "MEASURED(사용자 행위) — 적용 사실은 사용자 보고. 적용 후 스탯은 " + src + ".", a.note))
    con.execute("""UPDATE fut_club_players SET current_ovr=?, current_six=?, current_playstyles=COALESCE(?, current_playstyles),
                     current_roles_plus=COALESCE(?, current_roles_plus), current_roles_plus_plus=COALESCE(?, current_roles_plus_plus),
                     evo_count=evo_count+1, updated=? WHERE id=?""",
                (ovr_after, six_after,
                 ", ".join(after["playstyles"]) if after and after.get("playstyles") else None,
                 json.dumps(after["roles_plus"]) if after else None, json.dumps(after["roles_plus_plus"]) if after else None,
                 TODAY, cp["id"]))
    print(f"진화 기록: {cp['name']} ← {evo_name} (lv{a.level}) OVR {cp['current_ovr']} → {ovr_after} · 적용일 {a.date}")


def cmd_player_set(con, a):
    acc = account(con, a.account)
    rows = con.execute("SELECT * FROM fut_club_players WHERE account_id=? AND (id=? OR name=?)",
                       (acc["id"], a.player if str(a.player).isdigit() else -1, a.player)).fetchall()
    if len(rows) != 1:
        sys.exit(f"⛔ 보유 선수 '{a.player}' 특정 실패({len(rows)}건)")
    con.execute("UPDATE fut_club_players SET status=COALESCE(?, status), notes=COALESCE(?, notes), updated=? WHERE id=?",
                (a.status, a.notes, TODAY, rows[0]["id"]))
    print(f"갱신: {rows[0]['name']} status={a.status or rows[0]['status']}")


def cmd_import(con, a):
    """JSON 목록 → 보유 선수 일괄 등록 (GG Club/웹앱에서 사용자가 받아 온 목록의 적재 경로 — 자동 수집은 아니다).
    형식: [{"name": "...", "ea_item_id": 264209, "acquired": "2026-09-26", "how": "팩"}, ...]
    ea_item_id가 player_card_items에 있으면 player_id·현재 스탯을 자동으로 붙인다. 이미 있는 (account, ea_item_id)는 건너뛴다."""
    acc = account(con, a.account)
    items = json.load(open(a.path, encoding="utf-8"))
    have = {r[0] for r in con.execute("SELECT ea_item_id FROM fut_club_players WHERE account_id=?", (acc["id"],))}
    ins = skip = 0
    for it in items:
        if it.get("ea_item_id") in have:
            skip += 1; continue
        ns = argparse.Namespace(account=a.account, name=it["name"], player_id=it.get("player_id"), ea_item=it.get("ea_item_id"),
                                acquired=it.get("acquired"), how=it.get("how") or a.how, notes=it.get("notes") or f"import {TODAY} ({a.source})")
        cmd_player_add(con, ns); ins += 1
    print(f"임포트 {ins}명 · 기존 {skip}명 건너뜀 (출처: {a.source})")


def run(con, cmd, **kw):
    """serve.py 쓰기 API용 진입점 — CLI와 같은 함수를 같은 규약으로 실행한다(발명 금지·출처 기록 동일)."""
    defaults = dict(platform=None, game="FC27", notes=None, player_id=None, ea_item=None, acquired=None, how=None,
                    level=1, date=TODAY, completed=None, note=None, ovr_after=None, six_after=None, status=None, op="add")
    a = argparse.Namespace(**{**defaults, **kw})
    fn = {"account": cmd_account, "player": cmd_player_add, "player_set": cmd_player_set, "evolve": cmd_evolve}[cmd]
    fn(con, a)


def cmd_list(con, a):
    acc = account(con, a.account)
    for cp in con.execute("SELECT * FROM fut_club_players WHERE account_id=? ORDER BY status, name", (acc["id"],)):
        logs = con.execute("SELECT evo_name, ovr_before, ovr_after, applied_at FROM fut_evolution_log WHERE club_player_id=? ORDER BY applied_at", (cp["id"],)).fetchall()
        print(f"[{cp['id']}] {cp['name']:<14} {cp['status']:<9} OVR {cp['current_ovr'] or '-'}  진화 {cp['evo_count']}회"
              + "".join(f"\n      {l['applied_at']} {l['evo_name']} {l['ovr_before']}→{l['ovr_after']}" for l in logs))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("account"); s.add_argument("op", choices=["add"]); s.add_argument("name")
    s.add_argument("--platform"); s.add_argument("--game", default="FC27"); s.add_argument("--notes")
    s = sub.add_parser("player"); s.add_argument("op", choices=["add"]); s.add_argument("--account", required=True)
    s.add_argument("--name", required=True); s.add_argument("--player-id", type=int); s.add_argument("--ea-item", type=int)
    s.add_argument("--acquired"); s.add_argument("--how"); s.add_argument("--notes")
    s = sub.add_parser("evolve"); s.add_argument("--account", required=True); s.add_argument("--player", required=True)
    s.add_argument("--evo", type=int, required=True); s.add_argument("--level", type=int, default=1)
    s.add_argument("--date", default=TODAY); s.add_argument("--completed"); s.add_argument("--note")
    s.add_argument("--ovr-after", type=int); s.add_argument("--six-after", help='JSON {"PAC":..}')
    s = sub.add_parser("player-set"); s.add_argument("--account", required=True); s.add_argument("--player", required=True)
    s.add_argument("--status", choices=["owned", "sold", "discarded"]); s.add_argument("--notes")
    s = sub.add_parser("import"); s.add_argument("path"); s.add_argument("--account", required=True)
    s.add_argument("--source", default="manual", help="목록 출처 표기(예: gg-club 2026-09-26 · webapp-club-page)"); s.add_argument("--how")
    s = sub.add_parser("list"); s.add_argument("--account", required=True)
    a = ap.parse_args()
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    {"account": cmd_account, "player": cmd_player_add, "player-set": cmd_player_set, "evolve": cmd_evolve,
     "import": cmd_import, "list": cmd_list}[a.cmd](con, a)
    con.commit()
    if a.cmd != "list":
        print("다음: python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
