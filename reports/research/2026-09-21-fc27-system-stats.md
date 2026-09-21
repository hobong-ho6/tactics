<!-- 자동 생성: Workflow fc27-system-research (run wf_6927b4b8-516, 2026-09-21).
     수집 8에이전트(영·스·독·불·포르투갈 + EA 1차자료·역할·팀전술) → 저등급 주장 10건 2표 반증 → 종합.
     30/30 에이전트 완주·에러 0. 손편집 시 이 주석을 지우고 출처를 밝힐 것. -->

# EA SPORTS FC 27 게임 시스템·전술 구현·스탯 작용 — 8에이전트 다국어 수집 + 2표 반증 검증 리포트

수집일 2026-09-21 · 언어 커버리지: 영어 / 스페인어 / 독일어 / 프랑스어 / 포르투갈어(BR) + EA 1차 자료 전수 패스 + fut.gg 데이터 패스 + 팀전술 전용 패스
등급 표기: **(A)** EA 1차 자료 원문 · **(B)** 데이터마이닝/파일 분석 · **(C)** 통제 실측 또는 게임 내 UI 직독 · **(D)** 근거 없는 통설
⚠️ 시점 제약: FC27은 얼리액세스 2026-09-18, 정식 출시 2026-09-25다. 이 리포트는 **출시 4일 전** 상태의 자료다.

---

## 1. 한 문단 요약

이 조사로 확실해진 것은 **"FC27이 스탯 쪽으로 무게추를 옮겼다"는 방향성**이다 — EA는 FC27 목표를 「Our goal for FC 27 is to refine the balance between PlayStyles and Attributes so that both have a meaningful impact on player performance without feeling overpowered.」(「FC27의 목표는 PlayStyle과 스탯 사이의 균형을 다듬어, 둘 다 과도하게 느껴지지 않으면서도 선수 퍼포먼스에 의미 있는 영향을 주도록 하는 것이다」)라고 명시했고(A, FC27, https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive), 실제로 PlayStyle 10종의 보너스 항을 개별적으로 깎았으며, AI 수비 영향력을 줄이고 수동 수비를 강화했고, FUT의 PlayStyle+ 상한을 5→3으로 내리는 동시에 모든 스페셜 카드에 Role++를 일괄 부여해 역할 숙련도를 변별력 없는 상수로 만들었다(전부 A, FC27). 반면 **여전히 모르는 것이 이 리포트의 절반 이상**이다: ① EA는 FC27 1차 자료 어디에서도 Reactions·Ball Control·Composure·First Touch를 **단 한 번도** 언급하지 않았고(A, FC27 — 키워드 전수 스캔 각 0회), ② PlayStyle이 원 스탯과 곱셈인지·임계값인지·독립 판정인지 EA가 밝힌 적이 없으며, ③ 역할/포커스를 바꿨을 때 선수가 실제로 몇 미터 움직이는지에 대한 **공개 통제 실측이 어느 언어권에도 0건**이고, ④ 팀 전술 라인 높이 구간값(1–30/31–60/61–90/91–100)은 FC25 피치노트 이후 EA가 FC27에서 재확인한 적이 없는 캐리오버 추정이다. 8개 에이전트 전원이 **C등급(통제 실측) 0건, B등급(데이터마이닝) 0건**을 보고했는데, 이는 검색 실패가 아니라 FC27이 아직 출시되지 않아 데이터가 축적될 시간이 없었기 때문이다 — 출시 2~4주 후 재수집이 필수다.

---

## 2. 스탯 작용

### 2.0 대전제 — FC27 1차 자료에는 이 세 스탯이 없다

FC27 Gameplay Deep Dive 본문 전수 키워드 스캔 결과 **Reactions 0회 / Ball Control 0회 / Composure 0회 / "First Touch"(속성·PlayStyle명) 0회**다(A, FC27, https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive). FC27 Closed Beta Feedback Update에서도 네 항목 전부 0회이고, FC27 Career Deep Dive·Ratings Deep Dive에서도 미언급이다(A, FC27). 유일하게 FC27 The Grounds & Clubs Deep Dive에 Reactions 1회·Ball Control 1회·Composure 2회가 나오지만, 전부 **Pro 아키타입 마스터리 보상 표의 항목명**일 뿐 기능 설명이 아니다(A, FC27). help.ea.com에도 FC27 속성 설명 문서가 존재하지 않는다(A, FC27 — 검색 결과 21건 전량 확인). 따라서 **이 세 스탯에 대한 FC27 기준 1차 근거는 존재하지 않으며, 아래 서술은 전부 FC26 자료의 전용(轉用)이거나 통설이다.**

