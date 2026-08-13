#!/usr/bin/env python3
"""v1(data/avl_analysis.db) → v2(db/tactics.db) 마이그레이션.

재실행 가능(idempotent): 매 실행이 v2를 지우고 v1에서 전량 재구축한다.
— 컷오버(단계 6) 전까지 transfer-watch 등이 v1에 계속 쓰므로, 컷오버 직전에
  이 스크립트를 한 번 더 돌려 v2를 최신으로 맞춘다.

검증(스크립트 말미에 자동 실행):
  1. 테이블별 행수 대조표 (v1 → v2, 손실 0 확인)
  2. 인코딩 회귀 — 이관된 전 그리드의 map25를 cells에서 재인코딩해 대조
  3. 커널 앵커 — 캐시 measured:season RM .835를 **DB의 game_role_variants로** 재현
     (HTML 파싱 없이 — v2에서 커널의 정본은 DB다)
  4. obs 번호 연속성 (1..141 승계)
"""
import json
import math
import re
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V1 = ROOT / "data" / "avl_analysis.db"
V2 = ROOT / "db" / "tactics.db"
SCHEMA = ROOT / "db" / "migrations" / "001-schema.sql"

# 팀 → regime (v1 team 컬럼의 승계 사상)
REGIME = {"AVL": 1, "CHE": 2, "LIV": 3}
TEAM_FULLNAME = {"Aston Villa": "AVL", "Chelsea": "CHE", "Liverpool": "LIV"}

# SofaScore 선수 id — v1에서는 docs/30 목록·notes 산문·세션 지식에 흩어져 있던 것의 통합
SOFASCORE_IDS = {
    "Ezri Konsa": 827679, "Emiliano Buendia": 783126, "Matty Cash": 833956,
    "Lucas Digne": 96538, "Morgan Rogers": 948261, "Youri Tielemans": 331737,
    "John McGinn": 250223, "Amadou Onana": 923973, "Boubacar Kamara": 826204,
    "Tyrone Mings": 303638, "Marco Bizot": 100390, "Joe Gauci": 966874,
    "George Hemmings": 1398204, "Alejandro Garnacho": 1135873,
    "Johan Manzambi": 1518931, "João Gomes": 1015267, "Modou Kéba Cissé": 1944705,
    "Alysson": 1631879, "Tammy Abraham": 610766, "Ross Barkley": 98435,
}

# stats_json 키 방언 — v1에 두 세대가 공존한다 (구세대 축약키 / 신세대 풀네임)
STAT_KEYS = {
    "xg": ["xg"], "xa": ["xa"],
    "key_passes": ["key_passes", "kp"],
    "duels_won": ["duel_won", "duels_won", "duelW"],
    "duels_lost": ["duel_lost", "duels_lost", "duelL"],
    "tackles": ["tackles", "tkl"],
    "interceptions": ["interceptions", "intc"],
    "goals": ["goals"], "assists": ["assists"],
    "touches": ["touches", "touch"],
    "recoveries": ["recovery", "recov"],
}


def encode(cells):
    m = max(cells)
    if m == 0:
        return None
    return "".join("X" if v == m else str(min(9, math.floor(v / m * 10 + 0.5))) for v in cells)


def pick(d, keys):
    for k in keys:
        if k in d and d[k] is not None and d[k] != "":
            return d[k]
    return None


