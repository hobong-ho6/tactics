#!/usr/bin/env python3
"""GG Club 액티비티 피드 수집 — 진화 완료일 정정 + 영입 경로 채우기 (migration 137 · 2026-11-20).

왜 (사용자 지시 「액티비티 히스토리 … 진화 정보를 수집할수 있는지 검토」 → 「1·2 둘 다 여기서 구현」):
  fut.gg `/api/gg-club/<클럽>/activity/`는 **로그인 없이** 진화 완료·영입 이벤트를 시각과 함께 준다.
  ⑴ 진화 완료일: evo.completed(date_kind='sync')는 「싱크에서 발견한 시각」 = **실제 완료일의 상한**이다.
     원장 완료일이 그보다 늦으면 원장이 틀렸다(EA 이력 백필 날짜가 들어간 경우 — 11-18에 7~11일 늦은 5건).
     ⇒ 상한 날짜(한국 시간)로 내리고 notes에 정정 사유를 덧붙인다(migration 083 방식).
  ⑵ 영입 경로: signing.* 이벤트로 acquired_how를 채운다 — 기본값 「GG Club 싱크」인 행만(손 기록은 건드리지 않는다).

⛔ 하지 않는 것(2026-11-20 검토):
  · 진화 단계·중간 스탯 — 이벤트에 단계 번호가 없고, 카드 스냅샷은 진화가 아니라 **싱크 단위**다.
    EA 진화 이력(evo_detect --ea)이 더 정밀하다.
  · 처분 판정 — 판매·SBC 제출 이벤트가 없다.

사용:
    python3 scripts/collect_ggclub_activity.py            # 수집 + 정정 + 채우기
    python3 scripts/collect_ggclub_activity.py --dry-run  # 무엇을 바꿀지만 출력
"""
import argparse
import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                        # noqa: E402
from core.db import connect as connect_db                  # noqa: E402

KST = ZoneInfo("Asia/Seoul")
TODAY = dt.date.today().isoformat()
SRC = "fut.gg GG Club 액티비티 API(/api/gg-club/{club}/activity/ · 로그인 불요)"
CONF = "MEASURED — fut.gg가 EA 싱크로 기록한 이벤트. date_kind='sync'는 싱크에서 발견한 시각(실제 시각의 상한)"
DEFAULT_HOW = "GG Club 싱크"


def fetch(club):
    base = f"https://www.fut.gg/api/gg-club/{club}/activity/"
    hdr = {"User-Agent": "Mozilla/5.0", "Accept": "application/json",   # 기본 urllib UA는 Cloudflare 403
           "Referer": f"https://www.fut.gg/gg-club/{club}/"}
    items, url, pages = [], base, 0
    while url and pages < 200:                                          # 폭주 방지
        for t in range(3):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=30) as r:
                    d = json.load(r)
                break
            except urllib.error.HTTPError:
                if t == 2:
                    raise
                time.sleep(2)
        items += d["data"]
        pages += 1
        url = base + "?cursor=" + urllib.parse.quote(d["next"]) if d.get("next") else None
    return items, pages


def kst_date(iso):
    return dt.datetime.fromisoformat(iso).astimezone(KST).date().isoformat()


def item_base(item_id):
    """`2568732-943063496880-9` → `2568732-943063496880` (끝 접미는 싱크마다 바뀌는 버전)."""
    return "-".join(item_id.split("-")[:2])


