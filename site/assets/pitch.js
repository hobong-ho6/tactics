/* 피치 + 히트맵 렌더러 — 5×5 그리드를 칸 그대로(단일색 진하기 + 비중 %) 그린다.
   좌표 규약: 그리드 행0 = 공격 방향(위), 열0 = 좌측 터치라인.
   슬롯/선수 x,y는 툴좌표(0–100): x=좌우(0=좌), y=수직(작을수록 자기 골문 쪽 — v1 규약 유지). */

import { cssVar } from './tokens.js';

export function drawPitch(ctx, w, h){
  ctx.fillStyle = cssVar('--pitch-bg');
  ctx.fillRect(0, 0, w, h);
  ctx.strokeStyle = cssVar('--pitch-line'); ctx.lineWidth = 1;
  ctx.strokeRect(w*.03, h*.02, w*.94, h*.96);
  ctx.beginPath(); ctx.moveTo(w*.03, h*.5); ctx.lineTo(w*.97, h*.5); ctx.stroke();
  ctx.beginPath(); ctx.arc(w*.5, h*.5, w*.12, 0, Math.PI*2); ctx.stroke();
  for (const top of [true, false]){
    const y0 = top ? h*.02 : h*.98, dir = top ? 1 : -1;
    ctx.strokeRect(w*.24, y0, w*.52, dir*h*.16);
    ctx.strokeRect(w*.37, y0, w*.26, dir*h*.06);
  }
}

/* ⭐ 5×5 칸 그대로 그린다(2026-10-29 사용자 지시 「히트맵을 더 직관적으로」).
   ⛔ 종전엔 5×5 이미지를 피치 전체로 늘려 이중선형 보간 + 초록→노랑→빨강 램프로 그렸다 —
      원자료보다 정밀해 보였고, 낮은 값의 초록이 잔디색에 묻혔고, 범례·공격 방향이 없었다.
   ⇒ 칸 = 원자료 칸 · 단일색 진하기(CLAUDE.md 불변규칙 8) · 칸 숫자 = 활동 비중 % · 범례 · ▲ 공격 방향.
   vals = 25칸 0..1(최댓값 기준 진하기), share = 25칸 비중 %(합 100). 위 = 공격 방향. */
