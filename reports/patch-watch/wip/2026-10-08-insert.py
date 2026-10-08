"""FC27 패치 감시 2026-10-08 — EA 1차 자료 적재 (INSERT only, 불변규칙 2)."""
import sqlite3

TODAY = "2026-10-08"

GPDEV = "https://www.ea.com/games/ea-sports-fc/fc-27/news/fc-27-gameplay-developer-launch-update (2026-09-30)"
TU101 = "https://forums.ea.com/blog/ea-sports-fc-game-info-hub-en/fc-27-v1-0-1-small-bug-fix-update/13734805 (v1.0.1)"
TU102 = "https://forums.ea.com/blog/ea-sports-fc-game-info-hub-en/fc-27-v1-0-2---small-bug-fix-update/13752885 (v1.0.2)"
TU103 = "https://forums.ea.com/blog/ea-sports-fc-game-info-hub-en/fc-27-v1-0-3---small-bug-fix-update/13763421 (v1.0.3 · 2026-10-02)"
TU104 = "https://forums.ea.com/blog/ea-sports-fc-game-info-hub-en/ea-sports-fc%E2%84%A2-27--title-update-v1-0-4/13777445 (v1.0.4 · 2026-10-07)"
LAUNCH = "https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-launch-update (2026-09-14)"
FUTDEV = "https://www.ea.com/games/ea-sports-fc/fc-27/news/fc-27-fut-developer-launch-update (2026-10-01)"

A_DE = ("A (EA 1차 · 영어 원문 + 독일어 공식판 대조 2026-10-08). "
        "⚠️ 교차검증 아님에 주의 — 같은 글의 EA 자체 번역이다(불변규칙 12). "
        "⚠️ pt-br 공식판은 같은 문장을 「laterais avançando muito cedo」(풀백이 너무 일찍 **전진**)로 옮겨 "
        "en 「dropping」·de 「absinkt」(내려간다)와 **뜻이 반대다** — 로컬라이즈 오역으로 보고 en/de를 채택했다.")
A_PRIM = "A (EA 1차 · 원문 직접 확인 2026-10-08)."
A_NOLOC = ("A (EA 1차 · 원문 직접 확인 2026-10-08). "
           "⚠️ EA 포럼 Game Info Hub 글은 영어판만 존재해 다국어 대조가 불가능하다(불변규칙 10 예외 사유).")

