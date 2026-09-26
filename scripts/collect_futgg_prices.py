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
    """⛔⛔ 429 — **더 두드리지 않고 멈춘다**(2026-09-27 실측: 한 회차에 약 50장이 한도다).
       재시도로 뚫으려 하지 않는다. 남은 선수는 다음 회차가 **오래된 순으로** 이어 받는다."""


def signed_price(game, ea):
    """⑴ 서명 받고 ⑵ 서명된 경로를 GET 한다. 실패는 None(=조회 못 함)이고 **0원이 아니다**."""
    req = urllib.request.Request(
        f"{API}/price-access/sign/", method="POST",
        data=json.dumps({"url": f"/api/fut/player-prices/{game}/{ea}/"}).encode(),
        headers={**UA, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = (json.load(r) or {}).get("data") or {}
    except Exception:
        return None
    if d.get("challengeRequired"):
        raise Challenge(f"ea {ea}")
    if not d.get("url"):
        return None
    try:
        with urllib.request.urlopen(
                urllib.request.Request("https://www.fut.gg" + d["url"], headers=UA), timeout=30) as r:
            return ((json.load(r) or {}).get("data") or {}).get("currentPrice")
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise RateLimited(f"ea {ea}") from None
        return None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", nargs="*", default=["27"])
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--all", action="store_true", help="카드 표 전체(느리다 — 선수당 2요청)")
    a = ap.parse_args()
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
        ids = [i for i, _ in items]
        pid = dict(items)
        rows, priced, failed, limited = [], 0, 0, False
        for n, ea in enumerate(ids, 1):
            try:
                cur = signed_price(g, ea)           # Challenge는 잡지 않는다 — 위로 올려 멈춘다
            except RateLimited:
                limited = True
                print(f"   ⛔ 429 — {n-1}장에서 레이트 리밋. **여기서 멈춘다**(재시도로 뚫지 않는다).")
                break
            if cur is None:
                failed += 1
                price, has, mom = None, 0, None
            else:
                price = cur.get("price")
                # ⭐ `isExtinct`(멸종)는 **가격 없음과 다르다** — 값이 없지만 「시장에 없다」는 사실이다.
                has = 1 if price else 0
                priced += has
                mom = cur.get("priceChangePercentage") or cur.get("momentumPercentage")
            rows.append((gv, ea, pid.get(ea), price, has, mom, (cur or {}).get("platform") or "console",
                         f"fut.gg {API}/player-prices/{g}/{ea}/ (서명 조회 · {a.pulled}, collect_futgg_prices.py)",
                         "MEDIUM — fut.gg 집계 시세. price 없음은 **미형성/멸종**이지 0원이 아니다.", a.pulled))
            time.sleep(0.15)                        # ⚠️ 선수당 2요청이다 — 남의 서버를 배려한다
            if n % 50 == 0:
                print(f"   … {n}/{len(ids)} (시세 {priced} · 실패 {failed})")
        con.executemany("""INSERT INTO player_card_prices(game_version, ea_item_id, player_id, price, has_price, momentum, platform,
                             source, confidence, pulled) VALUES(?,?,?,?,?,?,?,?,?,?)
                           ON CONFLICT(game_version, ea_item_id, platform, pulled) DO UPDATE SET
                             price=excluded.price, has_price=excluded.has_price, momentum=excluded.momentum""", rows)
        con.commit()
        print(f"{gv}: 카드 {len(ids)}장 조회 → {len(rows)}행 적재 · 시세 있음 {priced}장 · "
              f"미형성/멸종 {len(rows) - priced - failed}장 · 조회 실패 {failed}장 (pulled {a.pulled})")
        if limited:
            con2 = con.execute("SELECT COUNT(*) FROM player_card_items WHERE game_version=?", (gv,)).fetchone()[0]
            print(f"   ⚠️ 레이트 리밋으로 이번 회차는 여기까지다 — **다음 회차가 오래된 순으로 이어 받는다.**"
                  f"\n      종료 보고에 「시세 N/{len(ids)}장까지」라고 적는다(전체 카드 {con2}장).")
        if priced == 0:
            print("   ⛔ **시세가 한 장도 안 잡혔다** — 「시장 미형성」으로 넘기지 말 것. "
                  "서명 흐름이 또 막힌 것일 수 있다(2026-09-27에 같은 증상으로 3회차를 날렸다).")
    print("\n다음: python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
