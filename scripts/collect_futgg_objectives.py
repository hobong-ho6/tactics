#!/usr/bin/env python3
"""FC 목표(Objectives) 과제 수집 — fut.gg 목표 페이지 (2026-09-22 신설).

왜: `fc_evolutions.unlock_text`는 **과제 이름만** 들고 있다(예: 「Pep's Domination」).
    「그래서 뭘 하면 되나」는 매번 fut.gg를 봐야 했다 — 사용자 질문에서 드러난 구멍이다.
    ⇒ 목표 그룹 페이지의 과제(이름·조건·보상)를 적재해 진화 카드가 같이 띄운다.

⛔ API가 없다 — `/api/fut/objectives/…`는 전부 404다(2026-09-22 실측).
   목표 페이지는 **서버 렌더(RSC)**라 HTML 본문에 값이 그대로 박혀 있고, 태그를 지우면
   `|과제명|조건|보상|` 꼴로 깔끔하게 끊긴다. 그걸 읽는다.
⚠️ 목록 페이지 HTML에는 `<a href>`가 없지만 **RSC 페이로드에 경로 문자열이 남아 있어** 정규식으로 잡힌다.
⚠️ 기간제다 — 스냅샷으로 적재하고 지난 회차를 덮지 않는다(불변규칙 2).
"""
import argparse, datetime as dt, html, re, sqlite3, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "db" / "tactics.db"
BASE = "https://www.fut.gg"
UA = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en"}