def main():
    if not V1.exists():
        sys.exit(f"v1 DB 없음: {V1}")
    V2.unlink(missing_ok=True)
    v1 = sqlite3.connect(V1)
    v1.row_factory = sqlite3.Row
    v2 = sqlite3.connect(V2)
    v2.executescript(SCHEMA.read_text(encoding="utf-8"))
    c1, c2 = v1.cursor(), v2.cursor()
    parity = []  # (표시명, v1행, v2행)

    # ── 축 ──────────────────────────────────────────────────────────
    c2.execute("INSERT INTO game_versions VALUES('FC26','2025-09-26','v1 전 데이터의 대상 버전')")
    c2.execute("INSERT INTO game_versions VALUES('FC27',NULL,'2026-09 발매 예정 — 온보딩 체크리스트는 docs/21')")

    for r in c1.execute("SELECT * FROM teams"):
        SOFA_TEAM = {"AVL": 40, "CHE": 38, "LIV": 44}      # CHE/LIV는 표준 id — 첫 수집에서 재확인
        FOTMOB = {"AVL": 10252, "CHE": 8455, "LIV": 8650}  # AVL만 실사용 검증됨(transfer-watch)
        c2.execute("INSERT INTO teams(code,name,name_kr,sofascore_id,fotmob_id,note) VALUES(?,?,?,?,?,?)",
                   (r["code"], r["name"], r["name_kr"], SOFA_TEAM.get(r["code"]),
                    FOTMOB.get(r["code"]), r["note"]))
    c2.executemany(
        "INSERT INTO regimes(id,team_code,manager,manager_kr,start,end,is_main,note) VALUES(?,?,?,?,?,?,?,?)",
        [(1, "AVL", "Unai Emery", "에메리", "2022-10-24", None, 1, "주 분석 대상(기준 구현)"),
         (2, "CHE", "Xabi Alonso", "알론소", "2026-07-01", None, 0,
          "레버쿠젠 3-4-2-1 블루프린트 이식 (docs/11). ⚠️ 25/26 첼시 팀 전술은 이 regime 것이 아니다"),
         (3, "LIV", "Andoni Iraola", "이라올라", "2026-07-01", None, 0,
          "본머스 실측 기반 이식 분석 (docs/12). ⚠️ 25/26 리버풀 팀 전술은 이 regime 것이 아니다")])

    n = c2.executemany("INSERT INTO seasons SELECT code,label FROM (SELECT ? code, ? label)",
                       c1.execute("SELECT code,label FROM seasons").fetchall()).rowcount
    parity.append(("seasons", c1.execute("SELECT COUNT(*) FROM seasons").fetchone()[0], n))

    # players — 식별자 승격
    sofifa = dict(c1.execute(
        "SELECT player_id, sofifa_id FROM player_fc_stats WHERE player_id IS NOT NULL AND sofifa_id IS NOT NULL"))
    rows = c1.execute("SELECT * FROM players").fetchall()
    for r in rows:
        c2.execute("""INSERT INTO players(id,name,name_kr,sofascore_id,sofifa_id,primary_position,notes)
                      VALUES(?,?,?,?,?,?,?)""",
                   (r["id"], r["name"], r["name_kr"], SOFASCORE_IDS.get(r["name"]),
                    sofifa.get(r["id"]), r["primary_position"], r["notes"]))
    parity.append(("players", len(rows), c2.execute("SELECT COUNT(*) FROM players").fetchone()[0]))

    rows = c1.execute("SELECT * FROM player_seasons").fetchall()
    for r in rows:
        club = r["club"] or ""
        c2.execute("""INSERT INTO player_tenures(player_id,season,club_code,club_name,position,shirt_no,minutes)
                      VALUES(?,?,?,?,?,?,?)""",
                   (r["player_id"], r["season"], TEAM_FULLNAME.get(club), club,
                    r["primary_position"], r["shirt_no"], r["minutes"]))
    parity.append(("player_seasons→tenures", len(rows),
                   c2.execute("SELECT COUNT(*) FROM player_tenures").fetchone()[0]))

    # ── 실세계 레이어 ────────────────────────────────────────────────
    rows = c1.execute("SELECT * FROM matches").fetchall()
    for r in rows:
        code = TEAM_FULLNAME.get(r["team"])
        if code is None:
            sys.exit(f"matches.team 사상 불가: {r['team']!r} (id={r['id']}) — TEAM_FULLNAME에 추가할 것")
        c2.execute("""INSERT INTO matches(id,team_code,season,date,opponent,competition,venue,result,
                                          is_club,stage,possession)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                   (r["id"], code, r["season"], r["date"], r["opponent"], r["competition"],
                    r["venue"], r["result"], r["is_club"], r["stage"], r["possession"]))
    parity.append(("matches", len(rows), c2.execute("SELECT COUNT(*) FROM matches").fetchone()[0]))

    # player_matches = positions(기저) + grids(병합) + appearances(병합/잔여 삽입)
    pos_rows = c1.execute("SELECT * FROM player_match_positions").fetchall()
    grids = {(g["player_id"], g["event_id"]): g
             for g in c1.execute("SELECT * FROM player_match_grids WHERE player_id IS NOT NULL")}
    n_grid_merged = 0
    # ⭐ 인코딩 정규화 — v1 그리드에는 반올림 세대가 섞여 있다(banker's round 계열 vs
    #    half-up 계열, 2026-08-11 마이그레이션 검증에서 112행 차이로 발견). cells가
    #    무손실 원자료이므로(docs/30 ③) v2는 정본 인코더(half-up + 9클램프)로 전량
    #    재인코딩한다. v1 값과 달라진 행 수는 아래에서 보고.
    n_reencoded = 0

    def canon_map25(g):
        nonlocal n_reencoded
        if not g or not g["cells"]:
            return g["map25"] if g else None
        m = encode([int(x) for x in g["cells"].split(",")])
        if m != g["map25"]:
            n_reencoded += 1
        return m
    for r in pos_rows:
        g = grids.pop((r["player_id"], r["event_id"]), None)
        st = json.loads(r["stats_json"]) if r["stats_json"] else {}
        vals = {k: pick(st, ks) for k, ks in STAT_KEYS.items()}
        c2.execute("""INSERT INTO player_matches
            (player_id,event_id,season,date,opponent,venue,competition,minutes,rating,started,
             lineup_pos,pos_class,lineup_order,formation,avg_x,avg_y,possession,
             hit_points,cells,map25,
             xg,xa,key_passes,duels_won,duels_lost,tackles,interceptions,goals,assists,touches,recoveries,
             stats_json,source,confidence)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (r["player_id"], r["event_id"], r["season"], r["date"], r["opponent"], r["venue"],
             r["competition"], r["minutes"], r["rating"], r["started"],
             r["lineup_pos"], r["pos_class"], r["lineup_order"], r["formation"],
             r["avg_x"], r["avg_y"],
             g["possession"] if g else None,
             g["hit_points"] if g else None, g["cells"] if g else None, canon_map25(g),
             vals["xg"], vals["xa"], vals["key_passes"], vals["duels_won"], vals["duels_lost"],
             vals["tackles"], vals["interceptions"], vals["goals"], vals["assists"],
             vals["touches"], vals["recoveries"],
             r["stats_json"], r["source"], r["confidence"]))
        if g:
            n_grid_merged += 1
    # 위치 행이 없는 고아 그리드 — 행으로 삽입 (표본 손실 금지)
    for (pid, eid), g in grids.items():
        c2.execute("""INSERT INTO player_matches
            (player_id,event_id,season,possession,hit_points,cells,map25,source,confidence)
            VALUES(?,?,?,?,?,?,?,?,?)""",
            (pid, eid, g["season"], g["possession"], g["hit_points"], g["cells"], canon_map25(g),
             g["source"], g["confidence"]))
        n_grid_merged += 1

    # appearances 병합 — (player_id, date)로 event 해소, 잔여는 match_id로 신규 행
    app_rows = c1.execute("""SELECT a.*, m.date mdate, m.season mseason, m.opponent mopp
                             FROM appearances a JOIN matches m ON m.id=a.match_id""").fetchall()
    n_app_merged = n_app_new = 0
    for a in app_rows:
        hit = c2.execute("""SELECT id, map25, pos_class, stats_json FROM player_matches
                            WHERE player_id=? AND date=?""", (a["player_id"], a["mdate"])).fetchone()
        heat_note = " / ".join(x for x in (a["heat_zones"], a["heat_summary"]) if x) or None
        if hit:
            # positions를 기저로 먼저 넣었더라도 appearances의 기능 스탯은 버리면 안 된다.
            # 기존 구현은 xg/xa/key_passes/goals/assists만 병합해 obs#132가 보정한
            # duels/tackles/interceptions와 stats_json 142행을 조용히 유실했다.
            app_stats = json.loads(a["stats_json"]) if a["stats_json"] else {}
            cur_stats = json.loads(hit[3]) if hit[3] else {}
            vals = {k: pick(app_stats, ks) for k, ks in STAT_KEYS.items()}
            merged_stats = {**app_stats, **cur_stats}  # 더 최신인 positions 값 우선
            c2.execute("""UPDATE player_matches SET
                match_id=?, role_note=?, heat_note=?, minutes=COALESCE(?,minutes),
                rating=COALESCE(?,rating),
                pos_class=COALESCE(pos_class,?), map25=COALESCE(map25,?),
                xg=COALESCE(xg,?), xa=COALESCE(xa,?), key_passes=COALESCE(key_passes,?),
                duels_won=COALESCE(duels_won,?), duels_lost=COALESCE(duels_lost,?),
                tackles=COALESCE(tackles,?), interceptions=COALESCE(interceptions,?),
                goals=COALESCE(goals,?), assists=COALESCE(assists,?),
                touches=COALESCE(touches,?), recoveries=COALESCE(recoveries,?),
                stats_json=?
                WHERE id=?""",
                (a["match_id"], a["role"], heat_note, a["minutes"], a["rating"],
                 a["position"], a["heat_map25"],
                 a["xg"] if a["xg"] is not None else vals["xg"],
                 a["xa"] if a["xa"] is not None else vals["xa"],
                 a["key_passes"] if a["key_passes"] is not None else vals["key_passes"],
                 vals["duels_won"], vals["duels_lost"], vals["tackles"],
                 vals["interceptions"],
                 a["goals"] if a["goals"] is not None else vals["goals"],
                 a["assists"] if a["assists"] is not None else vals["assists"],
                 vals["touches"], vals["recoveries"],
                 json.dumps(merged_stats, ensure_ascii=False) if merged_stats else None,
                 hit[0]))
            n_app_merged += 1
        else:
            st = json.loads(a["stats_json"]) if a["stats_json"] else {}
            vals = {k: pick(st, ks) for k, ks in STAT_KEYS.items()}
            c2.execute("""INSERT INTO player_matches
                (player_id,match_id,season,date,opponent,minutes,rating,pos_class,map25,
                 xg,xa,key_passes,duels_won,duels_lost,tackles,interceptions,goals,assists,
                 touches,recoveries,stats_json,role_note,heat_note,source,confidence)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (a["player_id"], a["match_id"], a["mseason"], a["mdate"], a["mopp"],
                 a["minutes"], a["rating"], a["position"], a["heat_map25"],
                 a["xg"], a["xa"], a["key_passes"], vals["duels_won"], vals["duels_lost"],
                 vals["tackles"], vals["interceptions"],
                 a["goals"], a["assists"], vals["touches"], vals["recoveries"],
                 a["stats_json"], a["role"], heat_note, a["source"], a["confidence"]))
            n_app_new += 1
    parity.append(("positions(880)+고아grids+app신규 → player_matches",
                   len(pos_rows), c2.execute("SELECT COUNT(*) FROM player_matches").fetchone()[0]))
    parity.append(("  ├ grids 병합", len(c1.execute("SELECT * FROM player_match_grids").fetchall()),
                   n_grid_merged))
    parity.append(("  └ appearances 병합/신규", len(app_rows), n_app_merged + n_app_new))

    for src, cols_v1, tbl, cols_v2, xform in [
        ("team_match_stats", "*", "team_match_stats", None, "team"),
        ("streaks", "*", "streaks", None, "team"),
        ("player_shot_profile", "*", "player_shot_profile", None, None),
        ("match_streak", "*", "match_streak", None, None),
    ]:
        rows = c1.execute(f"SELECT * FROM {src}").fetchall()
        for r in rows:
            d = dict(r)
            if xform == "team":
                d["team_code"] = d.pop("team")
            cols = ",".join(d.keys())
            c2.execute(f"INSERT INTO {tbl}({cols}) VALUES({','.join('?'*len(d))})", list(d.values()))
        parity.append((src, len(rows), c2.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]))

    # ── 지식 레이어 ─────────────────────────────────────────────────
    rows = c1.execute("SELECT * FROM tactic_observations").fetchall()
    for r in rows:
        c2.execute("""INSERT INTO observations(id,regime_id,season,scope,claim,evidence,source,confidence)
                      VALUES(?,?,?,?,?,?,?,?)""",
                   (r["id"], REGIME[r["team"]], r["season"], r["scope"], r["claim"],
                    r["evidence"], r["source"], r["confidence"]))
    parity.append(("tactic_observations→observations", len(rows),
                   c2.execute("SELECT COUNT(*) FROM observations").fetchone()[0]))

    rows = c1.execute("SELECT * FROM player_duties").fetchall()
    for r in rows:
        c2.execute("""INSERT INTO player_duties(id,regime_id,season,player_id,position,duties,
                      execution,adherence,game_role_implication,source,confidence)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                   (r["id"], REGIME[r["team"]], r["season"], r["player_id"], r["position"],
                    r["duties"], r["execution"], r["adherence"], r["game_role_implication"],
                    r["source"], r["confidence"]))
    parity.append(("player_duties", len(rows), c2.execute("SELECT COUNT(*) FROM player_duties").fetchone()[0]))

    # ── 게임 레이어 ─────────────────────────────────────────────────
    for tbl, key in [("game_roles", None), ("game_role_focus", None),
                     ("game_role_variants", None), ("game_tactic_params", None)]:
        rows = c1.execute(f"SELECT * FROM {tbl}").fetchall()
        for r in rows:
            d = dict(r)
            if tbl == "game_roles":
                d = {"game_version": d["game_version"], "role_id": d["role_id"], "name": d["name"],
                     "name_en": None, "position_type": d["position_type"], "focuses": d["focuses"]}
            cols = ",".join(d.keys())
            c2.execute(f"INSERT INTO {tbl}({cols}) VALUES({','.join('?'*len(d))})", list(d.values()))
        parity.append((tbl, len(rows), c2.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]))

    rows = c1.execute("SELECT * FROM player_fc_stats").fetchall()
    for r in rows:
        d = dict(r)
        d.pop("id")
        cols = ",".join(d.keys())
        c2.execute(f"INSERT INTO player_game_stats({cols}) VALUES({','.join('?'*len(d))})",
                   list(d.values()))
    parity.append(("player_fc_stats→player_game_stats", len(rows),
                   c2.execute("SELECT COUNT(*) FROM player_game_stats").fetchone()[0]))

    # ── 매핑 레이어 ─────────────────────────────────────────────────
    rows = c1.execute("SELECT * FROM team_slots").fetchall()
    FORMATION = {"AVL": "4-2-3-1 Wide", "CHE": "3-4-2-1", "LIV": "4-2-3-1"}
    for r in rows:
        c2.execute("""INSERT INTO slots(regime_id,formation,pos,slot_type,x,y,sort_order,source,confidence)
                      VALUES(?,?,?,?,?,?,?,?,?)""",
                   (REGIME[r["team"]], FORMATION[r["team"]], r["pos"], r["slot_type"],
                    r["x"], r["y"], r["sort_order"], r["source"], r["confidence"]))
    parity.append(("team_slots→slots", len(rows), c2.execute("SELECT COUNT(*) FROM slots").fetchone()[0]))

    # prescriptions ← player_role_map + 정형 필드 추출 (rationale 산문에서 — 마지막 1회)
    RE_N = re.compile(r"(?:n\s*=\s*|실측\s*)(\d+)\s*경기?")
    RE_RT = re.compile(r"(\d+)\s*경기\s*(?:평균|평점)\s*(\d+\.\d+)")
    rows = c1.execute("SELECT * FROM player_role_map").fetchall()
    for r in rows:
        rat = r["rationale"] or ""
        mn = RE_N.search(rat)
        mr = RE_RT.search(rat)
        c2.execute("""INSERT OR REPLACE INTO prescriptions
            (player_id,regime_id,season,game_version,kind,pos_label,x,y,role_id,focus,map25,
             sample_n,avg_rating,rationale)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (r["player_id"], REGIME[r["team"]], r["season"], r["game_version"], r["kind"],
             r["pos_label"], r["x"], r["y"], r["role_id"], r["focus"], r["map25"],
             int(mn.group(1)) if mn else None, float(mr.group(2)) if mr else None, rat))
    parity.append(("player_role_map→prescriptions", len(rows),
                   c2.execute("SELECT COUNT(*) FROM prescriptions").fetchone()[0]))

    # squad_entries ← squad_positions (label → player_id 해소)
    rows = c1.execute("SELECT * FROM squad_positions").fetchall()
    unresolved = []
    for r in rows:
        label = r["label"]
        base = re.sub(r"\((합류확정|신규|보유)\)$", "", label)
        hit = c2.execute("SELECT id FROM players WHERE name_kr=? OR name=?", (base, base)).fetchone()
        if not hit:
            cands = c2.execute("SELECT id FROM players WHERE name_kr LIKE '%'||?||'%'", (base,)).fetchall()
            hit = cands[0] if len(cands) == 1 else None   # 유일 부분일치만 인정 (예: 아브라함→타미 아브라함)
        if not hit:
            unresolved.append(label)
            continue
        c2.execute("""INSERT INTO squad_entries(regime_id,player_id,label,slot_type,lh,map25,
                      rate_v,rate_basis,rate_note,fit_role,fit_focus,fit_sim,source,confidence,sort_order)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                   (REGIME[r["team"]], hit[0], label if label != base else None, r["slot_type"],
                    r["lh"], r["map25"], r["rate_v"], r["rate_basis"], r["rate_note"],
                    r["fit_role"], r["fit_focus"], r["fit_sim"], r["source"], r["confidence"],
                    r["sort_order"]))
    parity.append(("squad_positions→squad_entries", len(rows),
                   c2.execute("SELECT COUNT(*) FROM squad_entries").fetchone()[0]))
    if unresolved:
        print(f"⚠️ squad label 미해소 {len(unresolved)}건: {unresolved} — players에 없음, 수동 확인 필요")

    rows = c1.execute("SELECT * FROM team_tactic_setups").fetchall()
    for r in rows:
        c2.execute("""INSERT INTO team_tactic_setups(id,regime_id,season,game_version,kind,formation,
                      build_up_style,defensive_approach,line_height,tactic_code,rationale,confidence)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                   (r["id"], REGIME[r["team"]], r["season"], r["game_version"], r["kind"],
                    r["formation"], r["build_up_style"], r["defensive_approach"], r["line_height"],
                    r["tactic_code"], r["rationale"], r["confidence"]))
    parity.append(("team_tactic_setups", len(rows),
                   c2.execute("SELECT COUNT(*) FROM team_tactic_setups").fetchone()[0]))

    # ── 이적 레이어 ─────────────────────────────────────────────────
    for tbl in ("transfer_targets", "transfer_outgoing", "transfer_ledger"):
        rows = c1.execute(f"SELECT * FROM {tbl}").fetchall()
        for r in rows:
            d = dict(r)
            d["team_code"] = d.pop("team")
            if tbl == "transfer_targets":
                hit = c2.execute("SELECT id FROM players WHERE name=?", (d["name"],)).fetchone()
                d["player_id"] = hit[0] if hit else None
            cols = ",".join(d.keys())
            c2.execute(f"INSERT INTO {tbl}({cols}) VALUES({','.join('?'*len(d))})", list(d.values()))
        parity.append((tbl, len(rows), c2.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]))

    # v1에서 의도적으로 버리는 것 (0행 또는 폐기 확정)
    print("ℹ️ 이관 제외: ingame_checks(0행 — 게임 내 검증 폐기 유지)")

    c2.execute("INSERT INTO _migration_log VALUES(?,?,?)",
               (date.today().isoformat(), str(V1), "full rebuild"))
    v2.commit()

    # ── 검증 ────────────────────────────────────────────────────────
    print(f"\nℹ️ 인코딩 정규화: v1 map25와 달라진 그리드 {n_reencoded}행 (cells에서 정본 재인코딩)")
    print("\n행수 대조 (v1 → v2):")
    ok = True
    for name, a, b in parity:
        flag = "✅" if (b >= a or name.startswith(" ")) else "⛔"
        if flag == "⛔":
            ok = False
        print(f"  {flag} {name:<44} {a:>5} → {b}")

    # 인코딩 회귀 — 이관 그리드 전수
    bad = 0
    for cells_s, m25 in c2.execute(
            "SELECT cells, map25 FROM player_matches WHERE cells IS NOT NULL AND map25 IS NOT NULL"):
        if encode([int(x) for x in cells_s.split(",")]) != m25:
            bad += 1
    n_g = c2.execute("SELECT COUNT(*) FROM player_matches WHERE map25 IS NOT NULL").fetchone()[0]
    print(f"\n인코딩 회귀: 그리드 {n_g}행 중 불일치 {bad} {'✅' if bad == 0 else '⛔'}")
    ok &= (bad == 0)

    # 커널 앵커 — DB 변형으로 캐시 measured:season RM .835 재현 (게이트의 v2 이관)
    def decode(code):
        return [1.0 if ch == "X" else int(ch) / 10 for ch in code]

    def cos(a, b):
        dot = sum(p * q for p, q in zip(a, b))
        na = math.sqrt(sum(p * p for p in a))
        nb = math.sqrt(sum(q * q for q in b))
        return dot / (na * nb) if na and nb else 0.0

    grp = dict(c2.execute("SELECT role_id, position_type FROM game_roles WHERE game_version='FC26'"))
    cash = c2.execute("""SELECT map25 FROM prescriptions p JOIN players pl ON pl.id=p.player_id
                         WHERE pl.name='Matty Cash' AND p.kind='measured:season'""").fetchone()
    v = decode(cash[0])
    best = (None, None, -1.0)
    for role, focus, px, k25 in c2.execute(
            "SELECT role_id, focus, pitch_x, kernel25 FROM game_role_variants WHERE game_version='FC26'"):
        if grp.get(role) != "WM":
            continue
        pass  # 변형은 슬롯 x=85 최근접 선택 — 아래에서 그룹별로 처리
    # 역할·포커스별 x=85 최근접 변형 선택 후 코사인
    from collections import defaultdict
    variants = defaultdict(list)
    for role, focus, px, k25 in c2.execute(
            "SELECT role_id, focus, pitch_x, kernel25 FROM game_role_variants WHERE game_version='FC26'"):
        if grp.get(role) == "WM":
            variants[(role, focus)].append((px, k25))
    for (role, focus), lst in variants.items():
        px, k25 = min(lst, key=lambda t: abs(t[0] - 85))
        s = cos(v, decode(k25))
        if s > best[2]:
            best = (role, focus, s)
    anchor_ok = best[0] == "wm_widemid" and best[1] == "Support" and abs(best[2] - 0.835) < 0.001
    print(f"커널 앵커(캐시 RM): {best[0]}/{best[1]} {best[2]:.3f} "
          f"{'✅ (.835 재현 — DB 커널 = 툴 커널)' if anchor_ok else '⛔ 기대 wm_widemid/Support .835'}")
    ok &= anchor_ok

    # obs 연속성
    lo, hi, cnt = c2.execute("SELECT MIN(id), MAX(id), COUNT(*) FROM observations").fetchone()
    obs_ok = (lo, hi, cnt) == (1, 141, 141)
    print(f"obs 연속성: {lo}..{hi} ({cnt}개) {'✅' if obs_ok else '⚠️ 갭 존재 — v1과 대조할 것'}")

    v1.close()
    v2.close()
    print(f"\n{'✅ 마이그레이션 완료' if ok else '⛔ 검증 실패 — 위 항목 확인'}: {V2}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
