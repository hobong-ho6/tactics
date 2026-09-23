#!/usr/bin/env python3
"""불변규칙 5의 고정 절차를 **한 번에** 실행한다 — 게이트 → export → dump → 명시 스테이징 → 커밋.

왜 (2026-09-23 사용자 지시 「코드나 스크립트로 대체 — 유지보수 편의와 동일한 결과, 토큰 절감」):
  CLAUDE.md 불변규칙 5(`export → dump → 함께 커밋`)는 **10개 문서에 흩어져** 있고, 매 회차 세션이
  손으로 4~5번 왕복한다. 왕복마다 그 시점의 대화 전체가 다시 입력으로 들어간다(club-sync 런북의 비용 모델).
  더 나쁜 것은 **순서·스테이징을 틀리면 사고가 난다**는 점이다 — 아래 방어가 전부 실제 사고에서 왔다.

⛔⛔ 이 스크립트가 막는 것(전부 docs/70의 실증):
  ⑴ **`git add -A`** — `.claude/settings.json`(Figma PAT)이 있어 푸시가 차단된다. 여기선 경로를 명시해야만 담긴다.
  ⑵ **남이 올려둔 인덱스와 함께 커밋** — 2026-09-21에 스케줄 세션이 인덱스에 되돌린 버전을 올려 둔 상태에서
     다른 파일만 add하고 커밋해 **직전 커밋의 규칙 43줄이 함께 지워졌다.** `git add <경로>`는 남의 것을 빼주지 않는다.
     ⇒ 시작할 때 인덱스가 비어 있지 않으면 **중단한다**(`--force-index`로만 강행).
  ⑶ **게이트를 건너뛴 export** — `scripts/export.py`가 자체 강제하지만, 실패 원인을 먼저 보여주고 멈춘다.
  ⑷ **dump 누락** — `.db`만 커밋하면 리뷰 불가능한 바이너리 변경만 남는다.

사용:
    python3 scripts/ship.py -m "data(fut): GG Club 싱크 2026-09-23 — 신규 1·갱신 1"
    python3 scripts/ship.py -F /tmp/msg.txt reports/match-watch/ docs/70-lessons.md
    python3 scripts/ship.py -m "…" --no-push        # 커밋만
    python3 scripts/ship.py --check                 # 게이트·export·dump만 (커밋 안 함)
⚠️ 코드만 고쳤고 DB를 안 건드렸어도 그대로 쓰면 된다 — export는 멱등이라 diff가 0이면 담기지 않는다.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# DB를 건드렸든 아니든 **늘 함께 가는 3종**(불변규칙 5). 변경이 없으면 git이 알아서 무시한다.
ALWAYS = ["db/tactics.db", "db/dump/", "site/data/"]
# ⛔ 이름만 스쳐도 담지 않는다 — .gitignore가 있어도 사람이 -f로 넣는 사고를 막는 2중 방어다.
FORBIDDEN = (".claude/settings.json", ".claude/settings.local.json", ".env")


def sh(cmd, **kw):
    return subprocess.run(cmd, shell=isinstance(cmd, str), cwd=ROOT, text=True,
                          capture_output=True, **kw)


def step(label, cmd):
    print(f"▶ {label}")
    r = sh(cmd)
    out = (r.stdout + r.stderr).strip()
    tail = "\n".join(out.split("\n")[-3:])
    if tail:
        print("   " + tail.replace("\n", "\n   "))
    if r.returncode:
        sys.exit(f"⛔ {label} 실패 — 여기서 멈춘다. 원인을 고치고 다시 실행할 것.")
    return out


def main(a):
    # ⑵ 인덱스 오염 검사 — **가장 먼저** 한다. 이걸 놓치면 남의 변경을 내 커밋에 싣는다.
    staged = [l for l in sh("git diff --cached --name-only").stdout.split("\n") if l.strip()]
    if staged and not a.force_index:
        print("⛔ 인덱스에 이미 올라온 파일이 있다 — 다른 세션이 스테이징했을 수 있다:")
        for f in staged[:20]:
            print("   ", f)
        sys.exit("   내가 올린 것이 맞으면 --force-index, 아니면 `git restore --staged <파일>`로 빼고 다시 실행할 것.\n"
                 "   ⚠️ 2026-09-21에 이걸 지나쳐 직전 커밋의 43줄이 지워졌다(docs/70).")

    step("게이트", "python3 scripts/gates.py")
    step("export", "python3 scripts/export.py")
    step("db dump", "scripts/db_dump.sh")
    if a.check:
        print("✅ 검사만 수행(--check) — 커밋하지 않았다.")
        return 0

    paths = ALWAYS + list(a.paths)
    for p in paths:
        if any(f in p for f in FORBIDDEN):
            sys.exit(f"⛔ 커밋 금지 파일이 경로에 들어 있다: {p}")
    sh(["git", "add", "--"] + paths)

    names = [l for l in sh("git diff --cached --name-only").stdout.split("\n") if l.strip()]
    if not names:
        print("변경 없음 — 커밋할 것이 없다.")
        return 0
    for n in names:
        if any(f in n for f in FORBIDDEN):
            sys.exit(f"⛔ 커밋 금지 파일이 스테이징됐다: {n} — `git restore --staged`로 빼고 다시 실행할 것.")
    print("▶ 스테이징 (⛔ git add -A 아님 · 아래가 전부여야 한다)")
    print("   " + sh("git diff --cached --stat").stdout.strip().replace("\n", "\n   "))

    # ⚠️ 커밋 메시지는 **파일로** 넘긴다 — 백틱이 든 메시지를 -m으로 주면 셸이 명령 치환을 한다(2026-09-22 실증).
    if a.message:
        msg = ROOT / ".git" / "SHIP_MSG"
        msg.write_text(a.message + "\n", encoding="utf-8")
        mf = str(msg)
    else:
        mf = a.file
    r = sh(["git", "commit", "-q", "-F", mf])
    if r.returncode:
        sys.exit("⛔ 커밋 실패:\n" + (r.stdout + r.stderr))
    print("▶ 커밋", sh("git log --oneline -1").stdout.strip())
    if a.push:
        r = sh("git push -q")
        if r.returncode:
            sys.exit("⛔ 푸시 실패 — 커밋은 남아 있다:\n" + (r.stdout + r.stderr))
        print("▶ 푸시 완료")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", help="추가로 담을 경로(명시 스테이징). db/site 3종은 자동으로 담긴다.")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("-m", "--message", help="커밋 메시지. ⚠️ 백틱이 많으면 -F를 쓸 것")
    g.add_argument("-F", "--file", help="커밋 메시지 파일")
    ap.add_argument("--no-push", dest="push", action="store_false", help="커밋만 하고 푸시하지 않는다")
    ap.add_argument("--force-index", action="store_true", help="이미 스테이징된 파일이 있어도 진행(내가 올린 게 확실할 때만)")
    ap.add_argument("--check", action="store_true", help="게이트·export·dump만 돌리고 끝낸다")
    a = ap.parse_args()
    if not a.check and not (a.message or a.file):
        ap.error("-m 또는 -F 가 필요하다 (--check 는 예외)")
    sys.exit(main(a))
