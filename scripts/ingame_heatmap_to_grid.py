#!/usr/bin/env python3
"""인게임(FC26) 선수 히트맵 스크린샷 → 5×5 그리드(map25) → 실측·커널과 코사인 대조 (2026-09-08 신설).

경로(docs/50 「경량 재개 절차」): PS5 화면을 **PS Remote Play(macOS)** 로 띄우고 ⌘⇧4로 창을 찍거나,
PS5 Create 버튼 캡처를 PS App/USB로 옮긴다. 카메라 촬영도 받되 정확도가 떨어진다(원근·반사).

사용:
  python3 scripts/ingame_heatmap_to_grid.py IMG --attack right [--box x0 y0 x1 y1]
        [--player-id N [--kind measured:season:full2526]] [--role wm_widemid --focus Support --x 87]
        [--save --regime 1 --tactic-code XXXX --note '…']
  --attack  이미지에서 그 팀의 공격 방향(up/down/left/right). 툴 그리드는 행0=공격 방향·열0=좌측 터치라인.
  --box     피치 영역 픽셀 좌표. 생략하면 초록 픽셀의 경계 상자로 자동 검출(실패 시 지정할 것).
  --save    결과를 ingame_captures에 INSERT(migration 028). 근거 없는 판정은 만들지 않는다 — 코사인만 기록.

⚠️ 실험적: FC26 히트맵 색 램프(초록 피치 위 노랑→빨강)를 「채도 높고 초록 아닌 픽셀」로 읽는다.
   첫 실물 스크린샷으로 --box·색 임계값을 검증한 뒤 정본으로 승격한다(docs/50).
"""
import argparse
import math
import sqlite3
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import DB                          # noqa: E402
from core.encode import encode               # noqa: E402
from core.kernel import Kernel, cos, decode  # noqa: E402


def load_hsv(path, box=None):
    im = Image.open(path).convert("RGB")
    if box:
        im = im.crop(tuple(box))
    hsv = np.asarray(im.convert("HSV"), dtype=np.float32) / 255.0   # H,S,V ∈ [0,1]
    return hsv


def auto_box(hsv):
    """초록(피치) 픽셀의 경계 상자. H 0.20~0.48 · S>0.25 · V>0.2."""
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    green = (h > 0.20) & (h < 0.48) & (s > 0.25) & (v > 0.2)
    ys, xs = np.where(green)
    if len(xs) < 100:
        raise SystemExit("⛔ 초록 피치 영역을 찾지 못했다 — --box로 지정할 것")
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def heat_weights(hsv):
    """히트 픽셀 가중치: 채도 높고 초록 밴드 밖(노랑~빨강·자홍) → S·V. 흰 선·검은 글자는 0."""
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    not_green = (h < 0.17) | (h > 0.52)
    heat = not_green & (s > 0.35) & (v > 0.25)
    return np.where(heat, s * v, 0.0)


def bin_grid(w, attack):
    """가중치 배열 → 25칸(툴 방향). attack ∈ up/down/left/right."""
    H, W = w.shape
    ys, xs = np.mgrid[0:H, 0:W]
    fx, fy = (xs + 0.5) / W, (ys + 0.5) / H
    if attack == "right":
        a, l = fx, fy
    elif attack == "left":
        a, l = 1 - fx, 1 - fy
    elif attack == "up":
        a, l = 1 - fy, fx
    elif attack == "down":
        a, l = fy, 1 - fx
    else:
        raise SystemExit("--attack은 up/down/left/right")
    row = np.clip(4 - np.floor(a * 5).astype(int), 0, 4)
    col = np.clip(np.floor(l * 5).astype(int), 0, 4)
    cells = np.zeros(25)
    np.add.at(cells, row * 5 + col, w)
    return [float(round(c, 3)) for c in cells]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--attack", required=True, choices=["up", "down", "left", "right"])
    ap.add_argument("--box", nargs=4, type=int)
    ap.add_argument("--player-id", type=int)
    ap.add_argument("--kind", default="measured:season:full2526")
    ap.add_argument("--role"); ap.add_argument("--focus"); ap.add_argument("--x", type=int)
    ap.add_argument("--save", action="store_true")
    ap.add_argument("--regime", type=int); ap.add_argument("--tactic-code"); ap.add_argument("--note", default="")
    ap.add_argument("--game-version", default="FC26")
    a = ap.parse_args()

    hsv = load_hsv(a.image)
    box = a.box or auto_box(hsv)
    hsv = hsv[box[1]:box[3], box[0]:box[2]]
    cells = bin_grid(heat_weights(hsv), a.attack)
    m25 = encode(cells)
    print(f"box={box} attack={a.attack}\ncells={cells}\nmap25={m25}")
    if not m25:
        raise SystemExit("⛔ 히트 픽셀 0 — 색 임계값·--box 확인")
    for r in range(5):
        print("  " + " ".join(f"{cells[r*5+c]:6.2f}" for c in range(5)))

    con = sqlite3.connect(DB)
    ref_kind = ref_map = sim = None
    if a.player_id:
        row = con.execute("SELECT map25 FROM prescriptions WHERE player_id=? AND kind=? AND map25 IS NOT NULL "
                          "ORDER BY season DESC LIMIT 1", (a.player_id, a.kind)).fetchone()
        if not row:
            row = con.execute("SELECT map25 FROM squad_entries WHERE player_id=? AND map25 IS NOT NULL LIMIT 1",
                              (a.player_id,)).fetchone()
        if row:
            ref_kind, ref_map = f"player:{a.player_id}:{a.kind}", row[0]
    if a.role and a.focus and a.x is not None:
        k = Kernel(a.game_version)
        pm = k.placed(a.role, a.focus, a.x)
        if pm:
            ref_kind, ref_map = f"kernel:{a.role}/{a.focus}@x{a.x}", encode(pm)
    if ref_map:
        sim = round(cos(decode(m25), decode(ref_map)), 3)
        print(f"대조 {ref_kind}: cos={sim}  (Δ≤0.05는 노이즈 구간 — docs/20 ①)")
    if a.save:
        con.execute("""INSERT INTO ingame_captures(captured, game_version, regime_id, tactic_code, player_id,
                       image_path, attack_dir, box, cells, map25, ref_kind, ref_map25, cosine, note, source, confidence)
                       VALUES(date('now'),?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (a.game_version, a.regime, a.tactic_code, a.player_id, str(a.image), a.attack,
                     ",".join(map(str, box)), ",".join(map(str, cells)), m25, ref_kind, ref_map, sim, a.note,
                     "scripts/ingame_heatmap_to_grid.py (스크린샷 색 분해)",
                     "EXPERIMENTAL — 색 임계값 미검증, 스트림 압축·UI 오버레이 오차 포함"))
        con.commit(); print("ingame_captures INSERT ✅")
    con.close()


if __name__ == "__main__":
    main()
