# 웹페이지 디자인·UX 검토 (2026-10-22)

> 검토 방법: 미러(`/private/tmp/tactics-preview/site` · `heatmap` 프리뷰 8123)에서 전 페이지 11개를 **데스크톱 1280px · 모바일 375px** 두 폭으로 확인.
> 모바일은 「뷰포트 폭이 375를 넘는가」를 JS로 전수 측정(`innerWidth`·`scrollWidth`)해 표를 안 두른 요소를 자동으로 잡았다 —
> 눈으로 본 것보다 이 측정이 먼저다. 콘솔 오류·HTTP는 `scripts/check_pages.py`(전 페이지 ✅ 이상 없음 · 알려진 FC25.json 404 제외).
> 범위: `site/` HTML·CSS 문구와 레이아웃. ⛔ `loadKernels('FC26')` 5곳·`kernel.js`·`data.js` 버전 배관은 다른 작업(FC27 승계)이 바꾸므로 손대지 않았다. DB·export 무변경.

## 발견과 조치

| 페이지 | 문제 | 심각도 | 조치 |
|---|---|---|---|
| 스쿼드 · 선수 비교 · 이적 · 리포트 · 게임 시스템 | **모바일에서 화면 전체가 축소된다** — `.scrollx`를 안 두른 표(`#tbl` · `#rank` · `#in` · `#sheet`/`#canon`/`#profile` · `#chg`/`#roles`)가 뷰포트를 **516~759px**로 밀어 글자가 절반 크기로 보였다 | **높음** | ✅ 고침 — 표마다 감싸는 대신 `@media(max-width:700px){.panel{overflow-x:auto}}` 한 줄로 **패널이 스크롤 컨테이너**가 되게 했다(불변규칙 13 ① — 빠뜨리는 구조 제거). 전 페이지 재측정 375/375. 툴팁 `.gl-tip`은 body 자식이라 안 잘리고, 절대 위치 요소는 전부 자기 피치·카드 안(확인) |
| 경기 분석 | 모바일에서 **경기 선택 셀렉트가 오른쪽으로 잘린다**(`min-width:230px` + 긴 옵션 문구) · 뷰포트 404px | **높음** | ✅ 고침 — 모바일에서 라벨을 flex 한 줄로, 셀렉트 `flex:1·min-width:0·max-width:100%` |
| 경기 분석 | 모바일에서 **sticky 선택 막대(셀렉트 4 + 목차)가 812px 화면의 1/3을 덮은 채 따라다닌다** | 중간 | ✅ 고침 — ≤700px에서 `position:static` · 목차 점프 `scroll-margin-top` 130→12px |
| 전 페이지 | **제목 위계** — `h1 small`·`h2 small`이 굵기와 거의 같은 크기를 물려받아(0.83em·bold) 부제가 제목처럼 보였고, 모바일에선 h1이 3줄 굵은 문단이 됐다 | 중간 | ✅ 고침 — `h1 small 13px/400` · `h2 small 12px/400` |
| 헤더(모바일) | 전체 메뉴(얼티밋팀·게임 시스템·매뉴얼)가 줄바꿈되면 `border-left` 세로선만 떠 있었다 | 낮음 | ✅ 고침 — ≤700px에서 선 제거 |
| 매뉴얼 | 제목 「실축 → **FC26** 구현 매뉴얼」 · 본문 「FC26은 역할 37 × …」 — 현행 FC27인데 문구가 낡음 | 중간 | ✅ 고침 — 「FC 구현 매뉴얼 … 현행 버전 FC27(FC26 데이터는 보존)」 · 「FC27(FC26 역할표 전항 일치로 승계 · 2026-10-22)은 …」 |
| 허브 | 부제 「감독·팀 페어 **3개** · (FC26 → FC27)」 — 카드는 4개(ATM 포함) | 낮음 | ✅ 고침 — 「감독·팀 페어 4 · 현행 게임 버전 FC27(FC26 데이터는 보존)」 |
| 히트맵 비교 | 안내문 「kernels/**FC26**.json」 하드코딩 문구 | 낮음 | ✅ 고침 — 「kernels/{현행 게임 버전}.json」 |
| 게임 시스템 | h1 부제 「역할 커널 **FC26**」 — `loadKernels('FC26')`에 묶인 값 | 중간 | ⏸ 남김 — 다른 작업(FC27 승계·`loadKernels(current)`)이 고치면 함께 바뀐다 |
| 리포트 | 설정 시트가 **Short Passing · 헤밍스 LM · 완비사카 RB** 등 낡은 선발(`prescriptions opt:*` FC26 승계분)을 「게임에 그대로 입력」으로 보여 준다 — 화면 문제가 아니라 **데이터** 문제 | 중간 | ⏸ 남김 — 구현 검토 리포트(`2026-10-22-fc27-avl-implementation-review.md` 1.3)에서 선발층 재생성으로 처리 |
| 리포트 | 「현재 설정」 고르기가 **kind 정렬 마지막 행**이라 FC27 26/27에 `optimal`(#46 · Balanced/Balanced/52)이 생긴 뒤에도 알파벳상 뒤인 `projected:emery-2627`(Short Passing · 폐기값)을 집었다 | **높음** | ✅ 고침 — `currentGameVersion()`(data.js)으로 **현행 버전·최신 시즌 `optimal` 행 1순위**, 없으면 종전 폴백. 확인: 리포트 「4-2-3-1 Wide · 빌드업 Balanced · 수비 Balanced · 라인 52 · 전술 코드 7ZTFKBu$37p7 · (optimal, 2026-27)」 · 스쿼드 본문 Short Passing 0건 · 바이킹전 경기 프리셋 Balanced/Balanced/52 |
| 선수 분석 | 데스크톱 상단 「부상 doubt · 복귀 예상 · 추가 경기 금지…」 경고 블록이 선수 카드보다 먼저 와서 **첫 화면이 경고로 시작**한다 | 낮음 | ⏸ 남김 — 사용자가 10-16에 「부상·정보 최신」을 1순위로 요구한 축이라 의도된 배치로 판단. 순서 변경은 사용자 판단 |
| 이적 | 종합 총평이 긴 산문 한 덩어리(스크린샷 기준 1화면 전체) — 요지/근거 구분이 약함 | 낮음 | ⏸ 남김 — 내용은 DB `transfer_*` 산문이라 화면에서 자를 수 없다(⛔ 산문 자르기 금지 규약). 정형 필드 분리는 데이터 작업 |
| 얼티밋팀 | 모바일 뷰포트 385px(10px 초과) — 벤치 카드 줄(`.fc-benchrow`)은 의도된 가로 스크롤 | 낮음 | ⏸ 남김 — 체감 없음(전체 축소 아님) |
| 경기 분석 · 리포트 · 이적 | `glossary.js`·`labels.js`가 **`?v=` 있는 URL과 없는 URL로 두 번** 로드된다(모듈 인스턴스 2개 · 툴팁 리스너는 `body.dataset` 가드로 중복 방지됨) | 낮음 | ⏸ 남김 — `prose.js`가 무버전으로 import하는 구조. G9는 `kernel.js`·`pitch.js`만 본다. 정리하려면 import 경로 통일(코드 작업) |
| 도구 | `python3 scripts/check_pages.py`가 「playwright 없음」으로 멈춘다 — `.venv/bin/python`과 시스템 `python3`의 `resolve()`가 같은 프레임워크 바이너리를 가리켜 **재실행 분기를 못 탄다**. `.venv/bin/python scripts/check_pages.py`는 정상 | 낮음 | ⏸ 남김 — `scripts/` 범위 밖. 이 PC(AL02359162)엔 playwright·chromium을 .venv에 설치해 뒀다 |

## 경기 분석 화면 — 정형 축 노출 확인

요약(`#summary`) → 경기 차트(`#viz`) → **가설 판정(`#hypPanel`)** → 부상(`#injPanel`) → 경기 프리셋 → 선수별 → 전술 분석 4칸 순서로 전부 보인다. 목차(히트맵·팀 스탯·경기 요약·경기 차트·가설·부상·프리셋·선수·전술·영상·원문)가 실제 패널에서 생성돼 빠진 항목 없음. 모바일에선 목차가 가로 스크롤 한 줄(의도).

## 바꾼 파일

- `site/assets/style.css` — 끝에 블록 2개 추가(제목 위계 · ≤700px 패널 스크롤/선택 막대/헤더)
- `site/manual.html` — h1 · §2 문구
- `site/index.html` — h1 부제
- `site/heatmap.html` — 안내문
- `site/report.html` — 「현재 설정」 선택을 현행 버전 `optimal` 우선으로(import에 `currentGameVersion` 추가)

## 검증

- 모바일 375px 전수 재측정: index·squad·heatmap·compare·transfer·report·game·match-report·player(id=59)·manual **전부 375/375** · evolutions 385(벤치 스크롤).
- 콘솔: 알려진 `kernels/FC25.json` 404 외 오류 없음. `check_pages.py` 전 페이지 ✅(렌더 길이 정상).
- 게이트: G9 ✅ · G10 ✅ · G22 ✅ · G38 ✅ (G34는 바이킹전 D+2·D+3 예약 누락 — 이 작업과 무관).
