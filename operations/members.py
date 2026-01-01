from __future__ import annotations

from datetime import datetime

from .queries import commit, run_query
from utils.utils import print_table, prompt, prompt_datetime, prompt_int
from utils.menu import crud_menu
from operations.sql_console import sql_console



def list_members(conn):
    headers, rows = run_query(
        conn,
        "SELECT Member_ID, Name, Contact_Details, Email, Membership_Type, Membership_Status "
        "FROM Member ORDER BY Member_ID",
        fetch=True,
    )
    print_table(headers, rows)


def add_member(conn):
    name = prompt("Name")
    contact = prompt("Contact_Details (e.g. 6012...)")
    email = prompt("Email")
    dob = prompt("Date_of_Birth (YYYY-MM-DD)", "1999-01-01")
    gender = prompt("Gender (M/F)", "M")[:1].upper()
    mtype = prompt("Membership_Type (Standard/Premium)", "Standard")
    start = prompt_datetime("Membership_Start (YYYY-MM-DD HH:MM:SS)", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    end = prompt_datetime("Membership_End (YYYY-MM-DD HH:MM:SS)", "2026-12-31 23:59:59")
    status = prompt("Membership_Status (Active/Pending/Expired)", "Active")

    sql = ("INSERT INTO Member (Name, Contact_Details, Email, Date_of_Birth, Gender, Membership_Type, "
           "Membership_Start, Membership_End, Membership_Status) "
           "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    run_query(conn, sql, (name, contact, email, dob, gender, mtype, start, end, status))
    commit(conn)
    print("Member added.")


def update_member(conn):
    mid = prompt_int("Member_ID to update")
    status = prompt("New Membership_Status", "Active")
    contact = prompt("New Contact_Details", "")
    email = prompt("New Email", "")

    fields = []
    params = []
    if status:
        fields.append("Membership_Status=%s")
        params.append(status)
    if contact:
        fields.append("Contact_Details=%s")
        params.append(contact)
    if email:
        fields.append("Email=%s")
        params.append(email)

    if not fields:
        print("Nothing to update.")
        return

    params.append(mid)
    sql = f"UPDATE Member SET {', '.join(fields)} WHERE Member_ID=%s"
    run_query(conn, sql, tuple(params))
    commit(conn)
    print("Member updated.")


def delete_member(conn):
    mid = prompt_int("Member_ID to delete")
    run_query(conn, "DELETE FROM Payment WHERE Member_ID=%s", (mid,))
    run_query(conn, "DELETE FROM Enrollment WHERE Member_ID=%s", (mid,))
    run_query(conn, "DELETE FROM MemberClassAttendance WHERE Member_ID=%s", (mid,))
    run_query(conn, "DELETE FROM StandardMember WHERE Member_ID=%s", (mid,))
    run_query(conn, "DELETE FROM PremiumMember WHERE Member_ID=%s", (mid,))
    run_query(conn, "DELETE FROM Member WHERE Member_ID=%s", (mid,))
    commit(conn)
    print("Member deleted (and dependent rows removed).")

def members_menu(conn):
    while True:
        print("\n=== MEMBERS ===")
        print("1) Selective Mode")
        print("2) Console Script Mode")
        print("0) Back")
        choice = prompt("Choose")

        if choice == "1":
            crud_menu(conn, "MEMBERS", {
                "1": ("List members", list_members),
                "2": ("Add member", add_member),
                "3": ("Update member", update_member),
                "4": ("Delete member", delete_member),
                "0": ("Back", lambda c: None),
            })
        elif choice == "2":
            sql_console(conn, "MEMBERS")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")