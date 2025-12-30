from __future__ import annotations

from typing import Any, Optional, Tuple


def run_query(conn, sql: str, params: Optional[Tuple[Any, ...]] = None, fetch: bool = False):
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        if fetch:
            rows = cur.fetchall()
            headers = [d[0] for d in cur.description] if cur.description else []
            return headers, rows
        return None
    finally:
        cur.close()


def commit(conn):
    conn.commit()


def rollback(conn):
    conn.rollback()
