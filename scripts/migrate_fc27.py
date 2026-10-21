#!/usr/bin/env python3
"""FC27 마이그레이션 점검·실행 도구 (docs/21 체크리스트의 기계 부분).

기본은 **드라이런(읽기 전용)** — 전제조건과 결손을 표로 보고만 한다.
`--apply`는 fut.gg 역할 JSON을 검증해 game_roles/game_role_focus/game_role_variants FC27 행을
만들 때만 쓰며, 그 전에 반드시 이 스크립트의 드라이런이 전부 ✅여야 한다.

⛔ 값을 발명하지 않는다 — 역할 목록·커널은 fut.gg /api/fut/roles/ FC27 응답에서만 온다.
⛔ FC26 행은 절대 건드리지 않는다(불변규칙 2 — 버전 추가 = 행 추가).

사용:
  python3 scripts/migrate_fc27.py                 # 드라이런 점검표
  python3 scripts/migrate_fc27.py --roles roles.json --check   # fut.gg JSON 구조·카운트 검증만
  python3 scripts/migrate_fc27.py --roles roles.json --apply   # 검증 통과 시 FC27 행 INSERT (사용자 승인 후)
"""
import argparse, json, sqlite3, sys
from pathlib import Path
import sys as _sys_db, pathlib as _pl_db; _sys_db.path.insert(0, str(_pl_db.Path(__file__).resolve().parent.parent))  # noqa: E401,E702
from core.db import connect as connect_db  # noqa: E402  ⭐ DB 연결 정본(대기·작성 중 표시)

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "tactics.db"
GV_NEW, GV_BASE = "FC27", "FC26"
BASE_EXPECTED = (37, 85, 217)   # core/kernel.py EXPECTED[FC26]와 동기

def q(con, sql, *a): return con.execute(sql, a).fetchall()

def dry_run(con):
    ok = True
    def line(flag, msg):
        nonlocal ok
        ok &= flag
        print(("✅" if flag else "⛔"), msg)

    print(f"== FC27 마이그레이션 드라이런 ({DB.name}) ==")
    gv = q(con, "SELECT code, released FROM game_versions WHERE code=?", GV_NEW)
    line(bool(gv), f"game_versions에 {GV_NEW} 행 — {gv[0][1] if gv else '없음'}")

    counts = {t: q(con, f"SELECT COUNT(*) FROM {t} WHERE game_version=?", GV_NEW)[0][0]
              for t in ("game_roles", "game_role_focus", "game_role_variants", "game_tactic_params",
                        "game_system_changes", "player_game_stats")}
    print("   FC27 행 수:", counts)
    line(counts["game_system_changes"] > 0, "game_system_changes FC27 사전 조사 행 존재(obs#445)")
    line(counts["game_roles"] == 0 or counts["game_role_focus"] > 0,
         "역할 행이 있으면 포커스 행도 있어야 한다(반쪽 적재 금지)")

    dup = q(con, """SELECT name_kr, COUNT(*) c FROM players WHERE name_kr IS NOT NULL AND trim(name_kr)!=''
                    GROUP BY name_kr HAVING c>1""")
    line(not dup, f"players.name_kr 중복 0건 (docs/21 함정 — 현재 {len(dup)}건 {dup[:5] if dup else ''})")

    both = q(con, """WITH a AS (SELECT DISTINCT player_id FROM player_game_stats WHERE game_version=? AND player_id IS NOT NULL),
                        b AS (SELECT DISTINCT player_id FROM player_game_stats WHERE game_version=? AND player_id IS NOT NULL)
                     SELECT (SELECT COUNT(*) FROM a), (SELECT COUNT(*) FROM b),
                            (SELECT COUNT(*) FROM a WHERE player_id IN (SELECT player_id FROM b))""", GV_BASE, GV_NEW)[0]
    print(f"   게임스탯 커버리지: FC26 {both[0]}명 · FC27 {both[1]}명 · 교집합(델타 가능) {both[2]}명")
    ps_null = q(con, "SELECT COUNT(*) FROM player_game_stats WHERE game_version=? AND (playstyles IS NULL OR playstyles='')", GV_NEW)[0][0]
    print(f"   FC27 playstyles NULL {ps_null}행 — 09-10 전체 DB 공개 전이면 정상(결손≠0)")

    base = tuple(q(con, f"SELECT (SELECT COUNT(*) FROM game_roles WHERE game_version=?),"
                          f"(SELECT COUNT(*) FROM game_role_focus WHERE game_version=?),"
                          f"(SELECT COUNT(*) FROM game_role_variants WHERE game_version=?)", GV_BASE, GV_BASE, GV_BASE)[0])
    line(base == BASE_EXPECTED, f"FC26 기준 커널 구조 {base} == {BASE_EXPECTED} (FC26 앵커 불변 확인)")

    print("\n== 다음 트리거 ==")
    print(" 1) 09-10 EA 전체 DB(PlayStyles 포함) → player_game_stats FC27 새 roster_date 행 + playstyles 채움")
    print(" 2) 09-18 얼리액세스 → fut.gg /api/fut/roles/ FC27 응답 확보 → 이 스크립트 --roles … --check")
    print(" 3) 카운트 확정 → core/kernel.py EXPECTED['FC27'] 추가 → gates.py G1/G5에 FC27 앵커 '새 행' → export → kernels/FC27.json")
    print("\n결과:", "드라이런 전항 통과 ✅" if ok else "미충족 항목 있음 ⛔")
    return ok

