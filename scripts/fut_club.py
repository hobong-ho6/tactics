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
            six = {"PAC": c["pac"], "SHO": c["sho"], "PAS": c["pas"], "DRI": c["dri"], "DEF": c["def"], "PHY": c["phy"]}
            at = json.loads(c["attrs"]) if c["attrs"] else None
            # ⭐ 6대 스탯이 빈 카드 행(옛 _ensure_card가 만든 것)은 29속성에서 환산한다 — null을 적지 않는다(2026-10-07).
            if None in six.values():
                if not at:
                    raise SystemExit(f"⛔ 카드 {a.ea_item}에 6대 스탯도 29속성도 없다 — 지어내지 않는다")
                is_gk = (c["best_pos"] or "") == "GK"
                six = face_of(at, con.execute("SELECT abbr, attr, weight, is_gk FROM fc_face_stats").fetchall(), is_gk=is_gk)
            cur = dict(current_ovr=c["ovr"], current_playstyles=c["playstyles"],
                       current_roles_plus=c["roles_plus"], current_roles_plus_plus=c["roles_plus_plus"],
                       current_six=json.dumps(six),
                       # ⭐ 29속성도 함께 — `evolve`가 여기서 출발한다(없으면 진화 기록이 계산을 못 한다)
                       current_attrs=json.dumps(at, ensure_ascii=False) if at else None)
            if not a.player_id:
                a.player_id = c["player_id"]
    con.execute("""INSERT INTO fut_club_players(account_id, player_id, ea_item_id, name, acquired, acquired_how, status,
                     current_ovr, current_six, current_playstyles, current_roles_plus, current_roles_plus_plus, current_attrs,
                     notes, updated)
                   VALUES(?,?,?,?,?,?,'owned',?,?,?,?,?,?,?,?)""",
                (acc["id"], a.player_id, a.ea_item, a.name, a.acquired, a.how,
                 cur.get("current_ovr"), cur.get("current_six"), cur.get("current_playstyles"),
                 cur.get("current_roles_plus"), cur.get("current_roles_plus_plus"), cur.get("current_attrs"),
                 a.notes, TODAY))
    print(f"보유 등록: {a.name} (player_id={a.player_id}, item={a.ea_item}, OVR {cur.get('current_ovr', '미상')})")


