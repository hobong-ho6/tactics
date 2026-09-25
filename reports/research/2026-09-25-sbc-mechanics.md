# FC 시리즈 SBC 메커니즘 조사 → 솔버 반영 (2026-09-25)

사용자 지시: 「지금까지 FC 시리즈의 SBC들을 분석해서 어떻게 스쿼드 구성 챌린지를 하는지 분석 및
공부하고 SBC 해법 도출하는 방법에 반영」.

사실 정본은 `game_system_changes`(area=meta, recorded=2026-09-25) **9행**이다 — 여기 산문은 그 행의
맥락과 「무엇을 고쳤나」만 적는다(불변규칙 12). 외국어 인용은 전부 번역 병기(불변규칙 11).

## 0. 조사 범위 (불변규칙 10 — 다국어)

| 언어 | 무엇을 찾았나 |
|---|---|
| 영어 | EA 도움말(1차) · fifauteam/timesaver 케미 해설 · 팀 레이팅 역산 · 오픈소스 솔버 5종 |
| 한국어 | Vortex Gaming·futmind 한국어판 — 「아웃 오브 포지션 = 0 케미, 단 팀 평점에는 영향 없음」이 영어 자료와 **독립적으로 일치** |
| 독일어 | EA 포럼 DE · help.ea.com/de — **희귀도(Selten/häufig) 축**이 등급(Bronze/Silver/Gold)과 별개라는 것이 여기서 가장 명확했다 |

⚠️ 안 훑은 언어: 스페인어·포르투갈어·일본어. 이유 — 위 3개에서 **같은 규칙이 이미 교차 확인**됐고,
추가 언어는 대개 영어 원문의 번역 복제라 교차검증이 되지 않는다(불변규칙 12의 경고).

## 1. 우리가 이미 맞게 하고 있던 것

- **케미 기준선** 클럽 2/4/7 · 리그 3/5/8 · 국적 2/5/8 — FC27 값과 **일치**.
- **팀 레이팅** = 평균 + (평균 초과분 합 / 인원), **내림** — 커뮤니티 역산식과 **일치**.
- **자리 안 맞으면 케미 0이고 링크 기여도 0** — 우리 모델과 **일치**. 제출은 막히지 않는다는 것도 확인.
- **저장 직전 독립 재검증** — `theblakelalonde/fc-sbc-solver`가 같은 걸 한다
  (「every squad is re-checked by independent rule code before placement」 = 모든 스쿼드를 배치 전에
  독립 규칙 코드로 재검증한다). 우리는 2026-09-25에 사용자 지적을 받고 같은 결론에 도달했다.

## 2. 고친 것 — 효과가 큰 순서

### ⑴ 보유 카드 44장의 포지션이 비어 있었다 ⭐ 최대 효과

`fut_club_sync.py`가 싱크 때 만드는 **스텁 행**(source 「카드 페이지 미수집」)이 원인이다. 두 군데가
동시에 놓쳤다: `collect_futgg_cards.py`의 대상 쿼리가 「카드 표에 **행이 없는**」 보유분만 봤고,
upsert의 SET 목록에 **`positions`가 아예 없었다**. 그래서 club·league·nation은 나중에 채워졌는데
positions만 영영 빈 채로 남았다.

증상이 「데이터가 없다」가 아니라 **「해가 없다」**로 나타난다 — 그 44장은 어느 칸에도 못 서서
무조건 자리 안 맞음이 되고, 케미 계산에서 통째로 빠진다. **보유 132장 중 44장(33%)이었다.**

⛔ 「COALESCE로 채우면 된다」가 아니다 — `NULLIF(TRIM(x),'')`을 써야 한다. 빈 문자열은 NULL이 아니라
COALESCE를 그냥 통과한다(migration 062에서 똑같이 당했다).

### ⑵ 배치가 탐욕법이었다

