#!/usr/bin/env python3
"""`measured` 계열 표본 감사 — 「포지션-순수」 선언이 사실인지 원천에서 확인한다 (2026-09-15 신설).

왜 (사용자 지시 「measured 계열 표본 감사 해줘」, obs#768·769):
  헤밍스 `#470`이 스스로 「**포지션-순수(LM) 6경기**」라 적고도 `pos_class=LDM`인 경기를 포함했다
  (90분 = 461분의 19.5%). ⇒ ⭐⭐ **「포지션-순수」라는 라벨을 믿을 수 없다.**

두 경로로 본다 — 둘이 보는 것이 다르다:
  ⑴ **일자 대조** — rationale이 열거한 경기 일자를 `player_matches.pos_class`와 맞춘다.
     「rationale이 거짓말을 하는가」를 본다.
  ⑵ **집계 재현** — `core.aggregate.player_aggregate`로 포지션-순수 재집계해 `map25`를 문자열 대조한다.
     rationale을 **거치지 않고 원천에서 다시 만들므로** 이쪽이 강하다.

⛔ **읽기 전용이다** — 아무것도 고치지 않는다. 오염이 전부 결함은 아니기 때문이다:
  ⑴ `pos_label`이 「우리 슬롯」이고 측정은 「실제 출전」일 수 있다(이강인 RST ↔ 실제 RM)
  ⑵ SofaScore `pos_class`가 같은 기능 역할에 대해 경기마다 흔들린다(소보슬라이 RDM↔CAM↔RAM)
  ⇒ 사람이 판정한다. 다만 **어느 쪽이든 「포지션-순수」 표기는 사실과 맞춰야 한다.**

사용:
    .venv/bin/python scripts/audit_measured_samples.py
    .venv/bin/python scripts/audit_measured_samples.py --season 2026-27
"""
import argparse
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                     # noqa: E402
from core.aggregate import player_aggregate             # noqa: E402

# pos_label → 허용 pos_class. ⛔ 좁게 잡는다 — 넓게 잡으면 오염을 통과시킨다.
OK = {"GK": ("GK",), "LB": ("LB",), "RB": ("RB",), "LCB": ("LCB",), "RCB": ("RCB",),
      "CCB": ("CCB", "CB"), "LDM": ("LDM",), "RDM": ("RDM",), "CDM": ("CDM",),
      "LCM": ("LCM",), "RCM": ("RCM",), "CAM": ("CAM",),
      "LM": ("LM", "LAM"), "RM": ("RM", "RAM"), "ST": ("ST",), "LST": ("LST",), "RST": ("RST",),
      "LAM": ("LAM",), "RAM": ("RAM",), "LW": ("LW",), "RW": ("RW",), "CM": ("CM",)}

# ⭐ 사람이 판정을 끝낸 행의 표식(2026-09-15 신설). 오염이 **전부 결함은 아니므로**
#    — pos_label이 우리 슬롯이거나(RDM↔RCM), pos_class 자체가 현상인 경우(false9→CAM) —
#    판정이 끝난 행을 계속 ⛔로 띄우면 **영구 오탐**이 되어 게이트로 못 올린다.
ADJUDICATED = "[표본판정"
USED = "사용 경기"      # 재집계가 남기는 「사용 경기 N건(...): 날짜…」 목록의 표식
DATE = re.compile(r"(20\d\d-\d\d-\d\d)\(")
SEG = re.compile(r"\[20\d\d-\d\d-\d\d[^\]]*\]")


def name(con, pid):
    return con.execute("SELECT COALESCE(name_kr, name) FROM players WHERE id=?", (pid,)).fetchone()[0]


def audit_dates(con):
    """⑴ rationale이 열거한 일자의 pos_class 대조."""
    bad, done = [], []
    for r in con.execute("SELECT id, player_id, pos_label, sample_n, rationale FROM prescriptions "
                         "WHERE kind LIKE 'measured%' AND rationale LIKE '%(%'"):
        ra = r["rationale"] or ""
        # ⭐ 「사용 경기」 명시 목록이 있으면 그것만 읽는다(2026-09-15 추가).
        #    ⛔ 없으면 마지막 일자 포함 구간을 쓰는데, 그 방식은 **제외 사유로 언급한 일자**를
        #       사용 일자와 구분하지 못한다(헤밍스 #470에서 실증: 「2026-08-23(브라이턴)의 pos_class는 LDM」이
        #       제외 설명인데 사용 일자로 세어졌다). 재집계 시 「사용 경기」 목록을 반드시 쓴다.
        if USED in ra:
            dates = DATE.findall(ra[ra.rindex(USED):])
        else:
            parts = SEG.split(ra)
            dates = next((d for d in (DATE.findall(s) for s in reversed(parts)) if d), [])
        if not dates:
            continue
        dates = sorted(set(dates))
        allow = OK.get((r["pos_label"] or "").strip())
        if not allow:
            continue
        off, miss = [], []
        for d in dates:
            m = con.execute("SELECT pos_class FROM player_matches WHERE player_id=? AND date=?",
                            (r["player_id"], d)).fetchone()
            if not m:
                miss.append(d)
            elif m[0] is not None and m[0] not in allow:
                off.append((d, m[0]))
        if off or miss or (r["sample_n"] and r["sample_n"] != len(dates)):
            rec = (r["id"], name(con, r["player_id"]), r["pos_label"],
                   r["sample_n"], len(dates), off, miss)
            (done if ADJUDICATED in (r["rationale"] or "") else bad).append(rec)
    return bad, done


