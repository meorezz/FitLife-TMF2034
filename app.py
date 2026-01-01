from __future__ import annotations

import sys

from mysql.connector import Error
from database.db_connection import DBConfig, connect_db
from utils.menu import crud_menu
from utils.utils import prompt
from operations.reports import *
from operations.members import *
from operations.trainers import *
from operations.programs import *
from operations.classes import *
from operations.enrollments import *
from operations.payments import *
from operations.attendance import *
from utils.utils import prompt
from operations.sql_console import sql_console 


def module_mode_menu(conn, title: str, ops: dict):
    while True:
        print(f"\n=== {title} ===")
        print("1) Selective Mode")
        print("2) Console Script Mode")
        print("0) Back")
        ch = prompt("Choose")

        if ch == "1":
            crud_menu(conn, title, ops)
        elif ch == "2":
            sql_console(conn, title)
        elif ch == "0":
            return
        else:
            print("Invalid choice.")
            
def main():
    cfg = DBConfig()
    try:
        conn = connect_db(cfg)
    except Error as e:
        print("Could not connect to database.")
        print(f"Error: {e}")
        print("\nTip: set env vars DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME")
        sys.exit(1)

    print("Connected to database:", cfg.database)

    try:
        while True:
            print("\n****************************")
            print("\n=== FITLIFE WELLNESS APP ===")
            print("\n****************************")
            print("\nChoose any module to proceed:")
            print("\n")
            print("1) Members")
            print("2) Trainers")
            print("3) Programs")
            print("4) Classes")
            print("5) Enrollments")
            print("6) Payments")
            print("7) Attendance")
            print("8) Reports")
            print("0) Exit")
            choice = prompt("\nChoose")

            if choice == "1":
                module_mode_menu(conn, "MEMBERS", {
                    "1": ("List members", list_members),
                    "2": ("Add member", add_member),
                    "3": ("Update member", update_member),
                    "4": ("Delete member", delete_member),
                    "0": ("Back", lambda c: None),
                })
            elif choice == "2":
                module_mode_menu(conn, "TRAINERS", {
                    "1": ("List trainers", list_trainers),
                    "2": ("Add trainer", add_trainer),
                    "3": ("Update trainer", update_trainer),
                    "4": ("Delete trainer", delete_trainer),
                    "0": ("Back", lambda c: None),
                })
            elif choice == "3":
                module_mode_menu(conn, "PROGRAMS", {
                    "1": ("List programs", list_programs),
                    "2": ("Add program", add_program),
                    "3": ("Update program", update_program),
                    "4": ("Delete program", delete_program),
                    "0": ("Back", lambda c: None),
                })
            elif choice == "4":
                module_mode_menu(conn, "CLASSES", {
                    "1": ("List classes", list_classes),
                    "2": ("Add class", add_class),
                    "3": ("Update class", update_class),
                    "4": ("Delete class", delete_class),
                    "0": ("Back", lambda c: None),
                })
            elif choice == "5":
                module_mode_menu(conn, "ENROLLMENTS", {
                    "1": ("List enrollments", list_enrollments),
                    "2": ("Add enrollment", add_enrollment),
                    "3": ("Update enrollment", update_enrollment),
                    "4": ("Delete enrollment", delete_enrollment),
                    "0": ("Back", lambda c: None),
                })
            elif choice == "6":
                module_mode_menu(conn, "PAYMENTS", {
                    "1": ("List payments", list_payments),
                    "2": ("Add payment", add_payment),
                    "3": ("Update payment", update_payment),
                    "4": ("Delete payment", delete_payment),
                    "0": ("Back", lambda c: None),
                })
            elif choice == "7":
                module_mode_menu(conn, "ATTENDANCE", {
                    "1": ("List attendance", list_attendance),
                    "2": ("Add attendance", add_attendance),
                    "3": ("Update attendance", update_attendance),
                    "4": ("Delete attendance", delete_attendance),
                    "0": ("Back", lambda c: None),
                })
            elif choice == "8":
                reports_menu(conn)
            elif choice == "0":
                print("Bye.")
                return
            else:
                print("Invalid choice.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
