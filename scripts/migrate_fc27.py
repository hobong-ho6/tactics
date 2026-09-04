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

def apply_roles(con, items):
    print("⛔ --apply 는 아직 구현을 비워 두었다 — fut.gg FC27 응답 스키마를 실제로 본 뒤 필드 매핑(id·slug·position_type·heatmap→kernel25, 좌표 y=0 최전방/x=0 좌측, 0/30/60/100↔0/3/6/X)을 채운다(docs/20 「대상 시스템의 구조」).")
    print("   FC26 행은 건드리지 않으며, INSERT 전 드라이런 전항 ✅와 사용자 승인이 필요하다.")
    return False

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--roles", help="fut.gg /api/fut/roles/ FC27 응답 JSON 파일")
    ap.add_argument("--check", action="store_true", help="역할 JSON 구조 검증만")
    ap.add_argument("--apply", action="store_true", help="검증 통과 시 FC27 행 적재(사용자 승인 후)")
    a = ap.parse_args()
    con = sqlite3.connect(DB)
    ok = dry_run(con)
    if a.roles:
        items = check_roles(a.roles)
        if a.apply and items and ok:
            apply_roles(con, items)
    sys.exit(0 if ok else 1)
