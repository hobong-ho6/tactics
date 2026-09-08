#!/usr/bin/env python3
"""G14 후보 「원장 정정 규약」 — 프로토타입(게이트 미편입).

⚠️ 아직 scripts/gates.py에 넣지 않았다. 게이트에 넣으면 이후 모든 DB 쓰기가 여기서 막히므로
   사용자 승인 후 편입한다. 편입 방법은 이 파일 맨 아래 「편입 절차」 참조.

배경 — 2026-09-08에 obs#503이 **제자리에서 덮어써졌다**(불변규칙 2 위반, 커밋 1211c43).
그 덮어쓰기가 파생 결함 2건을 함께 만들었고(텍스트 중복 · claim↔evidence 모순),
**G1~G13 전항 통과 상태에서 발생했다** — 기존 게이트는 전부 구조·수치 층이고
「행 내부 자연어」와 「행의 편집 이력」은 검사 대상이 아니다(obs#517).

G14가 담당하는 것은 **그 두 사각지대만**이다. G13이 「FK가 성립해서 G6가 원리적으로 못 잡는
부류」만 모은 것과 같은 원칙이다.

  ⑴ append_rewrite   원장 테이블의 기존 행 텍스트가 **prefix를 보존하지 않고 재작성**됐다.
  ⑵ dup_phrase       한 필드 안에서 **한글 명사구가 인접 반복**됐다(편집 사고의 지문).
  ⑶ claim_evid_clash 같은 행의 claim과 evidence가 **공유 명사구 뒤에서 극성이 반대**다.

⭐ 불변식을 「변경 금지」가 아니라 **「prefix 보존(덧붙임만)」**으로 잡은 것이 핵심이다.
   git 히스토리 실측(2026-09-08): observations는 정당한 **덧붙임 21건** 대비 재작성이
   **8필드(2커밋)**뿐이었다. 즉 이 저장소의 실제 규약은 「행을 늘리는 것은 정상, 고쳐 쓰는 것은 사고」다.
   「변경 금지」로 잡으면 그 21건이 전부 오탐이 된다.

⛔ 대상 테이블을 좁힌 근거(같은 실측):
   observations   재작성 8 / 커밋 160  → **강한 규약. 대상.**
   player_duties  덧붙임 375 · 재작성 207(대부분 v1 i18n·스키마 이관) → **대상(전방 검사만).**
   transfer_targets  69커밋 중 66이 편집 → 등급 갱신이 정상 작업. **대상 아님.**
   prescriptions / match_reports → fit 재산출·draft→complete가 정상. **대상 아님.**

사용:
    .venv/bin/python scripts/g14_prototype.py              # 현재 상태 검사
    .venv/bin/python scripts/g14_prototype.py --backtest 40 # 최근 40커밋 역검증
"""
import argparse
import difflib
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 테이블 → prefix 보존을 요구하는 텍스트 필드
PROTECTED = {
    "observations": ["claim", "evidence", "source", "confidence"],
    "player_duties": ["duties", "execution", "adherence", "game_role_implication",
                      "source", "confidence", "sample_note"],
}

# ⑵⑶ 자연어 검사는 observations에만 적용한다(claim/evidence 쌍 구조가 있는 유일한 테이블).
NEG = re.compile(r"(없다|없었다|없음|아니다|불가|0건|0장|0회|부재)")
POS = re.compile(r"(있다|있었다|가용|가능|1장|1건|뿐이다|존재한다)")
HAN = re.compile(r"[가-힣]")


def _sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=ROOT)
    return r.stdout


def baseline(commit="HEAD"):
    """`commit` 시점 dump를 메모리 DB로 적재한다 — 이것이 「직전 정본」이다.

    ⭐ dump 텍스트를 직접 비교하지 않고 sqlite에 태워 필드로 비교한다.
       .dump가 특수문자 행을 unistr(...)로 직렬화하므로 텍스트 대조는 형식 차이로 오탐이 난다.
    """
    schema = _sh(f"git show {commit}:db/dump/schema.sql")
    if not schema.strip():
        return None
    con = sqlite3.connect(":memory:")
    con.executescript(schema)
    for table in PROTECTED:
        data = _sh(f"git show {commit}:db/dump/{table}.sql")
        if data.strip():
            con.executescript(data)
    return con