def pre_step_state(con, cp, game):
    """이 단계를 밟기 **직전** 카드 상태 — (attrs, ovr, six). 없으면 None.

    ⛔⛔ `current_attrs`(EA 싱크값)를 출발점으로 쓰지 않는다(2026-10-05 Emily Ramsey 실측 사고).
       클럽 싱크가 **이미 진화가 반영된 카드**를 받아 온 뒤에 기록하면 보상이 두 번 얹혀
       상한값이 들어갔다(가속 46→50 · 반사신경 78→80). ovr_before·six_before도 같은 이유로
       현재값이 들어가 「79→79」가 됐다(런북 연관표 #2 — 손으로 고치던 것).
    ⇒ 출발점은 **원장 사슬**이다: 이 카드의 마지막 유효 로그(attrs_after)가 있으면 그것,
       없으면 기준 카드(`player_card_items`). EA 실측과의 대조는 호출부가 한다."""
    last = con.execute("""SELECT ovr_after, six_after, attrs_after FROM fut_evolution_log
                           WHERE club_player_id=? AND COALESCE(is_void,0)=0 AND completed_at IS NOT NULL
                           ORDER BY applied_at DESC, id DESC LIMIT 1""", (cp["id"],)).fetchone()
    if last and last["attrs_after"]:
        return json.loads(last["attrs_after"]), last["ovr_after"], last["six_after"]
    # ⛔⛔ **사슬이 끊긴 카드(옛 로그에 attrs_after 없음 · migration 082 이전)는 기준 카드로 물러서지 않는다**
    #    (2026-10-08 마조 Batigol 실측 사고 — 진화 11회를 밟은 80 카드가 베이스 65에서 출발해 「80 → 73」으로 적혔다).
    #    마지막 로그의 OVR과 EA 싱크 OVR이 같으면 EA 카드가 그 로그 직후 상태다 → 그것을 출발점으로 쓴다.
    #    다르면(뒷단계가 이미 반영됐거나 싱크가 낡음) 판단할 수 없으니 멈춘다 — Emily Ramsey 이중 적용(위)을 막는 조건이다.
    if last:
        if cp["current_attrs"] and cp["current_ovr"] == last["ovr_after"]:
            return json.loads(cp["current_attrs"]), cp["current_ovr"], cp["current_six"]
        sys.exit(f"⛔ 옛 로그(29속성 없음)의 OVR {last['ovr_after']} ≠ EA 싱크 OVR {cp['current_ovr']} — 진화 직전 상태를 "
                 "알 수 없다. 클럽 싱크 후 `python3 scripts/evo_detect.py --verify`로 맞춘 뒤 다시 기록할 것")
    for sql, arg in (("SELECT attrs, ovr FROM player_card_items WHERE ea_item_id=? AND game_version=?", cp["ea_item_id"]),
                     ("SELECT attrs, ovr FROM player_card_items WHERE player_id=? AND is_base=1 AND game_version=?",
                      cp["player_id"])):
        if arg is None:
            continue
        r = con.execute(sql, (arg, game)).fetchone()
        if r and r["attrs"]:
            return json.loads(r["attrs"]), r["ovr"], None
    return None


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
    #    ⇒ 이제 서버가 카탈로그 보상을 **원장 사슬 상태**(pre_step_state)에 얹어 **attrs·six·ovr 셋을 한꺼번에** 갱신한다.
    #       두 벌이 갈릴 수 있는 구조 자체가 없어진다. 화면이 보낸 숫자는 **대조용으로만** 본다.
    attrs_after = None
    ovr_before, six_before = cp["current_ovr"], cp["current_six"]   # 카탈로그로 계산하면 원장 사슬 값으로 바뀐다
    ps_after = None                 # 카탈로그로 계산하면 채운다 — 없을 때만 path_json(완주 카드)으로 물러선다
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
            # ⭐ 출발점 = 원장 사슬(pre_step_state) — EA 싱크값이 아니다. GK 5속성 등 기준 카드에 없는 키는 현재값으로 메운다.
            pre = pre_step_state(con, cp, acc["game_version"])
            if pre is None:
                sys.exit("⛔ 기준 카드(player_card_items)도 이전 로그도 없다 — 진화 직전 상태를 알 수 없다. "
                         "collect_futgg_cards.py로 카드를 먼저 받을 것")
            pre_attrs = {**cur_attrs, **pre[0]}
            attrs_after = dict(pre_attrs)
            # ⭐⭐ **역할·PlayStyle 보상도 카탈로그에서 읽는다**(2026-09-27 실측 사고).
            #    ⛔ 종전엔 `player_evolutions.path_json`이 있을 때만 역할을 갱신했다. 그런데
            #       `GK Roles++`처럼 **역할만 주는 진화**는 경로 축이 안 덮어 path_json이 없고,
            #       그러면 `current_roles_plus_plus`가 **영영 갱신되지 않는다**(스즈키 GK 역할++ 실측).
            #    ⚠️ 기존 보유와 **합집합**으로 둔다 — 진화는 역할을 빼앗지 않는다.
            gain_rpp = [u["value"] for u in ups if u.get("upgrade") == "role_plus_plus"]
            gain_rp = [u["value"] for u in ups if u.get("upgrade") == "role_plus"]
            gain_ps = [u["value"] for u in ups if u.get("upgrade") == "play_style"]
            # ⛔⛔ PlayStyle도 **이 단계 보상만** 얹는다(2026-09-28 실측 사고 — 바르가스 반복 배급 1단계).
            #    종전엔 `path_json`(fut.gg **완주** 카드)의 PlayStyle을 그대로 적어서, 1단계만 끝났는데
            #    2·3단계 보상(핑드 패스·퍼스트 터치)이 현재 카드에 붙었다. 스탯은 이미 단계별 계산이었다.
            ps_names = {r[0]: r[1] for r in con.execute(
                "SELECT ea_id, name FROM fc_playstyle_ids WHERE game_version=?", (acc["game_version"],))}
            miss_ps = [v for v in gain_ps if v not in ps_names]
            if miss_ps:
                sys.exit(f"⛔ 모르는 PlayStyle id {miss_ps} — 지어내지 않는다. collect_playstyle_ids.py를 먼저 돌릴 것")
            have_ps = [x.strip() for x in (cp["current_playstyles"] or "").split(",") if x.strip()]
            # ⭐ 「(^N)」 = 보유 PlayStyle 개수 상한(game_system_changes #41 · 인게임 C). 이미 N개면 새 PS는 붙지 않는다
            #    (2026-10-08 알레망 Nine Duty 실측 — PS 4개라 Game Changer (^3)가 EA 카드에 없는데 로그엔 붙었다).
            ps_after = list(have_ps)
            for u in ups:
                if u.get("upgrade") != "play_style" or ps_names[u["value"]] in ps_after:
                    continue
                cap = u.get("maxValue")
                if cap and len(ps_after) >= int(cap):
                    print(f"ℹ️ PlayStyle {ps_names[u['value']]}는 받지 못한다 — 보유 {len(ps_after)}개 ≥ 상한 {cap}")
                    continue
                ps_after.append(ps_names[u["value"]])
            face_rows = con.execute("SELECT abbr, attr, weight, is_gk FROM fc_face_stats").fetchall()
            # ⛔ GK는 GK 구성식(DIV·HAN…)으로 환산한다 — 빼먹으면 필드 6대가 들어간다(2026-09-27 스즈키 실측 사고).
            #    GK 여부는 현재 카드의 6대 모양(EA 실측)으로 가른다.
            is_gk = "DIV" in json.loads(cp["current_six"] or "{}")
            bump, unknown = apply_upgrades(attrs_after, ups, face_rows, is_gk=is_gk)
            if unknown:
                sys.exit(f"⛔ 모르는 보상 항목 {unknown} — 지어내지 않는다. core/futgg_attrs.py의 표를 먼저 채울 것")
            ovr_before = pre[1] if pre[1] is not None else cp["current_ovr"]
            six_before = pre[2] or json.dumps(face_of(pre_attrs, face_rows, is_gk=is_gk), ensure_ascii=False)
            ovr_after = bump(ovr_before or 0)
            six_after = json.dumps(face_of(attrs_after, face_rows, is_gk=is_gk), ensure_ascii=False)
            # ⚠️ EA 실측이 직전·적용 후 어느 쪽과도 다르면 **알리기만** 한다 — 멈추지 않는다.
            #    정상인 경우가 둘 있다: EA가 뒷단계까지 앞서 있다(2단계까지 한 뒤 1단계부터 기록) ·
            #    EA 싱크가 아직 낡았다. 기록 안 된 진화 여부는 클럽 싱크의 `evo_detect.py --verify`가 매 회차 본다.
            common = [k for k in cur_attrs if k in pre[0]]
            if not any(all(x[k] == cur_attrs[k] for k in common) for x in (pre_attrs, attrs_after)):
                diff = {k: (pre_attrs[k], attrs_after[k], cur_attrs[k]) for k in common
                        if cur_attrs[k] not in (pre_attrs[k], attrs_after[k])}
                print(f"ℹ️ EA 실측이 이 단계 직전·적용 후와 다르다 (직전, 적용 후, EA) {dict(list(diff.items())[:6])} — "
                      "뒷단계가 이미 반영됐거나 싱크가 낡은 것이면 정상. 기록 후 `python3 scripts/evo_detect.py --verify`로 검산할 것")
            # ⭐⭐ **이 단계에서 구성 속성이 안 바뀐 6대 스탯은 다시 환산하지 않고 직전 값(EA 실측 사슬)을 잇는다**
            #    — 스탯 하나하나 단위로(2026-10-06 · 불변규칙 13 ① — 같은 사고 2회차).
            #    1회차(2026-09-29 스즈키 GK 역할++): 구성식 SPD 56 ↔ EA 58 → 「속성이 하나도 안 바뀌는 진화」만 예외로 뺐다.
            #    2회차(2026-10-06 스즈키 Goal Guardian): DIV·HAN이 올라 예외를 벗어나자 **안 바뀐 SPD**가 56으로 재환산돼 또 막혔다.
            #    ⇒ 구성식과 EA 표시값의 반올림 차이가 「건드리지 않은 스탯」에 새어 들어올 구조를 없앤다.
            prev_six = json.loads(pre[2] or cp["current_six"] or "{}")
            if prev_six:
                comp = {}
                for r in face_rows:
                    if bool(r["is_gk"]) == is_gk:
                        comp.setdefault(r["abbr"], []).append(r["attr"])
                new_six = json.loads(six_after)
                for k, attrs_k in comp.items():
                    if k in prev_six and all(pre_attrs.get(x) == attrs_after.get(x) for x in attrs_k):
                        new_six[k] = prev_six[k]
                six_after = json.dumps(new_six, ensure_ascii=False)
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
    if six_before and six_after:
        b, f = json.loads(six_before), json.loads(six_after)
        down = {k: (b[k], f[k]) for k in b if k in f and f[k] < b[k]}
        if down:
            sys.exit(f"⛔ 적용 후 6대 스탯이 내려간다 — {down} (before→after). 진화는 스탯을 내리지 않으니 "
                     "원장이 어긋난 것이다. `current_attrs`가 `current_six`보다 낡지 않았는지 먼저 볼 것.")
    if (ovr_after or 0) < (ovr_before or 0):
        sys.exit(f"⛔ 적용 후 OVR이 내려간다 — {ovr_before} → {ovr_after}. 같은 사유다.")
    # ⭐ 로그의 역할 칸도 **카탈로그 보상 ∪ 현재 보유**로 적는다(2026-09-29 만잠비 CAM Roles++ 실측 사고).
    #    ⛔ 종전엔 path_json에서만 읽어, 경로 축이 안 덮는 역할 전용 진화는 로그 칸이 비었다.
    def _union(cur_json, gain):
        try:
            have = json.loads(cur_json) if cur_json else []
        except Exception:                                    # noqa: BLE001
            have = []
        return list(have) + [v for v in gain or [] if v not in have]
    # ⭐ --in-progress: 「시작했다」는 사실만 남긴다(2026-09-19). 진화는 챌린지·훈련이 남으면 **스탯이 아직 안 올라간다** —
    #    완료 전에 current_* 를 올리면 화면이 없는 능력치를 보여준다. 소진·다음 추천 계산에는 포함된다(카드가 그 경로에 묶였으므로).
    #    완료되면 `complete` 서브커맨드로 그때 스탯을 반영한다.
    con.execute("""INSERT INTO fut_evolution_log(club_player_id, evo_id, evo_name, level, applied_at, completed_at,
                     ovr_before, ovr_after, six_before, six_after, attrs_after, playstyles_after, roles_plus_after,
                     roles_plus_plus_after, source, confidence, notes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (cp["id"], a.evo, evo_name, a.level, a.date, a.completed, ovr_before, ovr_after, six_before, six_after,
                 # ⭐ 29속성을 함께 남긴다(migration 082) — `complete`가 이걸 보고 current_attrs를 올린다.
                 json.dumps(attrs_after, ensure_ascii=False) if attrs_after is not None else None,
                 json.dumps(ps_after, ensure_ascii=False) if ps_after is not None else
                 (json.dumps((after or {}).get("playstyles"), ensure_ascii=False) if after else None),
                 json.dumps(_union(cp["current_roles_plus"], gain_rp)) if attrs_after is not None else (
                     json.dumps((after or {}).get("roles_plus")) if after else None),
                 json.dumps(_union(cp["current_roles_plus_plus"], gain_rpp)) if attrs_after is not None else (
                     json.dumps((after or {}).get("roles_plus_plus")) if after else None),
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
    # ⭐ 역할은 **합집합**으로 병합한다(카탈로그 보상 우선 · 없으면 path_json).
    def _merge(cur_json, gain):
        out = _union(cur_json, gain)
        return json.dumps(out) if out != _union(cur_json, []) else None
    rp_new = _merge(cp["current_roles_plus"], gain_rp) if attrs_after is not None else (
        json.dumps(after["roles_plus"]) if after else None)
    rpp_new = _merge(cp["current_roles_plus_plus"], gain_rpp) if attrs_after is not None else (
        json.dumps(after["roles_plus_plus"]) if after else None)
    con.execute("""UPDATE fut_club_players SET current_ovr=?, current_six=?, current_playstyles=COALESCE(?, current_playstyles),
                     current_roles_plus=COALESCE(?, current_roles_plus), current_roles_plus_plus=COALESCE(?, current_roles_plus_plus),
                     evo_count=evo_count+1, updated=? WHERE id=?""",
                (ovr_after, six_after,
                 ", ".join(ps_after) if ps_after is not None else
                 (", ".join(after["playstyles"]) if after and after.get("playstyles") else None),
                 rp_new, rpp_new, TODAY, cp["id"]))
    print(f"진화 기록: {cp['name']} ← {evo_name} (lv{a.level}) OVR {ovr_before} → {ovr_after} · 적용일 {a.date}")


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
    # ⛔⛔ **여기도 `current_attrs`를 함께 올린다**(2026-09-26 · migration 082).
    #    종전엔 `current_ovr`·`current_six`만 올려서, 081이 `evolve`에서 없앤 「두 벌 갈림」이
    #    **`complete` 경로로 그대로 재현**됐다. 같은 버그를 두 문에 남겨 두지 않는다(불변규칙 13).
    #    ⚠️ 옛 행은 `attrs_after`가 NULL이다 — 그때는 29속성을 못 올리니 **말없이 넘기지 않고 경고한다**.
    if log["attrs_after"]:
        con.execute("UPDATE fut_club_players SET current_attrs=? WHERE id=?", (log["attrs_after"], cp["id"]))
    else:
        print("⚠️ 이 로그 행에는 적용 후 29속성이 없다(migration 082 이전 기록) — `current_attrs`를 올리지 못했다. "
              "다음 클럽 싱크의 EA 실측이 맞춰 줄 때까지 6대 스탯과 29속성이 갈린 상태다.")
    six_new = a.six_after or log["six_after"]
    ovr_new = a.ovr_after or log["ovr_after"]
    # 게이트 — `evolve`와 같은 규칙이다. 진화는 스탯을 내리지 않는다.
    if cp["current_six"] and six_new:
        b, f = json.loads(cp["current_six"]), json.loads(six_new)
        down = {k: (b[k], f[k]) for k in b if k in f and f[k] < b[k]}
        if down:
            sys.exit(f"⛔ 완료 처리하면 6대 스탯이 내려간다 — {down} (before→after). 로그의 after 값이 어긋난 것이다.")
    con.execute("""UPDATE fut_club_players SET current_ovr=?, current_six=COALESCE(?, current_six),
                     current_playstyles=COALESCE(?, current_playstyles), current_roles_plus=COALESCE(?, current_roles_plus),
                     current_roles_plus_plus=COALESCE(?, current_roles_plus_plus), updated=? WHERE id=?""",
                (ovr_new, six_new,
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
        # ⭐ 스토리지 카드도 되돌린다(migration 095)
        n += con.execute("UPDATE fut_sbc_storage SET status='stored', used_challenge_ea_id=NULL, used_at=NULL "
                         "WHERE used_challenge_ea_id=? AND status='used'", (ch,)).rowcount
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
    ids = [p["id"] for p in sq if p["id"] > 0]
    sids = [-p["id"] for p in sq if p["id"] < 0]          # ⭐ 음수 id = SBC 스토리지 카드(migration 095)
    bad = con.execute("SELECT name, status FROM fut_club_players WHERE id IN (%s) AND status<>'owned'"
                      % ",".join("?" * len(ids)), ids).fetchall() if ids else []
    if sids:
        bad += con.execute("SELECT name, status FROM fut_sbc_storage WHERE id IN (%s) AND status<>'stored'"
                           % ",".join("?" * len(sids)), sids).fetchall()
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
                    "WHERE id IN (%s)" % ",".join("?" * len(ids)), [ch, TODAY] + ids).rowcount if ids else 0
    if sids:
        n += con.execute("UPDATE fut_sbc_storage SET status='used', used_challenge_ea_id=?, used_at=? "
                         "WHERE id IN (%s)" % ",".join("?" * len(sids)), [ch, TODAY] + sids).rowcount
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


# ── SBC 스토리지 (2026-10-02 사용자 지시 「sbc 스토리지 선수도 조회」 → 「화면 등록으로」 · migration 095) ──
#   ⛔ fut.gg가 스토리지를 주지 않아 사람이 등록한다. 해법(sbc_solve.py)이 이 카드를 **가장 먼저** 쓴다.
READONLY = {"storage_search"}      # serve.py가 export를 건너뛰는 명령(아무것도 쓰지 않는다)


def cmd_storage_search(con, a):
    """fut.gg FC27 카드를 이름으로 찾는다 — 결과를 JSON 한 줄로 찍는다(화면이 읽는다)."""
    from scripts.collect_futgg_history import API, get
    import urllib.parse
    q = (a.q or "").strip()
    if len(q) < 2:
        raise SystemExit("⛔ 두 글자 이상 넣는다")
    out = []
    for x in (get(f"{API}/players/v2/27/?name={urllib.parse.quote(q)}") or {}).get("data", [])[:24]:
        cl, lg = x.get("club") or {}, x.get("league") or {}
        out.append({"ea": x["eaId"], "name": x.get("commonName") or f"{x.get('firstName','')} {x.get('lastName','')}".strip(),
                    "ovr": x.get("overall"), "pos": x.get("position"), "rarity": x.get("rarityName"),
                    "club": cl.get("name"), "league": lg.get("name"), "card": x.get("cardImageUrl") or x.get("simpleCardImageUrl"),
                    "special": bool(x.get("isSpecial"))})
    print(json.dumps({"results": out}, ensure_ascii=False))


def _ensure_card(con, ea, game):
    """스토리지 카드의 정보 행이 없으면 fut.gg 정의로 만든다(채움 전용 — 있으면 건드리지 않는다)."""
    if con.execute("SELECT 1 FROM player_card_items WHERE game_version=? AND ea_item_id=?", (game, ea)).fetchone():
        return
    from scripts.collect_futgg_history import API, ATTR_MAP, POS, get
    d = get(f"{API}/player-item-definitions/27/{ea}/")
    d = (d or {}).get("data") or d or {}
    if not d.get("overall"):
        raise SystemExit(f"⛔ fut.gg에 카드 {ea} 정의가 없다 — 지어내지 않는다")
    x = ((get(f"{API}/players/v2/27/?ea_ids={ea}") or {}).get("data") or [{}])[0]
    cl, lg, na = x.get("club") or d.get("club") or {}, x.get("league") or d.get("league") or {}, x.get("nation") or d.get("nation") or {}
    name = d.get("commonName") or f"{d.get('firstName','')} {d.get('lastName','')}".strip()
    pos = POS.get(d.get("position"))
    alts = [POS.get(p) for p in (d.get("alternativePositionIds") or []) if POS.get(p)]
    attrs = {ATTR_MAP[k]: d[k] for k in ATTR_MAP if d.get(k) is not None}
    r = d.get("rarity") or {}
    # ⭐ 6대 스탯·PlayStyle·역할·개인기/약발도 같은 정의에서 채운다(2026-10-07 사용자 지시 「고쳐줘」).
    #    종전엔 빼먹어서 이 카드를 `player add`하면 current_six가 {"PAC": null, …}로 적혔다(알레망 실측).
    ps_name = {r2[0]: r2[1] for r2 in con.execute("SELECT ea_id, name FROM fc_playstyle_ids WHERE game_version=?", (game,))}
    ps = [ps_name.get(i) for i in d.get("playstyles") or []] + [f"{ps_name.get(i)}+" for i in d.get("playstylesPlus") or []]
    if None in ps or "None+" in ps:
        raise SystemExit(f"⛔ 모르는 PlayStyle id {d.get('playstyles')}/{d.get('playstylesPlus')} — collect_playstyle_ids.py를 먼저 돌릴 것")
    con.execute("""INSERT INTO player_card_items(game_version, ea_item_id, base_ea_id, is_base, name_kr, rarity_ea_id, rarity_name,
                     club, positions, best_pos, ovr, attrs, card_image_url, futgg_url, source, confidence, is_special, first_seen,
                     nation, league, is_icon, is_hero, club_ea_id, sibling_club_ea_id, league_ea_id, grading_score,
                     pac, sho, pas, dri, def, phy, playstyles, roles_plus, roles_plus_plus, skill_moves, weak_foot)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (game, ea, d.get("basePlayerEaId"), int(ea == d.get("basePlayerEaId")), name, d.get("rarityEaId"),
                 r.get("name") if isinstance(r, dict) else x.get("rarityName"), cl.get("name"),
                 "/".join([p for p in [pos] + alts if p]), pos, d.get("overall"), json.dumps(attrs, ensure_ascii=False),
                 x.get("cardImageUrl"), f"https://www.fut.gg{x['url']}" if x.get("url") else None,
                 f"fut.gg player-item-definitions/27/{ea} (SBC 스토리지 등록 {TODAY}, fut_club.py storage_add)",
                 "HIGH — fut.gg 카드 정의", int(bool(d.get("isSpecial"))), TODAY,
                 na.get("name"), lg.get("name"), int(bool(d.get("isIcon"))), int(bool(d.get("isHero"))),
                 cl.get("eaId"), cl.get("siblingClubEaId"), lg.get("eaId"), d.get("gradingScore"),
                 d.get("facePace"), d.get("faceShooting"), d.get("facePassing"), d.get("faceDribbling"),
                 d.get("faceDefending"), d.get("facePhysicality"), ", ".join(ps),
                 json.dumps(d.get("rolesPlus") or []), json.dumps(d.get("rolesPlusPlus") or []),
                 d.get("skillMoves"), d.get("weakFoot")))


