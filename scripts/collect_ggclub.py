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
⚠️ 토큰 수명은 약 1시간이다(JWT exp). 만료되면 404가 나므로 다시 꺼낸다.

⭐⭐ **에이전트는 `--print-snippet` → `--raw-file` 경로를 쓴다**(2026-09-26 완성본화).
   토큰을 클립보드·파일·환경변수로 꺼내는 코드는 정책상 「자격증명 실체화」로 차단된다(2026-09-24 실측).
   ⇒ 토큰을 **꺼내지 말고** 브라우저 안에서 다 쓰고, **응답만** 꺼낸다.
   ⛔ 종전엔 `--print-snippet`이 **헤더만** 돌려줬고 수집 코드는 세션마다 손으로 다시 썼다.
      그때마다 쿼리 파라미터(`?game=…&sorts=…`)를 빠뜨리거나 「끝 신호 404」를 오류로 읽었다
      (2026-09-26에 그 둘로 4회를 허비했다). ⇒ 이제 스니펫이 **수집·COPY 버튼까지 끝낸다.**

    .venv/bin/python scripts/collect_ggclub.py --print-snippet   # 스니펫 + 뒷 절차가 같이 나온다

사람이 쉘에서 직접 돌릴 때의 토큰 경로도 그대로 남아 있다:

    FUTGG_AUTH='<헤더 JSON>' .venv/bin/python scripts/collect_ggclub.py --apply-squad

── 출력 ──────────────────────────────────────────────────────────────────────
`fut_club_sync.py`가 먹는 형식으로 파일을 쓴다:
    [{"ea","n","ovr","six":[6],"cs","cp","gg","added","paid"}, ...]
`--apply-squad`면 `fut_squad_slots`(XI 11 + BENCH 12)도 갱신한다.
표준출력은 **요약 몇 줄뿐** — 선수 데이터는 절대 찍지 않는다(그게 이 스크립트의 존재 이유다).

사용:
    .venv/bin/python scripts/collect_ggclub.py --print-snippet            # ⭐ 에이전트는 이것
    .venv/bin/python scripts/collect_ggclub.py --raw-file /tmp/… --apply-squad
    FUTGG_AUTH='…' .venv/bin/python scripts/collect_ggclub.py --apply-squad
    .venv/bin/python scripts/collect_ggclub.py --auth-file /tmp/ggauth.json --apply-squad
