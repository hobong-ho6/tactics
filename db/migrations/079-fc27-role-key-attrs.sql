-- 079 역할 가중표 FC27판 — 가속·질주 비중 상향 (2026-09-26 사용자 지시 「가중표를 FC27 조정을 반영해」)
--
-- 근거(EA 1차 verbatim · `game_system_changes` FC27/attributes):
--   「We've slightly reduced the impact of AcceleRATE profiles on a player's running performance,
--     bringing Explosive, Controlled, and Lengthy players a little closer together … greater emphasis
--     on a player's **Acceleration and Sprint Speed** Attributes」
--   (AcceleRATE 프로필이 달리기 성능에 미치는 영향을 약간 줄여 세 유형을 가깝게 만들었고,
--    **가속력·질주 속도 속성**의 비중을 높였다)
--
-- ⇒ 유형(AcceleRATE)의 몫이 줄고 **원값(가속·질주)의 몫이 늘었다**. 가중표는 원값을 재는 표이므로 올린다.
--
-- ⛔⛔ **FC26 행은 건드리지 않는다**(불변규칙 2 — 새 버전 = 행 추가). FC26은 실축 재현 축이고
--    이 변경은 FC27 게임플레이 조정이다. 두 버전이 같은 표를 쓰면 어느 게임 얘긴지 잃는다.
--
-- ⚠️ **이미 있는 역할의 가속·질주만 +1 한다**(상한 3). EA는 「속성 비중이 커졌다」고 했지 
--    「새 역할에도 중요해졌다」고 하지 않았다 — 없던 역할에 넣는 건 우리 발명이다.
-- ⚠️ 가중 자체는 여전히 **판단값(MEDIUM)** — EA가 역할별 가중을 공개한 적은 없다. 바뀐 건 근거의 방향뿐이다.
--
-- 영향: `st_advanced` 가속 2→3 · 질주 2→3 ⇒ 마조 케미 스타일 순위에서 Hunter가 Finisher에 근접한다.

INSERT INTO game_role_key_attrs(game_version, role_id, attr, weight, source, confidence)
SELECT 'FC27', role_id, attr,
       CASE WHEN attr IN ('가속','질주 속도') THEN MIN(3, weight + 1) ELSE weight END,
       source || ' → FC27판(2026-09-26): 가속·질주 +1(상한 3). '
       || 'EA Beta Feedback Update 「greater emphasis on a player''s Acceleration and Sprint Speed Attributes」',
       'MEDIUM — EA 미공개 판단값. 가속·질주 상향의 **방향**만 EA 1차(HIGH)로 뒷받침된다(크기는 우리 판단).'
  FROM game_role_key_attrs WHERE game_version='FC26';