const HEAT_RGB = '255,196,60';
export function drawHeat(ctx, w, h, vals, share){
  const x0 = w*.03, y0 = h*.02, cw = w*.94/5, ch = h*.96/5;
  for (let i = 0; i < 25; i++){
    const v = Math.max(0, Math.min(1, vals[i])), r = i / 5 | 0, c = i % 5;
    ctx.fillStyle = `rgba(${HEAT_RGB},${(v ? .06 + v * .86 : 0).toFixed(3)})`;
    ctx.fillRect(x0 + c*cw + 1, y0 + r*ch + 1, cw - 2, ch - 2);
    if (!share) continue;
    const pct = Math.round(share[i]);
    ctx.font = `${pct ? 'bold ' : ''}26px sans-serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'top';
    ctx.fillStyle = v > .5 ? cssVar('--on-color-ink') : (pct ? cssVar('--on-pitch-txt') : cssVar('--on-pitch-dim'));
    ctx.fillText(pct ? `${pct}%` : '·', x0 + (c + .5)*cw, y0 + r*ch + 10);
  }
  // 칸 경계 — 숫자가 어느 칸 것인지 읽히게
  ctx.strokeStyle = 'rgba(255,255,255,.12)'; ctx.lineWidth = 1;
  for (let k = 1; k < 5; k++){
    ctx.beginPath(); ctx.moveTo(x0 + k*cw, y0); ctx.lineTo(x0 + k*cw, y0 + 5*ch); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x0, y0 + k*ch); ctx.lineTo(x0 + 5*cw, y0 + k*ch); ctx.stroke();
  }
  drawPitchLegend(ctx, w, h);
}

/* ▲ 공격 방향(왼쪽 위) + 진하기 범례(오른쪽 아래) */
function drawPitchLegend(ctx, w, h){
  const pill = (x, y, tw, align) => {
    ctx.fillStyle = cssVar('--pitch-chip-bg');
    ctx.beginPath(); ctx.roundRect(align === 'right' ? x - tw : x, y, tw, 30, 8); ctx.fill();
  };
  ctx.font = 'bold 20px sans-serif'; ctx.textBaseline = 'middle';
  const a = '▲ 공격 방향', aw = ctx.measureText(a).width + 18;
  pill(w*.03 + 8, h*.02 + 46, aw);
  ctx.fillStyle = cssVar('--on-pitch-txt'); ctx.textAlign = 'left';
  ctx.fillText(a, w*.03 + 17, h*.02 + 61);

  ctx.font = '18px sans-serif';
  const bw = 120, lw = ctx.measureText('적음').width, rw = ctx.measureText('많음').width;
  const tw = lw + bw + rw + 34, right = w*.97 - 8, top = h*.98 - 38, left = right - tw;
  pill(right, top, tw, 'right');
  ctx.fillStyle = cssVar('--on-pitch-dim');
  ctx.fillText('적음', left + 9, top + 15);
  const g = ctx.createLinearGradient(left + lw + 17, 0, left + lw + 17 + bw, 0);
  g.addColorStop(0, `rgba(${HEAT_RGB},0)`); g.addColorStop(1, `rgba(${HEAT_RGB},.92)`);
  ctx.fillStyle = g; ctx.fillRect(left + lw + 17, top + 8, bw, 14);
  ctx.strokeStyle = 'rgba(255,255,255,.3)'; ctx.strokeRect(left + lw + 17, top + 8, bw, 14);
  ctx.fillStyle = cssVar('--on-pitch-dim');
  ctx.fillText('많음', left + lw + bw + 25, top + 15);
}

/* 여러 선수의 map25를 합성해 그린다 — 진하기는 최댓값 기준, 숫자는 합계 대비 비중 %. */
export function drawComposite(ctx, w, h, decoded, intensity = 1){
  const acc = new Float32Array(25);
  for (const d of decoded) for (let i = 0; i < 25; i++) acc[i] += d[i];
  let m = 0, sum = 0; for (const v of acc){ m = Math.max(m, v); sum += v; }
  if (!m) return;
  const vals = Array.from(acc, v => Math.min(1, (v / m) * intensity));
  drawHeat(ctx, w, h, vals, Array.from(acc, v => v / sum * 100));
}

/* 슬롯 칩 (선수명 라벨) — 툴좌표 x(0=좌), y(0=자기 골문) → 캔버스 (위=공격) */
export function drawChip(ctx, w, h, x, y, label, color = cssVar('--warn')){
  const px = w*.03 + (x/100) * w*.94;
  const py = h*.02 + (1 - y/100) * h*.96;
  ctx.font = '12px sans-serif';
  const tw = ctx.measureText(label).width + 12;
  ctx.fillStyle = cssVar('--pitch-chip-bg');
  ctx.beginPath(); ctx.roundRect(px - tw/2, py - 10, tw, 20, 9); ctx.fill();
  ctx.strokeStyle = color; ctx.stroke();
  ctx.fillStyle = cssVar('--pitch-chip-txt'); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(label, px, py);
}

/* 25칸 미니 그리드(SVG) — 비교 카드용 */
export function miniGrid(map25, size = 90){
  const cell = size / 5;
  let rects = '';
  for (let i = 0; i < 25; i++){
    const v = map25[i] === 'X' ? 1 : (+map25[i]) / 10;
    const r = i / 5 | 0, c = i % 5;
    rects += `<rect x="${c*cell}" y="${r*cell}" width="${cell-1}" height="${cell-1}" rx="2"
      fill="rgba(42,160,90,${(0.06 + v*0.94).toFixed(3)})"/>`;
  }
  return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}"
    role="img" aria-label="5x5 히트맵 그리드">${rects}</svg>`;
}
