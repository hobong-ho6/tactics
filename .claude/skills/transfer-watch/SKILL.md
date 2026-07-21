---
name: transfer-watch
description: 아스톤 빌라 이적 루머 정기 감시 — TransferFeed 스캔 → 1~2티어 기자 크로스체크 → 강한 루머만 실측 분석 후 transfer_targets에 추가. 스케줄(매일 09/21시) 또는 수동(/transfer-watch)으로 실행.
---

# 빌라 이적 루머 감시 파이프라인

작업 디렉터리: `/Users/user/Documents/tactics`. 규칙은 CLAUDE.md와 docs/30-data-rules.md를 따른다.

## 1. 루머 소스 스캔

- `WebFetch`로 https://www.transferfeed.com/clubs/aston-villa/15 와
  https://www.fotmob.com/rumours?teamIds=10252 를 읽고
  **영입(incoming) 루머 선수 목록**을 추출한다 (선수명, 소속, 포지션, 루머 요지).
  두 소스 결과를 합쳐 중복 제거 후 크로스체크 대상으로 삼는다.
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

**보존 정책 (2026-07-21 확정)**: `transfer_targets`에는 **MEDIUM-HIGH 이상만 보존**한다.
MEDIUM·MEDIUM-LOW·LOW·DEAD로 판정/강등된 건은 DB에서 삭제하고, 그날의 근거는
리포트 파일(reports/transfer-watch/)에만 남긴다 (DB=실행 가능한 숏리스트, 리포트=전체 로그).
새 루머가 MEDIUM이면 리포트에 기록하되 DB에는 넣지 않는다.

## 3. 강한 루머(MEDIUM 이상) 분석 → DB 추가

docs/20-fc-game-system.md의 영입 후보 파이프라인 그대로:

1. SofaScore API에서 선수 검색 → 최근 6경기(45분+, 히트포인트 15+) 히트맵 수집.
   **API는 sofascore.com 페이지 컨텍스트에서만 접근 가능** (claude-in-chrome javascript_tool).
   Chrome 연결이 없는 헤드리스 실행이면: transfer_targets에 map25 없이 행을 만들고
   confidence에 `PENDING MEASUREMENT`를 남긴 뒤 종료 보고에 명시한다.
2. 5×5 툴 그리드(툴x=100−소파y, 툴y=소파x) + 중심좌표 + 평균 평점 계산.
3. 커널 적합도: fc26-heatmap.html의 MAPS를 파싱해 해당 슬롯 x에서 placedMap
   (미러+시프트) 후 코사인 — 기존 세션 스크립트 패턴 재사용.
4. `transfer_targets`에 INSERT OR REPLACE (window='2026-summer', 근거 URL·등급·캐비앗 +
   **`short_label` 필수** — 툴에 쓸 짧은 한글/영문 이름, 예: `Matías Soulé` → `소울레`).
   실측상 부적합 슬롯(예: 적합도 <0.4)은 애초에 그 슬롯 행을 만들지 않는 것으로 대신한다.
5. **fc26-heatmap.html은 손으로 고치지 않는다.** DB 갱신 후
   `python3 scripts/sync_transfer_ui.py`를 실행하면 `TRANSFER_TARGETS`/`TRANSFER_OUTGOING`
   미러 배열이 재생성되고, 툴의 `injectTransferCandidates()`가 런타임에 SQUAD_SLOTS/
   PLAYER_BEST/XI_POOL로 자동 주입한다 (2026-07-14 리팩터, docs/20-fc-game-system.md 참조).

## 4. 상태 변화 처리

- 무산/타클럽 이적 확정: likelihood를 `DEAD (사유)`로 갱신 — `sync_transfer_ui.py` 재실행 후
  자동으로 SQUAD_SLOTS/XI_POOL 후보에서 빠진다(injectTransferCandidates가 DEAD 필터).
- 빌라 이적 확정: likelihood `CONFIRMED`로 갱신. 라벨 `(합류확정)`은 툴이 런타임에 자동
  붙이므로 손으로 안 바꿔도 됨. 시즌 데이터가 쌓이면 players로 승격 (docs/20 규칙).

