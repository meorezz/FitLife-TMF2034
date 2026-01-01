from __future__ import annotations

from .queries import commit, run_query
from utils.utils import print_table, prompt, prompt_decimal, prompt_int
from utils.menu import crud_menu
from operations.sql_console import sql_console



def list_programs(conn):
    headers, rows = run_query(
        conn,
        "SELECT p.Program_ID, p.Program_Name, p.Category, p.Duration_Weeks, p.Fee, t.Full_Name AS Trainer "
        "FROM Program p LEFT JOIN Trainer t ON t.Trainer_ID=p.Trainer_ID "
        "ORDER BY p.Program_ID",
        fetch=True,
    )
    print_table(headers, rows)


def add_program(conn):
    pname = prompt("Program_Name")
    cat = prompt("Category", "General Fitness")
    weeks = prompt_int("Duration_Weeks", 8)
    fee = prompt_decimal("Fee", 300.00)
    trainer_id = prompt_int("Trainer_ID", 1)

    sql = "INSERT INTO Program (Program_Name, Category, Duration_Weeks, Fee, Trainer_ID) VALUES (%s,%s,%s,%s,%s)"
    run_query(conn, sql, (pname, cat, weeks, fee, trainer_id))
    commit(conn)
    print("Program added.")


def update_program(conn):
    pid = prompt_int("Program_ID to update")
    fee = prompt("New Fee (blank to skip)", "")
    weeks = prompt("New Duration_Weeks (blank to skip)", "")

    fields = []
    params = []
    if fee:
        fields.append("Fee=%s")
        params.append(float(fee))
    if weeks:
        fields.append("Duration_Weeks=%s")
        params.append(int(weeks))

    if not fields:
        print("Nothing to update.")
        return

    params.append(pid)
    sql = f"UPDATE Program SET {', '.join(fields)} WHERE Program_ID=%s"
    run_query(conn, sql, tuple(params))
    commit(conn)
    print("Program updated.")


def delete_program(conn):
    pid = prompt_int("Program_ID to delete")
    run_query(conn, "DELETE FROM Enrollment WHERE Program_ID=%s", (pid,))
    run_query(conn, "DELETE FROM `Class` WHERE Program_ID=%s", (pid,))
    run_query(conn, "DELETE FROM Program WHERE Program_ID=%s", (pid,))
    commit(conn)
    print("Program deleted (and dependent rows removed).")
    
def programs_menu(conn):
    while True:
        print("\n=== PROGRAMS ===")
        print("1) Selective Mode")
        print("2) Console Script Mode")
        print("0) Back")
        choice = prompt("Choose")

        if choice == "1":
            crud_menu(conn, "PROGRAMS", {
                "1": ("List programs", list_programs),
                "2": ("Add program", add_program),
                "3": ("Update program", update_program),
                "4": ("Delete program", delete_program),
                "0": ("Back", lambda c: None),
            })
        elif choice == "2":
            sql_console(conn, "PROGRAMS",)
        elif choice == "0":
            return
        else:
            print("Invalid choice.")
