#!/usr/bin/env python3
"""포지션별 OVR 산정식 적합 → `fc_position_ovr_weights` (2026-10-02 신설 · migration 091).

왜 (사용자 지시 「진화를 수행하지 않은 카드로 각 포지션별 오버롤 산정식을 추정해보자」):
  EA는 산정식을 공개하지 않고, 커뮤니티 표(FIFA 19 · 등급 D)는 FC27에서 정확 일치 32%였다.
  ⇒ fut.gg FC27 카드 중 **진화·특별·아이콘·히어로가 아닌** 카드의 29속성과 OVR로 직접 적합한다(등급 C).

어떻게:
  ⑴ `--fetch`: 목록 API(`/players/v2/27/?page=`)를 훑어 조건에 맞는 카드만 정의 API로 29속성을 받는다.
     그룹당 `--per-group`장까지. 결과는 `--cache`(jsonl)에 쌓이고 **이어 받기**가 된다.
  ⑵ `--fit`: 그룹마다 70% 적합 / 30% 시험. 비음수 최소제곱(가중 합 = 1) → 1% 미만 가중을 걷어 내고 재적합
     → **정수 %**로 맞춘다(알려진 EA 표가 그 모양이다). 보고 값은 **시험셋** 정확도다(외운 값이 아니다).
     최종 저장 가중치는 표본 전체로 다시 맞춘 것이다.
  ⑶ `--save`: 회차(`fitted`=오늘)로 행을 **추가**한다(불변규칙 2).
⚠️ numpy·scipy가 필요하다(이 스크립트만). 회차는 드물다 — 게임 패치로 OVR 체계가 바뀔 때 다시 돌린다.
⚠️ LWB·RWB·CF는 일반 카드가 거의 없어 적합하지 않는다 — core/position_ovr.py가 근사 그룹으로 보낸다.

사용:
    python3 scripts/fit_position_ovr.py --fetch --cache /tmp/ovrfit/cards.jsonl
    python3 scripts/fit_position_ovr.py --fit --cache /tmp/ovrfit/cards.jsonl            # 결과만 본다
    python3 scripts/fit_position_ovr.py --fit --save --cache /tmp/ovrfit/cards.jsonl     # DB에 적는다
"""
import argparse
import collections
import datetime as dt
import json
import math
import os
import random
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import DB                                        # noqa: E402
from core.futgg_attrs import ATTR_KR                       # noqa: E402
from core.position_ovr import APPROX, GROUP                # noqa: E402

GKA = ["다이빙", "핸들링", "킥", "포지셔닝", "반사신경"]
TODAY = dt.date.today().isoformat()


def fetch(cache, per_group):
    from scripts.collect_futgg_history import API, get
    have = {}
    if os.path.exists(cache):
        for line in open(cache):
            d = json.loads(line)
            have[d["ea"]] = d
    groups = {g for p, g in GROUP.items() if p not in APPROX}
    cnt = collections.Counter(GROUP.get(d["pos"]) for d in have.values())
    print(f"이미 받음 {len(have)}장 {dict(cnt)}", flush=True)
    with open(cache, "a") as f:
        for page in range(1, 335):
            if all(cnt[g] >= per_group for g in groups):
                break
            lst = get(f"{API}/players/v2/27/?page={page}") or {}
            for x in lst.get("data", []):
                if (x.get("isSpecial") or x.get("isEvolutionPlayerItem") or x.get("evolutionId")
                        or x.get("isIcon") or x.get("isHero")):
                    continue
                p = x.get("position")
                g = GROUP.get(p)
                if p in APPROX or not g or cnt[g] >= per_group or x["eaId"] in have:
                    continue
                d = get(f"{API}/player-item-definitions/27/{x['eaId']}/")
                d = (d or {}).get("data") or d or {}
                rec = {"ea": x["eaId"], "pos": p, "ovr": x.get("overall"), "def_ovr": d.get("overall"),
                       "attrs": {ATTR_KR[k]: d[k] for k in ATTR_KR if d.get(k) is not None}, "page": page}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                have[x["eaId"]] = rec
                cnt[g] += 1
                time.sleep(0.35)                 # 예의상 간격
            if page % 10 == 0:
                print(f"page {page} {dict(cnt)}", flush=True)
            time.sleep(0.5)
    print(f"끝 {len(have)}장 {dict(cnt)}")


