#!/usr/bin/env python3
"""영상·스카우트 분석의 **반영 상태 재계산** — 자동 판정분만 (2026-09-14 신설, 09-15 정밀화).

왜:
  `player_duties.applied_status`는 「이 분석이 처방에 닿았는가」를 담는다(migration 031, G16).
  처방·분석이 늘어날 때마다 다시 계산해야 하므로 **재실행 가능한 스크립트**로 뺐다.
  match-watch 회차마다 실측·처방을 갱신한 뒤 이 스크립트를 돌린다.

⛔ **사람이 내린 판정(APPLIED/HELD/REJECTED)은 건드리지 않는다** — 자동 4종만 재계산한다.

⛔⛔ **「자동 4종만 재계산」은 `applied_status`에만 참이고 `applied_note`에는 거짓이었다**(2026-09-15 사고).
   자동 상태의 **사유에도 사람이 쓴 교정이 들어 있다** — ATM PROSE 9행의 「재판정 조건: map25 수집」이
   틀렸다고 손으로 고쳐놨는데 이 스크립트가 재실행에서 **자동 템플릿으로 통째로 덮었다**.
   G14는 `applied_note`를 보호 목록에 두지 않아 잡지 못했고, dump diff를 직접 읽어서야 발견했다.
   ⇒ 이제 **상태가 실제로 바뀔 때만 사유를 다시 쓴다**(`--force-note`로 강제 가능).
   ⭐ 부류: **「자동 재계산」 스크립트는 자기가 쓴 필드에 사람 손이 섞였는지 먼저 물어야 한다.**

⭐⭐ **슬롯 접두가 다른 같은 역할을 충돌로 세지 않는다** (09-15 정정 → 09-15 확장).
   역할은 `slots` 표가 정하는 슬롯과 별개 축이다 — 바르콜라 `w_wideplm`(LW 분석) ↔
   우리 `wm_wideplm`(LM 슬롯)을 충돌로 세면 오탐이다(obs#743).
   ⛔ 그런데 그 정정이 **`w_`/`wm_` 한 쌍만** 고쳤다. 전수 확인하니 어간 **7개**가 여러 접두에 걸쳐 있고
   `dlp`·`holding`(cm/dm) · `halfwinger`·`playmaker`(cam/cm) **4쌍이 오탐으로 남아 있었다**(obs#785).
   ⇒ 이제 `canon()`이 **접두를 전부 뗀다**.

사용:
    .venv/bin/python scripts/refresh_duty_applied.py --dry-run
    .venv/bin/python scripts/refresh_duty_applied.py
"""
import argparse
import datetime as dt
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                                     # noqa: E402

AUTO = ("MATCH", "CONFLICT", "NO_RX", "PROSE")


# 슬롯 접두 정본 — `game_roles.role_id`의 접두는 이 9종이다(2026-09-15 전수 확인).
SLOT_PREFIX = re.compile(r"^(cam|cb|cm|dm|fb|gk|st|wm|w)_")


