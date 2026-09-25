#!/usr/bin/env python3
"""GG Club 스냅샷 직접 수집 — 보유 카드 전량 + 활성 스쿼드 (2026-09-21 신설).

왜 (사용자 지시 2026-09-21 「스크립트를 만들어서 싱크해」): 종전 절차는 브라우저가 읽은 100명치 JSON을
**에이전트 컨텍스트를 두 번 통과**시켰다(브라우저 출력 → 파일 쓰기). 14KB × 2 ≈ 1만 토큰이 회차마다 샜다.
이 스크립트가 API를 직접 호출하면 **보유가 100명이든 1000명이든 컨텍스트 비용은 0**이다.

⛔ 인원을 줄여 아끼지 않는다. 원장의 처분 판정이 「EA 목록에 없는 보유 행 = 매각」 규칙이라
   **전량을 읽어야 그 규칙이 성립한다**(활성 스쿼드만 읽으면 나머지가 전부 '사라진 것'으로 보인다).
   실증(2026-09-21): 전량 순회가 매각 4건(긴터·페랭·라트바인·퀸)을 잡아냈다.

⛔ 로그인·「Sync Club」 클릭 대행은 금지다(런북 §0). 이 스크립트는 **이미 로그인된 세션의 토큰을 빌려
   읽기만** 한다 — 계정에 작업을 걸지 않는다.

── 인증 ──────────────────────────────────────────────────────────────────────
⚠️ `/api/gg-club/…`는 **Authorization 헤더가 없으면 404**다(2026-09-21 실측 — 쿠키만으로는 안 된다).
토큰은 로그인된 fut.gg 탭에서 한 번 꺼내 **환경변수로** 넘긴다. 디스크에 쓰지 않는다.

    # ① 로그인된 fut.gg GG Club 탭의 콘솔에서 (앱이 보내는 헤더를 가로챈다)
    #    → 출력된 JSON 한 줄을 복사
    #    스니펫은 `--print-snippet`으로 찍어 쓴다.
    # ② 쉘에서
    FUTGG_AUTH='<복사한 JSON>' .venv/bin/python scripts/collect_ggclub.py --apply-squad

⚠️ 토큰 수명은 약 1시간이다(JWT exp). 만료되면 404가 나므로 다시 꺼낸다.

── 출력 ──────────────────────────────────────────────────────────────────────
`fut_club_sync.py`가 먹는 형식으로 파일을 쓴다:
    [{"ea","n","ovr","six":[6],"cs","cp","gg","added","paid"}, ...]
`--apply-squad`면 `fut_squad_slots`(XI 11 + BENCH 12)도 갱신한다.
표준출력은 **요약 몇 줄뿐** — 선수 데이터는 절대 찍지 않는다(그게 이 스크립트의 존재 이유다).

사용:
    .venv/bin/python scripts/collect_ggclub.py --print-snippet
    FUTGG_AUTH='…' .venv/bin/python scripts/collect_ggclub.py --apply-squad
    .venv/bin/python scripts/collect_ggclub.py --auth-file /tmp/ggauth.json --apply-squad
"""
import argparse
import datetime as dt
import json
import os
import sqlite3
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                     # noqa: E402

TODAY = dt.date.today().isoformat()
API = "https://www.fut.gg/api/gg-club"
SIX = ["facePace", "faceShooting", "facePassing", "faceDribbling", "faceDefending", "facePhysicality"]
SIX_GK = ["gkFaceDiving", "gkFaceHandling", "gkFaceKicking", "gkFaceReflexes", "gkFaceSpeed", "gkFacePositioning"]

# 로그인된 GG Club 탭에서 실행 → Authorization 헤더를 한 번 가로채 JSON으로 찍는다.
SNIPPET = r"""
(async () => {
  const of_ = window.__ggOf || window.fetch; window.__ggOf = of_;
  let hdr = null;
  await new Promise(res => {
    window.fetch = async (...a) => {
      const r = await of_(...a);
      try {
        const u = (typeof a[0] === 'string' ? a[0] : a[0].url) || '';
        if (u.includes('/api/gg-club/') && a[1] && a[1].headers) {
          const h = a[1].headers;
          hdr = h instanceof Headers ? Object.fromEntries(h) : h;
          res();
        }
      } catch (e) {}
      return r;
    };
    const a = [...document.querySelectorAll('a')].find(x => (x.getAttribute('href') || '').startsWith('/gg-club/my/'));
    if (a) a.click();
    setTimeout(res, 6000);
  });
  window.fetch = of_;
  return hdr ? JSON.stringify(hdr) : 'NO_AUTH_HEADER — GG Club 페이지에서 실행했는지 확인';
})()
"""


