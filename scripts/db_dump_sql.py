#!/usr/bin/env python3
"""db/tactics.db → db/dump/*.sql — **sqlite3 CLI 버전과 무관한 형식**으로 쓴다(scripts/db_dump.sh가 부른다).

왜 (2026-11-02 · 불변규칙 13 — 같은 문제 2회째): 종전엔 `sqlite3 .schema` / `.mode insert`로 썼는데 CLI 버전마다 출력이 달랐다.
  ⑴ 실수: 옛 CLI `7.299999999999999823` ↔ 3.54 `7.3` ⑵ 스키마: `CREATE TABLE IF NOT EXISTS` 유무
  ⑶ 개행 등 제어 문자: 3.54는 `unistr('…\\u000a…')` — **3.50 이전 sqlite에는 unistr가 없어 복원조차 안 된다**.
  ⇒ PC·OS가 바뀔 때마다 내용은 같은데 수만 줄이 바뀌었다(`e994c9e` 19파일 · `671ed8c` 2.6만 줄).
  ⇒ 형식을 여기 한 곳에서 정한다: 실수 = 파이썬 repr(가장 짧은 왕복 표기 · 3.1+ 고정) · 제어 문자 = `char(N)` 이음(모든 sqlite 버전) ·
     스키마 = sqlite_master.sql 원문 그대로.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core.db import connect  # noqa: E402 — G36: DB 연결은 core.db만

OUT = ROOT / "db" / "dump"


def lit(v):
    if v is None:
        return "NULL"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        if math.isnan(v):
            return "NULL"
        if math.isinf(v):
            return "1e999" if v > 0 else "-1e999"
        return repr(v)
    if isinstance(v, bytes):
        return "X'" + v.hex().upper() + "'"
    # 문자열 — 제어 문자는 char(N)로 잇는다(unistr는 3.50+ 전용이라 쓰지 않는다)
    parts, buf = [], []
    for ch in v:
        if ord(ch) < 32 or ch == "\x7f":
            if buf:
                parts.append("'" + "".join(buf).replace("'", "''") + "'")
                buf = []
            parts.append(f"char({ord(ch)})")
        else:
            buf.append(ch)
    if buf or not parts:
        parts.append("'" + "".join(buf).replace("'", "''") + "'")
    return "||".join(parts)


def main():
    con = connect()
    OUT.mkdir(parents=True, exist_ok=True)
    rows = con.execute("SELECT type, name, sql FROM sqlite_master WHERE sql IS NOT NULL AND name NOT LIKE 'sqlite_%' ORDER BY rowid").fetchall()
    (OUT / "schema.sql").write_text("".join(f"{sql};\n" for _t, _n, sql in rows), encoding="utf-8")
    tables = [n for t, n, _s in rows if t == "table"]
    for t in sorted(tables):
        with open(OUT / f"{t}.sql", "w", encoding="utf-8") as f:
            for r in con.execute(f'SELECT * FROM "{t}"'):
                f.write(f"INSERT INTO {t} VALUES(" + ",".join(lit(v) for v in r) + ");\n")


if __name__ == "__main__":
    main()
