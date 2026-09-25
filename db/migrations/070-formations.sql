-- 070 FC27 포메이션 정본 (2026-09-25 사용자 지시 「선택 가능한 포메이션은 FC27에서 지원하는 모든 포메이션」)
--
-- 왜: 종전엔 솔버·화면이 **4종을 코드에 박아** 쓰고 있었다(4-2-3-1/4-4-2/4-3-3/3-5-2).
--   실제 FC27은 **29종**이고, SBC는 챌린지마다 포메이션이 고정이므로 목록이 모자라면 기록 자체가 불가능하다.
--
-- 원천: fut.gg 웹앱 번들의 포메이션 배열(스쿼드 빌더가 쓰는 것) —
--   `{id, index, name, uniquePositionSlots, generalPositionSlots}`.
--   · `general…`(등급 A · 번들 enum으로 확인) = **그 칸에 설 수 있는 카드 포지션**. 케미 판정은 이 값으로 한다.
--       확인된 enum: 0 GK · 2 RWB · 3 RB · 5 CB · 7 LB · 8 LWB · 10 CDM · 12 RM · 14 CM · 16 LM ·
--                    18 CAM · 21 CF · 23 RW · 25 ST · 27 LW
--   · `unique…` = 좌우까지 가른 표시용 id(LCB/RCB…). 이름표는 **EA 통용표**라 등급 D로 적는다.
CREATE TABLE IF NOT EXISTS fc_formations(
  game_version TEXT NOT NULL REFERENCES game_versions(code),
  ea_id   INTEGER NOT NULL,
  name    TEXT NOT NULL,
  slots   TEXT NOT NULL,          -- JSON [{i, uniq, gen, label, x, y}] — x·y는 우리 피치 좌표(%)
  source TEXT, confidence TEXT, pulled TEXT NOT NULL,
  PRIMARY KEY(game_version, ea_id)
);
