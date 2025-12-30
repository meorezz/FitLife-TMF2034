from __future__ import annotations

from datetime import datetime

from .queries import commit, run_query
from utils.utils import print_table, prompt, prompt_datetime, prompt_int


def list_enrollments(conn):
    headers, rows = run_query(
        conn,
        "SELECT e.Enrollment_ID, DATE_FORMAT(e.Enrollment_Date, '%Y-%m-%d %H:%i') AS EnrollDate, "
        "e.Enrollment_Status, e.Payment_Status, m.Name AS Member, p.Program_Name AS Program "
        "FROM Enrollment e "
        "LEFT JOIN Member m ON m.Member_ID=e.Member_ID "
        "LEFT JOIN Program p ON p.Program_ID=e.Program_ID "
        "ORDER BY e.Enrollment_ID",
        fetch=True,
    )
    print_table(headers, rows)


def add_enrollment(conn):
    dt = prompt_datetime("Enrollment_Date (YYYY-MM-DD HH:MM:SS)", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    estatus = prompt("Enrollment_Status", "Active")
    pstatus = prompt("Payment_Status", "Pending")
    member_id = prompt_int("Member_ID", 1001)
    program_id = prompt_int("Program_ID", 1)

    sql = ("INSERT INTO Enrollment (Enrollment_Date, Enrollment_Status, Payment_Status, Member_ID, Program_ID) "
           "VALUES (%s,%s,%s,%s,%s)")
    run_query(conn, sql, (dt, estatus, pstatus, member_id, program_id))
    commit(conn)
    print("Enrollment added.")


def update_enrollment(conn):
    eid = prompt_int("Enrollment_ID to update")
    pstatus = prompt("New Payment_Status (Paid/Pending/Partial)", "Paid")

    run_query(conn, "UPDATE Enrollment SET Payment_Status=%s WHERE Enrollment_ID=%s", (pstatus, eid))
    commit(conn)
    print("Enrollment updated.")


def delete_enrollment(conn):
    eid = prompt_int("Enrollment_ID to delete")
    run_query(conn, "DELETE FROM Payment WHERE Enrollment_ID=%s", (eid,))
    run_query(conn, "DELETE FROM Enrollment WHERE Enrollment_ID=%s", (eid,))
    commit(conn)
    print("Enrollment deleted (and dependent payments removed).")