def check_roles(path):
    """fut.gg roles JSON의 최소 구조 검증 + FC26 대비 diff 요약. 쓰기 없음."""
    data = json.loads(Path(path).read_text())
    items = data if isinstance(data, list) else data.get("data") or data.get("roles") or []
    if not items:
        print("⛔ 역할 항목이 비어 있다 — JSON 루트 구조를 확인할 것(list 또는 {data:[…]})"); return None
    ids = [it.get("id") for it in items]
    slugs = [it.get("slug") for it in items]
    print(f"역할 항목 {len(items)}개 · id 유일 {len(set(ids))==len(ids)} · slug 유일 {len(set(slugs))==len(slugs)} (⚠️ 키는 id — obs#92)")
    focus_n = sum(len(it.get("focuses") or it.get("focus") or []) for it in items)
    print(f"포커스 합계 {focus_n} (FC26: 85) · 역할 {len(items)} (FC26: 37)")
    return items

POS_GROUP = {"LB": "FB", "RB": "FB", "LM": "WM", "RM": "WM", "LW": "W", "RW": "W", "CDM": "DM"}
HEAT = {0: "0", 30: "3", 60: "6", 100: "X"}
COPY_TABLES = ("game_roles", "game_role_focus", "game_role_variants", "game_role_groups")


def _k25(heat):
    """fut.gg 히트맵(x 0=좌 · y 0=최전방 · 0/30/60/100) → kernel25 문자열(행 우선 · 0/3/6/X)."""
    g = [["?"] * 5 for _ in range(5)]
    for c in heat:
        g[c["y"]][c["x"]] = HEAT.get(c["value"], "?")
    return "".join("".join(r) for r in g)


def _mirror(k):
    return "".join(k[r * 5:(r + 1) * 5][::-1] for r in range(5))


