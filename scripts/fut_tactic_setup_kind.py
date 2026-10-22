#!/usr/bin/env python3
"""인게임 전술(fut_tactics pulled 행) ↔ 시즌 프리셋(team_tactic_setups.kind) 자동 판정 (2026-10-22 · migration 118).

왜: pulled 코드가 어느 프리셋(optimal · optimal:low-possession …)을 켠 것인지 적는 칸이 없어 「LB가 #33 값인데 괴리인지
  의도인지」를 판별할 수 없었다(구현 검토 §1.2 LB 행 · §2.3 #10). club_sync.py 전술 단계가 손 적재 뒤에 이 스크립트를 부른다.

판정(행마다 · pulled 날짜에 살아 있던 버전 `core.game_version.live_on` · 그 시즌):
  ① 포메이션(fut 표기 → 정본 표기)·빌드업·수비 접근·라인 4개가 전부 같은 team_tactic_setups 행(-deprecated 제외)이 후보.
     후보에 `optimal`이 있으면 그것 · 없고 하나뿐이면 그것 · 여럿이면 NULL + 보고 · 없으면 NULL + 보고.
  ② 11칸 역할/포커스는 slot_canon_roles(그 포메이션 정본)와 대조해 차이를 setup_diff에 적는다 — 정본을 고치지 않는다
     (인게임 칸이 정본과 다른 것은 사용자 판단 사안 · club-sync 런북 §3-3 「보고만 하고 고치지 않는다」).
  setup_kind가 이미 있는 행은 건너뛴다(불변규칙 2). `--all`로 결손 행 전부, 기본은 최신 pulled 행만.

사용:
    python3 scripts/fut_tactic_setup_kind.py            # 최신 pulled 행
    python3 scripts/fut_tactic_setup_kind.py --all      # setup_kind가 비어 있는 행 전부
    python3 scripts/fut_tactic_setup_kind.py --dry-run
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                        # noqa: E402
from core.db import connect as connect_db                  # noqa: E402  ⭐ DB 연결 정본
from core.game_version import live_on                      # noqa: E402
from scripts.collect_futgg_history import ROLE_NAME_TO_ID, ROLE_POS_GROUP  # noqa: E402  역할 이름 → role_id 단일 정본

# fut.gg/EA 포메이션 표기 → team_tactic_setups·slot_canon_roles 표기. 다른 포메이션은 슬롯 대응표가 없어 3축만 판정한다.
FUT_FORMATION = {"4-2-3-1 (2)": "4-2-3-1 Wide"}
# EA positionUniqueId(4-2-3-1 (2)) → 정본 슬롯 pos. EA는 수비수·미드필더를 오른쪽부터 센다(2=RCB·3=LCB · 5=RDM·6=LDM —
#   2026-10-22 pulled 행의 포커스(2 Aggressive=RCB 정본 · 6 Roaming=LDM 정본)로 확인).
FUT_SLOT = {"4-2-3-1 Wide": {0: "GK", 1: "RB", 2: "RCB", 3: "LCB", 4: "LB", 5: "RDM", 6: "LDM", 7: "RM", 8: "LM", 9: "CAM", 10: "ST"}}
REGIME = 1   # fut 계정은 에메리·빌라 구현 계정 하나다(fut_tactics.account_id=1)


def season_of(day):
    y, m = int(day[:4]), int(day[5:7])
    return f"{y}-{str(y + 1)[2:]}" if m >= 7 else f"{y - 1}-{str(y)[2:]}"


def judge(con, account_id, pulled):
    """(setup_kind 또는 None, setup_diff 문자열, 보고 줄 목록)"""
    t = con.execute("SELECT formation, build_up_style, defensive_approach, line_height, tactic_code FROM fut_tactics "
                    "WHERE account_id=? AND pulled=?", (account_id, pulled)).fetchone()
    form = FUT_FORMATION.get(t[0], t[0])
    gv, season = live_on(con, pulled[:10]), season_of(pulled[:10])
    cands = con.execute("""SELECT id, kind FROM team_tactic_setups WHERE regime_id=? AND game_version=? AND season=?
                           AND kind NOT LIKE '%-deprecated' AND formation=? AND build_up_style=? AND defensive_approach=?
                           AND line_height=? ORDER BY kind""", (REGIME, gv, season, form, t[1], t[2], t[3])).fetchall()
    notes = []
    kinds = [k for _, k in cands]
    if "optimal" in kinds:
        kind = "optimal"
    elif len(kinds) == 1:
        kind = kinds[0]
    else:
        kind = None
        notes.append(f"3축 일치 후보 {'없음' if not kinds else '여럿: ' + ' · '.join(kinds)} "
                     f"({form} · {t[1]}/{t[2]}/{t[3]} · {gv} {season})")
    # ② 11칸 대조 — 정본은 slot_canon_roles(그 포메이션 · 그 버전)
    canon = {p: (r, f) for p, r, f in con.execute(
        "SELECT pos, role_id, focus FROM slot_canon_roles WHERE regime_id=? AND game_version=? AND formation=?", (REGIME, gv, form))}
    slot = FUT_SLOT.get(form)
    if not canon or not slot:
        diff = f"11칸 대조 불가({form} 슬롯 대응표/정본 없음)"
    else:
        diffs, n_ok, missing = [], 0, []
        for pid, pname, rname, focus in con.execute(
                "SELECT position_id, position_name, role_name, focus FROM fut_tactic_roles WHERE account_id=? AND pulled=? ORDER BY position_id",
                (account_id, pulled)):
            pos = slot.get(pid)
            rid = ROLE_NAME_TO_ID.get((ROLE_POS_GROUP.get(pname, pname), rname))
            if pos not in canon or rid is None:
                missing.append(f"{pname}#{pid} {rname}")
                continue
            if (rid, focus) == canon[pos]:
                n_ok += 1
            else:
                diffs.append(f"{pos} {canon[pos][0]}/{canon[pos][1]}→{rid}/{focus}")
        diff = f"일치 {n_ok}/{len(canon)}" + (f" · 불일치 {len(diffs)}칸: " + " · ".join(diffs) if diffs else "") \
            + (f" · 대응 불가: " + " · ".join(missing) if missing else "")
    return kind, diff, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="setup_kind가 비어 있는 행 전부(기본: 최신 pulled 행만)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    con = connect_db(DB)
    rows = con.execute("SELECT account_id, pulled, tactic_code FROM fut_tactics WHERE setup_kind IS NULL ORDER BY pulled"
                       + ("" if a.all else " DESC LIMIT 1")).fetchall()
    if not rows:
        print("setup_kind 결손 행 없음")
        return
    unresolved = 0
    for acc, pulled, code in rows:
        kind, diff, notes = judge(con, acc, pulled)
        print(f"{pulled} {code or '-':14} → setup_kind={kind or 'NULL'} · {diff}")
        for n in notes:
            print(f"   ⚠️ {n}")
        unresolved += kind is None
        if not a.dry_run:
            con.execute("UPDATE fut_tactics SET setup_kind=?, setup_diff=? WHERE account_id=? AND pulled=?",
                        (kind, diff, acc, pulled))
    if not a.dry_run:
        con.commit()
    print(f"{'[dry-run] ' if a.dry_run else ''}{len(rows)}행 판정 · 미해결 {unresolved}"
          + (" — ⚠️ 종료 보고에 적을 것(어느 프리셋인지 사람이 판단)" if unresolved else ""))


if __name__ == "__main__":
    main()
