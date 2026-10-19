"""DB 연결 정본 — 동시 작업 대기·순번제 (2026-10-19 사용자 지시 「여러 데이터를 수집할 때 서로 DB를 점유해서
다른 작업을 못 하는데 이거 개선」 · 방식 「대기·순번제」).

왜:
  ⑴ DB가 롤백 저널(journal_mode=delete)이라 한 세션이 쓰는 동안 다른 세션은 잠긴다. 스크립트 73개가 각자
     `sqlite3.connect`를 **기본 5초**로 열어 「database is locked」로 바로 넘어졌다.
  ⑵ `ship.py`가 공용 DB에서 게이트를 돌려, 다른 세션이 수집하는 **도중의 상태**에 걸려 실패했다(10-19 G18).
  ⇒ ① 잠기면 기다린다(60초) ② 실제로 쓴 세션은 「작성 중」 표시(lease)를 남기고, `ship.py`는 남의 작성이
     끝날 때까지 기다렸다가 게이트를 돈다(scripts/ship.py · wait_for_writers).
  ⚠️ WAL은 쓰지 않는다 — `~/Documents`가 iCloud 동기화 폴더라 -wal/-shm이 따로 동기화되면 다른 PC에서 깨진다.

⛔ 메인 DB에 `sqlite3.connect`를 직접 쓰지 않는다 — G36이 막는다. 이 모듈의 `connect()`만 쓴다.

lease(작성 중 표시):
  - 위치 `db/.leases/<세션키>.json` (git 밖 · .gitignore) · 세션키 = CLAUDE_PID(대화 세션 프로세스) 없으면 프로세스 pid
  - **쓰기(INSERT·UPDATE·DELETE·DDL)가 실제로 일어날 때만** 남긴다(읽기만 하는 세션은 남을 막지 않는다)
  - 살아 있는 것으로 치는 조건: 그 pid가 살아 있고 마지막 쓰기가 QUIET_SEC 안쪽 — 죽은 세션·오래 조용한 세션은 무시
  - 자기 커밋을 끝낸 `ship.py`가 자기 lease를 지운다(release)
  ⚠️ `sqlite3` CLI로 직접 쓰는 것은 잡지 못한다(파이썬 밖) — 수집은 스크립트로 한다.
"""
import json
import os
import sqlite3
import sys
import time
from pathlib import Path

from core import DB, ROOT

LEASE_DIR = ROOT / "db" / ".leases"
QUIET_SEC = 10 * 60          # 마지막 쓰기 뒤 이만큼 조용하면 「작성 끝」으로 본다
BUSY_SEC = 60                # 잠금 대기

_WRITE_ACTIONS = {
    sqlite3.SQLITE_INSERT, sqlite3.SQLITE_UPDATE, sqlite3.SQLITE_DELETE,
    sqlite3.SQLITE_CREATE_TABLE, sqlite3.SQLITE_DROP_TABLE, sqlite3.SQLITE_ALTER_TABLE,
    sqlite3.SQLITE_CREATE_INDEX, sqlite3.SQLITE_DROP_INDEX,
}


def session_key():
    return str(os.environ.get("CLAUDE_PID") or os.getpid())


def _is_main(path):
    try:
        return Path(path).resolve() == DB.resolve()
    except (TypeError, OSError):
        return False


def _touch_lease():
    LEASE_DIR.mkdir(parents=True, exist_ok=True)
    p = LEASE_DIR / f"{session_key()}.json"
    info = {"pid": int(session_key()), "session": os.environ.get("CLAUDE_CODE_HOST_SESSION_ID"),
            "script": Path(sys.argv[0]).name if sys.argv and sys.argv[0] else "python",
            "last": time.time()}
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(info, ensure_ascii=False))
    tmp.replace(p)


SHIP = LEASE_DIR / "ship.json"
SHIP_MAX_SEC = 15 * 60       # ship 하나가 이보다 오래 걸린 적은 없다 — 넘으면 표시를 무시한다(죽은 표시 방지)


def _ship_holder():
    """다른 세션이 ship(게이트→export→dump→커밋) 중이면 그 정보, 아니면 None."""
    try:
        info = json.loads(SHIP.read_text())
    except (OSError, ValueError):
        return None
    if str(info.get("pid")) == session_key() or not _alive(int(info.get("pid") or 0)) \
            or time.time() - float(info.get("since") or 0) > SHIP_MAX_SEC:
        return None
    return info