def fit(cache, save):
    import numpy as np
    from scipy.optimize import nnls
    cards = [json.loads(line) for line in open(cache)]
    outf = [k for k in cards[0]["attrs"] if k not in GKA]
    rnd = lambda v: math.floor(v + 0.5)                                          # noqa: E731

    def nfit(S, keys, lam=1e4):
        X = np.array([[c["attrs"][k] for k in keys] for c in S], float)
        y = np.array([c["ovr"] for c in S], float)
        w, _ = nnls(np.vstack([X, lam * np.ones(len(keys))]), np.append(y, lam))   # 가중 합 = 1
        return w

    def sparse(S, keys, cut=0.01):
        ks, w = list(keys), nfit(S, keys)
        for _ in range(6):
            keep = [k for k, v in zip(ks, w) if v >= cut]
            if len(keep) == len(ks):
                break
            ks, w = keep, nfit(S, keep)
        return dict(zip(ks, w))

    def integer(w):
        p = {k: v * 100 for k, v in w.items()}
        r = {k: math.floor(v) for k, v in p.items()}
        for k in sorted(p, key=lambda k: -(p[k] - math.floor(p[k])))[:100 - sum(r.values())]:
            r[k] += 1
        return {k: v for k, v in r.items() if v > 0}

    def score(S, w):
        res = collections.Counter(rnd(sum(c["attrs"][k] * v for k, v in w.items()) / 100) - c["ovr"] for c in S)
        return res[0], res[0] + res[1] + res[-1]

    random.seed(7)
    byg = collections.defaultdict(list)
    for c in cards:
        g = GROUP.get(c["pos"])
        if g and c["pos"] not in APPROX and c["ovr"] == c.get("def_ovr", c["ovr"]):
            byg[g].append(c)
    rows = []
    for g, S in sorted(byg.items()):
        S = S[:]
        random.shuffle(S)
        cut = int(len(S) * 0.7)
        tr, te = S[:cut], S[cut:]
        keys = GKA + ["반응력"] if g == "GK" else outf
        ex, w1 = score(te, integer(sparse(tr, keys)))
        wf = integer(sparse(S, keys))                 # 저장값: 표본 전체로 다시 맞춘 것
        print(f"{g:4} 표본 {len(S):3} · 시험셋 정확 {ex}/{len(te)} ({ex / len(te):.0%}) · ±1 {w1}/{len(te)}"
              f"\n      {sorted(wf.items(), key=lambda t: -t[1])}")
        for a, v in wf.items():
            rows.append(("FC27", g, a, v, TODAY, len(S), len(te), ex, w1,
                         f"fut.gg FC27 비진화·비특별 카드 {len(S)}장 적합(scripts/fit_position_ovr.py · {TODAY}) — "
                         "비음수 최소제곱·가중 합 1·1% 미만 제거·정수 %",
                         f"등급 C(우리 적합 · EA 비공개). 시험셋 정확 {ex}/{len(te)}·±1 {w1}/{len(te)}. "
                         "⚠️ 절대값보다 진화 전후 차이로 쓸 것 — 국제 명성 등 선수별 오차가 차이에서 상쇄된다."))
    if save:
        con = sqlite3.connect(DB)
        con.executemany("""INSERT OR REPLACE INTO fc_position_ovr_weights(game_version,pos_group,attr,weight_pct,fitted,
                             sample_n,test_n,test_exact,test_within1,source,confidence) VALUES(?,?,?,?,?,?,?,?,?,?,?)""", rows)
        con.commit()
        print(f"\n적재 {len(rows)}행 → fc_position_ovr_weights (fitted {TODAY})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/ovrfit/cards.jsonl")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--per-group", type=int, default=220)
    ap.add_argument("--fit", action="store_true")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        Path(a.cache).parent.mkdir(parents=True, exist_ok=True)
        fetch(a.cache, a.per_group)
    if a.fit:
        fit(a.cache, a.save)


if __name__ == "__main__":
    main()
