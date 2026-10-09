-- 104 역할 근거 — 커뮤니티 체감·실사용 증언 (2026-10-10 사용자 지시 「지금은 너무 EA 내용을 보여주는 것 같아」
--   「커뮤니티나 실제 체감 등의 자료를 더 수집해서 보완」).
--
-- 왜: 역할 장면 해설(migration 103)이 EA 원문만 근거로 삼아 「써 보니 어떻더라」가 없었다.
--   우리 인게임 실측(ingame_captures · v_kernel_fidelity)은 13조합뿐이라 나머지를 커뮤니티 증언으로 메운다.
-- ⭐ 한 행 = 출처 하나의 관찰 하나. 원문 인용 + 한국어 번역 병기(불변규칙 11) · 근거 등급(불변규칙 12).
-- ⛔ 같은 글의 복제는 교차검증이 아니다 — 한 행만 둔다.
-- role_id는 FC26 카탈로그 id로 잇는다(역할 목록이 FC25~27에서 이름이 같다). 관찰 버전은 observed_gv에 따로 둔다.
CREATE TABLE game_role_evidence(
  id            INTEGER PRIMARY KEY,
  role_id       TEXT NOT NULL,            -- game_roles.role_id (FC26 카탈로그)
  focus         TEXT,                     -- NULL = 역할 전체에 대한 관찰
  claim_kr      TEXT NOT NULL,            -- 무엇을 관찰했다는가(한국어 요약)
  quote_orig    TEXT,                     -- 원문 인용(짧게 · 원어 그대로)
  quote_kr      TEXT,                     -- 한국어 번역
  lang          TEXT,                     -- en·ko·es·de·ja·it·fr·pt …
  source_name   TEXT,                     -- 'Reddit r/EASportsFC' 등
  source_url    TEXT NOT NULL,
  observed_gv   TEXT,                     -- FC25·FC26·FC27·unknown
  observed_date TEXT,
  grade         TEXT NOT NULL CHECK(grade IN ('C','D')),  -- C 통제 실측 · D 일화·의견·가이드
  snippet_only  INTEGER DEFAULT 0,        -- 1 = 검색 요약문만 봄(본문 미확인)
  contradicts_ea INTEGER DEFAULT 0,       -- 1 = EA 설명과 어긋나는 관찰
  notes         TEXT,
  collected     TEXT NOT NULL,
  source        TEXT,                     -- 수집 경로(조사 회차)
  UNIQUE(role_id, focus, source_url, quote_orig)
);