"""
import argparse
import datetime as dt
import json
import os
import sqlite3
import sys
import time
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

# ⭐⭐ 목록 URL은 **여기 하나뿐이다**(2026-09-26 · 단일 정본).
#    ⛔ 쿼리를 빼면 404다 — `?game=…&sorts=-overall&page=…`가 전부 필수다.
#       2026-09-26에 런북의 스니펫 예시가 `?page=N`만 적고 있어서 404를 「토큰 만료」로 오판해 4회를 허비했다.
#    ⇒ 파이썬 경로와 브라우저 스니펫이 **같은 문자열에서 만들어진다** — 한쪽만 고쳐질 여지를 없앤다.
PLAYERS_URL = "/players/?game={game}&sorts=-overall&page={page}"

# ⭐⭐⭐ 404가 **세 가지**다(2026-09-26 실측). 구분하지 않으면 정상을 오류로, 오류를 정상으로 읽는다:
#    ⑴ **마지막 페이지 다음** — 179명 = 6페이지고 7페이지가 404다. 즉 404는 「끝」 신호이기도 하다.
#    ⑵ **간헐 404** — 같은 URL·같은 헤더가 200과 404를 오간다(워밍업·X-Session-Cache-Key와 무관하게
#       재현됐다). 한 번 맞고 포기하면 **1페이지에서 죽어** 「토큰 만료」로 오진한다.
#    ⑶ **진짜 인증 실패** — 토큰 수명 약 1시간.
#    ⇒ 판정 규칙을 하나로 둔다: **페이지마다 RETRY회까지 재시도하고, 그래도 404면
#      1페이지는 인증 실패 · 2페이지 이후는 끝.** 양쪽(파이썬·스니펫)에 같은 규칙을 심는다.
RETRY = 4
RETRY_MS = 800

# 로그인된 GG Club 탭에서 실행 → ⑴ Authorization 헤더를 가로채고 ⑵ **그 자리에서 전량 수집**해
# ⑶ `window.__ggPayload`에 담고 ⑷ COPY 버튼을 띄운다. 헤더는 페이지 밖으로 나가지 않는다.
# ⛔ 손으로 조립할 자리를 남기지 않는다 — 종전엔 헤더만 돌려주고 수집 코드를 세션마다 다시 썼고,
#    그때마다 쿼리 파라미터·404 판정을 틀렸다(2026-09-26).
SNIPPET = r"""
(async () => {
  const of_ = window.__ggOf || window.fetch; window.__ggOf = of_;
  let hdr = null;
  // ① 헤더 가로채기 — SPA 이동이 일어나야 호출이 난다. **현재와 다른** /gg-club/ 경로여야 한다.
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
    const cur = location.pathname;
    const a = [...document.querySelectorAll('a')].find(x => {
      const h = x.getAttribute('href') || '';
      return h.startsWith('/gg-club/') && h !== cur && !h.includes('?');
    });
    if (a) a.click();
    setTimeout(res, 8000);
  });
  window.fetch = of_;
  if (!hdr) return 'NO_AUTH_HEADER — 로그인된 /gg-club/…/players/ 에서 실행했는지 확인';

  // ② 같은 페이지 안에서 전량 수집. ⛔ 헤더는 여기서만 쓰고 밖으로 내보내지 않는다.
  //    ⚠️ 404는 세 가지다 — 끝 · 간헐 · 인증 실패. __RETRY__회 재시도한 뒤에 판정한다.
  const players = [];
  let page = 1, end = null, retried = 0;
  while (page <= 100) {
    let arr = null, last = 0;
    for (let t = 0; t < __RETRY__; t++) {
      const r = await of_('/api/gg-club/players/?game=__GAME__&sorts=-overall&page=' + page, {headers: hdr});
      last = r.status;
      if (r.ok) { const j = await r.json(); arr = j.data || j.results || []; break; }
      if (r.status !== 404) break;                            // 404 아닌 오류는 재시도하지 않는다
      retried++;
      await new Promise(x => setTimeout(x, __RETRY_MS__));
    }
    if (arr === null) {
      if (last !== 404) { hdr = null; return 'API_' + last + '@page' + page; }
      if (page === 1) { hdr = null; return 'AUTH_404 — 1페이지가 __RETRY__회 모두 404다. 토큰 만료·로그인 풀림'; }
      end = '404@' + page; break;                             // ⭐ 마지막 페이지 다음 = 끝
    }
    if (!arr.length) { end = 'empty@' + page; break; }
    players.push(...arr);
    page++;
  }
  const sr = await of_('/api/gg-club/active-squad/', {headers: hdr});
  const squad = sr.ok ? await sr.json() : null;
  hdr = null;                                                 // ⛔ 토큰 폐기 — 반환값에 섞이지 않게

  // ③ 페이로드 보관 + COPY 버튼. ⚠️ navigator.clipboard는 패널에서 막히므로 execCommand만 쓴다.
  window.__ggPayload = JSON.stringify({players, squad});
  document.getElementById('ggCopyBtn')?.remove();
  const b = document.createElement('button');
  b.id = 'ggCopyBtn';
  b.textContent = 'COPY';
  b.style.cssText = 'position:fixed;top:120px;left:20px;z-index:2147483647;width:220px;height:70px;'
                  + 'font-size:28px;background:#e11;color:#fff;border:0;cursor:pointer';
  b.onclick = () => {
    const ta = document.createElement('textarea');
    ta.value = window.__ggPayload || '';
    ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0';
    document.body.appendChild(ta);
    ta.select();
    const ok = document.execCommand('copy');
    ta.remove();
    b.textContent = ok ? 'OK ' + (window.__ggPayload || '').length : 'FAIL';
  };
  document.body.appendChild(b);
  // ⛔ 선수 데이터는 반환하지 않는다 — 요약만 낸다(그게 이 경로의 존재 이유다).
  return JSON.stringify({players: players.length, pages: page - 1, end, retried,
                         squad: !!squad, bytes: window.__ggPayload.length});
})()
"""

# 페이지를 치우는 스니펫 — 수집이 끝나면 버튼과 페이로드를 지운다(런북 §2-4 ⑸).
CLEANUP_SNIPPET = r"""
document.getElementById('ggCopyBtn')?.remove(); delete window.__ggPayload;
JSON.stringify({btn: !!document.getElementById('ggCopyBtn'), payload: !!window.__ggPayload})
"""


def get(url, headers, end_on_404=False):
    """⚠️ 404는 세 가지다(위 RETRY 주석) — 끝 · 간헐 · 인증 실패.
    간헐 404는 여기서 재시도로 흡수하고, 남은 404의 해석만 호출부가 한다
    (`end_on_404=True` = 목록 2페이지 이후 → 「끝」)."""
    req = urllib.request.Request(url, headers=headers)
    for t in range(RETRY):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
            if t < RETRY - 1:
                time.sleep(RETRY_MS / 1000)
    if end_on_404:
        return None                               # 끝 — 오류가 아니다
    sys.exit(f"⛔ 404 — {RETRY}회 모두 404다. 토큰이 만료됐거나 헤더가 빠졌다(수명 약 1시간).\n"
             "   (목록 2페이지 이후의 404라면 그건 「마지막 페이지 다음」이라 정상이다)")


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
    ap.add_argument("--print-snippet", action="store_true",
                    help="브라우저 안에서 **전량 수집까지 끝내는** 스니펫을 출력하고 끝낸다(손조립 불필요)")
    ap.add_argument("--auth-file", help="토큰 JSON이 든 파일(저장소 밖). 읽는 즉시 삭제한다.")
    ap.add_argument("--raw-file", help="브라우저 안에서 받아 둔 원본 응답 {players,squad} JSON. 토큰 경로를 쓰지 않는다.")
    a = ap.parse_args()

    if a.print_snippet:
        # ⭐ `--game`이 스니펫 안으로 그대로 흘러간다 — 두 곳에 같은 버전을 적을 자리를 없앤다.
        raw_out = a.out.replace("ggclub-", "ggclub-raw-")
        print(SNIPPET.replace("__GAME__", a.game)
                     .replace("__RETRY_MS__", str(RETRY_MS))     # ⚠️ __RETRY__보다 먼저 — 접두가 겹친다
                     .replace("__RETRY__", str(RETRY)))
        print("── 이 뒤는 셸에서 ─────────────────────────────────────────────")
        print("# ⑴ 위를 로그인된 /gg-club/…/players/ 탭에서 실행 → 요약 JSON이 나오고 COPY 버튼이 뜬다")
        print("# ⑵ COPY 버튼을 **실제 마우스로** 클릭(합성 이벤트는 false를 뱉는다)")
        print(f"LANG=en_US.UTF-8 pbpaste > {raw_out}")
        print(f".venv/bin/python scripts/collect_ggclub.py --raw-file {raw_out} --apply-squad")
        print("printf '' | pbcopy      # 클립보드 비우기")
        print("# ⑶ 페이지 치우기 — 아래를 같은 탭에서 실행")
        print(CLEANUP_SNIPPET.strip())
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
    while page <= 100:                                    # 폭주 방지
        d = get(API + PLAYERS_URL.format(game=a.game, page=page), headers, end_on_404=page > 1)
        if d is None:                                     # ⭐ 마지막 페이지 다음의 404 = 정상 종료
            page -= 1
            break
        players += d.get("data") or []
        if not d.get("next"):
            break
        page = d["next"]

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
