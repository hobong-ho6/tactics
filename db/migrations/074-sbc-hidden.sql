-- 074 목록에서 감출 SBC (2026-09-26 사용자 지시 「Sbc 이름 중에 업그레이드가 붙은 건 대부분
--    선수만 채우면 되는 것들이야. 브론즈, 실버, 골드, 79+ 업그레이드 모두 목록에서 제거」)
--
-- 왜 표로 두나: 「이 챌린지는 내가 알아서 한다」는 **사람 판단**이다. 코드에 이름 패턴을 박으면
--   ⑴ 새 업그레이드 SBC가 나올 때 **묻지도 않고 감춰지고** ⑵ 왜 안 보이는지 화면에서 알 수 없다.
--   ⇒ 행으로 적고 사유를 남긴다(포메이션 069·완료 068·고정 073과 같은 축 — 전부 사용자 판단).
--
-- ⛔ 지우지 않는다 — 감출 뿐이다. 조건·보상·판정은 그대로 남고 화면 머리에 **건수만 적는다**
--    (원클릭 제외와 같은 규약: 조용히 없애지 않는다).
CREATE TABLE IF NOT EXISTS fc_sbc_hidden(
  game_version    TEXT NOT NULL REFERENCES game_versions(code),
  challenge_ea_id INTEGER NOT NULL,
  reason          TEXT,
  source TEXT, added TEXT,
  PRIMARY KEY(game_version, challenge_ea_id)
);

INSERT INTO fc_sbc_hidden(game_version, challenge_ea_id, reason, source, added) VALUES
 ('FC27', 16, '업그레이드 — 등급만 맞춰 선수를 채우면 되는 것이라 해법을 낼 게 없다(Bronze Upgrade)',
  '사용자 지시(2026-09-26)', '2026-09-26'),
 ('FC27', 42, '업그레이드 — 같음(Silver Upgrade)', '사용자 지시(2026-09-26)', '2026-09-26'),
 ('FC27', 18, '업그레이드 — 같음(Gold Upgrade)', '사용자 지시(2026-09-26)', '2026-09-26'),
 ('FC27', 28, '업그레이드 — 같음(2x 79+ Upgrade)', '사용자 지시(2026-09-26)', '2026-09-26');
-- ⚠️ 34 「83+ Upgrade」는 이미 ONE_CLICK_CHALLENGE라 따로 빠져 있다 — 중복해 적지 않는다.
