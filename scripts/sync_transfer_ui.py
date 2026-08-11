#!/usr/bin/env python3
"""Regenerate the AUTOGEN blocks in fc26-heatmap.html from data/avl_analysis.db.

Run this after any transfer_targets/transfer_outgoing change (transfer-watch
runs, manual DB edits), before scripts/db_dump.sh + commit. See docs/40-pipeline.md.

Rewrites two blocks only, between marker comments:
  AUTOGEN:TRANSFER_TARGETS   <- transfer_targets rows (window=2026-summer, likelihood != 'OWNED')
  AUTOGEN:TRANSFER_OUTGOING  <- transfer_outgoing rows joined with players.name

Everything else in the file (SQUAD_SLOTS owned-player opts, PLAYER_BEST for
nailed-on starters, XI_POOL owned rows, etc.) is untouched — incoming-candidate
entries for those three are derived at runtime from TRANSFER_TARGETS by
injectTransferCandidates() (see fc26-heatmap.html), not generated here.
"""
import json
import re
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "avl_analysis.db"
HTML = ROOT / "fc26-heatmap.html"
WINDOW = "2026-summer"
# 팀 축 (2026-07-30 도입 → 2026-08-11 UI까지 일반화). 종전에는 TEAM="AVL" 단일 값으로
# 필터해 빌라 행만 툴에 실었고, 그래서 첼시·리버풀 행은 warn_dropped_teams()가 경고만 하고
# 버려졌다. 이제 팀별 블록(`*_BY_TEAM`)을 생성하므로 세 팀이 같은 형태로 실린다.
TEAM = "AVL"          # 하위호환용 기본 팀 (프리뷰·로그 표기)
TEAM_CODES = ["AVL", "CHE", "LIV"]


def js_obj(fields):
    """Render an ordered dict of Python values as a compact JS object literal.
    None -> JS null (valid JS, keeps falsy semantics for e.g. `if(row.map25)`)."""
    parts = [f"{k}:{json.dumps(v, ensure_ascii=False)}" for k, v in fields.items()]
    return "{" + ",".join(parts) + "}"


def by_team_block(varname, per_team):
    """{AVL:[...],CHE:[...],LIV:[...]} 형태의 팀별 블록을 만든다.
    per_team: team -> (list[str] 항목 리터럴). 빈 팀도 키는 남긴다(접근자 분기 단순화)."""
    chunks = []
    for code in TEAM_CODES:
        items = per_team.get(code, [])
        body = "\n".join(items)
        chunks.append(f" {code}:[\n{body}\n ],")
    return f"const {varname}_BY_TEAM={{\n" + "\n".join(chunks) + "\n};"


def gen_transfer_targets(conn, TEAM):
    rows = conn.execute(
        """SELECT name,name_kr,slot,club,position,likelihood,confidence,
                  fit_sim,opt_role,opt_focus,fit_role,fit_focus,source,
                  map25,tool_x,tool_y,sample_n,avg_rating,short_label,last_news_date
           FROM transfer_targets
           WHERE team=? AND window=? AND likelihood!='OWNED'
           ORDER BY id""",
        (TEAM, WINDOW,),
    ).fetchall()
    lines = []
    for row in rows:
        r = dict(row)
        obj = js_obj(
            {
                "name": r["name"],
                "name_kr": r["name_kr"],
                "slot": r["slot"],
                "club": r["club"],
                "position": r["position"],
                "likelihood": r["likelihood"],
                "confidence": r["confidence"],
                "fit_sim": r["fit_sim"],
                "opt_role": r["opt_role"],
                "opt_focus": r["opt_focus"],
                "fit_role": r["fit_role"],
                "fit_focus": r["fit_focus"],
                "source": r["source"],
                "map25": r["map25"],
                "avg_rating": r["avg_rating"],
                "sample_n": r["sample_n"],
                "short_label": r["short_label"],
                "last_news_date": r["last_news_date"],
            }
        )
        lines.append(obj + ",")
    return lines


def gen_transfer_outgoing(conn, TEAM):
    rows = conn.execute(
        """SELECT p.name,t.dest_club,t.likelihood,t.confidence,t.source,t.last_news_date
           FROM transfer_outgoing t JOIN players p ON p.id=t.player_id
           WHERE t.team=? AND t.window=?
           ORDER BY t.player_id""",
        (TEAM, WINDOW,),
    ).fetchall()
    lines = []
    for name, dest_club, likelihood, confidence, source, last_news_date in rows:
        obj = js_obj(
            {
                "player": name,
                "dest_club": dest_club,
                "likelihood": likelihood,
                "confidence": confidence,
                "source": source,
                "last_news_date": last_news_date,
            }
        )
        lines.append(obj + ",")
    return lines


