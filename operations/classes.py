from __future__ import annotations

from .queries import commit, run_query
from utils.utils import print_table, prompt, prompt_datetime, prompt_int
from utils.menu import crud_menu
from operations.sql_console import sql_console



def list_classes(conn):
    headers, rows = run_query(
        conn,
        "SELECT c.Class_ID, DATE_FORMAT(c.Schedule_DateTime, '%Y-%m-%d %H:%i') AS Schedule, "
        "c.Room, c.Max_Capacity, c.Class_Status, p.Program_Name, t.Full_Name AS Trainer "
        "FROM `Class` c "
        "LEFT JOIN Program p ON p.Program_ID=c.Program_ID "
        "LEFT JOIN Trainer t ON t.Trainer_ID=c.Trainer_ID "
        "ORDER BY c.Schedule_DateTime",
        fetch=True,
    )
    print_table(headers, rows)


def add_class(conn):
    dt = prompt_datetime("Schedule_DateTime (YYYY-MM-DD HH:MM:SS)", "2026-01-10 09:00:00")
    room = prompt("Room", "Studio A")
    cap = prompt_int("Max_Capacity", 20)
    program_id = prompt_int("Program_ID", 1)
    trainer_id = prompt_int("Trainer_ID", 1)
    status = prompt("Class_Status (Active/Cancelled/Completed)", "Active")

    sql = ("INSERT INTO `Class` (Schedule_DateTime, Room, Max_Capacity, Program_ID, Trainer_ID, Class_Status) "
           "VALUES (%s,%s,%s,%s,%s,%s)")
    run_query(conn, sql, (dt, room, cap, program_id, trainer_id, status))
    commit(conn)
    print("Class added.")


def update_class(conn):
    cid = prompt_int("Class_ID to update")
    status = prompt("New Class_Status (Active/Cancelled/Completed)", "Active")
    room = prompt("New Room (blank to skip)", "")

    fields = []
    params = []
    if status:
        fields.append("Class_Status=%s")
        params.append(status)
    if room:
        fields.append("Room=%s")
        params.append(room)

    if not fields:
        print("Nothing to update.")
        return

    params.append(cid)
    sql = f"UPDATE `Class` SET {', '.join(fields)} WHERE Class_ID=%s"
    run_query(conn, sql, tuple(params))
    commit(conn)
    print("Class updated.")


def delete_class(conn):
    cid = prompt_int("Class_ID to delete")
    run_query(conn, "DELETE FROM MemberClassAttendance WHERE Class_ID=%s", (cid,))
    run_query(conn, "DELETE FROM `Class` WHERE Class_ID=%s", (cid,))
    commit(conn)
    print("Class deleted (and dependent rows removed).")


def classes_menu(conn):
    while True:
        print("\n=== CLASSES ===")
        print("1) Selective Mode")
        print("2) Console Script Mode")
        print("0) Back")
        choice = prompt("Choose")

        if choice == "1":
            crud_menu(conn, "CLASSES", {
                "1": ("List classes", list_classes),
                "2": ("Add class", add_class),
                "3": ("Update class", update_class),
                "4": ("Delete class", delete_class),
                "0": ("Back", lambda c: None),
            })
        elif choice == "2":
            sql_console(conn, "CLASSES",)
        elif choice == "0":
            return
        else:
            print("Invalid choice.")
