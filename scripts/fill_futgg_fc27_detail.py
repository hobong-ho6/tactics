#!/usr/bin/env python3
"""FC27 09-10 스냅샷의 **빈 칸만** 채운다 — fut.gg 아이템 정의 API(채움 전용).

왜 (2026-09-14 신설):
  09-10·09-11 수집은 클럽 페이지/벌크 목록 경로라 **주발 0/131 · 나이 0/131**이고 attrs 15명·
  AcceleRATE 28명·키 11명·몸무게 16명이 비어 있었다. `/api/fut/player-item-definitions/27/{eaId}/`는
  한 응답에 주발·생년월일·34속성·PlayStyles(+)·AcceleRATE·키·몸무게·포지션이 전부 있고 **curl 200**이다
  (collect_futgg_history.py가 FC25·FC26에 쓰는 그 경로 — 같은 소스라 provenance가 섞이지 않는다).

⛔ **값을 덮어쓰지 않는다**(불변규칙 2). NULL/빈 문자열만 채우고, 기존 값과 API 값이 다르면
   **적재하지 않고 충돌로 보고**한다(사람이 판정). playstyles의 빈 문자열은 「EA 0종」과 「미수집」이
   구분되지 않아 함께 채움 대상으로 본다 — 실제 0종이면 API도 0종이므로 그대로 빈 칸으로 남는다.

⚠️ 동일성: `gender==1` + 이름 토큰 교차(09-10 수집이 리스 제임스에 로렌 제임스 카드를 붙인 이력).

사용:
    .venv/bin/python scripts/fill_futgg_fc27_detail.py --dry-run
    .venv/bin/python scripts/fill_futgg_fc27_detail.py
"""
import argparse
import datetime as dt
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DB = ROOT / "db" / "tactics.db"

