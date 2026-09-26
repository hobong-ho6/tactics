#!/usr/bin/env python3
"""진화의 **한국어 이름·설명·과제** 수집 — futmind (2026-09-26 신설, 사용자 질문
   「진화의 한글명도 수집할 수 있어?」 → 가능하다).

어디서: futmind.com이 **EA 공식 현지화 19개 언어**를 그대로 노출한다.
    https://futmind.com/api/evolutions
      → [{ id, locales:{ names:{en,ko,ja,…}, descriptions:{…} },
            levels:[{ objectives:[{ locales:{names:{ko,…}} }] }] }]
  ⛔ fut.gg는 한국어를 주지 않는다(2026-09-26 실측: Accept-Language·?lang=ko·?locale=ko 모두 영어).

⛔⛔ **조인 키가 영문명뿐이다** — futmind id(2730) ↔ fut.gg evo_id(2508)는 다른 체계다.
   불변규칙 6은 라벨 조인을 금하지만 여기는 사람·팀·체제가 아니라 **카탈로그 항목**이고
   다른 키가 존재하지 않는다. ⇒ ⑴ 영문명 중복을 먼저 세고(있으면 멈춘다)
     ⑵ fut.gg 접미 `[SP 7]`·`[SP+ 14]`를 떼어 맞추고 ⑶ 못 맞춘 것은 **NULL로 둔다**.

⚠️ futmind 목록은 24종이라 **시즌패스·목표 해금형이 빠진다**(2026-09-26: 9종). 그건 결손으로 남긴다.
⚠️ 근거 등급 **B** — futmind가 EA 원본이라 밝힌 적은 없다(현지화 문구가 인게임과 일치하는지는 미확인).

사용:
    .venv/bin/python scripts/collect_futmind_kr.py            # 한국어 채우기
    .venv/bin/python scripts/collect_futmind_kr.py --dry-run
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
SRC = "https://futmind.com/api/evolutions"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", "Accept": "application/json"}

# fut.gg가 이름 뒤에 붙이는 해금 표시 — futmind에는 없다.
SUFFIX = re.compile(r"\s*\[SP\+?\s*\d+\]\s*$")
strip = lambda s: SUFFIX.sub("", s or "").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="ko")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    rows = json.load(urllib.request.urlopen(urllib.request.Request(SRC, headers=UA), timeout=40))
    by = {}
    dup = []
    for o in rows:
        en = ((o.get("locales") or {}).get("names") or {}).get("en")
        if not en:
            continue
        k = strip(en)
        if k in by:
            dup.append(k)
        by[k] = o
    if dup:
        raise SystemExit(f"⛔ 영문명이 중복이다 {dup} — 이름 조인이 성립하지 않는다. 멈춘다.")
    print(f"futmind {len(rows)}종 · 영문명 중복 0")

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    pulled = con.execute("SELECT MAX(pulled) FROM fc_evolutions").fetchone()[0]
    ours = con.execute("SELECT evo_id, name FROM fc_evolutions WHERE pulled=?", (pulled,)).fetchall()

    upd, miss, tasks, lvkr = [], [], [], []
    for r in ours:
        o = by.get(strip(r["name"]))
        if not o:
            miss.append(r["name"])
            continue
        L = o.get("locales") or {}
        nm = (L.get("names") or {}).get(a.lang)
        de = (L.get("descriptions") or {}).get(a.lang)
        if nm or de:
            upd.append((nm, de, r["evo_id"], pulled))
        # 단계별 미션 한국어(migration 077) — 영문은 fut.gg `levels[].challenges`에 이미 있다.
        # ⭐ 단계 번호가 맞는다: futmind `level` == fut.gg `idx`(2026-09-26 대조 확인).
        lk = {}
        for lv in (o.get("levels") or []):
            got = []
            for ob in (lv.get("objectives") or []):
                t = ((ob.get("locales") or {}).get("names") or {})
                if t.get("en") and t.get(a.lang):
                    tasks.append((t["en"], t[a.lang]))
                if t.get(a.lang):
                    got.append(t[a.lang])
            if got:
                lk[str(lv.get("level"))] = got
        if lk:
            lvkr.append((json.dumps(lk, ensure_ascii=False), r["evo_id"], pulled))

    print(f"이름·설명 채울 것 {len(upd)}종 · 미매칭 {len(miss)}종")
    if miss:
        print("  ⚠️ 미매칭(해금형이라 futmind 목록에 없다 — 결손으로 남긴다):")
        for m in miss:
            print("     ·", m)
    for nm, de, eid, _ in upd[:8]:
        print(f"  {eid:<6} → {nm}")
    uniq = {e: k for e, k in tasks}
    print(f"과제 문구 한국어 {len(uniq)}종 · 단계별 미션 {len(lvkr)}종")

    if a.dry_run:
        print("\n--dry-run — DB에 쓰지 않았다.")
        return
    con.executemany("UPDATE fc_evolutions SET name_kr=COALESCE(?, name_kr), description_kr=COALESCE(?, description_kr) "
                    "WHERE evo_id=? AND pulled=?", upd)
    con.executemany("UPDATE fc_evolutions SET levels_kr=? WHERE evo_id=? AND pulled=?", lvkr)
    # ⭐ 과제 번역 — 영문이 같으면 같은 번역이다(EA 현지화가 문구 단위라). 빈 칸만 채운다.
    n = 0
    for en, ko in uniq.items():
        n += con.execute("UPDATE fc_objective_tasks SET task_text_kr=? "
                         "WHERE task_text=? AND COALESCE(TRIM(task_text_kr),'')=''", (ko, en)).rowcount
    con.commit()
    print(f"\n적재: 진화 {len(upd)}종 · 단계별 미션 {len(lvkr)}종 · 과제 번역 {n}행")
    print("다음: python3 scripts/export.py")


if __name__ == "__main__":
    main()
