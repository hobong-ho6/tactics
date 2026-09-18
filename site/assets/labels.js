/* 읽기용 라벨 — 코드값·내부 참조를 사람이 읽는 말로 바꾼다 (2026-09-18, 사용자 지시
   「코드 값을 그대로 넣거나 클로드가 판단하기 위한 근거나 주석이 많다 — 사용자가 읽는 정보니 정리」).
   ⚠️ DB 값은 고치지 않는다(불변규칙 2) — 화면에서만 바꾸고 원문 코드는 title(hover)에 남긴다.
   「원문 표기」 토글(localStorage reader_raw=1)을 켜면 변환을 끈다. */

export const ROLE_KR = {
  gk_goalkeeper:'골키퍼', gk_sweeper:'스위퍼 키퍼', gk_ballplaying:'볼 플레잉 키퍼',
  cb_defender:'센터백', cb_stopper:'스토퍼', cb_bpd:'볼 플레잉 센터백', cb_wideback:'와이드 백',
  fb_fullback:'풀백', fb_wingback:'윙백', fb_att_wb:'공격형 윙백', fb_falseback:'폴스백', fb_inverted:'인버티드 윙백',
  dm_holding:'홀딩', dm_centrehalf:'센터 하프', dm_dlp:'딥라잉 플레이메이커', dm_widehalf:'와이드 하프', dm_boxcrasher:'박스 크래셔',
  cm_holding:'홀딩', cm_dlp:'딥라잉 플레이메이커', cm_b2b:'박스 투 박스', cm_playmaker:'플레이메이커', cm_halfwinger:'하프 윙어',
  cam_playmaker:'플레이메이커', cam_shadow:'섀도 스트라이커', cam_halfwinger:'하프 윙어', cam_classic10:'클래식 10번',
  w_winger:'윙어', w_insidefwd:'인사이드 포워드', w_wideplm:'와이드 플레이메이커',
  wm_winger:'윙어', wm_insidefwd:'인사이드 포워드', wm_wideplm:'와이드 플레이메이커', wm_widemid:'와이드 미드필더',
  st_advanced:'어드밴스드 포워드', st_false9:'폴스 나인', st_poacher:'포처', st_target:'타깃 포워드',
};
const POS_OF = { gk:'GK', cb:'CB', fb:'풀백', dm:'DM', cm:'CM', cam:'CAM', w:'윙', wm:'측면 MF', st:'ST' };
export const FOCUS_KR = { Attack:'공격', Balanced:'균형', Defend:'수비', 'Build-Up':'빌드업', Roaming:'자유 이동',
  Support:'지원', Versatile:'다재다능', Aggressive:'적극', 'Ball-Winning':'볼 탈취', Wide:'넓게' };
export const VERDICT_KR = { APPLIED:'반영됨', HELD:'보류', REJECTED:'기각', PENDING:'판정 대기', NA:'해당 없음',
  MATCH:'일치', CONFLICT:'충돌', PROSE:'산문' };
export const AXIS_KR = { role:'역할', focus:'포커스', team_axis:'팀 설정', instruction:'지시·운용', limit:'재현 한계', none:'주장 없음' };

/* 구현 주장 field/value 슬러그 → 문장. 사전에 없으면 밑줄을 띄어쓰기로. */
export const FIELD_KR = {
  cup_competition_stance:'컵대회에 대한 태도', added_asset:'새로 더해진 자산', gk_long_distribution_target:'GK 롱볼 타깃',
  rb_build_up_shape:'우측 풀백의 빌드업 형태', winger_width:'윙어의 폭', double_pivot:'더블 피벗', selection_gate:'선발 조건',
  set_piece_defence:'수비 세트피스', set_pieces:'세트피스', striker_depth:'스트라이커의 깊이', striker_first_duty:'스트라이커의 1차 임무',
  advance_depth:'전진 깊이', fullback_inside_release:'풀백의 안쪽 진입', left_cover:'좌측 커버', link_pair:'연결 짝', release_speed:'볼 처리 속도',
  second_half_change:'후반 변화', vs_back3:'백3 상대 대응', wide_asymmetry:'측면 비대칭', formation:'포메이션', in_possession:'점유 국면',
  pressing:'압박', rotation:'로테이션', situational:'상황별', build_up_style:'빌드업 스타일', defensive_approach:'수비 접근', line_height:'라인 높이',
  rest_defense_left:'좌측 rest-defense',
};
export const VALUE_KR = {
  europe_route_not_rotation_filler:'유럽 진출 경로(로테이션 소화가 아님)', speed_direct_running:'스피드·직선 돌파', mbaye_run_in_behind:'음바예의 배후 침투',
  tuck_in_hybrid_back3:'안으로 접혀 하이브리드 백3', hold_touchline_right:'우측 터치라인 폭 유지', barkley_bogarde_pairing_unstable_on_ball:'바클리–보가르드 짝은 볼을 잡으면 불안',
  away_defensive_workload:'원정 수비 부담', free_kick_wall_too_deep:'프리킥 벽이 너무 물러남', near_post_target_repeated:'니어포스트 타깃 반복',
  opponent_marking:'상대 마킹 실패', routine:'설계 루틴', stays_as_box_reference:'박스 기준점으로 남는다', pressing_intensity:'압박 강도',
  raised_by_carrier_swap:'캐리어 교체로 상승', enabled_by_wide_anchor:'폭 고정 선수가 있을 때 가능', 'LCB covers LWB back':'좌측 CB가 좌측 윙백 뒤를 커버',
  'Short Passing':'짧은 패스', Counter:'역습', Balanced:'균형', High:'높음', Deep:'낮음', 'man-to-man':'대인 마킹',
};

