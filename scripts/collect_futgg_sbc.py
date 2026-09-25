#!/usr/bin/env python3
"""SBC(스쿼드 빌딩 챌린지) 수집 — fut.gg (2026-09-25 신설, 사용자 지시 「sbc 정보도 가져오자」).

어디서:
    세트 목록   https://www.fut.gg/api/fut/sbc/?page=N
    세트 상세   https://www.fut.gg/api/fut/sbc/challenge/{challengeEaId}/   → 세트 + 챌린지 전부

⚠️⚠️ **요구 조건은 사람이 읽는 문장으로만 온다**(`requirementsText`) — 구조화된 조건이 아니다.
   ⇒ 원문을 그대로 넣는다. 파싱은 판정 스크립트(`scripts/sbc_solve.py`)가 하고,
     못 읽은 문장은 거기서 「판정 불가」로 남긴다. ⛔ 여기서 파싱 결과로 원문을 대체하지 않는다.

⛔ 만료된 세트도 지우지 않는다 — `is_expired`로 뒤집고 행은 남긴다(진화 카탈로그와 같은 규약).
   회차 스냅샷(`pulled`)이라 과거 조건을 되돌아볼 수 있다.

사용:
    .venv/bin/python scripts/collect_futgg_sbc.py
    .venv/bin/python scripts/collect_futgg_sbc.py --dry-run
"""
import argparse
import datetime as dt
import json
import sqlite3
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DB = ROOT / "db" / "tactics.db"

API = "https://www.fut.gg/api/fut"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", "Accept": "application/json"}
# fut.gg 카테고리 id → 표기. ⚠️ 목록 화면 탭과 대조해 확정(2026-09-25 실측: 5=foundations · 4는 미관측).
CATEGORY = {1: "players", 2: "upgrades", 3: "challenges", 5: "foundations"}


def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except Exception as e:
            if i == tries - 1:
                raise
            print(f"  ⚠️ 재시도 {i + 1}/{tries} ({type(e).__name__}) {url}")
            time.sleep(1.5)


def awards_of(obj):
    """보상 표기 — 팩·선수·코인·진화가 섞여 온다. 사람이 읽을 문자열로 줄여 담는다."""
    out = []
    for a in (obj.get("awards") or []):
        bits = [a.get("pack"), a.get("evolutionName"),
                (a.get("player") or {}).get("commonName") if isinstance(a.get("player"), dict) else None,
                f"{a['coins']} 코인" if a.get("coins") else None, a.get("other")]
        nm = " · ".join(str(b) for b in bits if b)
        if nm:
            out.append({"name": nm, "count": a.get("count"), "untradeable": a.get("isUntradeable")})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="FC27")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    sets, page = [], 1
    while True:
        d = get(f"{API}/sbc/?page={page}")
        sets += d.get("data") or []
        if not d.get("next"):
            break
        page = d["next"]
    print(f"세트 {len(sets)}개")

    # 세트 상세는 **챌린지 id로** 부른다(세트 id로는 404). 세트마다 첫 챌린지 하나면 전부 딸려 온다.
    set_rows, ch_rows, no_ch = [], [], []
    for s in sets:
        ids = s.get("challengeEaIds") or []
        detail = None
        if ids:
            try:
                detail = get(f"{API}/sbc/challenge/{ids[0]}/")["data"]
            except Exception as e:
                print(f"  ⚠️ 세트 '{s.get('name')}' 상세 실패({type(e).__name__})")
        src = f"fut.gg {API}/sbc/ + /sbc/challenge/ ({a.pulled} 수집, collect_futgg_sbc.py)"
        set_rows.append((a.game, s["eaId"], a.pulled, s.get("name"), s.get("slug"), s.get("description"),
                         CATEGORY.get(s.get("categoryEaId")) or str(s.get("categoryEaId") or ""),
                         s.get("endTime"), int(bool(s.get("isExpired"))),
                         int(bool(s.get("isRepeatable"))), s.get("repeatabilityMode"), s.get("numberOfRepeats"),
                         s.get("repeatRefreshIntervalText"), s.get("challengesCount"),
                         json.dumps(awards_of(s), ensure_ascii=False), s.get("url"), src,
                         "HIGH — fut.gg가 EA 정의를 그대로 노출한다. ⚠️ 기간제 — end_time 이후는 사실이 아니다."))
        chs = (detail or {}).get("challenges") or []
        if not chs:
            no_ch.append(s.get("name"))
        for c in chs:
            ch_rows.append((a.game, s["eaId"], c["eaId"], a.pulled, c.get("name"), c.get("description"),
                            c.get("challengeType"), c.get("eligibilityOperation"),
                            json.dumps(c.get("requirementsText") or [], ensure_ascii=False),
                            json.dumps(awards_of(c), ensure_ascii=False),
                            c.get("cheapestSolutionPrice") or None, src,
                            "HIGH — 조건은 fut.gg 원문 그대로. ⚠️ 최저가는 fut.gg 계산이지 우리 판정이 아니다."))
        time.sleep(0.15)

    print(f"챌린지 {len(ch_rows)}개 · 조건 문장 "
          f"{sum(len(json.loads(r[8])) for r in ch_rows)}개")
    if no_ch:
        print(f"⚠️ 챌린지를 못 받은 세트 {len(no_ch)}개: {', '.join(no_ch)}")
    exp = sum(1 for r in set_rows if r[8])
    print(f"만료 {exp}세트 · 진행 {len(set_rows) - exp}세트")
    if a.dry_run:
        print("\n--dry-run — DB에 쓰지 않았다.")
        return

    con = sqlite3.connect(DB)
    con.executemany("""INSERT INTO fc_sbc_sets(game_version,set_ea_id,pulled,name,slug,description,category,
                         end_time,is_expired,is_repeatable,repeatability_mode,number_of_repeats,
                         repeat_refresh_text,challenges_count,awards_text,url,source,confidence)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                       ON CONFLICT(game_version,set_ea_id,pulled) DO UPDATE SET
                         name=excluded.name, category=excluded.category, end_time=excluded.end_time,
                         is_expired=excluded.is_expired, awards_text=excluded.awards_text,
                         challenges_count=excluded.challenges_count, source=excluded.source""", set_rows)
    con.executemany("""INSERT INTO fc_sbc_challenges(game_version,set_ea_id,challenge_ea_id,pulled,name,description,
                         challenge_type,eligibility_op,requirements_text,awards_text,cheapest_price,source,confidence)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                       ON CONFLICT(game_version,challenge_ea_id,pulled) DO UPDATE SET
                         requirements_text=excluded.requirements_text, awards_text=excluded.awards_text,
                         cheapest_price=excluded.cheapest_price""", ch_rows)
    con.commit()
    print(f"\n적재: 세트 {len(set_rows)} · 챌린지 {len(ch_rows)}")
    print("다음: .venv/bin/python scripts/sbc_solve.py")


if __name__ == "__main__":
    main()
