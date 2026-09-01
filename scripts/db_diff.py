#!/usr/bin/env python3
"""DB 스냅샷 대비 **행 단위** 변경 대조 — 파괴적 정리가 의도한 것만 했는지 증명한다. 읽기 전용.

왜 있는가 (2026-09-01):
  이 날 정리 4연쇄(에수구 병합 · 이중기록 77쌍 · team_code 739행)에서 매번 손으로
  `ATTACH '백업' AS bak; SELECT ... WHERE b.x IS NOT c.x` 를 쳤다.
  특히 ⭐**「새로 NULL 된 행 0」을 증명한 것이 백업 대조뿐**이었다 — 게이트도 FK 검사도
  「값이 조용히 지워졌다」는 잡지 못한다. 그 절차를 스크립트로 굳힌 것이다.
  (CLAUDE.md 고정 작업 규칙 「파괴적 정리 전에는 백업한다」의 짝이다.)

  ⛔ 어느 DB도 수정하지 않는다.

사용:
    python3 scripts/db_diff.py --snapshot                  # 지금 상태를 스냅샷으로 떠 둔다
    python3 scripts/db_diff.py <before.db>                 # 그 스냅샷 대비 전체 대조
    python3 scripts/db_diff.py <before.db> -t player_matches -v
    python3 scripts/db_diff.py <before.db> --only-changed  # 변경 있는 테이블만

읽는 법:
    +N / −N            행 추가 / 삭제
    ~N                 값이 바뀐 행
    ⚠️ null화 N        NOT NULL → NULL 로 바뀐 칸 수 (**의도치 않은 정보 손실 신호**)
종료 코드는 항상 0이다 — 이 스크립트는 판정이 아니라 **보고**다. 판단은 사람이 한다.
"""
import argparse
import shutil
import sqlite3
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB   # noqa: E402

SNAP_DIR = ROOT / "db" / ".snapshots"


