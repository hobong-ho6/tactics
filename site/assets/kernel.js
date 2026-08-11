/* 커널 적합 엔진 (JS) — core/kernel.py의 미러.
   정본은 파이썬+DB이고, 이 파일의 동치는 scripts/gates.py G5(JS 동치)가 보증한다.
   여기를 고치면 반드시 core/kernel.py와 같이 고치고 게이트를 돌릴 것. */

export function decodeMap(code){
  const a = new Float32Array(25);
  for (let i = 0; i < 25; i++) a[i] = code[i] === 'X' ? 1 : (+code[i]) / 10;
  return a;
}

export function cmpCos(a, b){
  let dot = 0, na = 0, nb = 0;
  for (let i = 0; i < 25; i++){ dot += a[i]*b[i]; na += a[i]*a[i]; nb += b[i]*b[i]; }
  return (na && nb) ? dot / Math.sqrt(na * nb) : 0;
}

export class Kernel {
  /* kernels/{GV}.json 객체로 초기화 */
  constructor(data){
    this.gv = data.game_version;
    this.roleGroup = {}; this.roleName = {};
    for (const r of data.roles){ this.roleGroup[r.role_id] = r.position_type; this.roleName[r.role_id] = r.name; }
    this.variants = new Map();          // 'role|focus' -> [{x, map}]
    for (const v of data.variants){
      const k = v.role_id + '|' + v.focus;
      if (!this.variants.has(k)) this.variants.set(k, []);
      this.variants.get(k).push({ x: v.pitch_x, map: decodeMap(v.kernel25) });
    }
    const nVar = data.variants.length, nCombo = this.variants.size, nRole = data.roles.length;
    if (this.gv === 'FC26' && (nRole !== 37 || nCombo !== 85 || nVar !== 217))
      throw new Error(`커널 정합 실패 ${nRole}/${nCombo}/${nVar} (기대 37/85/217)`);
  }
  placed(role, focus, x){
    const lst = this.variants.get(role + '|' + focus);
    if (!lst || !lst.length) return null;
    let best = lst[0], bd = Math.abs(lst[0].x - x);
    for (const v of lst){ const d = Math.abs(v.x - x); if (d < bd){ bd = d; best = v; } }
    return best.map;
  }
  fit(map25, role, focus, x){
    const pm = this.placed(role, focus, x);
    return pm ? cmpCos(decodeMap(map25), pm) : 0;
  }
  bestFit(map25, x, slotType){
    const v = decodeMap(map25);
    let best = { role: null, focus: null, sim: -1 };
    for (const [k, lst] of this.variants){
      const [role, focus] = k.split('|');
      if (this.roleGroup[role] !== slotType) continue;
      let pv = lst[0], bd = Math.abs(lst[0].x - x);
      for (const vv of lst){ const d = Math.abs(vv.x - x); if (d < bd){ bd = d; pv = vv; } }
      const s = cmpCos(v, pv.map);
      if (s > best.sim) best = { role, focus, sim: s };
    }
    return best;
  }
}
