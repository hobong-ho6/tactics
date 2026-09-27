-- 086 마조 처방 포커스 Attack → Versatile (2026-09-27 사용자 판단)
--
-- 왜: 사용자 질문 「마조인 경우엔 st 다재다능으로 하고」 — 커널로 대조해 확정했다.
--   `st_advanced`의 두 포커스는 최전방 점유가 거의 같다:
--     · Attack    행0 = 0 · .6 · 1.0 · .6 · 0
--     · Versatile 행0 = .3 · .6 · 1.0 · .6 · .3     ⇒ **Attack의 상위집합**(중앙 1.0 유지 + 양 끝 .3)
--   갈리는 것은 **페널티뿐**이다: Attack = `Limited Width` · Versatile = `Build-Up Support`.
--
-- ⭐ 판정 근거: **그 선수에게 무해한 페널티를 고른다.**
--   마조는 짧은 패스 70 · 볼컨트롤 76으로 **빌드업 관여가 원래 약하다** ⇒ `Build-Up Support(−)`는 사실상 무해.
--   반대로 `Limited Width(−)`는 폭을 실제로 못 쓰게 만드는 손해다.
-- ⚠️ 이 판정은 **판단값**이다 — 「몇 골 더 넣는다」는 통제 실측이 없다(커널 점유는 우리 인코딩).
--
-- ⛔ 잭슨과 섞지 않는다: 잭슨은 체력 76·공격성 72라 `Support`가 맞고 마조는 체력 63이라 그 페널티를 정통으로 맞는다.
--    ⇒ **ST에 누가 서느냐에 따라 포커스가 달라진다**는 것이 이번 결론이다.
UPDATE prescriptions
   SET focus = 'Versatile',
       rationale = COALESCE(rationale || ' ', '') ||
         '⚠️ 2026-09-27 포커스 정정(Attack→Versatile · 사용자 판단): st_advanced의 Versatile은 Attack의 '
         || '상위집합이고(중앙 1.0 유지 + 양 끝 .3) 갈리는 것은 페널티뿐이다 — Attack=Limited Width · '
         || 'Versatile=Build-Up Support. 마조는 짧은 패스 70·볼컨 76이라 빌드업 관여가 원래 약해 후자가 무해하다. '
         || '⛔ 잭슨(체력 76·공격성 72)은 Support가 맞다 — ST에 누가 서느냐로 포커스가 갈린다.'
 WHERE id = 506 AND player_id = 61 AND role_id = 'st_advanced';
