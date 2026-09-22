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
    /* ⚠️ 스캔 범위를 카드 끝까지(0.06~0.94) 잡으면 **금색 테두리·그림자가 잉크로 잡혀**
       첫 그룹 중심이 왼쪽으로 끌려가고, 그 자리에 그린 값이 카드 밖으로 잘린다(2026-09-22 실측).
       스탯 줄은 카드 안쪽에만 있으므로 양끝을 잘라낸다. */
    const sx0 = Math.round(W * 0.15), sx1 = Math.round(W * 0.85);
    const sb = bandsIn(sx0, sx1, Math.round(H * 0.62), Math.round(H * 0.82));
    const labelB = sb.length >= 2 ? sb[sb.length - 2] : null, valB = sb.length >= 2 ? sb[sb.length - 1] : sb[0];
    if (valB){
      /* ⭐⭐⭐ 중심은 **값 줄 자체**에서 읽는다(2026-09-22 전면 수정).
         종전에는 라벨 줄(`PAC SHO …`)에서 x를 읽어 값을 그렸는데, 라벨은 6단어 18글자라
         잉크 조각이 **19개**로 쪼개지고 그걸 6개로 줄이는 과정에서 엉뚱한 자리를 골라
         **값이 통째로 밀려 그려졌다**(사용자 지적 「스탯이 밀려서 나온다」).
         ⇒ 지울 대상인 **원본 값 줄의 숫자 6덩이 중심**을 그대로 쓰면 「지운 자리에 다시 쓴다」가 되어
            어긋날 여지가 없다. 숫자는 2자리씩이라 덩이 구분도 라벨보다 훨씬 깨끗하다.
         ⚠️ 그래도 조각이 6개를 넘을 수 있어(두 자리 숫자 사이 틈) **간격이 가장 큰 5곳에서만** 자른다. */
      const groupCenters = (band) => {
        const colInk = [];
        for (let x = sx0; x < sx1; x++){
          let ink = 0, n = 0;
          for (let y = band.a; y <= band.b; y++){ const c = at(x, y); if (c[3] < 40) continue; n++;
            const bgc = at(Math.max(sx0, x - 10), y); if (Math.abs(lum(c) - lum(bgc)) > 40) ink++; }
          colInk.push(n && ink / n > 0.25);
        }
        let st = null; const runs = [];
        colInk.forEach((v, i) => { if (v && st == null) st = i; else if (!v && st != null){ runs.push({ s: st, e: i }); st = null; } });
        if (st != null) runs.push({ s: st, e: colInk.length });
        if (runs.length < 6) return [];
        const gaps = runs.slice(1).map((r, i) => ({ g: r.s - runs[i].e, i }));
        const cuts = gaps.sort((a, b) => b.g - a.g).slice(0, 5).map(x => x.i).sort((a, b) => a - b);
        const out = []; let from = 0;
        for (const c of cuts.concat([runs.length - 1])){
          const grp = runs.slice(from, c + 1);
          out.push(sx0 + (grp[0].s + grp[grp.length - 1].e) / 2);
          from = c + 1;
        }
        return out;
      };
      let centers = groupCenters(valB);
      if (centers.length !== 6 && labelB) centers = groupCenters(labelB);   // 값 줄이 비면 라벨로 물러선다
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
