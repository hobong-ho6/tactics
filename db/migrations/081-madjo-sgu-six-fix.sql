-- 081 마조 「빛나는 스트라이커」 4행의 6대 스탯 정정 + 현재 29속성 동기화 (2026-09-26)
--
-- ⛔⛔ **무엇이 틀렸나** — 진화 기록인데 **스탯이 내려가 있었다**:
--     1단계 PAC 75 → **70** · SHO 73 → **69**. 진화는 스탯을 내리지 않는다.
--
-- ⭐ 원인은 「현재 카드」가 원장에 **두 벌** 있었고 한 벌만 갱신된 것이다.
--    `fut_club.py evolve`는 `current_ovr`·`current_six`만 올리고 `current_attrs`(29속성)는
--    **아무도 올리지 않았다**. 화면은 before를 `current_six`에서, after를 `current_attrs`에
--    보상을 얹어 계산한다 ⇒ 두 벌이 갈린 순간 after가 before보다 낮게 적힌다.
--    실측: 클릭 시점의 `current_ovr`=73(최전방의 역설 1·2단계 반영)인데
--          `current_attrs`는 **카드 인쇄값**(가속 65·질주 74) 그대로였다.
--
-- ⭐⭐ 구조를 없앴다(불변규칙 13 ①). 같은 회차에 함께 고친다:
--    ⑴ `core/futgg_attrs.py`에 `apply_upgrades`·`face_of`를 신설 — 보상 적용·6대 환산의 단일 정본.
--    ⑵ `fut_club.py evolve`가 **서버에서** `current_attrs`에 보상을 얹어
--       **attrs·six·ovr 셋을 한꺼번에** 갱신한다. 갈릴 수 있는 구조가 사라진다.
--    ⑶ 그래도 어긋나면 **게이트가 멈춘다** — 6대나 OVR이 하나라도 내려가면 기록을 거부한다.
--    ⑷ 화면은 스탯을 보내지 않는다. **갈림길 번호(`pick`)만** 알려 준다.
--
-- 아래는 이미 적힌 4행의 정정이다. **적용 사실 자체는 옳다**(사용자가 인게임에서 완주했다) —
-- 고치는 것은 우리가 계산한 숫자뿐이라 행을 지우지 않고 값만 다시 쓰고 사유를 notes에 남긴다.
-- ⚠️ 값은 여전히 **등급 B(우리 계산)** 다 — 다음 클럽 싱크의 EA 실측이 정본이다.
-- ⚠️ 최전방의 역설 3단계(evo 2508 lv3)는 기록된 값이 맞아 건드리지 않는다.
UPDATE fut_evolution_log SET ovr_before=73, ovr_after=80,
       six_before='{"PAC": 75, "SHO": 73, "PAS": 56, "DRI": 67, "DEF": 22, "PHY": 74}', six_after='{"PAC": 75, "SHO": 74, "PAS": 57, "DRI": 67, "DEF": 22, "PHY": 74}',
       source='migration 081 재계산 (core/futgg_attrs.py · current_attrs 기준)',
       notes=notes || ' ⚠️ 2026-09-26 정정: 최초 기록은 화면이 낡은 29속성으로 계산해 스탯이 거꾸로 내려갔다(PAC 75→70). migration 081에서 EA 실측 29속성 기준으로 다시 계산했다.'
 WHERE club_player_id=30 AND evo_id=2494 AND level=1 AND is_void=0;
UPDATE fut_evolution_log SET ovr_before=80, ovr_after=80,
       six_before='{"PAC": 75, "SHO": 74, "PAS": 57, "DRI": 67, "DEF": 22, "PHY": 74}', six_after='{"PAC": 75, "SHO": 80, "PAS": 58, "DRI": 70, "DEF": 22, "PHY": 77}',
       source='migration 081 재계산 (core/futgg_attrs.py · current_attrs 기준)',
       notes=notes || ' ⚠️ 2026-09-26 정정: 최초 기록은 화면이 낡은 29속성으로 계산해 스탯이 거꾸로 내려갔다(PAC 75→70). migration 081에서 EA 실측 29속성 기준으로 다시 계산했다.'
 WHERE club_player_id=30 AND evo_id=2494 AND level=2 AND is_void=0;
UPDATE fut_evolution_log SET ovr_before=80, ovr_after=80,
       six_before='{"PAC": 75, "SHO": 80, "PAS": 58, "DRI": 70, "DEF": 22, "PHY": 77}', six_after='{"PAC": 79, "SHO": 80, "PAS": 59, "DRI": 74, "DEF": 22, "PHY": 77}',
       source='migration 081 재계산 (core/futgg_attrs.py · current_attrs 기준)',
       notes=notes || ' ⚠️ 2026-09-26 정정: 최초 기록은 화면이 낡은 29속성으로 계산해 스탯이 거꾸로 내려갔다(PAC 75→70). migration 081에서 EA 실측 29속성 기준으로 다시 계산했다.'
 WHERE club_player_id=30 AND evo_id=2494 AND level=3 AND is_void=0;
UPDATE fut_evolution_log SET ovr_before=80, ovr_after=80,
       six_before='{"PAC": 79, "SHO": 80, "PAS": 59, "DRI": 74, "DEF": 22, "PHY": 77}', six_after='{"PAC": 79, "SHO": 81, "PAS": 61, "DRI": 75, "DEF": 22, "PHY": 77}',
       source='migration 081 재계산 (core/futgg_attrs.py · current_attrs 기준)',
       notes=notes || ' ⚠️ 2026-09-26 정정: 최초 기록은 화면이 낡은 29속성으로 계산해 스탯이 거꾸로 내려갔다(PAC 75→70). migration 081에서 EA 실측 29속성 기준으로 다시 계산했다.'
 WHERE club_player_id=30 AND evo_id=2494 AND level=4 AND is_void=0;
UPDATE fut_club_players SET current_attrs='{"가속": 80, "질주 속도": 79, "공격 위치 선정": 82, "결정력": 83, "슈팅력": 82, "중거리슛": 78, "발리 슛": 78, "페널티킥": 75, "시야": 62, "크로스": 44, "프리킥 정확도": 47, "짧은 패스": 72, "긴 패스": 61, "커브": 65, "민첩성": 74, "균형 감각": 67, "반응력": 76, "볼컨트롤": 76, "드리블": 76, "침착": 70, "차단력": 19, "헤딩 정확도": 68, "수비 위치 선정": 14, "스탠딩 태클": 18, "슬라이딩 태클": 13, "점프": 83, "체력": 63, "힘": 91, "공격성": 56, "다이빙": 7, "핸들링": 12, "킥": 8, "포지셔닝": 14, "반사신경": 12}',
       current_six='{"PAC": 79, "SHO": 81, "PAS": 61, "DRI": 75, "DEF": 22, "PHY": 77}', current_ovr=80, updated='2026-09-26' WHERE id=30;
