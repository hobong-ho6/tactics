#!/usr/bin/env python3
"""인게임(FC26) Match Facts 선수 히트맵 스크린샷 → 5×5 그리드(map25) → 커널·실측 코사인 (2026-09-08 신설 · 실물 15장으로 검증).

UI 전제(FC26 「선수 경기 내용」 화면, PS Remote Play 720p 창 캡처, Retina 2× → 피치 외곽 759×1013px):
  · 피치는 반투명 어두운 직사각형 + 회백색 외곽선(좌측선 밝기≈105, 우측선≈80 — 임계 60).
  · 히트맵은 **밝은 초록 육각형**(g > r+40, g > b+40, g > 110), 밀도가 높을수록 밝다 → g값을 가중치로 쓴다.
  · 검은 포메이션 점 11개가 피치에 고정 — **GK 점 중심 = 피치 하단선 − 48px** 를 세로 기준점으로 쓴다
    (상단선은 히트맵·「총 등급」 텍스트에 자주 가려 열 프로파일만으로는 어긋났다 — 15장 중 2장 실패 → GK 점 도입 후 15/15).
  · 화면 방향: 우리 골문이 아래, 공격이 위(--attack up 기본). 툴 그리드 행0=공격 방향, 열0=공격 팀 기준 좌측 터치라인 = 화면 좌측.
  ⚠️ FC26 히트맵은 **위치 기반**(14분 출전 선수도 연속 분포)이라 SofaScore 터치 기반 실측과 원천이 다르다 — 실측 코사인은 참고치.

사용:
  python3 scripts/ingame_heatmap_to_grid.py IMG [--attack up] [--box x0 y0 x1 y1]
        [--player-id N [--slot-type WM]] [--role wm_widemid --focus Support --x 85]
        [--save --regime 1 --tactic-code XXXX --report-id N --note '…' --controlled]
  --controlled  사용자가 주로 조작한 선수 — note에 「조작 오염」을 붙이고 커널 대조 근거로 쓰지 않는다(docs/50 한계 표).
"""
import argparse
import sqlite3
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                          # noqa: E402
from core.encode import encode               # noqa: E402
from core.kernel import Kernel, cos, decode  # noqa: E402

PH, PW, GK_OFF = 1013, 759, 48   # 피치 외곽 크기 · GK 점 중심→하단선 거리 (Remote Play 창 크기 고정 전제)


def _clusters(idx, gap=3):
    cl = []
    for x in idx:
        if cl and x - cl[-1][-1] <= gap:
            cl[-1].append(x)
        else:
            cl.append([x])
    return [int(np.mean(c)) for c in cl]


def _pair(cands, gap, tol=15):
    best = None
    for i, a in enumerate(cands):
        for b in cands[i + 1:]:
            if abs((b - a) - gap) < tol and (best is None or abs((b - a) - gap) < best[0]):
                best = (abs((b - a) - gap), a, b)
    return best[1:] if best else None


def auto_box(a):
    """피치 외곽 상자 (x0,y0,x1,y1). 좌·우선은 열 프로파일(PH 윈도우 회색 ≥85%), 세로는 GK 점 기준."""
    lum = a.mean(axis=2)
    sat = a.max(axis=2) - a.min(axis=2)
    grey = (lum > 60) & (sat < 40)
    H, W = grey.shape
    c = np.concatenate([np.zeros((1, W), int), np.cumsum(grey, axis=0)])
    colwin = (c[PH:] - c[:-PH]).max(axis=0)
    xs = _pair(_clusters([x for x in range(W) if colwin[x] >= 0.85 * PH]), PW)
    if not xs:
        raise SystemExit("⛔ 피치 좌·우 외곽선을 찾지 못했다 — --box로 지정할 것")
    xl, xr = xs
    xc = (xl + xr) // 2
    dark = (lum[:, xc - 25:xc + 25] < 35).sum(axis=1)
    runs = []
    for y in [y for y in range(H) if dark[y] >= 30]:
        if runs and y - runs[-1][-1] <= 2:
            runs[-1].append(y)
        else:
            runs.append([y])
    gk = [r for r in runs if 22 <= len(r) <= 48]
    if not gk:
        raise SystemExit("⛔ GK 포메이션 점을 찾지 못했다 — --box로 지정할 것")
    yb = (gk[-1][0] + gk[-1][-1]) // 2 + GK_OFF
    return (xl, yb - PH, xr, yb)


