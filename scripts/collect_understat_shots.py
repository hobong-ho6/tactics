#!/usr/bin/env python3
"""Understat 슛맵 대량 수집 — 축11(`player_shot_profile`)을 채운다.

왜 Understat인가 (2026-08-21 신설):
  이 작업 PC에서 **SofaScore·WhoScored·FBref·sofifa가 전부 403**이다(curl·Playwright
  헤드리스·헤드풀·브라우저 MCP 전부 동일 — 자동화 탐지가 아니라 네트워크/IP 단위 차단).
  축11 슛맵의 기존 원천이 SofaScore `/event/{eid}/shotmap`이라 지금은 경로가 없다.
  Understat은 200으로 열리고 **슛 단위 좌표·xG·슛타입·상황을 커리어 전체로** 준다.
  ⛔ 단 커버리지가 **빅5 리그(+RFPL)** 뿐이다 — 챔피언십·에레디비시 등은 없다.

⛔ curl로는 안 된다 — `/getPlayerData/{id}`가 오리진 밖에서는 에러 페이지를 준다.
   `scripts/collect_fotmob_players.py`와 같은 Playwright 오리진 fetch 패턴을 쓴다.

⚠️ `player_shot_profile`은 PK가 `player_id`라 **선수당 1행**이다. 기존 9행은 SofaScore
   sweep 산출물이므로 이 스크립트는 **행이 없는 선수만 INSERT**한다(불변규칙 2 — 재작성 금지).
   기존 행을 Understat 값으로 교체할지는 세션·사용자 판단 사항이다.

⚠️ 좌표 규약: Understat X∈[0,1](1=상대 골라인) · Y∈[0,1](폭). 105×68m로 환산한다.
   `mean_y`는 **Understat 핸디드니스 그대로 Y×100**이다 — SofaScore 기반 기존 9행의
   좌우 부호와 같다는 보장이 없다(docs/30 ⑨). 좌우 편향 비교에 쓸 때 `source`를 확인할 것.

사용:
    .venv/bin/python scripts/collect_understat_shots.py --team AVL --include-targets --dry-run
    .venv/bin/python scripts/collect_understat_shots.py --players 16 23 --seasons 2025 2024
    .venv/bin/python scripts/collect_understat_shots.py --team AVL --all-career
"""
import argparse
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "tactics.db"

PITCH_L, PITCH_W = 105.0, 68.0
BOX_X, BOX_HALF_W = 16.5, 20.16        # 페널티박스 16.5m × 40.32m
SIX_X, SIX_HALF_W = 5.5, 9.16          # 골에어리어 5.5m × 18.32m

# 오리진 fetch 2종. 검색은 GET /main/getPlayersName/{query}, 데이터는 GET /getPlayerData/{id}.
JS_SEARCH = """async (q) => {
  const r = await fetch('/main/getPlayersName/' + encodeURIComponent(q),
                        {headers: {'x-requested-with': 'XMLHttpRequest'}});
  if (r.status !== 200) return {err: 'search HTTP ' + r.status};
  const d = await r.json();
  return {players: (d.response && d.response.players) || []};
}"""

JS_SHOTS = """async (uid) => {
  const r = await fetch('/getPlayerData/' + uid, {headers: {'x-requested-with': 'XMLHttpRequest'}});
  if (r.status !== 200) return {err: 'HTTP ' + r.status};
  const d = await r.json();
  return {shots: (d.shots || []).map(s => ({
    m: s.match_id, se: s.season, x: +s.X, y: +s.Y, xg: +s.xG,
    t: s.shotType, r: s.result, si: s.situation}))};
}"""


def norm(s):
    """비교용 정규화 — 발음기호 제거 + 소문자. 'Victor Lindelof' ↔ 'Victor Lindelöf'."""
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s)
                   if not unicodedata.combining(c)).casefold().strip()


def resolve(pg, en):
    """이름 → (understat_id, 표시명, 소속, 매칭규칙) 또는 (None, 후보목록, 사유).

    ⚠️ 완전일치가 없을 때만 **유일 접두사 일치**를 허용한다('Ezri Konsa' → 'Ezri Konsa Ngoyo').
       유일하지 않으면 넘기지 않는다 — 동명이인 오매칭이 조용히 행을 덮는다(2026-08-19 규약).
    """
    seen, cands = set(), []
    for q in [en, en.split()[-1]]:                 # 풀네임 → 실패 시 성만 (Matty Cash·Cissé)
        for c in pg.evaluate(JS_SEARCH, q).get("players", []):
            if c["id"] not in seen:
                seen.add(c["id"])
                cands.append(c)
    exact = [c for c in cands if norm(c["player"]) == norm(en)]
    if len(exact) == 1:
        return int(exact[0]["id"]), exact[0]["player"], exact[0]["team"], "완전일치"
    pref = [c for c in cands if norm(c["player"]).startswith(norm(en))]
    if not exact and len(pref) == 1:
        return int(pref[0]["id"]), pref[0]["player"], pref[0]["team"], "접두사 유일일치"
    return None, cands, ("완전일치 다수" if len(exact) > 1 else "일치 없음/모호"), None


