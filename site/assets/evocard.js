/* 진화 카드 다시 그리기 — 카드 아트에 인쇄된 OVR·포지션·6대 스탯을 **현재 값으로 교체**한다.
   2026-09-19에 player.html 안에서 만들었고, 2026-09-21에 「지금 내 팀」 피치 카드도 같은 그림이
   필요해져 모듈로 뺐다(사용자 지시 「진화가 적용된 오버롤을 카드에 직접 보여줘」).
   ⛔ 두 화면이 **같은 함수**를 쓴다 — 한쪽만 고치면 같은 카드가 두 값으로 보인다.

   어떻게: 캔버스에 원본을 그린 뒤 ⑴ 글자 행 묶음을 밝기로 찾고 ⑵ 그 자리를 **위아래 색으로 세로
   보간**해 지우고(카드 판이 그라데이션이라 단색으로 칠하면 네모가 남는다) ⑶ 원래 잉크색·크기로 다시 쓴다.
   ⚠️ `crossorigin="anonymous"`로 로드한 이미지여야 getImageData가 된다(아니면 캔버스가 오염돼 예외).
   ⚠️ 실패하면 null을 반환한다 — 호출측은 원본 <img>를 그대로 둔다(빈 칸을 만들지 않는다). */
/* ⭐⭐ **레어도 판(카드 틀) 교체** — 진화로 등급이 오르면 판을 갈아 끼운다 (2026-09-27 신설,
   사용자 지시 「진화해서 금카가 된 건 금카로 카드 이미지도 바꿔줘」).

   ⛔⛔ **진화 카드의 완성 이미지는 어디에도 없다**(실측). fut.gg의 `paths/v2`가 주는 단계별 카드는
      OVR 65와 75가 **같은 이미지 파일**을 가리키고, GG Club은 아이템 id를 **base 그대로** 준다.
   ⭐ fut.gg 화면이 골드로 보이는 건 **클라이언트가 합성**하기 때문이다 —
      빈 판(`rarities-level-{1,2,3}`) + 선수 렌더 + 텍스트·로고.
   ⇒ 우리는 재료(선수 렌더·로고 URL)를 다 갖고 있지 않으므로 **차분으로 판만 바꾼다**:
      ⑴ 원래 등급의 빈 판을 카드 크기로 그려 **기준판**을 만든다
      ⑵ 원본 카드와 기준판이 **다른 픽셀 = 요소**(선수·이름·스탯·로고)다
      ⑶ 목표 등급 판 위에 그 요소만 얹는다
   ⭐ 실측(2026-09-27 마조 실버→골드): 요소로 잡힌 픽셀 22.8% · 얼굴·이름·로고·테두리 모두 보존됐다.
   ⚠️ 임계값 60은 압축 노이즈를 넘기고 요소는 살리는 값이다 — 낮추면 판 무늬가 요소로 딸려온다.
   ⚠️ 실패하면 **null**을 돌려준다. 호출측은 원본을 그대로 쓴다(빈 칸을 만들지 않는다). */
export const RARITY_LEVEL_CUT = [64, 74];   // ≤64 브론즈(1) · 65~74 실버(2) · ≥75 골드(3)

/* ⛔ 등급 판정의 **단일 정본**. 경계는 2026-09-27 실측으로 확정했다(등급 C) —
   fut.gg 간이 카드 자산을 직접 열어 64 브론즈 · 65 실버 · 74 실버 · 75 골드를 확인했다.
   ⛔ 이 숫자를 다른 곳에 다시 적지 않는다. */
export function rarityLevel(ovr){
  const v = Number(ovr);
  if (!Number.isFinite(v)) return null;
  return v <= RARITY_LEVEL_CUT[0] ? 1 : v <= RARITY_LEVEL_CUT[1] ? 2 : 3;
}

const loadImg = u => new Promise((res, rej) => {
  const i = new Image(); i.crossOrigin = 'anonymous';
  i.onload = () => res(i); i.onerror = () => rej(new Error('img'));
  i.src = u;
});

export async function replateCard(im, fromUrl, toUrl){
  try {
    const W = im.naturalWidth, H = im.naturalHeight;
    if (!W || !fromUrl || !toUrl || fromUrl === toUrl) return null;
    const [a, b] = await Promise.all([loadImg(fromUrl), loadImg(toUrl)]);
    const mk = (src) => { const c = document.createElement('canvas'); c.width = W; c.height = H;
      const x = c.getContext('2d', { willReadFrequently: true }); x.drawImage(src, 0, 0, W, H);
      return x.getImageData(0, 0, W, H); };
    const C = mk(im).data, S = mk(a).data, G = mk(b);
    let hit = 0;
    for (let i = 0; i < C.length; i += 4){
      const d = Math.abs(C[i] - S[i]) + Math.abs(C[i + 1] - S[i + 1]) + Math.abs(C[i + 2] - S[i + 2]);
      if (d > 60){ G.data[i] = C[i]; G.data[i + 1] = C[i + 1]; G.data[i + 2] = C[i + 2]; G.data[i + 3] = C[i + 3]; hit++; }
    }
    /* ⛔ 요소가 너무 적거나(판이 안 맞음) 너무 많으면(기준판 불일치) **바꾸지 않는다** —
       어설프게 바뀐 카드보다 원본이 낫다. 실측값 22.8%를 가운데 두고 넉넉히 잡았다. */
    const ratio = hit / (W * H);
    if (ratio < 0.08 || ratio > 0.55) return null;
    const cv = document.createElement('canvas'); cv.width = W; cv.height = H;
    cv.getContext('2d').putImageData(G, 0, 0);
    return cv;
  } catch (e) { return null; }
}

export function repaintEvoCard(im, vals){
  try {
    // ⚠️ 판 교체를 거치면 `im`이 **캔버스**다 — 캔버스엔 naturalWidth가 없다(2026-09-27).
    const W = im.naturalWidth || im.width, H = im.naturalHeight || im.height; if (!W) return null;
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