def how_of(ev):
    """signing.* 이벤트 → [(item_id, acquired_how)]."""
    t, p = ev["type"], ev["payload"]
    if t == "signing.bought":
        return [(x["card"]["itemId"], f"구매 {x['price']:,}코인" if x.get("price") else "구매") for x in p["items"]]
    if t == "signing.reward":
        ref = (p.get("sourceRef") or {}).get("name")
        label = {"sbc": "SBC 보상", "objective": "목표 보상"}.get(p.get("source"), f"보상({p.get('source')})")
        return [(c["itemId"], f"{label} · {ref}" if ref else label) for c in p["cards"]]
    if t == "signing.season_pass":
        return [(x["card"]["itemId"], f"시즌패스 Lv{x['level']}" + (" 프리미엄" if x.get("isPremium") else ""))
                for x in p["cards"]]
    if t == "signing.packed_day":
        return [(c["itemId"], "팩 개봉") for c in p["cards"]]
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--club", default="ho6", help="GG Club 주소의 클럽 이름(fut.gg/gg-club/<club>/)")
    ap.add_argument("--account", type=int, default=1)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    items, pages = fetch(a.club)
    print(f"▶ 액티비티 {len(items)}건 · {pages}페이지 · 가장 오래된 {items[-1]['occurredAt'][:10] if items else '—'}")
    con = connect_db(DB)

    # ── 원본 적재(추가만) ──
    n_new = 0
    for ev in items:
        if a.dry_run:
            continue
        cur = con.execute("""INSERT OR IGNORE INTO fut_club_activity
              (event_id, account_id, type, occurred_at, date_kind, payload, pulled, source, confidence)
              VALUES (?,?,?,?,?,?,?,?,?)""",
                          (ev["id"], a.account, ev["type"], ev["occurredAt"], ev.get("dateKind"),
                           json.dumps(ev["payload"], ensure_ascii=False), TODAY, SRC.format(club=a.club), CONF))
        n_new += cur.rowcount
    print(f"   원본 신규 {n_new}건")

    cp = {item_base(g): (i, nm) for i, g, nm in con.execute(
        "SELECT id, gg_player_id, name FROM fut_club_players WHERE account_id=? AND gg_player_id IS NOT NULL",
        (a.account,))}
    ea2evo = {}
    for evo_id, ea in con.execute("SELECT evo_id, ea_evo_id FROM fc_evolutions WHERE ea_evo_id IS NOT NULL"):
        ea2evo.setdefault(ea, set()).add(evo_id)

    # ── ⑴ 진화 완료일 정정 ──
    # (카드, EA 진화) 별 상한 = 그 진화의 마지막 발견 날짜. 반복 진화도 마지막 회차가 상한이다.
    bound = {}
    for ev in items:
        if ev["type"] != "evo.completed" or ev.get("dateKind") != "sync":
            continue
        p = ev["payload"]
        k = (item_base(p["upgraded"]["itemId"]), p["evolution"]["eaId"])
        bound[k] = max(bound.get(k, ""), kst_date(ev["occurredAt"]))
    # ⚠️ 피드가 마지막으로 싱크한 날 이후에 원장에 적힌 완료는 피드가 아직 못 봤을 수 있다 → 정정하지 않는다.
    last_sync = max((kst_date(e["occurredAt"]) for e in items if e.get("dateKind") == "sync"), default="")
    fixed = []
    for (b, ea), lim in sorted(bound.items()):
        if b not in cp or ea not in ea2evo:
            continue                                         # 코스메틱 등 카탈로그 밖 — fut_evo_ea_ack가 다룬다
        cid, nm = cp[b]
        evs = sorted(ea2evo[ea])
        rows = con.execute(f"""SELECT id, evo_name, level, completed_at FROM v_evo_log
              WHERE club_player_id=? AND evo_id IN ({','.join('?' * len(evs))})
                AND completed_at > ? AND completed_at <= ?""", (cid, *evs, lim, last_sync)).fetchall()
        for lid, en, lv, old in rows:
            fixed.append((nm, en, lv, old, lim))
            if a.dry_run:
                continue
            con.execute("""UPDATE fut_evolution_log SET completed_at=?,
                  applied_at=CASE WHEN applied_at > ? THEN ? ELSE applied_at END,
                  notes=COALESCE(notes || ' ', '') || ? WHERE id=?""",
                        (lim, lim, lim,
                         f"⚠️ {TODAY} 완료일 정정 {old} → {lim}: GG Club 액티비티 evo.completed가 {lim}(KST)에 "
                         f"이미 발견했다(싱크 발견 시각 = 완료 상한 · collect_ggclub_activity.py · migration 137).", lid))
    print(f"\n■ 진화 완료일 정정 {len(fixed)}행")
    for nm, en, lv, old, new in fixed:
        print(f"   {nm} · {en} {lv}단계  {old} → {new}")

    # ── ⑵ 영입 경로 채우기 ──
    filled = []
    for ev in sorted(items, key=lambda e: e["occurredAt"]):
        for item_id, how in how_of(ev):
            hit = cp.get(item_base(item_id))
            if not hit:
                continue
            if a.dry_run:
                cur_how = con.execute("SELECT acquired_how FROM fut_club_players WHERE id=?", (hit[0],)).fetchone()[0]
                if cur_how == DEFAULT_HOW:
                    filled.append((hit[1], how))
                continue
            n = con.execute("UPDATE fut_club_players SET acquired_how=? WHERE id=? AND acquired_how=?",
                            (how, hit[0], DEFAULT_HOW)).rowcount
            if n:
                filled.append((hit[1], how))
    print(f"\n■ 영입 경로 채움 {len(filled)}장")
    for nm, how in filled:
        print(f"   {nm} — {how}")

    if a.dry_run:
        print("\n(--dry-run — DB에 쓰지 않았다)")
    else:
        con.commit()


if __name__ == "__main__":
    main()