def season_label(codes):
    """Understat 시즌(시작연도 문자열) → 우리 표기. ['2025','2024'] → '2024-25~2025-26'."""
    ys = sorted(int(c) for c in codes)
    lab = [f"{y}-{str(y + 1)[2:]}" for y in ys]
    return lab[0] if len(lab) == 1 else f"{lab[0]}~{lab[-1]}"


def aggregate(shots):
    n = len(shots)
    dist, ys, box, six, head, goals, xg = [], [], 0, 0, 0, 0, 0.0
    for s in shots:
        dx = (1.0 - s["x"]) * PITCH_L                  # 골라인까지 거리
        dy = (s["y"] - 0.5) * PITCH_W                  # 골 중앙 기준 좌우
        dist.append((dx ** 2 + dy ** 2) ** 0.5)
        ys.append(s["y"] * 100)
        if dx <= BOX_X and abs(dy) <= BOX_HALF_W:
            box += 1
        if dx <= SIX_X and abs(dy) <= SIX_HALF_W:
            six += 1
        if s["t"] == "Head":
            head += 1
        if s["r"] == "Goal":
            goals += 1
        xg += s["xg"]
    return {
        "events_n": len({s["m"] for s in shots}), "shots": n,
        "xg_sum": round(xg, 2), "box_n": box, "sixyard_n": six,
        "headers": head, "goals": goals,
        "mean_dist": round(sum(dist) / n, 1), "mean_y": round(sum(ys) / n, 1),
    }


def targets(con, team, players, include_targets):
    # --dry-run에서 아직 컬럼이 없을 수 있다. 없으면 NULL로 읽어 매핑을 메모리에서만 쓴다.
    has = "understat_id" in {r[1] for r in con.execute("PRAGMA table_info(players)")}
    uid = "p.understat_id" if has else "NULL"
    if players:
        q = (f"SELECT id, COALESCE(name_kr, name), name, {uid.replace('p.', '')} FROM players "
             f"WHERE id IN ({','.join('?' * len(players))})")
        return con.execute(q, players).fetchall()
    if not team:
        sys.exit("--team 또는 --players 중 하나는 필요하다")
    rid = con.execute("SELECT id FROM regimes WHERE team_code=?", (team,)).fetchone()
    if not rid:
        sys.exit(f"regimes에 team_code={team} 없음")
    sql = f"""SELECT p.id, COALESCE(p.name_kr, p.name), p.name, {uid} FROM players p
             WHERE p.id IN (SELECT player_id FROM squad_entries WHERE regime_id=?)"""
    args = [rid[0]]
    if include_targets:
        sql += (" OR p.id IN (SELECT player_id FROM transfer_targets"
                " WHERE team_code=? AND player_id IS NOT NULL)")
        args.append(team)
    return con.execute(sql + " ORDER BY p.id", args).fetchall()