def get(url, headers):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sys.exit("⛔ 404 — 토큰이 만료됐거나 헤더가 빠졌다. 탭에서 다시 꺼낼 것(수명 약 1시간).")
        raise


# ⭐⭐ 29속성 — GG Club이 **EA 실측 그대로** 준다(2026-09-22 확인, 사용자 질문 「싱크로 상세 스탯까지 가져올 수 있지?」).
#    종전에는 기준 카드 + 진화 보상으로 **재구성 추정**을 했는데, 그럴 필요가 없다.
#    ⇒ 재구성은 이제 **검증용**으로만 남긴다(추정↔실측 대조 = 진화 기록 오류 탐지기).
# ⛔ 표를 여기 두지 않는다 — 정본은 `core/futgg_attrs.py`다(2026-09-23).
#    종전엔 같은 표가 네 파일에 복제돼 있었고 **이 파일만** `attributeFreeKickAccuracy`(오타)를 찾아
#    「프리킥 정확도」를 100% 흘렸다 → 6대 스탯 PAS가 보유 89명 전원에서 2~4 낮게 계산됐다.
from core.futgg_attrs import parse_attrs        # noqa: E402  (ROOT를 sys.path에 넣은 뒤라 아래에 둔다)

# 수집 중 발견한 결손 속성 — ⛔ 조용히 넘기지 않고 끝에 건수로 보고한다(obs#132).
MISSING = {}


def rows_of(players):
    out = []
    for p in players:
        q = p.get("playerDef") or {}
        keys = SIX_GK if q.get("position") == 0 else SIX
        name = q.get("commonName") or f"{q.get('firstName') or ''} {q.get('lastName') or ''}".strip()
        # ⚠️ GK는 필드 29속성을 다 갖지 않는다 — 기준을 나눠 대조한다.
        attrs, missing = parse_attrs(q, want=set() if q.get("position") == 0 else None)
        if missing:
            MISSING[tuple(missing)] = MISSING.get(tuple(missing), 0) + 1
        nm_of = lambda o: (o or {}).get("name")                    # noqa: E731  nation/league/club은 객체로 온다
        out.append({"ea": q.get("eaId"), "n": name, "ovr": q.get("overall"),
                    "six": [q.get(k) for k in keys],
                    "attrs": attrs or None,                       # ⛔ 없으면 None — 빈 dict를 「0」으로 굳히지 않는다
                    "accel": q.get("accelerateType"),             # ⚠️ 실측 0/99 — GG Club은 AcceleRATE를 안 준다(카드 수집기 몫)
                    # ⭐ 역할 숙련도 GG Club이 준다(2026-09-22) — 원장의 `current_roles_*`가 낡아 있었다
                    #    (캐시: EA는 [5,23]=RB Wingback·RM Winger인데 원장은 []였다).
                    "rp": q.get("rolesPlus"), "rpp": q.get("rolesPlusPlus"),
                    # ⭐⭐ ① PlayStyle **EA 실측**(2026-09-24 신설 · migration 061 참조).
                    #    ⛔ 종전엔 안 받아서 원장이 fut.gg 계산 카드(path_json)를 썼고, 보가르데·루제리에
                    #       **없는 Inventive가 찍혔다.** 숫자 id로 오며 이름은 `fc_playstyle_ids`가 푼다.
                    "ps": q.get("playstyles"), "psp": q.get("playstylesPlus"),
                    "cs": p.get("chemistryStyle"), "cp": p.get("chemistryPoints"), "gg": p.get("id"),
                    "added": (p.get("addedToClubAt") or "")[:10] or None, "paid": p.get("purchasedFor"),
                    # ③ 스쿼드·자산 축 — 보유행에서 온다(playerDef가 아니다).
                    "unt": p.get("isUntradeable"), "act": p.get("isInActiveSquad"),
                    "cap": p.get("isCaptain"), "kit": p.get("kitNumber"), "own": p.get("numberOfOwners"),
                    # ② 경기 기록 — 누적값이라 회차 스냅샷으로 쌓는다.
                    "st": {"gp": p.get("gamesPlayed"), "g": p.get("goals"), "a": p.get("assists"),
                           "yc": p.get("yellowCards"), "rc": p.get("redCards"), "ga": p.get("ga"),
                           "lgp": p.get("lifetimeGamesPlayed"), "lg": p.get("lifetimeGoals"),
                           "la": p.get("lifetimeAssists"), "lyc": p.get("lifetimeYellowCards"),
                           "lrc": p.get("lifetimeRedCards")},
                    # ④⑤ 카드 프로필·링크 — `player_card_items`의 **빈 칸만** 채운다(카드 수집기 값을 덮지 않는다).
                    # ⚠️ `six`는 GK면 gkFace* 다 — `player_card_items.pac..phy`는 GK도 **필드 표기**를 쓰므로
                    #    카드 행을 새로 만들 때 그대로 넣으면 안 된다. 그 판정을 여기서 실어 보낸다.
                    "card": {"gk": q.get("position") == 0,
                             "base": q.get("basePlayerEaId"), "url": q.get("url"),
                             "sm": q.get("skillMoves"), "wf": q.get("weakFoot"),
                             "foot": {1: "오른쪽", 2: "왼쪽"}.get(q.get("foot")),
                             "h": q.get("height"), "w": q.get("weight"), "dob": q.get("dateOfBirth"),
                             "nat": nm_of(q.get("nation")), "lg": nm_of(q.get("league")),
                             "club": nm_of(q.get("club")),
                             # ⚠️ 겉모습 축이다(migration 066) — 성능 판단에 쓰지 않는다.
                             #    `is` 대신 원값을 그대로 넘긴다: 없으면 NULL(미수집)로 남겨야 한다.
                             "face": None if q.get("isRealFace") is None else int(q.get("isRealFace")),
                             "rar": nm_of(q.get("rarity")), "rar_ea": (q.get("rarity") or {}).get("eaId")}})
    out.sort(key=lambda r: r["ea"] or 0)
    return out