같은 세션에서 최대 이분 매칭 + 케미 목적 국소탐색으로 교체했다. 목적함수를 처음에 「자리 맞는 인원」으로
뒀다가 케미가 9 → 2로 떨어져 **케미 우선, 인원은 동점 처리**로 정정했다(최대 매칭끼리는 포함 관계가
아니라 인원이 같아도 맞는 사람이 통째로 바뀐다).

### ⑶ 아이콘·히어로 케미를 안 세고 있었다

자리만 맞으면 **무조건 3**이고, 추가 링크 기여가 있다. ⛔ 규칙을 코드에 박지 않고 fut.gg의
`player_card_items.chem_extra`를 읽는다 — **EA가 2026-09-14에 실제로 바꿨기 때문이다**
(아이콘 국적 +2 → +1 · 히어로 리그 +2 → +1). 박았다면 그날 조용히 틀렸다.
⚠️ 우리 보유분에 아이콘·히어로가 0장이라 **통제 실측을 못 했다** — 등급 B로 남긴다.

### ⑷ 감독 케미를 「모른다」고 밝히게 했다

감독은 국적·리그가 같은 선발에게 +1을 주고 SBC에도 적용된다. 어느 감독을 쓸지는 사용자만 알므로
**세지 않되**, 우리 케미가 **하한**이라는 것을 화면에 적었다. ⇒ 「케미 부족」이 인게임에선
감독만으로 메워질 수 있다.
⚠️ 출처들이 기여량에서 엇갈린다고 스스로 밝힌다(등급 C) — 통제 실측이 필요한 항목이다.

## 3. 결과 (같은 보유분·같은 시드)

| | 조사 전 | 조사 후 |
|---|---|---|
| 달성 가능 | 3 | **5** |
| 불가·못 찾음 | 4 | **2** |
| 콘솔에 찍힌 「자리 안 맞음」 | 17 | **5** |

## 4. 하지 않은 것과 그 이유

- **최소 비용 정수계획법(CP-SAT)** — 공개 솔버의 정석이지만 목적함수가 **가격**이다.
  fut.gg가 **FC27 시세를 아직 주지 않아**(조회분 전부 `hasPrice:false`) 우리에겐 목적함수가 없다.
  보유분 판정이 목적인 지금 구조가 맞다. ⇒ 시세가 열리면 재검토한다.
- **희귀도 조건 파싱** — 존재는 확인했으나 우리 수집분 **65개 문장에는 아직 없다**.
  ⛔ 미리 패턴을 발명하지 않는다. 나오면 솔버가 「판정 불가」로 떨어뜨려 드러난다.
- **top-heavy 레이팅 조합** — 팀 레이팅 조건을 살 카드로 맞출 때의 정석이지만, 이것도 가격 축이다.
- **카드 소모 추적** — 제출한 11장이 무엇이었는지 EA가 주지 않는다. 연속 SBC 해법이 이미 낸 카드를
  다시 쓸 수 있다는 한계를 화면에 적어 뒀다.

## 출처

- [help.ea.com — Squad Building Challenges](https://help.ea.com/en/articles/ea-sports-fc/squad-building-challenges/) (등급 A)
- [timesaver.gg — FC 27 Chemistry Explained](https://timesaver.gg/blog/fc-27-chemistry-explained-icon-hero-link-changes)
- [fifauteam — FC 26 Chemistry](https://fifauteam.com/fc-26-chemistry/) · [FC 26 Squad Rating Guide](https://fifauteam.com/fc-26-squad-rating-guide/)
- [Vortex Gaming(한국어) — FC 26 최고의 SBC 팀](https://vortexgaming.io/postdetail/875342)
- [EA Forums DE — Kann mir jemand SBC erklären?](https://forums.ea.com/discussions/fc-24-general-discussion-de/re-kann-mir-jemand-sbc-erkl%C3%A4ren/7656151)
- [github.com/Regista6/EA-FC-Automated-SBC-Solving](https://github.com/Regista6/EA-FC-Automated-SBC-Solving) · [theblakelalonde/fc-sbc-solver](https://github.com/theblakelalonde/fc-sbc-solver) · [kosciukiewicz/sbc-solver](https://github.com/kosciukiewicz/sbc-solver)
