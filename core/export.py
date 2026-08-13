"""DB → site/data/*.json 익스포트 — v1 sync_transfer_ui.py의 후계.

파일 구조 (팀·버전 추가 = 파일 추가, 코드 수정 없음):
  site/data/index.json          — 팀·regime·버전 메타 (허브/네비가 로드)
  site/data/kernels/{GV}.json   — 역할·포커스·위치변형·팀전술 파라미터 (버전당 1파일)
  site/data/teams/{CODE}.json   — regime 자산 전체: slots / slot_candidates / squad / prescriptions /
                                  match_reports / transfer{targets,outgoing,ledger} / setups / profile

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
        gs = _rows(con, """SELECT name_kr, sofifa_name, sofifa_id, club, positions, best_pos, age, height_cm,
                                  value_eur, preferred_foot, accelerate,
                                  ovr, pot, pac, sho, pas, dri, def, phy, playstyles, role_familiarity
                           FROM player_game_stats WHERE game_version=? ORDER BY name_kr""", (gv,))
        written.append(_write(SITE_DATA / "game_stats" / f"{gv}.json", {g["name_kr"]: g for g in gs}))

    # ── teams/{CODE}.json ────────────────────────────────────────────
    for rg in regimes:
        rid, code = rg["id"], rg["team_code"]
        slots = _rows(con, """SELECT formation, pos, slot_type, x, y, sort_order
                              FROM slots WHERE regime_id=? ORDER BY formation, sort_order""", (rid,))
        # 슬롯별 전술 정본(인선 무관) — migrations/008. 프리셋(fc26:opt:*)과 다르면 편차로 읽는다.
        canon = _rows(con, """SELECT c.formation, c.pos, c.game_version, c.role_id, c.focus,
                                     c.rationale, c.source, c.confidence, c.updated
                              FROM slot_canon_roles c JOIN slots s
                                ON s.regime_id=c.regime_id AND s.formation=c.formation AND s.pos=c.pos
                              WHERE c.regime_id=? ORDER BY c.formation, s.sort_order""", (rid,))
        # name_kr = 다른 맵(form·season_stats·fbref…)의 키. label은 표시용이라 접미·별칭이 붙어 다를 수 있다.
        squad = _rows(con, """SELECT s.player_id, COALESCE(s.label, p.name_kr, p.name) label,
                                     p.name name_en, COALESCE(p.name_kr, p.name) name_kr,
                                     s.slot_type, s.lh, s.map25, s.rate_v, s.rate_basis, s.rate_note,
                                     s.fit_role, s.fit_focus, s.fit_sim, s.sort_order, s.grid_club, s.grid_caveat
                              FROM squad_entries s JOIN players p ON p.id=s.player_id
                              WHERE s.regime_id=? ORDER BY s.sort_order, label""", (rid,))
        prescriptions = _rows(con, """
            SELECT pr.player_id, COALESCE(p.name_kr, p.name) label, pr.season, pr.game_version,
                   pr.kind, pr.pos_label, pr.x, pr.y, pr.role_id, pr.focus, pr.map25, pr.starter,
                   pr.fit_sim, pr.sample_n, pr.avg_rating, pr.rationale, pr.grid_club
            FROM prescriptions pr JOIN players p ON p.id=pr.player_id
            WHERE pr.regime_id=? ORDER BY pr.player_id, pr.kind""", (rid,))
        # 모든 화면이 공유하는 슬롯 후보 정본. squad/transfer를 페이지별로 다시 합치지 않는다.
        # v_slot_candidates가 (regime, formation, pos, player_id) 중복 제거와 승격 우선순위를 보장한다.
        slot_candidates = _rows(con, """
            SELECT regime_id, team_code, formation, pos, slot_type, player_id, label,
                   name_en, name_kr, source_kind, status, map25, rating, rate_basis,
                   rate_note, fit_role, fit_focus, fit_sim, source, confidence,
                   sort_order, grid_club, grid_caveat
            FROM v_slot_candidates WHERE regime_id=?
            ORDER BY formation, pos, source_kind, sort_order, label""", (rid,))
        setups = _rows(con, """SELECT season, game_version, kind, formation, build_up_style,
                                      defensive_approach, line_height, tactic_code, rationale, confidence
                               FROM team_tactic_setups WHERE regime_id=?
                               ORDER BY season, kind""", (rid,))
        profile = _rows(con, """SELECT axis, content, evidence, confidence, updated
                                FROM manager_profiles WHERE regime_id=? ORDER BY axis""", (rid,))
        targets = _rows(con, """SELECT player_id, name, name_kr, short_label, slot, club, position,
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
                                      d.execution, d.adherence, d.game_role_implication, d.source, d.confidence,
                                      d.observed_from, d.observed_to, d.sample_scope, d.sample_note
                               FROM player_duties d JOIN players p ON p.id=d.player_id
                               WHERE d.regime_id=? ORDER BY p.id""", (rid,))
        pstats = _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, v.n, v.avg_rating, v.minutes,
                                      v.xg_pg, v.xa_pg, v.kp_pg, v.dw_pg, v.tk_pg, v.ic_pg
                               FROM v_player_profile v JOIN players p ON p.id=v.player_id
                               WHERE v.player_id IN (SELECT player_id FROM squad_entries WHERE regime_id=?
                                     UNION SELECT player_id FROM prescriptions WHERE regime_id=?)""", (rid, rid))
        evals = _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, p.name name_en, e.player_id,
                                     e.overall, e.traits, e.strengths, e.stat_eval, e.fotmob_eval,
                                     e.fit_emery, e.fit_alonso, e.fit_iraola,
                                     e.source, e.confidence, e.updated
                              FROM player_evaluations e JOIN players p ON p.id=e.player_id
                              WHERE e.regime_id=? ORDER BY e.player_id""", (rid,))
        season_stats = {}
        for r in _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, v.season, v.competition,
                                      v.n, v.starts, v.minutes, v.goals, v.assists, v.avg_rating
                               FROM v_player_season_stats v JOIN players p ON p.id=v.player_id
                               WHERE v.player_id IN (SELECT player_id FROM squad_entries WHERE regime_id=?
                                     UNION SELECT player_id FROM prescriptions WHERE regime_id=?)
                               ORDER BY v.season DESC, v.n DESC""", (rid, rid)):
            season_stats.setdefault(r.pop("label"), []).append(r)
        fbref = {}   # 리그 백분위 — Fotmob 상세 스탯(migrations/006). 지표별 동포지션 백분위.
        for r in _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, f.season, f.league,
                                      f.metric_key, f.metric, f.metric_kr, f.stat_value, f.per90,
                                      f.percentile, f.percentile_per90, f.pulled
                               FROM fotmob_detail_stats f JOIN players p ON p.id=f.player_id
                               WHERE f.player_id IN (SELECT player_id FROM squad_entries WHERE regime_id=?
                                     UNION SELECT player_id FROM prescriptions WHERE regime_id=?
                                     UNION SELECT p2.id FROM transfer_targets t JOIN players p2
                                           ON p2.name=t.name WHERE t.team_code=?)
                               ORDER BY f.percentile DESC""", (rid, rid, code)):
            fbref.setdefault(r.pop("label"), []).append(r)
        fm_season = {}
        for r in _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, f.league, f.season,
                                      f.metric, f.metric_kr, f.value, f.pulled
                               FROM fotmob_season_stats f JOIN players p ON p.id=f.player_id
                               WHERE f.player_id IN (SELECT player_id FROM squad_entries WHERE regime_id=?
                                     UNION SELECT player_id FROM prescriptions WHERE regime_id=?
                                     UNION SELECT p2.id FROM transfer_targets t JOIN players p2
                                           ON p2.name=t.name WHERE t.team_code=?)
                               ORDER BY f.id""", (rid, rid, code)):
            fm_season.setdefault(r.pop("label"), []).append(r)
        form = {}
        for r in _rows(con, """SELECT COALESCE(p.name_kr,p.name) label, m.date, m.rating, m.competition
              FROM player_matches m JOIN players p ON p.id=m.player_id
              WHERE m.rating IS NOT NULL AND m.player_id IN
                (SELECT player_id FROM squad_entries WHERE regime_id=?
                 UNION SELECT player_id FROM prescriptions WHERE regime_id=?)
              ORDER BY m.date""", (rid, rid)):
            form.setdefault(r["label"], []).append([r["date"], r["rating"], r["competition"]])
        form = {k: v[-10:] for k, v in form.items()}   # 최근 10경기
        # 경기별 리포트 — 해석은 match_reports/match_player_reports, 원천 수치는
        # matches/player_matches/team_match_stats에서 같은 event_id로 묶는다.
        match_reports = _rows(con, """
            SELECT mr.id, mr.event_id, mr.match_id, mr.season, mr.report_date, mr.title,
                   mr.status, mr.tactical_description, mr.tactical_features,
                   mr.tactical_changes, mr.game_implications, mr.report_path,
                   mr.source, mr.confidence, mr.created_at, mr.updated_at,
                   m.date, m.opponent, m.competition, m.venue, m.result, m.stage,
                   m.possession, ts.xg_v, ts.xg_o, ts.shots_v, ts.shots_o,
                   ts.sot_v, ts.sot_o, ts.bigch_v, ts.bigch_o, ts.passes_v,
                   ts.passes_o, ts.long_att_v, ts.long_acc_v, ts.long_att_o,
                   ts.long_acc_o, ts.cross_att_v, ts.cross_acc_v, ts.corners_v,
                   ts.corners_o, ts.duelpct_v, ts.fouls_v, ts.fouls_o,
                   ts.formation_v, ts.formation_o
            FROM match_reports mr
            LEFT JOIN matches m ON m.id=mr.match_id
            LEFT JOIN team_match_stats ts
              ON ts.event_id=mr.event_id AND ts.team_code=mr.team_code
            WHERE mr.team_code=?
            ORDER BY COALESCE(m.date,mr.report_date) DESC, mr.id DESC""", (code,))
        for report in match_reports:
            report["players"] = _rows(con, """
                SELECT mpr.player_id, COALESCE(p.name_kr,p.name) label, p.name name_en,
                       mpr.position, mpr.tactical_role, mpr.characteristics,
                       mpr.performance, mpr.game_implication, mpr.source, mpr.confidence,
                       pm.minutes, pm.rating, pm.started, pm.lineup_pos, pm.pos_class,
                       pm.avg_x, pm.avg_y, pm.hit_points, pm.map25, pm.xg, pm.xa,
                       pm.key_passes, pm.duels_won, pm.duels_lost, pm.tackles,
                       pm.interceptions, pm.goals, pm.assists, pm.touches,
                       pm.recoveries, pm.stats_json
                FROM match_player_reports mpr
                JOIN players p ON p.id=mpr.player_id
                LEFT JOIN player_matches pm
                  ON pm.player_id=mpr.player_id AND pm.event_id=?
                WHERE mpr.report_id=?
                ORDER BY COALESCE(pm.lineup_order,99), p.id""",
                (report["event_id"], report["id"]))
            setup = _rows(con, """
                SELECT report_id,game_version,formation,build_up_style,
                       defensive_approach,line_height,tactic_code,match_only,
                       rationale,source,confidence
                FROM match_game_setups WHERE report_id=?""", (report["id"],))
            report["game_setup"] = setup[0] if setup else None
            report["game_players"] = _rows(con, """
                SELECT mpp.player_id,COALESCE(p.name_kr,p.name) label,p.name name_en,
                       mpp.game_version,mpp.pos_label,mpp.role_id,gr.name role_name,
                       mpp.focus,mpp.fit_sim,mpp.starter,mpp.sort_order,mpp.rationale,
                       mpp.replaced_player_id,mpp.minute_on,
                       mpp.source,mpp.confidence,s.x,s.y
                FROM match_player_prescriptions mpp
                JOIN players p ON p.id=mpp.player_id
                JOIN game_roles gr
                  ON gr.game_version=mpp.game_version AND gr.role_id=mpp.role_id
                LEFT JOIN match_game_setups mgs ON mgs.report_id=mpp.report_id
                LEFT JOIN slots s ON s.regime_id=? AND s.formation=mgs.formation
                                 AND s.pos=mpp.pos_label
                WHERE mpp.report_id=? ORDER BY mpp.sort_order,p.id""",
                (rid, report["id"]))
            report_file = ROOT / report["report_path"]
            report["report_markdown"] = (
                report_file.read_text(encoding="utf-8") if report_file.is_file() else None)
        departed = [r["label"] for r in _rows(con, """SELECT COALESCE(p.name_kr,p.name) label
            FROM transfer_outgoing o JOIN players p ON p.id=o.player_id
            WHERE o.team_code=? AND o.likelihood='CONFIRMED'""", (code,))]
        written.append(_write(SITE_DATA / "teams" / f"{code}.json", {
            "regime": rg, "slots": slots, "slot_canon": canon,
            "slot_candidates": slot_candidates,
            "squad": squad, "prescriptions": prescriptions,
            "duties": duties, "player_stats": pstats, "departed": departed, "form": form,
            "match_reports": match_reports,
            "evaluations": evals, "season_stats": season_stats, "fbref": fbref,
            "fotmob_season": fm_season,
            "setups": setups, "profile": profile,
            "transfer": {"targets": targets, "outgoing": outgoing, "ledger": ledger}}))

    con.close()
    return written
