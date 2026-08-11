/* 피치 + 히트맵 렌더러 — 5×5 그리드를 이중선형 보간으로 부드럽게 그린다.
   좌표 규약: 그리드 행0 = 공격 방향(위), 열0 = 좌측 터치라인.
   슬롯/선수 x,y는 툴좌표(0–100): x=좌우(0=좌), y=수직(작을수록 자기 골문 쪽 — v1 규약 유지). */

export function drawPitch(ctx, w, h){
  ctx.fillStyle = '#0d1b12';
  ctx.fillRect(0, 0, w, h);
  ctx.strokeStyle = 'rgba(255,255,255,.25)'; ctx.lineWidth = 1;
  ctx.strokeRect(w*.03, h*.02, w*.94, h*.96);
  ctx.beginPath(); ctx.moveTo(w*.03, h*.5); ctx.lineTo(w*.97, h*.5); ctx.stroke();
  ctx.beginPath(); ctx.arc(w*.5, h*.5, w*.12, 0, Math.PI*2); ctx.stroke();
  for (const top of [true, false]){
    const y0 = top ? h*.02 : h*.98, dir = top ? 1 : -1;
    ctx.strokeRect(w*.24, y0, w*.52, dir*h*.16);
    ctx.strokeRect(w*.37, y0, w*.26, dir*h*.06);
  }
}

/* cells 25칸(0..1 정규값) → 캔버스 열지도. 위 = 공격 방향. */
export function drawHeat(ctx, w, h, vals, alpha = 0.85){
  const off = document.createElement('canvas');
  off.width = 5; off.height = 5;
  const octx = off.getContext('2d');
  const img = octx.createImageData(5, 5);
  for (let i = 0; i < 25; i++){
    const v = Math.max(0, Math.min(1, vals[i]));
    // 초록→노랑→빨강 램프 (v1 감성 유지)
    const r = Math.min(255, Math.round(v * 2 * 255));
    const g = Math.min(255, Math.round((1 - Math.max(0, v - .5) * 2) * 255));
    img.data[i*4] = r; img.data[i*4+1] = g; img.data[i*4+2] = 40;
    img.data[i*4+3] = Math.round(Math.pow(v, .7) * 255 * alpha);
  }
  octx.putImageData(img, 0, 0);
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = 'high';
  ctx.drawImage(off, w*.03, h*.02, w*.94, h*.96);
}

/* 여러 선수의 map25를 합성해 그린다. players: [{map25, weight?}] */
export function drawComposite(ctx, w, h, decoded, intensity = 1){
  const acc = new Float32Array(25);
  for (const d of decoded) for (let i = 0; i < 25; i++) acc[i] += d[i];
  let m = 0; for (const v of acc) m = Math.max(m, v);
  if (!m) return;
  const vals = Array.from(acc, v => Math.min(1, (v / m) * intensity));
  drawHeat(ctx, w, h, vals);
}

/* 슬롯 칩 (선수명 라벨) — 툴좌표 x(0=좌), y(0=자기 골문) → 캔버스 (위=공격) */
export function drawChip(ctx, w, h, x, y, label, color = '#ffd54d'){
  const px = w*.03 + (x/100) * w*.94;
  const py = h*.02 + (1 - y/100) * h*.96;
  ctx.font = '12px sans-serif';
  const tw = ctx.measureText(label).width + 12;
  ctx.fillStyle = 'rgba(0,0,0,.65)';
  ctx.beginPath(); ctx.roundRect(px - tw/2, py - 10, tw, 20, 9); ctx.fill();
  ctx.strokeStyle = color; ctx.stroke();
  ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
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