또한 **FC27 넘버링 타이틀 업데이트는 2026-09-21 현재 한 건도 발행되지 않았고**, EA는 「we do not plan on making significant gameplay balance changes in our early Title Updates」(「초기 타이틀 업데이트에서는 유의미한 게임플레이 밸런스 변경을 할 계획이 없다」)고 명시했다(A, FC27, https://www.ea.com/games/ea-sports-fc/fc-27/news/fc-27-closed-beta-feedback-update). 즉 **현재 밸런스 정본 = 런치 빌드 = Gameplay Deep Dive + Closed Beta Feedback Update 두 문서**다.

### 2.1 볼컨트롤 (Ball Control)

EA가 이 스탯의 작용을 명시한 유일한 1차 서술은 FC26의 퍼스트 터치 난이도 설명이다(A, FC26): 「Factors influencing the difficulty of a first touch include ball speed relative to the player's speed, ball height, requested exit angle, opponent pressure, the part of the body used for the touch, the extent of stretching, and player attributes such as Ball Control, Interceptions, and Composure.」(「퍼스트 터치의 난이도에 영향을 주는 요인에는 선수 속도 대비 볼 속도, 볼 높이, 요구되는 이탈 각도, 상대의 압박, 터치에 사용된 신체 부위, 뻗는 정도, 그리고 볼컨트롤·인터셉트·침착 같은 선수 속성이 포함된다.」 / https://www.ea.com/games/ea-sports-fc/fc-26/news/pitch-notes-fc26-gameplay-deep-dive)

여기서 읽어야 할 세 가지(전부 A, FC26):
- **퍼스트 터치는 볼컨트롤 단독 판정이 아니다.** 볼컨트롤·인터셉트·침착 **세 스탯의 복합**이며, 그 위에 상황 변수 6종이 얹힌다. 「퍼스트 터치 = 볼컨트롤」이라는 통념은 EA 1차 서술과 다르다.
- **Reactions와 Dribbling은 이 목록에 없다.** EA가 「드리블 스탯이 수신에 관여한다」고 말한 적도, 「관여하지 않는다」고 말한 적도 없다 — 언급 자체가 없다.
- **유저 입력이 스탯을 일부 보상한다**: 「holding L2 || LT will greatly improve the players ability to control the ball at the trade-off of player's move speed. Earlier timing of this input will result in increased control.」(「L2/LT를 누르고 있으면 선수의 이동 속도를 대가로 공을 다루는 능력이 크게 향상된다. 이 입력을 더 일찍 넣을수록 컨트롤이 더 좋아진다.」) → 낮은 볼컨트롤 카드의 트랩 열세는 **조작으로 일부 메울 수 있다**(A, FC26).

FC27 신규 기능 중 볼컨트롤이 **명시적으로 배제된** 사례가 하나 있다. Off-Balance Dribbling은 「Driven by Balance, Agility and Dribbling Attributes」(「Balance·Agility·Dribbling 속성으로 구동되며」)로 정의되고 볼컨트롤이 입력값에 없다(A, FC27, https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive). 독일어판은 판정 조건을 더 구체적으로 쓴다: 「Wenn ein Dribbelprofi mit den benötigten Werten von einem Zusammenprall, einem Rempler oder einem Schulterrempler getroffen wird, geht der Profi in eine Dribbling-im-Stolpern-Animation über.」(「필요한 수치를 갖춘 드리블 선수가 충돌·몸싸움·어깨싸움을 당하면, 그 선수는 '비틀거리며 드리블' 애니메이션으로 전환된다.」 / A, FC27, https://www.ea.com/de-de/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive) — 「benötigten Werten」(필요한 수치)이라는 표현은 **계단형 게이팅**을 시사하나 EA가 컷 수치를 공개하지 않았다.

⚠️ 상충 자료 1건: gamereactor.fr의 EA 밴쿠버 핸즈온 기사는 「un mécanisme permet aux joueurs ayant le meilleur contrôle de balle de conserver la possession」(「볼컨트롤이 가장 좋은 선수가 소유권을 유지하게 해주는 메커니즘이 있다」)라고 썼으나, EA 공식 프랑스어판은 같은 메커니즘의 입력값으로 「équilibre, agilité et dribble」(균형·민첩성·드리블)을 명시한다(A, FC27, https://www.ea.com/fr/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive). **기자 인상평(D)이 EA 1차(A)와 충돌하므로 EA를 채택한다.** 접촉 유지 판정에 볼컨트롤이 들어간다는 서술은 1차 근거 없음.

**결론(볼컨트롤)**: 볼컨트롤은 **정적 수신(트랩) 축**의 스탯이고, **접촉·경합 중 유지 축**은 Balance·Agility·Dribbling이 가져간다(A, FC26+FC27). 즉 "압박 하에서 공을 지킨다"는 하나의 체감이 게임 내부에서는 **두 개의 다른 판정식**으로 갈라져 있다.

### 2.2 침착 (Composure)

EA 1차 자료로 확인되는 것은 **두 가지뿐**이다:
1. FC26 퍼스트 터치 난이도 계산의 입력 속성 중 하나(A, FC26 — 위 인용). 포르투갈어판도 동일: 「qualidades de atleta como controle de bola, interceptações e frieza」(「볼컨트롤·인터셉트·침착 같은 선수 스탯」 / A, FC26, https://www.ea.com/pt-br/games/ea-sports-fc/fc-26/news/pitch-notes-fc26-gameplay-deep-dive).
2. 페널티킥의 Composure Circle(링) 수축 속도와 퍼펙트 타이밍 창 크기 결정(A, FC25 — 반증 검증 과정에서 확인됨).

**그 외의 모든 침착 서술은 1차 근거가 없다.** 특히 널리 퍼진 "압박 인지 반경" 정의 — 「Este atributo determina a qué distancia el jugador con la pelota comienza a sentir la presión del oponente.」(「이 속성은 볼을 가진 선수가 상대의 압박을 느끼기 시작하는 거리를 결정한다.」 / D, 버전 불명, https://es.fifauteam.com/atributos-en-fifa-21/) — 는 **2/2 반증으로 기각**됐다. 상세는 §8을 볼 것. 독일어권 용어집도 같은 정의를 반복한다: 「Ruhe: Dieser Wert zeigt, ab Entfernung der Spieler durch einen Gegenspieler unter Druck gerät.」(「침착: 이 값은 선수가 상대 선수에 의해 어느 거리부터 압박을 받게 되는지를 보여준다.」 원문 오탈자 그대로 / D, 버전 불명, https://onefootball.com/de/news/fifa-23-spielerattribute-erklaert-dribbling-36441917) — 그러나 이는 독립 관측이 아니라 **동일 계보의 복제**이므로 다국어 교차검증으로 카운트할 수 없다.

**프로젝트 반영 지침**: 침착을 **'거리 파라미터'가 아니라 '압박 하 액션 오차 계수(퍼스트 터치 포함)'로 기록**할 것. 거리 해석은 채택하지 않는다.

### 2.3 반응력 (Reactions)

**이 축은 사실상 빈손이다.** EA 1차 자료(FC25·FC26·FC27 피치노트 전문 + EA Help 전체) 어디에도 Reactions의 정의·작용 서술이 **없다**(A, FC25~FC27 — 부재 증거). FC26 퍼스트 터치 인자 목록에도 미포함이다(A, FC26).

특히 **"반응력은 AI 팀메이트에게만 의미가 있다"는 통설과, 그 통설을 부정하는 반론 모두 근거가 없다.** 스페인어권 표준 해설은 「Muchas personas piensan que este atributo sólo tiene importancia sobre los jugadores que están siendo controlados por la computadora ... pero esto no es cierto.」(「많은 사람들이 이 속성은 컴퓨터가 조작하는 선수에게만 의미가 있다고 생각한다 … 그러나 이는 사실이 아니다.」 / D, 버전 불명, https://es.fifauteam.com/atributos-en-fifa-21/)라고 명시적으로 부정하지만, 이는 **2/2 반증으로 기각**됐다 — 측정 근거가 없고, 영어 원문과 스페인어 번역판이 동일 출처라 다국어 교차검증에 해당하지 않으며, FIFA16 이후 재검증 없이 복제돼 온 텍스트다(§8 참조).

**조작 주체(유저 vs AI)에 따라 스탯 작용이 달라진다는 EA의 유일한 명시적 진술**은 반응력이 아니라 **수비 리치 한 건뿐**이다(A, FC27): 「We've also reduced AI defensive reach for interceptions. A manually-controlled defender will be able to reach further than an AI-controlled defender, encouraging you to switch to the player actively defending instead of relying on AI teammates to win possession. … Previously, AI-controlled defenders could automatically attempt to win the ball when a dribbler came close enough to them. In FC 27, defenders will now rely more on their positioning and support the play until you take control and choose when to make a tackle. … The following changes to AI Defending only apply to Competitive gameplay.」(「우리는 인터셉트에 대한 AI의 수비 리치도 줄였다. 수동 조작 중인 수비수는 AI 조작 수비수보다 더 멀리 닿을 수 있게 되며, 이는 AI 팀메이트가 공을 따내 주기를 기대하는 대신 실제로 수비하는 선수로 전환하도록 유도한다. … 이전에는 드리블러가 충분히 가까워지면 AI 조작 수비수가 자동으로 공을 따내려 시도할 수 있었다. FC27에서 수비수는 이제 자신의 위치 선정에 더 의존하며, 당신이 조작을 넘겨받아 태클 시점을 고를 때까지 플레이를 받쳐 준다. … 다음 AI 수비 변경 사항은 Competitive 게임플레이에만 적용된다.」 / https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive)

⚠️ **마지막 문장이 중요하다** — 이 변경은 **Competitive(얼티밋팀) 게임플레이 전용**이고 Authentic 프리셋에는 적용되지 않는다(A, FC27). 우리 실측 설계에서 프리셋을 반드시 통제 변수로 고정해야 하는 이유다.

**세컨볼 경합·루즈볼 반응 개시·애니메이션 전환을 어떤 스탯이 판정하는가** — 영어·스페인어·독일어·프랑스어·포르투갈어 5개 언어권 전부에서 A/B/C 어느 등급도 찾지 못했다. FC27 딥다이브에 loose ball이 1회 등장하지만 「AI 수비수가 루즈볼이 닿는 범위에 오면 여전히 소유권을 얻을 수 있다」는 서술뿐 스탯 귀속이 없다(A, FC27).

---

## 3. PlayStyles와 원 스탯의 관계

### 3.1 FC27의 방향은 전 언어권에서 일관된다

EA는 FC27에서 **PlayStyle과 스탯의 격차 축소**를 공식 목표로 선언했다(A, FC27). 포르투갈어판이 문제 인식까지 적어 두어 가장 명확하다: 「Ouvimos os comentários da comunidade sobre alguns Estilos de Jogo que pareciam ter um impacto muito grande em determinadas situações. Nosso objetivo no FC 27 é aprimorar o equilíbrio entre Estilos de Jogo e Qualidades para que os dois fatores tenham um impacto significativo.」(「일부 플레이스타일이 특정 상황에서 지나치게 큰 영향을 준다는 커뮤니티 의견을 들었다. FC 27의 목표는 플레이스타일과 스탯 사이의 균형을 개선해 두 요소 모두가 유의미한 영향을 갖게 하는 것이다.」 / A, FC27, https://www.ea.com/pt-br/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive)

**FC27에서 변경된 PlayStyle은 정확히 10종**이다(A, FC27 — EA 1차 전수 확인): Finesse Shot, Technical Dribbler, Intercept, Rapid, Quick Step, Pinged Pass, Tiki Taka, Jockey, Precision Header, Low Driven. 여기에 Closed Beta 후속으로 **Bruiser+ 추가 효과 소폭 축소**가 붙는다(A, FC27). **FC27 신규 PlayStyle은 1차 자료에 한 건도 발표되지 않았다**(A, FC27) — 독일어권 확인도 일치한다: 「Neue Spielstile gibt es in dieser Saison zwar nicht」(「이번 시즌 신규 플레이스타일은 없다」 / C, FC27, eurogamer.de). 36종·6카테고리 구조가 유지된다.

### 3.2 결합 방식 — 곱셈이 아니라 "떼어낼 수 있는 보너스 다발"

**EA는 PlayStyle과 원 스탯이 어떻게 결합되는지 한 번도 명시한 적이 없다**(A, FC27 — 부재 증거). 그러나 **변경 서술 방식 자체**가 구조를 드러낸다. 가장 결정적인 사례는 Low Driven이다(A, FC27):

> 「Low Driven — Removed the shot speed boost previously applied to low-driven shots. Shot velocity now scales purely based on core shooting Attributes and input power, for more consistent and attribute-driven results. The Playstyle and PlayStyle+ still add an accuracy boost」
> (「낮고 강한 슛에 적용되던 슛 속도 부스트를 제거했다. 이제 슛 속도는 오로지 코어 슈팅 속성과 입력 파워에만 기반해 스케일하며, 더 일관되고 속성 주도적인 결과를 낸다. 해당 PlayStyle과 PlayStyle+는 여전히 정확도 부스트를 더한다.」 / https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive)

**속도 부스트만 떼어내고 정확도 부스트는 남겼다** — 이는 PlayStyle이 원 스탯에 곱해지는 단일 배율이 아니라, **액션별로 독립적으로 얹히고 독립적으로 제거 가능한 효과 다발**임을 보여준다(A, FC27 — 단, 이는 EA의 변경 서술 방식으로부터의 추론이며 EA가 "가산/독립 부스트다"라고 명시한 것은 아니다. 이 구분을 유지할 것).

같은 구조가 Intercept에서 반대 방향으로 나타난다: 「Intercept: Increased reach and improved chances of retaining possession of the ball when performing an interception for Non-PlayStyle players who have a high Interceptions Attribute.」(「높은 인터셉트 스탯을 가진 비(非)PlayStyle 선수의 리치를 늘리고, 인터셉트 수행 시 공을 계속 소유할 확률을 개선했다.」 / A, FC27) — **PlayStyle 없는 고스탯 선수만 골라 상향**할 수 있다는 것은 두 축이 같은 결과값에 합산되는 구조임을 시사한다(추론).

### 3.3 ⭐ First Touch ↔ 볼컨트롤 한계효용 — **정량 답을 찾지 못했다**

이것이 이번 조사의 **최대 미해결 항목**이며, 5개 언어권 전원이 동일하게 실패를 보고했다.

확인된 것:
- **First Touch PlayStyle은 FC27 변경 목록 10종에 포함되지 않았다**(A, FC27) → EA 기준 FC26 사양 유지로 추정되나 명시는 없다.
- 공식 효과 서술은 스페인어 카탈로그 페이지가 가장 간결하다: 「Menos errores al recibir el balón, transición de regate más rápida」(「볼을 받을 때 실수가 줄어들고, 드리블 전환이 더 빠르다」 / A, FC27, https://www.ea.com/es/games/ea-sports-fc/ratings/abilities-ratings/first-touch/play-style/trait1_4194304). **"볼컨트롤 원값을 대체한다"는 표현은 EA 1차 자료 어디에도 없다**(A, FC27).

찾지 못한 것: **같은 선수의 볼컨트롤만 바꿔 트랩 오차를 측정한 통제 실측이 영어·스페인어·독일어·프랑스어·포르투갈어 전부에서 0건**이다. futbin·fut.gg·futmind·fcradar·millenium·dexerto 등은 전부 EA 설명문(「reduced error」/「minimal error」)을 그대로 복사한 D등급이다. ⇒ **"First Touch를 붙이면 볼컨트롤 70짜리가 볼컨트롤 90처럼 되는가"에 대한 답은 현재 존재하지 않으며, 우리가 직접 측정해야 한다.**

### 3.4 ⭐ 가장 실무적으로 중요한 변경 — "패서가 리시버의 터치를 덮어주던 경로"가 끊겼다

이것은 **5개 언어권 EA 공식판 전부에서 독립 확인된** 유일한 항목이다(A, FC27).

영어: 「Pinged Pass — Removed the effect that slightly reduced trap error on the pass receiver. This change ensures that the PlayStyle primarily enhances pass delivery rather than providing an additional first-touch advantage to an unrelated player. / Tiki Taka — Removed the animation playback speed boost and the effect that slightly reduced trap error on the pass receiver.」(「Pinged Pass — 패스 수신자의 트랩 오차를 약간 줄여주던 효과를 제거했다. 이 변경으로 해당 PlayStyle은 무관한 선수에게 추가적인 퍼스트 터치 이점을 주는 대신 패스 전달력 자체를 향상시키는 데 주력하게 된다. / Tiki Taka — 애니메이션 재생 속도 부스트와 패스 수신자의 트랩 오차를 약간 줄여주던 효과를 제거했다.」 / https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive)

독일어: 「Wir haben den Effekt entfernt, durch den die Ballannahme-Fehlerquote beim passempfangenden Profi leicht verringert wurde. Diese Änderung sorgt dafür, dass der PlayStyle in erster Linie den Pass verbessert, statt einem anderen Profi zusätzlich einen Vorteil bei der Ballannahme zu geben.」(「패스를 받는 선수의 볼 수신 오차율을 소폭 낮춰주던 효과를 제거했다. 이 변경으로 이 PlayStyle은 무엇보다 패스 자체를 개선하게 되며, 다른 선수에게 볼 수신 상의 추가 이점을 주지 않는다.」 / https://www.ea.com/de-de/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive)

프랑스어: 「Passe fusante : Suppression de l'effet qui réduisait légèrement l'erreur de contrôle pour le receveur de passe」(「핑드 패스: 패스 수신자의 컨트롤 오차를 소폭 줄여주던 효과 삭제」 / https://www.ea.com/fr/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive)

포르투갈어: 「Removemos o impulso de velocidade da animação e o efeito que reduzia levemente o erro de domínio em atletas que recebiam o passe.」(「애니메이션 속도 부스트와, 패스를 받는 선수의 트래핑 오차를 약간 줄여주던 효과를 제거했다.」 / https://www.ea.com/pt-br/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive)

스페인어권 2차 정리도 같은 함의를 뽑았다: 「la calidad del receptor debe evaluarse por separado; un buen pasador no transfiere sus atributos de control al compañero.」(「수신자의 질은 별도로 평가되어야 한다; 좋은 패서가 자신의 컨트롤 속성을 동료에게 전달하지는 않는다.」 / C, FC27, https://www.itemd2r.com/blog/fc-27/fc-27-cambios-playstyles-explicados-repaso-completo-deep-dive)

**우리 프로젝트 함의**: FC26까지는 "패서를 좋게 만들면 리시버의 퍼스트 터치도 좋아진다"가 성립했다. **FC27에서는 성립하지 않는다.** 티키타카형 짧은 연계 구현에서 **리시버 본인의 볼컨트롤·침착·First Touch PlayStyle을 각자 따로 평가**해야 하며, 패서의 PlayStyle로 리시버의 결점을 가리는 처방은 FC27에서 폐기해야 한다(A, FC27).

### 3.5 나머지 변경 — 스피드 계열 하향, 슛 계열 스탯화

- Rapid / Quick Step: 「Reduzimos o impulso de velocidade aplicado a atletas com o Estilo de Jogo e o Estilo de Jogo+ ao conduzir a bola e acelerar … Isto torna a Qualidade Aceleração mais importante.」(「해당 플레이스타일 및 플레이스타일+를 가진 선수가 드리블하고 가속할 때 적용되던 속도 부스트를 축소했다. … 이로써 '가속' 스탯이 더 중요해진다.」 / A, FC27) → **PlayStyle 슬롯을 스피드에 쓰는 가치가 전년보다 낮아졌다**.
- Finesse Shot: 「Nous avons mis à jour le tir en finesse pour que les attributs des joueurs jouent un rôle plus important」(「선수 스탯이 더 큰 역할을 하도록 피네스 슛을 수정했다」 / A, FC27, https://www.ea.com/fr/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive).
- PlayStyle과 PlayStyle+ **사이의 격차도 축소**: 「se reduce la diferencia entre tener determinados Estilos de juego y sus versiones "+", dando más importancia a los atributos naturales del futbolista」(「특정 플레이스타일을 보유하는 것과 그 '+' 버전 사이의 차이가 줄어들어, 선수의 타고난 속성에 더 큰 비중이 실린다」 / C, FC27, https://vandal.elespanol.com/guias/guia-ea-sports-fc-27-trucos-consejos-y-secretos/novedades-y-cambios).
- FUT 상한: 「we're reducing the maximum number of PlayStyle+ available on a single Item from five to three, alongside reducing the scale of Attribute upgrades throughout the year」(「한 아이템이 가질 수 있는 PlayStyle+ 최대 개수를 5개에서 3개로 줄이고, 연중 스탯 업그레이드의 규모도 함께 축소한다」 / A, FC27, https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-fut-deep-dive).

**진화 설계 함의**: PS+ 스택 전략의 상한이 5→3으로 내려갔고 스탯 상승 폭 자체도 축소됐다 — **진화 기대값이 PlayStyle+에서 원 스탯 쪽으로 이동**했다(A, FC27).

---

## 4. 역할·포커스 → 선수 움직임

### 4.1 정의 — 적용 국면이 분리되어 있다

EA의 가장 압축적인 정의는 독일어판 FC25 FC IQ Deep Dive에 있다(A, FC25): 「Ihr könnt unsere Systeme folgendermaßen betrachten: HyperMotionV bezieht sich auf die einzigartigen Bewegungs-Merkmale der Profis. Der GES-Wert bildet die physischen und mentalen Attribute ab. Die PlayStyles sind die Fähigkeiten am Ball. Und die Rollen sind die Fähigkeiten ohne Ball.」(「우리 시스템은 이렇게 보면 된다: HyperMotionV는 선수 고유의 움직임 특성을 다룬다. 종합 능력치(GES)는 신체적·정신적 속성을 나타낸다. PlayStyle은 공을 가진 상태의 능력이다. 그리고 역할(Rollen)은 공 없는 상태의 능력이다.」 / https://www.ea.com/de-de/games/ea-sports-fc/fc-25/news/pitch-notes-fc-25-fc-iq-deep-dive)

영어 원문의 정의도 같다(A, FC25): 「Player Roles guide how every player thinks, behaves, and moves off the ball.」(「플레이어 역할은 모든 선수가 공 없이 어떻게 생각하고 행동하고 움직이는지를 인도한다.」) / 「While a Role dictates the primary responsibilities of the player, the Focus is a modifier upon the Role that enables you to tweak one or two characteristics of it slightly.」(「역할이 선수의 주된 임무를 규정하는 반면, 포커스는 역할 위의 수식자로서 그 특성 한두 가지를 약간 조정할 수 있게 해준다.」 / https://www.ea.com/en/games/ea-sports-fc/fc-25/news/pitch-notes-fc-25-fc-iq-deep-dive)

**⇒ 역할 변경은 원칙적으로 온더볼 스탯 성능이 아니라 오프더볼 움직임을 바꾼다**(A, FC25). 한 가지 유의: EA가 "조작 중인 선수에게는 역할이 작동하지 않는다"고 명시한 1차 문장은 **찾지 못했다** — off-ball 규정에서 강하게 함의될 뿐이므로 단정하지 않는다.

### 4.2 역할 숙련도 — 스탯 시트를 건드리지 않는 제3의 항

가장 중요한 1차 수치다(A, FC25): 「Before FC IQ, we used either the Positioning Attribute or Defensive Awareness Attribute to determine how good the AI players were in the system (in any calculation required). Now, instead of just Positioning or Defensive Awareness, we also use Familiarity in every formula. The rate at which we use Familiarity varies from context to context, but it can account for 10% to 40% of the result.」(「FC IQ 이전에는 AI 선수들이 시스템 안에서 얼마나 잘하는지를 (필요한 모든 계산에서) Positioning 속성이나 Defensive Awareness 속성 중 하나로 판정했다. 이제는 Positioning이나 Defensive Awareness만이 아니라 모든 공식에 숙련도(Familiarity)도 함께 사용한다. 숙련도를 적용하는 비율은 맥락마다 다르지만, 결과값의 10%에서 40%까지를 차지할 수 있다.」 / https://www.ea.com/en/games/ea-sports-fc/fc-25/news/pitch-notes-fc-25-fc-iq-deep-dive)

**정확한 해석**(A, FC25): "스탯 보정인가 행동 정교함인가"의 답은 **"둘 다이되, 스탯 시트를 건드리지 않는 제3의 항"**이다. 카드의 표시 숫자는 그대로이지만, 내부 포지셔닝 계산식에서는 **스탯과 동일한 수치 채널**에 들어가 결과의 10~40%를 차지한다. 「Rol+는 패스 레인을 0.5초 먼저 인식한다」류의 시간 단위 수치는 **창작이며 인용 금지**다(§8 참조).

행동 이행률의 계단은 EA가 예시로 설명했다(A, FC25): 「A Poacher++ will focus solely on attacking. A Poacher+ will put most of their effort into attack. A base Poacher will attempt to attack but may sometimes not put all their effort into it. An out-of-position Poacher may slack on their attacking duties.」(「포처++는 오직 공격에만 집중한다. 포처+는 노력 대부분을 공격에 쏟는다. 기본 포처는 공격을 시도하지만 때로는 전력을 다하지 않을 수 있다. 포지션을 벗어난 포처는 공격 임무를 게을리할 수 있다.」) — **행동 목록이 아니라 행동 이행률이 갈린다**(A, FC25). 독일어판은 추가로 「Je niedriger die Vertrautheit ist, desto länger dauert der Übergang der Profis.」(「숙련도가 낮을수록 선수의 (공수) 전환에 걸리는 시간이 길어진다.」 / A, FC25)를 명시한다.

⚠️ **버전 이월 금지**: FC26 Gameplay Deep Dive는 「Significantly improved usage of regular Roles and Roles+, to bring them closer to Roles++」(「일반 Role과 Role+의 활용을 크게 개선해 Role++에 근접시켰다」)와 「Drastically reduced the negative impact of being Out of Position」(「포지션 이탈의 불이익을 대폭 축소」)을 명시했다(A, FC26). **FC26에서 티어 간 격차가 의도적으로 좁혀졌으므로 FC25의 Poacher 예시 강도를 FC26·FC27에 그대로 적용하면 안 된다.** 10~40% 수치도 FC26·FC27에서 재공시된 적이 없다.

### 4.3 FC27의 3층 위계 — 이번 세대의 핵심 구조

FC27 Closed Beta Feedback Update가 **처음으로 역할과 숙련도의 작용점을 분리해 명시**했다(A, FC27):

> 「Player Roles continue to determine the types of runs a player can make based on their position and Role. … Role Familiarity then influences the urgency with which a player makes those available runs. Players with greater familiarity in a Role, including Role+ and Role++, will show more urgency when making those movements. Attacking Spatial Awareness doesn't replace Player Roles. Instead, the two systems work together to influence a player's attacking movement.」
> (「플레이어 역할은 선수의 포지션과 역할에 따라 그 선수가 할 수 있는 런의 종류를 계속해서 결정한다. … 그다음 역할 숙련도가 선수가 그 가능한 런들을 수행하는 긴급성에 영향을 준다. Role+와 Role++를 포함해 특정 역할에 대한 숙련도가 높은 선수일수록 그 움직임을 만들 때 더 높은 긴급성을 보인다. Attacking Spatial Awareness는 플레이어 역할을 대체하지 않는다. 대신 두 시스템이 함께 작동해 선수의 공격 움직임에 영향을 준다.」 / https://www.ea.com/games/ea-sports-fc/fc-27/news/fc-27-closed-beta-feedback-update)

| 층 | 결정하는 것 | 근거 |
|---|---|---|
| **Role** | 어떤 **종류**의 침투가 가능한가 (런의 메뉴) | A, FC27 |
| **Role Familiarity (+/++)** | 그 침투를 얼마나 **적극적으로(urgency)** 실행하는가 | A, FC27 |
| **Attacking Spatial Awareness (신규)** | 빈 **공간을 인지해 점유**하는가 (곡선 런) | A, FC27 |

프랑스어판이 ASA의 동작을 더 구체적으로 쓴다: 「Notre perception spatiale en attaque mise à jour rend les attaquants de l'IA plus conscients de l'espace qui les entoure … ils effectuent désormais des appels courbés plus intelligents et contextuels qui soutiennent mieux chaque mouvement offensif」(「업데이트된 공격 공간 인지는 AI 공격수가 주변 공간을 더 잘 인지하게 만든다 … 이제 그들은 더 영리하고 상황에 맞는 곡선형 침투 움직임을 수행해 공격 전개를 더 잘 뒷받침한다」 / A, FC27, https://www.ea.com/fr/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive).

**⭐ 우리 히트맵 축에 직접 타격이 있는 지점**: EA 스스로 도입 사유로 「Roles can sometimes feel too strict in gameplay」(「게임플레이에서 역할은 때때로 너무 엄격하게 느껴질 수 있다」)를 인정했다(A, FC27). 즉 **역할 히트맵이 예측하는 위치의 결정성은 FC26보다 약해졌다** — 약화 폭은 EA가 수치로 밝히지 않았다. 우리 실측 설계는 **단판 히트맵이 무효**이고 역할당 최소 5~10경기 누적 평균이 필요하며, **버전·프리셋(Competitive/Authentic)·Role Familiarity(Base/+/++) 3개를 통제 변수로 고정**해야 한다.

### 4.4 ⭐ FC27 FUT에서 역할 숙련도는 상수가 된다

「Building on that feedback, all special Items released throughout the year in EA SPORTS FC™ 27 will receive Role++ familiarity across every role in their primary and secondary positions, giving players more freedom to shape their squad and tactics.」(「그 피드백을 바탕으로, EA SPORTS FC 27에서 한 해 동안 출시되는 모든 스페셜 아이템은 주포지션과 부포지션의 모든 역할에 걸쳐 Role++ 숙련도를 받게 되며, 이를 통해 스쿼드와 전술을 구성할 자유가 더 커진다.」 / A, FC27, https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-fut-deep-dive)

**결과**(A, FC27):
- FUT 스쿼드에서 "누가 이 역할에 숙련됐나"는 **카드 선택 기준에서 탈락**한다.
- Role+/++를 부여하던 **진화의 가치가 스페셜 카드 한정으로 소멸**한다(베이스 카드에는 남는다).
- 역할 선택이 **순수하게 움직임 설계 문제**로 환원된다.
- ⚠️ **커리어 모드·베이스 카드에는 해당하지 않는다.**

### 4.5 ⛔ 이 축에서 기각된 정량 주장 2건

이번 조사에서 **역할 축의 정량 주장 두 건이 모두 2/2 반증으로 기각**됐다. 상세는 §8을 볼 것. 요약하면:
- **"FC27 역할 카탈로그 = FC26과 완전 동일"** → fut.gg `/api/fut/roles/`에 버전 인자가 없고 `?game=26`과 `?game=27` 응답의 md5가 동일(bd4280cb715b26c6c68fc9b9a9c5c5e8, 354,999B)하며, last-modified가 얼리액세스(09-18) 이전이다. **동일성 확인이 아니라 미확정(UNKNOWN)**이다.
- **"포커스보다 역할이 2배 이상 움직인다"** → 수치가 FC26 카탈로그에서 나왔고, 재계산하면 1.16~1.33배이며, 동일 포지션 역할쌍의 35%는 포커스 중앙값보다도 덜 움직인다.

**살아남은 것**(D, FC27 — 0/2 반증): **같은 선수·같은 포메이션·같은 팀 전술에서 역할(또는 포커스)만 바꿔 히트맵·평균 위치 변화를 반복 측정한 공개 통제 실측은 FC25·FC26·FC27 어느 버전에서도, 영·독·일·서어 웹 검색 범위에서 발견되지 않았다.** (단 YouTube·Reddit·Discord 영상/스레드는 미탐색 — 등급 D의 근거는 '부재'가 아니라 '탐색 한계'다.) 또한 **EA가 제공하는 것은 측정 히트맵이 아니라 "Activity Map"(역할별 활동 영역 일러스트)과 인게임 전술 화면의 우스틱 토글 프리뷰이며, 수치가 붙지 않은 정성 시각물**이다(A, FC25) — **이 축의 정량 근거는 현재 사실상 0이다.**

---

## 5. 팀 전술 파라미터 → 팀 움직임

### 5.1 파라미터 집합 — 무엇이 있고 무엇이 없는가

FC25 FC IQ 개편에서 **다음 슬라이더가 삭제됐고 FC27까지 돌아오지 않았다**(A, FC25): 「As a result of all the changes, the following settings have been transformed or removed from the game: Removed: Defensive Width, Chance Creation, Attacking Width, Pressure, Players in Box, Players in Corners, Players in Free Kicks」(「이 모든 변경의 결과로 다음 설정들이 변형되거나 게임에서 제거되었다: 제거됨 — 수비 폭, 찬스 크리에이션, 공격 폭, 압박, 박스 안 인원, 코너 인원, 프리킥 인원」 / https://www.ea.com/en/games/ea-sports-fc/fc-25/news/pitch-notes-fc-25-fc-iq-deep-dive)

대신: 「the Roles now determine your team's width, directly affect your chance creation, and also help inform what type of pressure the players exert.」(「이제 Role이 팀의 폭을 결정하고, 찬스 크리에이션에 직접 영향을 주며, 선수들이 어떤 유형의 압박을 가하는지도 규정한다.」 / A, FC25)

**⇒ 「폭을 한 칸 넓힌다」는 조작은 존재하지 않는다**(A, FC25). 전술 요약 화면의 Width는 조절 항목이 아니라 포메이션·Role 배치의 **결과를 읽어주는 산출 지표**다 — Winger / Half-Winger / Wide Playmaker 같은 역할 배치로만 간접 구현된다.

**감독 전술 재현 가능/불가능 정리**(A, FC25+FC27):
- 가능: 라인 높이·블록 깊이, 전환 속도(빌드업 스타일), 무소유 시 형태(포메이션), 소유 시 형태·폭(11개 Role/Focus), 경기 중 전술 5개 전환
- **불가능**: 폭을 독립 축으로 조절 / 압박 강도를 라인별로 분리 / 압박 트리거 조건 지정 / 맨마킹 지정 / 중간블록+전방압박 하이브리드

### 5.2 수비 접근 — 한 칸이 3~4가지를 동시에 바꾼다

EA 정의(A, FC25): 「FC 25 has four Defensive Approaches, which combine Line Height/Depth, Pressure, and Run Tracking. Each Defensive Approach is directly connected to your team's Line Height, which you can manually adjust between specific values.」(「FC 25에는 라인 높이/깊이·압박·런 트래킹을 결합한 네 가지 Defensive Approach가 있다. 각 Defensive Approach는 팀의 라인 높이와 직접 연결되며, 라인 높이는 특정 값들 사이에서 수동 조정할 수 있다.」)

| 접근 | 라인 구간 (기본값) | Run Tracking | Pressure |
|---|---|---|---|
| Deep | 1–30 (25) | 상대 전진 시 라인이 내려앉음 | 없음 |
| Balanced | 31–60 (50) | 유연 추적 | 없음 |
| High | 61–90 (70) | 거의 추적 안 함 | 최소 |
| Aggressive | 91–100 (95) | **절대 추적 안 함**, 최고 라인 유지 스텝업 | **헤비터치 시 압박** + 오프사이드 트랩 + **추가 스태미나 소모** |

(전부 A, FC25, https://www.ea.com/en/games/ea-sports-fc/fc-25/news/pitch-notes-fc-25-fc-iq-deep-dive · 독일어판 동일 확인 https://www.ea.com/de-de/games/ea-sports-fc/fc-25/news/pitch-notes-fc-25-fc-iq-deep-dive)

**⇒ 「높은 라인 + 침투 추적」이나 「낮은 라인 + 즉시 압박」 같은 조합은 선택할 수 없다**(A, FC25).

⛔ **번역 오류 정정 — DB·리포트 전수 점검 필요**: Aggressive의 압박 발동 조건은 「immediately after losing possession」, 즉 **「소유권 상실 직후」(턴오버 직후 카운터프레스)**이지 **「실점 직후」가 아니다**(A, FC25). 기존 문서에 「실점 직후」로 적혀 있으면 전부 고칠 것.

⚠️ **이 표는 FC25 문서이며 EA가 FC27에서 재확인한 적이 없다**(C, FC27 — fifauteam FC27 가이드 https://fifauteam.com/fc-27-tactics/ 가 동일 수치를 싣고 있으나 게임 내 UI 직독 수준이다). **게임 내 전술 화면 실측으로만 확정된다.**

### 5.3 빌드업 스타일 — 패스 길이가 아니라 "전환 시간 + 비볼선수 방향"

「The Build-Up Style also determines the base time it takes to transition from the defensive to the attacking phase (the Role Familiarity further impacts that). … Short Passing: Players will come short to support the ball carrier rather than make forward runs. This more cautious approach allows the team to maintain its defensive shape for longer during the transition. … Counter: This approach encourages players to get in behind the opposition's defense as the team transitions quickly from defense to attack.」(「빌드업 스타일은 수비 국면에서 공격 국면으로 전환하는 데 걸리는 기본 시간도 결정한다(Role Familiarity가 여기에 추가로 영향을 준다). … Short Passing: 선수들은 전진 런을 하는 대신 볼 캐리어를 지원하러 짧게 내려온다. 이 더 신중한 접근은 팀이 전환 중에도 수비 형태를 더 오래 유지하게 해준다. … Counter: 이 접근은 팀이 수비에서 공격으로 빠르게 전환할 때 선수들이 상대 수비 배후로 들어가도록 유도한다.」 / A, FC25, https://www.ea.com/en/games/ea-sports-fc/fc-25/news/pitch-notes-fc-25-fc-iq-deep-dive)

**⇒ 같은 빌드업 스타일이라도 스쿼드의 역할 숙련도에 따라 실제 전환 속도가 달라진다**(A, FC25). 이는 §4.2의 「숙련도가 낮을수록 전환에 오래 걸린다」와 정합한다.

### 5.4 Tactical Focus — 두 축이 묶여서 움직인다

「Selecting "Attacking" as your Tactical Focus will increase the Build-Up by 1 level and push up your Defensive Approach by 1 level. Example 1: You have a Balanced Build-Up and a Balanced Defensive Approach. After selecting your Tactical Focus as Attacking, your Build-Up will become Counter, and your Defensive Approach will change to High.」(「Tactical Focus로 "Attacking"을 선택하면 빌드업이 1단계 올라가고 Defensive Approach도 1단계 밀려 올라간다. 예시 1: Balanced 빌드업과 Balanced Defensive Approach를 쓰고 있다면, Tactical Focus를 Attacking으로 선택한 뒤 빌드업은 Counter가 되고 Defensive Approach는 High로 바뀐다.」 / A, FC25, https://www.ea.com/en/games/ea-sports-fc/fc-25/news/pitch-notes-fc-25-fc-iq-deep-dive)

**⇒ 인게임에서 두 축을 독립 조정할 수 없다**(A, FC25). 「공격은 직선적으로 바꾸되 라인은 그대로」 같은 조정은 **미리 저장해 둔 다른 커스텀 전술로 통째 교체(My Tactics)**해야만 가능하다.

### 5.5 ⭐ FC27의 실질 변화 — AI 수비가 빠진 자리

FC27에서 팀 전술 **파라미터 집합은 그대로인데 같은 설정값의 실효 거동이 바뀌었다**. 네 건이 EA 1차로 확인된다:

**(1) AI 수비 영향력 축소**(A, FC27): 「Nous réduisons l'influence de la défense contrôlée par l'IA, donnant plus de pouvoir à la défense manuelle … La défense de l'IA joue désormais un rôle plus de soutien grâce à son positionnement sur le terrain」(「우리는 AI가 제어하는 수비의 영향력을 줄이고 수동 수비에 더 큰 권한을 준다 … AI 수비는 이제 필드 위 포지셔닝을 통한 보조 역할을 더 많이 수행한다」 / https://www.ea.com/fr/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive). 개발자 직접 발언도 스페인어권에서 나왔다: 「Estamos haciendo que la defensa de la IA sea menos potente, pero potenciando la defensa manual. Es una forma de lograr un equilibrio a la hora de crear un nuevo juego.」(「우리는 AI 수비를 덜 강력하게 만들되, 수동 수비를 강화하고 있다. 새 게임을 만들 때 균형을 잡는 하나의 방식이다.」 / A, FC27, https://www.gamereactor.es/impresiones-con-ea-sports-fc-27-nuestra-preview-completa-tras-probarlo-en-persona-en-ea-vancouver-1760953/)

**⇒ 팀 전술의 수비 파라미터는 태클 결과가 아니라 '어디에 서 있는가'를 통해서만 작동하게 되고, 실제 볼 탈취는 조작 선수의 수동 판정으로 옮겨간다. 역할·포커스 배치 실수의 비용이 FC26보다 커진다.**

**(2) Team Press 하드 임계값**(A, FC27): 「Team Press is intended to be a way to apply pressure higher up the pitch, but we found it was also too effective when used close to your own goal. … To address this, Team Press will now have no effect while the ball is in your defensive third.」(「Team Press는 피치 상단에서 압박을 가하는 수단으로 의도된 것이지만, 자기 골문 가까이에서 쓸 때도 지나치게 효과적이라는 점을 발견했다. … 이를 해결하기 위해, 볼이 당신의 수비 3분의 1 구역에 있는 동안 Team Press는 이제 아무 효과도 내지 않는다.」 / https://www.ea.com/games/ea-sports-fc/fc-27/news/fc-27-closed-beta-feedback-update)

**⇒ 저블록 상태에서 AI 팀메이트에게 압박을 시키는 것이 구조적으로 불가능해졌다. 시메오네형 「저블록 후 선택적 압박」은 FC27에서 재현 불가다**(A, FC27).

**(3) 압박의 실효 주체는 중원·전방**(A, FC27): 「When Team Press is used further up the pitch, defenders can still step towards their marked players, but will be less effective at applying pressure than midfielders and forwards. This also comes with a trade-off: as defenders move closer to their marked players, they can become more susceptible to passes played in behind the defensive line.」(「Team Press를 피치 더 위쪽에서 사용하면 수비수들도 여전히 자신이 마크하는 선수 쪽으로 스텝업할 수 있지만, 미드필더·공격수보다 압박을 가하는 데 덜 효과적이다. 여기엔 트레이드오프도 따른다: 수비수가 마크 대상에게 가까이 붙을수록 수비 라인 배후로 넘어오는 패스에 더 취약해질 수 있다.」)

**(4) 낮은 뎁스가 더 확실히 반영됨**(A, FC27): 「We've made adjustments so that lower depth settings are more clearly reflected in how your defensive line positions itself, with defenders retreating sooner and maintaining a more conservative position to leave less space in behind. Your defensive line will still adjust to what's happening on the pitch, so setting a low depth doesn't mean your defenders will stay deep in every situation.」(「낮은 뎁스 설정이 수비 라인의 위치 잡기에 더 분명히 반영되도록 조정했으며, 수비수들이 더 일찍 물러나고 더 보수적인 위치를 유지해 배후 공간을 덜 남기게 된다. 수비 라인은 여전히 피치 위 상황에 따라 조정되므로, 낮은 뎁스를 설정했다고 해서 모든 상황에서 수비수들이 깊게 머무르는 것은 아니다.」) — **마지막 문장이 저블록 재현의 상한**이다.

**(5) 보조 압박(Secondary Contain) 거리 증가**(A, FC27): 「Wenn ihr das Sekundäre Zustellen einsetzt, deckt das KI-Teammitglied den ballführenden Profi aus einer etwas größeren Entfernung als bisher. Wenn ihr effektiveren Druck auf den dribbelnden Profi ausüben wollt, müsst ihr zum Abwehrprofi wechseln und manuell verteidigen.」(「보조 압박을 쓰면 AI 팀 동료가 볼 소유자를 이전보다 다소 먼 거리에서 커버한다. 드리블하는 선수에게 더 효과적인 압박을 가하려면, 그 수비수로 전환해 직접 수동으로 수비해야 한다.」 / https://www.ea.com/de-de/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive)

**⇒ 전체 종합**: FC27에서 **팀 전술로 만들 수 있는 것은 "위치"뿐이고, "탈취"는 전부 유저 조작으로 넘어갔다**(A, FC27). FC26 처방을 FC27로 옮길 때 전술 코드는 재사용하더라도 **라인 높이·프레스 계열은 재실측이 필수**다.

### 5.6 용어 표기 주의

EA 1차 자료는 「line height」가 아니라 **「Defensive Depth」**라는 용어를 쓴다(A, FC27). DB 라벨 정본을 정할 때 이 표기 차이를 기록해 둘 것.

---

## 6. 임계값·구간 — 선형인가 계단형인가

### 6.1 확실한 계단형 — EA가 자인한 2건 (스탯 축)

**(1) 스탠드 태클**(A, FC26): 「Players with a low stand tackle attribute (below 71) can only perform basic stand tackle animations. Players with a medium stand tackle attribute (71-84) can perform most stand tackle animations. Players with a high stand tackle attribute (85+) can perform all stand tackle animations.」(「스탠드 태클 스탯이 낮은(71 미만) 선수는 기본 스탠드 태클 애니메이션만 수행할 수 있다. 중간인(71~84) 선수는 대부분의 스탠드 태클 애니메이션을 수행할 수 있다. 높은(85 이상) 선수는 모든 스탠드 태클 애니메이션을 수행할 수 있다.」 / https://www.ea.com/en/games/ea-sports-fc/fc-26/news/pitch-notes-fc26-gameplay-deep-dive)

**⇒ 71과 84는 게이팅상 동일하고, 70→71에서 불연속 점프가 발생한다**(A, FC26). **EA가 스탯의 계단형을 자인한 사실상 유일한 사례**다.

**(2) AcceleRATE**(A, FC26): 「Explosive: Agility minimum 65, (Agility - Strength) >= 10, Acceleration minimum 80. … Lengthy: Strength minimum 65, (Strength - Agility) >= 4, Acceleration minimum 40.」 포르투갈어판이 세 번째 유형까지 명시한다: 「Controlada: qualquer atleta que não atenda aos outros dois requisitos.」(「제어형: 나머지 두 조건을 충족하지 못하는 모든 선수.」 / https://www.ea.com/pt-br/games/ea-sports-fc/fc-26/news/pitch-notes-fc26-gameplay-deep-dive). FC26 Title Update 1.4.0에서 Lengthy 신장 조건 185cm/165cm이 기술됐다(A, FC26).

**⇒ 순수 계단형 + 스탯 차이 조건 + 키 상한. 컷을 1이라도 못 넘기면 유형이 통째로 바뀐다**(A, FC26).

FC27 변경(A, FC27): 「We've slightly reduced the impact of AcceleRATE profiles on a player's running performance, bringing Explosive, Controlled, and Lengthy players a little closer together. This places greater emphasis on a player's Acceleration and Sprint Speed Attributes.」(「AcceleRATE 프로파일이 주행 성능에 미치는 영향을 소폭 줄여 Explosive·Controlled·Lengthy를 서로 조금 더 가깝게 만들었다. 이로써 선수의 Acceleration·Sprint Speed 속성 비중이 더 커진다.」) + 여자 선수 Lengthy 신설 임계 「female players will need to be at least 5'8" (172 cm) to be eligible for Lengthy」(「여자 선수는 Lengthy 자격을 얻으려면 최소 172cm여야 한다」 / https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-gameplay-deep-dive). **계단 구조는 유지되되 계단의 높이가 낮아졌다.**

### 6.2 확실한 계단형 — 전술 축 2건

- **라인 높이 4구간**: Deep 1–30 / Balanced 31–60 / High 61–90 / Aggressive 91–100, 구간이 바뀌면 Run Tracking·Pressure·오프사이드 트랩이 함께 바뀐다(A, FC25 · **FC27 미확인**).
- **Team Press 수비 서드 무효화**: 볼 위치 기반 하드 임계값(A, FC27).

### 6.3 ⛔ 그 외 일반 스탯의 계단 여부 — **1차 근거 전무**

「반응력 80과 90 사이에 체감 계단이 있다」「85 넘으면 다르다」류 주장에 대한 **EA 1차 근거는 존재하지 않는다**(A, FC25~FC27 — 부재 증거). 5개 언어권 전부에서 스탯 응답곡선을 역공학한 **B등급 자료 0건**, 통제 실측 **C등급 0건**이다. 스페인어권 정리본은 스스로 「los umbrales no están verificados para FC 26; EA nunca los ha publicado」(「FC26용 임계값은 검증되지 않았다; EA가 공개한 적이 없다」 / D)라고 못박고 있다.

또한 커뮤니티가 유통하는 스탯 가중치 공식 — 「DRI = Agility 25% + Balance 25% + Reactions 15% + Ball Control 20% + Composure 10% + Dribbling 5%」 — 는 **1차 근거가 없고 출처마다 서로 모순**된다(FC25판은 Reactions 0%·Ball Control 35%·Dribbling 50%로 완전히 다름). **인용 금지**(D).

**⇒ 현재 답할 수 있는 것은 "최소한 일부 영역에서 명백히 계단형이다"까지이며, "일반 법칙"은 확인 불가다.**

### 6.4 ⭐⭐ 부수 발견 — 우리 코드가 EA 구간을 위반하고 있다 (반증 작업 중 확인, 이번 세션 실측 재확인)

`/Users/user/Documents/tactics/core/team_settings.py`의 수비 접근 매핑이 EA 구간을 벗어난다:

```
out.update(defensive_approach="High",     line_lo=62, line_hi=72)
out.update(defensive_approach="Balanced", line_lo=55, line_hi=62)   # EA 상한 60 초과
out.update(defensive_approach="Balanced", line_lo=48, line_hi=58)
out.update(defensive_approach="Deep",     line_lo=0,  line_hi=45)   # EA 상한 30 초과
```

`db/tactics.db`의 `match_game_setups` 실적재 현황(이번 세션 직접 조회):

| defensive_approach | 행 수 | line_height 최소 | 최대 | EA 구간(FC25) | 판정 |
|---|---|---|---|---|---|
| Deep | 4 | 35 | 40 | 1–30 | ⛔ 전량 구간 초과 |
| Balanced | 24 | 48 | **62** | 31–60 | ⛔ 상단 2 초과 |
| High | 6 | 62 | 72 | 61–90 | ✅ 적합 |

`docs/20` line 567의 매핑표도 같은 값이라 **문서·코드·DB가 함께 어긋나 있다**. Deep을 선택하면 게임 내 슬라이더가 30에서 멈출 가능성이 있어, **적재된 Deep 35~40 조합은 게임에서 선택 자체가 불가능할 수 있다.**

**조치 순서**: ① FC27 게임 내 전술 화면에서 슬라이더 상하한 실측 → ② `team_settings.py` 임계값을 30/60/90 경계로 재정렬 → ③ 기존 행은 **불변규칙 2에 따라 덮지 말고 새 행으로 추가 정정** → ④ `game_tactic_params`에 FC27 행으로 구간값 기록.

---

## 7. FC26 → FC27 변경분

### 7.1 EA 1차로 확정된 변경

| 축 | 변경 | 등급 |
|---|---|---|
| AI 수비 | 자동 태클 제거, 인터셉트 리치 축소, 수동 조작 수비수 리치 > AI 리치. **Competitive 전용** | A |
| AI 수비 | 보조 압박(Secondary Contain)이 더 먼 거리에서 커버 | A |
| Team Press | 자기 수비 서드에서 **효과 0** | A |
| Team Press | 수비수는 미드필더·공격수보다 압박 효율 낮음 + 배후 패스 취약 트레이드오프 | A |
| Defensive Depth | 낮은 설정이 라인 위치에 더 뚜렷이 반영, 조기 후퇴 | A |
| 신규 기능 | **Off-Balance Dribbling** — Balance·Agility·Dribbling 구동. PS5/XSX\|S/PC/Switch2 전용 | A |
| 신규 기능 | **Attacking Spatial Awareness** — 공간 인지 기반 곡선 런, Role을 대체하지 않고 병행 | A |
| AcceleRATE | 프로파일 영향력 소폭 축소, Acceleration·Sprint Speed 비중 증가. 여자 Lengthy 172cm 신설 | A |
| PlayStyles | **10종 변경**(Finesse Shot, Technical Dribbler, Intercept, Rapid, Quick Step, Pinged Pass, Tiki Taka, Jockey, Precision Header, Low Driven) + Bruiser+ 소폭 축소. **신규 0종** | A |
| PlayStyles | Pinged Pass·Tiki Taka의 **수신자 트랩 오차 감소 효과 삭제** | A |
| PlayStyles | Low Driven 슛 속도 부스트 삭제(정확도만 잔존), Rapid/Quick Step 속도 부스트 축소 | A |
| PlayStyles | **First Touch는 변경 목록에 없음**(= EA 기준 미변경) | A |
| FUT | 아이템당 **PlayStyle+ 5개 → 3개**, 스탯 상승 폭도 축소 | A |
| FUT | 연중 출시 **모든 스페셜 아이템에 주·부 포지션 전 역할 Role++** 일괄 부여 | A |
| 타이틀 업데이트 | **FC27 넘버링 TU 0건**(2026-09-21 현재). 초기 TU에서 유의미한 밸런스 변경 계획 없음 명시 | A |

### 7.2 전술 파라미터는 "그대로"인가

**미확정이다.** 2차 출처는 「The code includes the Formation, Build-Up Style, Defensive Approach, Line Height, and the eleven assigned Roles and Focuses, but it does not include the tactic name. … FC 26 tactics codes are compatible with FC 27 and will be converted to the FC27 format when applied.」(「이 코드에는 포메이션, 빌드업 스타일, 수비 접근, 라인 높이, 그리고 배정된 11개의 Role과 Focus가 포함되지만 전술 이름은 포함되지 않는다. … FC 26 전술 코드는 FC 27과 호환되며 적용 시 FC27 포맷으로 변환된다.」 / C, FC27, https://fifauteam.com/fc-27-tactics/)라고 쓰지만, 반증 검증에서 **2/2 기각**됐다(§8 참조). 확인된 정정: 전술 코드는 11자리가 아니라 **12자**이고, FC26도 12자였다. 그리고 **파라미터 집합이 그대로여도 §5.5의 변경들 때문에 같은 설정값의 실효 거동은 바뀐다.**

우리 쪽 실측으로 말할 수 있는 것은 FC27 `fut_tactics` 행에 build_up_style / defensive_approach / line_height만 존재한다는 것까지다(C, FC27). **29 포메이션·수비 접근 4단·Role 추가 여부는 FC27 기준으로 아무도 1차 검증하지 않았다** — docs/21의 규약대로 **「없다로 읽지 말 것 — 미공개다」**를 적용한다.

---

## 8. ⛔ 기각된 통설 — 리포트 본문에 사실로 쓰지 말 것

### 8.1 「침착 = 압박 인지 반경」 (2/2 반증)

원 주장(D, https://fifauteam.com/fc-26-attributes/ · https://es.fifauteam.com/atributos-en-fifa-21/): 「This attribute determines at what distance the player with the ball starts feeling pressure from the opponent. … Dribbling has no connection with the ball receiving factor; that only has to do with ball control.」(「이 스탯은 공을 가진 선수가 상대의 압박을 느끼기 시작하는 거리를 결정한다. … 드리블은 볼 수신 요소와 아무 연관이 없다. 그것은 오직 볼컨트롤에만 달려 있다.」)

기각 사유:
- **「수신 = 볼컨트롤 전유」가 EA 1차와 정면 충돌한다**(A, FC26) — 퍼스트 터치는 볼컨트롤·인터셉트·침착 + 상황 6변수의 연속 모델이다.
- **「거리 파라미터」 정의는 EA 1차 자료에 없다.** EA 공개 자료로 확언 가능한 Composure의 작용은 ① 페널티 Composure Ring 수축 속도·퍼펙트 타이밍 창(A, FC25) ② FC26 퍼스트 터치 난이도 입력값(A, FC26) 두 가지뿐이다. FC26 서술에서 **'opponent pressure'는 Composure와 별개의 독립 입력**으로 나란히 나열된다.
- **출처 계보**: "영어권 표준"이 아니라 **FIFA19(2018) 이후 FIFAUTeam 단일 계보의 문장이 무수정 복제**된 것이며, 스페인어판·독일어권 용어집·프랑스어 포럼 전부 같은 계보의 번역·재서술이다. **다국어 교차검증으로 카운트 불가.**
- 근거로 제시되는 것은 **공개되지 않은 EA data-reviewer 문서**다. 설령 실재하더라도 그것은 실제 선수를 평가하는 **스카우트용 의미 규정이지 게임 엔진의 계산 방식이 아니다.**

**⇒ 사용 지침: 「엔진 메커닉 근거로 사용 금지, 페널티 링에 한해서만 인용 가능」.** 침착은 「압박 하 액션 오차 계수」로 기록한다. 닫으려면 프랙티스 아레나 통제 실측(수비수 거리 계단 × 침착 고저 카드 × 패스/슛 오차 분포)이 필요하다.

### 8.2 「반응력은 조작 중인 선수에게도 적용된다」 (2/2 반증)

원 주장(D, https://es.fifauteam.com/atributos-en-fifa-21/): 통설 부정 + 「인터셉트는 AI 쪽에 더 강하게 적용된다」.

기각 사유: 측정 근거 0건. **영어 원문과 스페인어 번역판이 동일 출처**라 다국어 교차검증에 해당하지 않는다. FIFA16~FC26까지 재검증 없이 복제. FC27 Pitch Notes에서 인터셉트는 AI/유저 축이 아니라 **PlayStyle 보유 여부 축**으로 기술된다(A, FC27).

**⇒ 「반응력 AI 전용」도 「반응력 양쪽 적용」도 모두 근거가 없다.** 프랙티스 아레나 A/B 실측(리바운드 상황 볼 획득률·첫 터치 성공률)이 필요하다.

### 8.3 「Rol+는 패스 레인을 0.5초 먼저 인식한다」 (2/2 반증)

원 주장(D, FC26, https://tacticasfc.com/fc26/fc26-roles): 「Un jugador con Rol+ identifica los carriles de pase medio segundo antes que los demás.」(「Rol+ 선수는 다른 선수들보다 패스 레인을 0.5초 먼저 인식한다.」)

기각 사유:
- **0.5초는 인용된 원문에도 없는 창작 수치**다.
- 「정도에 1차 근거 없음」이라는 서술 자체가 틀렸다 — EA는 **10~40%**라는 정량 수치를 공개했다(A, FC25). 없는 것은 **시간 단위 표현**뿐이다.
- 「스탯 보정이 아니다」는 **표시 스탯이 오르지 않는다**는 의미로만 참이고, 내부 계산에서는 스탯과 동일한 수치 채널에 들어간다.
- 「방향은 스페인어권 합의」도 틀렸다 — 이는 EA FC25 1차 사양이고 스페인어 가이드는 그 **파생 요약**이다. 독립 관측이 아니므로 근거로 세면 안 된다.
- FC26에서 Role/Role+가 Role++에 근접하도록 상향되고 포지션 이탈 페널티가 축소됐으므로(A, FC26), **「Rol+는 먼저 보고 Rol++만 위험 전에 커버한다」류 큰 격차 서술은 FC26 1차 자료 방향과 충돌한다.**

### 8.4 「FC27 역할 카탈로그 = FC26과 완전 동일」 (2/2 반증)

원 주장(B 자칭, FC27, https://www.fut.gg/roles/): 역할 30종·역할×포지션 49·역할×포커스 72쌍 완전 일치, 커널 217/217 일치 → FC27 신설·삭제·개명 0건.

기각 사유(실측 근거):
- **엔드포인트에 버전 인자가 없다.** `?game=26`과 `?game=27` 응답이 **md5 동일**(bd4280cb715b26c6c68fc9b9a9c5c5e8, 354,999B)이고 페이로드 어디에도 game·version 필드가 없다 — 「FC 27」은 **HTML 페이지 문구일 뿐 데이터 provenance가 아니다.**
- **응답 헤더 `last-modified: 2026-09-17 14:36 GMT` · `cf-cache-status: HIT` · age≈3.7일** — **얼리액세스(09-18) 이전에 고정된 캐시 문서**다.
- 2026-07-31 수집분의 역할 id 155/159/162가 현재 응답에 없고 id 공간이 298~442로 전면 교체됐는데 **오염(CAM Playmaker=id 413 안의 Winger 2항목)까지 그대로 복제**돼 있다 — 새 EA 추출이 아니라 **같은 카탈로그의 재적재 흔적**이다.
- **소스 내부도 불일치**: fut.gg `/roles/` 본문은 「There are currently 31 Roles」라고 쓰는데 자기 API의 distinct 역할명은 30이다.
- 대조 자체도 우리 85행(role_id×focus)·217변형이 아니라 **이름축 72쌍으로 뭉개 수행**돼, 커널이 갈리는 13행과 좌우·포지션 분기 147항목이 검증되지 않았다.

**⇒ 등급 B → UNKNOWN(미확정).** FC27 커널·역할 행 적재는 **발매 09-25 이후 게임 내/EA 확정 데이터로만** 하고, 그전까지 「37/85/217 유지」는 **「미공개」**로 남긴다. `EXPECTED["FC27"]`·게이트 앵커 추가는 보류.

### 8.5 「포커스보다 역할이 2배 이상 움직인다」 (2/2 반증)

원 주장(B 자칭, FC27, https://www.fut.gg/roles/): 포커스 간 중앙값 0.40칸 vs 역할 간 중앙값 0.85칸, 풀백 2.02칸.

기각 사유:
- **수치 출처가 FC27이 아니라 우리 저장소의 FC26 카탈로그다.** `db/tactics.db`의 `game_role_focus`(game_version=FC26, 85행·37역할, 2026-07-31 수집)와 `archive/v1/fc26-heatmap.html`의 MAPS에서 **포커스 최대 1.00칸(wm_widemid Defend 2.50 ↔ Build-Up 1.50)·풀백 2.02칸(fullback 3.57 ↔ inverted 1.55)이 소수점까지 그대로 재현**된다.
- **핵심 통계가 재현되지 않는다.** 「45개 역할」은 카탈로그와 불일치(37역할/포커스 2개 이상 33개/조합 85개). 역할 간 중앙값 0.85는 **어떤 자연스러운 정의로도 나오지 않는다**(동일 포지션 역할쌍 y중앙값 0.50, 2D 0.59, 포커스 단위 교차쌍 0.46, 최근접 역할 0.15). 재현값은 0.50/0.375 = **1.33배**다. 재계산자 중 하나는 1.16배(방식별 1.1~1.45배)를 얻었다.
- **서로 다른 통계를 비교했다** — 포커스는 역할 내 *범위(max−min)*, 역할은 포커스 *평균 간 차이*.
- **의사결정 규칙이 같은 데이터에서 깨진다**: 동일 포지션 역할쌍 60개 중 **21개(35%)가 포커스 중앙값보다 적게 움직이고, 51개(85%)가 최대 포커스 스윙보다 적게 움직인다.** 반례 — LB Attacking Wingback ↔ Inverted Wingback 0.04칸, CDM Holding ↔ Wide Half 0.02칸, CB BPD ↔ Stopper 0.02칸, ST Poacher ↔ Target 0.01칸. 반대로 LM Wide Midfielder는 **역할을 유지한 채 포커스만 바꿔 1.00칸**을 움직인다.
- **좌우 결론은 그림의 대칭성을 잰 것**이다 — CAM Classic 10의 Attack/Versatile/**Wide** 세 포커스는 질량중심이 (1.0, 2.0)으로 **완전히 동일**하고, ST Target Forward의 Attack ↔ Wide는 질량중심 이동 0.00칸인데 코사인 거리 0.51로 카탈로그 전체에서 형태 차이가 가장 크다.
- **해상도 바닥 효과**: 1칸 ≈ 21m 격자에서 EA가 라인 변경으로 서술한 포커스도 소수점으로 뭉갠다 — CDM Wide Half는 「When set to Build-Up, the Wide Half can move into the Wingback position, and forward into Wide Midfielder territory」(「빌드업에서는 윙백 위치로, 더 나아가 와이드 미드필더 영역까지 전진한다」) ↔ 「When instructed to Defend, the Wide Half can drop into Fullback and Wingback positions」(「수비 지시에서는 풀백·윙백 위치까지 내려간다」)인데 질량중심 차이는 2.80 → 3.20, **겨우 0.40칸**이다.
- fut.gg 격자는 EA 데이터가 아니라 **fut.gg 자체 인코딩({0,30,100} 또는 0/0.3/0.6/1.0 4단계)**이며, role eaId는 null이다.

**⇒ 안전하게 말할 수 있는 범위**: 「FC26 fut.gg 카탈로그 히트맵(5×5·4단계)의 전후 질량중심으로 보면, 포커스 변경의 중앙값 이동(0.375칸)은 동일 포지션 역할 변경의 중앙값(0.50칸)보다 작다. 다만 차이는 1.3배 수준이고, 역할쌍의 35%는 포커스보다도 덜 움직이며, 좌우 성분과 형태 변화는 이 지표로 측정되지 않는다. **미터 환산·경기 중 평균 위치·FC27 적용은 근거가 없다.**」 등급 **B → D**.

**진짜 결론은 「역할이 포커스보다 크다」가 아니라 「포지션마다 다르다」**다 — 풀백(역할 간 중앙값 1.01칸)·CDM(0.60)·LM/RM(0.63)에서만 역할 교체가 지렛대이고, CM(0.42)·CAM(0.37)·ST(0.33)·CB(0.28)·RW(0.20)·LW(0.15)에서는 역할을 바꿔도 포커스와 비슷하거나 덜 움직인다.

재현 스크립트 기준 파일: `/Users/user/Documents/tactics/db/tactics.db`(game_role_focus), `/Users/user/Documents/tactics/archive/v1/fc26-heatmap.html`(MAPS 블록).

### 8.6 「FC27 팀 전술 파라미터 미개편 + FC26 코드 그대로 적용」 (2/2 반증)

기각 사유: ① 전술 코드는 11자리가 아니라 **12자**이고 FC26도 12자였다(출처의 "11-digit"은 FC26 페이지 복사 오류). ② 원문 표현도 「그대로 적용」이 아니라 **「변환 적용」**이다. ③ 29 포메이션·수비 접근 4단·Role 추가는 **FC27 기준 아무도 1차 검증하지 않았다** — 우리 쪽도 FC27 `game_roles` 커널 0행(obs#629)이라 「불변」은 확인이 아니라 **미확정**이다. ④ **파라미터 집합이 그대로여도 §5.5로 실효 거동은 바뀐다.** ⑤ in-match Smart Tactics는 FC26에도 있던 기능이라 FC27 변화 근거로 쓸 수 없다. **등급 C → D.**

### 8.7 「극단 수비 밴드는 사어(死語)라 딥블록·고압박 재현이 검증 불가」 (2/2 반증)

원 주장(C 자칭, FC27, https://www.fut.gg/tactics/4-2-1-3/): 4-2-1-3 기준 Deep 1%·Aggressive 1%, 라인 중앙값 60.

**숫자 인용 자체는 2026-09-21 재확인 결과 페이지 그대로**이나 **해석이 전부 틀렸다**:
- **60은 중앙값이 아니라** 그 포메이션의 **최빈(추천) 전술 1건의 라인 높이**다 — fut.gg는 라인 높이 분포를 제공하지 않으므로 중앙값을 말할 수 없다. 커뮤니티·프로 항목이 동일 shareCode를 가리킨다.
- **프로 표본이 무의미하다** — 전 포메이션 합계 97스쿼드라 4-2-1-3 프로 n≈16. 「프로 75%」·「Deep 0%」는 통계적 의미가 없다.
- **밴드 폭이 비대칭이다** — Aggressive는 슬라이더의 10%뿐이라 **균등분포에서도 최소가 된다.** %는 '수비 스타일 선호도'가 아니라 슬라이더 구간 라벨 점유율이다.
- **4-2-1-3은 공격형 포메이션이라 딥블록 사용자가 애초에 선택하지 않는 조건부 표본**이다 — 시메오네 축은 5-4-1·4-4-2 계열에서 봐야 한다. 실제로 5-4-1은 Deep 6%·Aggressive 3%, 5-2-1-2는 Deep 3%·Aggressive 4%로 **수 배로 뛴다**. 커뮤니티 1%도 49,676 스쿼드 풀 기준이라 절대량은 수백 단위다.
- **⭐ 범주 오류가 핵심이다** — **시메오네형 딥블록의 게임 내 정본 구현은 'Deep 밴드'가 아니라 'Balanced + 라인 31~45 + Team Press 미사용'**이고, 이는 이미 54%의 다수 밴드 안에 들어간다. **에메리형 고압박도 Aggressive(91–100)가 아니라 High(61~70) + 국면별 Team Press**로 근사하는 것이 맞다. 실축 딥블록/압박을 EA의 Deep·Aggressive 밴드에 1:1 대응시킨 것이 오류다.
- 중앙값 60은 Balanced 상한(60)이자 High 하한(61) 바로 아래라 **경계에서 절단된(censored) 분포**를 뜻한다 — 54/44 스플릿은 60↔61 경계를 사이에 둔 **사실상 고라인 메타**로 읽어야 한다.
- 시점도 **FC27 정식 발매 이전 얼리액세스 표본**이고 FC26 코드가 변환 계승되므로 FC27 안정 메타로 고정 인용 금지.

**⇒ 유효하게 남는 경고는 「Aggressive는 라인 강제 범위(91–100)가 좁아 실축 라인과 어긋난다」까지**이며, **「극단 밴드가 사어라서 재현 검증 불가」는 성립하지 않는다.** 등급 **C → D.**

### 8.8 「fifauteam FC27 역할 페이지의 신규 역할·신규 Versatile 포커스」 (B, 사용 금지)

「In FC 27, Player Roles offer greater flexibility. Thanks to the new Versatile Focus options and fewer restrictions, players are no longer confined to strict role limitations.」(「FC 27에서 플레이어 역할은 더 큰 유연성을 제공한다. 새로운 Versatile 포커스 옵션과 줄어든 제약 덕분에, 선수들은 더 이상 엄격한 역할 제한에 갇히지 않는다.」 / B, https://fifauteam.com/fc-27-roles/)

**FC27 변화 근거로 쓰면 안 된다** — 이 페이지가 'FC26 대비 FC27 신규 4종'으로 적는 Wide Back·Inverted Wingback·Box Crasher·Ball-Playing Keeper는 **우리 DB의 FC26 적재분(2026-07-31)에 이미 전부 존재하는 FC26 신규 역할**이다. 「새로운 Versatile 포커스」도 FC26 서술의 이월이다(Versatile은 FC26 Classic 10·Fullback·Advanced Forward·Winger·Poacher에 이미 있었다).

---

## 9. 여전히 미해결 — 무엇을 못 찾았고 왜인가

### 9.1 구조적 원인 — 시점

**8개 에이전트 전원이 C등급(통제 실측) 0건, B등급(데이터마이닝) 0건을 보고했다.** FC27은 얼리액세스 09-18, 정식 출시 09-25이고 조사일은 09-21이다. **검색 실패가 아니라 데이터가 축적될 시간이 없었던 것**이다. → **출시 2~4주 후(2026-10-09 ~ 10-23) 재수집이 필수**이며, 그때까지 FC27에 대한 모든 정량 결론은 잠정이다.

### 9.2 축별 공백 목록

**축1 — 스탯 작용**
- **Reactions의 1차 정의**: 5개 언어권 전부 없음. EA 자료 전수 스캔에서 0회. 세컨볼 경합·루즈볼 반응 개시·애니메이션 전환의 스탯 귀속 불명.
- **조작 선수 vs AI 팀메이트의 스탯 차등**: EA의 명시적 진술은 **수비 리치 한 건뿐**(A, FC27, Competitive 전용). 반응력·볼컨트롤 축의 차등은 **어느 언어권에서도 찾지 못함**.
- **드리블 vs 볼컨트롤의 역할 분담**: EA는 Off-Balance Dribbling에서 Balance·Agility·Dribbling을 명시했을 뿐(A, FC27), 두 스탯의 일반 분담을 실측으로 가른 자료 **없음**.
- **침착의 FC26/FC27 수치적 동작**(임계거리 존재 여부·크기): EA 자료로도 통제 실측으로도 확인 불가.

**축2 — PlayStyles**
- ⭐ **First Touch PlayStyle이 볼컨트롤 원값의 한계효용을 얼마나 덮는가 — 5개 언어권 전부 찾지 못함.** 이번 조사의 최대 공백.
- **PlayStyle과 원 스탯의 결합 방식(곱셈/임계값/독립 판정)**: EA가 한 번도 명시한 적 없음. §3.2는 변경 서술 방식으로부터의 **추론**임을 반드시 구분해 읽을 것.

**축3 — 역할·포커스**
- ⭐ **포커스·역할별 실제 위치 이동량의 경기 중 추적 실측 — 0건**(영·독·일·서어 웹 검색 범위. YouTube·Reddit·Discord 미탐색).
- **Role+/++가 구체적으로 어떤 행동 옵션을 추가로 해금하는지의 목록**: EA는 「more options and improved behaviors」(「더 많은 선택지와 개선된 행동」)라고만 적고 목록을 공개한 적 없음.
- **포커스별 이동 거리의 미터 단위 EA 수치**: 존재하지 않음. 5×5 격자 → 105m×68m 환산은 전부 추정.
- **FC27 역할 카탈로그의 실체**(31 vs 30 결손 포함): 미확정. 발매 후 인게임 역할 선택 화면 전수 실측 + FC27 아이템 정의의 rolesPlus/rolesPlusPlus 공개 후 재수집 필요.
- **EA가 "조작 중인 선수에게 역할이 작동하지 않는다"고 명시한 1차 문장**: 찾지 못함(함의될 뿐).

**축4 — 팀 전술**
- **한 축을 바꾸면 "어느 선수의 무엇이 달라지는가"를 선수 단위로 명시한 EA 문서 없음.** 가장 근접한 것이 FC27 Team Press의 포지션 계층별 차등(§5.5-(3))까지.
- **같은 스쿼드·같은 역할로 라인 높이만 바꿔 프레임 비교한 A/B 테스트 0건**(FC26·FC27 양쪽). 가이드 사이트의 권장값(라인 60~70, 폭 50~55)은 전부 근거 없는 체감(D).
- **밴드 내부 수치가 의미 있는지**(예: High 61 vs 90): EA는 밴드별 Run Tracking/Pressure만 문서화했고 밴드 내 연속 변화 설명이 없음.
- **B등급 자료 0건**: teamtactics/buildupplay 테이블 덤프, 라인 높이 수치 → 실제 좌표 매핑을 보여주는 파일 분석 없음. FIFA Editor Tool/Frosty 계열 커뮤니티의 팀 전술 스키마가 검색에 잡히지 않음.
- **FC27 전술 UI 개편 여부**: 개편됐다는 1차 근거를 찾지 못함.

**축5 — 임계값**
- **일반 스탯의 계단 여부에 대한 EA 1차 근거 전무.** 확보한 계단형 증거는 스탠드 태클·AcceleRATE(스탯 축) + 라인 높이 4구간·Team Press 서드 무효화(전술 축)가 전부.
- **FC27용 라인 높이 구간값 재확인 실패** — FC25 캐리오버 추정. 게임 내 슬라이더 실측으로만 확정.

### 9.3 방법론적 미수집

- **개발자 인터뷰·EA SPORTS FC Direct 영상 전사**: EA 1차 패스는 ea.com 발행물과 EA Help만 훑었다. Gilliard Lopes(Principal Gameplay Designer) 등의 외부 매체 인터뷰 전사는 **별도 패스 필요**. 단 스페인어권에서 gamereactor.es 현장 취재로 Sam Rivera / Gilliard Lopes / Jamey Cane 직접 인용 3건이 확보됐다.
- **접근 실패 소스**: EA 스페인어 공식 포럼 피치노트(403), forums.ea.com 프랑스어 허브(403), kicker.de/at(동의벽), psverso.com.br(410 Gone), eurogamer.de·kicker(WebFetch 403 — 브라우저 직독으로 일부 대체).
- **제외 소스**: moyens.net·itemd2r.com/fr·ldshop.gg/fr 등 프랑스어 표기 상업 블로그 다수가 기계번역 스팸에 가까워 인용에서 제외.
- **불변규칙 10(다국어) 적용 범위 판단**: 게임 시스템 1차 자료는 **영문 EA 원문이 유일 원천**이고 현지어판은 번역물이다. 그럼에도 5개 언어권을 훑은 것은 ① 로컬라이즈 용어 대응 확보(Ballannahme-Fehlerquote / erreur de contrôle / erro de domínio) ② 현지 전용 취재(gamereactor.es 개발자 인용) ③ 영어권 요약본이 누락한 세부 확인 때문이며, 실제로 독일어판에서만 「Vertrautheit 10–40%」 문구와 Stolper-Dribbling 발동 조건이, 스페인어권에서만 개발자 직접 발언이 나왔다. **다만 스탯 통설 축(§8.1~8.2)에서는 스페인어·독일어·프랑스어 자료가 전부 FIFAUTeam 단일 계보의 번역·재서술이어서 교차검증으로 기능하지 못했다** — 이 사실 자체가 중요한 발견이다.

### 9.4 다음 세션 우선순위 (제안)

1. **FC27 게임 내 전술 화면 실측** — 수비 접근별 라인 슬라이더 상하한(Deep이 30에서 멈추는가), 포메이션 수, 전술 코드 자릿수. → §6.4의 `core/team_settings.py` 위반 정정과 직결.
2. **FC27 역할 카탈로그 인게임 전수 수집**(발매 09-25 이후) — 31 vs 30 결손, role_id·좌우 변형 단위 대조. 그전까지 FC27 커널 행 적재 금지.
3. **프랙티스 아레나 통제 실측 3종 설계** — ① 볼컨트롤만 다른 카드의 트랩 오차(First Touch PlayStyle 유/무 교차) ② 침착만 다른 카드의 수비수 거리별 패스·슛 오차 분포 ③ 반응력만 다른 카드의 리바운드 볼 획득률. **버전·프리셋(Competitive/Authentic)·Role Familiarity 3개를 통제 변수로 고정.**
4. **역할·포커스 히트맵 실측** — 역할당 최소 5~10경기 누적 평균(ASA 때문에 단판 무효), 역할 고정·포커스만 변경한 대조군 별도 편성.
5. **2026-10-09~10-23 재수집** — C등급 커뮤니티 실측·B등급 데이터마이닝이 축적될 시점.

---

## 부록 — 완결성 비평(워크플로 Critic 단계 산출)

## 점검 ①~⑤ 응답 + 누락 지적

### A. 저장소 대조가 통째로 빠졌다 (가장 큰 결손)

리포트는 웹 8에이전트 패스만 하고 **우리 DB·코드·리포트 자산을 한 번도 조회하지 않았다.** 결과:

1. **`game_system_changes`의 FC27 21행(#10~#21)을 대조하지 않았다.** §7.1 "EA 1차 확정 변경" 표에서 이미 적재된 것들이 빠졌다 — #11 Triggered Runs **거리 제한(재트리거 필요)**, #15의 **조키 속도↑·수동 스탠딩 태클 범위↑**(리포트는 "AI 리치 축소"만 적고 수동 상향분을 뺐다), #16 **Dinked Pass 완전 수동 + Player Lock 자동 회피 제거·CPU 패스 오차↑**, #17 커리어(7포지션·**부포지션 OOP 페널티 0**·Dynamic OVR·성장 프로필 6·슬라이더 25+10·Authentic CPU 전술 다양화/접촉/파울↑).
2. **#21 = FC27 Launch Update 피치노트(2026-09-19 확인)가 이미 DB에 있다.** 리포트 §2.0의 「FC27 TU 0건 · 밸런스 정본 = Gameplay Deep Dive + Closed Beta Feedback 두 문서」는 이 문서를 놓친 결과다. 게다가 #21은 「All promo players will have Role++ for their **base** positions」인데 리포트 §4.4는 「**주·부 포지션 전 역할** Role++」로 범위가 더 넓다 — 두 서술의 충돌을 조정하지 않았다.
3. **`ingame_captures` 75행(FC26·커널 cosine 대조 포함)과 `scripts/ingame_heatmap_to_grid.py`, 미추적 `reports/ingame/2026-09-08-avl-test3|test4`, `2026-09-09-avl-sim1`, `2026-09-10-avl-test5` 4개 디렉터리**를 인벤토리하지 않았다. 「역할·포커스 통제 실측 0건」은 **외부 한정**인데 단서가 없고, §9.4-4는 이미 있는 파이프라인을 새로 설계하자고 한다. 이 75행의 한계(「조작 오염 — 커널 대조 근거로 쓰지 않음」)를 어떻게 넘을지가 진짜 설계 과제인데 언급 없다.
4. **§6.4의 코드 위반 판정이 층위를 섞었다.** `/Users/user/Documents/tactics/docs/20-fc-game-system.md` 558행 이하 매핑표는 **PPDA→라인 제안용 사전값**이고 「`team_match_stats.def_x_v`가 쌓이면 실측으로 보정한다」고 자기 문서에 명시돼 있다. EA의 *선택 가능 구간*과 같은 축에 놓고 「위반」이라 부를 수 없다. 또 `game_tactic_params` 9행에는 **구간 수치가 아예 없다**(전부 서술문) — 「문서·코드·DB가 함께 어긋나 있다」의 DB 근거는 실재하지 않는다.
5. **`fut_tactics.is_custom_def`를 보지 않았다.** 2026-09-20 싱크 행이 `is_custom_def=1, line_height=50`이다. 「Deep 35~40은 게임에서 선택 자체가 불가능할 수 있다」는 추정은 **커스텀 수비접근의 라인 자유도**를 확인하면 바로 갈리는데, 그 확인 없이 코드 정정을 지시한다.
6. **`fut_tactics`에는 `game_version` 컬럼이 없다.** §7.2의 「FC27 `fut_tactics` 행에 …만 존재한다(C, FC27)」는 버전 귀속 근거가 없는 진술이다.
7. **`fut_tactic_roles`(2026-09-20, 11행)에 `role_ea_id` 298~442 공간과 포커스명이 실제 계정 데이터로 들어와 있다.** §8.4가 fut.gg 캐시 응답을 UNKNOWN 처리한 것까지는 맞으나, **계정 측 라이브 데이터로 부분 대조**하는 경로를 검토하지 않았다.
8. `reproduction_limits`·`video_impl_claims`·`observations`(현 max 919) 어느 테이블도 언급되지 않는다.

### B. 축 자체가 통째로 빠졌다 (점검 ① 답)

리포트가 말하는 「빈약한 축」은 반응력·임계값이지만, **아예 스캔되지 않은 축**이 더 크다.

- **골키퍼 0건.** GK PlayStyles 카테고리(docs/22 §3 6카테고리 중 하나), GK 역할 5조합(`gk_goalkeeper`/`gk_sweeper`/`gk_ballplaying`), FC27 GK 변경 유무 — **부재 확인조차 없다.** 마르티네스·스즈키 처방이 이 축에 걸려 있다.
- **세트피스 0건.** FC25에서 Players in Box/Corners/Free Kicks 슬라이더가 삭제된 뒤 **무엇으로 대체됐는가**를 안 물었다. Composure Ring 한 줄이 전부.
- **스태미나·피지컬·부상 0건.** Aggressive의 추가 소모 한 줄뿐. 90분 동안 라인·압박이 유지되는가는 감독 재현의 핵심인데 FC27 접촉/파울 변경(#17)과 함께 빠졌다.
- **경기 중 운용 축**: 전술 5슬롯 전환·Smart Tactics·교체의 FC27 변경 여부 미조사(§8.6에서 「FC26에도 있던 기능」이라고 기각하고 끝냄).
- **CPU(상대) 거동**: 우리 실측은 CPU 상대 경기에서 나온다. #17의 「CPU 전술 다양화」는 히트맵 실측의 교란 요인인데 통제 변수 목록(버전·프리셋·Familiarity 3개)에 없다.
- **케미스트리·진화 원장**: PS+ 5→3 함의를 한 줄로 적었을 뿐 `fc_evolutions`/`player_evolutions`/`fc_chemistry_styles` 대조 없음.
- **PlayStyle 카탈로그 수 불일치**: §3.1은 「36종·6카테고리 유지」인데 `/Users/user/Documents/tactics/docs/22-fc-gameplay-mechanics.md` 53행은 FC26을 **35종**으로 적재한다. 35/36 미조정·출처 없음.

### C. 언어 커버리지 (점검 ⑤ 관련)

- **이탈리아어·일본어·네덜란드어 0건.** 불변규칙 10의 실증 사례(스즈키 3건)가 **일본어·이탈리아어에서만** 나왔다는 사실과 정면으로 어긋난다.
- **내부 모순**: §1은 EN/ES/DE/FR/PT 5개라 하고, §9.2 역할 축은 「영·독·**일**·서어 검색 범위」라고 적어 일본어를 훑은 것처럼 읽힌다.
- 「ES/DE/FR가 전부 FIFAUTeam 단일 계보였다」를 발견하고도, **그럼 어느 언어권이 독립 계보인가**(이탈리아·일본·폴란드·튀르키예)라는 후속 질문으로 이어지지 않았다.
- **영상·전사 축 0건.** `/Users/user/Documents/tactics/reports/transcripts/` 222개 파일과 전사 파이프라인이 이미 있는데 「YouTube·Reddit·Discord 미탐색」으로 끝냈다 — 도구가 없어서가 아니다. 미추적 `QkA0fScs5s8.en.md`·`U4OewDAQMCk.en.md`·`ofp0s7RaNoc.en.md`가 이 주제인지조차 확인 안 됨. 불변규칙 11의 auto-caption 조항은 적용 기회 자체가 없었다.
- 제외 사유 기록(불변규칙 10/DoD)이 이탈리아어·일본어·한국어에 대해 **없다**.

### D. 번역 누락 (점검 ③ 답 — 불변규칙 11 위반)

- §6.1 AcceleRATE 공식 원문 「Explosive: Agility minimum 65, (Agility − Strength) >= 10 …」 — 한국어 병기 없음.
- §3.3 「reduced error」 / 「minimal error」 — 병기 없음.
- §8.4 「There are currently 31 Roles」 — 병기 없음.
- §8.5의 fut.gg 인코딩 서술(`{0,30,100}`) 등 영문 조각 여럿 동일.

### E. 등급·버전 표기 (점검 ②④ 답)

- **부재에 (A)를 붙인다.** 「(A, FC27 — 부재 증거)」·「(A, FC25~FC27 — 부재 증거)」. A는 *1차 자료 원문* 등급인데 *검색 결과 없음*에 쓰면 등급 체계가 무너진다. 부재는 별도 기호가 필요하고, **탐색 범위·쿼리·수집일**을 함께 적지 않으면 재현·반증이 불가능하다(현재 쿼리 로그 0).
- **D의 정의가 둘로 갈려 있다** — 「근거 없는 통설」(§8)과 「탐색 한계」(§4.5)가 같은 D다.
- **추론에 A를 붙인 곳**: §2.1 결론 「(A, FC26+FC27)」, §5.5 종합 「팀 전술로 만들 수 있는 것은 위치뿐」. §3.2에서는 추론임을 명시했으면서 여기선 안 한다.
- **버전 미표기·캐리오버 경고 누락**: §6.1 스탠드 태클 71/85 컷(FC26)에 FC27 재확인 경고가 없다(§6.2 라인 구간엔 달았다). §5.3 빌드업 스타일·§5.4 Tactical Focus 연동은 전부 FC25 문서인데 FC26/FC27 재확인 여부 무표기. §4.1 HyperMotionV/GES 정의도 FC25판이며 FC27 세대 변경 여부 미확인.
- **URL 없는 A 주장**: §2.2 「페널티 Composure Ring(A, FC25)」, §6.1 「FC26 TU 1.4.0 Lengthy 185/165cm」 — 링크 없음.

### F. 결론이 DB로 내려가지 않았다 (DoD 미충족)

- **적재 계획이 전무하다.** 새로 확정한 사실(§5.5 Secondary Contain 거리↑, Team Press 포지션 계층 차등)을 `game_system_changes` 행으로 쓸지, 기각 5건을 `observations`/`reproduction_limits`에 남길지 판단 없음.
- **재발형 함정 2건이 `docs/70-lessons.md`로 가지 않았다** — ⑴ fut.gg 캐시 응답(`last-modified` 얼리액세스 이전 · md5 동일)을 버전 근거로 쓴 것, ⑵ FIFAUTeam 단일 계보를 다국어 교차검증으로 센 것. 둘 다 재발 이력형이다.
- §5.2의 **「실점 직후 → 소유권 상실 직후」 오역 정정은 지시만 있고 실행되지 않았다** — 대상 파일·행 수·grep 결과가 없다.
- §6.4 조치 4단계에 **불변규칙 5(export → dump → 명시 스테이징 커밋)**가 빠졌다.

### G. 방법론 공백

- **「2/2 반증」의 두 표가 독립이었는지** 기록이 없다. 기각 5건 전부 2/2인데 표본·에이전트 식별자·근거 분리 여부가 없어 검증 불가.
- **8에이전트 분담표·검색어 원문이 없다.** 점검 ⑤(다음 회차 검색어)를 리포트 자체로는 답할 수 없다.
- **얼리액세스 09-18이 3일 지났는데 §8.4·§9.4는 「발매 09-25 이후」로 미룬다** — 09-20 GG Club 싱크 행이 있으므로 **지금 인게임 접근이 되는지부터** 확정해야 한다. 내부 모순이자 3일치 기회 상실.
- **성공 기준이 없다.** 「역할당 5~10경기」의 근거·수렴 판정 기준·표본 크기 산정·종료 조건이 없다. §9.4 전체가 검증 가능한 목표가 아니라 할 일 나열이다.

### H. 다음 회차 검색어 (리포트에 답이 없어 보완)

- **EA 1차 미탐**: `FC 27 Launch Update pitch notes` · `FC 27 Title Update 1.x` · help.ea.com `FC 27 attributes` 재시도 · EA Forums 피치노트 미러 · EA SPORTS FC Direct 영상 전사.
- **이탈리아어**: `FC 27 ruoli giocatore focus movimento test` · `FC 27 compostezza controllo palla attributi come funziona` · `FC 27 linea difensiva altezza valori`.
- **일본어**: `FC27 ロール ファミリアリティ 検証` · `FC27 プレースタイル 弱体化 比較` · `FC27 ディフェンスライン 高さ 数値` · `FC27 ファーストタッチ ボールコントロール 検証`.
- **폴란드어·튀르키예어**(독립 계보 후보): `FC 27 role zawodnika test` / `FC 27 oyuncu rolleri test`.
- **데이터마이닝(B등급 겨냥)**: `FC 27 datamine roles json` · `fifa editor tool FC27 teamtactics table` · `frosty FC27 attribdata` · `FC 27 buildupplay table dump`.
- **통제 실측(C등급 겨냥)**: r/EASportsFC `controlled test first touch` · `practice arena test composure` · YouTube `FC 27 role heatmap test` (+ 메모리 규칙상 빌라 축 영상은 UTVFANCHANNEL·TheVillans 포함).
- **개발자 인터뷰**: Gilliard Lopes / Sam Rivera / Jamey Cane — ES·FR·IT·PT-BR 매체 현장 취재분.

관련 파일: `/Users/user/Documents/tactics/core/team_settings.py` (44~50행), `/Users/user/Documents/tactics/docs/20-fc-game-system.md` (558행 이하 매핑 규칙), `/Users/user/Documents/tactics/docs/21-game-fc27.md`, `/Users/user/Documents/tactics/docs/22-fc-gameplay-mechanics.md` (53행), `/Users/user/Documents/tactics/db/tactics.db` (`game_system_changes` FC27 #10~#21, `game_tactic_params`, `ingame_captures`, `fut_tactics`, `fut_tactic_roles`).
