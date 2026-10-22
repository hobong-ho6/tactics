/* 라이트/다크 선택 — 페이지가 그려지기 **전에** <html data-theme>를 정한다 (2026-10-22 사용자 요청 「토글 추가」).
   ⭐ 모든 페이지 <head>에서 theme.css 바로 뒤에 **동기(classic) 스크립트**로 읽는다 — 모듈(data.js)은 늦게 돌아
      라이트를 골라도 다크가 한 번 번쩍인다(FOUC).
   선택값 localStorage 'tactics_theme' = auto(기본 · 기기 설정을 따른다) | light | dark.
   ⛔ 색은 여기 없다 — theme.css :root(다크) / html[data-theme="light"](라이트) 한 곳이 정본이다. */
(function () {
  var KEY = 'tactics_theme';
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: light)') : null;
  function pref() {
    try { var v = localStorage.getItem(KEY); return v === 'light' || v === 'dark' ? v : 'auto'; } catch (e) { return 'auto'; }
  }
  function apply() {
    var p = pref(), el = document.documentElement;
    el.dataset.themePref = p;
    el.dataset.theme = p === 'auto' ? (mq && mq.matches ? 'light' : 'dark') : p;
  }
  apply();
  window.tacticsTheme = {
    pref: pref,
    /* 고르면 저장하고 다시 그린다 — 캔버스(피치·열지도)는 색이 바뀌어도 다시 안 그려지므로 새로 고친다(tokens.js와 같은 규칙) */
    set: function (p) { try { localStorage.setItem(KEY, p); } catch (e) {} location.reload(); },
  };
})();
