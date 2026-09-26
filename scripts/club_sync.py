#!/usr/bin/env python3
"""클럽 싱크 **항목 실행기** (2026-09-27 신설).

왜 (사용자 지시 「클럽 싱크를 세분화해서…」 → 「그럼 이제 분리해서 할 수 있는 거야?」):
  런북에 디스패치 표를 적는 것만으로는 **세션이 그 표를 읽어야** 작동한다(불변규칙 13의 ⑤문서 수준).
  ⛔ 읽는 것은 확률이 1이 아니다 — 실제로 시세·SBC·전술 세 축이 **표에 없어서 아무도 안 불렀고**
     `player_card_prices`가 8일, `fut_squads`가 8일 낡았다.
  ⇒ 순서·구성을 **여기 한 곳**에 두고(④스크립트), 런북은 이 명령을 부르기만 한다.

⛔ 여기서 **커밋하지 않는다** — 커밋 메시지는 회차마다 판단이 필요하다(무엇이 바뀌었나).
   끝나면 `ship.py` 한 줄을 찍어 준다.
⛔ **브라우저·로그인이 필요한 단계는 이 스크립트가 하지 않는다**(로그인 대행 금지).
   `선수`·`전술`은 사람이 먼저 캡처/조회한 뒤 부른다 — 무엇이 남았는지 끝에 찍는다.

사용:
    python3 scripts/club_sync.py 진화
    python3 scripts/club_sync.py 선수 --capture /tmp/ggclub-20260927.json
    python3 scripts/club_sync.py 전체 --capture /tmp/ggclub-20260927.json
    python3 scripts/club_sync.py sbc | 시세 | 전술
    python3 scripts/club_sync.py 진화 --dry-run      # 무엇을 돌릴지만 찍는다
"""
import argparse
import datetime as dt
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                        # noqa: E402

PY = str(ROOT / ".venv" / "bin" / "python")
if not Path(PY).exists():
    PY = sys.executable
S = lambda n: str(ROOT / "scripts" / n)                     # noqa: E731

# ── 항목 정의 ────────────────────────────────────────────────────────────────
# ⛔ **새 수집 축을 만들면 반드시 여기에 올린다** — 표에 없으면 아무도 부르지 않는다(위 주석의 실증).
#    `capture`가 True인 단계는 캡처 파일 경로를 인자로 받는다.
STEPS = {
    "선수": [
        ("보유·스쿼드 반영", [PY, S("fut_club_sync.py"), "{capture}", "--account", "main"], True),
        ("관리 4팀 카드 수집", [PY, S("collect_futgg_cards.py"), "--games", "27"], False),
        ("링크 결손", [sys.executable, S("gaps.py"), "links"], False),
        ("동일성 3요소", [sys.executable, S("gaps.py"), "identity"], False),
        ("스쿼드 조회 범위", [sys.executable, S("gaps.py"), "squad"], False),
    ],
    "진화": [
        ("진화 카탈로그·경로·적용가능", [PY, S("collect_futgg_evolutions.py"), "--games", "27", "--fill-catalog"], False),
        ("해금 조건(목표 과제)", [PY, S("collect_futgg_objectives.py")], False),
        ("한국어 이름·설명·미션", [PY, S("collect_futmind_kr.py")], False),
        ("원장 검산(EA 실측 대조)", [sys.executable, S("evo_detect.py"), "--verify"], False),
    ],
    "sbc": [
        ("SBC 세트·챌린지 수집", [PY, S("collect_futgg_sbc.py")], False),
        ("해법 재계산", [PY, S("sbc_solve.py")], False),
    ],
    "시세": [
        ("카드 시세 스냅샷", [PY, S("collect_futgg_prices.py"), "--games", "27"], False),
    ],
    "참조": [   # 전체에서만 — 평소엔 안 바뀌지만 EA 패치 때 바뀐다
        ("케미 스타일", [PY, S("collect_chem_styles.py")], False),
        ("6대 구성식", [PY, S("collect_face_stat_defs.py")], False),
        ("PlayStyle id", [PY, S("collect_playstyle_ids.py")], False),
        ("포메이션", [PY, S("collect_futgg_formations.py")], False),
        ("케미 신호", [PY, S("collect_futgg_chem.py")], False),
    ],
}
# ⭐ 순서가 곧 의존이다 — `선수`가 `진화`의 입력(대상 명단·현재 스탯)을 채운다(런북 「순서 의존」).
ALL_ORDER = ["선수", "진화", "sbc", "시세", "참조"]
ALIAS = {"all": "전체", "전체": "전체", "player": "선수", "선수": "선수", "evo": "진화", "진화": "진화",
         "sbc": "sbc", "SBC": "sbc", "price": "시세", "시세": "시세", "tactic": "전술", "전술": "전술"}

