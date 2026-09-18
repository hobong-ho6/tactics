#!/usr/bin/env python3
"""케미스트리 스타일 24종의 **개별 속성 부스트**를 수집한다 (2026-09-19 신설).

왜 (사용자 지시 2026-09-19 「선수에게 부여할 호크나 엔진 이런 케미」):
  스타일 추천을 하려면 「SHO +3」 같은 6대 스탯 요약으로는 부족하다. 우리 역할 가중
  (`game_role_key_attrs`)이 **개별 속성**(결정력·시야·스탠딩 태클…) 단위라, 같은 +3이라도
  그 역할에 쓰이는 속성인지 아닌지가 갈린다. 그래서 개별 속성 표가 필요하다.

어디서:
  EA도 fut.gg API도 이 표를 주지 않는다. fut.gg 웹앱 번들(index-*.js) 안에 `CHEMISTRY_STYLES`
  상수로 박혀 있어 그것을 파싱한다. ⚠️ 번들 해시는 배포마다 바뀌므로 홈에서 참조를 먼저 읽는다.
  ⚠️ 2차 소스(fifauteam·realsport 요약표)와 방향이 일치하는지 눈으로 확인했다 — Sniper=슈팅+피지컬,
     Finisher=슈팅+드리블(FC26에서 뒤집힌 배치)까지 일치한다.

사용:
    .venv/bin/python scripts/collect_chem_styles.py            # FC27로 적재
    .venv/bin/python scripts/collect_chem_styles.py --dry-run
"""
import argparse
import datetime as dt
import json
import re
import sqlite3
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DB = ROOT / "db" / "tactics.db"

from scripts.collect_futgg_history import ATTR_MAP  # noqa: E402  같은 한글 속성 라벨을 쓴다

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


def _get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode()


def fetch_styles():
    home = _get("https://www.fut.gg/")
    refs = re.findall(r'src="([^"]*index-[^"]*\.js)"', home)
    if not refs:
        raise SystemExit("번들 참조를 찾지 못했다 — fut.gg 배포 구조가 바뀌었다")
    js = _get(refs[0] if refs[0].startswith("http") else "https://www.fut.gg" + refs[0])
    enum = {k: int(v) for k, v in re.findall(r"e\[e\.([A-Z_]+)=(\d+)\]", js)}
    m = re.search(r"\[\{id:\w+\.BASIC,name:", js)
    if not m:
        raise SystemExit("CHEMISTRY_STYLES 배열을 찾지 못했다")
    i, depth = m.start(), 0
    for k in range(i, len(js)):                      # 대괄호 균형으로 배열 끝을 찾는다
        depth += (js[k] == "[") - (js[k] == "]")
        if depth == 0:
            end = k + 1
            break
    src = js[i:end]
    src = re.sub(r"\w+\.([A-Z_]+)", lambda x: str(enum.get(x.group(1), 0)), src)
    src = src.replace("`", '"').replace("!0", "true").replace("!1", "false")
    src = re.sub(r"([{,])\s*([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', src)
    return json.loads(src), refs[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="FC27")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    styles, bundle = fetch_styles()
    con = sqlite3.connect(DB)
    rows = []
    for s in styles:
        boosts, unknown = {}, []
        for b in s["boosts"]:
            kr = ATTR_MAP.get(b["attribute"])
            (boosts.setdefault(kr, b["value"]) if kr else unknown.append(b["attribute"]))
        if unknown:
            print(f"  ⚠️ {s['name']}: 매핑 없는 속성 {unknown} — 추천 계산에서 빠진다")
        rows.append((a.game, s["id"], s["name"], 1 if s.get("isGk") else 0,
                     json.dumps(boosts, ensure_ascii=False), a.pulled,
                     f"fut.gg 웹앱 번들 CHEMISTRY_STYLES ({bundle.split('/')[-1]}, {a.pulled} 파싱, collect_chem_styles.py)",
                     "HIGH — 게임 클라이언트 값과 같은 표. ⚠️ EA 1차 공개가 아니라 fut.gg 구현을 읽은 것이다"))
        print(f"  {s['name']:<10} {'GK' if s.get('isGk') else '  '} " +
              " · ".join(f"{k}+{v}" for k, v in sorted(boosts.items(), key=lambda x: -x[1])[:4]))
    if a.dry_run:
        print(f"\n(dry-run) {len(rows)}종")
        return
    con.executemany("""INSERT INTO fc_chemistry_styles(game_version, style_id, name, is_gk, boosts, pulled, source, confidence)
                       VALUES(?,?,?,?,?,?,?,?)
                       ON CONFLICT(game_version, style_id) DO UPDATE SET
                         boosts=excluded.boosts, pulled=excluded.pulled, source=excluded.source""", rows)
    con.commit()
    print(f"\n적재 {len(rows)}종 ({a.game})")


if __name__ == "__main__":
    main()
