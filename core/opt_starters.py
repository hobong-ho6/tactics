"""선발 처방 층(prescriptions opt:* starter=1) 자동 산출 — 손으로 고르지 않는다 (2026-10-28 신설 · obs#1148).

왜(불변규칙 13 — 같은 문제 2회차 · 구조 제거):
  선발 플래그는 손으로 고쳐 왔고, 가용 인원이 바뀔 때마다 낡았다.
  ⑴ 10-22 obs#1120 — FC26→FC27 승계가 7~9월 선발을 그대로 옮겨 11칸 중 7칸이 낡음
  ⑵ 10-28 obs#1148 — 10-22 재지정 때 부상·강제로 고른 3칸(LB 밍스·LDM 바클리·CAM 부엔디아)이 풀렸는데 그대로
  역할/포커스는 G8+가 정본과 맞추게 강제하므로, 낡는 것은 「누가 선발이냐」 하나뿐이었다 ⇒ 그것을 계산으로 바꾼다.

규칙(손으로 고른 10-22·10-28 선발 11칸을 그대로 재현함을 10-28에 확인):
  슬롯마다 최근 클럽 공식전 N(=5)경기의 경기 처방 선발(match_player_prescriptions starter=1 · pos_label)에서
  ⑴ 장기 부상자를 빼고 ⑵ 그 슬롯 선발 횟수 최다 ⑶ 동률이면 가장 최근 선발 ⑷ 그래도 같으면 출전 분 합.
  역할/포커스 = slot_canon_roles(현행 버전) · 적합 = core.kernel ↔ 그 슬롯 선발 경기만의 그리드(슬롯 순수 · 45분+).
  후보가 하나도 없으면 그 칸은 그대로 둔다.
  ⇒ 단일 경기 상대 맞춤 배치(예: 맨시티전 맥긴 CAM)는 다수결에서 걸러진다.

호출: scripts/export.py가 게이트 전에 apply()를 부른다(ship·export 어느 경로든 빠뜨릴 수 없다).
      변경이 있으면 tactic_change_log에 자동 사유로 적는다(G19).
범위: AVL만(2026-10-20 사용자 결정 — CHE·LIV·ATM 보류 · G8+와 같은 범위).
"""
import datetime as _dt

from core.aggregate import aggregate_rows, NON_OFFICIAL_COMP
from core.game_version import current, OPT_PREFIX
from core.kernel import Kernel

__all__ = ["long_term_injured", "derive", "apply", "TEAMS", "RECENT_N"]

TEAMS = ("AVL",)
RECENT_N = 5
REASON = f"자동 산출 core.opt_starters — 최근 클럽 공식전 {RECENT_N}경기 슬롯 선발 최다(장기 부상 제외)"
_MON = {m: i for i, m in enumerate(("January", "February", "March", "April", "May", "June", "July",
                                     "August", "September", "October", "November", "December"), 1)}


def long_term_injured(con, today=None):
    """{player_id: (value, detail, as_of)} — player_status 최신 스냅샷이 장기 부상인 선수.
    「장기」(데이터에 명시 필드가 없어 보수적으로 둔다): 복귀 예상(detail 「Month YYYY」)이 이번 달 뒤이거나,
    부상일(as_of) 21일 경과 뒤 최신 스냅샷(7일 내)이 여전히 injury. G8+와 선발 산출이 같이 쓴다."""
    today = today or _dt.date.today()
    out = {}
    for pid, kind, value, detail, as_of, pulled in con.execute("""
        SELECT s.player_id, s.kind, s.value, s.detail, s.as_of, s.pulled FROM player_status s
        WHERE s.kind IN ('injury','injury_none')
          AND s.pulled=(SELECT MAX(x.pulled) FROM player_status x WHERE x.player_id=s.player_id
                         AND x.kind IN ('injury','injury_none'))"""):
        if kind != "injury":
            continue
        long_term = False
        parts = (detail or "").split()
        if len(parts) == 2 and parts[0] in _MON and parts[1].isdigit():
            long_term = (int(parts[1]), _MON[parts[0]]) > (today.year, today.month)
        try:
            injured_days = (today - _dt.date.fromisoformat(as_of[:10])).days if as_of else 0
            fresh = (today - _dt.date.fromisoformat(pulled[:10])).days <= 7 if pulled else False
        except ValueError:
            injured_days, fresh = 0, False
        if injured_days >= 21 and fresh:
            long_term = True
        if long_term:
            out[pid] = (value, detail, as_of)
    return out


