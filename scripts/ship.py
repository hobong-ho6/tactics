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
  ⑷ **dump 누락** — 2026-10-12부터 git에 실리는 DB는 dump뿐이다. dump를 빼면 DB 변경이 통째로 사라진다.
  ⑸ **남이 수집하는 도중의 DB로 게이트·커밋** — 2026-10-19 뉴캐슬전 D+2·주간 매치워치가 쓰는 도중이라 G18이 걸려
     다른 세션이 아무것도 커밋하지 못했다(사용자 「서로 DB를 점유해서 다른 작업을 못 한다」 · 방식 「대기·순번제」).
     ⇒ 다른 세션의 「작성 중」 표시(core/db.py lease)가 사라질 때까지 **기다렸다가** 게이트를 돈다(`--wait`초 · 기본 540).
     ⇒ ship 중에는 `db/.leases/ship.json`을 걸어 **다른 세션의 새 연결이 끝날 때까지 기다리게** 한다(core/db.connect).
     ⇒ 커밋을 마치면 자기 lease를 지운다 — 다음 세션이 곧장 진행한다.

  ⑹ **하위 세션이 각자 커밋** — 2026-10-20 하위 세션 4개가 DB 순번을 기다리며 서로의 변경을 남의 커밋에 실었다
     (클럽 싱크 데이터가 평가 커밋 60b540a에 · 경기 분석 일부가 숨김 커밋 33357be에). 사용자 지시 「모든 하위 세션의 작업이
     완료되면 이 부모 세션에서 모두 모아서 커밋 및 푸시」 ⇒ 부모가 `--collect <하위 세션 id…>`로 등록하면 그 세션들의 ship은
     **거부된다**(--check는 허용). 하위 세션은 「바꾼 파일·DB 변경·커밋 메시지 초안」을 부모에게 보고하고 끝낸다.
     부모는 하위가 모두 끝나면 한 번에 ship하고 `--collect-end`로 표시를 지운다. 등록되지 않은 세션(예약 회차 등)은 영향 없다.

사용:
    python3 scripts/ship.py -m "data(fut): GG Club 싱크 2026-09-23 — 신규 1·갱신 1"
    python3 scripts/ship.py -F /tmp/msg.txt reports/match-watch/ docs/70-lessons.md
    python3 scripts/ship.py -m "…" --no-push        # 커밋만
    python3 scripts/ship.py --check                 # 게이트·export·dump만 (커밋 안 함)
⚠️ 코드만 고쳤고 DB를 안 건드렸어도 그대로 쓰면 된다 — export는 멱등이라 diff가 0이면 담기지 않는다.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import db as coredb  # noqa: E402  ⭐ 작성 중 표시(lease)·ship 표시 정본
# DB를 건드렸든 아니든 **늘 함께 가는 2종**(불변규칙 5). 변경이 없으면 git이 알아서 무시한다.
# ⛔ db/tactics.db는 2026-10-12부터 싣지 않는다 — GitHub 100MB 상한을 두 번 넘었다(10-04 · 10-12).
#    git은 dump만 나르고, 다른 PC는 scripts/db_restore.sh로 DB를 만든다(.gitignore에 있어 add하면 실패한다).
ALWAYS = ["db/dump/", "site/data/"]
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


COLLECT = coredb.LEASE_DIR / "collector.json"   # 부모 세션의 「모아서 커밋」 표시(git 밖 · db/.leases/)


def _me():
    return os.environ.get("CLAUDE_CODE_HOST_SESSION_ID") or ""


def collector():
    """살아 있는 부모 표시 — {owner, owner_pid, children:[…]} · 부모 프로세스가 죽었으면 None(표시도 지운다)."""
    try:
        info = json.loads(COLLECT.read_text())
    except (OSError, ValueError):
        return None
    if not coredb._alive(int(info.get("owner_pid") or 0)):
        COLLECT.unlink(missing_ok=True)
        return None
    return info


def main(a):
    # ⑹ 부모가 모아서 커밋하는 중이면 하위 세션은 ship하지 않는다(--check는 커밋하지 않으니 허용)
    col = collector()
    if col and _me() in col.get("children", []) and not a.check:
        sys.exit(f"⛔ 부모 세션({col.get('owner')})이 하위 세션 변경을 모아서 커밋한다 — 여기서는 커밋하지 않는다.\n"
                 "   부모에게 보고할 것: ⑴ 바꾼 파일 경로 ⑵ DB 변경(표·행·migration 번호) ⑶ 커밋 메시지 초안 ⑷ 게이트 결과(--check).")
    # ⑵ 인덱스 오염 검사 — **가장 먼저** 한다. 이걸 놓치면 남의 변경을 내 커밋에 싣는다.
    staged = [l for l in sh("git diff --cached --name-only").stdout.split("\n") if l.strip()]
    if staged and not a.force_index:
        print("⛔ 인덱스에 이미 올라온 파일이 있다 — 다른 세션이 스테이징했을 수 있다:")
        for f in staged[:20]:
            print("   ", f)
        sys.exit("   내가 올린 것이 맞으면 --force-index, 아니면 `git restore --staged <파일>`로 빼고 다시 실행할 것.\n"
                 "   ⚠️ 2026-09-21에 이걸 지나쳐 직전 커밋의 43줄이 지워졌다(docs/70).")

    # ⑸ 남의 작성이 끝날 때까지 기다린다 — 끝나면 ship 표시를 걸어 새 연결을 멈춰 세운다.
    coredb.mark_waiting()                     # 나는 이제 안 쓴다 — 서로 기다리는 교착을 막는다
    try:
        wait_for_writers(a.wait)
        coredb.hold_ship()                    # 한 세션만 잡는다(원자적) — 남이 잡고 있으면 기다린다
        try:
            return _ship(a)
        finally:
            coredb.release_ship()
    finally:
        coredb.clear_waiting()


