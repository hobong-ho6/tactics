---
name: club-sync
description: 내 얼티밋 구단 동기화 — fut.gg GG Club에서 현재 스쿼드·보유 카드·케미 스타일·진화 상태를 읽어 원장(fut_*)에 반영하고, 신규 카드 수집·케미 재계산·커밋까지 닫는다. /club-sync로 실행.
---

# fut.gg 구단 동기화 런북 (2026-09-19 신설, 사용자 지시 「스쿼드 동기화를 match-watch처럼 스킬로」)

작업 디렉터리: 저장소 루트. DB `db/tactics.db`. 규칙은 CLAUDE.md·HANDOFF.md.

## 0. 전제 — 로그인·싱크는 **사용자 몫**

- ⛔ **로그인 대행 금지.** fut.gg·EA 아이디/비밀번호 입력, 로그인 버튼 클릭, EA 접근 허용 클릭을 하지 않는다.
- 로그인이 안 돼 있으면 **사용자에게 요청하고 멈춘다**: 「브라우저 패널에서 fut.gg에 로그인해 주세요. 끝나면 알려주세요.」
- EA 구단 자동 수집은 FC Community API 승인 파트너 전용이라 우리가 직접 호출하지 않는다. **GG Club 페이지는 읽기만** 한다.
- ⭐ 「Sync Club」·「Refresh Now」 버튼은 **사용자 계정에 작업을 거는 동작**이다 — 누르기 전에 **승인을 받는다**
  (이번 세션에서 이미 「눌러줘」를 받았으면 그대로 진행하고, 아니면 물어본다).

## 1. 게이트

`python3 scripts/gates.py` 통과 확인. 실패면 중단하고 원인만 보고한다.

## 2. 브라우저로 GG Club 읽기 (in-app 브라우저)

1. `mcp__Claude_Browser__navigate` → `https://www.fut.gg/gg-club/my/players/`
2. 로그인 상태 확인 — 클럽이 안 보이면 §0대로 사용자에게 요청.
3. 최신화가 필요하면 「Sync Club」(또는 「Refresh Now」) 클릭 → **6~8초 대기**.
   ⚠️ 누른 직후 바로 읽으면 이전 데이터가 온다. 버튼 라벨이 `Sync Club` → `Refresh Now`로 바뀌면 반영된 것이다.
4. `fetch` 훅을 설치하고 **페이지를 전부 넘겨** 응답을 모은다(30장/페이지):
   ```js
   window.__c=[]; const of_=window.fetch;
   window.fetch=async(...a)=>{const r=await of_(...a); try{const u=(typeof a[0]==='string'?a[0]:a[0].url)||'';
     if(u.includes('/api/gg-club/players')) window.__c.push(await r.clone().json());}catch(e){} return r;};
   // 페이지 버튼(1,2,3…)을 2~3회 순회하며 2.5초씩 대기 → 중복 제거
   ```
   ⚠️ 한 번 순회로는 누락된다(실측). **같은 페이지를 두 번 이상** 밟아 unique 수가 더 안 늘 때까지 돈다.
5. 활성 스쿼드는 별도다: `/gg-club/my/squads/` → `/gg-club/my/` 로 SPA 이동하면
   `/api/gg-club/active-squad/`가 다시 불린다. `activeGroupPositions`에서 `positionIdx ↔ playerEaId`를 받는다.
   슬롯 순서(f4231a): `0 GK · 1 RB · 2 CB · 3 CB · 4 LB · 5 CDM · 6 CDM · 7 RM · 8 LM · 9 CAM · 10 ST` (우→좌).

## 3. 원장 반영

1. 캡처를 `[{"ea","n","ovr","six":[6],"cs","cp","gg","added","paid"}, …]` 형태로 `/tmp/ggclub-YYYYMMDD.json`에 저장.
2. `.venv/bin/python scripts/fut_club_sync.py /tmp/ggclub-YYYYMMDD.json --account main`
   - 신규는 추가, 기존은 OVR·6대 스탯·케미 스타일·개인 케미 갱신.
   - ⛔ **EA에 없는 보유 행을 자동 처분하지 않는다** — 목록만 내고 사용자에게 확인받는다.
   - ⭐ 「진화 완주로 보이는 선수」 보고가 뜨면 `fut_club.py complete`로 닫되, **어떤 진화였는지는 사용자에게 확인**한다
     (fut.gg는 경로를 주지 않는다 — 「GG Club tracks your players' final stats, but not the evolution path that created them.」).
3. 활성 스쿼드 슬롯을 `fut_squad_slots`에 반영(11명 + 교체). 포메이션·감독 국적/리그가 바뀌었으면 `fut_squads`도 갱신.
4. 새로 들어온 카드가 있으면 `.venv/bin/python scripts/collect_futgg_cards.py --games 27`
   (국적·리그·클럽·29속성·심플카드 URL이 이때 채워진다 — 이게 없으면 케미·추천 계산에서 빠진다).

## 4. 완료 절차

`python3 scripts/gates.py` → `python3 scripts/export.py` → `scripts/db_dump.sh` →
`git add db/tactics.db db/dump/ site/data/ && git commit -m "data(fut): GG Club 싱크 YYYY-MM-DD — 신규 N·갱신 M" && git push`
⚠️ `git add -A` 금지 — 명시 스테이징만.

## 5. 종료 보고 (이 형식으로)

- **보유**: 총 N명(빌라 M명) · 신규 K명(이름·OVR) · 사라진 행 L명(**처분 여부 사용자 확인 요청**)
- **선발 XI**: 슬롯별 11명 + **팀 케미 n/33**. 직전과 달라졌으면 바뀐 자리를 짚는다.
- **케미 스타일**: 새로 붙인 것 / 우리 추천과 갈리는 칸.
- **진화**: 완주 추정·진행 중 목록.
- **화면 확인**: 진화·내 구단 → 케미스트리 탭에서 「지금 쓰는 스쿼드」가 갱신됐는지.

## 하지 말 것

- 로그인·EA 연동 대행, 비밀번호 입력 (§0)
- 보유 행 자동 삭제, 진화 경로 추정 기입
- 처방·역할 가중 변경(그건 사용자 판단 사안이다)
- HANDOFF.md 갱신(사실 적재 회차라 불필요 — 구조가 바뀌었을 때만)