def fetch(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(1.5 * (i + 1))
    return None


def strip_tags(s):
    return html.unescape(re.sub(r"\|+", "|", re.sub(r"<[^>]+>", "|", s)))


def parse_group(page):
    """그룹 페이지 → [(과제명, 조건, 보상)]. 조건 문장은 마침표로 끝나는 안내문만 취한다."""
    txt = strip_tags(page)
    parts = [p.strip() for p in txt.split("|")]
    out, i = [], 0
    while i + 2 < len(parts):
        name, desc, rew = parts[i], parts[i + 1], parts[i + 2]
        # 조건 문장은 「… in the …」처럼 문장으로 끝난다. 과제명은 짧고 마침표가 없다.
        # ⛔ 페이지 제목(「… - EA SPORTS FC 27 Objectives」)과 푸터(「2026 | Stormstrike Inc. …」)가
        #    같은 3칸 모양이라 과제로 잡힌다(2026-09-22 실측). 둘 다 이름으로 걸러낸다.
        junk = ("EA SPORTS FC" in name or re.fullmatch(r"\d{4}", name) or rew in {"About"}
                or "All rights reserved" in desc)
        if (not junk and name and desc and 2 <= len(name) <= 60 and not name.endswith(".")
                and desc.endswith(".") and 15 <= len(desc) <= 300 and rew and len(rew) <= 80):
            out.append((name, desc, rew))
            i += 3
            continue
        i += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="FC27")
    ap.add_argument("--pulled", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    idx = fetch(f"{BASE}/objectives/")
    if not idx:
        sys.exit("목록 페이지 조회 실패")
    groups = sorted(set(re.findall(r"/objectives/([a-z-]+)/(\d+-[a-z0-9-]+)/", idx)))
    print(f"목표 그룹 {len(groups)}개")

    rows = []
    for cat, slug in groups:
        page = fetch(f"{BASE}/objectives/{cat}/{slug}/")
        if not page:
            print(f"  ⚠️ 조회 실패 {cat}/{slug}")
            continue
        m = re.search(r"<title>([^<]+)</title>", page)
        gname = html.unescape(m.group(1)).split(" - ")[0] if m else slug
        for name, desc, rew in parse_group(page):
            # ⛔ 그룹 이름과 같은 줄은 **그룹 소개문**이지 과제가 아니다 — 넣으면 해금 조건 조회가 그걸 집는다
            #    (2026-09-22 실증: Believe 진화가 Ted Lasso 그룹 소개문을 조건으로 띄웠다).
            if name.strip() == gname.strip():
                continue
            rows.append((a.game, f"{cat}/{slug}", gname, cat, name, desc, rew))
        time.sleep(0.3)
    print(f"과제 {len(rows)}개 수집")

    con = sqlite3.connect(DB)
    # 진화가 실제로 참조하는 과제만 보고한다 — 나머지는 조용히 적재한다(나중에 새 진화가 걸릴 수 있다).
    want = {r[0] for r in con.execute(
        "SELECT unlock_text FROM fc_evolutions WHERE unlock_text IS NOT NULL AND unlock_text<>''")}
    # ⚠️ 해금 문구가 **과제 이름**일 때도 있고 **그룹 이름**일 때도 있다
    #    (Pinged Pass → 과제 「Pep's Domination」 · Believe → 그룹 「Ted Lasso's Masterclass」).
    #    둘 다 맞춰 본다 — 한쪽만 보면 절반을 놓친다(2026-09-22 실측).
    hit = [r for r in rows if r[4] in want or r[2] in want]
    print(f"  그중 진화 해금과 이름이 맞는 것 {len(hit)}개:")
    for r in hit:
        via = "과제" if r[4] in want else f"그룹 「{r[2]}」"
        print(f"    ⭐ [{via}] {r[4]}  ←  {r[5]}  (보상 {r[6]})")
    miss = want - {r[4] for r in rows} - {r[2] for r in rows}
    if miss:
        print(f"  ⚠️ 과제를 못 찾은 해금 문구 {len(miss)}개(목표가 아니라 SBC·시즌패스일 수 있다): {', '.join(sorted(miss))}")

    if a.dry_run:
        print("(dry-run) 적재 안 함")
        return
    src = f"fut.gg 목표 페이지 HTML ({a.pulled} 수집, collect_futgg_objectives.py)"
    conf = ("HIGH — fut.gg가 EA 목표를 그대로 노출한다. ⚠️ 기간제라 pulled 시점의 사실이다. "
            "⚠️ 조건 문장은 원문 그대로이고 한국어 번역은 사람이 채운다(task_text_kr).")
    # ⭐ 원문이 같은 과제의 한국어 번역은 직전 회차에서 **이어받는다**(2026-09-25 신설).
    #    회차마다 행이 새로 생기므로 이월하지 않으면 손으로 채운 번역이 매번 사라지고
    #    화면(최신 pulled만 내보낸다)에서 번역이 통째로 빠진다 — 09-22·23·24 세 회차 모두 손으로 다시 채웠다.
    #    ⚠️ 이어받는 기준은 **원문(task_text)이 글자까지 같을 때**뿐이다. 원문이 바뀌면 번역도 다시 해야 한다.
    kr = {t: k for t, k in con.execute(
        """SELECT task_text, task_text_kr FROM fc_objective_tasks
           WHERE task_text_kr IS NOT NULL AND task_text_kr<>'' AND pulled<?
           ORDER BY pulled""", (a.pulled,))}
    n = 0
    for gv, slug, gname, cat, name, desc, rew in rows:
        cur = con.execute(
            """INSERT INTO fc_objective_tasks(game_version,group_slug,group_name,group_category,
               task_name,task_text,task_text_kr,reward,source,confidence,pulled)
               VALUES(?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(game_version,group_slug,task_name,pulled) DO NOTHING""",
            (gv, slug, gname, cat, name, desc, kr.get(desc), rew, src, conf, a.pulled))
        n += cur.rowcount
    con.commit()
    carried = sum(1 for r in rows if kr.get(r[5]))
    print(f"적재 {n}행 (기존 {len(rows)-n}행) · 번역 이월 {carried}행")
    print("\n다음: python3 scripts/gates.py && python3 scripts/export.py && scripts/db_dump.sh")


if __name__ == "__main__":
    main()
