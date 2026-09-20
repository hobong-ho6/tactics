# 2026-09-19 AVL 토트넘 원정 — D+1 병렬 세션 산출물 (인계용)

> ⚠️ **이 파일은 인계 메모다. 정본이 아니다.**
> 2026-09-20 21:30 KST, 이 경기 D+1 추적을 **두 세션이 병렬로** 수행했다.
> 다른 세션이 `observations` #866·#867을 21:23에 적재했고 리포트 D+1 절을 담당한다.
> 이 세션은 **DB를 쓰지 않았다.** 아래는 obs#863~867과 **겹치지 않는** 산출물만 모은 것이다.
> 흡수한 뒤 이 파일은 삭제해도 된다.

## 미결 4건 — D+1 종료 시점 현황

| # | 항목 | 상태 | 근거 |
|---|---|---|---|
| ① | 완비사카 HT 교체 사유 | ✅ **해결** | 「캐시 컨디션 미달 → 완비사카 선발 → 전반 부진 → 예정된 교체」(Townley, §4) · 부상·경고 아님(obs#867 + 카드 0장) |
| ② | 만잠비 72′ 교체가 부상인지 | ✅ **부상 아님** | 대표팀 소집 확인(SRF) · 본인 인터뷰 · 교체 직후 하이파이브(Tanswell) · 4중 정황(§4) |
| ③ | 후반 2실점 감독 진단 | ⛔ **0건 확정** | 회견 6문항 전부 확인 — **질문 자체가 없었다.** 다음 기회 10-09 브렌트포드전 전 회견 |
| ④ | 루헤리 평가 충돌 | ✅ **해소 제안** | 충돌 축이 「빌라↔토트넘」이 아니라 **「전반↔후반」**이었다(§4) |

**부수 수확**: 카마라 백3가 The Athletic 정식 기사로 재확인(obs#866과 정합) · 에메리의 **롱볼 설계 자백** ·
맥긴의 **잭슨 골 = 훈련된 패턴** 확인 · 데 제르비 회견 **공식 전문**(auto-caption → 공식 승격 가능) ·
**콘사는 아스날 이적**(명단 제외가 아니다).

---

## 1. ⛔ 리포트 109행 부엔디아 수치(35.6 → 47.6)는 재현되지 않는다

본문 §2 「후반 우측 편중 백5」 표의 **부엔디아 행만** 어떤 방법으로도 재현되지 않는다.
**같은 표의 맥긴 행은 재현된다** — 후반 32.1(n8)이 표준 필터(`core.whoscored.DEF_TYPES` + `period`)로 소수점까지 일치한다.

| | 리포트 기재 | 당일 스냅샷 20건을 `period`로 재분할 | D+1 재수집 |
|---|---|---|---|
| 전반 | 35.6 (n6) | 41.8 (n8) | 44.1 (n9) |
| 후반 | **47.6** (n14) | 43.4 (n11) | 42.7 (n16) |
| Δ | **+12.0** | +1.6 | −1.4 |

**전수 탐색 결과 0건.** 필터(수비액션 8종 / PPDA 4종 / 보유 이벤트) × 분할(`period` / `minute≤45`)
× 출전 선수 16명 × x축·y축 전 조합에서 `(35.6, n=6)`과 `(47.6, n=14)`를 동시에 만드는 조합은 없다.

### 출처 자체는 특정됐다
표본 수가 당일 스냅샷(`/tmp/ws_events.json`, 빌라 610건)과 맞물린다:
- 팀 def_x **30.6** = 리포트 기재값과 일치 (n160)
- 맥긴 수비액션 총 **11**건 = 리포트 3+8
- 부엔디아 수비액션 총 **20**건 = 리포트 6+14

⇒ 지표·필터·데이터 출처는 맞고 **전·후반 분할 단계에서 부엔디아 행만 어긋났다.**

### ⚠️ 분할 방법 자체에도 함정이 있다
이 경기 전반은 `expandedMinute` 기준 **52분까지** 이어진다(전반 추가시간이 45 이후로 연속 계산되고
만잠비 골이 49′). **`minute≤45`로 자르면 46~52분 이벤트가 통째로 후반으로 밀린다.**
정확한 분할은 `period` 필드뿐인데, **당일 스냅샷에는 `period`도 `minute`도 없다**(필드가
`playerId,teamId,type,x,y` 5개뿐). 당일 세션이 이 표를 만든 경로가 리포트에 기록돼 있지 않다.

### 결론은 살아남는다
리포트의 주장은 「좌측은 백5로 내려가지 않았으므로 대칭 5-3-2가 아니다」인데,
재계산에서도 부엔디아는 44.1 → 42.7로 **거의 움직이지 않는다**. 「안 내려갔다」는 성립한다.
틀린 것은 **「반대로 12점 올라갔다」** 부분이고 실제로는 **변화 없음**이다.

⇒ 처리 방침(2026-09-20 사용자 결정): **본문 109행은 그대로 두고 D+1 절에 「당일 수치 정정」으로 적는다**
(불변규칙 2·3 · match-watch §2-1a 「덮어쓰지 말고 D+N에 적는다」).

---

## 2. ⭐⭐ 당일 스냅샷은 「전체 이벤트」가 아니었다 + Opta 이벤트 사후 개정 실증

### ⑴ 당일 수집은 16종 화이트리스트였다
`/tmp/ws_events.json`의 이벤트 타입이 정확히 `POSS_TYPES | DEF_TYPES` 16종 안에만 들어간다(검증 완료).
D+1 재수집에만 있는 타입 14종: `Save`(9) · `SubstitutionOn/Off`(각 5) · `CornerAwarded`(12) ·
`KeeperPickup`(5) · `OffsideProvoked`(5) · `Claim`(4) · `Card`(2) · `Punch`(2) · `ShieldBallOpp`(2) ·
`OffsideGiven`(2) · `OffsidePass`(2) · `Error`(1) · `KeeperSweeper`(1).

즉 **스즈키 선방 9건과 빌라 교체 5장이 애초에 없었다.**
⇒ PPDA·def_x·국면 그리드는 16종만 쓰므로 **그 지표들 자체는 영향받지 않는다.**
⇒ 그러나 「카드가 없다」·「교체가 없다」를 **사실 판정의 근거로 쓰면 안 된다**(당일 데이터엔 원래 없다).

### ⑵ 화이트리스트 안에서도 두 스냅샷이 다르다 — 사후 개정
`(playerId, type, x, y)` 매칭 기준:

| | 건수 | 주요 타입 |
|---|---|---|
| D+1 재수집에만 있음 | 60 | Pass 26 · TakeOn 11 · Challenge 6 · BallTouch 4 |
| 당일 스냅샷에만 있음 | **44** | Pass 21 · BallTouch 5 · Clearance 4 · TakeOn 3 |

**「당일에만 있는 44건」이 핵심이다.** 단순 누락·보강이라면 한 방향으로만 늘어야 하는데
양방향이므로 Opta가 **좌표·타입을 재분류**했다는 뜻이다.
⇒ 종전엔 **xG만 사후 개정된다**고 알려져 있었다(docs/30 ⑧ · match-watch §3).
**이벤트 자체도 개정된다**는 것이 이 경기에서 처음 실증됐다.

부엔디아 수비액션은 개정으로 20 → 25건이 됐고, 늘어난 5건이 `Challenge` 4 · `Interception` 1 · `Tackle` 1인데
**좌표가 y 85~97 = 좌측 터치라인 극단**이다. 개정 후에 좌측 수비 관여가 더 잡혔다.

### ⇒ 규약 제안 (2026-09-20 사용자 승인 — 「obs로 남기고 규약화 제안」)
xG의 `xg_source`와 같은 방식으로, **PPDA·def_x·국면 그리드에도 수집 시각과 수집 범위를 남긴다.**
교차 경기 집계는 같은 조건끼리 고정한다. docs/30 ⑧ · match-watch §3에 반영 여부는 사용자 판단.

---

## 3. obs#863(우측 편중 백5) 보강 — 맥긴 개인 좌표 정량

`period` 분리 수비액션 x/y (**y 낮음 = 오른쪽**):

| 선수 | 전반 x/y (n) | 후반 x/y (n) |
|---|---|---|
| 맥긴 | 58/30 (3) | **32/18 (8)** |
| 캐시 | — | 17/21 (7) |
| 부엔디아 | 44/77 (9) | 43/78 (16) |
| 루헤리 | 15/78 (8) | 22/82 (20) |

맥긴이 후반에 **자기 진영 우측 깊이로 내려가 캐시(y 21)와 나란히 선다**(y 18).
반대쪽 부엔디아는 **전·후반 변화가 없고** 루헤리는 오히려 올라갔다.
⇒ 「좌측은 백5로 안 내려갔다 = 대칭이 아니다」가 **맥긴·부엔디아 개인 좌표로 독립 확인**된다.

⚠️ 팀 def_x 재계산은 전체 30.9 / 50~86′ 26.3 → 87′~ 35.8이다(리포트 30.6 · 26.1 → 34.6).
소폭 차이는 §2의 스냅샷 차이 때문이며 **결론 방향은 동일**하다. **리포트 값은 덮지 않았다.**

---

## 4. 서사 수집 결과 — 미결 4건 (서브에이전트 2축, 회견·기사 축은 미완)

⚠️ 아래 인용은 전부 **auto-caption 또는 웹 기사**이며, 영상 **직접 시청 0건**이다.

### ④ 루헤리 평가 충돌 → ⭐⭐ **해소 쪽. 단 D+0의 전제가 반대였다**
D+0 §8-3은 「토트넘 매체가 **루헤리에게 빠르게 봉쇄됐다**고 썼다」고 기록했으나,
D+1에 확보한 토트넘 소스는 **초반에 대해 정반대**로 말한다. 갈린 축은 **빌라 ↔ 토트넘이 아니라 전반 ↔ 후반**이다.

- The Tottenham Blueprint `XRJgUjer1cc` 「especially Savio who was having a lot of joy against the Villa left back」
  (특히 빌라 왼쪽 수비를 상대로 크게 재미를 보고 있던 사비뉴) — auto-caption
- Bains Analysis `noampLJzxn0` 「Savinho, especially in the first 20, was getting the beating of him.」
  (특히 첫 20분간 사비뉴가 그를 이기고 있었다) — auto-caption ⚠️ 이 전사는 루헤리를 **「Reguilon」으로 오인식**한다
- Spurs Web(Rae Nkwocha, 9/19, 사비뉴 5/10) 「struggled to beat his man Ruggeri, **who grew into the game**」
  (자기 마크맨 루헤리를 제치는 데 고전했고, **루헤리는 경기에 녹아들었다**) — **그리고 사비뉴는 후반에 왼쪽으로 옮겨졌다**
- Football Italia(Sam Wilson, 9/19) 제목 「Ruggeri shines on first Premier League start」 ·
  「Ruggeri **worked him out inside 20 minutes**」(루헤리가 **20분 안에 그를 간파했다**)
- The Villans `kj4gz1QXrl8` 「I thought Rogeri had a tough first half … it's definitely a tactical tweak at halftime
  that Emery got going on that left side with Wendia helping out a lot more」
  (루헤리는 힘든 전반을 보냈다 … 하프타임에 에메리가 **부엔디아가 좌측을 훨씬 더 돕게 한 것은 분명한 전술 조정**이었다) — auto-caption

**⭐ 결정적 물증**: 스퍼스가 후반에 **사비뉴를 왼쪽으로 옮겼다**(Spurs Web). 표적이 유효했다면 옮길 이유가 없다.
**⭐ 상대 매체가 빌라의 좌측 전진을 인정**: 아치 그레이 평점 항목의 「Villa finding space down Spurs' right」는
우리 실측 **「보유 셀 22개가 상대 진영 좌측」**과 독립적으로 일치한다.

**⭐ 빌라 전담 기자의 1차 평가 — 양쪽을 한 문장에 담았다**(John Townley, Birmingham Live, **6점**):
> 원문 「**Ruggeri struggled at times against Savio** … **His physicality helped him out at times** — he's a
> good size for Premier League football. **Gave the ball away for Spurs' goal late on.**」
> (**루헤리는 사비우를 상대로 때때로 고전했다** … **그의 피지컬이 몇 번 그를 구해줬다** — 프리미어리그에
> 적합한 체격이다. **후반 막판 스퍼스 골 장면에서 볼을 내줬다.**)

⚠️ **새 지목 1건**: **86′ 갤러거 실점 장면의 볼 로스트 책임**이 루헤리에게 있다는 서술은 **우리 실측 축에 없던 항목**이다.
⇒ obs#865(「블록이 풀렸다」)의 **개인 귀속 후보**지만 단일 소스이므로 **영상 확인 전까지 채택 보류**.

⚠️ 토트넘 팬 매체(Spurs Odyssey, D+1)도 「봉쇄됐다」가 아니라 **초반 위협 인정** 쪽이다:
「Spurs had some **early defending to do** against Villa left back Matteo Ruggeri」
(스퍼스는 빌라 좌측 수비수 루헤리를 상대로 **초반 수비를 해야 했다**)
⇒ D+0이 기록한 「토트넘 매체 = 봉쇄됐다」는 **사비우 개인 평점 맥락**의 문장이었을 가능성이 높다.

⇒ **제안**: 「초반 표적 → 20′ 내 적응 → 후반 상대가 매치업 포기」의 **2단계 경기**로 재기술.
단일 라벨 「struggled」는 기각. 평가 상향하되 **「초반 취약 → 경기 중 적응」을 명시**.
⚠️ 미해소 잔여: 평점 SofaScore 6.4 ↔ FotMob 7.5, 인터셉트 5↔6 · 회수 9↔11 — **제공사 차이므로 충돌로 적지 말고 병기**.

### ② 만잠비 72′ 교체 → **부상 아님**
- avfc.co.uk D+1 인터뷰 `yn-UvcWhAio` 만잠비 본인 「we can go happy … **on the national team**, and when we come back
  I hope we do like today」(우리는 기쁘게 **대표팀에** 갈 수 있고, 돌아왔을 때 오늘처럼 하길 바란다) — auto-caption
- SRF: 만잠비가 **스위스 네이션스리그 소집 명단 포함**(9/26 북마케도니아 · 9/29 스코틀랜드 · 10/3 슬로베니아 · 10/6)
- 체력 관리설 2건: The Villans `kj4gz1QXrl8` 「his fitness … he looked spent」(체력이 … 소진돼 보였다) ·
  UTV `BTW1C1UCPN0` 「playing at about 65% of your peak ability」(최고 능력치의 65% 정도로 뛰고 있다) — 둘 다 auto-caption
- ⚠️ 병존 배경: Blick 「**Nach einer Knieverletzung, die er sich während seiner starken WM zugezogen hatte**」
  (월드컵에서 입은 **무릎 부상** 이후) 노팅엄전에야 데뷔. **부하 관리 가설은 배제되지 않으나 직접 진술 0건.**
- 🇨🇭 Blick 추가: 「**20 Jahre und 340 Tage**」 = PL 역대 **3번째로 어린 스위스 득점자** · 이적료 6,000만 유로 구단 최고액

### ① 완비사카 46′ 교체 → ⭐⭐ **해결. 「캐시 컨디션 미달 → 완비사카 선발 → 전반 부진 → 예정된 교체」**
(obs#867이 「경고 0장」을 확정했다 — 그 다음 층이 D+1에 닫혔다.)

**John Townley(Birmingham Live 빌라 담당) 평점 기사, 2026-09-19 14:34 BST 발행 / 17:06 갱신**
> 원문 「**Wan-Bissaka continued at right-back while Cash wasn't quite ready to start today. He wasn't
> effective enough in possession and was replaced by Cash at the break.** 6」
> (**완비사카는 캐시가 오늘 선발할 만큼 완전히 준비되지 않았기에 계속 오른쪽 풀백으로 나섰다. 그는
> 볼을 가진 상태에서 충분히 효과적이지 못했고 하프타임에 캐시로 교체됐다.** 6점)
> `birminghammail.co.uk/sport/football/football-news/john-townleys-aston-villa-player-34641341`

⇒ **부상 아님 · 경고 관리 아님 · 전술적 형태 변경 아님 — 「경기력 + 예정된 교체」다.**
⭐ **D+0의 Tanswell 실시간 관찰과 정합**: 「Matty Cash going through his own warm-up at half time.
May be coming on pretty soon.」(캐시가 하프타임에 자기 워밍업을 하고 있다. 곧 들어올 것 같다.)
= **하프타임 전부터 준비된 교체**였다.
⇒ ⚠️ **obs 신설 후보**: 이 교체를 「후반 우측 편중 백5의 일부」로 읽으면 오독이다.
캐시 투입은 **가용성 판단**이고, 맥긴 하강(백5)은 **그 뒤의 별도 조치**다.
(HANDOFF 「선발 11명을 감독의 선택으로 읽기 전에 가용 인원부터 확인하라 — obs#787」의 교체판 사례.)

**보조 근거(팬채널 — 위치선정 문제로 서술)**
- 1874 `ahxMgX0BH2c` 「I was actually quite relieved when he came off at halftime … he just looked a little bit lost
  and a little bit isolated at right back」(하프타임에 그가 나갔을 때 솔직히 안도했다 … 우측 수비에서 좀 길을 잃고
  고립돼 보였다) — auto-caption
- The Villans `kj4gz1QXrl8` 「the only player I did think struggled … his **positional sense** is struggling …
  he'll get drawn into the wrong one」(고전했다고 생각한 유일한 선수 … **위치 선정 감각**이 흔들린다 … 엉뚱한 쪽으로 끌려간다) — auto-caption
- Villa News(Max Wilkins) **3점** 「Far from good enough」 — 근거는 **45분간 듀얼 3패 · 드리블 돌파 1회 허용 · 볼 로스트 1회**
- ⭐ **상대팀 소스 4편이 완비사카를 한 번도 언급하지 않았다**(0 hits) — 표적이 아니었다는 간접 신호
- ⭐ **캐시는 부상에서 복귀해 하프타임에 투입**됐다(컨디션 관리 축과 맞물림)
⇒ D+0의 「피지컬 리스크(경고 회피)」 가설을 지지하는 새 근거는 **0건**. 두 팬채널 모두 **위치선정·적응**을 사유로 본다.
⇒ 기재 시 `confidence`에 **「감독 확인 없음 / 기자·팬채널 해석 기반」**을 명기할 것.

### ③ 후반 2실점 진단 → **에메리 본인 진단 여전히 0건**(회견 2편에 질문 자체가 없었다)
- 외부는 「빌라가 물러앉았다」까지만 말하고 **시간 분할을 하지 않는다**:
  토트넘 공식 「Villa were **content to sit back**, soak up the pressure and try to hit us on the break」
  (빌라는 **물러앉는 데 만족**했고 압박을 흡수해 역습으로 쳤다) ·
  🇧🇷 Trivela 「o time mostrou dificuldade para **romper o bloqueio montado por Unai Emery**」
  (그 팀은 **에메리가 세운 블록을 뚫는 데** 어려움을 보였다) — 블록이 **기능했다**는 서술
- 데 제르비는 실점 원인을 전부 **스퍼스 쪽**에 돌렸다. 빌라가 무너졌다는 서술 0.
- ⭐⭐ **obs#865(「내려앉은 게 아니라 풀렸다」)의 새 지지 근거**: 🇸🇳 Seneweb이 **84′ 카마라 OUT(↔음바예) +
  맥긴 OUT(↔바클리) 더블 체인지**를 확인했다. def_x 상승 시점(87′~)과 **정확히 맞물린다** —
  「풀림」이 **교체로 인한 구조 소실**로 설명된다. 이 주장은 실측 시계열 + 교체 명단만으로 성립하므로 서사에 의존하지 않는다.
- ⚠️ **의도 축(에메리가 의도적으로 내렸는가)은 서사가 1차 소스인데 본인 발언이 없다 → 미확정 유지.**

### ⑤ 후반 백5 — 상대 채널 독립 확인 1건 (기사·블로그 축은 0건)
The Tottenham Blueprint `XRJgUjer1cc` 「They started bringing their midfield very deep to protect the sides …
**McGinn was dropping in on the right as well to protect us against Marmoush**」
(측면을 보호하려 미드필드를 아주 깊게 내리기 시작했다 … **맥긴 역시 오른쪽으로 내려와 마무슈를 상대로 우리를 막았다**) — auto-caption
⇒ **하강 주체가 맥긴(우측)만 지목되고 좌측은 언급되지 않는다** — §3 실측과 정합.
⚠️ 단 **기사·전술블로그 축에서는 백5 언급 0건**이므로 `confidence`에 「외부 교차검증: 영상 1건」으로 한정할 것.

### ⑦ 데 제르비 「롱볼 +86%」 후속
- 영어 원문(ESPN) 「this season Aston Villa are playing **86% more long balls** than last season」
- 🇮🇹 이탈리아 매체는 **86% 대목을 전혀 옮기지 않았다** — 커버가 **데 제르비 신변 프레임**이지 전술 프레임이 아니다
- 🇮🇹 데 제르비 verbatim(D+0 0건 칸 해소) 「**Siamo troppo fragili** … il calcio non si riduce a 90 minuti di
  possesso palla」(**우리는 너무 물렁하다** … 축구는 90분간의 볼 점유로 환원되지 않는다) — TMW
  ⇒ 우리 실측(점유는 토트넘 우위, 3골 전부 전환)과 **같은 방향의 자백**
- 🇮🇹/영어 「we conceded one unacceptable goal **from a goal kick**」(**골킥에서** 용납할 수 없는 골 하나를 내줬다)
  ⇒ D+0의 `gk_long_kick_route` **APPLIED 판정을 상대 감독이 직접 뒷받침**한다

---

## 4-b. 1차 발언 축 — 새로 확보한 verbatim (리포트 미수록분)

⭐ **접근 경로 돌파 2건**: `avfc.co.uk`는 브라우저로 전면 접근 가능하다(첫 접속이 쿠키 배너면
**같은 URL로 1회 재navigate**하면 본문이 뜬다 — 2회 재현. 쿠키 동의는 누르지 않았다).
`tottenhamhotspur.com` 「Every word」는 **D+1에 발행**됐고 데 제르비 회견 **공식 전문**을 확보했다
⇒ D+0에 auto-caption으로 잡았던 데 제르비 문장들의 **confidence를 공식 전사로 승격 가능**하다.

### ⭐⭐ ⑧ 콘사는 명단 제외가 아니라 **아스날로 이적**했다 (2026-08-22)
avfc.co.uk 공식 「Konsa completes Arsenal switch」
> 원문 「**Aston Villa can confirm that Ezri Konsa has completed a permanent transfer to Arsenal.**」
> (**아스톤 빌라는 에즈리 콘사가 아스날로 완전 이적을 완료했음을 확인할 수 있다.**)

보강 — 에메리 D-1 회견이 콘사를 **과거형으로만** 언급한다:
> 「Last December, we had neither Torres nor Mings, and we had **Lindelof with Konsa**. We performed fantastically.」
> (지난 12월엔 토레스도 밍스도 없었고 **린델뢰프와 콘사**가 있었다. 우리는 환상적으로 해냈다.)

✅ **DB는 이미 정확하다** — `squad_entries`에 콘사 행 0건(`players.id=3`은 이력으로 보존).
⚠️ 다만 **수비진 가용성 축은 「콘사 매각 + 파우 햄스트링」 2중 결손**으로 읽어야 한다.
현 CB 옵션: **린델뢰프 · 밍스 · 하우드-벨리스**(+복귀 시 파우 토레스).

### ⭐⭐ 「카마라 백3」가 The Athletic 정식 기사 본문으로 재확인됐다
Jacob Tanswell, The Athletic, 2026-09-20 — D+0에는 라이브 포스트뿐이었다.
> 원문 「**A quarter of an hour into the match, when Villa built from the back, Manzambi dropped deep,
> occasionally alongside Joao Gomes, as Boubacar Kamara moved into a back three.**」
> (경기 15분 무렵 **빌라가 후방 빌드업을 할 때** 만잠비는 깊게 내려왔고, 때때로 주앙 고메스 옆에 섰으며,
> **카마라는 백3로 이동**했다.)
> 원문 「**From Suzuki's kicks, Manzambi partnered Jackson, with Villa moving into a 4-2-2-2 shape and,
> as De Zerbi recognised, playing increasingly directly.**」
> (**스즈키의 킥 상황에서** 만잠비가 잭슨과 짝을 이뤘고, 빌라는 **4-2-2-2 형태**로 이동했으며,
> 데 제르비가 알아챘듯 점점 더 직선적으로 플레이했다.)

⚠️ **obs#866과 충돌하지 않는다.** Tanswell의 서술은 **「후방 빌드업 국면 한정」·「경기 15분 무렵」**으로
명시적으로 국면·시점을 한정한다 — obs#866의 결론(「장면은 실재하나 **상시 구조가 아니다**」)과 같은 방향이다.
⭐ 다만 **새 축이 하나 나왔다**: 「**만잠비가 고메스 옆까지 내려오는 것**」과 「**스즈키 킥 상황의 4-2-2-2**」는
우리 리포트에 없는 형태 서술이다. 만잠비 CAM 처방(`cam_playmaker/Build-Up` Δ0.010 무결정)의 **2위 후보 재검토 재료**.

### ⭐⭐ 에메리 — 스즈키 영입 이유 = **롱볼이 설계라는 자백**
질문 자체가 「**You're playing more long balls this season — is that planned?**」
(올 시즌 롱볼을 더 많이 쓴다 — 계획된 것인가?)였다. Birmingham Live 회견 전문 + Tanswell X 이중 확인.
> 원문 「Suzuki is a player who should first save balls from his goal. Second, **he should help us build
> in combination, like we want. We signed him for that.** … **with short and long balls that can threaten
> the opponent when they go into a high press and man-to-man. We must react quickly.**」
> (스즈키는 먼저 자기 골문에서 볼을 막아야 하는 선수다. 둘째로, **우리가 원하는 대로 조합으로 빌드업하는 것을
> 도와야 한다. 우리는 그것을 위해 그를 영입했다.** … **상대가 하이프레스와 맨투맨으로 나올 때 위협할 수 있는
> 짧은 볼과 긴 볼로 말이다. 우리는 빠르게 반응해야 한다.**)

⇒ 데 제르비의 「+86%」와 **같은 사안을 양쪽 감독이 각각 확인**했다(obs#864의 빌라 측 대응 근거).
⭐ **buildup 축 26/27 갱신의 두 번째 독립 확인**이자, 이번엔 **감독 본인의 1차 진술**이다.

### ⭐⭐ 맥긴 — 67′ 잭슨 골은 **훈련된 패턴**이다 (avfc 공식 + The Athletic 이중 확인)
> 원문 「Before the game, he spoke to us in detail about how we could exploit some space, and I think with
> Nicolas' goal, he'll be delighted because **we worked on that, quite a lot before it.**」
> (경기 전에 그는 우리가 어떻게 공간을 활용할 수 있을지 상세히 이야기했고, 니콜라의 골에 대해 그는 기뻐할 것이다.
> **우리가 그것을 사전에 꽤 많이 연습했기 때문이다.**)

⇒ **`gk_long_kick_route`(APPLIED) 판정의 결정적 보강** — 67′ 경로(스즈키 롱킥 → 만잠비 플릭 → 잭슨)가
「우연한 전환」이 아니라 **사전 훈련된 패턴**임을 주장 선수가 확인했다. 브뤼헤전·포레스트전 GK 롱킥 축과 이어진다.
> 맥긴 추가 「it was really frustrating in the first half … **throw-ins, set-pieces, we were a little bit ragged.**」
> (전반은 정말 답답했다 … **스로인, 세트피스에서 우리는 약간 너덜너덜했다.**) ⇒ 세트피스 축 자기 진단.

### 데 제르비 공식 전문 — 후반 붕괴 자기 진단 (상대팀 축, obs#865 보강)
tottenhamhotspur.com 「Every word」, D+1 발행
> 원문 「**in the second half we lost balance because we were losing. We forced the pass, we forced the
> situation. We lost ball and Aston Villa winning, they played more in counter-attack.**」
> (**후반에 우리는 지고 있었기 때문에 균형을 잃었다. 패스를 무리했고 상황을 무리했다.** 볼을 잃었고
> 아스톤 빌라는 이기고 있었으므로 역습을 더 많이 했다.)
> 원문 「In the beginning of the second half, I spoke with the four attackers to use the head, calm.
> **It was minute 51.** … but the goal we conceded, the second goal, was incredible.」
> (후반 시작에 나는 네 명의 공격수에게 머리를 쓰라고, 침착하라고 말했다. **51분이었다.** … 하지만
> 우리가 내준 골, 두 번째 골은 믿기지 않았다.)

⇒ ⭐ **obs#865와 상충하지 않는다.** 오히려 「빌라가 낮게 내려가 있어도 실점 위험이 낮았던 이유」의
**상대 측 설명**이 된다 — 빌라의 후반 전환 3골이 **상대의 균형 상실을 활용한 것**임을 상대 감독이 서술했다.
> 원문 「**I put Betancur as a centre-back in that moment, Matheus Fernandes as a midfielder.**」
> (**그 순간 나는 벤탄쿠르를 센터백으로, 마테우스 페르난드스를 미드필더로 뒀다.**)
⇒ 리포트 §8-4 ③(판 데 벤은 교체되지 않았다)의 보강 — 1분간의 대응이 **즉흥이 아니라 지시**였다.

### 에메리 — 잭슨 **출전 시간 관리**가 의도라는 1차 근거 (신규)
> 원문 「He was able to play 80 minutes with the runs he made, being consistent physically. **We are expecting
> him to play a lot of matches this year, so it is important to manage different moments.**」
> (그가 만들어낸 침투 뛰기와 함께 80분을 뛸 수 있었고 신체적으로 일관됐다. **올해 그가 많은 경기를 뛸 것으로
> 기대하므로 다양한 순간을 관리하는 것이 중요하다.**)
⇒ obs#845(포레스트전 45분 교체)와 이어지는 **의도적 부하 관리** 축.

### 에메리 — 총평 (리포트 미수록 부분)
> 「**We knew before the match what our game plan would be, facing Tottenham. Defensively, we worked
> fantastically because the players believed in the way we have worked before here.**」
> (**토트넘을 상대로 우리 게임 플랜이 무엇일지 경기 전에 알고 있었다. 수비적으로 환상적으로 해냈다 —
> 선수들이 우리가 예전부터 해온 방식을 믿었기 때문이다.**)
> 「**We had to be patient and resilient in the moments when they were attacking. … Deserved or not, this is
> the competitive way that we have achieved results before during the time I have been here.**」
> (**그들이 공격하는 순간에 인내심 있고 회복력 있어야 했다. … 자격이 있든 없든, 이것이 내가 여기 있는 동안
> 결과를 얻어온 경쟁적 방식이다.**)

### 부상·가용성 축 (⏰ 할 일 0-3b 갱신 재료)
- **파우 토레스** — 포레스트전 **햄스트링**, 「**won't feature again until after the extended international
  break**」(확대 A매치 휴식기 이후까지 출전 불가). 에메리 D-1 회견.
  ⭐ 같은 답변의 **구조 우선 선언**은 `manager_profiles`에 쓸 만한 1차 문장이다:
  「When Tyrone Mings is not here, you ask for Tyrone Mings … But we have still performed without Pau or
  Tyrone. **The structure is the most important thing.**」(밍스가 없으면 밍스를 묻는다 … 하지만 우리는
  파우나 타이론 없이도 퍼포먼스를 냈다. **구조가 가장 중요하다.**)
- **결장 명단(D-1 회견 원문)** 「Marco Bizot is out, Onana is out, Cisse is out. **Pau and Maatsen are out.**
  Goretzka is out. Madjo is out.」
- **마첸** — D+1 신규 언급 **0건**. 기존값(발목 인대 손상, 골절 없음, **6~8주** — Tanswell 09-13) 유지.
- **마조** — 「expected to return to full training **during the international break**」(휴식기 중 정식 훈련 복귀 예상).
- **알리송** — 코번트리전에서 이상, 스퍼스전 명단 제외, 휴식기 후 복귀 예상(Tanswell 09-19).
- ⭐ **이번 경기 신규 부상 0건** — 빌라 교체 5장 전부 전술 교체다.
- **다음 경기: 2026-10-10 브렌트포드(홈)**. 휴식기 중 **스페인 캠프 + 사우샘프턴과 비공개 친선전**(다음 주 금).
  징계 리스크: 잭슨·캐시 경고, 누적 퇴장 사유 없음.

### 🟡 미확보로 남은 것
1. **에메리의 후반 2실점 진단** — 회견 6문항 전부를 확인했고 **질문 자체가 없었다**. 다음 기회는
   **10-09 브렌트포드전 전 회견**(3주 뒤). ⇒ 「D+3까지 0건」으로 닫아도 무방하다.
2. **Tanswell X 부엔디아 포스트의 「Emery wanted …」 이후 문장** — 비로그인 X에서 잘렸다. 로그인 세션 필요.
   (확보분: 「**Ran over 12km today. 0.6km more than any other #AVFC player**」 — 오늘 12km 이상을 뛰었고
   다른 어떤 빌라 선수보다 0.6km 많다. ⇒ 부엔디아의 **무보유 주행량**은 우리 실측에 없는 축이다.)
3. **The Athletic 라이브블로그 58′ 루헤리 항목**(「Cheeky nutmeg from Ruggeri」) — 페이월로 전문 미확인. **인용 보류.**

---

## 5. 전사 10편 — `match_videos` 등재 상태 (2026-09-20 21:40 시점)

전사 파일은 10편 모두 `reports/transcripts/`에 있다. **병렬 세션이 21:36에 7편을 등재**했고
(report 47 귀속 · summary · impl_claims 포함) **3편이 남았다.**

| 상태 | video_id | 채널 | 성격 | claims |
|---|---|---|---|---|
| ✅ | `BTW1C1UCPN0` | UTV \| Aston Villa Fan Channel | D+1 리뷰 (필수 3채널) | 3 |
| ✅ | `kj4gz1QXrl8` | The Villans | D+1 리뷰 (필수 3채널) | 1 |
| ✅ | `ahxMgX0BH2c` | 1874 : The Aston Villa Channel | D+0 라이브 반응 (필수 3채널) | 1 |
| ✅ | `yn-UvcWhAio` | Aston Villa FC 공식 | 만잠비 경기 후 인터뷰 | 1 |
| ✅ | `noampLJzxn0` | Bains Analysis | 전술 분석 | 1 |
| ✅ | `XRJgUjer1cc` | The Tottenham Blueprint | 상대팀 | 1 |
| ✅ | `FP7obsFLxRQ` | ⚠️ **채널명 결손 — 아래 참조** | 상대팀 + 전술 | 1 |
| ⛔ | `U4OewDAQMCk` | MAH | 상대팀 | 0 |
| ⛔ | `QkA0fScs5s8` | Chris Cowlin: Spurs Chat Podcast | 상대팀, 분단위 경기 로그 | 0 |
| ⛔ | `ofp0s7RaNoc` | Cash talk's Football | ⚠️ 아래 참조 — **등재 가치 낮음** | 0 |

⭐ **필수 3채널은 각각 D+1 리뷰를 정확히 1편씩만 올렸고 전부 확보·등재됐다**(채널 `/videos` 직접 조회로 확인).
⛔ 남은 3편도 **G17상 `impl_claims` 1행이 필요하다** — 주장이 없으면 `{"axis":"none"}`을 넣어야
「주장 없음」과 「미작성」이 구분된다.

### ⚠️ `FP7obsFLxRQ` 채널명이 결손이다 — 값을 여기 남긴다
DB에 **「채널 미상 (oEmbed Unauthorized)」**로 들어갔다. oEmbed 인증 실패이지 채널이 없는 게 아니다.
확인된 값:

| 필드 | 값 |
|---|---|
| channel | **Alice - ECILA Football** |
| title | Tottenham 2-3 Villa Exposed Two Very Different Futures For These Clubs.. |
| published | 2026-09-19 |
| 길이 | 18:47 |
| kind | 상대팀(전술 분석 겸함) |

⚠️ 이 전사는 **루헤리를 「Reguilon」으로 오인식**하는 등 인명 오류가 있다(§5 오인식 대조표).
인용 시 실측 라인업으로 교차검증할 것.

### ⚠️ `ofp0s7RaNoc`는 등재 가치가 낮다 — 판단이 필요하다
**PL 전 경기 골 모음 포맷**이라 이 경기 비중이 **서두 ~2분**뿐이고, 본문에 「Dunk」 등 **타 경기 내용이 섞여 있다**.
⇒ 등재한다면 `kind`를 「경기반응」으로 두지 말 것(경기 화면 「이 경기 영상 분석」 패널이 오독을 부른다).
**아예 제외하는 편이 낫다** — 제외한다면 그 사유를 리포트 소스 커버리지에 남겨
다음 회차가 같은 영상을 다시 후보로 올리지 않게 한다.

### 자막 오인식 대조표 (신규 실증 — docs/30에 추가 후보)
`Ruggeri` → 「Rogeri / Rogério / Roger / **Reguilon**」 · `Wan-Bissaka` → 「Wasaka / Wambasaka / Juan Bisaka」 ·
`Kamara` → 「Kamar / **camera**」 · `Buendía` → 「Wendia / Benua / Bendia / **Miliano**」
⚠️ 회견 자막의 「Emiliano / Miliano」는 **에밀리아노 부엔디아**다(마르티네스 아님 — 이 경기 GK는 스즈키).

---

## 6. 소스 축 상태 갱신 (다음 회차 중복 방지)

### ⛔ 전술 블로그 칸의 구성을 바꿔야 한다 — 「0건」의 성격이 다르다
| 매체 | 상태 |
|---|---|
| The Football Analyst | ⛔ **도메인 소멸**(307 → godaddy 매물). **칸에서 영구 삭제 대상** |
| Spielverlagerung | ⛔ **휴면** — 최신 글 2026-07-19, PL 커버 중단 |
| Between the Posts | ⛔ **의도적 미커버** — 9/20에 다른 경기 2편 발행. 활동 중인데 이 경기를 고르지 않았다 |
| Coaches' Voice | ⛔ 빌라 관련 전부 아카이브(브라우저로 검색 전체 확인) |
| The Analyst(Opta) | ◐ 스탯 나열형. **수비 라인·PPDA·압박 지표 없음** — 전술 블로그로 계산하지 말 것 |

⇒ **승격 제안**: Read Aston Villa(James Chettle) · Yahoo/Roundtable(Dan Bardell)을 **상시 전술 소스로**.
⭐ **Read Aston Villa는 이번에 403이 풀렸다**(D+1 기사 2편 확보) — 할 일 0-3d의 「403 4패스 연속」 항목 갱신 대상.

### 접근 경로 지식
- ⭐ **에메리 회견은 스페인 매체가 아니라 avfc.co.uk를 브라우저로 여는 게 정답**
  (클라이언트 렌더링 → 3~4초 대기 후 `get_page_text`로 전문 취득 성공). 🇪🇸 Marca·AS·Relevo·MD·El Desmarque는 **2회차 연속 0건**.
- ⛔ **Cartilage Free Captain은 이 환경에서 접근 불가**(WebFetch 거부 + 브라우저 실패) → 대체로 **Spurs Web**.
- 🇸🇪 **린델뢰프 축은 일반 라운드에서 0건이 기본값**이다(패턴 확인 — 스웨덴 매체는 사건성 서사에서만 다루고
  일반 라운드 평점은 영국 매체를 재인용한다). **빅매치·대표팀 소집·사건 발생 시에만 돌릴 것.**
- 🇧🇷 브라질 매체의 PL 커버는 **브라질 선수 이벤트(골·부상·논란)에 종속**된다 — 주앙 고메스가 무득점·무도움이라
  ge.globo·Lance·UOL 0건. Trivela만 경기 리포트를 냈다.
- 🇮🇹 **pagelle는 D+1에도 0건** — 이탈리아 매체는 세리에A 외 리그에 숫자 평점을 잘 붙이지 않는다.
  Football Italia가 **FotMob 7.5를 인용**하는 방식으로 대체했다(이탈리아 자체 평점이 아니다).

### ⭐ 접근 경로 — 이번에 뚫린 것 (docs/30 소스 표 갱신 후보)
| 매체 | 결과 | 경로 |
|---|---|---|
| **avfc.co.uk** | ✅ 전면 접근 | 브라우저. **쿠키 배너만 뜨면 같은 URL 재navigate**(2회 재현) |
| **tottenhamhotspur.com 「Every word」** | ✅ **D+1 발행, 전문 확보** | 브라우저 |
| **The Athletic 전술 분석** | ✅ | 브라우저(기프트 링크). **WebFetch는 nytimes.com 차단** |
| **Birmingham Live** | ✅ **수확 최대** | 브라우저. 회견 전문·Townley 평점·부상 |
| **Guardian** | ✅ | 브라우저. **WebSearch/WebFetch는 도메인 차단** |
| **Read Aston Villa** | ✅ **403 아님** | 브라우저. ⏰ **할 일 0-3d의 「403 4패스 연속」 항목 갱신 대상** |
| **Spurs Odyssey** | ✅ | 브라우저. 라인업·교체 시각 대조에 유용 |
| football.london | ❌ 빌라 피드 미노출 | 구조 문제. `site:` 검색도 0건 |
| Cartilage Free Captain | ❌ 접근 불가 | WebFetch 거부 + 브라우저 실패 → **Spurs Web으로 대체** |
| Tanswell X `@J_Tanswell` | 🟡 **본문 말미 잘림** | 비로그인. Bluesky 공개 API는 D+1 신규 1건뿐 |

### ⛔ 소스 오류 — 인용 배제 권고 (신규 3건)
1. **WebSearch 요약 레이어가 원문에 없는 문장을 생성했다** — 「완비사카가 마무슈를 오프더볼로 넘어뜨려
   레드카드 위기」는 **어떤 1차 소스에도 없다**. 이번 회차 **2번째 요약 왜곡 사례**다.
   ⇒ ⭐ **검색 요약을 근거로 쓰지 말고 1차 소스 본문을 열어라**(docs/30 규약 재확인 사례).
2. **Spurs Odyssey**: 「Martinez, who like Morgan Rogers went to Chelsea」 — **마르티네스의 첼시행은
   다른 어떤 소스에서도 확인되지 않는다.** 이 매체의 **이적 서술은 채용하지 말 것**(라인업·시각은 정확했다).
3. **인명 전사 충돌**: 맥긴 인터뷰의 같은 문장이 avfc 공식판엔 「it took **Lucas Digne** time」,
   Birmingham Live판엔 「it took **Lamare [Bogarde]** time」로 다르다. ⇒ **병기하거나 이 문장은 배제**.

### ⚠️ 표기 충돌 (값은 덮지 말고 병기)
- **만잠비 교체 시각**: 우리 DB·Spurs Odyssey **72′** ↔ Townley 평점 기사 **75′**. **다수설 72′**.
- **맥긴/카마라 OUT**: Seneweb **84′** ↔ Spurs Odyssey·Townley **84~85′**. 1분 차.
- **만잠비 이적료**: The Athletic 「in excess of **£50m**」 ↔ Birmingham Live 「**£52 million** hijack」
  (뉴캐슬과 합의 직전 가로채기). 병기 권장.
- **루헤리 평점**: SofaScore 6.4 · FotMob 7.5 · Townley 6 · Villa News 6 · AVR 4 — **제공사·매체 차**.

### 미수행
- **영상 축의 다국어 스윕 0건** — 스즈키(일본어)·만잠비(프랑스어)·루헤리(이탈리아어) **영상**은 한 건도 훑지 않았다
  (영상 에이전트가 영어권으로 한정 지시받음). 기사 축은 다국어로 훑었다.
- `0-ibTNpHej0`(Harry's Football Debrief, 선수 평점) 자동자막 없음 — `yt_transcript_json3.py` 경로 미시도.
- 맥긴·부엔디아 avfc.co.uk 인터뷰 미확보(만잠비만 확보).
- 🇯🇵 D+1 신규 0건.

---

## 7. 이 세션이 하지 않은 것 (경계 명시)

- **DB 쓰기 0건.** `observations`·`match_reports`·`match_videos`·`player_duties` 전부 손대지 않았다.
- **리포트 본문 수정 0건.** `2026-09-19-avl-tottenham.md`는 읽기만 했다.
- `export.py`·`db_dump.sh`·커밋 **미실행**.
- 서브에이전트 3축(영상 / 회견·기사 / 전술블로그·다국어) **전부 완료**되어 이 파일에 반영됐다.
- ⭐ **카마라 건은 obs#866이 정본이다.** 이 세션도 같은 재수집으로 분포를 봤고 「전반 35% vs 후반 10%」로
  APPLIED를 제안했으나, 그것은 **CB 평균에 마진 4를 더한 컷**(x≤34.2)을 쓴 것이라 D+0이 건 임계(Δ≤8)를
  사후 완화한 셈이다. obs#866이 원래 임계를 지켰고 교차검증(자기 진영 한정 Δ=8.8)까지 했으므로 **obs#866을 따른다.**
