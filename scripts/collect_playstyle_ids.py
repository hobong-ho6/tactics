#!/usr/bin/env python3
"""PlayStyle **숫자 id → 이름** 표를 fut.gg 웹앱 번들에서 받는다 (2026-09-24 신설).

왜 (사용자 지시 2026-09-24 「fut.gg 번들에서 PlayStyle 이름표 받아서 나머지도 채워줘」):
  GG Club API(`playerDef.playstyles`)와 진화 경로가 PlayStyle을 **숫자 id로만** 준다.
  종전에는 `core/export.py`가 `player_evolutions`의 id 배열 ↔ path_json 이름 배열을 **역산**해
  표를 만들었는데, 역산은 **표본이 있는 id만** 채워진다 — 실제로 40종 중 10종이 비어 있었고
  화면에 「PlayStyle #7」이 떴다(2026-09-24 AVL 전수 대조에서 발견).
  ⇒ 번들에 `PLAY_STYLE_LABELS` 상수로 **전종이 박혀 있다**. 역산 대신 이것을 받는다.

⭐ 이름 정본은 **fut.gg 카드 페이지 쪽**이다(`player_card_items.playstyles`) — 화면·비교가 전부
   그 문자열로 붙기 때문이다. 번들 라벨은 일부가 짧다:
     id 7  번들 `Long Ball`      ↔ 카드 `Long Ball Pass`  (카드 29장)
     id 34 번들 `Low Driven`     ↔ 카드 `Low Driven Shot` (카드 21장)
   ⇒ **카드에 실제로 쓰인 이름이 있으면 그것을 쓰고**, 없을 때만 번들 라벨을 쓴다.
   ⛔ 이 우선순위를 뒤집지 말 것 — 뒤집으면 비교 화면의 「상대에게 없는 PlayStyle」 판정이
      같은 스타일을 서로 다른 이름으로 봐서 전부 초록이 된다.

⚠️ 번들 해시는 배포마다 바뀐다 — 홈에서 참조를 먼저 읽는다(collect_chem_styles.py와 같은 경로).

사용:
    .venv/bin/python scripts/collect_playstyle_ids.py
    .venv/bin/python scripts/collect_playstyle_ids.py --dry-run
"""
import argparse
import datetime as dt
import re
import sqlite3
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DB = ROOT / "db" / "tactics.db"

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


def _get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode()


def fetch_labels():
    """번들에서 {id: 라벨}을 뽑는다. enum(`e[e.NAME=ID]=\\`NAME\\``) × 라벨표(`[I.NAME]:\\`Label\\``)."""
    home = _get("https://www.fut.gg/")
    refs = re.findall(r'src="([^"]*index-[^"]*\.js)"', home)
    if not refs:
        raise SystemExit("⛔ 번들 참조를 찾지 못했다 — fut.gg 배포 구조가 바뀌었다")
    url = refs[0] if refs[0].startswith("http") else "https://www.fut.gg" + refs[0]
    js = _get(url)
    enum = {k: int(v) for k, v in re.findall(r"e\[e\.([A-Z_0-9]+)=(\d+)\]=`\1`", js)}
    i = js.find("a_={[I.FINESSE_SHOT]:")          # PLAY_STYLE_LABELS 본체
    end = js.find("},Bme=a_", i)
    if i < 0 or end < 0:
        raise SystemExit("⛔ PLAY_STYLE_LABELS를 찾지 못했다 — 번들 구조가 바뀌었다")
    out = {}
    for name, label in re.findall(r"\[I\.([A-Z_0-9]+)\]:`([^`]+)`", js[i:end]):
        if name in enum:
            out[enum[name]] = label
    return out, url


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="FC27")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    bundle, url = fetch_labels()
    con = sqlite3.connect(DB)
    ours = dict(con.execute("SELECT ea_id, name FROM fc_playstyle_ids WHERE game_version=?", (a.game,)))
    # 카드 페이지에 실제로 쓰인 이름(정본) — `+` 접미는 PlayStyle+ 표기라 떼고 센다.
    used = set()
    for (s,) in con.execute("SELECT playstyles FROM player_card_items WHERE game_version=? AND playstyles<>''", (a.game,)):
        used.update(x.strip().rstrip("+") for x in s.split(",") if x.strip())

    rows, kept = [], []
    for eid, label in sorted(bundle.items()):
        cur = ours.get(eid)
        # ⭐ 카드에 쓰인 이름이 이미 원장에 있으면 **번들 라벨로 덮지 않는다**(위 주석).
        if cur and cur != label and cur in used:
            kept.append((eid, cur, label))
            continue
        name = cur if cur == label else label
        if cur == name:
            continue
        rows.append((a.game, eid, name,
                     f"fut.gg 웹앱 번들 PLAY_STYLE_LABELS ({url.split('/')[-1]}, {a.pulled} 파싱, collect_playstyle_ids.py)",
                     "HIGH — fut.gg가 EA 정의를 그대로 쓴다(등급 B: 번들 상수). "
                     "⚠️ 라벨이 카드 페이지보다 짧을 수 있다 — 카드에 쓰인 이름이 있으면 그쪽이 정본이다.",
                     a.pulled))

    print(f"번들 {len(bundle)}종 · 원장 {len(ours)}종 · 새로 채울 {len(rows)}종")
    for _, eid, name, *_ in rows:
        print(f"   + {eid:>3} {name}")
    for eid, cur, label in kept:
        print(f"   ⭐ {eid:>3} 카드 이름 유지 [{cur}] — 번들 라벨 [{label}]은 짧은 표기")
    missing = sorted(set(ours) - set(bundle))
    if missing:
        print(f"⚠️ 번들에 없는 원장 id {missing} — 구버전 잔재인지 확인할 것(지우지 않는다)")
    if a.dry_run or not rows:
        return
    con.executemany("""INSERT INTO fc_playstyle_ids(game_version, ea_id, name, source, confidence, pulled)
                       VALUES(?,?,?,?,?,?)
                       ON CONFLICT(game_version, ea_id) DO UPDATE SET
                         name=excluded.name, source=excluded.source,
                         confidence=excluded.confidence, pulled=excluded.pulled""", rows)
    con.commit()
    print(f"\n적재 {len(rows)}행 → fc_playstyle_ids")
    print("다음: python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