def heat_cells(a, box, attack="up"):
    xl, yt, xr, yb = box
    sub = a[yt:yb, xl:xr].astype(int)
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    heat = (g > r + 40) & (g > b + 40) & (g > 110)
    w = np.where(heat, g / 255.0, 0.0)
    H, W = w.shape
    ys, xs = np.mgrid[0:H, 0:W]
    fx, fy = (xs + 0.5) / W, (ys + 0.5) / H
    if attack == "up":
        a_, l_ = 1 - fy, fx
    elif attack == "down":
        a_, l_ = fy, 1 - fx
    elif attack == "right":
        a_, l_ = fx, fy
    elif attack == "left":
        a_, l_ = 1 - fx, 1 - fy
    else:
        raise SystemExit("--attack은 up/down/left/right")
    row = np.clip(4 - np.floor(a_ * 5).astype(int), 0, 4)
    col = np.clip(np.floor(l_ * 5).astype(int), 0, 4)
    cells = np.zeros(25)
    np.add.at(cells, row * 5 + col, w)
    return [round(float(v), 1) for v in cells], int(heat.sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--attack", default="up", choices=["up", "down", "left", "right"])
    ap.add_argument("--box", nargs=4, type=int)
    ap.add_argument("--player-id", type=int)
    ap.add_argument("--slot-type", help="squad_entries 실측 그리드 선택용 (GK/CB/FB/DM/CM/CAM/WM/W/ST)")
    ap.add_argument("--role"); ap.add_argument("--focus"); ap.add_argument("--x", type=int)
    ap.add_argument("--save", action="store_true"); ap.add_argument("--controlled", action="store_true")
    ap.add_argument("--regime", type=int); ap.add_argument("--tactic-code"); ap.add_argument("--report-id", type=int)
    ap.add_argument("--note", default=""); ap.add_argument("--game-version", default="FC26")
    a = ap.parse_args()

    arr = np.asarray(Image.open(a.image).convert("RGB")).astype(int)
    box = tuple(a.box) if a.box else auto_box(arr)
    cells, n = heat_cells(arr, box, a.attack)
    m25 = encode(cells)
    if not m25:
        raise SystemExit("⛔ 히트 픽셀 0 — 색 임계값·--box 확인")
    own = round(100 * sum(cells[15:]) / sum(cells), 1)
    print(f"box={box} attack={a.attack} heat_px={n}\nmap25={m25}  자기진영(행3~4) {own}%")
    for r in range(5):
        print("  " + " ".join(f"{cells[r*5+c]:8.1f}" for c in range(5)))

    con = sqlite3.connect(DB)
    k = Kernel(a.game_version)
    ref_kind = ref_map = sim = None
    extra = []
    if a.role and a.focus and a.x is not None:
        pm = k.placed(a.role, a.focus, a.x)
        if pm:
            ref_kind, ref_map = f"kernel:{a.role}/{a.focus}@x{a.x}", encode(pm)
            sim = round(cos(decode(m25), pm), 3)
            print(f"게임 커널 {ref_kind}: cos={sim}")
    if a.player_id:
        q = "SELECT map25, slot_type FROM squad_entries WHERE player_id=? AND map25 IS NOT NULL"
        p = (a.player_id,)
        if a.slot_type:
            q += " AND slot_type=?"; p += (a.slot_type,)
        row = con.execute(q + " LIMIT 1", p).fetchone()
        if row and set(row[0]) != {"0"}:
            cm = round(cos(decode(m25), decode(row[0])), 3)
            extra.append(f"실측({row[1]}) cos={cm}")
            if ref_map is None:
                ref_kind, ref_map, sim = f"player:{a.player_id}:{row[1]}", row[0], cm
    if a.slot_type and a.x is not None:
        b = k.best_fit(m25, a.x, a.slot_type)
        extra.append(f"군내 최적 {b[0]}/{b[1]} {b[2]:.3f}")
    if extra:
        print(" · ".join(extra))
    if a.save:
        note = ("[조작 오염 — 커널 대조 근거로 쓰지 않음] " if a.controlled else "") + a.note
        if extra:
            note += " | " + " · ".join(extra)
        con.execute("""INSERT INTO ingame_captures(captured, game_version, regime_id, tactic_code, report_id, player_id,
                       image_path, attack_dir, box, cells, map25, ref_kind, ref_map25, cosine, note, source, confidence)
                       VALUES(date('now'),?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (a.game_version, a.regime, a.tactic_code, a.report_id, a.player_id, str(a.image), a.attack,
                     ",".join(map(str, box)), ",".join(map(str, cells)), m25, ref_kind, ref_map, sim, note,
                     "scripts/ingame_heatmap_to_grid.py (Remote Play 720p 캡처 · 초록 육각 가중 · GK 점 기준 상자)",
                     "MEDIUM — 위치 기반 게임 히트맵 vs 터치 기반 실측 원천 차이 · 사용자 플레이 스타일 혼입 · 단일 경기"))
        con.commit()
        print("ingame_captures INSERT ✅")
    con.close()


if __name__ == "__main__":
    main()