def cmd_storage_add(con, a):
    """SBC 스토리지에 카드 한 장을 등록하고 해법을 다시 푼다."""
    ea = int(a.ea_item)
    _ensure_card(con, ea, a.game)
    nm = con.execute("SELECT name_kr, ovr FROM player_card_items WHERE game_version=? AND ea_item_id=?", (a.game, ea)).fetchone()
    con.execute("""INSERT INTO fut_sbc_storage(account_id, game_version, ea_item_id, name, added_at, source, notes)
                   VALUES((SELECT id FROM fut_accounts ORDER BY id LIMIT 1),?,?,?,?,?,?)""",
                (a.game, ea, nm["name_kr"], TODAY, "사용자 등록(화면 · fut.gg가 스토리지를 주지 않는다)", a.notes))
    con.commit()
    print(f"📦 {nm['name_kr']}({nm['ovr']}) 스토리지 등록 — SBC 해법을 다시 푸는 중…")
    _resolve()


def cmd_storage_remove(con, a):
    """스토리지 카드를 뺀다(행은 남기고 removed로 — 불변규칙 2) · 해법을 다시 푼다."""
    sid = int(a.storage_id)
    r = con.execute("SELECT name, status FROM fut_sbc_storage WHERE id=?", (sid,)).fetchone()
    if not r:
        raise SystemExit(f"⛔ 스토리지 카드 {sid}를 모른다")
    con.execute("UPDATE fut_sbc_storage SET status='removed', notes=COALESCE(notes||' · ','')||? WHERE id=?",
                (f"{TODAY} 사용자가 뺌", sid))
    con.commit()
    print(f"🗑 {r['name']} 스토리지에서 뺐다 — SBC 해법을 다시 푸는 중…")
    _resolve()


