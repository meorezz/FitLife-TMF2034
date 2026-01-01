from __future__ import annotations

from .queries import commit, run_query
from utils.utils import print_table, prompt, prompt_int
from utils.menu import crud_menu
from operations.sql_console import sql_console



def list_trainers(conn):
    headers, rows = run_query(
        conn,
        "SELECT Trainer_ID, Full_Name, Specialization, Certification_Level, Trainer_Type "
        "FROM Trainer ORDER BY Trainer_ID",
        fetch=True,
    )
    print_table(headers, rows)


def add_trainer(conn):
    full_name = prompt("Full_Name")
    spec = prompt("Specialization", "")
    cert = prompt("Certification_Level", "")
    contact = prompt("Contact_Details", "")
    ttype = prompt("Trainer_Type (Yoga/Fitness/Physio)", "Fitness")

    sql = ("INSERT INTO Trainer (Full_Name, Specialization, Certification_Level, Contact_Details, Trainer_Type) "
           "VALUES (%s,%s,%s,%s,%s)")
    run_query(conn, sql, (full_name, spec, cert, contact, ttype))
    commit(conn)
    print("Trainer added.")


def update_trainer(conn):
    tid = prompt_int("Trainer_ID to update")
    contact = prompt("New Contact_Details", "")
    cert = prompt("New Certification_Level", "")

    fields = []
    params = []
    if contact:
        fields.append("Contact_Details=%s")
        params.append(contact)
    if cert:
        fields.append("Certification_Level=%s")
        params.append(cert)

    if not fields:
        print("Nothing to update.")
        return

    params.append(tid)
    sql = f"UPDATE Trainer SET {', '.join(fields)} WHERE Trainer_ID=%s"
    run_query(conn, sql, tuple(params))
    commit(conn)
    print("Trainer updated.")


def delete_trainer(conn):
    tid = prompt_int("Trainer_ID to delete")
    run_query(conn, "DELETE FROM Program WHERE Trainer_ID=%s", (tid,))
    run_query(conn, "DELETE FROM `Class` WHERE Trainer_ID=%s", (tid,))
    run_query(conn, "DELETE FROM YogaTrainer WHERE Trainer_ID=%s", (tid,))
    run_query(conn, "DELETE FROM PhysioTrainer WHERE Trainer_ID=%s", (tid,))
    run_query(conn, "DELETE FROM FitnessTrainer WHERE Trainer_ID=%s", (tid,))
    run_query(conn, "DELETE FROM Trainer WHERE Trainer_ID=%s", (tid,))
    commit(conn)
    print("Trainer deleted (and dependent rows removed).")
    
def trainers_menu(conn):
    while True:
        print("\n=== TRAINERS ===")
        print("1) Selective Mode")
        print("2) Console Script Mode")
        print("0) Back")
        choice = prompt("Choose")

        if choice == "1":
            crud_menu(conn, "TRAINERS", {
                "1": ("List trainers", list_trainers),
                "2": ("Add trainer", add_trainer),
                "3": ("Update trainer", update_trainer),
                "4": ("Delete trainer", delete_trainer),
                "0": ("Back", lambda c: None),
            })
        elif choice == "2":
            sql_console(conn, "TRAINERS")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")