def strip_noise(t):
    """수사적 반복이 정당한 구역을 제거한다 — 이 필터가 ⑵의 오탐 0을 만든다.

    「」 안은 verbatim 인용이라 「Duro, duro, duro」·「혹독하고 혹독하고」 같은 반복이 정상이다.
    코드·URL·마크다운 표 문법도 반복 패턴을 정상적으로 갖는다.
    """
    t = re.sub(r"「[^」]*」", " ", t)
    t = re.sub(r"`[^`]*`", " ", t)
    t = re.sub(r"https?://\S+|\S+\.(?:com|eus|es|ng|io|md|uk)\S*", " ", t)
    t = re.sub(r"[|\-]{3,}", " ", t)
    return t


def dup_phrase(text):
    """한글 명사구 인접 반복(X + 짧은 연결 + X)."""
    out = []
    for m in re.finditer(r"([가-힣][가-힣 ]{5,25}?)([가-힣]{0,2} ?)\1", strip_noise(text)):
        unit = m.group(1)
        if len(unit.strip()) >= 6:
            out.append(unit.strip())
    return out


def clash(claim, evid, minblk=8, win=14):
    """claim·evidence의 공유 명사구 뒤 극성이 반대인 지점."""
    out = []
    sm = difflib.SequenceMatcher(None, claim, evid, autojunk=False)
    for i, j, n in sm.get_matching_blocks():
        if n < minblk:
            continue
        blk = claim[i:i + n]
        if len(HAN.findall(blk)) < 4:
            continue
        ta, tb = claim[i + n:i + n + win], evid[j + n:j + n + win]
        if (NEG.search(ta) and POS.search(tb)) or (POS.search(ta) and NEG.search(tb)):
            out.append((blk.strip()[-24:], ta.strip(), tb.strip()))
    return out


def g14_checks(con, base):
    """{키: 위반 리스트} — **읽기 전용**. base가 None이면 ⑴을 건너뛴다(첫 커밋 등)."""
    out = {"append_rewrite": [], "dup_phrase": [], "claim_evid_clash": []}

    # ⑴ prefix 비보존 재작성 + 행 삭제
    allow = {s.strip() for s in os.environ.get("G14_ALLOW_REWRITE", "").split(",") if s.strip()}
    if base is not None:
        for table, fields in PROTECTED.items():
            cols = ", ".join(["id"] + fields)
            try:
                old = {r[0]: r[1:] for r in base.execute(f"SELECT {cols} FROM {table}")}
                new = {r[0]: r[1:] for r in con.execute(f"SELECT {cols} FROM {table}")}
            except sqlite3.Error:
                continue
            # ⚠️ 빈 baseline 가드 — 2026-09-08에 실제로 물린 함정이다.
            #    구 커밋은 dump가 data/dump/에 있어 `git show HEAD:db/dump/...`가 빈 문자열을
            #    돌려주고, 그러면 old={}가 되어 **모든 재작성이 조용히 통과**한다(거짓 ✅).
            #    baseline이 비었는데 현재는 행이 있으면 「검사 불가」를 위반으로 올린다.
            if not old and new:
                out["append_rewrite"].append(
                    (table, 0, "(baseline 적재 실패 — 검사 불가)", "", ""))
                continue
            for rid, ovals in old.items():
                key = f"{table}:{rid}"
                if key in allow:
                    continue
                if rid not in new:
                    out["append_rewrite"].append((table, rid, "(행 삭제)", "", ""))
                    continue
                for fld, o, n in zip(fields, ovals, new[rid]):
                    if o == n:
                        continue
                    if o is None:                     # NULL → 값: 결손 채움이므로 허용
                        continue
                    if n is not None and n.startswith(o):
                        continue                      # 덧붙임(prefix 보존) → 정상
                    out["append_rewrite"].append(
                        (table, rid, fld, (o or "")[:60], (n or "")[:60]))

    # ⑵⑶ observations 자연어 층 — ⭐ **델타 검사다**(전수 아님).
    #    전수로 두면 obs#503처럼 「불변규칙 2 때문에 일부러 고치지 않기로 한 행」이 영구 실패를 만든다.
    #    (obs#503의 중복·모순은 obs#517이 정정 기록으로 닫았고, 행 자체는 보존한다 — 재작성 금지.)
    #    ⇒ **HEAD 이후 새로 생기거나 텍스트가 바뀐 행만** 본다. 결함을 「도입 시점」에 잡는 것이 목적이다.
    try:
        rows = con.execute("SELECT id, claim, evidence, source, confidence "
                           "FROM observations").fetchall()
    except sqlite3.Error:
        rows = []
    if base is not None:
        try:
            prev = {r[0]: r[1:] for r in base.execute(
                "SELECT id, claim, evidence, source, confidence FROM observations")}
        except sqlite3.Error:
            prev = {}
        rows = [r for r in rows if prev.get(r[0]) != tuple(r[1:])]
    for rid, c, e, s, cf in rows:
        for fld, txt in (("claim", c), ("evidence", e), ("source", s), ("confidence", cf)):
            if not txt:
                continue
            for unit in dup_phrase(txt):
                out["dup_phrase"].append((rid, fld, unit))
        if c and e:
            for blk, ta, tb in clash(c, e):
                out["claim_evid_clash"].append((rid, blk, ta, tb))
    return out