def cmd_gallery_complete(con, a):
    """갤러리 세트를 **완성했다**고 원장에 행을 추가한다(2026-10-02 · migration 093 — 「내가 완성한 갤러리 정보도 우리 디비에서 관리」).
       · grade를 주지 않으면 **최신 평가 등급**으로 적는다. 인게임 등급이 다르면(태그 보너스 등) grade로 밝힌다.
       · cards=True면 최신 평가가 고른 카드·점수를 함께 남긴다(우리 제안대로 넣었을 때). 다른 카드로 넣었으면 cards=False.
       · undo=True면 그 세트의 **가장 최근 행 하나**를 지운다(잘못 누른 기록 되돌리기).
       ⛔ fut.gg에는 쓰지 않는다 — 인게임 갤러리 화면이 정본이고 이 원장이 그 기록이다."""
    sid = int(a.set_id)
    s = con.execute("""SELECT name FROM fc_gallery_sets WHERE game_version=? AND set_id=?
                        ORDER BY pulled DESC LIMIT 1""", (a.game, sid)).fetchone()
    if not s:
        raise SystemExit(f"⛔ 갤러리 세트 {sid}를 모른다")
    if getattr(a, "undo", False):
        r = con.execute("""SELECT id, grade, completed_at FROM fut_gallery_completions WHERE game_version=? AND set_id=?
                            ORDER BY id DESC LIMIT 1""", (a.game, sid)).fetchone()
        if not r:
            raise SystemExit(f"⛔ {s['name']}: 되돌릴 완성 기록이 없다")
        con.execute("DELETE FROM fut_gallery_completions WHERE id=?", (r["id"],))
        con.commit()
        print(f"↩️ {s['name']} 완성 기록 {r['grade']}({r['completed_at']})을 지웠다")
        return
    ev = con.execute("""SELECT grade, base_score, card_ids FROM fut_gallery_eval WHERE game_version=? AND set_id=?
                         ORDER BY pulled DESC LIMIT 1""", (a.game, sid)).fetchone()
    g = (a.grade or "").strip().upper() or (ev["grade"] if ev else None)
    if g not in ("D", "C", "B", "A", "S"):
        raise SystemExit(f"⛔ {s['name']}: 등급을 정할 수 없다(받은 값 {a.grade!r} · 평가 등급 {ev['grade'] if ev else None}) — "
                         "세트를 완성하지 못했으면 기록하지 않는다")
    cards = getattr(a, "cards", True)
    con.execute("""INSERT INTO fut_gallery_completions(game_version,set_id,grade,completed_at,score,card_ids,source,notes)
                   VALUES(?,?,?,?,?,?,?,?)""",
                (a.game, sid, g, a.date or TODAY, ev["base_score"] if (ev and cards) else None,
                 ev["card_ids"] if (ev and cards) else None,
                 "사용자 완성 처리(인게임 갤러리) — 화면 또는 fut_club.py gallery_complete"
                 + ("" if cards else " · 넣은 카드는 우리 제안과 달라 남기지 않음"), a.notes))
    con.commit()
    print(f"🏁 {s['name']} 완성 — {g} ({a.date or TODAY})")


