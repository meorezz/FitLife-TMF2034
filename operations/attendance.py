from __future__ import annotations

from .queries import commit, run_query
from utils.utils import print_table, prompt, prompt_int


def list_attendance(conn):
    headers, rows = run_query(
        conn,
        "SELECT a.Attendance_ID, m.Name AS Member, a.Class_ID, a.Attendance_Status, "
        "DATE_FORMAT(a.Checkin_Time, '%Y-%m-%d %H:%i') AS Checkin "
        "FROM MemberClassAttendance a "
        "LEFT JOIN Member m ON m.Member_ID=a.Member_ID "
        "ORDER BY a.Attendance_ID",
        fetch=True,
    )
    print_table(headers, rows)


def add_attendance(conn):
    member_id = prompt_int("Member_ID", 1001)
    class_id = prompt_int("Class_ID", 1)
    status = prompt("Attendance_Status (Attended/Absent)", "Attended")
    checkin = prompt("Checkin_Time (YYYY-MM-DD HH:MM:SS) or blank", "")
    checkin_val = checkin if checkin else None

    sql = ("INSERT INTO MemberClassAttendance (Member_ID, Class_ID, Attendance_Status, Checkin_Time) "
           "VALUES (%s,%s,%s,%s)")
    run_query(conn, sql, (member_id, class_id, status, checkin_val))
    commit(conn)
    print("Attendance added.")


def update_attendance(conn):
    aid = prompt_int("Attendance_ID to update")
    status = prompt("New Attendance_Status (Attended/Absent)", "Attended")
    run_query(conn, "UPDATE MemberClassAttendance SET Attendance_Status=%s WHERE Attendance_ID=%s", (status, aid))
    commit(conn)
    print("Attendance updated.")


def delete_attendance(conn):
    aid = prompt_int("Attendance_ID to delete")
    run_query(conn, "DELETE FROM MemberClassAttendance WHERE Attendance_ID=%s", (aid,))
    commit(conn)
    print("Attendance deleted.")