G14_LABELS = {
    "append_rewrite": "원장재작성",
    "dup_phrase": "구중복",
    "claim_evid_clash": "claim↔evidence모순",
}


def report(res, prefix="G14 원장 정정 규약"):
    bad = {k: v for k, v in res.items() if v}
    parts = " · ".join(f"{G14_LABELS[k]} {len(res[k])}" for k in G14_LABELS)
    print(f"{prefix}: {parts} {'❌' if bad else '✅'}")
    for k, rows in bad.items():
        for r in rows[:6]:
            print(f"    ⛔ {G14_LABELS[k]}: {r}")
        if len(rows) > 6:
            print(f"    … 외 {len(rows) - 6}건")
    return not bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backtest", type=int, metavar="N",
                    help="최근 N커밋에 대해 ⑴을 역검증한다(각 커밋을 그 부모와 대조)")
    a = ap.parse_args()

    if a.backtest:
        commits = _sh(f"git log --format=%h -n {a.backtest}").split()
        print(f"역검증: 최근 {len(commits)}커밋 (⑴ append_rewrite만)\n")
        flagged = 0
        for c in commits:
            cur, par = baseline(c), baseline(c + "^")
            if cur is None or par is None:
                continue
            res = g14_checks(cur, par)
            hits = res["append_rewrite"]
            cur.close(); par.close()
            if hits:
                flagged += 1
                subj = _sh(f"git log -1 --format=%s {c}").strip()[:56]
                print(f"  ❌ {c} 재작성 {len(hits):3d}  {subj}")
                for t, rid, fld, o, n in hits[:3]:
                    print(f"        {t}#{rid}.{fld}")
        print(f"\n적발 커밋 {flagged} / {len(commits)}")
        return 0

    con = sqlite3.connect(ROOT / "db" / "tactics.db")
    base = baseline("HEAD")
    ok = report(g14_checks(con, base))
    con.close()
    if base:
        base.close()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

# ── 편입 절차(승인 후) ────────────────────────────────────────────────────────
# 1. 이 파일의 g14_checks/G14_LABELS/baseline/dup_phrase/clash를 scripts/gates.py로 옮긴다
#    (g13_checks 옆. G13처럼 **검사식을 한 곳에 두고** 회귀 테스트가 import해 공유하게 한다).
# 2. gates.py run()의 G13 보고 다음에 report()와 같은 한 줄을 추가하고 실패 시 종료코드에 반영.
# 3. gates.py 모듈 docstring 게이트 표에 G14 항목 추가 + docs/20 게이트 표 동기화.
# 4. scripts/test_g14_regression.py 신설 — test_g13_regression.py처럼 **결함 3종을 합성 주입**해
#    검사가 실제로 잡는지 본다(재작성 1건·구중복 1건·모순 1건).
# 5. HANDOFF 「회귀」 줄을 G1~G14로 갱신.
