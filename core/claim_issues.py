"""판정 쟁점(claim_issues) 트리거 판정 정본 (2026-10-21 · migration 114).

왜: 영상 구현 주장 PENDING의 「판정 조건」이 산문에만 있어 아무도 닫지 않았다(165건). 조건을 셀 수 있는 트리거로 두고
  여기 한 곳에서 센다 — scripts/claim_issues.py(목록·닫기)·scripts/gates.py G39(기한 초과 차단)·core/export.py(화면 진행도)가
  모두 이 모듈을 쓴다(불변규칙 4 — 세션 내 재구현 금지).

트리거:
  matches       — 팀 공식전(친선·대표팀 제외, core.aggregate.NON_OFFICIAL_COMP) 경기 수. comp='league'면 리그만.
  player_starts — 선수 공식전 선발 수(pos_class CSV로 좁힐 수 있다).
  date          — 그 날짜가 지나면.
「since 이후」는 date > since(당일 경기는 판정 근거가 이미 반영된 경우가 많아 다음 경기부터 센다).
"""
import datetime as dt

from core.aggregate import NON_OFFICIAL_COMP

LEAGUE_COMP = {"AVL": "Premier League", "CHE": "Premier League", "LIV": "Premier League", "ATM": "LaLiga"}
GRACE_DAYS = 7          # 트리거가 찬 뒤 이 기간이 지나도 열려 있으면 G39가 막는다


def _comp_sql(comp, team):
    if comp == "league":
        return "competition = ?", [LEAGUE_COMP.get(team, "Premier League")]
    return ("competition NOT IN (%s)" % ",".join("?" * len(NON_OFFICIAL_COMP))), list(NON_OFFICIAL_COMP)


def _dates(con, issue):
    """트리거를 세는 경기 날짜 목록(오름차순). date 트리거는 None."""
    k = issue["trigger_kind"]
    if k == "date":
        return None
    csql, cpar = _comp_sql(issue["trigger_comp"], issue["team_code"])
    if k == "matches":
        rows = con.execute(f"SELECT date FROM matches WHERE team_code=? AND date>? AND {csql} ORDER BY date",
                           [issue["team_code"], issue["since"], *cpar]).fetchall()
    else:
        pos = [p.strip() for p in (issue["trigger_pos"] or "").split(",") if p.strip()]
        psql = (" AND pos_class IN (%s)" % ",".join("?" * len(pos))) if pos else ""
        rows = con.execute(f"""SELECT DISTINCT date FROM player_matches WHERE player_id=? AND started=1 AND date>?
                               AND {csql}{psql} ORDER BY date""",
                           [issue["trigger_player_id"], issue["since"], *cpar, *pos]).fetchall()
    return [r[0] for r in rows]


def progress(con, issue, today=None):
    """{'count', 'need', 'due', 'due_date'} — due_date = 트리거가 찬 날(아직이면 None)."""
    today = today or dt.date.today().isoformat()
    if issue["trigger_kind"] == "date":
        due = today > issue["trigger_date"]
        return {"count": None, "need": None, "due": due, "due_date": issue["trigger_date"] if due else None}
    ds = _dates(con, issue)
    n = issue["trigger_n"]
    due = len(ds) >= n
    return {"count": len(ds), "need": n, "due": due, "due_date": ds[n - 1] if due else None}


def overdue(con, issue, today=None):
    """트리거가 찬 뒤 GRACE_DAYS가 지나도 열려 있는가(보류 팀 제외)."""
    if issue["status"] != "open" or issue["hold"]:
        return False
    p = progress(con, issue, today)
    if not p["due"]:
        return False
    today = dt.date.fromisoformat(today or dt.date.today().isoformat())
    # 기한은 「트리거가 찬 날」과 「쟁점을 만든 날」 중 늦은 날부터 센다 — 이미 찬 조건으로 새로 연 쟁점이 즉시 초과가 되지 않게
    start = max(p["due_date"], issue["created"])
    return (today - dt.date.fromisoformat(start)).days > GRACE_DAYS


def trigger_kr(con, issue):
    """화면·목록용 한 줄 — 「PL 5경기 뒤(2/5)」."""
    k = issue["trigger_kind"]
    if k == "date":
        return f"{issue['trigger_date']} 이후"
    p = progress(con, issue)
    comp = "리그" if issue["trigger_comp"] == "league" else "공식전"
    if k == "matches":
        return f"{issue['since']} 이후 {comp} {p['need']}경기 ({p['count']}/{p['need']})"
    name = con.execute("SELECT COALESCE(name_kr, name) FROM players WHERE id=?",
                       (issue["trigger_player_id"],)).fetchone()[0]
    pos = f" {issue['trigger_pos']}" if issue["trigger_pos"] else ""
    return f"{issue['since']} 이후 {name}{pos} 선발 {p['need']}경기 ({p['count']}/{p['need']})"


def insert_issue(con, spec, source):
    """쟁점 1행 추가 → id. spec 키: team_code·title_kr·question_kr·measure_kr·trigger_kind·trigger_n·trigger_comp·
    trigger_player(이름, 유일 일치)|trigger_player_id·trigger_pos·trigger_date·since·hold."""
    pid = spec.get("trigger_player_id")
    if pid is None and spec.get("trigger_player"):
        rows = con.execute("SELECT id FROM players WHERE name_kr=? OR name=?",
                           (spec["trigger_player"], spec["trigger_player"])).fetchall()
        if len(rows) != 1:
            raise SystemExit(f"⛔ 트리거 선수 「{spec['trigger_player']}」가 유일하게 해석되지 않는다({len(rows)}건)")
        pid = rows[0][0]
    if len((spec.get("title_kr") or "").strip()) > 40:
        raise SystemExit(f"⛔ title_kr가 40자를 넘는다 — 「{spec['title_kr']}」")
    cur = con.execute("""INSERT INTO claim_issues(team_code, title_kr, question_kr, measure_kr, trigger_kind, trigger_n,
                             trigger_comp, trigger_player_id, trigger_pos, trigger_date, since, hold, source, confidence)
                         VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                      (spec["team_code"], spec["title_kr"], spec["question_kr"], spec["measure_kr"],
                       spec["trigger_kind"], spec.get("trigger_n"), spec.get("trigger_comp") or "official", pid,
                       spec.get("trigger_pos"), spec.get("trigger_date"), spec.get("since"), int(bool(spec.get("hold"))),
                       source, spec.get("confidence") or "트리거는 verdict_note 산문 조건을 셀 수 있는 형태로 옮긴 것"))
    return cur.lastrowid