def tables(con):
    return [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%' ORDER BY name")]


def cols_and_pk(con, t):
    info = con.execute(f"PRAGMA table_info({t})").fetchall()
    cols = [r[1] for r in info]
    pk = [r[1] for r in sorted((r for r in info if r[5] > 0), key=lambda r: r[5])]
    return cols, pk


def load(con, t, cols, pk):
    """PK → {컬럼: 값} 사전. PK가 없으면 None(대조 불가)."""
    if not pk:
        return None
    q = f"SELECT {', '.join(cols)} FROM {t}"
    out = {}
    for row in con.execute(q):
        d = dict(zip(cols, row))
        out[tuple(d[c] for c in pk)] = d
    return out


def diff_table(before, after, t, verbose, limit):
    bcols, bpk = cols_and_pk(before, t)
    acols, apk = cols_and_pk(after, t)
    if bcols != acols:
        return {"schema_changed": True,
                "added_cols": [c for c in acols if c not in bcols],
                "dropped_cols": [c for c in bcols if c not in acols]}
    if not bpk:
        nb = before.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        na = after.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        return {"no_pk": True, "count": (nb, na)}

    b = load(before, t, bcols, bpk)
    a = load(after, t, acols, apk)
    added = [k for k in a if k not in b]
    removed = [k for k in b if k not in a]
    changed, nulled, col_changes = [], [], Counter()
    for k in a:
        if k not in b:
            continue
        bv, av = b[k], a[k]
        diffs = [c for c in bcols if bv[c] != av[c]]
        if not diffs:
            continue
        changed.append(k)
        for c in diffs:
            col_changes[c] += 1
            # ⭐ NOT NULL → NULL 은 「덮어쓰기」가 아니라 「지워짐」이다. 따로 센다.
            if bv[c] is not None and av[c] is None:
                nulled.append((k, c))
    return {"added": added, "removed": removed, "changed": changed,
            "nulled": nulled, "col_changes": col_changes,
            "pk": bpk, "limit": limit, "verbose": verbose}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("before", nargs="?", help="비교 기준 스냅샷 DB 경로")
    ap.add_argument("--db", default=str(DB), help="현재 DB (기본: db/tactics.db)")
    ap.add_argument("-t", "--table", help="이 테이블만")
    ap.add_argument("-v", "--verbose", action="store_true", help="바뀐 PK를 나열")
    ap.add_argument("--limit", type=int, default=8, help="나열 개수 상한 (기본 8)")
    ap.add_argument("--only-changed", action="store_true", help="변경 있는 테이블만 출력")
    ap.add_argument("--snapshot", action="store_true",
                    help="현재 DB를 db/.snapshots/ 에 떠 두고 경로를 출력한다")
    a = ap.parse_args()

    if a.snapshot:
        SNAP_DIR.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(a.db)
        # ⚠️ 파일명에 시각을 쓰지 않는다 — 세션마다 시계가 다르고 비교가 어렵다.
        #    대신 「가장 최근 관측 id」로 이름을 붙여 어느 시점인지 DB 스스로 말하게 한다.
        try:
            obs = con.execute("SELECT MAX(id) FROM observations").fetchone()[0]
        except sqlite3.Error:
            obs = "x"
        finally:
            con.close()
        dst = SNAP_DIR / f"tactics-obs{obs}.db"
        n = 1
        while dst.exists():
            dst = SNAP_DIR / f"tactics-obs{obs}-{n}.db"
            n += 1
        shutil.copy(a.db, dst)
        print(f"📸 스냅샷: {dst}")
        print(f"   대조:   python3 scripts/db_diff.py {dst}")
        return 0

    if not a.before:
        ap.error("비교할 스냅샷 경로가 필요하다 (먼저 --snapshot 으로 떠 둘 것)")
    bp, dp = Path(a.before), Path(a.db)
    for p in (bp, dp):
        if not p.exists():
            sys.exit(f"⛔ DB 없음: {p}")

    before, after = sqlite3.connect(bp), sqlite3.connect(dp)
    tb, ta = set(tables(before)), set(tables(after))
    print(f"기준 {bp.name}  →  현재 {dp.name}")
    for t in sorted(ta - tb):
        print(f"  ⭐ 테이블 신설: {t}")
    for t in sorted(tb - ta):
        print(f"  ⚠️ 테이블 삭제: {t}")

    targets = [a.table] if a.table else sorted(tb & ta)
    total_null = 0
    for t in targets:
        if t not in tb or t not in ta:
            print(f"  ⚠️ {t}: 한쪽에만 있다 — 건너뜀")
            continue
        r = diff_table(before, after, t, a.verbose, a.limit)
        if r.get("schema_changed"):
            print(f"  ⭐ {t}: 스키마 변경 — 추가 {r['added_cols']} / 삭제 {r['dropped_cols']}")
            continue
        if r.get("no_pk"):
            nb, na = r["count"]
            if nb != na or not a.only_changed:
                print(f"  ⚠️ {t}: PK 없어 행 대조 불가 — 행 수만 {nb} → {na}")
            continue
        na, nr, nc, nn = len(r["added"]), len(r["removed"]), len(r["changed"]), len(r["nulled"])
        if a.only_changed and not (na or nr or nc):
            continue
        if not (na or nr or nc):
            print(f"     {t}: 변동 없음")
            continue
        total_null += nn
        parts = []
        if na:
            parts.append(f"+{na}")
        if nr:
            parts.append(f"−{nr}")
        if nc:
            parts.append(f"~{nc}")
        line = f"  ● {t}: " + " ".join(parts)
        if nn:
            line += f"   ⚠️ null화 {nn}"
        print(line)
        if nc:
            top = ", ".join(f"{c} {n}" for c, n in r["col_changes"].most_common(6))
            print(f"       바뀐 칸: {top}")
        if nn:
            ex = ", ".join(f"pk={k} · {c}" for k, c in r["nulled"][:a.limit])
            print(f"       ⚠️ NOT NULL → NULL: {ex}"
                  + (" …" if nn > a.limit else ""))
        if a.verbose:
            for label, keys in (("추가", r["added"]), ("삭제", r["removed"]), ("변경", r["changed"])):
                if keys:
                    shown = ", ".join(str(k) for k in keys[:a.limit])
                    print(f"       {label} pk({','.join(r['pk'])}): {shown}"
                          + (" …" if len(keys) > a.limit else ""))
    before.close()
    after.close()

    print()
    if total_null:
        print(f"⚠️⚠️ NOT NULL → NULL 총 {total_null}칸 — **의도한 것인지 확인할 것**. "
              "값이 조용히 지워지는 것은 게이트도 FK 검사도 잡지 못한다.")
    else:
        print("✅ NOT NULL → NULL 0칸 — 값이 조용히 지워진 곳은 없다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