def cmd_sbc_resolve(con, a):
    """SBC 해법 재계산 — 화면 버튼(2026-10-05 사용자 지시 「sbc 해법 다시 계산하는 버튼」).
       ⛔ 계산을 여기 다시 짜지 않는다 — 클럽 싱크 「해법 재계산」 단계와 **같은 명령**(sbc_solve.py --save)을 그대로 부른다.
       끝나면 serve.py가 export를 돌린다(읽기 전용 아님)."""
    import subprocess
    root = Path(__file__).resolve().parent.parent
    py = root / ".venv" / "bin" / "python"
    py = str(py) if py.exists() else sys.executable
    r = subprocess.run([py, str(root / "scripts" / "sbc_solve.py"), "--save"], capture_output=True, text=True,
                       cwd=root, timeout=900)
    tail = "\n".join((r.stdout or "").strip().splitlines()[-8:])
    if r.returncode != 0:
        raise SystemExit(f"⛔ sbc_solve.py 실패(코드 {r.returncode})\n{tail}\n{(r.stderr or '')[-600:]}")
    print(f"🔁 SBC 해법 재계산 완료\n{tail}")


def run(con, cmd, **kw):
    """serve.py 쓰기 API용 진입점 — CLI와 같은 함수를 같은 규약으로 실행한다(발명 금지·출처 기록 동일)."""
    defaults = dict(platform=None, game="FC27", notes=None, player_id=None, ea_item=None, acquired=None, how=None,
                    level=1, date=TODAY, completed=None, note=None, ovr_after=None, six_after=None, status=None, op="add",
                    in_progress=False, evo=None, challenge=None, formation=None, club_player=None, undo=False, cards=True,
                    expect_player_id=None, set_id=None, grade=None, q=None, storage_id=None)
    a = argparse.Namespace(**{**defaults, **kw})
    fn = {"account": cmd_account, "player": cmd_player_add, "player_set": cmd_player_set, "evolve": cmd_evolve, "complete": cmd_complete,
          "sbc_formation": cmd_sbc_formation, "sbc_exclude": cmd_sbc_exclude,
          "sbc_submit": cmd_sbc_submit, "gallery_complete": cmd_gallery_complete, "sbc_resolve": cmd_sbc_resolve,
          "storage_search": cmd_storage_search, "storage_add": cmd_storage_add, "storage_remove": cmd_storage_remove}[cmd]
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
    # ⛔⛔ CLI에도 교차검증을 연다 — `players.id`와 `fut_club_players.id`는 같은 번호 공간이고
    #    실측으로 22쌍이 충돌한다(예: club 18=스즈키 ↔ players 18=게상). 화면만 막아선 부족하다.
    s.add_argument("--expect-player-id", dest="expect_player_id", type=int,
                   help="players.id — 찾은 카드가 그 선수의 것인지 교차검증한다(강력 권장)")
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