def audit_reproduce(con, season):
    """⑵ 포지션-순수 재집계로 map25 재현 여부. (재현, 불일치, 표본부족, 어휘밖)"""
    ok, diff, thin, unk, done = [], [], [], [], []
    for r in con.execute("SELECT id, player_id, pos_label, sample_n, minutes, map25, rationale "
                         "FROM prescriptions "
                         "WHERE kind='measured' AND map25 IS NOT NULL AND season=?", (season,)):
        allow = OK.get((r["pos_label"] or "").strip())
        if not allow:
            # ⭐ 서술 라벨(`LWB(3-4-2-1)` 등)은 판정이 끝났으면 어휘밖으로 세지 않는다
            rec = (r["id"], name(con, r["player_id"]), r["pos_label"])
            (done if ADJUDICATED in (r["rationale"] or "") else unk).append(rec)
            continue
        ph = ",".join("?" * len(allow))
        agg = player_aggregate(r["player_id"],
                               where=f"season=? AND minutes>=45 AND pos_class IN ({ph})",
                               params=(season, *allow))
        row = (r["id"], name(con, r["player_id"]), r["pos_label"], r["sample_n"], r["minutes"])
        adj = ADJUDICATED in (r["rationale"] or "")
        if not agg:
            (done if adj else thin).append(row)
        elif agg["map25"] == r["map25"]:
            ok.append(row)
        elif adj:
            done.append(row)
        else:
            diff.append(row + (agg["n"], agg["minutes"]))
    return ok, diff, thin, unk, done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--season", default="2026-27")
    a = ap.parse_args()
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    bad, done1 = audit_dates(con)
    print(f"=== ⑴ 일자 대조 — 미판정 이상 {len(bad)}행 · 판정완료 {len(done1)}행 ===")
    for i, nm, pos, nd, nl, off, miss in sorted(bad):
        print(f"  #{i} {nm} [{pos}] 선언 n={nd} · 열거 {nl}건")
        for d, c in off:
            print(f"      ⛔ {d} pos_class={c} ← 허용 {OK[pos]} 밖")
        for d in miss:
            print(f"      ⛔ {d} player_matches에 행 없음")

    ok, diff, thin, unk, done2 = audit_reproduce(con, a.season)
    print(f"\n=== ⑵ 집계 재현({a.season}) — ✅재현 {len(ok)} · ⛔불일치 {len(diff)} · "
          f"⛔⛔표본부족 {len(thin)} · ⊘판정완료 {len(done2)} · 어휘밖 {len(unk)} ===")
    print("\n  ⛔ map25 불일치 (선언 → 포지션-순수 재집계)")
    for i, nm, pos, nd, md, na, ma in sorted(diff, key=lambda x: (x[3] or 0) - x[5], reverse=True):
        kind = "오염" if (nd or 0) > na else "노후" if (nd or 0) < na else "동수·다른구성"
        print(f"    #{i:<5}{nm:<14}{pos:<5} n={nd}({md}분) → n={na}({ma}분)  [{kind}]")
    print("\n  ⛔⛔ 순수 표본 2경기 미만 — core.aggregate 「집계 금지」 위반")
    for i, nm, pos, nd, md in sorted(thin):
        act = con.execute("""SELECT pos_class, COUNT(*) n, SUM(minutes) m FROM player_matches
                             WHERE player_id=(SELECT player_id FROM prescriptions WHERE id=?)
                               AND season=? AND minutes>=45 AND hit_points>=15
                             GROUP BY pos_class ORDER BY m DESC LIMIT 2""", (i, a.season)).fetchall()
        real = " · ".join(f"{x['pos_class']} {x['n']}경기 {x['m']}분" for x in act) or "(자격 출전 없음)"
        print(f"    #{i:<5}{nm:<14}선언 {pos} n={nd} → ⭐ 실제 최다: {real}")
    if unk:
        print("\n  ⚠️ pos_label 어휘밖:", ", ".join(f"#{i} {nm}({p})" for i, nm, p in unk))
    print("\n⛔ 읽기 전용 — 판정은 사람이 한다(리포트 reports/ingame/2026-09-15-measured-sample-audit.md).")


if __name__ == "__main__":
    main()