/* 지표·내부 컬럼명 → 읽는 말 (title에 원문) */
export const METRIC_KR = {
  avg_x:'평균 전진 위치', avg_y:'평균 좌우 위치', tool_x:'좌우 위치', tool_y:'전진 위치', hit_points:'접점 수', hp:'접점 수',
  pos_class:'위치 분류', pos_label:'슬롯', fit_sim:'적합도', sample_n:'표본 경기 수', avg_rating:'평균 평점', map25:'위치 격자',
  cells_poss:'점유 시 격자', cells_def:'비점유 시 격자', map25_poss:'점유 시 격자', map25_def:'비점유 시 격자',
  ppda_v:'우리 PPDA', ppda_o:'상대 PPDA', def_x:'수비 액션 평균 위치', xg_v:'우리 xG', xg_o:'상대 xG', xg_op:'오픈플레이 xG',
  applied_status:'반영 상태', applied_note:'반영 메모', rationale:'근거', confidence:'신뢰도', verdict:'판정', team_code:'팀 코드',
  player_id:'선수 id', regime_id:'체제 id', role_id:'역할', game_version:'게임 버전', name_kr:'이름', lineup_pos:'라인업 위치',
};

export const isRaw = () => localStorage.getItem('reader_raw') === '1';
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;' }[c]));

export function roleLabel(role_id, focus, { pos = false } = {}){
  if (!role_id) return '';
  const kr = ROLE_KR[role_id];
  const code = role_id + (focus ? '/' + focus : '');
  if (isRaw() || !kr) return `<span class="hz" title="${esc(code)}">${esc(code)}</span>`;
  const head = pos ? `${POS_OF[role_id.split('_')[0]] ?? ''} ` : '';
  return `<span class="hz" title="${esc(code)}">${head}${kr}${focus ? ` <small class="dim">· ${FOCUS_KR[focus] ?? focus}</small>` : ''}</span>`;
}
export const focusLabel = f => f ? (isRaw() ? f : `<span class="hz" title="${esc(f)}">${FOCUS_KR[f] ?? f}</span>`) : '';
const slug = s => String(s ?? '').replace(/_/g, ' ');
export function claimLabel(field, value){
  if (isRaw()) return `<code>${esc(field ?? '')}</code>${value ? ' = ' + esc(value) : ''}`;
  const f = FIELD_KR[field] ?? slug(field);
  const v = value == null ? '' : (VALUE_KR[value] ?? (/^[a-z0-9_ -]+$/i.test(value) ? slug(value) : value));
  return `<span class="hz" title="${esc(field ?? '')}${value ? ' = ' + esc(value) : ''}"><b>${esc(f)}</b>${v ? `: ${esc(v)}` : ''}</span>`;
}

/* ── 산문 변환 ──
   ⑴ 역할/포커스 코드 → 한글  ⑵ 컬럼명 → 읽는 말  ⑶ 내부 참조(obs#·docs/·migration·G17·scripts/·커밋)는 본문에서 빼서 끝에 「참조」로 모은다.
   태그 안(<…>)은 건드리지 않는다. 반환 { html, refs }. */
