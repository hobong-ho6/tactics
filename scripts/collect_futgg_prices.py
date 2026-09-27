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

사용:
    .venv/bin/python scripts/collect_futgg_prices.py --games 27
    .venv/bin/python scripts/collect_futgg_prices.py --games 27 --all      # 카드 표 전체
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
import time                                          # noqa: E402
import urllib.error                                  # noqa: E402
import urllib.request                                # noqa: E402


class Challenge(Exception):
    """⛔ fut.gg가 봇 검사를 요구했다 — **우회하지 않는다**. 호출부가 멈추고 사람에게 보고한다."""


class RateLimited(Exception):
    """⛔⛔ 429 — **더 두드리지 않고 멈춘다**. 재시도로 뚫으려 하지 않는다.
       ⭐ 2026-09-27부터 아래 `Budget`이 **애초에 여기 닿지 않도록** 속도를 죈다 —
          이 예외가 뜨면 그건 「우리 추정 쿼터가 틀렸다」는 신호다(보고할 것)."""


class Budget:
    """⭐ 요청 속도를 한 곳에서 죈다 (2026-09-27 사용자 지시 「쿨다운 안 걸리게 수집 주기 조절」).

    ⛔ 종전엔 `time.sleep(0.15)`가 전부라 **초당 13요청**으로 때렸고, 90~126요청마다 429가 났다
       (실측 429 지점: 45·56·58·63장 · 선수당 2요청). 회복은 대략 10분이었다.
    ⇒ fut.gg의 제한은 **미끄러지는 창**으로 보인다 — 「총 몇 장」이 아니라 「최근 N초에 몇 요청」이다.
       그래서 장수를 세는 대신 **요청 시각을 창에 담아** 예산을 넘기면 창이 비는 만큼 기다린다.
    ⚠️ 기본값 90요청/600초는 **실측에서 역산한 추정**이다(공개된 값이 아니다 · 근거 등급 C).
       429가 또 나면 그 사실이 곧 반증이니 `--budget`을 낮춰 잡는다.
    """

    def __init__(self, budget, window):
        self.budget, self.window, self.hits = budget, window, []

    def take(self):
        now = time.monotonic()
        self.hits = [t for t in self.hits if now - t < self.window]
        if len(self.hits) >= self.budget:
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
        return None, f"fail:get HTTP {e.code}"
    except Exception as e:
        return None, f"fail:get {type(e).__name__}"


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
    a = ap.parse_args()
    global BUDGET
    BUDGET = Budget(a.budget, a.window)
    con = sqlite3.connect(DB)
    for g in a.games:
        gv = f"FC{g}"
        # ⭐ 선수당 2요청이고 **한 회차 약 50장이 한도**다(429). 그래서:
        #   ⑴ 기본 대상은 **보유 + 관리 4팀**(`--all`이면 전체)
        #   ⑵ 정렬은 **가장 오래 전에 가격을 받은 순** — 회차를 나눠 돌면 전원이 차례로 갱신된다.
        #   ⛔ ea_item_id 순으로 두면 앞쪽 50장만 영원히 갱신되고 뒤는 **영영 안 받는다**.
        scope = ("" if a.all else
                 " AND (i.ea_item_id IN (SELECT ea_item_id FROM fut_club_players WHERE status='owned')"
                 "      OR i.player_id IN (SELECT se.player_id FROM squad_entries se"
                 "                           JOIN regimes g ON g.id=se.regime_id))")
        items = con.execute(
            "SELECT i.ea_item_id, i.player_id FROM player_card_items i"
            " WHERE i.game_version=?" + scope +
            " ORDER BY COALESCE((SELECT MAX(p.pulled) FROM player_card_prices p"
            "                     WHERE p.ea_item_id=i.ea_item_id AND p.price IS NOT NULL), '0000'),"
            "          i.ea_item_id", (gv,)).fetchall()
        pid = dict(items)
        ids = [i for i, _ in items]
        # ⭐ 오늘 이미 받은 카드는 건너뛴다(2026-09-27) — 이어 돌릴 때 **예산을 이미 끝낸 카드에 쓰던** 것을 막는다.
        #    실증: 391장이 끝난 상태에서 45장을 더 받았는데 새로 채워진 건 2장뿐이었다.
        if not a.refresh:
            done = {e for (e,) in con.execute(
                "SELECT ea_item_id FROM player_card_prices WHERE game_version=? AND pulled=?", (gv, a.pulled))}
            skipped = len(ids)
            ids = [e for e in ids if e not in done]
            skipped -= len(ids)
            if skipped:
                print(f"   ↪️ 오늘 이미 받은 {skipped}장은 건너뛴다(--refresh로 강제)")
        if a.limit:
            ids = ids[:a.limit]
        if ids:
            need = len(ids) * 2
            mins = max(0, (need - a.budget)) / a.budget * (a.window / 60)
            print(f"   ⏱️ {len(ids)}장 = {need}요청 · 예산 {a.budget}/{a.window}초 → 약 {mins:.0f}분 예상"
                  f"{' — 백그라운드로 돌리는 편이 낫다' if mins > 5 else ''}")
        rows, priced, failed, limited = [], 0, 0, False
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
        print(f"{gv}: 카드 {len(ids)}장 조회 → {len(rows)}행 적재 · 시세 있음 {priced}장 · "
              f"미형성/멸종 {len(rows) - priced}장 · 못 받음 {failed}장 (pulled {a.pulled})")
        # ⭐ 사유를 찍는다 — 종전엔 전부 「조회 실패 N장」이라 **무엇이 막혔는지 알 수 없었다**.
        for r, c in sorted(why.items(), key=lambda kv: -kv[1]):
            tag = "ℹ️ fut.gg에 없는 카드(영구)" if r == "missing" else "⚠️"
            print(f"   {tag} {r}: {c}장")
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


if __name__ == "__main__":
    main()