def slots_of(squad):
    """/api/gg-club/active-squad/ 응답에서 슬롯 리스트만 꺼낸다.
    ⭐ 봉투가 `{data:{data:{activeGroupPositions:[…]}}}`라 --raw-file로 원본을 그대로 먹이면
       리스트가 아니라 dict가 들어온다(2026-09-25 실측). 벗기는 자리를 여기 하나로 둔다."""
    while isinstance(squad, dict):
        squad = squad.get("activeGroupPositions") or squad.get("data") or []
    return squad


def apply_squad(squad, account_id):
    """활성 스쿼드 슬롯 반영. FIELD→XI · SUBSTITUTE→BENCH (기존 표 어휘를 유지한다)."""
    squad = slots_of(squad)
    grp_of = {"FIELD": "XI", "SUBSTITUTE": "BENCH"}
    con = sqlite3.connect(DB)
    con.execute("DELETE FROM fut_squad_slots WHERE account_id=?", (account_id,))
    n = 0
    for s in squad:
        grp = grp_of.get(s.get("group"))
        if grp is None:
            continue
        con.execute("INSERT INTO fut_squad_slots(account_id,grp,idx,ea_item_id,gg_player_id,synced_at)"
                    " VALUES(?,?,?,?,?,?)",
                    (account_id, grp, s.get("positionIdx"), s.get("playerEaId"), s.get("ggClubPlayerId"), TODAY))
        n += 1
    con.commit()
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=f"/tmp/ggclub-{TODAY.replace('-', '')}.json")
    ap.add_argument("--game", default="27")
    ap.add_argument("--apply-squad", action="store_true", help="fut_squad_slots도 갱신한다")
    ap.add_argument("--account-id", type=int, default=1)
    ap.add_argument("--print-snippet", action="store_true", help="토큰 추출 스니펫만 출력하고 끝낸다")
    ap.add_argument("--auth-file", help="토큰 JSON이 든 파일(저장소 밖). 읽는 즉시 삭제한다.")
    ap.add_argument("--raw-file", help="브라우저 안에서 받아 둔 원본 응답 {players,squad} JSON. 토큰 경로를 쓰지 않는다.")
    a = ap.parse_args()

    if a.print_snippet:
        print(SNIPPET)
        return

    # ⭐ 토큰 경로 ⑶ `--raw-file`(2026-09-24 신설) — ⑴⑵가 막혔을 때의 대안이다.
    #    토큰을 페이지 밖(클립보드·환경변수·파일)으로 꺼내는 행위가 정책상 **자격증명 실체화**로 차단되면
    #    브라우저 **안에서** API를 호출해 응답만 꺼내고, 여기서는 그 원본을 먹는다.
    #    ⇒ 토큰은 페이지 스코프를 벗어나지 않고, 행 변환은 그대로 이 모듈(=단일 정본)이 한다.
    if a.raw_file:
        raw = json.loads(Path(a.raw_file).read_text(encoding="utf-8"))
        write_out(rows_of(raw.get("players") or []), raw.get("squad") or [], a, pages="raw")
        return

    # ⭐ 토큰 경로 2개(2026-09-21 확장, 사용자 지시 「그냥 네가 실행하도록 정정해」):
    #    ⑴ `FUTGG_AUTH` 환경변수 — 사람이 쉘에서 직접 돌릴 때.
    #    ⑵ `--auth-file` — **에이전트가 돌릴 때.** 토큰을 명령줄에 박으면 자격증명이 프로세스 목록·
    #       쉘 히스토리에 남고, 그 행위 자체가 차단된다(2026-09-21 실측). 파일로 건네고 **읽는 즉시 지운다**.
    #    ⛔ 어느 경로든 토큰을 저장소 안에 쓰지 않는다 — `--auth-file`은 /tmp 같은 저장소 밖만 받는다.
    raw = os.environ.get("FUTGG_AUTH")
    if not raw and a.auth_file:
        p = Path(a.auth_file).resolve()
        if ROOT in p.parents:
            sys.exit(f"⛔ 토큰 파일이 저장소 안이다({p}) — /tmp 등 저장소 밖에 두라")
        raw = p.read_text(encoding="utf-8").strip()
        try:
            p.unlink()                      # 읽은 즉시 폐기 — 디스크에 남기지 않는다
            print(f"토큰 파일 폐기: {p}")
        except OSError as e:
            print(f"⚠️ 토큰 파일 삭제 실패({e}) — 직접 지울 것: {p}")
    if not raw:
        sys.exit("⛔ 토큰이 없다 — `FUTGG_AUTH` 환경변수나 `--auth-file`을 주라 "
                 "(`--print-snippet`으로 스니펫을 받아 로그인된 탭에서 꺼낸다)")
    headers = json.loads(raw)
    headers.setdefault("Accept", "application/json")
    # ⚠️ 기본 urllib UA로는 403이다(Cloudflare) — 다른 수집기와 같은 UA를 쓴다(2026-09-21 실측).
    headers.setdefault("User-Agent", "Mozilla/5.0")
    headers.setdefault("Origin", "https://www.fut.gg")
    headers.setdefault("Referer", "https://www.fut.gg/gg-club/my/players/")

    players, page = [], 1
    while True:
        d = get(f"{API}/players/?game={a.game}&sorts=-overall&page={page}", headers)
        players += d.get("data") or []
        if not d.get("next"):
            break
        page = d["next"]
        if page > 100:                                    # 폭주 방지
            break

    squad = []
    try:
        squad = (((get(f"{API}/active-squad/", headers) or {}).get("data") or {}).get("data") or {}).get(
            "activeGroupPositions") or []
    except Exception as e:
        print(f"⚠️ 활성 스쿼드 조회 실패({e}) — 선수 목록만 쓴다")

    write_out(rows_of(players), squad, a, pages=page)


