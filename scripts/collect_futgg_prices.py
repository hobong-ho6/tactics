#!/usr/bin/env python3
"""관리 선수 카드 시세 스냅샷 — fut.gg 목록 API (2026-09-18 신설, migration 037).

왜 (사용자 지시 「제한된 자원에서 누구를 먼저 사야 하는지 등 선수 가격 정보까지」):
  구매 우선순위는 처방 역할(전술 필요)과 시세(자원)의 대조다. 시세는 매일 움직이므로 날짜별 스냅샷으로 쌓고
  화면이 최신값을 읽는다. ⛔ 우선순위 판정은 여기서 하지 않는다.

원천(2026-09-27 정정): **`/api/fut/player-prices/{game}/{eaId}/?verify=…`**.
  ⛔⛔ 종전 주석은 「전용 가격 API는 Cloudflare 403이라 쓰지 않는다」였고, 대신 목록 API의
     `currentDbPrice`·`hasPrice`를 읽었다. **그 두 필드는 항상 null/false다** —
     실증: 3회차(09-18·09-19·09-27) 전부 「시세 있음 0장」이었다. 즉 **가격을 한 번도 못 받았다.**
     증상이 고약하다 — 「시장 미형성」이라는 그럴듯한 설명이 붙어 있어 아무도 의심하지 않았다.
  ⭐ 403의 원인은 Cloudflare가 아니라 **서명 누락**이었다. 흐름은 두 단계다:
     ⑴ `POST /api/fut/price-access/sign/` body `{"url": "/api/fut/player-prices/27/{ea}/"}`
        → `{"data": {"url": "<서명이 붙은 경로>", "challengeRequired": false, "expiresIn": 120}}`
     ⑵ 그 **서명된 경로를 그대로** GET 한다. 토큰은 **선수마다 다르고 120초**만 산다
        (다른 선수 id에 재사용하면 403이다 — 실측).
  ⛔⛔ **`challengeRequired`가 true면 멈춘다.** 그건 봇 검사이고, 우회는 하지 않는다.
  ⚠️ 일괄 조회는 없다(`?ea_ids=`는 404) — 선수당 2요청이다. 그래서 기본 대상을
     **보유 카드 + 관리 4팀**으로 좁히고 `--all`로만 전체를 돈다.

⭐⭐ 2026-09-29 동선 재설계(사용자 지시 「클럽 싱크에서 시세 받아오는게 오래걸리고 항상 막히는것 같은데」):
  ⛔ 종전엔 대상 283장 = 566요청을 한 번에 끝내려고 **예산이 빌 때마다 10분씩 잤다**(약 1시간).
     세션의 셸은 10분에 끊기므로 앞에서 부르면 **중간에 죽었고**, 끊긴 회차는 G21(최신 회차가 직전 절반 미만)에
     걸려 **export·ship까지 막혔다** — 「오래 걸린다」와 「항상 막힌다」가 같은 구조에서 나왔다.
  ⇒ ⑴ **보유 거래불가 카드는 대상에서 뺀다** — 팔 수 없고 어느 화면도 그 시세를 쓰지 않는다(283 → 약 100장).
     ⑵ **기본은 예산 한 번만 쓰고 멈춘다**(약 45장 · 1분 안쪽 · 자지 않는다). 오래된 순 정렬이라 회차가 돌아가며 채운다.
     ⑶ export는 **카드별 최신 시세**를 읽는다(core/export.py) — 부분 회차가 나머지 카드 시세를 지우지 않는다.
     ⑷ 그래서 G21 감시 목록에서 이 표를 뺐다(부분 회차가 정상 동작이 됐다).
  `--full`은 종전처럼 기다리며 끝까지 받는다(오래 걸린다 — 백그라운드로 돌릴 것).

사용:
    .venv/bin/python scripts/collect_futgg_prices.py --games 27            # 예산 한 번(~45장) · 기다리지 않음
    .venv/bin/python scripts/collect_futgg_prices.py --games 27 --full     # 대상 전량(기다린다 · 백그라운드)
    .venv/bin/python scripts/collect_futgg_prices.py --games 27 --all      # 카드 표 전체(보유 거래불가 제외는 동일)
    # ⭐ fut.gg가 막혔을 때(2026-11-11) — FUTWIZ 대체 경로(아래 「FUTWIZ 대체 경로」 절)
    .venv/bin/python scripts/collect_futgg_prices.py --futwiz-snippet      # 앱 안 브라우저 futwiz.com 탭에서 돌릴 JS
    .venv/bin/python scripts/collect_futgg_prices.py --futwiz-file /tmp/futwiz-prices-YYYYMMDD.json
"""
import argparse
import datetime as dt
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DB = ROOT / "db" / "tactics.db"
from scripts.collect_futgg_history import API, UA, get   # noqa: E402
import json                                          # noqa: E402
import re                                            # noqa: E402
import time                                          # noqa: E402
import urllib.error                                  # noqa: E402
import urllib.request                                # noqa: E402
from core.db import connect as connect_db  # noqa: E402  ⭐ DB 연결 정본(대기·작성 중 표시)


