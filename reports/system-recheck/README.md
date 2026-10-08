# 시스템 재조사 회차 리포트

스케줄 작업 `fc27-system-recheck`(매월 1일·15일 14:00)가 발행한다. 파일명은 `YYYY-MM-DD.md`.

## 패치 감시와의 역할 분담 — 섞지 않는다

| | `fc27-patch-watch` (매일 10:00) | `fc27-system-recheck` (1일·15일 14:00) |
|---|---|---|
| 보는 것 | **EA 1차 자료만**(등급 A) | **B**(데이터마이닝) · **C**(통제 실측) · **D**(통설) |
| 질문 | 「EA가 무엇을 바꿨나」 | 「우리가 아직 모르는 것이 채워졌나」 |
| 산출 | `reports/patch-watch/` | `reports/system-recheck/` + 실측 프로토콜 |

- **변경이 없어도 발행한다** — 「확인했고 없었다」와 「확인하지 않았다」는 다른 상태다.
- 사실의 정본은 여기가 아니라 **`game_system_changes`**(웹: 게임 시스템 → 시스템 분석)다.
- 절차 정본은 `/Users/user/.claude/scheduled-tasks/fc27-system-recheck/SKILL.md`.

## 출발점

- 결손 목록의 원본: [reports/research/2026-09-21-fc27-system-stats-summary.md](../research/2026-09-21-fc27-system-stats-summary.md) §5·§6
- 그 리포트가 적은 재수집 시점: **2026년 10월 중순**(FC27 출시 2~4주 후)
- 1차 시도(2026-10-07 · `game_system_changes` #43)는 **새 A/B/C 0건**이었다 — 웹 자료만으로는 안 채워진다는 것이
  이미 한 번 확인됐다. 그래서 이 루틴은 **우리가 직접 재는 쪽(C등급)**에 무게를 둔다.
