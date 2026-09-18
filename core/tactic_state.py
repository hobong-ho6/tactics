"""시즌 전술 「설정 층」의 현재 상태를 키→값으로 편다 — 변경 로그(tactic_change_log)와 G19가 같은 함수를 쓴다.

세 층만 본다(사용자 질문 2026-09-18 「개별 경기를 분석하면서 리포트의 시즌 전술이 업데이트되고 있는 거지?」에 답하는 층):
  slot_canon  — slot_canon_roles: 슬롯 정본 역할/포커스(인선 무관)
  team_setup  — team_tactic_setups: 팀 설정 3축 + 포메이션 (kind별)
  starter     — prescriptions fc26:opt:* starter=1: 선발 인선 + 역할/포커스
manager_profiles(서사 11축)는 여기 없다 — 그 층은 덧붙임 문단의 `[YYYY-MM-DD …]` 표식이 자체 히스토리다.
"""
import sqlite3

__all__ = ["state", "LAYERS"]

LAYERS = ("slot_canon", "team_setup", "starter")


def state(con: sqlite3.Connection) -> dict:
    """{(layer, regime_id, key): value} — 값은 사람이 읽는 한 줄 문자열(before/after로 그대로 저장한다)."""
    out = {}
    have = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "slot_canon_roles" in have:
        for r in con.execute("SELECT regime_id, formation, pos, role_id, focus FROM slot_canon_roles"):
            out[("slot_canon", r[0], f"{r[1]}|{r[2]}")] = f"{r[3]}/{r[4]}"
    if "team_tactic_setups" in have:
        for r in con.execute("SELECT regime_id, season, kind, formation, build_up_style, defensive_approach, line_height "
                             "FROM team_tactic_setups"):
            out[("team_setup", r[0], f"{r[1]}|{r[2]}")] = f"{r[3]} · 빌드업 {r[4]} · 수비 {r[5]} · 라인 {r[6]}"
    if "prescriptions" in have:
        cols = {c[1] for c in con.execute("PRAGMA table_info(prescriptions)")}
        if {"kind", "starter", "pos_label", "role_id", "focus", "player_id"} <= cols and "players" in have:
            for r in con.execute("SELECT p.regime_id, p.pos_label, COALESCE(pl.name_kr, pl.name, p.player_id), p.role_id, p.focus "
                                 "FROM prescriptions p LEFT JOIN players pl ON pl.id=p.player_id "
                                 "WHERE p.kind LIKE 'fc26:opt:%' AND p.starter=1"):
                out[("starter", r[0], r[1] or "")] = f"{r[2]}: {r[3]}/{r[4]}"
    return out