def gen_transfer_ledger(conn, TEAM):
    rows = conn.execute(
        """SELECT kind,label,amount_m,note,confidence
           FROM transfer_ledger WHERE team=? AND window=?
           ORDER BY CASE kind WHEN 'in' THEN 0 WHEN 'deduct' THEN 1 WHEN 'out' THEN 2 ELSE 3 END,
                    amount_m DESC""",
        (TEAM, WINDOW,),
    ).fetchall()
    lines = []
    for r in rows:
        obj = js_obj(
            {
                "kind": r["kind"],
                "label": r["label"],
                "amount": r["amount_m"],
                "note": r["note"],
                "confidence": r["confidence"],
            }
        )
        lines.append(obj + ",")
    return lines


def gen_xi_owned(conn, TEAM):
    """보유 선수의 포지션별 Best-11 엔트리 — squad_positions 단일 소스.
    다포지션 선수(맥긴 WM+DM, 부엔디아 WM+CAM, 보가르드 DM+FB)는 여러 행으로 나온다."""
    rows = conn.execute(
        """SELECT label,slot_type,lh,map25,rate_v,rate_basis,rate_note
           FROM squad_positions WHERE team=? ORDER BY sort_order, label""",
        (TEAM,),
    ).fetchall()
    lines = []
    for r in rows:
        obj = js_obj(
            {
                "label": r["label"],
                "grid": r["map25"],
                "lh": r["lh"],
                "rate": {"v": r["rate_v"], "b": r["rate_basis"], "s": r["rate_note"]},
                "t": r["slot_type"],
            }
        )
        lines.append(obj + ",")
    return lines


def gen_role_kernels(conn):
    """MAPS — 역할×포커스 히트맵 커널 85개 (obs#105, SSOT 1단계).

    툴에만 있던 프로젝트 최심부 데이터를 DB에서 생성한다. 이 커널이 모든 적합값의 뿌리다
    (placedMap·cmpCos·fit_sim·COLL_CAL·에메리 솔버가 전부 여기서 파생).

    정렬은 **피치 순서**(GK→CB→FB→DM→CM→CAM→WM→W→ST)를 유지한다 — 알파벳순으로 두면
    포지션 그룹이 흩어져 사람이 읽을 수 없다. 그룹 사이 빈 줄은 넣지 않는다(그룹 경계가
    바뀌면 diff가 나기 때문).
    포커스 키는 하이픈을 포함할 수 있어(`Build-Up`·`Ball-Winning`) 항상 인용한다.
    diff 안정성: 값이 25자 고정 문자열이고 정렬이 결정적이므로 DB 무변경 시 diff 0.
    """
    PITCH_ORDER = ["GK", "CB", "FB", "DM", "CM", "CAM", "WM", "W", "ST"]
    rows = conn.execute(
        "SELECT f.role_id, f.focus, f.kernel25, r.position_type "
        "FROM game_role_focus f JOIN game_roles r "
        "  ON r.game_version=f.game_version AND r.role_id=f.role_id "
        "WHERE f.game_version='FC26' AND f.kernel25 IS NOT NULL"
    ).fetchall()
    unknown = sorted({r["position_type"] for r in rows} - set(PITCH_ORDER))
    if unknown:
        sys.exit(f"gen_role_kernels: PITCH_ORDER에 없는 position_type {unknown} — 순서를 정의할 것")
    by_role = {}
    ptype = {}
    for r in rows:
        by_role.setdefault(r["role_id"], []).append((r["focus"], r["kernel25"]))
        ptype[r["role_id"]] = r["position_type"]
    lines = []
    for role in sorted(by_role, key=lambda x: (PITCH_ORDER.index(ptype[x]), x)):
        inner = ",".join(f"'{f}':'{k}'" for f, k in sorted(by_role[role]))
        lines.append(f"  {role}:{{{inner}}},")
    return "const MAPS = {\n" + "\n".join(lines) + "\n};", len(rows)


def gen_role_variants(conn):
    """ROLE_VARIANTS — 위치 변형 217개 (obs#107, SSOT 2단계).

    obs#94에서 placedMap이 "슬롯 x 최근접 변형을 골라 그대로 쓴다"로 바뀐 뒤 이 표가
    placedMap의 실질 본체다. MAPS(중앙판 커널 85개)와는 별개 자료다.

    정렬은 MAPS와 같은 **피치 순서** + role_id + focus + pitch_x. pitch_x 오름차순은
    툴 원본과 같으므로 diff 0이 성립한다.
    """
    PITCH_ORDER = ["GK", "CB", "FB", "DM", "CM", "CAM", "WM", "W", "ST"]
    rows = conn.execute(
        "SELECT v.role_id, v.focus, v.pitch_x, v.kernel25, r.position_type "
        "FROM game_role_variants v JOIN game_roles r "
        "  ON r.game_version=v.game_version AND r.role_id=v.role_id "
        "WHERE v.game_version='FC26' "
        "ORDER BY v.role_id, v.focus, v.pitch_x"
    ).fetchall()
    unknown = sorted({r["position_type"] for r in rows} - set(PITCH_ORDER))
    if unknown:
        sys.exit(f"gen_role_variants: PITCH_ORDER에 없는 position_type {unknown}")
    by_role, ptype = {}, {}
    for r in rows:
        by_role.setdefault(r["role_id"], {}).setdefault(r["focus"], []).append(
            (r["pitch_x"], r["kernel25"]))
        ptype[r["role_id"]] = r["position_type"]
    lines = []
    for role in sorted(by_role, key=lambda x: (PITCH_ORDER.index(ptype[x]), x)):
        parts = []
        for focus in sorted(by_role[role]):
            vs = ",".join(f"[{x},'{k}']" for x, k in by_role[role][focus])
            parts.append(f"'{focus}':[{vs}]")
        lines.append(f"  {role}:{{{','.join(parts)}}},")
    return "const ROLE_VARIANTS = {\n" + "\n".join(lines) + "\n};", len(rows)