def wait_for_writers(max_wait):
    t0, last = time.time(), None
    while True:
        ws = coredb.active_writers()
        if not ws:
            if last:
                print(f"▶ 다른 세션 작성 끝 — {int(time.time() - t0)}초 기다렸다")
            return
        now = sorted((w.get("session") or str(w.get("pid")), w.get("script")) for w in ws)
        if now != last:
            print("⏳ 다른 세션이 DB에 쓰는 중이라 기다린다(게이트가 반쯤 쓴 상태에 걸리지 않게):")
            for w in ws:
                print(f"    · {w.get('session') or 'pid ' + str(w.get('pid'))} — 마지막 쓰기 {w['idle_sec']}초 전 ({w.get('script')})")
            last = now
        if time.time() - t0 > max_wait:
            sys.exit(f"⛔ {max_wait}초를 기다려도 끝나지 않았다 — 이번엔 커밋하지 않는다(작업 트리는 그대로).\n"
                     "   더 기다리려면 백그라운드로 `--wait 3600`을 주고 다시 실행할 것. "
                     f"조용해진 지 {coredb.QUIET_SEC // 60}분이 지난 표시는 자동으로 무시된다.")
        time.sleep(20)


def _ship(a):
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
    # ⛔⛔ git add의 실패를 확인한다(2026-10-05 · 같은 날 두 번 — 불변규칙 13).
    #    다른 세션·앱의 git 조회가 .git/index.lock을 잠깐 잡으면 add가 통째로 실패하는데, 종전엔 반환값을 안 봐서
    #    「변경 없음 — 커밋할 것이 없다」로 **조용히 거짓 보고**했다(바뀐 파일이 그대로 남아 있었다).
    #    ⇒ 잠금이면 잠깐 기다려 다시 하고, 그래도 실패하면 오류를 그대로 보이고 멈춘다.
    import time
    for t in range(8):
        r = sh(["git", "add", "--"] + paths)
        if r.returncode == 0:
            break
        if "index.lock" not in (r.stderr or ""):
            sys.exit(f"⛔ git add 실패:\n{r.stderr.strip()}")
        time.sleep(1.5)
    else:
        sys.exit(f"⛔ git add 실패 — .git/index.lock이 계속 잡혀 있다(다른 git 작업 중):\n{r.stderr.strip()}")

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
    coredb.release()                 # 내 작성은 커밋에 담겼다 — 기다리던 다른 세션이 곧장 진행한다
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
    ap.add_argument("--wait", type=int, default=540,
                    help="다른 세션의 DB 작성이 끝나길 기다리는 최대 초(기본 540 · 셸 10분 제한 안쪽). 길게는 백그라운드로")
    ap.add_argument("--collect", nargs="+", metavar="SESSION_ID",
                    help="(부모 세션) 이 하위 세션들의 ship을 막고 내가 모아서 커밋한다 — 여러 번 부르면 누적")
    ap.add_argument("--collect-end", action="store_true", help="(부모 세션) 모아서 커밋을 끝내고 표시를 지운다")
    a = ap.parse_args()
    if a.collect or a.collect_end:
        cur = collector() or {}
        if a.collect_end:
            COLLECT.unlink(missing_ok=True)
            sys.exit(print("▶ 모아서 커밋 표시를 지웠다 — 하위 세션도 다시 직접 ship할 수 있다") or 0)
        COLLECT.parent.mkdir(parents=True, exist_ok=True)
        info = {"owner": _me(), "owner_pid": int(coredb.session_key()),
                "children": sorted(set(cur.get("children", [])) | set(a.collect))}
        COLLECT.write_text(json.dumps(info, ensure_ascii=False))
        sys.exit(print(f"▶ 하위 세션 {len(info['children'])}개의 ship을 막았다(부모 {info['owner']}): "
                       + ", ".join(info["children"])) or 0)
    if not a.check and not (a.message or a.file):
        ap.error("-m 또는 -F 가 필요하다 (--check 는 예외)")
    sys.exit(main(a))
