"""역할 근거(커뮤니티 체감) 적재 — 조사 JSON → game_role_evidence (migration 104).

    python3 scripts/load_role_evidence.py FILE[:SLOT] … [--source "<조사 회차>"] [--dry-run]

FILE은 {"items": [{role, slot?, focus?, claim_kr, quote_orig, quote_kr, lang, source_url, source_name,
game_version, date, grade, snippet_only, contradicts_ea, notes}]} 꼴이다. ':SLOT'은 slot이 빈 항목의 기본값.
⛔ 이름으로 잇는 유일한 자리다 — EA 역할명 + 슬롯군 → role_id 표(ROLE)가 정본이다. 표에 없거나
   포커스가 그 역할에 없으면 **적재하지 않고 보고**한다(추측해 잇지 않는다).
⛔ 이미 있는 행(같은 role·focus·URL·인용)은 건너뛴다(불변규칙 2).
"""
import argparse
import datetime as dt
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "tactics.db"

SLOT = {"ST": "ST", "CF": "ST", "CAM": "CAM", "AM": "CAM", "W": "W", "LW": "W", "RW": "W",
        "WM": "WM", "LM": "WM", "RM": "WM", "CM": "CM", "CDM": "DM", "DM": "DM",
        "FB": "FB", "LB": "FB", "RB": "FB", "LWB": "FB", "RWB": "FB", "CB": "CB", "GK": "GK"}
ROLE = {
    ("ST", "advanced forward"): "st_advanced", ("ST", "poacher"): "st_poacher",
    ("ST", "target forward"): "st_target", ("ST", "false 9"): "st_false9", ("ST", "false nine"): "st_false9",
    ("CAM", "classic 10"): "cam_classic10", ("CAM", "shadow striker"): "cam_shadow",
    ("CAM", "playmaker"): "cam_playmaker", ("CAM", "half winger"): "cam_halfwinger", ("CAM", "half-winger"): "cam_halfwinger",
    ("W", "winger"): "w_winger", ("W", "inside forward"): "w_insidefwd", ("W", "wide playmaker"): "w_wideplm",
    ("WM", "winger"): "wm_winger", ("WM", "inside forward"): "wm_insidefwd", ("WM", "wide playmaker"): "wm_wideplm",
    ("WM", "wide midfielder"): "wm_widemid",
    ("CM", "box-to-box"): "cm_b2b", ("CM", "box to box"): "cm_b2b", ("CM", "deep-lying playmaker"): "cm_dlp",
    ("CM", "half winger"): "cm_halfwinger", ("CM", "half-winger"): "cm_halfwinger", ("CM", "holding"): "cm_holding",
    ("CM", "playmaker"): "cm_playmaker",
    ("DM", "box crasher"): "dm_boxcrasher", ("DM", "centre-half"): "dm_centrehalf", ("DM", "centre half"): "dm_centrehalf",
    ("DM", "center half"): "dm_centrehalf", ("DM", "deep-lying playmaker"): "dm_dlp", ("DM", "holding"): "dm_holding",
    ("DM", "wide half"): "dm_widehalf",
    ("FB", "fullback"): "fb_fullback", ("FB", "full-back"): "fb_fullback", ("FB", "wingback"): "fb_wingback",
    ("FB", "attacking wingback"): "fb_att_wb", ("FB", "falseback"): "fb_falseback", ("FB", "false back"): "fb_falseback",
    ("FB", "inverted wingback"): "fb_inverted",
    ("CB", "defender"): "cb_defender", ("CB", "ball-playing defender"): "cb_bpd", ("CB", "stopper"): "cb_stopper",
    ("CB", "wideback"): "cb_wideback", ("CB", "wide back"): "cb_wideback",
    ("GK", "goalkeeper"): "gk_goalkeeper", ("GK", "sweeper keeper"): "gk_sweeper", ("GK", "ball-playing keeper"): "gk_ballplaying",
}
# 슬롯 없이 이름만으로 정해지는 역할(이름이 한 군에만 있다)
UNIQUE = {}
for (s, n), rid in ROLE.items():
    UNIQUE.setdefault(n, set()).add(rid)


def slots_of(raw, default):
    raw = (raw or default or "").upper().replace(" ", "")
    out = []
    for part in raw.replace("/", ",").replace("+", ",").split(","):
        if part in SLOT and SLOT[part] not in out:
            out.append(SLOT[part])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--source", default="역할 커뮤니티 조사 2026-10-10 (다국어 웹 검색 · 서브에이전트 4갈래)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    con = sqlite3.connect(DB)
    foci = {}
    for rid, f in con.execute("SELECT role_id, focus FROM game_role_focus WHERE game_version='FC26'"):
        foci.setdefault(rid, set()).add(f)
    today = dt.date.today().isoformat()
    ins = dup = 0
    skipped = []
    for spec in a.files:
        path, _, default = spec.partition(":")
        for it in json.loads(Path(path).read_text()).get("items", []):
            # 「A / B」처럼 역할을 **명시해 나열**한 항목은 각 역할에 싣는다(추측이 아니라 원 항목이 둘 다 지목했다).
            slots = slots_of(it.get("slot"), default)
            rids = []
            for name in [x.strip().lower() for x in (it.get("role") or "").split(" / ")]:
                hit = [ROLE[(s, name)] for s in slots if (s, name) in ROLE]
                if not hit and len(UNIQUE.get(name, ())) == 1:
                    hit = list(UNIQUE[name])
                if not hit:
                    rids = []
                    break
                rids += [h for h in hit if h not in rids]
            if not rids:
                skipped.append(f"역할 미확정: {it.get('role')} / slot={it.get('slot')} ({path})")
                continue
            if not it.get("source_url") or not it.get("claim_kr") or it.get("grade") not in ("C", "D"):
                skipped.append(f"필수값 결손: {it.get('role')} {it.get('source_url')}")
                continue
            # ⛔ 원문 없는 번역은 싣지 않는다(불변규칙 11 — 검증 불가). 요약(claim_kr)과 출처만 남긴다.
            if not it.get("quote_orig") and it.get("quote_kr"):
                it["quote_kr"] = None
                it["notes"] = "[원문 미확보 — 번역 인용 제거] " + (it.get("notes") or "")
            for rid in rids:
                focus = it.get("focus") or None
                note = it.get("notes") or ""
                if focus and focus not in foci.get(rid, ()):
                    note = f"[포커스 「{focus}」는 이 역할에 없어 역할 전체로 적재] " + note
                    focus = None
                cur = con.execute("""INSERT OR IGNORE INTO game_role_evidence
                    (role_id, focus, claim_kr, quote_orig, quote_kr, lang, source_name, source_url, observed_gv,
                     observed_date, grade, snippet_only, contradicts_ea, notes, collected, source)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (rid, focus, it["claim_kr"], it.get("quote_orig"), it.get("quote_kr"), it.get("lang"),
                     it.get("source_name"), it["source_url"], it.get("game_version"), it.get("date"),
                     it["grade"], int(bool(it.get("snippet_only"))), int(bool(it.get("contradicts_ea"))),
                     note or None, today, a.source))
                ins += cur.rowcount
                dup += 1 - cur.rowcount
    print(f"적재 {ins}행 · 중복 건너뜀 {dup} · 보류 {len(skipped)}")
    for s in skipped:
        print("  ⚠️", s)
    if a.dry_run:
        con.rollback()
        print("(dry-run — 쓰지 않았다)")
    else:
        con.commit()


if __name__ == "__main__":
    main()
