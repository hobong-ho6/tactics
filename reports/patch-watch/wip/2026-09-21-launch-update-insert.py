import sqlite3

SRC = "https://www.ea.com/games/ea-sports-fc/fc-27/news/pitch-notes-fc27-launch-update (2026-09-14)"
CONF_A = ("A (EA 1차 · 피치노트 원문 직접 확인 2026-09-21). "
          "⚠️ 이 글은 de/pt-br 로케일에서도 영어 본문만 제공돼 다국어 교차검증이 불가능하다(불변규칙 10 예외 사유).")

ROWS = [
    dict(
        area="meta",
        change=(
            "⭐ 케미스트리 개편 — ICON의 **국적 기여가 +2→+1**로 축소된다(모든 리그에 +1 리그 링크는 유지, "
            "포지션에 맞게 기용 시 풀 케미도 유지). Hero의 **리그 기여가 +2→+1**로 축소된다(국적 +1은 유지). "
            "신설 티어 Hall of FUT은 Hero와 동일한 케미 규칙을 따른다. 캠페인·스페셜 아이템에 보정 케미를 주는 것도 "
            "연중 더 선별적으로만 한다."
        ),
        evidence=(
            "「ICONs will continue to receive full Chemistry when played in position and provide a +1 League link to "
            "every League. Their Nation contribution is being reduced from +2 to +1.」"
            "(ICON은 포지션에 맞게 기용되면 계속 풀 케미스트리를 받고 모든 리그에 +1 리그 링크를 제공한다. "
            "국적 기여는 +2에서 +1로 축소된다.) · "
            "「Heroes will also continue to receive full Chemistry when played in position, while their League "
            "contribution is being reduced from +2 to +1. Their +1 Nation contribution remains unchanged. "
            "Hall of FUT Items will follow the same Chemistry rules as Heroes.」"
            "(Hero 역시 포지션에 맞게 기용되면 계속 풀 케미스트리를 받으며, 리그 기여는 +2에서 +1로 축소된다. "
            "국적 +1 기여는 변하지 않는다. Hall of FUT 아이템은 Hero와 동일한 케미스트리 규칙을 따른다.)"
        ),
        impact=(
            "FUT 원장(fut_*)의 스쿼드 설계 판단이 바뀐다. `chem_points`는 EA에서 동기화해 받는 값이라 코드 수정은 "
            "필요 없지만, **ICON을 국적 허브로 쓰던 구성과 Hero를 리그 허브로 쓰던 구성이 각각 한 단계 약해진다** — "
            "PL 리그 링크를 Hero로 메우던 빌라 재현 스쿼드류는 케미 재계산이 필요하다. "
            "다음 /club-sync 회차에서 현재 스쿼드를 FC27 규칙으로 다시 검산할 것."
        ),
    ),
    dict(
        area="meta",
        change=(
            "업그레이드 페이싱 완화 — **캠페인 간 속성 상승폭을 축소**한다. 캠페인 스쿼드 자체도 작아지고"
            "(Destined for Glory 기준 주당 15명), 최상위 아이템과 하위 아이템의 **속성·PlayStyle 부스트 분포 간격이 좁아진다**. "
            "연간 캠페인 주차도 약 5주 감소하고 그 자리를 신규 스페셜 아이템 없는 Series가 채운다. "
            "(PlayStyle+ 상한 5→3은 id 13·21에 기적재 — 같은 문장의 앞 절이다.)"
        ),
        evidence=(
            "「we're establishing a more gradual upgrade pacing across the year by reducing the maximum number of "
            "PlayStyles+ from five to three and reducing the attribute increases between Campaigns」"
            "(우리는 PlayStyle+ 최대 개수를 5개에서 3개로 줄이고 캠페인 간 속성 상승폭을 축소함으로써 "
            "연중 업그레이드 속도를 더 완만하게 만들고 있다.) · "
            "「In practice, Campaign squads will have a tighter spread of Attributes and PlayStyle boosts.」"
            "(실제로 캠페인 스쿼드는 속성과 PlayStyle 부스트의 분포 폭이 더 좁아질 것이다.)"
        ),
        impact=(
            "**처방의 유효기간이 길어진다.** FC26까지는 시즌 중 캠페인 아이템이 속성을 크게 밀어올려 「지금 좋은 카드」가 "
            "달마다 갈렸지만, FC27은 상승폭이 작아 한 번 맞춘 `prescriptions`를 시즌 내내 유지할 수 있다 — 재검토 주기를 "
            "짧게 잡을 이유가 줄었다. 반대 방향이 더 중요하다: **「캠페인 나오면 메워지겠지」로 미뤄둔 포지션은 캠페인이 "
            "메워주지 않는다** — SBC·진화·이적시장으로 직접 채워야 한다."
        ),
    ),
    dict(
        area="meta",
        change=(
            "진화(Evolutions) 규칙 변경 — 출시 **빈도를 낮추고** 의도된 시점에만 배포한다. 대신 **포지션·속성 요건이 구체화된 "
            "맞춤 성장 경로**로 바뀌어, 선수 고유의 강점을 보존하는 방향으로만 성장시킨다. 저평점 선수용 Training Camp 진화는 확대."
        ),
        evidence=(
            "「you can still expect to see impactful Evolutions throughout the year, just at a lower frequency and "
            "released at more intentional moments」"
            "(연중 영향력 있는 진화는 여전히 기대할 수 있지만, 빈도는 더 낮아지고 더 의도된 시점에 배포된다.) · "
            "「Evolutions will also feature more tailored progression paths, with specific positional and Attribute "
            "requirements designed to preserve a player's unique identity and on-pitch strengths as they grow.」"
            "(진화는 또한 더 맞춤화된 성장 경로를 갖게 되며, 선수가 성장하는 동안에도 고유한 정체성과 경기장에서의 강점을 "
            "보존하도록 설계된 구체적인 포지션·속성 요건이 붙는다.)"
        ),
        impact=(
            "**진화 선택 판단의 축이 바뀐다.** 빈도가 낮아져 한 번의 진화 슬롯 선택 비용이 커졌고, 요건이 포지션·속성으로 "
            "구체화돼 **요건에 걸리는 카드를 미리 확보해 두는 것**이 이득이 된다. `fut_evolution_log`에 후보를 남길 때 "
            "「왜 이 카드인가」를 포지션·속성 요건 기준으로 적을 것. 진화가 고유 강점 보존 방향이라면, 우리 처방이 요구하는 "
            "역할별 속성(에메리식 역할 등)과 진화 요건이 겹치는 카드를 고르는 것이 가장 정확한 선택이다."
        ),
    ),
]

con = sqlite3.connect("db/tactics.db")
for r in ROWS:
    con.execute(
        "INSERT INTO game_system_changes(game_version, area, change, evidence, impact, source, confidence, recorded) "
        "VALUES('FC27', ?, ?, ?, ?, ?, ?, '2026-09-21')",
        (r["area"], r["change"], r["evidence"], r["impact"], SRC, CONF_A),
    )
con.commit()
print([row for row in con.execute(
    "SELECT id, area, substr(change,1,40) FROM game_system_changes WHERE recorded='2026-09-21' ORDER BY id")])
con.close()