def canon(role):
    """**슬롯 접두를 떼고 역할 어간만 남긴다** — 같은 역할이 슬롯마다 다른 접두를 갖기 때문이다.

    ⭐ 2026-09-15 확장(obs#785). obs#743은 `w_`/`wm_` 한 쌍만 고쳤는데,
    전수 확인 결과 **어간 7개가 여러 접두에 걸쳐 있었다**:
      `dlp`(cm/dm) · `holding`(cm/dm) · `halfwinger`(cam/cm) · `playmaker`(cam/cm) ·
      `insidefwd`·`wideplm`·`winger`(w/wm).
    ⇒ 나머지 4쌍(cm/dm · cam/cm)이 **오탐으로 남아 있었다** — 소보슬라이 `#195`가 실증
    (분석 `cm_halfwinger` ↔ 보유 `cam_halfwinger`를 불일치로 셌다).
    ⛔ 접두를 전부 떼도 **어간 충돌은 없다**(위 7개만 중복이고 전부 인접 슬롯군이다).
    """
    return SLOT_PREFIX.sub("", role or "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force-note", action="store_true",
                    help="⛔ 자동 상태의 기존 사유까지 템플릿으로 덮어쓴다 — 사람이 쓴 교정이 날아간다(2026-09-15 사고)")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    roles = {r[0] for r in con.execute("SELECT DISTINCT role_id FROM game_role_focus")}
    have = defaultdict(set)
    # ⭐ 출처별로도 따로 담는다(2026-09-20) — 「닿았을 수 있다」 보고에 근거의 층을 표기하기 위해서다.
    #   시즌 처방 ↔ 경기 전용 프리셋 ↔ fit_role은 **층이 다르다**(고정 작업 규칙 5).
    season_role, match_role, fit_role = defaultdict(set), defaultdict(set), defaultdict(set)
    for q, c, bucket in (
            ("SELECT player_id, role_id FROM prescriptions WHERE role_id IS NOT NULL", "role_id", season_role),
            ("SELECT player_id, role_id FROM match_player_prescriptions WHERE role_id IS NOT NULL", "role_id", match_role),
            ("SELECT player_id, fit_role FROM squad_entries WHERE fit_role IS NOT NULL", "fit_role", fit_role)):
        for r in con.execute(q):
            have[r["player_id"]].add(r[c])
            bucket[r["player_id"]].add(r[c])

    note0 = f"[{a.pulled} 자동 재계산] 사람 승인 아님 — 분석이 명시한 역할 코드 ↔ prescriptions·match_player_prescriptions·squad_entries.fit_role 전량 대조(슬롯 접두가 다른 같은 역할은 동일하게 봄 — canon()이 접두를 뗀다)."
    changed, kept, counts = [], [], defaultdict(int)
    for d in con.execute("""SELECT id, player_id, game_role_implication imp, applied_status, applied_note
                            FROM player_duties
                            WHERE applied_status IS NULL OR applied_status IN (%s)"""
                         % ",".join("?" * len(AUTO)), AUTO):
        found = {x for x in roles if x in (d["imp"] or "")}
        mine = have.get(d["player_id"], set())
        hit = {x for x in found if canon(x) in {canon(y) for y in mine}}
        if not found:
            st, extra = "PROSE", " 역할 코드가 없어 기계 판정 불가 — 반영 여부는 사람이 적어야 한다."
        elif not mine:
            st, extra = "NO_RX", " 이 선수의 처방 행이 아직 없다."
        elif hit:
            st, extra = "MATCH", f" 일치 역할: {', '.join(sorted(hit))}."
            slot_only = [x for x in hit if x not in mine]
            if slot_only:
                extra += f" ⭐ 슬롯 계열만 다르다({', '.join(sorted(slot_only))} ↔ 보유 {', '.join(sorted(mine))}) — 역할은 같다."
        else:
            st, extra = "CONFLICT", f" 분석 {', '.join(sorted(found))} ↔ 보유 처방 {', '.join(sorted(mine))} — 사람 판정 대기."
        counts[st] += 1
        if st != d["applied_status"]:
            changed.append((d["id"], d["applied_status"], st))
        if not a.dry_run:
            # ⛔⛔ **상태가 그대로면 사유를 건드리지 않는다**(2026-09-15 사고 후 추가).
            #    자동 상태(PROSE·MATCH·NO_RX·CONFLICT)의 사유에도 **사람이 쓴 교정이 들어 있다** —
            #    09-15에 ATM PROSE 9행의 「재판정 조건: map25 수집」이 틀렸다고 손으로 고쳐놨는데,
            #    이 스크립트가 재실행에서 그걸 **자동 템플릿으로 통째로 덮었다**(G14는 applied_note를
            #    보호 목록에 두지 않아 잡지 못했다). 종전 주석의 「자동 4종만 재계산」은
            #    **상태**에만 참이었고 **사유**에는 거짓이었다.
            #    ⇒ 사유는 **판정이 실제로 바뀔 때만** 다시 쓴다. `--force-note`로 강제 가능.
            if st != d["applied_status"] or a.force_note or not (d["applied_note"] or "").strip():
                con.execute("UPDATE player_duties SET applied_status=?, applied_note=? WHERE id=?",
                            (st, note0 + extra, d["id"]))
                kept.append(None)
            else:
                con.execute("UPDATE player_duties SET applied_status=? WHERE id=?", (st, d["id"]))
                kept.append(d["id"])
    if not a.dry_run:
        con.commit()
    print(f"자동 판정 {sum(counts.values())}행:", dict(counts))
    print(f"상태 변경 {len(changed)}행:", changed[:20])
    if not a.dry_run:
        n_kept = len([x for x in kept if x is not None])
        print(f"⭐ 사유 보존 {n_kept}행(상태 불변 — 사람이 쓴 교정을 덮지 않는다) · 사유 재작성 {len(kept) - n_kept}행")
    held = con.execute("""SELECT applied_status, COUNT(*) FROM player_duties
                          WHERE applied_status NOT IN (%s) GROUP BY 1""" % ",".join("?" * len(AUTO)), AUTO).fetchall()
    print("사람 판정(건드리지 않음):", {r[0]: r[1] for r in held})

    # ⭐⭐ **재판정 조건 충족 후보 보고**(2026-09-15 신설 — 할 일 34, obs#785).
    #    왜: HELD 34행이 「재판정 조건: 역할 자체를 다투는 새 근거(역할 코드 명시 분석 또는 커널 Δ)」를
    #    걸어놨는데, 그 뒤 처방이 대거 바뀌었음에도 **아무도 조건을 확인하지 않아 5행이 방치돼 있었다.**
    #    ⛔ 판정 시점을 `applied_note`의 날짜로 파싱하는 방식은 취하지 않는다 — 표기가 흔들리고
    #       「처방이 바뀌었는지」를 날짜로 알 수 없다. 대신 **지금 대조를 다시 해서 사람 판정과 어긋나는 상태**를 센다.
    #    ⇒ 이번 재검증에서 실제로 나온 3부류와 정확히 대응한다.
    # ⭐ 무효화된 측정 행을 가진 선수 — map25는 있는데 role_id가 비워진 행(obs#770·783 패턴).
    #    「기존 처방을 그대로 둔다」로 HELD한 근거가 사라진 경우를 잡는다.
    voided = {r[0] for r in con.execute(
        "SELECT DISTINCT player_id FROM prescriptions "
        "WHERE map25 IS NOT NULL AND role_id IS NULL AND season='2026-27'")}
    review = {"닿았을 수 있다": [], "다시 갈렸다": [], "근거가 무효화됐다": []}
    suppressed = []          # 사람이 「조건 미충족」으로 확인을 끝낸 행(2026-09-20 · obs#888)
    for d in con.execute("""SELECT id, player_id, game_role_implication imp, applied_status,
                                   applied_note,
                                   (SELECT COALESCE(name_kr, name) FROM players WHERE id=player_id) nm
                            FROM player_duties
                            WHERE applied_status NOT IN (%s)""" % ",".join("?" * len(AUTO)), AUTO):
        mine = have.get(d["player_id"], set())
        note = d["applied_note"] or ""
        # ⛔ **「처방이 아예 없다」는 후보가 아니다** — 사라진 게 아니라 애초에 없는 선수다
        #    (obs#748이 수집 불가로 종결한 ATM 3명 · 유스 선수들). 자동 판정이라면 `NO_RX`에 해당하고
        #    **상태가 변한 것이 아니라서** 회차마다 떠도 할 일이 되지 않는다. ⇒ 세지 않는다.
        # ⭐ **측정 행이 무효화된 경우만 잡는다**(map25는 있는데 role이 비었다 — obs#770·783 패턴):
        #    「기존 처방을 그대로 둔다」로 HELD한 **근거 자체가 사라진** 상태다.
        #    ⛔ 사람이 이미 사유에 「무효화」를 적었으면 확인이 끝난 것이므로 억제한다 —
        #       그렇지 않으면 회차마다 같은 4행이 떠서 신호가 죽는다.
        if (d["player_id"] in voided and d["applied_status"] in ("HELD", "APPLIED")
                and "무효화" not in note):
            review["근거가 무효화됐다"].append((d["id"], d["nm"], d["applied_status"]))
        found = {x for x in roles if x in (d["imp"] or "")}
        if not found or not mine:
            continue                      # 역할 코드가 없으면 층 판단이라 역할 대조로는 재검증할 수 없다
        hit = {x for x in found if canon(x) in {canon(y) for y in mine}}
        # ⛔⛔ **억제 토큰 — 2026-09-20 신설(obs#888).** 이 부류에는 억제 경로가 **아예 없어서**
        #    조건이 충족되지 않은 행이 회차마다 그대로 다시 떴다(알리송 #31은 09-17에 이미 오탐으로
        #    판정했는데 09-20에 또 올라왔다). obs#786이 경고한 「같은 행이 회차마다 떠서 신호가 죽는다」가
        #    「근거가 무효화됐다」 부류에만 막혀 있었던 것이다. ⇒ 사람이 사유에 **「조건 미충족」**을 적으면 억제한다.
        #    ⭐ 억제는 판정이 아니라 **확인이 끝났다는 표시**다 — 조건이 실제로 충족되면 사람이 토큰을 지운다.
        if hit and "조건 미충족" in note:
            suppressed.append((d["id"], d["nm"]))
            hit = set()
        if hit and d["applied_status"] in ("HELD", "REJECTED"):
            # ⭐ **근거의 출처를 함께 보고한다**(2026-09-20 신설). `have`에는 시즌 처방·**경기 전용 프리셋**·
            #    `squad_entries.fit_role`이 섞여 있는데, 재판정 조건은 대개 **시즌 표본**을 말한다.
            #    ⛔ 경기 전용(`match_player_prescriptions`)은 고정 작업 규칙 5에 따라 시즌 정본에 병합되지 않으므로
            #       그것만으로 「닿았다」고 읽으면 **층이 다른 근거로 시즌 조건을 닫는 것**이 된다(알리송 #31 실측 사례).
            src = []
            if {canon(y) for y in season_role.get(d["player_id"], set())} & {canon(x) for x in hit}:
                src.append("시즌처방")
            if {canon(y) for y in match_role.get(d["player_id"], set())} & {canon(x) for x in hit}:
                src.append("경기전용")
            if {canon(y) for y in fit_role.get(d["player_id"], set())} & {canon(x) for x in hit}:
                src.append("fit_role")
            review["닿았을 수 있다"].append(
                (d["id"], d["nm"], d["applied_status"], sorted(hit), "+".join(src) or "?"))
        elif not hit and d["applied_status"] == "APPLIED":
            review["다시 갈렸다"].append((d["id"], d["nm"], sorted(found), sorted(mine)))
    tot = sum(len(v) for v in review.values())
    print(f"\n⏰ **재판정 조건 충족 후보 {tot}건** (⛔ 사람 판정은 자동으로 바꾸지 않는다 — 보고만)")
    for k, lst in review.items():
        if not lst:
            continue
        print(f"  [{k}] {len(lst)}건")
        for row in lst:
            print("     " + " · ".join(str(x) for x in row))
    if not tot:
        print("  (없음 — 사람 판정이 현재 처방과 정합한다)" if not suppressed
              else "  (신규 없음)")
    # ⭐ 억제분은 **따로 보고한다**(2026-09-20 · obs#888) — 「0건」과 「억제 N건」은 다른 상태다.
    #    합쳐서 「정합」이라 쓰면 다음 세션이 **조건이 충족된 줄로 오해한다**.
    if suppressed:
        print(f"  ⏸ 억제 {len(suppressed)}건 — 사람이 「조건 미충족」으로 확인을 끝낸 행이다(조건이 실제로 충족되면 그 토큰을 지운다):")
        for did, nm in suppressed:
            print(f"     {did} · {nm}")
    print("\n다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