def mark_waiting():
    """ship.py가 커밋 순서를 기다리는 동안 — 이 세션은 더 쓰지 않는다는 표시."""
    os.environ.setdefault("CLAUDE_PID", str(os.getpid()))
    LEASE_DIR.mkdir(parents=True, exist_ok=True)
    (LEASE_DIR / f"{session_key()}.waiting").write_text(str(time.time()))


def hold_ship():
    """ship 표시를 **한 세션만** 잡는다(원자적 생성). 남이 잡고 있으면 풀릴 때까지 기다린다."""
    # ⚠️ 터미널에서 직접 돌리면 CLAUDE_PID가 없다 — 그러면 자식(gates·export)이 pid가 달라 「남의 ship」으로 보고
    #    자기 자신을 기다린다. ship 프로세스 pid를 세션키로 박아 자식에게 물려준다.
    os.environ.setdefault("CLAUDE_PID", str(os.getpid()))
    LEASE_DIR.mkdir(parents=True, exist_ok=True)
    body = json.dumps({"pid": int(session_key()), "since": time.time(),
                       "session": os.environ.get("CLAUDE_CODE_HOST_SESSION_ID")})
    said = False
    while True:
        try:
            fd = os.open(SHIP, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w") as f:
                f.write(body)
            return
        except FileExistsError:
            h = _ship_holder()
            if h is None:                                   # 죽었거나 오래된 표시 · 내 것 — 치우고 다시
                SHIP.unlink(missing_ok=True)
                continue
            if not said:
                print(f"⏳ 다른 세션({h.get('session') or h.get('pid')})이 먼저 커밋 중 — 끝나면 이어서 한다")
                said = True
            time.sleep(5)


def release_ship():
    try:
        if str(json.loads(SHIP.read_text()).get("pid")) == session_key():
            SHIP.unlink()
    except (OSError, ValueError):
        pass


def connect(path=None, *, timeout=BUSY_SEC):
    """메인 DB(또는 주어진 경로) 연결. 잠기면 timeout초 기다린다. 메인 DB에 쓰면 lease를 남긴다.
    ⭐ 다른 세션이 ship 중이면 끝날 때까지 기다린다 — 그 커밋에 반쯤 쓴 상태가 섞이지 않게(최대 SHIP_MAX_SEC)."""
    path = path or DB
    if _is_main(path):
        h, said = _ship_holder(), False
        while h:
            if not said:
                print(f"⏳ 다른 세션({h.get('session') or h.get('pid')})이 커밋(ship) 중이라 끝날 때까지 기다린다…",
                      file=sys.stderr)
                said = True
            time.sleep(5)
            h = _ship_holder()
    con = sqlite3.connect(path, timeout=timeout)
    con.execute(f"PRAGMA busy_timeout={int(timeout * 1000)}")
    if _is_main(path):
        state = {"last": 0.0}

        def _auth(action, *_):
            if action in _WRITE_ACTIONS and time.time() - state["last"] > 30:   # 30초에 한 번만 파일을 갱신
                state["last"] = time.time()
                try:
                    _touch_lease()
                except OSError:
                    pass                                    # 표시 실패가 쓰기를 막지는 않는다
            return sqlite3.SQLITE_OK

        con.set_authorizer(_auth)
    return con


def _alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def active_writers(exclude_self=True):
    """지금 작성 중인 다른 세션 목록 — [{pid, session, script, idle_sec}]. 죽었거나 오래 조용한 lease는 지운다."""
    out = []
    if not LEASE_DIR.is_dir():
        return out
    me = session_key()
    for p in LEASE_DIR.glob("*.json"):
        try:
            info = json.loads(p.read_text())
        except (OSError, ValueError):
            continue
        idle = time.time() - float(info.get("last") or 0)
        if not _alive(int(info.get("pid") or 0)) or idle > QUIET_SEC:
            p.unlink(missing_ok=True)
            continue
        if exclude_self and p.stem == me:
            continue
        # ⭐ 이미 ship.py에서 커밋 순서를 기다리는 세션은 「작성 끝」이다 — 세지 않는다(둘이 서로 기다리는 교착 방지)
        if (LEASE_DIR / f"{p.stem}.waiting").exists():
            continue
        out.append({**info, "idle_sec": int(idle)})
    return out


def release():
    """자기 lease·대기 표시를 지운다 — 자기 커밋을 끝낸(또는 그만둔) ship.py가 부른다."""
    (LEASE_DIR / f"{session_key()}.json").unlink(missing_ok=True)
    clear_waiting()


def clear_waiting():
    (LEASE_DIR / f"{session_key()}.waiting").unlink(missing_ok=True)
