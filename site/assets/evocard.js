/* 진화 카드 다시 그리기 — 카드 아트에 인쇄된 OVR·포지션·6대 스탯을 **현재 값으로 교체**한다.
   2026-09-19에 player.html 안에서 만들었고, 2026-09-21에 「지금 내 팀」 피치 카드도 같은 그림이
   필요해져 모듈로 뺐다(사용자 지시 「진화가 적용된 오버롤을 카드에 직접 보여줘」).
   ⛔ 두 화면이 **같은 함수**를 쓴다 — 한쪽만 고치면 같은 카드가 두 값으로 보인다.

   어떻게: 캔버스에 원본을 그린 뒤 ⑴ 글자 행 묶음을 밝기로 찾고 ⑵ 그 자리를 **위아래 색으로 세로
   보간**해 지우고(카드 판이 그라데이션이라 단색으로 칠하면 네모가 남는다) ⑶ 원래 잉크색·크기로 다시 쓴다.
   ⚠️ `crossorigin="anonymous"`로 로드한 이미지여야 getImageData가 된다(아니면 캔버스가 오염돼 예외).
   ⚠️ 실패하면 null을 반환한다 — 호출측은 원본 <img>를 그대로 둔다(빈 칸을 만들지 않는다). */
export function repaintEvoCard(im, vals){
  try {
    const W = im.naturalWidth, H = im.naturalHeight; if (!W) return null;
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H;
    const cx = cv.getContext('2d', { willReadFrequently: true }); cx.drawImage(im, 0, 0);
    const D = cx.getImageData(0, 0, W, H).data;
    const at = (x, y) => { const i = ((y | 0) * W + (x | 0)) * 4; return [D[i], D[i + 1], D[i + 2], D[i + 3]]; };
    const lum = c => (c[0] * 299 + c[1] * 587 + c[2] * 114) / 1000;
    /* 글자 행 묶음 찾기 — 행 중앙값 밝기에서 크게 벗어난 픽셀을 잉크로 센다 */
    const bandsIn = (x0, x1, y0, y1, th = 0.08) => {
      const out = []; let cur = null;
      for (let y = y0; y < y1; y++){
        const vs = []; for (let x = x0; x < x1; x += 2){ const c = at(x, y); if (c[3] < 40) continue; vs.push(lum(c)); }
        let ink = 0;
        if (vs.length){ const st = vs.slice().sort((a, b) => a - b), bg = st[st.length >> 1];
          ink = vs.filter(v => Math.abs(v - bg) > 45).length / vs.length; }
        if (ink > th){ cur = cur || { a: y, b: y }; cur.b = y; }
        else if (cur){ if (cur.b - cur.a > 2) out.push(cur); cur = null; }
      }
      if (cur && cur.b - cur.a > 2) out.push(cur);
      return out;
    };
    /* ⭐ 지우기 — **열마다 위아래 행 색을 세로 보간**한다. 카드 판은 위에서 아래로 그라데이션이라
       한 색으로 칠하면 네모가 보이지만, 보간하면 원래 판처럼 이어진다(2026-09-19 실측으로 방식 확정). */
    const erase = (x0, x1, b, pad = 2) => {
      const yA = Math.max(0, b.a - pad - 1), yB = Math.min(H - 1, b.b + pad + 1);
      for (let x = x0; x < x1; x++){
        const cA = at(x, yA), cB = at(x, yB);
        if (cA[3] < 40 && cB[3] < 40) continue;
        for (let y = b.a - pad; y <= b.b + pad; y++){
          const t = (y - yA) / Math.max(1, yB - yA);
          const c = [0, 1, 2].map(k => Math.round(cA[k] * (1 - t) + cB[k] * t));
          cx.fillStyle = `rgb(${c[0]},${c[1]},${c[2]})`; cx.fillRect(x, y, 1, 1);
        }
      }
    };
    const inkColor = (x0, x1, b) => {
      let best = null;
      for (let y = b.a; y <= b.b; y++) for (let x = x0; x < x1; x++){
        const c = at(x, y); if (c[3] < 40) continue;
        const v = lum(c); if (best == null || v < best.v) best = { v, c: `rgb(${c[0]},${c[1]},${c[2]})` };
      }
      return best ? best.c : '#222';
    };
    /* 글자 크기 — 잉크 행 높이는 글자의 **본문 높이**라 그대로 쓰면 원본보다 작아 보인다(2026-09-19 사용자 지적).
       숫자는 1.32배, 포지션 같은 대문자 라벨은 1.2배로 키운다. */
    const draw = (txt, cxx, b, weight, scale = 1.32) => {
      const h = (b.b - b.a + 1) * scale;
      cx.textAlign = 'center'; cx.textBaseline = 'middle';
      cx.font = `${weight} ${Math.round(h)}px "DIN Alternate","Arial Narrow",Arial,sans-serif`;
      cx.fillText(txt, cxx, (b.a + b.b) / 2 + 0.5);
    };
    // ① 좌상단 OVR·포지션 (원본 카드 그대로의 자리)
    const ox0 = Math.round(W * 0.12), ox1 = Math.round(W * 0.34);
    const ob = bandsIn(ox0, ox1, Math.round(H * 0.11), Math.round(H * 0.42));
    if (ob[0]){ const col = inkColor(ox0, ox1, ob[0]); erase(ox0, ox1, ob[0]); cx.fillStyle = col;
                draw(String(vals.ovr ?? '—'), (ox0 + ox1) / 2, ob[0], 700); }
    if (ob[1] && vals.pos){ const col = inkColor(ox0, ox1, ob[1]); erase(ox0, ox1, ob[1]); cx.fillStyle = col;
                draw(vals.pos, (ox0 + ox1) / 2, ob[1], 600, 1.2); }
    // ② 하단 6대 스탯 — **값 줄만** 바꾼다(이름·라벨은 원본 그대로 두어 배치가 같다)
    const sx0 = Math.round(W * 0.06), sx1 = Math.round(W * 0.94);
    const sb = bandsIn(sx0, sx1, Math.round(H * 0.62), Math.round(H * 0.82));
    const labelB = sb.length >= 2 ? sb[sb.length - 2] : null, valB = sb.length >= 2 ? sb[sb.length - 1] : sb[0];
    if (valB){
      // 라벨 줄에서 6칸의 x 중심을 읽어 값 위치를 정확히 맞춘다
      let centers = [];
      if (labelB){
        const colInk = [];
        for (let x = sx0; x < sx1; x++){
          let ink = 0, n = 0;
          for (let y = labelB.a; y <= labelB.b; y++){ const c = at(x, y); if (c[3] < 40) continue; n++;
            const bgc = at(Math.max(sx0, x - 10), y); if (Math.abs(lum(c) - lum(bgc)) > 40) ink++; }
          colInk.push(n && ink / n > 0.25);
        }
        let st = null;
        colInk.forEach((v, i) => { if (v && st == null) st = i; else if (!v && st != null){
          if (i - st > 2) centers.push(sx0 + (st + i) / 2); st = null; } });
        /* 라벨 세 글자가 붙어 한 덩어리로 잡히거나 글자별로 쪼개지면 6칸이 안 나온다 —
           7칸 이상이면 **가장 넓은 6개**를 고른다(2026-09-20 사용자 지적 「진화카드 스탯 간격」). */
        if (centers.length > 6){
          const gaps = centers.slice(1).map((c, i) => c - centers[i]);
          while (centers.length > 6){
            let k = 0; for (let i = 1; i < gaps.length; i++) if (gaps[i] < gaps[k]) k = i;
            centers.splice(k + 1, 1); gaps.splice(k, 1);
          }
        }
      }
      /* 폴백 범위가 6~94%면 값이 라벨보다 바깥으로 퍼져 어긋난다 — 실제 스탯 줄은 그보다 좁다. */
      if (centers.length !== 6){ const a = Math.round(W * 0.11), b2 = Math.round(W * 0.89);
        const cw = (b2 - a) / 6; centers = [0,1,2,3,4,5].map(i => a + cw * (i + 0.5)); }
      const col = inkColor(sx0, sx1, valB);
      erase(sx0, sx1, valB);
      cx.fillStyle = col;
      vals.six.forEach(([, v], i) => draw(v == null ? '—' : String(v), centers[i], valB, 700));
    }
    return cv;
  } catch (e){ return null; }
}
