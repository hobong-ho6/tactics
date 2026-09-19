#!/usr/bin/env python3
"""6대 스탯 구성식(개별 속성 → PAC/SHO/… 가중) 수집 — fut.gg 웹앱 번들 파싱 (2026-09-19 신설).

왜 (사용자 지시 「붙인 후 스탯의 변경도 볼수있게」): 케미 스타일 부스트는 **개별 속성**에만 들어온다.
「PAC가 몇으로 오르나」를 말하려면 6대 스탯이 개별 속성을 어떤 가중으로 합치는지 알아야 한다.
EA는 공개하지 않고, fut.gg 번들이 그 표(`facePace: 가속 .45 + 질주 .55` …)를 갖고 있다.

⚠️ 계산 규칙도 번들과 같게 쓴다: `min(99, floor(Σ 가중×속성 + 0.501))`.
"""
import argparse, datetime as dt, json, re, sqlite3, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DB = ROOT / "db" / "tactics.db"
from scripts.collect_futgg_history import ATTR_MAP  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0"}


def _get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode()


def parse():
    home = _get("https://www.fut.gg/")
    ref = re.findall(r'src="([^"]*index-[^"]*\.js)"', home)[0]
    js = _get(ref if ref.startswith("http") else "https://www.fut.gg" + ref)
    out = []
    # {label:`Pace`,abbreviation:`PAC`,key:`facePace`,attributes:[{label:…,key:`attributeX`,weight:.45},…]}
    # ⚠️ 항목마다 shortLabel 같은 선택 키가 끼어든다(PHY가 그랬다 — 첫 수집에서 통째로 빠졌다).
    #    abbreviation과 key 사이에 무엇이 오든 받아들인다.
    for m in re.finditer(r"abbreviation:`([A-Z]{3})`,[^\[]*?key:`(\w+)`,attributes:\[(.*?)\]\}", js):
        abbr, key, body = m.group(1), m.group(2), m.group(3)
        for a in re.finditer(r"key:`(\w+)`,weight:([\d.]+)", body):
            out.append((key, abbr, 1 if key.startswith("gk") else 0, a.group(1), float(a.group(2))))
    return out, ref


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="FC27")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    a = ap.parse_args()
    rows, ref = parse()
    con = sqlite3.connect(DB)
    n, skip = 0, []
    for key, abbr, is_gk, attr_en, w in rows:
        kr = ATTR_MAP.get(attr_en)
        if not kr:
            skip.append(attr_en); continue
        con.execute("""INSERT INTO fc_face_stats(game_version, face_key, abbr, is_gk, attr, weight, pulled, source, confidence)
                       VALUES(?,?,?,?,?,?,?,?,?)
                       ON CONFLICT(game_version, face_key, attr) DO UPDATE SET weight=excluded.weight, pulled=excluded.pulled""",
                    (a.game, key, abbr, is_gk, kr, w, a.pulled,
                     f"fut.gg 웹앱 번들 6대 스탯 구성식 ({ref.split('/')[-1]}, {a.pulled} 파싱)",
                     "HIGH — 게임 표기와 일치하는 구성식. ⚠️ EA 1차 공개가 아니라 fut.gg 구현을 읽은 것"))
        n += 1
    con.commit()
    print(f"적재 {n}행" + (f" · 매핑 없는 속성 {sorted(set(skip))}" if skip else ""))
    for r in con.execute("SELECT abbr, group_concat(attr||' '||weight, ' + ') FROM fc_face_stats WHERE game_version=? GROUP BY abbr ORDER BY is_gk, abbr", (a.game,)):
        print(f"  {r[0]:<4} {r[1]}")


if __name__ == "__main__":
    main()
