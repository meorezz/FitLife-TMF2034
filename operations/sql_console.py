# operations/sql_console.py
from __future__ import annotations
from mysql.connector import Error


def _print_rows(columns, rows):
    if not rows:
        print("(0 rows)")
        return

    widths = [len(str(c)) for c in columns]
    for r in rows:
        for i, c in enumerate(columns):
            widths[i] = max(widths[i], len(str(r.get(c, ""))))

    def fmt(vals):
        return " | ".join(str(vals[i]).ljust(widths[i]) for i in range(len(vals)))

    print(fmt(columns))
    print("-+-".join("-" * w for w in widths))
    for r in rows:
        print(fmt([r.get(c, "") for c in columns]))


def sql_console(conn, title: str):
    print("\n==============================")
    print(f" {title} - CONSOLE SCRIPT MODE")
    print("==============================")
    print("Paste/type SQL and end with ';'")
    print("Commands: :q (back)\n")

    cur = conn.cursor(dictionary=True)
    buf = []
    while True:
        line = input("SQL> ").rstrip()
        if line.strip().lower() in (":q", ":quit", "quit", "exit"):
            cur.close()
            return

        buf.append(line)
        if line.endswith(";"):
            sql = "\n".join(buf).strip()
            buf = []
            if not sql:
                continue

            try:
                for res in cur.execute(sql, multi=True):
                    stmt = (res.statement or "").strip()
                    if not stmt:
                        continue

                    if res.with_rows:
                        rows = res.fetchall()
                        cols = list(res.column_names)
                        print(f"\n--- RESULT ({len(rows)} rows) ---")
                        _print_rows(cols, rows)
                    else:
                        conn.commit()
                        print("\n--- OK ---")
                        print(f"Rows affected: {res.rowcount}")
            except Error as e:
                conn.rollback()
                print("\n--- ERROR ---")
                print(e)
