-- 096 국가대표 팀 표식 (2026-10-02 · G18 「친선·대표팀 제외」 구멍을 구조로 막는다)
--
-- 왜: `measured` 집계 규칙은 「클럽 공식전만」인데, 그 걸러내기를 **대회 이름 목록**으로 해 왔다
--   (G18·audit_measured_samples.py에 같은 목록이 두 벌 · 대표팀은 'FIFA World Cup' 하나뿐).
--   2026-10-02 A매치 창(네이션스리그·AFCON 예선)을 적재하자 G18 재집계에 대표팀 경기가 섞여
--   완비사카 RB(#493)·루제리 LB(#507)가 불일치로 떴다 — 데이터가 아니라 **규칙 구현**의 구멍이다.
--   ⛔ 대회 이름으로는 못 가른다: 'Euro'는 유로파리그에, 'Qual'은 챔스 예선에 걸린다(실측).
--   ⇒ 「대표팀」을 **팀의 속성**으로 둔다. 판정은 core.aggregate.club_official_sql() 한 곳(불변규칙 13 ②).
ALTER TABLE teams ADD COLUMN is_national INTEGER NOT NULL DEFAULT 0;
UPDATE teams SET is_national=1 WHERE code IN
  ('ARG','BRA','CAN','CIV','COD','CZE','ECU','EGY','ENG','ESP','FRA','GER','HUN','ITA','JAM','JPN','LUX',
   'NED','NIR','NOR','POL','POR','SCO','SEN','SRB','SUI','SWE','URU','USA');
