from __future__ import annotations

from .queries import run_query
from utils.utils import print_table, prompt
from operations.sql_console import sql_console


def report_members_summary(conn):
    sql = """
    SELECT
        m.Member_ID,
        m.Name,
        m.Membership_Type,
        m.Membership_Status,
        COALESCE(COUNT(DISTINCT e.Program_ID), 0) AS Total_Programs_Enrolled,
        COALESCE(SUM(CASE WHEN a.Attendance_Status='Attended' THEN 1 ELSE 0 END), 0) AS Total_Classes_Attended,
        COALESCE(SUM(p.Amount), 0) AS Total_Payments
    FROM Member m
    LEFT JOIN Enrollment e ON e.Member_ID = m.Member_ID
    LEFT JOIN MemberClassAttendance a ON a.Member_ID = m.Member_ID
    LEFT JOIN Payment p ON p.Member_ID = m.Member_ID
    GROUP BY m.Member_ID, m.Name, m.Membership_Type, m.Membership_Status
    ORDER BY m.Member_ID
    """
    headers, rows = run_query(conn, sql, fetch=True)
    print_table(headers, rows)


def report_scheduled_classes(conn):
    sql = """
    SELECT
        c.Class_ID,
        DATE_FORMAT(c.Schedule_DateTime, '%Y-%m-%d %H:%i') AS Schedule,
        t.Full_Name AS Trainer,
        c.Class_Status,
        pr.Category AS Program_Category,
        pr.Program_Name,
        c.Room,
        c.Max_Capacity
    FROM `Class` c
    JOIN Trainer t ON t.Trainer_ID = c.Trainer_ID
    JOIN Program pr ON pr.Program_ID = c.Program_ID
    ORDER BY c.Schedule_DateTime
    """
    headers, rows = run_query(conn, sql, fetch=True)
    print_table(headers, rows)


def report_trainer_performance(conn):
    sql = """
    SELECT
        t.Trainer_ID,
        t.Full_Name AS Trainer,
        COUNT(c.Class_ID) AS Total_Classes_Assigned,
        SUM(CASE WHEN c.Class_Status='Cancelled' THEN 1 ELSE 0 END) AS Total_Cancelled,
        SUM(CASE WHEN c.Class_Status='Completed' THEN 1 ELSE 0 END) AS Total_Completed,
        SUM(CASE WHEN c.Class_Status='Active' THEN 1 ELSE 0 END) AS Total_Active
    FROM Trainer t
    LEFT JOIN `Class` c ON c.Trainer_ID = t.Trainer_ID
    GROUP BY t.Trainer_ID, t.Full_Name
    ORDER BY Total_Classes_Assigned DESC, t.Full_Name
    """
    headers, rows = run_query(conn, sql, fetch=True)
    print_table(headers, rows)


def report_fees_quarterly_and_annual(conn):
    q_sql = """
    SELECT
        YEAR(Payment_Date) AS Year,
        QUARTER(Payment_Date) AS Quarter,
        SUM(Amount) AS Total_Fees
    FROM Payment
    GROUP BY YEAR(Payment_Date), QUARTER(Payment_Date)
    ORDER BY Year, Quarter
    """
    a_sql = """
    SELECT
        YEAR(Payment_Date) AS Year,
        SUM(Amount) AS Total_Fees
    FROM Payment
    GROUP BY YEAR(Payment_Date)
    ORDER BY Year
    """
    headers, rows = run_query(conn, q_sql, fetch=True)
    print("\nQuarterly Fees")
    print_table(headers, rows)

    headers, rows = run_query(conn, a_sql, fetch=True)
    print("\nAnnual Fees")
    print_table(headers, rows)


def report_top5_programs(conn):
    sql = """
    SELECT
        pr.Program_ID,
        pr.Program_Name,
        pr.Category,
        t.Full_Name AS Assigned_Trainer,
        COUNT(DISTINCT e.Member_ID) AS Total_Enrolled_Members
    FROM Program pr
    LEFT JOIN Enrollment e ON e.Program_ID = pr.Program_ID
    LEFT JOIN Trainer t ON t.Trainer_ID = pr.Trainer_ID
    GROUP BY pr.Program_ID, pr.Program_Name, pr.Category, t.Full_Name
    ORDER BY Total_Enrolled_Members DESC, pr.Program_Name
    LIMIT 5
    """
    headers, rows = run_query(conn, sql, fetch=True)
    print_table(headers, rows)


def reports_selective_menu(conn):
    while True:
        print("\n=== REPORTS (Selective Mode) ===")
        print("1) All members list with total number of programs enrolled, total classes attended, total payments made and membership status.")
        print("2) All scheduled classes with date, time, trainer, class status (completed, cancelled, active) and program category")
        print("3) Trainer performance reports (trainer name, total no. of classes taught, total missed or cancelled classes)")
        print("4) Quarterly and annual membership fees")
        print("5) Top 5 most popular programs with the total no. of enrolled members, assigned trainer and program category")
        print("0) Back")
        choice = prompt("Choose")
        if choice == "1":
            report_members_summary(conn)
        elif choice == "2":
            report_scheduled_classes(conn)
        elif choice == "3":
            report_trainer_performance(conn)
        elif choice == "4":
            report_fees_quarterly_and_annual(conn)
        elif choice == "5":
            report_top5_programs(conn)
        elif choice == "0":
            return
        else:
            print("Invalid choice.")

QUESTIONS = {
    "1": "All members list with total number of programs enrolled, total classes attended, total payments made and membership status.",
    "2": "All scheduled classes with date, time, trainer, class status (completed, cancelled, active) and program category.",
    "3": "Trainer performance reports (trainer name, total no. of classes taught, total missed or cancelled classes).",
    "4": "Quarterly and annual membership fees.",
    "5": "Top 5 most popular programs with the total no. of enrolled members, assigned trainer and program category."
}
            
def reports_menu(conn):
    while True:
        print("\n=== REPORTS ===")
        print("1) Selective Mode")
        print("2) Console Script Mode")
        print("0) Back")
        choice = prompt("Choose")

        if choice == "1":
            reports_selective_menu(conn)
        elif choice == "2":
            print("\n=== REPORT QUESTIONS ===")
            print("1) All members list with total number of programs enrolled, total classes attended, total payments made and membership status.")
            print("2) All scheduled classes with date, time, trainer, class status (completed, cancelled, active) and program category")
            print("3) Trainer performance reports (trainer name, total no. of classes taught, total missed or cancelled classes)")
            print("4) Quarterly and annual membership fees")
            print("5) Top 5 most popular programs with the total no. of enrolled members, assigned trainer and program category")
            print("0) Back")
            q = prompt("Choose question")
            
            if q == "0":
                break
            
            if q in QUESTIONS:
                print("\n==============================")
                print(f"Selected Question = Question {q}:")
                print(QUESTIONS[q])
                print("==============================")


                sql_console(conn, f"REPORTS - Question {q}")
            
            else:
                print("Invalid choice.")
                
        elif choice == "0":
            return
        else:
            print("Invalid choice.")
