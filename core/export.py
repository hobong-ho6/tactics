"""DB → site/data/*.json 익스포트 — v1 sync_transfer_ui.py의 후계.

파일 구조 (팀·버전 추가 = 파일 추가, 코드 수정 없음):
  site/data/index.json          — 팀·regime·버전 메타 (허브/네비가 로드)
  site/data/kernels/{GV}.json   — 역할·포커스·위치변형·팀전술 파라미터 (버전당 1파일)
  site/data/teams/{CODE}.json   — regime 자산 전체: slots / squad / prescriptions /
                                  transfer{targets,outgoing,ledger} / setups / profile

원칙:
  · 값은 DB 컬럼의 1:1 사상 — 여기서 가공하지 않는다 (가공은 분석 단계의 일)
  · 매 실행 전 게이트 통과 필수 (호출측 scripts/export.py가 강제)
  · 키 정렬·결정적 직렬화 — DB 무변경이면 diff 0
"""
import json
import sqlite3
from pathlib import Path

from . import DB, ROOT

SITE_DATA = ROOT / "site" / "data"

__all__ = ["export_all"]


def _rows(con, sql, params=()):
    con.row_factory = sqlite3.Row
    return [dict(r) for r in con.execute(sql, params).fetchall()]


def _write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                    encoding="utf-8")
    return path