ROWS = [
    dict(
        area="engine",
        change=(
            "⭐ 타이틀 업데이트 v1.0.1에서 **Authentic 프리셋 전용**으로 조키·스프린트 조키 기본 슬라이더 값이 "
            "중간 폭 상향됐다 — **Competitive에는 영향 없다**. The Grounds 11v11은 피로가 장기 스태미너에 주는 "
            "영향이 커졌다. 이후 **v1.0.2·v1.0.3·v1.0.4에는 게임플레이 변경이 0건**이다(1.0.3·1.0.4는 "
            "「게임플레이 밸런스·튜닝 변경 없음」을 본문에 명시, 1.0.2는 UT 버그 1건뿐)."
        ),
        evidence=(
            "「In Authentic Gameplay only (available in Career Mode and Kick Off) Jockey and Sprint Jockey Speed "
            "default slider values have moderately been increased. This change does not impact Competitive Gameplay.」"
            "(Authentic 게임플레이에서만(커리어 모드·킥오프에서 사용 가능) 조키 및 스프린트 조키 속도 기본 슬라이더 "
            "값이 중간 정도로 상향됐다. 이 변경은 Competitive 게임플레이에 영향을 주지 않는다.) · "
            "「In The Grounds 11v11 matches, increased the impact of fatigue on long-term player stamina.」"
            "(The Grounds 11v11 경기에서 피로가 선수의 장기 스태미너에 주는 영향을 증가시켰다.) · "
            "v1.0.3·v1.0.4 「There are no gameplay balance and tuning changes in this update.」"
            "(이 업데이트에는 게임플레이 밸런스·튜닝 변경이 없다.)"
        ),
        impact=(
            "**C등급(통제 실측)을 할 때 프리셋을 반드시 명기해야 한다.** 우리가 전술 재현을 확인하는 자리는 "
            "커리어·킥오프(Authentic)인데, 바로 그쪽만 조키가 빨라졌다 — 같은 선수·같은 전술이라도 "
            "v1.0.0 Authentic에서 잰 수비 체감과 v1.0.1 이후 수치가 다르다. "
            "기존 행 #15(수동 수비 강화는 Competitive 전용)의 전제가 **절반 깨졌다**: 수동 수비 보상은 여전히 "
            "Competitive 전용이지만, **조키 속도만은 Authentic에도 들어왔다**. "
            "⇒ 앞으로 `match_game_setups`·실측 메모에 프리셋(Competitive/Authentic)과 타이틀 버전을 같이 적는다."
        ),
        source=f"{TU101} · {TU102} · {TU103} · {TU104}",
        confidence=A_NOLOC,
    ),
    dict(
        area="positioning",
        change=(
            "⭐⭐ EA가 **풀백이 너무 일찍 내려와 수비 라인을 깨는 현상**을 출시 후 최다 피드백으로 공식 인정했다. "
            "원인 조사 중이며 **아직 수정하지 않았다** — 커뮤니티의 「초반에 게임을 바꾸지 말라」 요구를 받아들여 "
            "조사를 끝낸 뒤에나 조정한다고 밝혔다."
        ),
        evidence=(
            "en 「One of the largest quantities of feedback we've received has been around fullbacks dropping too "
            "early and breaking the defensive line.」"
            "(우리가 받은 피드백 중 가장 많은 양을 차지한 것 하나가 풀백이 너무 일찍 내려와 수비 라인을 깨는 "
            "문제에 관한 것이었다.) · "
            "de 공식판 「Wir hören im Feedback der Community sehr oft, dass die Außenverteidigung zu früh absinkt "
            "und die Defensivlinie auflöst.」"
            "(커뮤니티 피드백에서 측면 수비가 너무 일찍 내려앉아 수비 라인을 해체한다는 말을 아주 자주 듣는다.)"
        ),
        impact=(
            "**에메리 재현의 핵심 전제가 흔들린다.** 우리 처방은 높은 수비 라인 + 풀백의 전진 유지를 전제로 "
            "역할·전술 슬라이더를 깔아 왔는데, 엔진이 풀백을 조기 하강시키면 그 라인이 실제로는 유지되지 않는다 — "
            "`prescriptions`의 풀백 역할·수비 라인 높이 항목이 **의도대로 재현되지 않고 있을 가능성**이 크다. "
            "⚠️ 다만 EA가 **고칠 수도 있다고 밝힌 상태**라, 지금 체감에 맞춰 처방을 영구 변경하면 수정 패치 후 "
            "두 번 틀린다. ⇒ 처방은 그대로 두고, 인게임 관측(`reports/ingame/`)에 **「풀백 조기 하강 여부」를 "
            "고정 관측 항목으로 추가**해 수정 패치 전후를 비교할 수 있게 둔다."
        ),
        source=GPDEV,
        confidence=A_DE,
    ),
    dict(
        area="attributes",
        change=(
            "⭐ EA가 **수비 속성이 낮은 선수의 인터셉트가 과도하게 효과적일 수 있다**고 공식 인정했다 — "
            "「최고 수비수에게나 기대할 법한 인터셉트」를 낮은 수비 스탯 아이템이 해내고 있다는 것. "
            "다만 **수동 수비 보상이라는 설계 목표 자체는 달성됐다고 보고 유지한다**고 밝혔다(관측만, 미수정)."
        ),
        evidence=(
            "en 「Our design goals are to reward the manual defender for getting into passing lanes, and we feel "
            "we're achieving that.」"
            "(우리의 설계 목표는 패스 길목에 들어가는 수동 수비자에게 보상하는 것이고, 우리는 그것을 달성하고 "
            "있다고 본다.) · "
            "en 「That said, players using items with lower defensive attributes may be too effective at making the "
            "types [of interceptions typically expected only of the best defenders].」"
            "(그렇지만 수비 속성이 낮은 아이템을 쓰는 플레이어가 보통 최고 수비수에게나 기대되는 종류의 인터셉트를 "
            "하는 데 지나치게 효과적일 수 있다.) · "
            "de 공식판 「Aber es kann vorkommen, dass Profis mit niedrigeren Defensivwerten zu effektiv sind. Solche "
            "Profis können Bälle abfangen, die eigentlich nur die besten Abwehrprofis abfangen sollten.」"
            "(하지만 수비 수치가 낮은 선수가 지나치게 효과적인 경우가 생길 수 있다. 그런 선수가 원래는 최고의 "
            "수비 선수만 끊어야 할 공을 끊어낼 수 있다.)"
        ),
        impact=(
            "**수비 스탯 투자의 가성비 판단이 바뀐다 — 단, 한시적으로만.** 지금은 인터셉트 축에서 수비 스탯 문턱이 "
            "실질적으로 낮으므로, 중원·수비에 「인터셉트를 위해 수비 스탯을 더 산다」는 처방·진화 선택의 근거가 약하다 "
            "(같은 코스트면 다른 축이 낫다). ⚠️ EA가 명시적으로 **계속 모니터링한다**고 했으므로 이것은 "
            "**버그성 과효율일 가능성이 있는 상태**다 — `fut_evolution_log`·`prescriptions`에 이 사실을 근거로 쓸 때 "
            "「2026-10-08 기준 v1.0.4, EA 수정 예고 없음」을 함께 적는다. 수정되면 되돌려야 한다. "
            "⭐ 반대로 **수동 수비 보상 설계는 유지된다**고 EA가 못박았으므로, 패스 길목 차단을 전제로 한 "
            "압박 처방(시메오네·에메리 중원 압박)은 그대로 유효하다."
        ),
        source=GPDEV,
        confidence=A_DE,
    ),
    dict(
        area="meta",
        change=(
            "출시 초기 밸런스 정책이 **실행으로 확인됐다**(기존 #18은 예고였다) — v1.0.1~v1.0.4 어디에도 "
            "코어 게임플레이 밸런스 변경이 없다. EA는 ⑴ 킥오프 직후 득점 증가를 데이터에서 관측 중 ⑵ 니어포스트 "
            "로우드리븐 슛이 강하다는 피드백은 받았으나 **「슛과 골키퍼의 현재 밸런스에 상당히 만족한다」**고 밝힘 "
            "⑶ 현재 작업 중인 것은 **반칙 판정**뿐(특정 경합에서 심판이 올바른 결과를 주지 않는 문제)이라고 밝혔다."
        ),
        evidence=(
            "en 「While we aren't changing anything that would impact core gameplay, we are looking into several "
            "issues related to fouls.」"
            "(코어 게임플레이에 영향을 주는 것은 아무것도 바꾸지 않고 있지만, 반칙과 관련된 몇 가지 문제는 "
            "들여다보고 있다.) · "
            "en 「we're pretty happy with the current balance between shooting and goalkeeping」"
            "(우리는 슈팅과 골키핑 사이의 현재 밸런스에 상당히 만족하고 있다) · "
            "en 「a presence on this list does not mean we will be making changes」"
            "(이 목록에 올라 있다는 것이 우리가 변경을 하리라는 뜻은 아니다)"
        ),
        impact=(
            "**처방의 재검토 주기를 짧게 잡을 이유가 없다.** 2026-10-08 기준 v1.0.0의 게임플레이 튜닝이 사실상 "
            "그대로 살아 있다(Authentic 조키 1건 예외 — 같은 회차 engine 행 참조). "
            "⇒ 지금 쌓는 인게임 실측은 **한 버전의 일관된 표본**으로 묶어도 된다 — docs/22 §2.1이 예고한 "
            "「출시 2~4주 후 C등급 통제 실측」에 지금이 적기다. "
            "⚠️ 반대로 **반칙 판정은 곧 바뀐다** — 태클·경합 관련 실측(적극성 스탯의 반칙 리스크 축)은 "
            "지금 재면 수정 후 무효가 될 수 있으니 뒤로 미룬다."
        ),
        source=f"{GPDEV} · {TU101} · {TU103} · {TU104}",
        confidence=A_DE,
    ),
    dict(
        area="meta",
        change=(
            "캠페인 업그레이드 페이싱 완화가 **런치 업데이트 예고(09-14) → FUT 개발팀 런치 업데이트(10-01) 재확인**으로 "
            "닫혔다 — 캠페인 간 속성 상승폭을 줄이고, 캠페인 스쿼드를 **작게·OVR 분포를 좁게** 간다. "
            "목표는 「캠페인 스쿼드의 어느 아이템이든 선발 11명에 들 수 있게」. 연간 캠페인 주차도 약 5주 줄고 "
            "그 자리를 신규 스페셜 아이템 없는 Series가 채운다."
        ),
        evidence=(
            "런치 업데이트 「We're establishing a more gradual upgrade pacing across the year by reducing the maximum "
            "number of PlayStyles+ from five to three and reducing the attribute increases between Campaigns.」"
            "(우리는 PlayStyle+ 최대 개수를 5개에서 3개로 줄이고 캠페인 간 속성 상승폭을 축소함으로써 연중 업그레이드 "
            "속도를 더 완만하게 만들고 있다.) · "
            "FUT 개발팀 런치 업데이트 「we're taking a more focused approach with smaller squads and a tighter OVR "
            "spread than in previous years」"
            "(우리는 예년보다 더 작은 스쿼드와 더 좁은 OVR 분포로 더 집중된 접근을 취하고 있다) · "
            "「any Campaign squad item can earn a place in your starting XI」"
            "(캠페인 스쿼드의 어떤 아이템이든 당신의 선발 11명에 들 자격을 얻을 수 있다)"
        ),
        impact=(
            "**처방의 유효기간이 길어진다.** FC26까지는 캠페인 아이템이 속성을 크게 밀어올려 「지금 좋은 카드」가 "
            "달마다 갈렸지만, FC27은 상승폭이 작아 한 번 맞춘 `prescriptions`를 시즌 내내 유지할 수 있다. "
            "⭐ 더 중요한 반대 방향: **「캠페인 나오면 메워지겠지」로 미뤄둔 포지션은 캠페인이 메워주지 않는다** — "
            "SBC·진화·이적시장으로 직접 채워야 한다. 다음 /club-sync에서 결손 포지션을 캠페인 대기로 두지 말 것."
        ),
        source=f"{LAUNCH} · {FUTDEV}",
        confidence=(A_PRIM + " ⚠️ 두 글 모두 de/pt-br 로케일에서 영어 본문만 제공돼 다국어 대조가 불가능하다"
                    "(불변규칙 10 예외 사유)."),
    ),
    dict(
        area="evolution",
        change=(
            "⭐ 진화(Evolutions) 규칙 변경 — 출시 **빈도를 낮추고** 의도된 시점에만 배포한다. 대신 "
            "**포지션·속성 요건이 구체화된 맞춤 성장 경로**로 바뀌어, 선수 고유의 강점을 보존하는 방향으로만 "
            "성장시킨다(런치 업데이트 09-14). FUT 개발팀이 10-01에 **「진화 튜닝에 의미 있는 변경을 가했다」**고 "
            "재확인했다. 저평점 선수용 Training Camp 진화는 확대."
        ),
        evidence=(
            "런치 업데이트 「you can still expect to see impactful Evolutions throughout the year, just at a lower "
            "frequency and released at more intentional moments」"
            "(연중 영향력 있는 진화는 여전히 기대할 수 있지만, 빈도는 더 낮아지고 더 의도된 시점에 배포된다.) · "
            "「Evolutions will also feature more tailored progression paths, with specific positional and Attribute "
            "requirements designed to preserve a player's unique identity and on-pitch strengths as they grow.」"
            "(진화는 또한 더 맞춤화된 성장 경로를 갖게 되며, 선수가 성장하는 동안에도 고유한 정체성과 경기장에서의 "
            "강점을 보존하도록 설계된 구체적인 포지션·속성 요건이 붙는다.) · "
            "FUT 개발팀 런치 업데이트 「made meaningful changes to the tuning of Evolutions」"
            "(진화의 튜닝에 의미 있는 변경을 가했다)"
        ),
        impact=(
            "**진화 선택 판단의 축이 바뀐다.** 빈도가 낮아져 진화 슬롯 한 칸의 기회비용이 커졌고, 요건이 "
            "포지션·속성으로 구체화돼 **요건에 걸리는 카드를 미리 확보해 두는 것**이 이득이 된다. "
            "`fut_evolution_log`에 후보를 남길 때 「왜 이 카드인가」를 포지션·속성 요건 기준으로 적는다. "
            "진화가 고유 강점 보존 방향이라면, 우리 처방이 요구하는 역할별 속성(에메리식 역할 등)과 진화 요건이 "
            "겹치는 카드를 고르는 것이 가장 정확한 선택이다. 기존 행 #41(PlayStyle 보상의 (^3) = 보유 상한 3)과 "
            "같은 방향 — 진화로 메울 수 있는 폭 자체가 좁아졌다."
        ),
        source=f"{LAUNCH} · {FUTDEV}",
        confidence=(A_PRIM + " ⚠️ 두 글 모두 de/pt-br 로케일에서 영어 본문만 제공돼 다국어 대조가 불가능하다"
                    "(불변규칙 10 예외 사유)."),
    ),
]

con = sqlite3.connect("db/tactics.db")
for r in ROWS:
    con.execute(
        "INSERT INTO game_system_changes"
        "(game_version, area, change, evidence, impact, source, confidence, recorded) "
        "VALUES('FC27', ?, ?, ?, ?, ?, ?, ?)",
        (r["area"], r["change"], r["evidence"], r["impact"], r["source"], r["confidence"], TODAY),
    )
con.commit()
for row in con.execute(
        "SELECT id, area, substr(change,1,50) FROM game_system_changes WHERE recorded=? ORDER BY id", (TODAY,)):
    print(row)
con.close()