from scripts.collect_futgg_history import (  # noqa: E402  같은 소스·같은 매핑을 재사용한다
    API, ATTR_MAP, FOOT, GK_ATTRS, OUTFIELD_DROP, POS, accelerate_label, get, norm,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roster-date", default="2026-09-10")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    playstyle = {x["eaId"]: x["name"] for x in get(f"{API}/playstyles/")["data"]}

    rows = con.execute("""SELECT g.id, g.player_id, g.name_kr, g.positions, g.best_pos, g.age, g.height_cm,
                                 g.weight_kg, g.attrs, g.playstyles, g.accelerate, g.preferred_foot,
                                 g.card_image_url, g.source, p.name
                          FROM player_game_stats g LEFT JOIN players p ON p.id=g.player_id
                          WHERE g.game_version='FC27' AND g.roster_date=?""", (a.roster_date,)).fetchall()
    print(f"대상 {len(rows)}행 (FC27 {a.roster_date})")

    # ⚠️ 같은 eaId가 두 행에 붙어 있으면 한쪽이 남의 카드다(09-10 수집에서 다트로↔웨슬리 포파나 실제 발생).
    #    이름 토큰 교차는 성(姓)이 같으면 통과하므로 **eaId 중복 자체를 먼저 막는다.**
    dup_ea = {}
    for r in rows:
        m = re.search(r"/27-(\d+)\.", r["card_image_url"] or "")
        if m:
            dup_ea.setdefault(int(m.group(1)), []).append(r["name_kr"])
    dup_ea = {k: v for k, v in dup_ea.items() if len(v) > 1}

    cur = con.cursor()
    filled, conflicts, missing, mismatch, roles_seen = 0, [], [], [], 0
    counts = {}
    for r in rows:
        m = re.search(r"/27-(\d+)\.", r["card_image_url"] or "")
        if not m:
            missing.append((r["name_kr"], "eaId 없음"))
            continue
        ea = int(m.group(1))
        if ea in dup_ea:
            missing.append((r["name_kr"], f"eaId {ea} 중복({'·'.join(dup_ea[ea])}) — 카드 오염 의심, 건드리지 않음"))
            continue
        d = get(f"{API}/player-item-definitions/27/{ea}/")
        d = d.get("data", d) if isinstance(d, dict) else None
        if not d:
            missing.append((r["name_kr"], f"API 404 (ea {ea})"))
            continue
        nm = " ".join(filter(None, [d.get("commonName"), d.get("firstName"), d.get("lastName")]))
        if d.get("gender") != 1 or not (norm(r["name"] or r["name_kr"]) & norm(nm)):
            mismatch.append((r["name_kr"], ea, d.get("commonName"), d.get("gender")))
            continue
        if d.get("rolesPlus") or d.get("rolesPlusPlus"):
            roles_seen += 1

        gk = d.get("position") == 0
        attrs = {ATTR_MAP[k]: d[k] for k in ATTR_MAP if d.get(k) is not None}
        attrs = {k: v for k, v in attrs.items() if (k in GK_ATTRS if gk else k not in OUTFIELD_DROP)}
        ps = [playstyle.get(i, f"PS#{i}") for i in d.get("playstyles") or []] + \
             [playstyle.get(i, f"PS#{i}") + "+" for i in d.get("playstylesPlus") or []]
        positions = "/".join([POS.get(d.get("position"), str(d.get("position")))] +
                             [POS.get(i, str(i)) for i in d.get("alternativePositionIds") or []])
        age = None
        if d.get("dateOfBirth"):
            b = dt.date.fromisoformat(d["dateOfBirth"]); ref = dt.date.fromisoformat(a.roster_date)
            age = ref.year - b.year - ((ref.month, ref.day) < (b.month, b.day))

        new = {
            "preferred_foot": FOOT.get(d.get("foot")),
            "age": age,
            "height_cm": d.get("height"),
            "weight_kg": d.get("weight"),
            "accelerate": accelerate_label(d.get("accelerateType")),
            "attrs": json.dumps(attrs, ensure_ascii=False) if attrs else None,
            "playstyles": ", ".join(ps) or None,
            "positions": positions or None,
            "best_pos": (positions.split("/")[0] if positions else None),
        }
        upd, extended = {}, []
        for k, v in new.items():
            old = r[k]
            blank = old is None or (isinstance(old, str) and not old.strip())
            if v is None:
                continue
            if blank:
                upd[k] = v
            elif k == "positions" and str(old).strip() == v.split("/")[0]:
                # 클럽 페이지 경로는 주 포지션 하나만 준다. 대체 포지션을 **뒤에 덧붙이는** 확장이라
                # 기존 값(주 포지션)은 그대로 보존된다 — 덮어쓰기가 아니다(G14 prefix 보존과 같은 형태).
                upd[k] = v
                extended.append(f"{old}→{v}")
            elif k == "playstyles" and {x.strip() for x in str(old).split(",")} == {x.strip() for x in v.split(",")}:
                pass          # 같은 집합, 순서만 다름 — 건드리지 않는다
            elif k in ("attrs",):
                # 속성은 부분집합 비교 — 기존 키의 값이 다르면 충돌로 본다
                try:
                    o = json.loads(old)
                except Exception:
                    conflicts.append((r["name_kr"], k, old, v)); continue
                diff = {kk: (o[kk], attrs[kk]) for kk in o if kk in attrs and o[kk] != attrs[kk]}
                if diff:
                    conflicts.append((r["name_kr"], k, json.dumps(diff, ensure_ascii=False)[:200], ""))
            elif str(old).strip() != str(v).strip():
                conflicts.append((r["name_kr"], k, old, v))
        if not upd:
            continue
        for k in upd:
            counts[k] = counts.get(k, 0) + 1
        filled += 1
        src = (r["source"] or "") + (
            (f" · 포지션 확장 {'/'.join(extended)}" if extended else "") +
            f" · [{a.pulled}] 빈 칸 채움({', '.join(sorted(upd))}) "
            f"fut.gg /api/fut/player-item-definitions/27/{ea}/ (fill_futgg_fc27_detail.py, 덮어쓰기 없음)")
        if a.dry_run:
            print(f"  {r['name_kr']:<14} ← {', '.join(f'{k}={str(upd[k])[:28]}' for k in sorted(upd))}")
        else:
            sets = ", ".join(f"{k}=:{k}" for k in upd)
            cur.execute(f"UPDATE player_game_stats SET {sets}, source=:source WHERE id=:id",
                        {**upd, "source": src, "id": r["id"]})
    if not a.dry_run:
        con.commit()

    print(f"\n채운 행 {filled} · 컬럼별 {counts}")
    print(f"역할 숙련(rolesPlus/++) 응답 보유 {roles_seen}명 — 0이면 09-18 얼리액세스 전까지 EA 미공개(docs/21)")
    if missing:
        print(f"⚠️ 결손 {len(missing)}건: " + ", ".join(f"{n}({w})" for n, w in missing))
    if mismatch:
        print("⛔ 동일성 불일치 — 건드리지 않음:")
        for x in mismatch:
            print("   ", x)
    if conflicts:
        print(f"⛔ 기존 값 충돌 {len(conflicts)}건 — 덮어쓰지 않음(사람이 판정):")
        for x in conflicts:
            print("   ", x)
    print("\n다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