def ensure_column(con):
    cols = {r[1] for r in con.execute("PRAGMA table_info(players)")}
    if "understat_id" in cols:
        return
    con.execute("ALTER TABLE players ADD COLUMN understat_id INTEGER")
    con.execute("INSERT INTO _migration_log(run_at, v1_path, note) VALUES(?,?,?)",
                ("016-players-understat-id", "2026-08-21",
                 "players.understat_id 추가 — 축11 슛맵의 Understat 경로"
                 " (SofaScore·WhoScored·FBref 전부 403인 환경의 대체 원천)"))
    con.commit()
    print("스키마: players.understat_id 추가 (016)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", help="팀 코드 (regime의 squad_entries)")
    ap.add_argument("--players", nargs="*", type=int, help="players.id 직접 지정")
    ap.add_argument("--include-targets", action="store_true",
                    help="transfer_targets 후보도 포함 (player_id가 채워진 행만)")
    ap.add_argument("--seasons", nargs="*", default=["2025"],
                    help="Understat 시즌(시작연도). 기본 2025 = 25/26")
    ap.add_argument("--all-career", action="store_true", help="시즌 필터 없이 커리어 전량")
    ap.add_argument("--min-shots", type=int, default=5,
                    help="이 미만 표본은 적재하지 않는다 (평균 거리가 무의미해진다)")
    ap.add_argument("--dry-run", action="store_true", help="DB에 쓰지 않고 요약만 출력")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    if not a.dry_run:
        ensure_column(con)
    rows = targets(con, a.team, a.players, a.include_targets)
    if not rows:
        sys.exit("대상 0명")

    existing = {r[0] for r in con.execute("SELECT player_id FROM player_shot_profile")}
    todo = [r for r in rows if r[0] not in existing]
    print(f"대상 {len(rows)}명 · 기존 행 보유 {len(rows) - len(todo)}명은 건너뛴다"
          f"(PK가 player_id라 덮어쓰기가 되므로 — 교체는 사용자 판단)")
    if not todo:
        sys.exit("적재 대상 0명")

    from playwright.sync_api import sync_playwright
    results, mapped, unresolved = [], [], []
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page()
        pg.goto("https://understat.com/", wait_until="domcontentloaded", timeout=60_000)
        for pid, kr, en, uid in todo:
            if not uid:
                uid, label, team, rule = resolve(pg, en)
                if not uid:
                    unresolved.append((pid, kr, en, label[:6], team))  # label=후보 · team=사유
                    continue
                mapped.append((pid, kr, uid, team))
                print(f"  매핑 {kr}({pid}) → understat {uid} · {label} · {team}"
                      f" [{rule}] — ⚠️ 소속으로 동명이인 확인할 것")
            r = pg.evaluate(JS_SHOTS, str(uid))
            if r.get("err"):
                print(f"  ⚠️ {kr}({pid}) {r['err']}")
                continue
            shots = r["shots"] if a.all_career else [
                s for s in r["shots"] if s["se"] in set(a.seasons)]
            if len(shots) < a.min_shots:
                print(f"  ⚠️ {kr}({pid}) 표본 {len(shots)}슛 < {a.min_shots} — 건너뜀"
                      f" (커리어 전체 {len(r['shots'])}슛)")
                continue
            agg = aggregate(shots)
            seasons = {s["se"] for s in shots}
            results.append((pid, kr, uid, agg, seasons))
            print(f"  {kr}: {agg['shots']}슛 / {agg['events_n']}경기 · xG {agg['xg_sum']}"
                  f" · 박스 {agg['box_n']} · 6야드 {agg['sixyard_n']} · 헤더 {agg['headers']}"
                  f" · 골 {agg['goals']} · 평균거리 {agg['mean_dist']}m · mean_y {agg['mean_y']}")
        br.close()

    if unresolved:
        print("\n⛔ understat_id 미해결 — 세션에서 처리할 것"
              " (players.understat_id를 채우고 재실행하면 멱등하게 이어진다):")
        for pid, kr, en, cands, why in unresolved:
            hint = ", ".join(f"{c['player']}({c['id']}, {c['team']})" for c in cands) or "검색 0건"
            print(f"  {kr}({pid}) [{en}] {why} → {hint}")

    if a.dry_run:
        print("\n--dry-run — DB에 쓰지 않았다.")
        return

    cur = con.cursor()
    for pid, kr, uid in ((m[0], m[1], m[2]) for m in mapped):
        cur.execute("UPDATE players SET understat_id=? WHERE id=?", (uid, pid))
    ins = 0
    for pid, kr, uid, agg, seasons in results:
        window = f"{season_label(seasons)} ({agg['events_n']} events, Understat)"
        src = (f"understat.com/getPlayerData/{uid} (슛 단위 좌표·xG,"
               f" scripts/collect_understat_shots.py)")
        conf = ("MEDIUM — Understat 좌표계(X,Y∈[0,1]→105×68m) 환산값이다."
                " mean_y는 Understat 핸디드니스 그대로라 SofaScore 기반 행과 좌우 부호가"
                " 같다는 보장이 없다. 커버리지는 빅5 리그 한정 — 타 리그 출전분은 빠져 있다.")
        cur.execute(
            """INSERT INTO player_shot_profile(player_id,window,events_n,shots,xg_sum,box_n,
               sixyard_n,headers,goals,mean_dist,mean_y,source,confidence)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(player_id) DO NOTHING""",
            (pid, window, agg["events_n"], agg["shots"], agg["xg_sum"], agg["box_n"],
             agg["sixyard_n"], agg["headers"], agg["goals"], agg["mean_dist"],
             agg["mean_y"], src, conf))
        ins += cur.rowcount
    con.commit()
    print(f"\n적재: player_shot_profile +{ins}행 · understat_id +{len(mapped)}")
    print("다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