class Challenge(Exception):
    """⛔ fut.gg가 봇 검사를 요구했다 — **우회하지 않는다**. 호출부가 멈추고 사람에게 보고한다."""


def _blocked(e):
    """⛔ Cloudflare 봇 차단 페이지(403 「Attention Required」)인가 — 2026-09-29 실측.
       서명은 200인데 GET이 전부 이 페이지로 막혔다. **우회하지 않는다** — Challenge로 올려 멈춘다."""
    try:
        body = e.read(4096).decode("utf-8", "ignore").lower()
    except Exception:                                    # noqa: BLE001
        return False
    return "cloudflare" in body and ("attention required" in body or "cf-" in body)


class RateLimited(Exception):
    """⛔⛔ 429 — **더 두드리지 않고 멈춘다**. 재시도로 뚫으려 하지 않는다.
       ⭐ 2026-09-27부터 아래 `Budget`이 **애초에 여기 닿지 않도록** 속도를 죈다 —
          이 예외가 뜨면 그건 「우리 추정 쿼터가 틀렸다」는 신호다(보고할 것)."""


class Exhausted(Exception):
    """⭐ 이번 회차 예산을 다 썼다 — **기다리지 않고 멈춘다**(기본 모드 · 2026-09-29).
       실패가 아니다. 남은 카드는 오래된 순 정렬이라 다음 회차가 이어 받는다."""


class Budget:
    """⭐ 요청 속도를 한 곳에서 죈다 (2026-09-27 사용자 지시 「쿨다운 안 걸리게 수집 주기 조절」).

    ⛔ 종전엔 `time.sleep(0.15)`가 전부라 **초당 13요청**으로 때렸고, 90~126요청마다 429가 났다
       (실측 429 지점: 45·56·58·63장 · 선수당 2요청). 회복은 대략 10분이었다.
    ⇒ fut.gg의 제한은 **미끄러지는 창**으로 보인다 — 「총 몇 장」이 아니라 「최근 N초에 몇 요청」이다.
       그래서 장수를 세는 대신 **요청 시각을 창에 담아** 예산을 넘기면 창이 비는 만큼 기다린다.
    ⚠️ 기본값 90요청/600초는 **실측에서 역산한 추정**이다(공개된 값이 아니다 · 근거 등급 C).
       429가 또 나면 그 사실이 곧 반증이니 `--budget`을 낮춰 잡는다.
    """

    def __init__(self, budget, window, wait=True):
        self.budget, self.window, self.hits, self.wait = budget, window, [], wait

    def take(self):
        now = time.monotonic()
        self.hits = [t for t in self.hits if now - t < self.window]
        if len(self.hits) >= self.budget:
            if not self.wait:
                raise Exhausted()
            wait = self.window - (now - self.hits[0]) + 0.5
            print(f"   ⏳ 예산 소진 — {wait:.0f}초 쉰다(창 {self.window}초에 {self.budget}요청)")
            time.sleep(wait)
            now = time.monotonic()
            self.hits = [t for t in self.hits if now - t < self.window]
        self.hits.append(now)


BUDGET = Budget(90, 600)     # main()이 인자로 덮어쓴다