## 4-1. 빌라 선수 유출(outgoing) 루머 확인

영입 스캔과 별도로, 빌라 기존 선수(`players` 테이블)의 이적설도 확인한다.

- `WebSearch`로 `"Aston Villa" "<선수명>" transfer` 또는 일반적으로
  "Aston Villa outgoing/exit rumours"를 스캔해 주전급 선수 유출 루머를 찾는다.
- 1~2티어 크로스체크는 §2와 동일 기준 적용.
- 통과한 건은 `transfer_outgoing(window, player_id, dest_club, likelihood, rationale,
  source, confidence)`에 INSERT OR REPLACE (player_id는 `players.id` FK).
  히트맵/커널 적합도 분석은 하지 않는다 — 이 테이블은 역할 적합성이 아니라 유출 위험을 추적한다.
- 이적 확정 시 likelihood `CONFIRMED`로 갱신 (player_seasons 등 승격은 별도 판단).

## 4-2. 일일 리포트 생성 (매 실행 필수)

DB 갱신과 별도로, **그날 수집한 기사·업데이트를 모은 리포트를 파일로 남긴다.**
`reports/transfer-watch/<YYYY-MM-DD>.md`에 작성한다(`<YYYY-MM-DD>`는 실행일).
같은 날 재실행이면 같은 파일을 **덮어쓰지 않고**, 파일 안에 `## <HH>시 실행` 섹션을 추가한다.

리포트는 스크립트가 아니라 이 실행이 직접 쓴다 — 원문 기사 서술은 WebSearch 결과에만
있고 DB 필드로는 복원되지 않기 때문. DB의 `rationale`/`source`와 그날 검색한 기사 내용을
결합해 아래 템플릿을 채운다.

```markdown
# 빌라 이적 감시 리포트 — <YYYY-MM-DD>

## 요약
- 스캔: 영입 ~N건 / 유출 ~M건 (소스: TransferFeed)
- 오늘 변동: 신규 X · 갱신 Y · 무산/DEAD Z

## 신규·갱신 (선수별)
### <선수> (<현소속>, <슬롯>) — <등급 old→new>
- 기사 요지: <그날 기사 1~3줄, 이적료·단계·경쟁 클럽>
- 출처: <기자/매체 (티어)>, <URL>
  (유출 건도 같은 형식으로. 실측 미수행 시 `실측 PENDING` 명시)

## 크로스체크 실패·보류
- <이름>: <사유 — 팬사이트 단독 / 미크로스체크 / 링크 소멸>

## 기존 행 재확인 (변동 없음)
- 영입: <등급 유지 요약>
- 유출: <등급 유지 요약>

## PENDING MEASUREMENT
- <이름(슬롯)> …
```

변동이 전혀 없는 날도 리포트는 남긴다(그날의 기사 로그·재확인 기록 보존).

## 5. 완료 기준 (매 실행)

- **DB 변경이 있으면**: `python3 scripts/sync_transfer_ui.py`(fc26-heatmap.html 미러 갱신)
  → `scripts/db_dump.sh`(dump 재생성) 실행. DB 변경이 없으면 이 둘은 건너뛴다.
- **리포트는 매 실행 작성**(§4-2) 후, 아래처럼 **파일을 명시 스테이징**해서 커밋한다.
  `git add -A`는 쓰지 않는다 — 저장소에 `.claude/settings.json`(Figma PAT 등) 등 커밋 금지
  파일이 있어 푸시가 차단된다:
  ```
  git add reports/transfer-watch/ data/avl_analysis.db data/dump/ fc26-heatmap.html
  git commit -m "data(transfer-watch): <요약> (<YYYY-MM-DD>)"
  git push
  ```
  (DB 변동이 없어 리포트만 있는 날도 리포트 파일만 스테이징해 커밋한다.)
- 종료 보고(터미널): 스캔된 이름 수 / 크로스체크 통과·실패 / 추가·갱신된 행 / PENDING 여부
  + **리포트 파일 경로**.