def apply_roles(con, items, src_note):
    """FC27 역할 응답을 FC26 행과 **칸 단위로** 대조하고, 전항 일치할 때만 FC26 행을 FC27로 승계한다.

    (2026-10-22 구현 · 사용자 지시 「FC27 역할표가 적재 안 되어 있다면 적재해」)
    ⭐ 실측: fut.gg `/api/fut/roles/`는 `?game=` 인자를 무시하고 **현행(FC27) 한 벌**만 준다 — 37역할·85포커스·
       위치 변형 히트맵 217개가 FC26 적재본과 원문·히트맵까지 같았다(차이는 아래 오염 2건뿐).
    ⛔ 하나라도 다르면 **쓰지 않고 멈춘다** — 다른 칸을 FC26 값으로 메우면 발명이 된다(불변규칙 3).
    ⭐ 오염 판정: 그 역할의 FC26 설명과 다르고 **다른 역할의 FC26 설명과 같으면** fut.gg 쪽 혼입으로 보고 뺀다
       (실측: CAM 플레이메이커 목록 앞머리에 윙어 Balanced·Attack 설명문이 그대로 붙어 있었다).
    ⭐ 한국어 해설 칸(identity_kr·movement_kr·장면 등)은 우리 분석이라 FC26 판을 그대로 승계한다 — source에 적는다."""
    if con.execute("SELECT COUNT(*) FROM game_roles WHERE game_version=?", (GV_NEW,)).fetchone()[0]:
        print(f"⛔ {GV_NEW} 역할 행이 이미 있다 — 덮지 않는다(불변규칙 2)"); return False
    pt = dict(q(con, "SELECT role_id, position_type FROM game_roles WHERE game_version=?", GV_BASE))
    base, kern, by_desc = {}, {}, {}
    for rid, f, n, d, pl, eq, ng, k in q(con, """SELECT role_id, focus, ea_role_name, description, plus, equal, negative,
                                                 kernel25 FROM game_role_focus WHERE game_version=?""", GV_BASE):
        key = (pt[rid], n, f)
        base[key] = (d, json.loads(pl or "[]"), json.loads(eq or "[]"), json.loads(ng or "[]"))
        kern.setdefault(key, set()).add(k)
        by_desc.setdefault(d, set()).add(key)
    names = {rid: (pt[rid], n) for rid, n in q(con, "SELECT role_id, ea_role_name FROM game_role_focus WHERE game_version=?", GV_BASE)}
    for rid, f, k in q(con, "SELECT role_id, focus, kernel25 FROM game_role_variants WHERE game_version=?", GV_BASE):
        kern.setdefault(names[rid] + (f,), set()).add(k)

    seen, junk, bad = set(), [], []
    for it in items:
        grp = POS_GROUP.get(it["positionName"], it["positionName"])
        for fo in it.get("focus") or []:
            key = (grp, it["cleanName"], fo["name"])
            ch = fo.get("characteristics") or {}
            got = (fo["description"], ch.get("plus") or [], ch.get("equal") or [], ch.get("negative") or [])
            if base.get(key, (None,))[0] != got[0] and by_desc.get(got[0], set()) - {key}:
                junk.append((it["positionName"], key[1], key[2], sorted(by_desc[got[0]])[0])); continue
            if key not in base:
                bad.append(("FC26에 없는 역할·포커스", it["positionName"], key)); continue
            if base[key] != got:
                bad.append(("설명·특성 다름", it["positionName"], key, got)); continue
            kk = _k25(fo["heatmap"])
            if kk not in kern[key] and _mirror(kk) not in kern[key]:
                bad.append(("히트맵 다름", it["positionName"], key, kk)); continue
            seen.add(key)
    # ⭐ 응답 내부 좌우 불일치 — 같은 역할·포커스의 다른 쪽(LM↔RM 등) 항목이 FC26과 일치하면 응답이 스스로 갈린 것이다
    #    (실측 2026-10-22: RM·RB 쪽 특성 태그 4건만 달랐고 LM·LB 쪽은 FC26 그대로). 설명문·히트맵이 같으면
    #    FC26 값으로 승계하되 그 행 note에 갈린 값을 원문 그대로 남긴다(불변규칙 3 — 충돌을 기록).
    intra = [b for b in bad if b[0] == "설명·특성 다름" and b[2] in seen and b[3][0] == base[b[2]][0]]
    bad = [b for b in bad if b not in intra]
    missing = sorted(set(base) - seen)
    print(f"대조: 일치 {len(seen)}/{len(base)} 포커스 · 오염 제외 {len(junk)} · 응답 내부 좌우 불일치 {len(intra)} · "
          f"불일치 {len(bad)} · FC27 응답에 없는 FC26 포커스 {len(missing)}")
    for b in intra:
        print(f"   ↔️ 좌우 불일치: {b[1]} {b[2][1]} {b[2][2]} — 반대쪽은 FC26과 같다 · 이쪽 특성 {b[3][1:]}")
    for j in junk:
        print(f"   🧹 오염 제외: {j[0]} {j[1]} {j[2]} — 설명문이 {j[3]}의 것")
    for b in bad:
        print("   ⛔", *b)
    for m in missing:
        print("   ⛔ 응답에 없음:", m)
    if bad or missing:
        print("⛔ 전항 일치가 아니다 — 쓰지 않는다. 다른 칸은 fut.gg 응답에서 새로 매핑해야 한다(발명 금지)."); return False

    note = (f"{src_note} — FC26 행과 원문·특성·히트맵 전항 일치 확인 후 승계(migrate_fc27.py --apply"
            f" · 오염 제외 {len(junk)}건 · 좌우 불일치 {len(intra)}건은 해당 행 note). 한국어 해설 칸은 FC26 판 그대로")
    for t in COPY_TABLES:
        cols = [r[1] for r in con.execute(f"PRAGMA table_info({t})")]
        sel = ", ".join("?" if c == "game_version" else
                        (f"COALESCE({c}, '') || ' ‖ ' || ?" if c == "source" else c) for c in cols)
        args = [GV_NEW] + ([note] if "source" in cols else []) + [GV_BASE]
        con.execute(f"INSERT INTO {t}({', '.join(cols)}) SELECT {sel} FROM {t} WHERE game_version=?", args)
    rid_of = {v: k for k, v in names.items()}
    for b in intra:
        con.execute("UPDATE game_role_focus SET note = COALESCE(note || ' ‖ ', '') || ? "
                    "WHERE game_version=? AND role_id=? AND focus=?",
                    (f"⚠️ fut.gg FC27 응답 내부 좌우 불일치({src_note}): {b[1]} 항목만 특성이 plus {b[3][1]} · equal {b[3][2]} · "
                     f"negative {b[3][3]} — 반대쪽 항목이 FC26과 같아 FC26 값을 승계. 인게임 확인 전까지 특성 태그는 LOW",
                     GV_NEW, rid_of[b[2][:2]], b[2][2]))
    con.commit()
    got = tuple(q(con, "SELECT (SELECT COUNT(*) FROM game_roles WHERE game_version=?),"
                       "(SELECT COUNT(*) FROM game_role_focus WHERE game_version=?),"
                       "(SELECT COUNT(*) FROM game_role_variants WHERE game_version=?)", GV_NEW, GV_NEW, GV_NEW)[0])
    print(f"✅ {GV_NEW} 적재 {got} (역할·포커스·변형) · 그룹 장면표 포함 — 다음: core/kernel.py EXPECTED['{GV_NEW}'] 등록")
    return True

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--roles", help="fut.gg /api/fut/roles/ FC27 응답 JSON 파일")
    ap.add_argument("--check", action="store_true", help="역할 JSON 구조 검증만")
    ap.add_argument("--apply", action="store_true", help="검증 통과 시 FC27 행 적재(사용자 승인 후)")
    ap.add_argument("--src", default="fut.gg /api/fut/roles/", help="적재 행 source에 덧붙일 수집 출처·날짜")
    a = ap.parse_args()
    con = connect_db(DB)
    ok = dry_run(con)
    if a.roles:
        items = check_roles(a.roles)
        if a.apply and items and ok:
            apply_roles(con, items, a.src)
    sys.exit(0 if ok else 1)
