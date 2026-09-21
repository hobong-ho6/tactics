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


def rows_of(players):
    out = []
    for p in players:
        q = p.get("playerDef") or {}
        keys = SIX_GK if q.get("position") == 0 else SIX
        name = q.get("commonName") or f"{q.get('firstName') or ''} {q.get('lastName') or ''}".strip()
        out.append({"ea": q.get("eaId"), "n": name, "ovr": q.get("overall"),
                    "six": [q.get(k) for k in keys],
                    "cs": p.get("chemistryStyle"), "cp": p.get("chemistryPoints"), "gg": p.get("id"),
                    "added": (p.get("addedToClubAt") or "")[:10] or None, "paid": p.get("purchasedFor")})
    out.sort(key=lambda r: r["ea"] or 0)
    return out


def apply_squad(squad, account_id):
    """활성 스쿼드 슬롯 반영. FIELD→XI · SUBSTITUTE→BENCH (기존 표 어휘를 유지한다)."""
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
    a = ap.parse_args()

    if a.print_snippet:
        print(SNIPPET)
        return

    raw = os.environ.get("FUTGG_AUTH")
    if not raw:
        sys.exit("⛔ FUTGG_AUTH 환경변수가 없다 — `--print-snippet`으로 스니펫을 받아 탭에서 토큰을 꺼낼 것")
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

    rows = rows_of(players)
    uniq = {r["gg"] for r in rows}
    Path(a.out).write_text(json.dumps(rows, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"수집 {len(rows)}명(고유 {len(uniq)}) · {page}페이지 · 스쿼드 슬롯 {len(squad)} → {a.out}")
    if len(uniq) != len(rows):
        print(f"⚠️ 중복 {len(rows) - len(uniq)}건 — 응답에 같은 카드가 두 번 들어왔다")
    if a.apply_squad and squad:
        print(f"fut_squad_slots 갱신 {apply_squad(squad, a.account_id)}행")
    print(f"다음: .venv/bin/python scripts/fut_club_sync.py {a.out} --account main")


if __name__ == "__main__":
    main()
