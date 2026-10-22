"""PlayStyle 이름 어휘 — 정본·별칭을 **한 곳**에서 읽는다 (2026-10-22 · migration 121).

왜: EA FC27 공식 이름(「1v1 Close Down」·「Gamechanger」)과 fut.gg·우리 저장 행의 이름(「Rush Out」·「Game Changer」)이 다르다.
    저장 행은 고치지 않고(불변규칙 2) 별칭 표 `fc_playstyle_aliases`로 잇는다. 읽는 쪽은 전부 이 모듈을 거친다 —
    파생 어휘를 세션마다 다르게 쓰는 사고(obs#527)를 구조로 막는다(불변규칙 13 ②).

    canonical(con, 'Rush Out+', 'FC27')  -> '1v1 Close Down+'
    vocab(con, 'FC27')                   -> 정본 ∪ 별칭 (게이트 G35 ⑵가 쓴다)
    canonical_names(con, 'FC27')         -> EA 공식 이름 집합(이 버전에 없는 잔존 이름은 제외)
"""
from __future__ import annotations

import re

_PLUS = re.compile(r"\s*\+$")


def split_plus(name: str) -> tuple[str, bool]:
    base = _PLUS.sub("", (name or "").strip())
    return base, bool(_PLUS.search((name or "").strip()))


def alias_map(con, gv: str) -> dict[str, str | None]:
    """alias → canonical(None = 이 버전에 없는 이름). 연결은 호출자가 core.db.connect로 연 것을 넘긴다(G36 — 직접 연결 금지)."""
    try:
        return {a: c for a, c in con.execute(
            "SELECT alias, canonical FROM fc_playstyle_aliases WHERE game_version=?", (gv,))}
    except Exception:          # 표가 없는 옛 DB(migration 121 이전) — 별칭 없음
        return {}


def canonical_names(con, gv: str) -> set[str]:
    """EA 공식 이름 집합 = fc_playstyle_ids 이름에 별칭을 적용하고, 이 버전에 없는 이름(canonical NULL)은 뺀다."""
    amap = alias_map(con, gv)
    out: set[str] = set()
    for (nm,) in con.execute("SELECT name FROM fc_playstyle_ids WHERE game_version=?", (gv,)):
        if nm in amap:
            if amap[nm]:
                out.add(amap[nm])
        else:
            out.add(nm)
    return out


def vocab(con, gv: str) -> set[str]:
    """정본 ∪ 별칭(잔존 이름 포함) — 「모르는 이름」 판정용."""
    return canonical_names(con, gv) | set(alias_map(con, gv).keys())


def canonical(con, name: str, gv: str) -> str:
    """이름(끝 `+` 허용)을 EA 공식 이름으로. 별칭이 아니면 그대로. 이 버전에 없는 잔존 이름도 그대로 둔다(지우지 않는다)."""
    base, plus = split_plus(name)
    c = alias_map(con, gv).get(base)
    base = c or base
    return base + ("+" if plus else "")


def split_list(s: str | None) -> list[str]:
    """`fut_club_players.current_playstyles` · `player_game_stats.playstyles` 형식(쉼표 구분 · 끝 `+`)을 목록으로."""
    return [x.strip() for x in (s or "").split(",") if x.strip()]
