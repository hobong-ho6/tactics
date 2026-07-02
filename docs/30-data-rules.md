# 데이터 수집·기록 규칙

## 스키마 (data/avl_analysis.db)

전체 설계는 [data/DESIGN.md](../data/DESIGN.md). 테이블 요약:

- `seasons(code,label)` — 시즌 코드는 `2025-26` 형식.
- `players` / `player_seasons` — 선수 정체성은 시즌 불변, 소속·등번호·출전시간은 시즌별.
- `matches(date,opponent,competition,venue,result,season,…)` — venue는 H/A/N.
- `appearances` — 선수×경기. 평점·포지션·역할·히트맵·출처·신뢰도.
- `streaks` + `match_streak` — 연승 등 구간 정의 (다대다).
- `game_roles` — FC 버전별 역할 라이브러리.
- `player_role_map` — 실측→게임 매핑 결과 (분석과 툴 사이의 계약).

## 표기 규약

- **competition**: 표준 명칭은 `Premier League`, `Europa League`, `FA Cup`, `EFL Cup`.
  스테이지·매치위크는 명칭에 붙이지 않고 필요하면 괄호 없이 별도 기록을 고려.
  ⚠️ 기존 데이터에 14가지 혼재 표기 있음 — 신규 입력은 표준 명칭만 사용, 기존 정규화는 백로그.
- **result**: 홈-원정 순 원문 스코어 (`4-2`). 승패는 venue와 조합해 판정.
  `W 4-0` 같은 접두 표기는 쓰지 않는다 (match 35가 예외로 남아있음 — 정규화 대상).
- **source**: URL 또는 API 엔드포인트를 그대로. 여러 소스는 ` ; `로 이어붙이고
  수집 날짜를 괄호로 남긴다.
- **confidence**: `HIGH / MEDIUM-HIGH / MEDIUM / QUALITATIVE` + 무엇이 어느 등급인지
  한 문장 근거. 항목별 등급이 다르면 나눠 적는다 (예: 평점 HIGH, 히트맵 MEDIUM).

## SofaScore 좌표 규약 ★중요

API 히트맵/평균위치 좌표는 0–100 스케일:

| 축 | 의미 |
|---|---|
| x | 공격 방향. 0=자기 골, 100=상대 골 |
| y | **낮음=오른쪽 측면, 높음=왼쪽 측면** |

- 홈/원정 관계없이 동일 (2026-07-02 검증: Cash(RB) y≈15–20, Digne(LB) y≈85–90,
  홈 3경기·원정/중립 2경기 교차 확인).
- 존 분할: x 3등분(def/mid/att) × y 3등분(right/centre/left, 33.34 경계).
- 툴(fc26-heatmap.html) 좌표는 x=좌우/y=공격방향으로 **축이 다르므로** 변환 주의.

## SofaScore 수집 절차

`api.sofascore.com`은 curl/서버 요청을 403으로 차단한다. **Chrome(claude-in-chrome)의
javascript_tool로 sofascore.com 페이지 컨텍스트에서 fetch** 하면 된다.

주요 엔드포인트:
```
/api/v1/search/all?q=<이름>                     → 선수/팀 ID
/api/v1/player/<pid>/events/last/<page>         → 선수의 과거 경기 목록 (event ID 확보)
/api/v1/event/<eid>/player/<pid>/heatmap        → 히트맵 좌표 배열 [{x,y},…]
/api/v1/event/<eid>/player/<pid>/statistics     → 그 경기 평점·분·터치·키패스
/api/v1/event/<eid>/lineups                     → 라인업·포메이션·전원 평점
```

수집 시 기록할 것: 존 분포 %(상위부터), 중심좌표(centroid), x/y 범위, 히트포인트 수,
터치 수 → `heat_zones`(존 요약)와 `heat_summary`(움직임 서술 + 수치)로.

주요 ID (25/26 확보분): Konsa 827679, Buendía 783126, Cash 833956, Digne 96538.
그 외 선수는 search로 확인하고, 자주 쓰는 ID는 여기에 추가해 갱신.

## 평점 권위 순서

SofaScore API 공식값 > SofaScore 뉴스 > 서드파티 매체 자체 평점.
하위 소스 값을 API로 교정하면 이전 값과 교정 사유를 `heat_summary` 또는
`confidence`에 남긴다 (예: 부엔디아 본머스전 9.0(Sportsdunia)→8.5(API)).
