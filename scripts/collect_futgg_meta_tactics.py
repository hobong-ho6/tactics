#!/usr/bin/env python3
"""fut.gg 커뮤니티 메타 전술(포메이션별 실사용 통계) → team_tactic_setups `meta:futgg-<날짜>` 행 (2026-10-22 신설).

왜 (FC27 시스템 검토 2026-10-22 §2 ⒜6 · §7 조치 4): 인게임 A/B에 「이기는 설정」 대조군이 없었다. fut.gg `/tactics/<formation>/`은
    활성 스쿼드 추적으로 포메이션 사용률·3축 분포·라인 높이·대표 코드·11칸 역할/포커스 분포를 준다(등급 B · 사용 통계이지 효과 근거가 아니다).
    ⚠️ 메타는 「에메리 재현」이 아니다 — 정본(optimal)을 메타로 바꾸는 근거로 쓰지 않는다. `fut_tactic_setup_kind.py`도 meta를 후보에서 뺀다.

저장: team_tactic_setups(regime AVL · 현행 버전 · 현 시즌 · kind=meta:futgg-<포메이션 슬러그>-<pulled> — UNIQUE(regime·season·version·kind)라 포메이션을 kind에 넣는다) 포메이션당 1행 · 11칸 분포는 rationale에 정형 줄(`ROLES:`)로.
    같은 pulled·포메이션 행이 있으면 건너뛴다(추가만 · 불변규칙 2). 역할 이름 → role_id는 game_roles.name_en과 유일 일치할 때만 적는다.

사용:
    .venv/bin/python scripts/collect_futgg_meta_tactics.py --dry-run
    .venv/bin/python scripts/collect_futgg_meta_tactics.py [--formations "4-2-3-1 Wide,4-4-2,3-4-2-1"] [--pulled 2026-10-22]
"""
import argparse
import datetime as dt
import html as _html
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core.db import connect as connect_db  # noqa: E402
from core.game_version import current as gv_current  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
REGIME = 1                     # AVL/에메리 — 대조군은 주 대상 체제에만 둔다
DEFAULT_FORMATIONS = ["4-2-3-1 Wide", "4-4-2", "3-4-2-1"]
SLUG = {"4-2-3-1 Wide": "4-2-3-1-wide", "4-4-2": "4-4-2", "3-4-2-1": "3-4-2-1", "4-1-4-1": "4-1-4-1", "3-4-3": "3-4-3", "5-4-1": "5-4-1"}
# fut.gg 역할 이름 → game_roles.name_en과 다른 표기만 손으로 잇는다(나머지는 이름 유일 일치)
ROLE_ALIAS = {"Deep-Lying Playmaker": "Deep Lying Playmaker", "Box-To-Box": "Box to Box", "Ball-Playing Defender": "Ball Playing Defender",
              "Ball Playing Keeper": "Ball-Playing Keeper", "Wide Playmaker": "Wide Playmaker", "Shadow Striker": "Shadow Striker"}
POS_GROUP = {"GK": "GK", "RB": "FB", "LB": "FB", "RCB": "CB", "LCB": "CB", "CB": "CB", "RDM": "DM", "LDM": "DM", "CDM": "DM",
             "RCM": "CM", "LCM": "CM", "CM": "CM", "CAM": "CAM", "RAM": "CAM", "LAM": "CAM", "RM": "WM", "LM": "WM",
             "RW": "W", "LW": "W", "ST": "ST", "RS": "ST", "LS": "ST"}


def page_text(url):
    b = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "ignore")
    t = re.sub(r"<script.*?</script>", "", b, flags=re.S)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = _html.unescape(t)
    return [ln.strip() for ln in t.split("\n") if ln.strip()]


