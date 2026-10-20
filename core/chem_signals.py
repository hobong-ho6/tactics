"""케미 신호(futgg_chem_signals) 「바뀐 행만 저장」 규약의 정본 (migration 106 · 2026-10-12).

행 = pulled부터 last_seen까지 같은 값으로 **연속 관측된** (카드, 스타일). 그날 유효한 행은 pulled ≤ 날짜 ≤ last_seen.
⭐ 「연속」은 **그 카드의 직전 관측** 기준이다(2026-10-20 증분 수집 전환) — 수집기가 회차마다 일부 카드만 열므로
   안 연 회차는 부재가 아니라 미관측이다. 직전 관측과 값이 같으면 잇고, 다르면 새 행을 연다.
   (종전 2026-10-12~10-20은 표 전체 회차 기준이었다 — 매번 전수를 열던 때.)
⛔ 수집기·마이그레이션·export·게이트가 각자 비교식을 다시 쓰지 않는다 — 여기서 import한다(불변규칙 13 ②).
"""


def content_key(accelerate, vote_pct):
    """내용 비교 키 — 값 두 칸만 본다(source·confidence는 관측 메타데이터)."""
    return (accelerate, vote_pct)


def prev_obs(con, ea_item_id, pulled):
    """그 카드의 pulled 직전 관측일(없으면 None). ⚠️ 그 카드의 오늘 행을 쓰기 **전에** 부른다."""
    return con.execute("SELECT MAX(last_seen) FROM futgg_chem_signals WHERE ea_item_id=? AND last_seen < ?",
                       (ea_item_id, pulled)).fetchone()[0]


def upsert(con, ea_item_id, pulled, style, accelerate, vote_pct, source, confidence, prev):
    """한 (카드, 스타일) 관측을 적는다. 반환: 'extend' | 'insert' | 'same-day'.

    prev = prev_obs()가 준 그 카드의 직전 관측일. 그날 같은 값으로 끝난 행이 있으면 last_seen만 늘린다.
    """
    row = con.execute("""SELECT id, pulled, last_seen, accelerate, vote_pct FROM futgg_chem_signals
                          WHERE ea_item_id=? AND style_name=? ORDER BY last_seen DESC, id DESC LIMIT 1""",
                      (ea_item_id, style)).fetchone()
    new = content_key(accelerate, vote_pct)
    if row is not None:
        rid, r_pulled, r_seen, r_acc, r_vote = row
        same = content_key(r_acc, r_vote) == new
        if r_seen == pulled:                         # 같은 날 재실행
            if same:
                return "same-day"
            if r_pulled == pulled:                   # 오늘 새로 만든 행 → 값만 바꾼다
                con.execute("UPDATE futgg_chem_signals SET accelerate=?, vote_pct=?, source=?, confidence=? WHERE id=?",
                            (accelerate, vote_pct, source, confidence, rid))
                return "same-day"
            # 앞 행을 오늘까지 늘려 놨는데 값이 바뀌었다 → 늘린 걸 되돌리고 새 행
            con.execute("UPDATE futgg_chem_signals SET last_seen=? WHERE id=?", (prev, rid))
        elif same and prev is not None and r_seen == prev:
            con.execute("UPDATE futgg_chem_signals SET last_seen=? WHERE id=?", (pulled, rid))
            return "extend"
    con.execute("""INSERT INTO futgg_chem_signals
                   (ea_item_id, pulled, last_seen, style_name, accelerate, vote_pct, source, confidence)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (ea_item_id, pulled, pulled, style, accelerate, vote_pct, source, confidence))
    return "insert"