def warn_unknown_teams(conn):
    """TEAM_CODES에 없는 팀 코드가 DB에 생기면 조용히 누락되므로 경고한다.

    2026-08-11 이전에는 이 함수가 `warn_dropped_teams`였고 "AVL 외 팀은 전부 UI에서
    제외됨"을 알렸다 — 그때는 AUTOGEN 블록이 빌라 전용이었기 때문이다. 이제 세 팀을
    모두 싣기 때문에, 남은 위험은 **네 번째 팀 코드**가 등장하는 경우뿐이다."""
    unknown = []
    for table in ("transfer_targets", "transfer_outgoing", "transfer_ledger", "squad_positions"):
        ph = ",".join("?" * len(TEAM_CODES))
        for team, n in conn.execute(
            f"SELECT team, COUNT(*) FROM {table} WHERE team NOT IN ({ph}) GROUP BY team",
            TEAM_CODES,
        ).fetchall():
            unknown.append(f"{table}:{team}={n}")
    if unknown:
        print(
            f"⚠️  TEAM_CODES에 없는 팀 행이 UI에서 제외됨 — {', '.join(unknown)}. "
            f"이 스크립트의 TEAM_CODES와 fc26-heatmap.html의 TEAMS 레지스트리에 "
            f"해당 코드를 추가할 것 (docs/40-pipeline.md).",
            file=sys.stderr,
        )


def replace_block(html, marker, new_body):
    start = f"/* AUTOGEN:{marker}:START */"
    end = f"/* AUTOGEN:{marker}:END */"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(html):
        sys.exit(f"marker block {marker} not found in {HTML}")
    replacement = f"{start}\n{new_body}\n{end}"
    return pattern.sub(lambda _m: replacement, html, count=1)


def main():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    html = HTML.read_text(encoding="utf-8")
    warn_unknown_teams(conn)
    kernels_body, n_kernels = gen_role_kernels(conn)
    variants_body, n_variants = gen_role_variants(conn)

    # 팀별 블록 4종 — 세 팀을 모두 싣는다(빈 팀도 키는 남긴다).
    counts = {}
    for marker, fn in (("TRANSFER_TARGETS", gen_transfer_targets),
                       ("TRANSFER_OUTGOING", gen_transfer_outgoing),
                       ("TRANSFER_LEDGER", gen_transfer_ledger),
                       ("XI_OWNED", gen_xi_owned)):
        per_team = {code: fn(conn, code) for code in TEAM_CODES}
        counts[marker] = {c: len(v) for c, v in per_team.items()}
        html = replace_block(html, marker, by_team_block(marker, per_team))
    html = replace_block(html, "MAPS", kernels_body)
    html = replace_block(html, "ROLE_VARIANTS", variants_body)
    HTML.write_text(html, encoding="utf-8")
    # ⭐ 2026-07-31 — 프리뷰 미러 자동 갱신.
    # 프리뷰 데몬은 ~/Documents TCC 권한이 없어 /private/tmp 미러를 서빙한다(.claude/launch.json).
    # 종전에는 이 cp를 사람이 손으로 해야 해서 **빠뜨리면 브라우저가 옛 화면을 보여주고**
    # 캐시 문제로 오진하게 됐다(2026-07-31에 두 번 발생). 툴을 재생성하는 이 스크립트가
    # 미러까지 책임지는 것이 옳다. 미러 디렉터리가 없으면 조용히 건너뛴다(프리뷰 미사용 환경).
    mirror = Path("/private/tmp/tactics-preview")
    if mirror.is_dir():
        shutil.copy2(HTML, mirror / HTML.name)
        print(f"mirrored → {mirror / HTML.name}")
    summary = " + ".join(
        f"{m} " + "/".join(f"{c}:{counts[m][c]}" for c in TEAM_CODES) for m in counts)
    print(f"synced {summary} + {n_kernels} MAPS + {n_variants} ROLE_VARIANTS into {HTML.name}")


if __name__ == "__main__":
    main()