# 사람이 해야 하는 단계 — 스크립트가 대신하지 않고 **무엇이 남았는지 찍는다**.
MANUAL = {
    "선수": ["브라우저로 GG Club 열고 `collect_ggclub.py --auth-file …`로 캡처를 만든다(로그인 대행 금지)"],
    "전술": ["`https://www.fut.gg/gg-club/my/tactics/` 본문을 읽어 `fut_tactics`/`fut_tactic_roles`에 새 `pulled` 행 추가",
             "활성 스쿼드 응답의 formation/manager/buildUp을 보고 `fut_squads` 갱신(케미에 직접 들어간다)"],
}


def run(label, cmd, dry):
    print(f"\n▶ {label}\n   $ {' '.join(Path(c).name if c.startswith('/') else c for c in cmd)}")
    if dry:
        return True
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        print(f"   ⛔ 실패(exit {r.returncode}) — 여기서 멈춘다. 원인을 보고할 것.")
        return False
    return True


def staleness():
    """⚠️ 「업데이트했다」가 낡은 입력 위에서 돌았다는 사실을 덮지 않게 — 축별 최신 수집일을 찍는다."""
    con = sqlite3.connect(DB)
    q = [("보유 카드", "SELECT MAX(synced_at) FROM fut_club_players"),
         ("진화 카탈로그", "SELECT MAX(pulled) FROM fc_evolutions"),
         ("SBC", "SELECT MAX(pulled) FROM fc_sbc_sets"),
         ("시세", "SELECT MAX(pulled) FROM player_card_prices"),
         ("전술", "SELECT MAX(pulled) FROM fut_tactics"),
         ("스쿼드 메타", "SELECT MAX(synced_at) FROM fut_squads")]
    today = dt.date.today()
    print("\n■ 축별 신선도")
    for name, sql in q:
        try:
            v = con.execute(sql).fetchone()[0]
        except sqlite3.OperationalError:
            v = None
        if not v:
            print(f"   ⚪ {name:<12} (없음)")
            continue
        d = (today - dt.date.fromisoformat(str(v)[:10])).days
        mark = "✅" if d <= 1 else "⚠️" if d <= 3 else "⛔"
        print(f"   {mark} {name:<12} {str(v)[:10]}  ({d}일)")
    con.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("item", nargs="?", default="전체")
    ap.add_argument("--capture", help="collect_ggclub.py가 만든 /tmp/ggclub-YYYYMMDD.json")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    item = ALIAS.get(a.item)
    if item is None:
        sys.exit(f"⛔ 모르는 항목 '{a.item}' — {sorted(set(ALIAS))}")

    print(f"■ 클럽 싱크 — 항목 **{item}**" + (" (dry-run)" if a.dry_run else ""))
    if not run("게이트", [sys.executable, S("gates.py")], a.dry_run):
        sys.exit(1)                     # ⛔ 게이트 실패면 수집하지 않는다(런북 §1)

    if item == "전술":
        print("\n⚠️ 전술은 **손 작업**이다 — 스크립트가 대신하지 않는다.")
        for m in MANUAL["전술"]:
            print(f"   · {m}")
        staleness()
        return

    buckets = ALL_ORDER if item == "전체" else [item]
    if item != "전체" and item != "선수":
        # ⚠️ 단독 실행은 **낡은 입력 위에서 돌 수 있다**(런북 「순서 의존」).
        con = sqlite3.connect(DB)
        v = con.execute("SELECT MAX(synced_at) FROM fut_club_players").fetchone()[0]
        con.close()
        if v:
            d = (dt.date.today() - dt.date.fromisoformat(str(v)[:10])).days
            if d >= 2:
                print(f"\n⚠️⚠️ 보유 카드가 **{d}일 낡았다**({v}). `{item}` 계산의 입력이 그만큼 낡았다는 뜻이다 —"
                      "\n     새 카드는 대상 명단에서 빠지고, 요구조건(Max OVR·Pace·PS)은 낡은 스탯으로 판정된다."
                      "\n     ⇒ **종료 보고에 이 사실을 적는다.** 정확히 하려면 `선수`를 먼저 돌린다.")

    for b in buckets:
        if b == "선수" and not a.capture and not a.dry_run:
            print("\n⚠️ `선수`는 캡처 파일이 필요하다(`--capture`). 브라우저 단계는 사람이 한다:")
            for m in MANUAL["선수"]:
                print(f"   · {m}")
            print("   ⇒ 보유 반영을 건너뛰고 나머지(카드 수집·검산)만 돈다.")
        for label, cmd, needs_cap in STEPS[b]:
            if needs_cap:
                if not a.capture:
                    continue
                cmd = [c.replace("{capture}", a.capture) for c in cmd]
            if not run(f"[{b}] {label}", cmd, a.dry_run):
                sys.exit(1)

    if not a.dry_run:
        run("export", [sys.executable, S("export.py")], False)
    staleness()
    print("\n⛔ **커밋은 아직이다** — 무엇이 바뀌었는지 적어야 한다(불변규칙 5):")
    print(f'   python3 scripts/ship.py -m "data(fut): 클럽 싱크 {dt.date.today()} [{item}] — …"')


if __name__ == "__main__":
    main()
