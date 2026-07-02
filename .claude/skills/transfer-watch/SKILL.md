---
name: transfer-watch
description: 아스톤 빌라 이적 루머 정기 감시 — TransferFeed 스캔 → 1~2티어 기자 크로스체크 → 강한 루머만 실측 분석 후 transfer_targets에 추가. 스케줄(매일 09/21시) 또는 수동(/transfer-watch)으로 실행.
---

# 빌라 이적 루머 감시 파이프라인

작업 디렉터리: `/Users/user/Documents/tactics`. 규칙은 CLAUDE.md와 docs/30-data-rules.md를 따른다.

## 1. 루머 소스 스캔

- `WebFetch`로 https://www.transferfeed.com/clubs/aston-villa/15 을 읽고
  **영입(incoming) 루머 선수 목록**을 추출한다 (선수명, 소속, 포지션, 루머 요지).
- 이미 `transfer_targets`에 있는 선수는 상태 변화(협상 단계 진전/무산)만 확인.
  `sqlite3 data/avl_analysis.db "SELECT name, slot, likelihood FROM transfer_targets WHERE window='2026-summer'"`

## 2. 1~2티어 기자 크로스체크

새 이름 또는 상태 변화 후보마다 `WebSearch`로 확인한다:
`"Aston Villa" "<선수명>" transfer` (+필요시 기자명).

- **1티어**: Fabrizio Romano, David Ornstein(The Athletic), Sky Sports 공식,
  BBC Sport, The Athletic 클럽 담당(Jacob Tanswell 등).
- **2티어**: Telegraph, Times, Guardian, Birmingham Mail(빌라 전담 John Townley 등),
  Football Insider 수준의 전국지·전담 기자.
- 그 외(어그리게이터, 팬사이트 단독)는 **3티어 — 크로스체크 실패로 간주**.

등급 규칙:
| likelihood | 조건 |
|---|---|
| HIGH | 1티어가 협상/합의 단계를 보도 ("advanced talks", "agreement", "here we go") |
| MEDIUM-HIGH | 1티어 관심 보도 또는 2티어 복수가 협상 보도 |
| MEDIUM | 2티어 1곳 이상이 구체적 관심 보도 |
| 크로스체크 실패 | DB에 추가하지 않음 (다음 실행에서 재확인만) |

## 3. 강한 루머(MEDIUM 이상) 분석 → DB 추가

docs/20-fc-game-system.md의 영입 후보 파이프라인 그대로:

1. SofaScore API에서 선수 검색 → 최근 6경기(45분+, 히트포인트 15+) 히트맵 수집.
   **API는 sofascore.com 페이지 컨텍스트에서만 접근 가능** (claude-in-chrome javascript_tool).
   Chrome 연결이 없는 헤드리스 실행이면: transfer_targets에 map25 없이 행을 만들고
   confidence에 `PENDING MEASUREMENT`를 남긴 뒤 종료 보고에 명시한다.
2. 5×5 툴 그리드(툴x=100−소파y, 툴y=소파x) + 중심좌표 + 평균 평점 계산.
3. 커널 적합도: fc26-heatmap.html의 MAPS를 파싱해 해당 슬롯 x에서 placedMap
   (미러+시프트) 후 코사인 — 기존 세션 스크립트 패턴 재사용.
4. `transfer_targets`에 INSERT OR REPLACE (window='2026-summer', 근거 URL·등급·캐비앳 포함).
   실측상 부적합 슬롯(예: 적합도 <0.4)은 제공 금지 행으로 기록.
5. fc26-heatmap.html `SQUAD_SLOTS`의 해당 슬롯에 `영입·<이름>` 옵션 추가
   (opt=처방, fit=계산된 적합 역할). 스쿼드 바 안내문 갱신.

## 4. 상태 변화 처리

- 무산/타클럽 이적 확정: likelihood를 `DEAD (사유)`로 갱신, SQUAD_SLOTS에서 제거.
- 빌라 이적 확정: likelihood `CONFIRMED`, 라벨 `(합류확정)`으로 변경.
  시즌 데이터가 쌓이면 players로 승격 (docs/20 규칙).

## 5. 완료 기준 (매 실행)

- 변경이 있으면: `scripts/db_dump.sh` 실행 → `git add -A && git commit`(메시지 접두 `data(transfer-watch):`) → `git push`.
- 변경이 없으면 커밋하지 않는다.
- 종료 보고: 스캔된 이름 수 / 크로스체크 통과·실패 / 추가·갱신된 행 / PENDING 여부.