def parse(lines, formation):
    """텍스트 줄 목록 → dict(overview · dist · code · slots · roles)"""
    joined = "\n".join(lines)
    out = {"formation": formation}
    m = re.search(r"run by (<?\d+%) of them.*?a (\w[\w ]*?) build-up style, a (\w+) defensive line at a line height of (\d+)", joined, re.S)
    if not m:
        raise SystemExit(f"⛔ {formation}: 개요 문장을 못 찾았다 — fut.gg 페이지 구조가 바뀌었다")
    out["usage_comm"], out["build_up"], out["def_line"], out["line_height"] = m.group(1), m.group(2), m.group(3), int(m.group(4))
    mp = re.search(r"Pros\n(<?\d+%)\nof pro squads", joined)
    out["usage_pro"] = mp.group(1) if mp else None
    mr = re.search(r"#\n(\d+)\n most-used formation", joined)
    out["rank"] = int(mr.group(1)) if mr else None

    def nums(j):
        """lines[j]부터 (숫자, '%') 쌍을 읽는다 — 프로 열이 없는 페이지(3-4-2-1)는 1쌍만 온다. (값 목록, 다음 인덱스)"""
        vals = []
        while j + 1 < len(lines) and re.fullmatch(r"<?\d+", lines[j]) and lines[j + 1] == "%":
            vals.append(int(lines[j].lstrip("<")))
            j += 2
        return vals, j

    def dist(label, n):
        i = lines.index(label)
        res = {}
        j = i + 1
        for _ in range(n):
            name = lines[j]
            vals, j = nums(j + 1)
            res[name] = (vals[0] if vals else None, vals[1] if len(vals) > 1 else None)
        return res
    out["build_dist"] = dist("Build-up style", 3)
    out["def_dist"] = dist("Defensive line", 4)
    i = lines.index("Line height")
    out["line_comm"] = int(lines[i + 2])
    out["line_pro"] = int(lines[i + 4]) if lines[i + 3] == "Pros" else None
    i = lines.index("Code")
    out["code"] = lines[i + 1]
    # 11칸 대표 역할/포커스: "Positions" 뒤 포지션 목록 다음에 (POS, Role, Focus)×N
    i = lines.index("Positions")
    # 「Positions」 뒤에는 ⑴ 포지션 목록(「RDM · LDM」 같은 묶음 포함) ⑵ (POS, Role, Focus)×11 이 온다. 11칸은 늘 GK부터 —
    # 「GK」 다음 둘째 줄이 포커스 어휘인 첫 자리를 11칸의 시작으로 잡는다(목록의 GK는 다음 줄이 또 GK라 걸리지 않는다).
    FOCUS = {"Defend", "Balanced", "Build-Up", "Attack", "Roaming", "Support", "Aggressive", "Ball-Winning", "Sweeper", "Versatile", "Unknown"}
    j = i + 1
    while not (lines[j] == "GK" and j + 2 < len(lines) and lines[j + 2] in FOCUS):
        j += 1
    slots = []
    while j + 2 < len(lines) and re.fullmatch(r"(GK|RB|LB|RCB|LCB|CB|RDM|LDM|CDM|RCM|LCM|CM|CAM|RAM|LAM|RM|LM|RW|LW|ST|RS|LS)", lines[j]) and not lines[j + 1].startswith("The "):
        slots.append((lines[j], lines[j + 1], lines[j + 2]))
        j += 3
    if len(slots) != 11:
        raise SystemExit(f"⛔ {formation}: 11칸이 아니라 {len(slots)}칸을 읽었다 — 페이지 구조 확인")
    out["slots"] = slots
    # 칸별 역할/포커스 분포(상위 4)
    roles = {}
    for k in range(len(lines)):
        if lines[k] == "Roles used here" and k >= 4:
            # 형태: POS / Role / Focus / "focus" / "Roles used here" / Community / [Pros] / (Role / · / Focus / c / % / [p / %])×n
            #   POS는 「RDM · LDM」처럼 묶음 라벨일 수 있다 — 양쪽 칸에 같은 분포를 둔다.
            pos_label = lines[k - 4]
            m2 = k + 1
            while m2 < len(lines) and lines[m2] in ("Community", "Pros"):
                m2 += 1
            arr = []
            while m2 + 4 < len(lines) and lines[m2 + 1] == "·":
                vals, nxt = nums(m2 + 3)
                arr.append((lines[m2], lines[m2 + 2], vals[0] if vals else None, vals[1] if len(vals) > 1 else None))
                m2 = nxt
            for pos in [x.strip() for x in pos_label.split("·")]:
                roles[pos] = arr
    out["roles"] = roles
    return out


# fut.gg 영문 역할 이름 → role_id 접미(game_roles.name_en이 비어 있어 이름 유일 일치를 못 쓴다 · 접두는 포지션군)
ROLE_SUFFIX = {"Goalkeeper": "goalkeeper", "Ball Playing Keeper": "ballplaying", "Ball-Playing Keeper": "ballplaying", "Sweeper Keeper": "sweeper",
               "Fullback": "fullback", "Falseback": "falseback", "Wingback": "wingback", "Attacking Wingback": "att_wb", "Inverted Fullback": "inverted",
               "Defender": "defender", "Stopper": "stopper", "Ball-Playing Defender": "bpd", "Ball Playing Defender": "bpd", "Wide Back": "wideback",
               "Holding": "holding", "Centre-Half": "centrehalf", "Centre Half": "centrehalf", "Deep-Lying Playmaker": "dlp", "Deep Lying Playmaker": "dlp",
               "Wide Half": "widehalf", "Box Crasher": "boxcrasher", "Box-To-Box": "b2b", "Box to Box": "b2b", "Playmaker": "playmaker",
               "Half Winger": "halfwinger", "Shadow Striker": "shadow", "Classic 10": "classic10", "Winger": "winger", "Inside Forward": "insidefwd",
               "Wide Midfielder": "widemid", "Wide Playmaker": "wideplm", "Advanced Forward": "advanced", "Poacher": "poacher",
               "False 9": "false9", "Target Forward": "target"}