def export_all(db_path=None, window="2026-summer"):
    con = sqlite3.connect(db_path or DB)
    written = []

    # ── index.json ───────────────────────────────────────────────────
    regimes = _rows(con, """SELECT r.id, r.team_code, t.name team_name, t.name_kr team_kr,
                                   r.manager, r.manager_kr, r.is_main, r.start
                            FROM regimes r JOIN teams t ON t.code=r.team_code
                            WHERE r.end IS NULL ORDER BY r.is_main DESC, r.id""")
    versions = _rows(con, "SELECT code, released, notes FROM game_versions ORDER BY code")
    written.append(_write(SITE_DATA / "index.json",
                          {"regimes": regimes, "game_versions": versions, "window": window}))

    # ── kernels/{GV}.json ────────────────────────────────────────────
    for (gv,) in con.execute("SELECT code FROM game_versions"):
        roles = _rows(con, """SELECT role_id, name, name_en, position_type, focuses
                              FROM game_roles WHERE game_version=? ORDER BY role_id""", (gv,))
        if not roles:
            continue                      # FC27 등 미수집 버전은 파일을 만들지 않는다
        focus = _rows(con, """SELECT role_id, focus, kernel25, plus, equal, negative,
                                     ea_role_name, description
                              FROM game_role_focus WHERE game_version=?
                              ORDER BY role_id, focus""", (gv,))
        variants = _rows(con, """SELECT role_id, focus, pitch_x, kernel25
                                 FROM game_role_variants WHERE game_version=?
                                 ORDER BY role_id, focus, pitch_x""", (gv,))
        params = _rows(con, """SELECT param, option, description FROM game_tactic_params
                               WHERE game_version=? ORDER BY param, option""", (gv,))
        changes = _rows(con, """SELECT area, change, evidence, impact, source, confidence, recorded
                               FROM game_system_changes WHERE game_version=? ORDER BY id""", (gv,))
        written.append(_write(SITE_DATA / "kernels" / f"{gv}.json",
                              {"game_version": gv, "roles": roles, "focus": focus,
                               "variants": variants, "tactic_params": params,
                               "system_changes": changes}))

    # ── game_stats/{GV}.json — sofifa 스탯·플레이스타일 (name_kr 키, 표시 전용) ──
    for (gv,) in con.execute("SELECT DISTINCT game_version FROM player_game_stats"):
        gs = _rows(con, """SELECT name_kr, sofifa_id, club, positions, best_pos, age,
                                  ovr, pot, pac, sho, pas, dri, def, phy, playstyles, role_familiarity
                           FROM player_game_stats WHERE game_version=? ORDER BY name_kr""", (gv,))
        written.append(_write(SITE_DATA / "game_stats" / f"{gv}.json", {g["name_kr"]: g for g in gs}))

    # ── teams/{CODE}.json ────────────────────────────────────────────
    for rg in regimes:
        rid, code = rg["id"], rg["team_code"]
        slots = _rows(con, """SELECT formation, pos, slot_type, x, y, sort_order
                              FROM slots WHERE regime_id=? ORDER BY formation, sort_order""", (rid,))
        squad = _rows(con, """SELECT s.player_id, COALESCE(s.label, p.name_kr, p.name) label,
                                     s.slot_type, s.lh, s.map25, s.rate_v, s.rate_basis, s.rate_note,
                                     s.fit_role, s.fit_focus, s.fit_sim, s.sort_order
                              FROM squad_entries s JOIN players p ON p.id=s.player_id
                              WHERE s.regime_id=? ORDER BY s.sort_order, label""", (rid,))
        prescriptions = _rows(con, """
            SELECT pr.player_id, COALESCE(p.name_kr, p.name) label, pr.season, pr.game_version,
                   pr.kind, pr.pos_label, pr.x, pr.y, pr.role_id, pr.focus, pr.map25, pr.starter,
                   pr.fit_sim, pr.sample_n, pr.avg_rating, pr.rationale
            FROM prescriptions pr JOIN players p ON p.id=pr.player_id
            WHERE pr.regime_id=? ORDER BY pr.player_id, pr.kind""", (rid,))
        setups = _rows(con, """SELECT season, game_version, kind, formation, build_up_style,
                                      defensive_approach, line_height, tactic_code, rationale, confidence
                               FROM team_tactic_setups WHERE regime_id=?
                               ORDER BY season, kind""", (rid,))
        profile = _rows(con, """SELECT axis, content, evidence, confidence, updated
                                FROM manager_profiles WHERE regime_id=? ORDER BY axis""", (rid,))
        targets = _rows(con, """SELECT name, name_kr, short_label, slot, club, position,
                                       likelihood, last_news_date, map25, sample_n, avg_rating,
                                       opt_role, opt_focus, fit_role, fit_focus, fit_sim,
                                       confidence, source
                                FROM transfer_targets WHERE team_code=? AND window=?
                                  AND likelihood!='OWNED'
                                ORDER BY id""", (code, window))
        # OWNED는 스쿼드(squad_entries)에 이미 있다 — 이적 목록에서 제외 (v1 동일 필터)
        outgoing = _rows(con, """SELECT p.name, p.name_kr, o.dest_club, o.likelihood,
                                        o.last_news_date, o.confidence, o.source
                                 FROM transfer_outgoing o JOIN players p ON p.id=o.player_id
                                 WHERE o.team_code=? AND o.window=? ORDER BY o.player_id""",
                         (code, window))
        ledger = _rows(con, """SELECT kind, label, amount_m, note, confidence
                               FROM transfer_ledger WHERE team_code=? AND window=?
                               ORDER BY CASE kind WHEN 'in' THEN 0 WHEN 'deduct' THEN 1
                                        WHEN 'out' THEN 2 ELSE 3 END, amount_m DESC""",
                        (code, window))
        duties = _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, d.position, d.duties,
                                      d.execution, d.adherence, d.game_role_implication, d.source, d.confidence
                               FROM player_duties d JOIN players p ON p.id=d.player_id
                               WHERE d.regime_id=? ORDER BY p.id""", (rid,))
        pstats = _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, v.n, v.avg_rating, v.minutes,
                                      v.xg_pg, v.xa_pg, v.kp_pg, v.dw_pg, v.tk_pg, v.ic_pg
                               FROM v_player_profile v JOIN players p ON p.id=v.player_id
                               WHERE v.player_id IN (SELECT player_id FROM squad_entries WHERE regime_id=?)""", (rid,))
        written.append(_write(SITE_DATA / "teams" / f"{code}.json", {
            "regime": rg, "slots": slots, "squad": squad, "prescriptions": prescriptions,
            "duties": duties, "player_stats": pstats,
            "setups": setups, "profile": profile,
            "transfer": {"targets": targets, "outgoing": outgoing, "ledger": ledger}}))

    con.close()
    return written