const ROLE_RE = /\b(gk|cb|fb|dm|cm|cam|wm|w|st)_[a-z0-9]+(?:\/(Attack|Balanced|Defend|Build-Up|Roaming|Support|Versatile|Aggressive|Ball-Winning|Wide))?/g;
const METRIC_RE = new RegExp('(?<![\\w가-힣])(' + Object.keys(METRIC_KR).sort((a, b) => b.length - a.length).join('|') + ')(?![\\w])', 'g');
const REF_RES = [
  /\(?\bobs#\s?\d+(?:\s*[·~,~]\s*#?\d+)*\)?/g,
  /\(?\bdocs\/\d\d(?:-[\w-]+(?:\.md)?)?(?:\s*(?:§|「)?[\w⑴-⑽·~]*\s*(?:단계|절|표|」)?)?\)?/g,
  /\(?\bmigration\s?\d+\)?/g,
  /\(?\bG\d{1,2}\+?(?:이|가|는|을|로)?\s?(?:막는다|보고|검사|건수로 보고)?\)?/g,
  /\(?\b(?:scripts|core)\/[\w./-]+\.(?:py|js)\)?/g,
  /\(?\b(?:player_duties|prescriptions|observations)\s?(?:id\s?=|#)\s?\d+(?:\s*[·,]\s*\d+)*\)?/g,
  /\(?\bcommit\s[0-9a-f]{7}\)?/g,
  /\(?\bpulled\s?[0-9-]+\)?/g,
];
export function humanizeText(text){
  if (isRaw()) return { html: text, refs: [] };
  const refs = [];
  let t = text;
  // 참조는 자리표시자(\u0000)로 바꾼 뒤 **그 주변만** 정리한다. ⛔ 조각 전체를 trim하거나 앞머리 구두점을 지우면 안 된다 —
  //    이 함수는 태그(<b>) 사이의 텍스트 조각 단위로 불리므로, 전체 trim은 「낫다 — 25/26」의 공백·대시를 삭제해 「낫다25/26」을 만든다(2026-09-18 사고).
  for (const re of REF_RES) t = t.replace(re, m => { refs.push(m.replace(/^\(|\)$/g, '').trim()); return '\u0000'; });
  if (t.includes('\u0000')){
    t = t.replace(/\(\s*\u0000(?:\s*[—·,;:]\s*\u0000)*\s*\)/g, '\u0000')           // (obs#1 · obs#2) → 자리표시자 하나
         .replace(/\(\s*[—·,;:]?\s*\u0000\s*[—·,;:]?\s*/g, '(').replace(/\s*[—·,;:]?\s*\u0000\s*[—·,;:]?\s*\)/g, ')')   // ( — obs# · 본문) → (본문)
         .replace(/\s*[·,]\s*\u0000/g, '').replace(/\u0000\s*[·,]\s*/g, '')          // 「· obs#」 「obs# ·」 → 제거
         .replace(/[ \t]*\u0000[ \t]*/g, ' ')                                          // 남은 자리표시자는 공백 하나로
         .replace(/\(\s*\)/g, '').replace(/ {2,}/g, ' ').replace(/ ([,.)])/g, '$1');
  }
  t = t.replace(ROLE_RE, (m, _p, focus) => { const rid = m.split('/')[0]; const kr = ROLE_KR[rid];
    return kr ? `<span class="hz" title="${esc(m)}">${kr}${focus ? '(' + (FOCUS_KR[focus] ?? focus) + ')' : ''}</span>` : m; });
  t = t.replace(METRIC_RE, m => `<span class="hz" title="${esc(m)}">${METRIC_KR[m]}</span>`);
  return { html: t, refs: [...new Set(refs)] };
}
/* HTML 조각에 적용 — 태그는 건너뛰고 텍스트만. 참조는 끝에 한 줄로 모은다. */
export function humanize(html, { refsInline = true } = {}){
  if (!html || isRaw()) return html;
  const refs = [];
  const out = html.split(/(<[^>]*>)/).map(part => { if (part.startsWith('<')) return part;
    const r = humanizeText(part); refs.push(...r.refs); return r.html; }).join('');
  const u = [...new Set(refs)];
  return out + (refsInline && u.length ? ` <small class="refs-inline" title="내부 근거 참조">참조: ${u.map(esc).join(' · ')}</small>` : '');
}
export function refsChip(refs){
  const u = [...new Set(refs)];
  return u.length ? `<small class="refs-inline" title="내부 근거 참조">참조: ${u.map(esc).join(' · ')}</small>` : '';
}
/* 페이지 헤더 옆 토글 — 한 번 붙이면 된다 */
export function mountRawToggle(el){
  if (!el) return;
  const b = document.createElement('button');
  b.className = 'act ghost rawtoggle'; b.textContent = isRaw() ? '읽기용 표기로' : '원문 코드 표기로';
  b.title = '역할 코드·컬럼명·내부 참조를 원문 그대로 볼지 여부';
  b.addEventListener('click', () => { localStorage.setItem('reader_raw', isRaw() ? '0' : '1'); location.reload(); });
  el.appendChild(b);
}
