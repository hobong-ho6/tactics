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
        # ⭐ 갤러리(2026-10-02 사용자 지시 「클럽 싱크 선수 수집이 끝나면 달성 가능한 갤러리 목록 · NEW 알림」).
        #    보유가 바뀌면 낼 수 있는 등급이 바뀐다 ⇒ 선수 단계의 끝에서 세트 정의를 갱신하고 다시 평가한다.
        ("갤러리 세트 정의", [PY, S("collect_futgg_gallery.py"), "--games", "27"], False),
        ("갤러리 평가(달성 가능·NEW)", [PY, S("gallery_eval.py")], False),
    ],
    "진화": [
        ("진화 카탈로그·경로·적용가능", [PY, S("collect_futgg_evolutions.py"), "--games", "27", "--fill-catalog"], False),
        ("해금 조건(목표 과제)", [PY, S("collect_futgg_objectives.py")], False),
        ("한국어 이름·설명·미션", [PY, S("collect_futmind_kr.py")], False),
        # ⭐ 1차 판정: EA가 준 진화 이력과 로그를 대조한다(migration 090). 스탯 역추정(--verify)은 보조다.
        ("진화 이력 대조(EA 이력 ↔ 로그)", [sys.executable, S("evo_detect.py"), "--ea"], False),
        ("원장 검산(EA 실측 대조)", [sys.executable, S("evo_detect.py"), "--verify"], False),
    ],
    "sbc": [
        ("SBC 세트·챌린지 수집", [PY, S("collect_futgg_sbc.py")], False),
        # ⭐ 포메이션은 FUTBIN에서 온다(2026-09-28) — 받는 건 Chrome 단계라 여기선 **결손만 센다**.
        #    받아 넣으면(`--json-file`) 그 스크립트가 해법을 바로 다시 푼다. 없는 챌린지는 `need_form`으로 남는다.
        ("SBC 포메이션 결손(FUTBIN)", [sys.executable, S("collect_futbin_sbc_formations.py"), "--missing"], False),
        ("해법 재계산", [PY, S("sbc_solve.py"), "--save"], False),
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
# ⭐ **실패해도 싱크를 멈추지 않는 축**(2026-09-30 사용자 지시 「시세 정보를 받아오는게 실패하는데 받아올 수 없다면
#    시세 정보는 안 받게끔」). 시세는 **어느 축의 입력도 아니다**(구매 우선순위 화면만 읽는다) — 막혔다고
#    뒤의 참조 수집·export까지 세우면 시세 하나 때문에 나머지가 전부 낡는다(2026-09-29 Cloudflare 403 실측).
#    ⇒ 실패하면 **건너뛰고 이어 간다.** 화면은 카드별 최신 시세를 그대로 쓰고, 신선도 표·종료 보고에 남긴다.
#    ⛔ 여기에 다른 축을 함부로 넣지 않는다 — 입력이 되는 축(선수·진화·sbc)이 조용히 건너뛰면 뒤 계산이 낡은 값 위에서 돈다.
OPTIONAL = {"시세"}

# ⭐ 순서가 곧 의존이다 — `선수`가 `진화`의 입력(대상 명단·현재 스탯)을 채운다(런북 「순서 의존」).
ALL_ORDER = ["선수", "진화", "sbc", "시세", "참조"]

# ⭐⭐ **한 항목을 돌리면 그 결과에 기대는 축도 같이 다시 계산한다**(2026-09-27 사용자 지시
#    「클럽 싱크 끝나면 어떤 클럽 싱크가 완료되었는지에 따라 연관 있는 메뉴나 기능은 모두 갱신하도록 처리」).
#    ⛔ 「기억해서 같이 돌리자」로 두지 않는다 — 런북의 「연관 메뉴를 한 번에 닫는다」 표가
#       일곱 항목까지 늘어난 것이 그 방식의 한계를 보여준다. 의존을 **표로 적고 기계가 따라간다**.
#    ⚠️ 화면(진화 순위·케미 추천·전술 대조)은 **계산이 아니라 렌더**라 export만 다시 돌면 따라온다 —
#       그래서 여기 적는 것은 **DB를 다시 써야 하는 축**뿐이다.
AFTER = {
    # 보유가 바뀌면 SBC 해법이 바뀐다(카드가 들어오고 나간다). 진화 대상 명단·현재 스탯도 바뀐다.
    "선수": ["진화", "sbc"],
    # 진화가 바뀌면 소진·경로가 바뀌고, 그 카드로 푸는 SBC 해법도 바뀐다.
    "진화": ["sbc"],
}
ALIAS = {"all": "전체", "전체": "전체", "player": "선수", "선수": "선수", "evo": "진화", "진화": "진화",
         "sbc": "sbc", "SBC": "sbc", "price": "시세", "시세": "시세", "tactic": "전술", "전술": "전술"}

# ⭐⭐ **무엇이 있는지 외우게 하지 않는다**(2026-09-27 사용자 지적 「내가 무슨 인자가 있는지 까먹을 수 있잖아」).
#    ⛔ 종전엔 모르는 항목을 주면 `sorted(set(ALIAS))`를 그대로 뱉어 `['SBC','all','evo',…]`처럼
#       읽기 어려웠고, 인자 없이 부르면 **묻지도 않고 전체로 갔다**.
#    ⇒ 항목마다 한 줄 설명을 두고 ⑴ `--list` ⑵ 모르는 항목 ⑶ **인자 없음** 세 경우에 같은 표를 찍는다.
#    ⚠️ 인자 없음에서 **돌리지 않고 멈추는** 것이 핵심이다 — 호출부(런북·예약)는 전부 인자를 명시하므로
#       여기 걸릴 일이 없고, 걸린다면 그건 **사람이 셸에서 친 것**이라 고를 기회를 주는 게 맞다.
ITEM_HELP = [
    ("전체",  "all",    "아래 전부 + 참조 표 (가장 오래 걸린다)"),
    ("선수",  "player", "보유 카드·활성 스쿼드·케미 스타일 · 새 카드 수집 · 링크/동일성 검산 · 갤러리 평가  [--capture 필요]"),
    ("진화",  "evo",    "카탈로그·해금 조건·한국어 · 적용 가능 선수 · 원장 검산"),
    ("sbc",   "sbc",    "SBC 세트/챌린지 수집 + 해법 재계산"),
    ("시세",  "price",  "카드 시세 스냅샷 (예산 한 번 ~45장 · 1분 안쪽 · 나머지는 다음 회차가 이어 받는다)"),
    ("전술",  "tactic", "⚠️ 손 작업 — 인게임 전술 + 감독/포메이션 확인 안내만 찍는다"),
]


def print_items(head):
    print(head)
    print(f"\n  {'항목':<8}{'별칭':<9}무엇을")
    for ko, en, why in ITEM_HELP:
        print(f"  {ko:<8}{en:<9}{why}")
    after = " · ".join(f"{k}→{'·'.join(v)}" for k, v in AFTER.items())
    print(f"\n  ⭐ 연쇄: {after}  (고른 항목이 흔드는 축은 자동으로 따라 돈다)")
    print("  예:  python3 scripts/club_sync.py 진화")
    print("       python3 scripts/club_sync.py 전체 --capture /tmp/ggclub-YYYYMMDD.json")
    print("       python3 scripts/club_sync.py 진화 --dry-run")

# 사람이 해야 하는 단계 — 스크립트가 대신하지 않고 **무엇이 남았는지 찍는다**.
MANUAL = {
    "선수": ["브라우저로 GG Club 열고 `collect_ggclub.py --auth-file …`로 캡처를 만든다(로그인 대행 금지)"],
    "sbc": ["포메이션 결손이 있으면 Chrome의 www.futbin.com 탭에서 "
            "`collect_futbin_sbc_formations.py --print-snippet` ①시작 → ②읽기 → `--json-file`로 넣는다(해법은 자동 재계산)"],
    "전술": ["`https://www.fut.gg/gg-club/my/tactics/` 본문을 읽어 `fut_tactics`/`fut_tactic_roles`에 새 `pulled` 행 추가",
             "활성 스쿼드 응답의 formation/manager/buildUp을 보고 `fut_squads` 갱신(케미에 직접 들어간다)"],
}


def run(label, cmd, dry, optional=False):
    print(f"\n▶ {label}\n   $ {' '.join(Path(c).name if c.startswith('/') else c for c in cmd)}")
    if dry:
        return True
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        if optional:
            print(f"   ⏭️ 실패(exit {r.returncode}) — **이 축은 건너뛰고 이어 간다**(OPTIONAL). 기존 값을 그대로 쓴다.")
            return False
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
         ("스쿼드 메타", "SELECT MAX(synced_at) FROM fut_squads"),
         ("갤러리 평가", "SELECT MAX(pulled) FROM fut_gallery_eval"),
         # ⭐ 참조 표도 여기 올린다(2026-09-27). `collect_playstyle_ids.py`가 fut.gg 번들의 난독화
         #    변수명에 앵커를 걸어 두 배포 연속 깨졌는데, 실패가 로그 한 줄이라 **두 회차 묻혔다**.
         #    수집 실패는 「행이 없다」가 아니라 「행이 낡는다」로 나타나므로 날짜로만 보인다.
         ("케미 스타일", "SELECT MAX(pulled) FROM fc_chemistry_styles"),
         ("PlayStyle 이름", "SELECT MAX(pulled) FROM fc_playstyle_ids"),
         ("포메이션", "SELECT MAX(pulled) FROM fc_formations"),
         ("6대 스탯 구성식", "SELECT MAX(pulled) FROM fc_face_stats")]
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
    ap.add_argument("item", nargs="?")   # ⛔ 기본값을 두지 않는다 — 없으면 목록을 보여주고 멈춘다
    ap.add_argument("--list", action="store_true", help="항목 목록만 보여준다")
    ap.add_argument("--capture", help="collect_ggclub.py가 만든 /tmp/ggclub-YYYYMMDD.json")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.list or not a.item:
        print_items("■ 클럽 싱크 — 돌릴 항목을 고른다" if not a.item else "■ 클럽 싱크 항목")
        if not a.item:
            print("\n⛔ 항목을 지정하지 않았다 — 전체를 돌리려면 `전체`를 명시할 것(실수로 다 도는 것을 막는다).")
        return
    item = ALIAS.get(a.item)
    if item is None:
        print_items(f"⛔ 모르는 항목 '{a.item}'")
        sys.exit(1)

    print(f"■ 클럽 싱크 — 항목 **{item}**" + (" (dry-run)" if a.dry_run else ""))
    if not run("게이트", [sys.executable, S("gates.py")], a.dry_run):
        sys.exit(1)                     # ⛔ 게이트 실패면 수집하지 않는다(런북 §1)

    if item == "전술":
        print("\n⚠️ 전술은 **손 작업**이다 — 스크립트가 대신하지 않는다.")
        for m in MANUAL["전술"]:
            print(f"   · {m}")
        staleness()
        return

    # ⭐ 연쇄 — 고른 항목이 흔드는 축을 뒤에 붙인다(중복 없이 · ALL_ORDER 순서를 지킨다).
    if item == "전체":
        buckets = ALL_ORDER
    else:
        need = {item, *AFTER.get(item, [])}
        buckets = [b for b in ALL_ORDER if b in need]
        extra = [b for b in buckets if b != item]
        if extra:
            print(f"\n⭐ `{item}`이 바꾼 값에 기대는 축도 같이 돈다: {' · '.join(extra)}"
                  "\n   (의존은 club_sync.py의 AFTER 표가 정본이다 — 새 축을 만들면 거기 올린다)")
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

    skipped = []
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
            if not run(f"[{b}] {label}", cmd, a.dry_run, optional=b in OPTIONAL):
                if b in OPTIONAL:
                    skipped.append(b)
                    break                        # 그 축의 남은 단계도 건너뛴다
                sys.exit(1)

    if "sbc" in buckets:
        print("\n⚠️ SBC 포메이션은 **Chrome 단계**가 남을 수 있다:")
        for m in MANUAL["sbc"]:
            print(f"   · {m}")
    if not a.dry_run:
        run("export", [sys.executable, S("export.py")], False)
    staleness()
    if skipped:
        print(f"\n⏭️ 건너뛴 축: {' · '.join(skipped)} — 받아오지 못해 **기존 값을 그대로 둔다**."
              "\n   종료 보고·커밋 메시지에 「시세 미갱신(사유)」을 적는다(신선도 표의 날짜가 근거다).")
    print("\n⛔ **커밋은 아직이다** — 무엇이 바뀌었는지 적어야 한다(불변규칙 5):")
    note = f" · ⚠️ {'·'.join(skipped)} 미갱신" if skipped else ""
    print(f'   python3 scripts/ship.py -m "data(fut): 클럽 싱크 {dt.date.today()} [{item}] — …{note}"')


if __name__ == "__main__":
    main()
