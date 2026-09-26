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

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                     # noqa: E402
from core.futgg_attrs import apply_upgrades, face_of    # noqa: E402  ⭐ 진화 보상·6대 환산 정본

TODAY = dt.date.today().isoformat()


def account(con, name):
    r = con.execute("SELECT * FROM fut_accounts WHERE name=?", (name,)).fetchone()
    if not r:
        raise SystemExit(f"⛔ 계정 '{name}' 없음 — `account add {name}` 먼저")
    return r


def club_player(con, acc_id, key, expect_player_id=None):
    """보유 카드 한 장을 지목한다.

    ⛔⛔ **`key`는 `fut_club_players.id`다 — `players.id`가 아니다**(2026-09-26 사고).
       두 축의 id가 같은 번호 공간이라 **다른 사람의 카드에 조용히 기록된다**:
       마조의 players.id 61을 넘겼더니 fut_club_players.id 61인 **Helinho에 진화가 적혔다**.
       실측으로 이런 충돌이 **22쌍** 있다 — 우연이 아니라 구조적으로 터진다.
    ⇒ 호출부는 `expect_player_id`(= players.id)를 함께 넘겨 **찾은 카드가 그 선수의 것인지 확인**시킨다.
       어긋나면 멈춘다. ⛔ 「조심해서 넘기자」로 막지 않는다 — 읽는 사람이 있어야 작동한다(불변규칙 13)."""
    rows = con.execute("SELECT * FROM fut_club_players WHERE account_id=? AND (id=? OR name=?) AND status='owned'",
                       (acc_id, key if str(key).isdigit() else -1, key)).fetchall()
    if len(rows) != 1:
        sys.exit(f"⛔ 보유 선수 '{key}' 특정 실패({len(rows)}건) — id로 지정할 것")
    r = rows[0]
    if expect_player_id is not None and (r["player_id"] is None or int(r["player_id"]) != int(expect_player_id)):
        # ⛔⛔ `player_id IS NULL`도 **막는다**(2026-09-26 실측: 첫 판에 NULL을 통과시켜 가드가 무력했다).
        #    호출부가 기대를 밝혔는데 찾은 카드가 **누구 것인지 모른다**면 그건 통과시킬 근거가 아니라 멈출 이유다.
        sys.exit(f"⛔ 선수가 어긋난다 — 보유 카드 id {r['id']}는 '{r['name']}'"
                 f"(player_id={r['player_id'] if r['player_id'] is not None else '없음(우리 DB 미연결)'})인데 "
                 f"호출부는 player_id={expect_player_id}를 기대했다.\n"
                 f"   `player`에 **fut_club_players.id**를 넘겼는지 확인할 것(players.id가 아니다).")
    return r


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
    cp = club_player(con, acc["id"], a.player, getattr(a, "expect_player_id", None))
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
    # ⛔ 경로는 **기본 카드 기준**이다 — 이미 다른 진화를 밟은 카드에 그대로 쓰면 OVR이 거꾸로 내려간다
    #    (2026-09-19 실측: 마조 75 → 66). 경로의 출발 OVR이 현재와 다르면 값을 받아 쓰지 않는다.
    if after and cp["current_ovr"] is not None:
        base_ovr = json.loads(pe["path_json"])[0].get("ovr") if pe["path_json"] else None
        if base_ovr is not None and base_ovr != cp["current_ovr"]:
            print(f"⚠️ 경로 기준 카드 OVR {base_ovr} ≠ 현재 {cp['current_ovr']} — 이미 진화를 밟은 카드다. "
                  f"경로 값을 버리고 --ovr-after/--six-after를 쓴다.")
            after = None
    # ⭐⭐⭐ **적용 후 값은 서버가 `current_attrs`에서 계산한다**(2026-09-26 · 불변규칙 13 ①).
    #    ⛔ 종전엔 화면이 계산해 `--ovr-after/--six-after`로 보내고 서버는 **받아 적기만** 했다.
    #       그런데 원장에는 「현재 카드」가 **두 벌**(`current_six` · `current_attrs`) 있고 이 명령이
    #       **앞의 것만 갱신**했다. 화면은 before를 `current_six`에서, after를 `current_attrs`에서
    #       가져오므로 두 벌이 갈리는 순간 **after가 before보다 낮게** 적힌다.
    #       실증(마조 빛나는 스트라이커 1단계): PAC 75→**70** · SHO 73→**69**. 진화는 스탯을 내리지 않는다.
    #    ⇒ 이제 서버가 카탈로그 보상을 `current_attrs`에 얹어 **attrs·six·ovr 셋을 한꺼번에** 갱신한다.
    #       두 벌이 갈릴 수 있는 구조 자체가 없어진다. 화면이 보낸 숫자는 **대조용으로만** 본다.
    attrs_after = None
    cur_attrs = json.loads(cp["current_attrs"]) if cp["current_attrs"] else None
    lvrow = con.execute("SELECT levels FROM fc_evolutions WHERE evo_id=? ORDER BY pulled DESC",
                        (a.evo,)).fetchone()
    if cur_attrs and lvrow and lvrow["levels"]:
        step = next((x for x in json.loads(lvrow["levels"]) if x.get("idx") == a.level), None)
        if step is not None:
            ups = list(step.get("upgrades") or [])
            opts = step.get("upgradeOptions") or []
            if len(opts) > 1:
                pick = getattr(a, "pick", None)
                if pick is None:
                    sys.exit(f"⛔ {a.level}단계는 갈림길이다({len(opts)}갈래) — 어느 가지를 밟았는지 "
                             "`--pick N`(0부터)으로 밝혀야 한다. 지어내지 않는다.")
                o = opts[int(pick)]
                ups = list(o if isinstance(o, list) else (o.get("upgrades") or []))
            elif len(opts) == 1:
                o = opts[0]
                ups = list(o if isinstance(o, list) else (o.get("upgrades") or []))
            attrs_after = dict(cur_attrs)
            bump, unknown = apply_upgrades(attrs_after, ups)
            if unknown:
                sys.exit(f"⛔ 모르는 보상 항목 {unknown} — 지어내지 않는다. core/futgg_attrs.py의 표를 먼저 채울 것")
            ovr_after = bump(cp["current_ovr"] or 0)
            face_rows = con.execute("SELECT abbr, attr, weight, is_gk FROM fc_face_stats").fetchall()
            six_after = json.dumps(face_of(attrs_after, face_rows), ensure_ascii=False)
            src = "서버 계산 (current_attrs + fc_evolutions.levels · core/futgg_attrs.py)"
    if attrs_after is None:
        ovr_after = a.ovr_after or (after or {}).get("ovr")
        six_after = a.six_after or (json.dumps(after["six"]) if after else None)
        src = ("player_evolutions.path_json (fut.gg 계산 결과 카드)" if after else "사용자 입력값")
        print("⚠️ 29속성이나 카탈로그 단계가 없어 서버가 계산하지 못했다 — 받은 값을 그대로 적는다"
              f"(출처: {src}). 다음 클럽 싱크의 EA 실측으로 확정할 것.")
    if ovr_after is None:
        sys.exit("⛔ 적용 후 OVR을 알 수 없다 — 이 선수·진화의 path_json이 없으니 --ovr-after/--six-after를 직접 넘길 것")
    # ⛔⛔ **게이트 — 진화는 스탯을 내리지 않는다.** 위 계산이 옳아도 데이터가 어긋나면 여기서 멈춘다.
    #    「조심하자」로 막지 않는 이유: 조용히 틀린 값이라 화면만 봐선 알 수 없었다(실증 4행).
    if cp["current_six"] and six_after:
        b, f = json.loads(cp["current_six"]), json.loads(six_after)
        down = {k: (b[k], f[k]) for k in b if k in f and f[k] < b[k]}
        if down:
            sys.exit(f"⛔ 적용 후 6대 스탯이 내려간다 — {down} (before→after). 진화는 스탯을 내리지 않으니 "
                     "원장이 어긋난 것이다. `current_attrs`가 `current_six`보다 낡지 않았는지 먼저 볼 것.")
    if (ovr_after or 0) < (cp["current_ovr"] or 0):
        sys.exit(f"⛔ 적용 후 OVR이 내려간다 — {cp['current_ovr']} → {ovr_after}. 같은 사유다.")
    # ⭐ --in-progress: 「시작했다」는 사실만 남긴다(2026-09-19). 진화는 챌린지·훈련이 남으면 **스탯이 아직 안 올라간다** —
    #    완료 전에 current_* 를 올리면 화면이 없는 능력치를 보여준다. 소진·다음 추천 계산에는 포함된다(카드가 그 경로에 묶였으므로).
    #    완료되면 `complete` 서브커맨드로 그때 스탯을 반영한다.
    con.execute("""INSERT INTO fut_evolution_log(club_player_id, evo_id, evo_name, level, applied_at, completed_at,
                     ovr_before, ovr_after, six_before, six_after, playstyles_after, roles_plus_after, roles_plus_plus_after,
                     source, confidence, notes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (cp["id"], a.evo, evo_name, a.level, a.date, a.completed, cp["current_ovr"], ovr_after, cp["current_six"], six_after,
                 json.dumps((after or {}).get("playstyles"), ensure_ascii=False) if after else None,
                 json.dumps((after or {}).get("roles_plus")) if after else None,
                 json.dumps((after or {}).get("roles_plus_plus")) if after else None,
                 f"scripts/fut_club.py evolve ({TODAY} 기록) · 적용 후 값 출처: {src}",
                 "MEASURED(사용자 행위) — 적용 사실은 사용자 보고. 적용 후 스탯은 " + src + ".", a.note))
    if getattr(a, "in_progress", False):
        con.execute("UPDATE fut_club_players SET evo_count=evo_count+1, updated=? WHERE id=?", (TODAY, cp["id"]))
        print(f"진화 시작 기록: {cp['name']} ← {evo_name} (lv{a.level}) · 완주 시 OVR {cp['current_ovr']} → {ovr_after} "
              f"· 스탯은 **완료 시** 반영(`complete` 커맨드) · 시작일 {a.date}")
        return
    # ⭐ `current_attrs`를 **함께** 갱신한다 — 이것을 빼면 위 주석의 사고가 그대로 되돌아온다.
    if attrs_after is not None:
        con.execute("UPDATE fut_club_players SET current_attrs=? WHERE id=?",
                    (json.dumps(attrs_after, ensure_ascii=False), cp["id"]))
    con.execute("""UPDATE fut_club_players SET current_ovr=?, current_six=?, current_playstyles=COALESCE(?, current_playstyles),
                     current_roles_plus=COALESCE(?, current_roles_plus), current_roles_plus_plus=COALESCE(?, current_roles_plus_plus),
                     evo_count=evo_count+1, updated=? WHERE id=?""",
                (ovr_after, six_after,
                 ", ".join(after["playstyles"]) if after and after.get("playstyles") else None,
                 json.dumps(after["roles_plus"]) if after else None, json.dumps(after["roles_plus_plus"]) if after else None,
                 TODAY, cp["id"]))
    print(f"진화 기록: {cp['name']} ← {evo_name} (lv{a.level}) OVR {cp['current_ovr']} → {ovr_after} · 적용일 {a.date}")


def cmd_complete(con, a):
    """진행 중이던 진화를 완료 처리 — 그때 비로소 current_* 를 로그의 after 값으로 올린다."""
    acc = account(con, a.account)
    cp = club_player(con, acc["id"], a.player)
    log = con.execute("""SELECT * FROM fut_evolution_log WHERE club_player_id=? AND completed_at IS NULL
                         AND (?=0 OR evo_id=?) ORDER BY applied_at, id LIMIT 1""",
                      (cp["id"], 1 if a.evo else 0, a.evo or 0)).fetchone()
    if not log:
        raise SystemExit(f"⛔ {cp['name']}에게 진행 중인 진화가 없다")
    con.execute("UPDATE fut_evolution_log SET completed_at=? WHERE id=?", (a.date, log["id"]))
    con.execute("""UPDATE fut_club_players SET current_ovr=?, current_six=COALESCE(?, current_six),
                     current_playstyles=COALESCE(?, current_playstyles), current_roles_plus=COALESCE(?, current_roles_plus),
                     current_roles_plus_plus=COALESCE(?, current_roles_plus_plus), updated=? WHERE id=?""",
                (a.ovr_after or log["ovr_after"], a.six_after or log["six_after"],
                 ", ".join(json.loads(log["playstyles_after"])) if log["playstyles_after"] else None,
                 log["roles_plus_after"], log["roles_plus_plus_after"], TODAY, cp["id"]))
    print(f"진화 완료: {cp['name']} ← {log['evo_name']} · OVR {log['ovr_before']} → {a.ovr_after or log['ovr_after']} · 완료일 {a.date}")


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


def cmd_sbc_formation(con, a):
    """챌린지의 요구 포메이션을 기록하고 **그 챌린지만** 다시 푼다 (2026-09-25 신설 · migration 069).
       ⛔ EA·fut.gg가 주지 않는 값이라 사용자 입력이 유일한 출처다 — 그래서 source에 그렇게 적는다."""
    import subprocess
    import sys as _sys
    ch, form = int(a.challenge), str(a.formation).strip()
    row = con.execute("SELECT name FROM fc_sbc_challenges WHERE challenge_ea_id=? ORDER BY pulled DESC LIMIT 1",
                      (ch,)).fetchone()
    if not row:
        raise SystemExit(f"⛔ 챌린지 {ch}를 모른다 — 먼저 collect_futgg_sbc.py로 수집할 것")
    con.execute("""INSERT INTO fc_sbc_formations(game_version, challenge_ea_id, formation, source, confidence, updated)
                   VALUES(?,?,?,?,?,?)
                   ON CONFLICT(game_version, challenge_ea_id) DO UPDATE SET
                     formation=excluded.formation, source=excluded.source, updated=excluded.updated""",
                (a.game, ch, form, f"사용자 입력({TODAY}) — 인게임 SBC 화면 표기",
                 "MEASURED(사용자 확인) — EA·fut.gg가 이 값을 주지 않는다(migration 069 주석).", TODAY))
    con.commit()
    print(f"📐 {row['name']} 포메이션 {form} 기록 — 다시 푸는 중…")
    _resolve()


# ⛔⛔ **탐색 횟수를 여기 적지 않는다**(2026-09-25). 종전엔 `sbc_solve.py` 기본이 400인데 여기서 500을 줘서
#    **부르는 경로에 따라 같은 챌린지가 「달성 가능」과 「못 찾음」으로 갈렸다**(Norway v Portugal 실측).
#    ⇒ 값은 `sbc_solve.py`의 기본값 하나뿐이고 여기서는 그냥 부른다(불변규칙 13 ② 단일 정본).
def _resolve():
    import subprocess
    import sys as _sys
    r = subprocess.run([_sys.executable, str(ROOT / "scripts" / "sbc_solve.py"), "--save"],
                       capture_output=True, text=True, cwd=ROOT)
    print(r.stdout.strip()[-600:] if r.returncode == 0 else "⛔ 재계산 실패:\n" + (r.stdout + r.stderr)[-600:])


def cmd_sbc_submit(con, a):
    """⭐⭐ **SBC를 제출했다고 표시하고, 그 11장을 구단에서 덜어낸다**(2026-09-26 사용자 지시
       「sbc를 제출해서 내가 완료처리할 수 있도록 하고, 완료처리되면 해당 스쿼드의 선수들은
        스쿼드에서 없어진 걸로 처리 및 다른 sbc 해법 재계산하도록 수정」 · migration 072).

    왜 필요한가: SBC 제출은 되돌릴 수 없고 카드가 구단에서 **영구 제거**되는데, EA도 fut.gg도
      **어떤 카드를 냈는지 주지 않는다**. 그래서 다음 싱크 전까지 원장엔 「보유」로 남고
      다음 챌린지 해법이 **이미 낸 카드를 또 쓴다**(2026-09-25에 실제로 그랬다).
      ⇒ 제출 사실을 사람이 적는 순간 그 11장을 `status='sbc'`로 내려 **다음 계산에서 빠지게** 한다.

    ⛔ 무엇을 냈는지는 **우리가 제안한 스쿼드**로 기록한다 — 다른 조합으로 내셨다면 그건 사실이 아니다.
       그래서 `--undo`로 되돌릴 수 있게 두고, 기록에 그 한계를 적는다.
    ⛔ 해법이 없거나(`verdict != ok`) 스쿼드가 낡아 이미 소모된 카드를 품고 있으면 **멈춘다** —
       틀린 소모 기록은 다음 계산을 통째로 오염시킨다."""
    ch = int(a.challenge)
    row = con.execute("""SELECT c.name, c.set_ea_id, s.verdict, s.squad_json
                           FROM fc_sbc_challenges c
                           LEFT JOIN fc_sbc_solutions s ON s.challenge_ea_id=c.challenge_ea_id
                                AND s.pulled=(SELECT MAX(pulled) FROM fc_sbc_solutions)
                          WHERE c.challenge_ea_id=? ORDER BY c.pulled DESC LIMIT 1""", (ch,)).fetchone()
    if not row:
        raise SystemExit(f"⛔ 챌린지 {ch}를 모른다")

    if getattr(a, "undo", False):
        n = con.execute("UPDATE fut_club_players SET status='owned', sbc_challenge_ea_id=NULL, updated=? "
                        "WHERE sbc_challenge_ea_id=? AND status='sbc'", (TODAY, ch)).rowcount
        con.execute("DELETE FROM fut_sbc_log WHERE challenge_ea_id=? AND game_version=?", (ch, a.game))
        con.commit()
        print(f"↩️ {row['name']} 완료 취소 — 카드 {n}장을 보유로 되돌렸다. 다시 푸는 중…")
        _resolve()
        return

    # ⭐ **다른 조합으로 냈다 — 기록만**(2026-09-26 실측으로 필요해졌다).
    #    화면이 낡은 사이 인게임에서 다른 11장으로 제출하는 일이 실제로 있었다. 그때 우리는
    #    **무엇을 냈는지 알 수 없다** ⇒ 완료 사실만 적고 **카드는 건드리지 않는다**(발명 금지·불변규칙 3).
    #    소모된 카드는 다음 클럽 싱크가 「EA 목록에 없음」으로 잡아 준다.
    if not getattr(a, "cards", True):
        con.execute("""INSERT INTO fut_sbc_log(account_id, game_version, set_ea_id, challenge_ea_id,
                         completed_at, squad_note, source, confidence, notes)
                       VALUES((SELECT id FROM fut_accounts ORDER BY id LIMIT 1),?,?,?,?,NULL,?,?,?)
                       ON CONFLICT(account_id, game_version, challenge_ea_id) DO UPDATE SET
                         completed_at=excluded.completed_at""",
                    (a.game, row["set_ea_id"], ch, TODAY,
                     f"사용자가 화면에서 완료 처리({TODAY}) — 우리 제안과 **다른 조합**으로 제출",
                     "MEASURED(사용자 행위). ⚠️ 제출 카드는 **모른다** — 우리 해법과 다른 조합이라 "
                     "squad_note를 비운다. 소모된 카드는 다음 클럽 싱크가 잡는다.",
                     row["name"]))
        con.commit()
        print(f"🏁 {row['name']} 완료 처리(기록만) — 낸 카드는 모르므로 구단은 건드리지 않았다. "
              f"다음 클럽 싱크가 사라진 카드를 잡는다. 다시 푸는 중…")
        _resolve()
        return

    if row["verdict"] != "ok" or not row["squad_json"]:
        # ⚠️ 화면엔 「해법 완료」로 보이는데 여기 오는 일이 있다 — **그 사이 판정이 뒤집힌** 것이다
        #    (다른 SBC를 제출해 카드가 빠지면 남은 챌린지가 못 풀리게 된다). 그 사실을 그대로 적는다.
        raise SystemExit(
            f"⛔ {row['name']}: 지금 저장된 해법이 없다(verdict={row['verdict']}).\n"
            "   화면엔 해법이 보였다면 **그 사이 판정이 바뀐 것**이다 — 다른 SBC를 제출해 카드가 빠졌거나\n"
            "   다시 풀렸다. 새로고침하면 지금 판정이 보인다.\n"
            "   ⭐ 인게임에서 이미 내셨다면, 낸 카드를 알려 주시면 그대로 기록하겠다(해법과 달라도 된다).")
    sq = json.loads(row["squad_json"])["players"]
    ids = [p["id"] for p in sq]
    bad = con.execute("SELECT name, status FROM fut_club_players WHERE id IN (%s) AND status<>'owned'"
                      % ",".join("?" * len(ids)), ids).fetchall()
    if bad:
        raise SystemExit("⛔ 해법이 낡았다 — 이미 보유가 아닌 카드가 들어 있다: "
                         + ", ".join(f"{b['name']}({b['status']})" for b in bad)
                         + "\n   먼저 다시 풀 것(화면의 「이 포메이션으로 풀기」).")
    note = " · ".join(f"{p['slot']} {p['name']}({p['ovr']})" for p in sq)
    con.execute("""INSERT INTO fut_sbc_log(account_id, game_version, set_ea_id, challenge_ea_id,
                     completed_at, squad_note, source, confidence, notes)
                   VALUES((SELECT id FROM fut_accounts ORDER BY id LIMIT 1),?,?,?,?,?,?,?,?)
                   ON CONFLICT(account_id, game_version, challenge_ea_id) DO UPDATE SET
                     completed_at=excluded.completed_at, squad_note=excluded.squad_note""",
                (a.game, row["set_ea_id"], ch, TODAY, note,
                 f"사용자가 화면에서 완료 처리({TODAY}) — EA·fut.gg가 주지 않는 축이라 사람이 적는다",
                 "MEASURED(사용자 행위). ⚠️ 제출 카드는 **우리가 제안한 11장**으로 적었다 — "
                 "다른 조합으로 내셨다면 사실과 다르다(되돌리려면 완료 취소).",
                 row["name"]))
    n = con.execute("UPDATE fut_club_players SET status='sbc', sbc_challenge_ea_id=?, updated=? "
                    "WHERE id IN (%s)" % ",".join("?" * len(ids)), [ch, TODAY] + ids).rowcount
    con.commit()
    print(f"🏁 {row['name']} 완료 처리 — 카드 {n}장을 구단에서 덜어냈다. 남은 SBC를 다시 푸는 중…")
    _resolve()


def cmd_sbc_exclude(con, a):
    """⭐ **이 챌린지에서 이 카드를 빼고 다시 푼다**(2026-09-25 사용자 지시 「선수를 스쿼드에서 제외하고
       재계산하는 기능을 넣어줘 — 제외한 선수는 해당 sbc에 포함 안 시키는 용이야」).

    ⛔ 제외는 **챌린지별**이다. 전역 제외(활성 스쿼드·아스톤 빌라)와 축이 다르다 —
       「이 카드는 아껴 둔다」는 판단은 챌린지마다 달라진다.
    ⛔ 카드를 지우거나 상태를 바꾸지 않는다 — 제외는 **판정 입력**일 뿐이다(불변규칙 2).
    `--undo`면 제외를 푼다."""
    ch, cid = int(a.challenge), int(a.club_player)
    row = con.execute("SELECT name FROM fut_club_players WHERE id=?", (cid,)).fetchone()
    if not row:
        raise SystemExit(f"⛔ 보유 카드 {cid}를 모른다")
    if getattr(a, "undo", False):
        con.execute("DELETE FROM fc_sbc_exclusions WHERE game_version=? AND challenge_ea_id=? AND club_player_id=?",
                    (a.game, ch, cid))
        print(f"↩️ {row['name']} 제외 해제 — 다시 푸는 중…")
    else:
        con.execute("""INSERT INTO fc_sbc_exclusions(game_version, challenge_ea_id, club_player_id, reason, added)
                       VALUES(?,?,?,?,?) ON CONFLICT DO NOTHING""",
                    (a.game, ch, cid, a.notes or "사용자가 이 챌린지에서 뺌", TODAY))
        print(f"🚫 {row['name']} 제외 — 다시 푸는 중…")
    con.commit()
    _resolve()


def run(con, cmd, **kw):
    """serve.py 쓰기 API용 진입점 — CLI와 같은 함수를 같은 규약으로 실행한다(발명 금지·출처 기록 동일)."""
    defaults = dict(platform=None, game="FC27", notes=None, player_id=None, ea_item=None, acquired=None, how=None,
                    level=1, date=TODAY, completed=None, note=None, ovr_after=None, six_after=None, status=None, op="add",
                    in_progress=False, evo=None, challenge=None, formation=None, club_player=None, undo=False, cards=True,
                    expect_player_id=None)
    a = argparse.Namespace(**{**defaults, **kw})
    fn = {"account": cmd_account, "player": cmd_player_add, "player_set": cmd_player_set, "evolve": cmd_evolve, "complete": cmd_complete,
          "sbc_formation": cmd_sbc_formation, "sbc_exclude": cmd_sbc_exclude,
          "sbc_submit": cmd_sbc_submit}[cmd]
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
    s.add_argument("--ovr-after", type=int); s.add_argument("--six-after", help='JSON {"PAC":..} — ⚠️ 서버가 계산하지 못할 때만 쓰는 폴백')
    s.add_argument("--pick", type=int, help="갈림길 단계에서 **몇 번째 가지**를 밟았는지(0부터). 갈림길이면 필수다")
    s.add_argument("--in-progress", action="store_true", help="시작만 기록(챌린지·훈련이 남아 스탯은 아직 안 올랐다)")
    s = sub.add_parser("complete"); s.add_argument("--account", required=True); s.add_argument("--player", required=True)
    s.add_argument("--evo", type=int); s.add_argument("--date", default=TODAY)
    s.add_argument("--ovr-after", type=int); s.add_argument("--six-after")
    s = sub.add_parser("player-set"); s.add_argument("--account", required=True); s.add_argument("--player", required=True)
    s.add_argument("--status", choices=["owned", "sold", "discarded"]); s.add_argument("--notes")
    s = sub.add_parser("import"); s.add_argument("path"); s.add_argument("--account", required=True)
    s.add_argument("--source", default="manual", help="목록 출처 표기(예: gg-club 2026-09-26 · webapp-club-page)"); s.add_argument("--how")
    s = sub.add_parser("list"); s.add_argument("--account", required=True)
    a = ap.parse_args()
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    {"account": cmd_account, "player": cmd_player_add, "player-set": cmd_player_set, "evolve": cmd_evolve,
     "complete": cmd_complete, "import": cmd_import, "list": cmd_list}[a.cmd](con, a)
    con.commit()
    if a.cmd != "list":
        print("다음: python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