def signed_price(game, ea):
    """⑴ 서명 받고 ⑵ 서명된 경로를 GET 한다. `(가격객체, 사유)`를 돌려준다.

    ⛔⛔ 종전엔 어떤 실패든 `except Exception: return None`으로 뭉개고, 호출부가 그걸
       **`platform="console"`인 NULL 행**으로 적었다 — 즉 **못 받은 것을 「관측」으로 기록**했다.
       2026-09-27 실측 피해: 그렇게 만들어진 유령 행이 하루 369개였고, 그중 120장은 실제로는
       가격이 있는데 화면에 「미형성」으로 떴다(재조회 표본 6장 중 5장이 200 OK + 정상 가격).
    ⛔⛔ 더 나쁜 것: **서명 POST의 429도 그 자루에 들어갔다.** 429를 올려보내는 건 GET뿐이라
       서명 단계에서 막히면 「조회 실패」로 둔갑했다 — 매 회차 「조회 실패 8장」의 정체가 이것이다
       (속도를 죄자 같은 카드들이 전부 200으로 돌아왔다).
    ⇒ 이제 **사유를 갈라 돌려주고, 못 받은 것은 아무 행도 쓰지 않는다**(호출부가 처리).
       `missing`(404 = fut.gg에 그 카드가 없다 · 영구)과 `fail:*`(일시적 · 재시도 대상)을 구분한다.

    ⚠️ 서명 POST도 요청이다 — 둘 다 예산에서 뺀다(어느 쪽이 세어지는지 모르니 **많은 쪽**을 가정한다).
    """
    BUDGET.take()
    req = urllib.request.Request(
        f"{API}/price-access/sign/", method="POST",
        data=json.dumps({"url": f"/api/fut/player-prices/{game}/{ea}/"}).encode(),
        headers={**UA, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = (json.load(r) or {}).get("data") or {}
    except urllib.error.HTTPError as e:
        if e.code == 429:                       # ⛔ 서명 단계의 429도 429다 — 「조회 실패」로 묻지 않는다
            raise RateLimited(f"sign ea {ea}") from None
        if e.code == 403 and _blocked(e):
            raise Challenge(f"sign ea {ea} — Cloudflare 차단 페이지") from None
        return None, f"fail:sign HTTP {e.code}"
    except Exception as e:
        return None, f"fail:sign {type(e).__name__}"
    if d.get("challengeRequired"):
        raise Challenge(f"ea {ea}")
    if not d.get("url"):
        return None, "fail:sign 응답에 url 없음"
    BUDGET.take()
    try:
        with urllib.request.urlopen(
                urllib.request.Request("https://www.fut.gg" + d["url"], headers=UA), timeout=30) as r:
            return ((json.load(r) or {}).get("data") or {}).get("currentPrice"), "ok"
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise RateLimited(f"ea {ea}") from None
        if e.code == 404:                       # ⭐ fut.gg에 그 카드가 없다 — 재시도해도 같다
            return None, "missing"
        # ⛔⛔ 봇 차단은 카드 탓이 아니다 — 종전엔 「fail:get HTTP 403」으로 카드마다 재시도해
        #    차단된 창구를 회차 내내 두드렸다(2026-09-29 실측: 45장 × 2회 전부 403). 첫 장에서 멈춘다.
        if e.code == 403 and _blocked(e):
            raise Challenge(f"ea {ea} — Cloudflare 차단 페이지") from None
        return None, f"fail:get HTTP {e.code}"
    except Exception as e:
        return None, f"fail:get {type(e).__name__}"


# ── FUTWIZ 대체 경로 (2026-11-11 신설 — 불변규칙 13) ─────────────────────────────────────────────
# 왜: fut.gg 서명 가격 API가 Cloudflare 차단으로 **세 회차 연속**(11-10 오전·저녁 · 11-11 저녁) 막혔다.
#     club-sync 런북은 「같은 축이 두 회차 연속 대체 출처로 넘어가면 스크립트에 대체 경로를 넣는다」고 한다.
#     FUTWIZ는 앱 안 브라우저에서 봇 검사 없이 열린다(2026-10-22·11-06·11-11 실측) — SBC 포메이션과 같은 동선이다
#     (collect_futbin_sbc_formations.py --futwiz-snippet → --futwiz-file).
# ⭐ 조인은 **EA id로만** 한다. FUTWIZ 카드 페이지의 `definitionid`(= JSON-LD `mpn`)가 EA 아이템 id다
#    — 2026-11-11 실측: 쇠를로트 base 216549 · 잭슨 TOTW 67368061 · 잭슨 상위 버전 84145277 모두 우리 ea_item_id와 같다.
#    FUTWIZ 페이지 번호(line_id)는 FUTWIZ 자체 id다. 그걸 찾으려고 이름으로 **검색은** 하지만, 적재는
#    페이지의 mpn이 우리 ea_item_id와 **같을 때만** 한다(이름은 후보를 좁히는 데만 쓴다 — 불변규칙 6).
# ⭐⭐ fut.gg 시세와 **섞지 않는다** — `platform='futwiz-console'`로 적는다. platform은 UNIQUE 키에 들어 있어
#    같은 날 두 출처 행이 서로를 덮을 수 없고(같은 값을 쓰면 fut.gg의 ON CONFLICT가 FUTWIZ 행 가격만 바꿔
#    source는 FUTWIZ로 남는 **출처 위장**이 생긴다), 추세·비교는 같은 platform끼리만 하면 된다.
#    momentum은 비운다(FUTWIZ 변동률은 fut.gg momentum과 같은 정의가 아니다). source는 「FUTWIZ」로 시작한다.
#    export는 같은 날이면 fut.gg 행을 먼저 고른다(core/export.py).
# ⛔ 봇 검사가 뜨면 멈추고 보고한다 — 우회하지 않는다. 서버 액션은 FUTWIZ 화면의 검색창이 부르는 그 자동완성이다.
FW_PLATFORM = "futwiz-console"
FW_PLATFORM_LIKE = "futwiz%"
FW_URL_RE = re.compile(r"https://www\.futwiz\.com/fc27/player/[a-z0-9-]+/\d+")
FW_CONF = ("MEDIUM — FUTWIZ 카드 페이지 콘솔 BIN(등급 B · 3자 사이트 집계). ⛔ fut.gg 시세와 다른 출처다 — "
           "추세·비교는 같은 platform(futwiz-console)끼리만. price 없음은 미형성이지 0원이 아니다.")
# ⚠️ 두 번에 나눠 부른다(① 시작 → ② 결과 읽기) — 카드당 페이지 1~3장(장당 약 1.2MB)이라 한 번 평가로는 길다.
FW_SNIPPET = r"""window.__fwPrices = {progress: 0}; (async () => {
  // ⛔ 앱 안 브라우저의 https://www.futwiz.com/fc27/players 탭에서 실행한다(봇 검사 없음 · 같은 출처 fetch).
  const T = __TARGETS__;
  const out = {cards: {}, action: null, total: T.length, progress: 0};
  window.__fwPrices = out;
  const sleep = ms => new Promise(x => setTimeout(x, ms));
  // FUTWIZ 검색창의 자동완성(서버 액션 autocompleteFutSearch) id — 배포마다 바뀌므로 지금 로드된 청크에서 찾는다.
  for (const s of [...document.scripts].map(s => s.src).filter(s => s.includes('/_next/'))) {
    try {
      const m = (await (await fetch(s)).text()).match(/createServerReference\)\("([0-9a-f]+)",[^)]*?"autocompleteFutSearch"\)/);
      if (m) { out.action = m[1]; break; }
    } catch (e) {}
  }
  const slug = n => n.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  const seen = {};                                   // EA id → 읽은 카드(같은 선수의 다른 버전 재사용)
  const read = async path => {
    await sleep(250);                                // 예의상 간격 — 실제로 받을 때만 쉰다
    const r = await fetch(path);
    if (!r.ok) return null;
    const h = (await r.text()).replace(/\\"/g, '"');
    const id = h.match(/"sku":"(\d+)","mpn":"(\d+)"/);          // sku = FUTWIZ line_id · mpn = EA 아이템 id
    if (!id) return null;
    const m = h.match(new RegExp('"prices":\\{"console":(\\{"line_id":' + id[1] + ',[^}]*\\}),"pc":'));
    const p = m ? JSON.parse(m[1]) : {};
    const c = {ea: +id[2], line: +id[1], url: 'https://www.futwiz.com' + new URL(r.url).pathname,
               bin: p.bin ?? null, src: p.price_source ?? null, upd: p.last_update ?? null};
    seen[c.ea] = c;
    return c;
  };
  const found = {};                                  // 검색어 → 결과(같은 선수의 여러 카드가 같은 검색을 한다)
  const search = async q => {
    if (found[q]) return found[q];
    await sleep(250);
    const r = await fetch('/fc27/players', {method: 'POST', body: JSON.stringify([q, '27']),
                                           headers: {Accept: 'text/x-component', 'next-action': out.action}});
    const l = (await r.text()).split('\n').find(x => x.startsWith('1:'));
    return (found[q] = l ? JSON.parse(l.slice(2)) : []);
  };
  for (const [n, c] of T.entries()) {
    out.progress = n;
    let hit = seen[c.ea] || null, why = 'NOTFOUND';
    const cand = [];                                 // 못 찾았을 때 FUTWIZ 후보의 EA id — 진단용(재발행 id 50331648+base 등)
    try {
      if (!hit && c.url) { const r = await read(c.url.replace('https://www.futwiz.com', '')); if (r && r.ea === c.ea) hit = r; }
      if (!hit && !out.action) why = 'NOACTION';
      if (!hit && out.action) {
        let res = await search(c.q);
        if (!res.length && c.q.includes(' ')) res = await search(c.q.split(' ').slice(-1)[0]);  // 결과 0일 때만 성으로
        res = [...res].sort((a, b) => (b.rating === c.ovr) - (a.rating === c.ovr));         // OVR 같은 후보부터
        for (const p of res.slice(0, 8)) {
          const r = Object.values(seen).find(x => x.line === p.line_id)
                    || await read(`/fc27/player/${slug(p.common_name)}/${p.line_id}`).catch(() => null);
          if (r && r.ea === c.ea) { hit = r; break; }
          cand.push(r ? r.ea : 'p' + p.line_id);
        }
      }
    } catch (e) { why = 'ERR ' + e; }
    out.cards[c.ea] = hit ? {url: hit.url, bin: hit.bin, src: hit.src, upd: hit.upd} : {miss: why, cand};
  }
  out.progress = T.length;
  out.done = 1;
})(); 'started'"""
FW_READ = ("(o => o.done ? JSON.stringify(o) : `진행 ${o.progress}/${o.total}`)(window.__fwPrices)"
           "   // done:1 이 보이면 끝 — 이 문자열을 그대로 파일에 쓴다")


def futwiz_snippet(con, gv, all_=False, limit=None):
    """FUTWIZ 스니펫 대상 — `[{ea, q, ovr, url}]`. q는 fut.gg 카드 URL의 영문 slug(검색어일 뿐 — 조인 키 아님)."""
    known = {}
    for ea, src in con.execute("""SELECT ea_item_id, source FROM player_card_prices
                                  WHERE game_version=? AND platform=? ORDER BY pulled""", (gv, FW_PLATFORM)):
        m = FW_URL_RE.search(src or "")
        if m:
            known[ea] = m.group(0)            # 지난 회차에 찾은 FUTWIZ 페이지 — 검색 없이 바로 읽는다
    out, skip = [], []
    for ea, _ in targets(con, gv, all_):
        url_, name, ovr, pname = con.execute(
            """SELECT i.futgg_url, i.name_kr, i.ovr, p.name FROM player_card_items i
               LEFT JOIN players p ON p.id=i.player_id WHERE i.game_version=? AND i.ea_item_id=?""", (gv, ea)).fetchone()
        m = re.search(r"/players/\d+-([a-z0-9-]+)/", url_ or "")
        # ⚠️ fut.gg slug가 「unknown-player」인 카드가 있다(2026-11-11 실측 2장) — 그땐 우리 영문 이름으로 찾는다.
        q = m.group(1).replace("-", " ") if m and m.group(1) != "unknown-player" else None
        q = q or pname or (name if name and name.isascii() else None)
        if not q:
            skip.append(ea); continue
        out.append({"ea": ea, "q": q, "ovr": ovr, "url": known.get(ea)})
    if limit:
        out = out[:limit]
    return out, skip


def futwiz_load(con, gv, raw, pulled):
    """스니펫 결과를 `player_card_prices`에 적는다. **mpn = ea_item_id인 카드만** 들어온다(스니펫이 이미 걸렀다 — 여기서 한 번 더)."""
    if isinstance(raw, str):
        raw = json.loads(raw)
    if not raw.get("done"):
        raise SystemExit("⛔ `done`이 없다 — 스니펫이 아직 끝나지 않았다. 잠시 뒤 ②를 다시 읽을 것")
    if not raw.get("action"):
        print("   ⚠️ FUTWIZ 자동완성 id를 못 찾았다 — 지난 회차에 찾은 페이지만 읽었다. "
              "https://www.futwiz.com/fc27/players 탭에서 돌렸는지 확인할 것")
    pid = dict(targets(con, gv, all_=True))
    rows, miss, stale, nobin, diag = [], {}, 0, 0, []
    now = dt.datetime.now().timestamp()
    for k, c in (raw.get("cards") or {}).items():
        ea = int(k)
        if "miss" in c or not FW_URL_RE.fullmatch(c.get("url") or ""):
            why = c.get("miss", "URL")
            miss[why] = miss.get(why, 0) + 1
            if c.get("cand"):
                diag.append(f"{ea} → FUTWIZ 후보 EA id {c['cand']}")
            continue
        if ea not in pid:
            miss["카드 표에 없는 EA id"] = miss.get("카드 표에 없는 EA id", 0) + 1; continue
        bin_ = c.get("bin") or None
        nobin += bin_ is None
        upd = c.get("upd")
        when = dt.datetime.fromtimestamp(upd).strftime("%Y-%m-%d %H:%M") if upd else "미상"
        if upd and now - upd > 3 * 86400:
            stale += 1
        rows.append((gv, ea, pid[ea], bin_, 1 if bin_ else 0, None, FW_PLATFORM,
                     f"FUTWIZ 카드 페이지 prices.console.bin ({c['url']} · mpn=EA {ea} · FUTWIZ 갱신 {when} · "
                     f"price_source={c.get('src')} · {pulled}, collect_futgg_prices.py --futwiz-file)",
                     FW_CONF, pulled))
    con.executemany("""INSERT INTO player_card_prices(game_version, ea_item_id, player_id, price, has_price, momentum, platform,
                         source, confidence, pulled) VALUES(?,?,?,?,?,?,?,?,?,?)
                       ON CONFLICT(game_version, ea_item_id, platform, pulled) DO UPDATE SET
                         price=excluded.price, has_price=excluded.has_price, source=excluded.source""", rows)
    con.commit()
    n = len(raw.get("cards") or {})
    print(f"{gv} FUTWIZ: 대상 {n}장 → {len(rows)}행 적재(platform {FW_PLATFORM}) · 시세 있음 {len(rows) - nobin}장 · "
          f"BIN 없음 {nobin}장 · 못 찾음 {n - len(rows)}장 (pulled {pulled})")
    for r, c in sorted(miss.items(), key=lambda kv: -kv[1]):
        print(f"   ⚠️ {r}: {c}장")
    if diag:
        print("   ℹ️ 못 찾은 카드의 FUTWIZ 후보(같은 선수 다른 EA id — 적재하지 않았다 · 50331648+base는 EA 재발행 id):")
        for d in diag[:15]:
            print(f"      {d}")
    if stale:
        print(f"   ⚠️ FUTWIZ 갱신이 3일 넘은 카드 {stale}장 — 값은 적었고 갱신 시각은 source에 있다")
    print(f"   종료 보고에 「시세 FUTWIZ {len(rows)}/{n}장(fut.gg 차단 대체)」이라고 적는다.")


def targets(con, gv, all_=False):
    """시세 대상 카드 `[(ea_item_id, player_id)]` — fut.gg·FUTWIZ 두 경로가 **같은 대상**을 쓰게 한 곳에 둔다."""
    # ⭐ 선수당 2요청이고 **한 회차 약 50장이 한도**다(429). 그래서:
    #   ⑴ 기본 대상은 **보유 + 관리 4팀**(`--all`이면 전체)
    #   ⑵ 정렬은 **가장 오래 전에 가격을 받은 순** — 회차를 나눠 돌면 전원이 차례로 갱신된다.
    #   ⛔ ea_item_id 순으로 두면 앞쪽 50장만 영원히 갱신되고 뒤는 **영영 안 받는다**.
    #   ⭐ 「받은 날」은 **fut.gg 행으로만** 센다(2026-11-11) — FUTWIZ 대체 행이 fut.gg 순번을 밀어내지 않게.
    scope = ("" if all_ else
             " AND (i.ea_item_id IN (SELECT ea_item_id FROM fut_club_players WHERE status='owned')"
             "      OR i.player_id IN (SELECT se.player_id FROM squad_entries se"
             "                           JOIN regimes g ON g.id=se.regime_id))")
    # ⭐ 보유 **거래불가** 카드는 뺀다(2026-09-29) — 팔 수 없고, 화면은 미보유 카드 시세만 쓴다(구매 우선순위).
    #    같은 아이템을 거래 가능으로도 들고 있으면 남긴다(그건 팔 수 있다).
    scope += (" AND i.ea_item_id NOT IN (SELECT ea_item_id FROM fut_club_players"
              "                          WHERE status='owned' AND is_untradeable=1"
              "                            AND ea_item_id NOT IN (SELECT ea_item_id FROM fut_club_players"
              "                                                   WHERE status='owned' AND COALESCE(is_untradeable,0)=0))")
    return con.execute(
        "SELECT i.ea_item_id, i.player_id FROM player_card_items i"
        " WHERE i.game_version=?" + scope +
        " ORDER BY COALESCE((SELECT MAX(p.pulled) FROM player_card_prices p"
        "                     WHERE p.ea_item_id=i.ea_item_id AND p.price IS NOT NULL"
        "                       AND p.platform NOT LIKE ?), '0000'),"
        "          i.ea_item_id", (gv, FW_PLATFORM_LIKE)).fetchall()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", nargs="*", default=["27"])
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--all", action="store_true", help="카드 표 전체(느리다 — 선수당 2요청)")
    ap.add_argument("--budget", type=int, default=90, help="창 안에서 허용할 요청 수(기본 90)")
    ap.add_argument("--window", type=int, default=600, help="예산을 세는 창(초 · 기본 600)")
    ap.add_argument("--refresh", action="store_true",
                    help="오늘 이미 받은 카드도 다시 받는다(기본은 건너뛴다 — 예산을 아낀다)")
    ap.add_argument("--limit", type=int, help="앞에서 N장만(속도 조절 확인용)")
    ap.add_argument("--full", action="store_true",
                    help="예산이 비면 기다리며 대상 전량을 받는다(오래 걸린다 — 백그라운드로). 기본은 예산 한 번 쓰고 멈춘다")
    ap.add_argument("--futwiz-snippet", action="store_true",
                    help="⭐ fut.gg 차단 시 대체 — 앱 안 브라우저 futwiz.com/fc27/players 탭에서 돌릴 JS를 찍는다")
    ap.add_argument("--futwiz-file", help="FUTWIZ 스니펫 결과 JSON 파일을 적재한다(platform futwiz-console)")
    a = ap.parse_args()
    if a.futwiz_snippet or a.futwiz_file:
        con = connect_db(DB)
        gv = f"FC{a.games[0]}"
        if a.futwiz_file:
            futwiz_load(con, gv, json.load(open(a.futwiz_file)), a.pulled)
            print("\n다음: python3 scripts/export.py && scripts/db_dump.sh")
            return
        tg, skip = futwiz_snippet(con, gv, a.all, a.limit)
        out = f"/tmp/futwiz-prices-{a.pulled.replace('-', '')}.json"
        known = sum(1 for t in tg if t["url"])
        print(f"// 대상 {len(tg)}장(지난 회차에 찾은 FUTWIZ 페이지 {known}장 · 나머지는 검색으로 찾는다)"
              + (f" · 검색어 없음 {len(skip)}장 제외" if skip else ""))
        print("// ① 시작 — 앱 안 브라우저에서 https://www.futwiz.com/fc27/players 를 연 탭에서 실행\n"
              + FW_SNIPPET.replace("__TARGETS__", json.dumps(tg, ensure_ascii=False)))
        print("\n// ② 몇 분 뒤 결과 읽기(진행 중이면 「진행 n/N」)\n" + FW_READ)
        print(f"\n── 셸 ── (② 결과 JSON 문자열을 {out}에 쓴 뒤)\n"
              f".venv/bin/python scripts/collect_futgg_prices.py --futwiz-file {out}")
        return
    global BUDGET
    BUDGET = Budget(a.budget, a.window, wait=a.full)
    con = connect_db(DB)
    for g in a.games:
        gv = f"FC{g}"
        items = targets(con, gv, a.all)
        pid = dict(items)
        ids = [i for i, _ in items]
        # ⭐ 오늘 이미 받은 카드는 건너뛴다(2026-09-27) — 이어 돌릴 때 **예산을 이미 끝낸 카드에 쓰던** 것을 막는다.
        #    실증: 391장이 끝난 상태에서 45장을 더 받았는데 새로 채워진 건 2장뿐이었다.
        if not a.refresh:
            done = {e for (e,) in con.execute(
                "SELECT ea_item_id FROM player_card_prices WHERE game_version=? AND pulled=? AND platform NOT LIKE ?",
                (gv, a.pulled, FW_PLATFORM_LIKE))}
            skipped = len(ids)
            ids = [e for e in ids if e not in done]
            skipped -= len(ids)
            if skipped:
                print(f"   ↪️ 오늘 이미 받은 {skipped}장은 건너뛴다(--refresh로 강제)")
        if a.limit:
            ids = ids[:a.limit]
        if ids:
            need = len(ids) * 2
            if a.full:
                mins = max(0, (need - a.budget)) / a.budget * (a.window / 60)
                print(f"   ⏱️ {len(ids)}장 = {need}요청 · 예산 {a.budget}/{a.window}초 → 약 {mins:.0f}분 예상"
                      f"{' — 백그라운드로 돌리는 편이 낫다' if mins > 5 else ''}")
            else:
                print(f"   ⏱️ 대상 {len(ids)}장 중 이번 회차는 예산 {a.budget}요청(약 {a.budget // 2}장)까지 — "
                      "기다리지 않는다. 나머지는 다음 회차가 오래된 순으로 이어 받는다(--full이면 끝까지)")
        rows, priced, failed, limited, spent, blocked = [], 0, 0, False, False, None
        done_n = 0
        why = {}
        for n, ea in enumerate(ids, 1):
            try:
                cur, reason = signed_price(g, ea)   # Challenge는 잡지 않는다 — 위로 올려 멈춘다
                if cur is None and reason.startswith("fail:"):
                    # ⭐ 일시적 실패는 한 번 다시 묻는다 — 실측상 대부분 그 다음에 200이다.
                    time.sleep(2)
                    cur, reason = signed_price(g, ea)
            except RateLimited:
                limited = True
                print(f"   ⛔ 429 — {n-1}장에서 레이트 리밋. **여기서 멈춘다**(재시도로 뚫지 않는다).")
                break
            except Exhausted:
                spent = True
                break
            except Challenge as e:
                # ⛔ 우회하지 않는다. 받은 만큼은 적고(아래 INSERT) 멈춘 뒤 비정상 종료로 알린다.
                blocked = str(e)
                break
            done_n = n
            if cur is None:
                # ⛔⛔ **못 받았으면 아무 행도 쓰지 않는다.** 종전엔 여기서 platform을 `console`로
                #    지어내 NULL 행을 남겼고, 그게 화면에 「미형성」으로 떴다(2026-09-27 · 유령 행 369개).
                #    없는 값은 없는 대로 두고 다음 회차가 다시 받는다.
                failed += 1
                why[reason] = why.get(reason, 0) + 1
                continue
            price = cur.get("price")
            # ⭐ `isExtinct`(멸종)는 **가격 없음과 다르다** — 값이 없지만 「시장에 없다」는 사실이다.
            has = 1 if price else 0
            priced += has
            mom = cur.get("priceChangePercentage") or cur.get("momentumPercentage")
            rows.append((gv, ea, pid.get(ea), price, has, mom, cur.get("platform") or "ps5",
                         f"fut.gg {API}/player-prices/{g}/{ea}/ (서명 조회 · {a.pulled}, collect_futgg_prices.py)",
                         "MEDIUM — fut.gg 집계 시세. price 없음은 **미형성/멸종**이지 0원이 아니다.", a.pulled))
            # ⛔ 여기서 sleep 하지 않는다 — 속도는 `Budget`이 정본이다(두 곳에 두면 갈린다).
            if n % 50 == 0:
                print(f"   … {n}/{len(ids)} (시세 {priced} · 실패 {failed})")
        con.executemany("""INSERT INTO player_card_prices(game_version, ea_item_id, player_id, price, has_price, momentum, platform,
                             source, confidence, pulled) VALUES(?,?,?,?,?,?,?,?,?,?)
                           ON CONFLICT(game_version, ea_item_id, platform, pulled) DO UPDATE SET
                             price=excluded.price, has_price=excluded.has_price, momentum=excluded.momentum""", rows)
        con.commit()
        left = len(ids) - done_n
        print(f"{gv}: 대상 {len(ids)}장 중 {done_n}장 조회 → {len(rows)}행 적재 · 시세 있음 {priced}장 · "
              f"미형성/멸종 {len(rows) - priced}장 · 못 받음 {failed}장 (pulled {a.pulled})")
        # ⭐ 사유를 찍는다 — 종전엔 전부 「조회 실패 N장」이라 **무엇이 막혔는지 알 수 없었다**.
        for r, c in sorted(why.items(), key=lambda kv: -kv[1]):
            tag = "ℹ️ fut.gg에 없는 카드(영구)" if r == "missing" else "⚠️"
            print(f"   {tag} {r}: {c}장")
        if blocked:
            print(f"   ⛔⛔ fut.gg가 봇 차단(Cloudflare)을 걸었다 — {blocked}. **여기서 멈췄다**(우회하지 않는다)."
                  "\n      재시도·헤더 변경으로 뚫지 않는다. 시간을 두고 다음 회차에 다시 본다 — 화면은 카드별 최신 시세를 그대로 쓴다."
                  "\n      ⭐ 대체: FUTWIZ — `collect_futgg_prices.py --futwiz-snippet` → 앱 안 브라우저 futwiz.com 탭 → `--futwiz-file`"
                  "\n      (그것도 안 되면 종료 보고에 「시세 수집 차단(Cloudflare)」이라고 적는다).")
            BLOCKED[0] = True
        if spent and left:
            print(f"   ↪️ 이번 회차 예산을 다 썼다 — 남은 {left}장은 **다음 회차**가 오래된 순으로 받는다."
                  f"\n      종료 보고에 「시세 {done_n}/{len(ids)}장」이라고 적는다. 화면은 카드별 최신 시세를 쓴다.")
        if limited:
            con2 = con.execute("SELECT COUNT(*) FROM player_card_items WHERE game_version=?", (gv,)).fetchone()[0]
            print(f"   ⚠️ 레이트 리밋으로 이번 회차는 여기까지다 — **다음 회차가 오래된 순으로 이어 받는다.**"
                  f"\n      종료 보고에 「시세 N/{len(ids)}장까지」라고 적는다(전체 카드 {con2}장).")
        # ⛔ 「받을 게 없었다」와 「받았는데 0장이었다」는 다르다 — 앞의 것에 경고를 붙이면
        #    진짜 고장 신호가 무뎌진다(2026-09-27 건너뛰기 도입 직후 거짓 경보로 확인).
        if priced == 0 and rows:
            print("   ⛔ **시세가 한 장도 안 잡혔다** — 「시장 미형성」으로 넘기지 말 것. "
                  "서명 흐름이 또 막힌 것일 수 있다(2026-09-27에 같은 증상으로 3회차를 날렸다).")
    print("\n다음: python3 scripts/export.py && scripts/db_dump.sh")
    if BLOCKED[0]:
        sys.exit(2)          # ⭐ 실행기(club_sync.py)가 「실패 — 원인 보고」로 멈추게 한다


BLOCKED = [False]

if __name__ == "__main__":
    main()
