from __future__ import annotations

import sys

from mysql.connector import Error
from database.db_connection import DBConfig, connect_db
from utils.menu import crud_menu
from utils.utils import prompt
from operations.reports import reports_menu
from operations.members import list_members, add_member, update_member, delete_member
from operations.trainers import list_trainers, add_trainer, update_trainer, delete_trainer
from operations.programs import list_programs, add_program, update_program, delete_program
from operations.classes import list_classes, add_class, update_class, delete_class
from operations.enrollments import list_enrollments, add_enrollment, update_enrollment, delete_enrollment
from operations.payments import list_payments, add_payment, update_payment, delete_payment
from operations.attendance import list_attendance, add_attendance, update_attendance, delete_attendance
from utils.utils import prompt


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
            print("1) Members CRUD")
            print("2) Trainers CRUD")
            print("3) Programs CRUD")
            print("4) Classes CRUD")
            print("5) Enrollments CRUD")
            print("6) Payments CRUD")
            print("7) Attendance CRUD")
            print("8) Print Reports")
            print("0) Exit")
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
                crud_menu(conn, "TRAINERS", {
                    "1": ("List trainers", list_trainers),
                    "2": ("Add trainer", add_trainer),
                    "3": ("Update trainer", update_trainer),
                    "4": ("Delete trainer", delete_trainer),
                    "0": ("Back", lambda c: None),
                })
            elif choice == "3":
                crud_menu(conn, "PROGRAMS", {
                    "1": ("List programs", list_programs),
                    "2": ("Add program", add_program),
                    "3": ("Update program", update_program),
                    "4": ("Delete program", delete_program),
                    "0": ("Back", lambda c: None),
                })
            elif choice == "4":
                crud_menu(conn, "CLASSES", {
                    "1": ("List classes", list_classes),
                    "2": ("Add class", add_class),
                    "3": ("Update class", update_class),
                    "4": ("Delete class", delete_class),
                    "0": ("Back", lambda c: None),
                })
            elif choice == "5":
                crud_menu(conn, "ENROLLMENTS", {
                    "1": ("List enrollments", list_enrollments),
                    "2": ("Add enrollment", add_enrollment),
                    "3": ("Update enrollment", update_enrollment),
                    "4": ("Delete enrollment", delete_enrollment),
                    "0": ("Back", lambda c: None),
                })
            elif choice == "6":
                crud_menu(conn, "PAYMENTS", {
                    "1": ("List payments", list_payments),
                    "2": ("Add payment", add_payment),
                    "3": ("Update payment", update_payment),
                    "4": ("Delete payment", delete_payment),
                    "0": ("Back", lambda c: None),
                })
            elif choice == "7":
                crud_menu(conn, "ATTENDANCE", {
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