def _official(col="m.competition"):
    return f"{col} NOT IN ({','.join('?' * len(NON_OFFICIAL_COMP))})", NON_OFFICIAL_COMP


def _slot_fit(con, kernel, player_id, team, season, pos, role, focus, x):
    """그 슬롯 선발 경기만의 그리드(45분+ · hp 15+) → dict(map25, fit, n, minutes, avg_rating) · 2경기 미만 None."""
    w, p = _official("pm.competition")
    rows = con.execute(f"""
        SELECT pm.cells, pm.rating, pm.minutes, pm.avg_x, pm.avg_y FROM player_matches pm
        JOIN match_reports r ON r.match_id=pm.match_id
        JOIN match_player_prescriptions mp ON mp.report_id=r.id AND mp.player_id=pm.player_id AND mp.starter=1
        WHERE pm.player_id=? AND pm.team_code=? AND pm.season=? AND mp.pos_label=? AND pm.minutes>=45
          AND pm.cells IS NOT NULL AND pm.hit_points>=15 AND {w}""", (player_id, team, season, pos, *p)).fetchall()
    a = aggregate_rows(rows)
    if not a:
        return None
    return dict(map25=a["map25"], fit=round(kernel.fit(a["map25"], role, focus, x), 3), n=a["n"],
                minutes=a["minutes"], avg_rating=a["avg_rating"])


def derive(con):
    """[(regime_id, season, gv, pos, player_id, reason_text)] — 슬롯별 산출 선발. 쓰지 않는다."""
    gv = current(con)
    if not gv:
        return []
    hurt = long_term_injured(con)
    out = []
    for rid, team in con.execute(f"SELECT id, team_code FROM regimes WHERE team_code IN ({','.join('?' * len(TEAMS))})"
                                 " AND \"end\" IS NULL", TEAMS).fetchall():
        w, p = _official()
        reps = con.execute(f"""
            SELECT r.id, m.date, m.season FROM match_reports r JOIN matches m ON m.id=r.match_id
            WHERE m.team_code=? AND {w}
              AND EXISTS (SELECT 1 FROM match_player_prescriptions x WHERE x.report_id=r.id AND x.starter=1)
            ORDER BY m.date DESC LIMIT ?""", (team, *p, RECENT_N)).fetchall()
        if not reps:
            continue
        season = reps[0][2]
        reps = [r for r in reps if r[2] == season]
        canon = {pos for (pos,) in con.execute(
            "SELECT pos FROM slot_canon_roles WHERE regime_id=? AND game_version=?", (rid, gv))}
        tally = {}   # (pos, pid) -> [count, latest_date, minutes]
        for rep_id, date, _ in reps:
            for pos, pid in con.execute("SELECT pos_label, player_id FROM match_player_prescriptions "
                                        "WHERE report_id=? AND starter=1", (rep_id,)):
                if pos not in canon or pid in hurt:
                    continue
                mins = con.execute("SELECT COALESCE(SUM(pm.minutes),0) FROM player_matches pm JOIN match_reports r "
                                   "ON r.match_id=pm.match_id WHERE r.id=? AND pm.player_id=?", (rep_id, pid)).fetchone()[0]
                t = tally.setdefault((pos, pid), [0, "", 0])
                t[0] += 1
                t[1] = max(t[1], date)
                t[2] += mins
        for pos in sorted(canon):
            cands = sorted(((v, pid) for (ps, pid), v in tally.items() if ps == pos),
                           key=lambda c: (c[0][0], c[0][1], c[0][2]), reverse=True)
            if not cands:
                continue
            (cnt, last, _), pid = cands[0]
            out.append((rid, season, gv, pos, pid, f"최근 {len(reps)}경기 중 {cnt}회 선발 · 마지막 {last}"))
    return out


