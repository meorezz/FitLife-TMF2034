from __future__ import annotations

from datetime import datetime

from .queries import commit, run_query
from utils.utils import print_table, prompt, prompt_datetime, prompt_decimal, prompt_int
from utils.menu import crud_menu
from operations.sql_console import sql_console



def list_payments(conn):
    headers, rows = run_query(
        conn,
        "SELECT p.Payment_ID, p.Amount, DATE_FORMAT(p.Payment_Date, '%Y-%m-%d %H:%i') AS PayDate, "
        "p.Payment_Type, p.Reference_No, m.Name AS Member, p.Enrollment_ID "
        "FROM Payment p LEFT JOIN Member m ON m.Member_ID=p.Member_ID "
        "ORDER BY p.Payment_ID",
        fetch=True,
    )
    print_table(headers, rows)


def add_payment(conn):
    amount = prompt_decimal("Amount", 300.00)
    dt = prompt_datetime("Payment_Date (YYYY-MM-DD HH:MM:SS)", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ptype = prompt("Payment_Type", "Card")
    ref = prompt("Reference_No", f"REFNEW-{datetime.now().year}")
    member_id = prompt_int("Member_ID", 1001)
    enrollment_id = prompt_int("Enrollment_ID", 1)

    sql = ("INSERT INTO Payment (Amount, Payment_Date, Payment_Type, Reference_No, Member_ID, Enrollment_ID) "
           "VALUES (%s,%s,%s,%s,%s,%s)")
    run_query(conn, sql, (amount, dt, ptype, ref, member_id, enrollment_id))
    commit(conn)
    print("Payment added.")


def update_payment(conn):
    pid = prompt_int("Payment_ID to update")
    amount = prompt_decimal("New Amount", 300.00)
    run_query(conn, "UPDATE Payment SET Amount=%s WHERE Payment_ID=%s", (amount, pid))
    commit(conn)
    print("Payment updated.")


def delete_payment(conn):
    pid = prompt_int("Payment_ID to delete")
    run_query(conn, "DELETE FROM Payment WHERE Payment_ID=%s", (pid,))
    commit(conn)
    print("Payment deleted.")

def payments_menu(conn):
    while True:
        print("\n=== PAYMENTS ===")
        print("1) Selective Mode")
        print("2) Console Script Mode")
        print("0) Back")
        choice = prompt("Choose")

        if choice == "1":
            crud_menu(conn, "PAYMENTS", {
                "1": ("List payments", list_payments),
                "2": ("Add payment", add_payment),
                "3": ("Update payment", update_payment),
                "4": ("Delete payment", delete_payment),
                "0": ("Back", lambda c: None),
            })
        elif choice == "2":
            sql_console(conn, "PAYMENTS")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")