GROUP_PREFIX = {"GK": "gk", "FB": "fb", "CB": "cb", "DM": "dm", "CM": "cm", "CAM": "cam", "WM": "wm", "W": "w", "ST": "st"}


def role_id_map(con, gv):
    return {rid for (rid,) in con.execute("SELECT role_id FROM game_roles WHERE game_version=?", (gv,))}


def to_role_id(known, pos, role_name):
    suf = ROLE_SUFFIX.get(role_name)
    pre = GROUP_PREFIX.get(POS_GROUP.get(pos, pos))
    rid = f"{pre}_{suf}" if pre and suf else None
    return rid if rid in known else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--formations", default=",".join(DEFAULT_FORMATIONS))
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    con = connect_db()
    gv = gv_current(con)
    y, mth = int(a.pulled[:4]), int(a.pulled[5:7])
    season = f"{y}-{str(y + 1)[2:]}" if mth >= 7 else f"{y - 1}-{str(y)[2:]}"
    by_name = role_id_map(con, gv)
    added = []
    for formation in [f.strip() for f in a.formations.split(",") if f.strip()]:
        slug = SLUG.get(formation)
        if not slug:
            print(f"건너뜀(슬러그 미등록): {formation}"); continue
        # team_tactic_setups는 UNIQUE(regime, season, game_version, kind) — 포메이션을 kind에 넣는다
        kind = f"meta:futgg-{slug}-{a.pulled}"
        if con.execute("SELECT 1 FROM team_tactic_setups WHERE regime_id=? AND game_version=? AND season=? AND kind=? AND formation=?",
                       (REGIME, gv, season, kind, formation)).fetchone():
            print(f"이미 있음: {kind} {formation}"); continue
        url = f"https://www.fut.gg/tactics/{slug}/"
        d = parse(page_text(url), formation)
        pct = lambda c, p: f"{c}%/{p}%" if p is not None else f"{c}%"
        role_lines = []
        for pos, rname, focus in d["slots"]:
            rid = to_role_id(by_name, pos, rname)
            top = d["roles"].get(pos, [])
            share = next(((c, p) for r, f, c, p in top if r == rname and f == focus), (None, None))
            alt = " | ".join(f"{r}/{f} {pct(c, p)}" for r, f, c, p in top[:4])
            role_lines.append(f"{pos}: {rname}/{focus}" + (f" [{rid}]" if rid else " [role_id 미대응]")
                              + (f" {pct(share[0], share[1])}" if share[0] is not None else "") + (f" · 상위: {alt}" if alt else ""))
        rationale = (
            f"⭐ fut.gg 커뮤니티 메타 전술 대조군({formation} · {a.pulled} 열람 · 등급 B 사용 통계 · 효과 근거 아님). "
            f"사용률 커뮤니티 {d['usage_comm']}(#{d['rank']} 최다 사용) · 프로 {d['usage_pro']}. "
            f"빌드업 분포(커뮤/프로) " + " · ".join(f"{k} {pct(c, p)}" for k, (c, p) in d["build_dist"].items())
            + " · 수비 라인 " + " · ".join(f"{k} {pct(c, p)}" for k, (c, p) in d["def_dist"].items())
            + f" · 라인 높이 커뮤 {d['line_comm']} / 프로 {d['line_pro']}. 대표 코드 {d['code']}.\n"
            "⚠️ 「이기는 설정」이지 「에메리 재현」이 아니다 — 정본(optimal)을 바꾸는 근거로 쓰지 않는다(FC27 시스템 검토 2026-10-22 §6). "
            "인게임 A/B(T6·T7)의 대조군 코드로만 쓴다. fut_tactic_setup_kind.py는 meta를 후보에서 뺀다.\n"
            "ROLES: (칸: 대표 역할/포커스 [role_id] 커뮤%/프로% · 상위 분포)\n" + "\n".join(role_lines)
        )
        row = (REGIME, season, gv, kind, formation, d["build_up"], d["def_line"], d["line_comm"], d["code"], rationale,
               f"B — fut.gg /tactics/{slug}/ 활성 스쿼드 통계({a.pulled}) · 사용률이지 효과 근거가 아님", formation)
        print(f"{'[dry] ' if a.dry_run else ''}{kind} {formation}: {d['build_up']}/{d['def_line']}/{d['line_comm']} 코드 {d['code']} · "
              f"사용 {d['usage_comm']}/{d['usage_pro']} · 11칸 role_id 대응 {sum(1 for l in role_lines if '미대응' not in l)}/11")
        for l in role_lines:
            print("   ", l)
        if not a.dry_run:
            cur = con.execute("INSERT INTO team_tactic_setups(regime_id, season, game_version, kind, formation, build_up_style, defensive_approach, "
                              "line_height, tactic_code, rationale, confidence, ingame_formation) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", row)
            added.append(cur.lastrowid)
    if not a.dry_run:
        con.commit()
    print("추가 행:", added)


if __name__ == "__main__":
    main()