def write_out(rows, squad, a, pages):
    squad = slots_of(squad)
    uniq = {r["gg"] for r in rows}
    Path(a.out).write_text(json.dumps(rows, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"수집 {len(rows)}명(고유 {len(uniq)}) · {pages}페이지 · 스쿼드 슬롯 {len(squad)} → {a.out}")
    # ⛔⛔ **결손을 조용히 넘기지 않는다**(2026-09-23 · obs#132). 2026-09-22까지 「프리킥 정확도」가
    #    100% 빠지고 있었는데 아무도 몰랐고, 6대 스탯 PAS가 89명 전원에서 2~4 낮게 계산됐다.
    for miss, n in sorted(MISSING.items(), key=lambda kv: -kv[1]):
        print(f"⚠️ 속성 결손 {n}명 — {', '.join(miss)} (fut.gg 필드명이 바뀌었는지 확인할 것)")
    if len(uniq) != len(rows):
        print(f"⚠️ 중복 {len(rows) - len(uniq)}건 — 응답에 같은 카드가 두 번 들어왔다")
    if a.apply_squad and squad:
        print(f"fut_squad_slots 갱신 {apply_squad(squad, a.account_id)}행")
    print(f"다음: .venv/bin/python scripts/fut_club_sync.py {a.out} --account main")


if __name__ == "__main__":
    main()