def apply(con, dry_run=False):
    """산출 선발을 prescriptions에 반영하고 변경을 tactic_change_log에 적는다. 바뀐 칸 목록을 돌려준다."""
    from scripts.tactic_changes import diff, logged_state
    from core.tactic_state import state

    plan = derive(con)
    if not plan:
        return []
    kernels, changes = {}, []
    today = _dt.date.today().isoformat()
    for rid, season, gv, pos, pid, why in plan:
        kernel = kernels.setdefault(gv, Kernel(gv))
        kind = OPT_PREFIX + pos
        role, focus = con.execute("SELECT role_id, focus FROM slot_canon_roles WHERE regime_id=? AND game_version=? AND pos=?",
                                  (rid, gv, pos)).fetchone()
        x, y = con.execute("SELECT x, y FROM slots s JOIN slot_canon_roles c ON c.regime_id=s.regime_id "
                           "AND c.formation=s.formation AND c.pos=s.pos WHERE c.regime_id=? AND c.game_version=? AND c.pos=?",
                           (rid, gv, pos)).fetchone()
        team = con.execute("SELECT team_code FROM regimes WHERE id=?", (rid,)).fetchone()[0]
        cur = con.execute("SELECT player_id FROM prescriptions WHERE regime_id=? AND season=? AND game_version=? "
                          "AND kind=? AND starter=1", (rid, season, gv, kind)).fetchall()
        row = con.execute("SELECT id, role_id, focus, fit_sim, map25 FROM prescriptions WHERE player_id=? AND regime_id=? "
                          "AND season=? AND game_version=? AND kind=?", (pid, rid, season, gv, kind)).fetchone()
        f = _slot_fit(con, kernel, pid, team, season, pos, role, focus, x)
        is_new_starter = [r[0] for r in cur] != [pid]
        role_changed = bool(row) and (row[1], row[2]) != (role, focus)
        note = f" ‖ [{today} {REASON}] {why}"
        if role_changed:
            note += f" · 옛 역할 {row[1]}/{row[2]}(fit {row[3]}) → 정본 {role}/{focus}"
        if dry_run:
            if is_new_starter or role_changed:
                changes.append((pos, [r[0] for r in cur], pid, why))
            continue
        if row is None:
            con.execute("""INSERT INTO prescriptions(player_id, regime_id, season, game_version, kind, pos_label, x, y,
                           role_id, focus, map25, fit_sim, sample_n, avg_rating, minutes, rationale, starter, grid_club)
                           VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,0,(SELECT name FROM teams WHERE code=?))""",
                        (pid, rid, season, gv, kind, pos, x, y, role, focus,
                         f and f["map25"], f and f["fit"], f and f["n"], f and f["avg_rating"], f and f["minutes"],
                         note.lstrip(" ‖"), team))
            row_id = con.execute("SELECT last_insert_rowid()").fetchone()[0]
        else:
            row_id = row[0]
            if is_new_starter or role_changed:
                con.execute("UPDATE prescriptions SET rationale=COALESCE(rationale,'')||? WHERE id=?", (note, row_id))
            if role_changed:
                con.execute("UPDATE prescriptions SET role_id=?, focus=?, x=?, y=? WHERE id=?", (role, focus, x, y, row_id))
            if f and (f["map25"], f["fit"]) != (row[4], row[3]):
                con.execute("UPDATE prescriptions SET map25=?, fit_sim=?, sample_n=?, avg_rating=?, minutes=? WHERE id=?",
                            (f["map25"], f["fit"], f["n"], f["avg_rating"], f["minutes"], row_id))
            elif not f and role_changed:
                con.execute("UPDATE prescriptions SET map25=NULL, fit_sim=NULL, sample_n=NULL WHERE id=?", (row_id,))
        if is_new_starter:
            con.execute("UPDATE prescriptions SET starter=0 WHERE regime_id=? AND season=? AND game_version=? AND kind=? "
                        "AND id<>?", (rid, season, gv, kind, row_id))
            con.execute("UPDATE prescriptions SET starter=1 WHERE id=?", (row_id,))
        if is_new_starter or role_changed:
            changes.append((pos, [r[0] for r in cur], pid, why))
    if not dry_run:
        rids = {p[0] for p in plan}
        pend = [(k, b, af) for k, b, af in diff(logged_state(con), state(con)) if k[0] == "starter" and k[1] in rids]
        con.executemany("INSERT INTO tactic_change_log(regime_id, layer, key, before, after, changed_at, reason, source) "
                        "VALUES(?,?,?,?,?,?,?,?)",
                        [(k[1], k[0], k[2], b, af, today, REASON, "core.opt_starters") for k, b, af in pend])
        con.commit()
    return changes
