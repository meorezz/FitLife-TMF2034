"""
Enrollment Operations Module
Handles all CRUD operations for Enrollments
"""

from mysql.connector import Error
from datetime import datetime


class EnrollmentOperations:
    """Class to handle enrollment-related database operations"""
    
    def __init__(self, db):
        """Initialize with database connection"""
        self.db = db
        self.cursor = db.get_cursor()
        self.connection = db.get_connection()
    
    def add_enrollment(self):
        """Add a new enrollment"""
        print("\n" + "=" * 60)
        print(" " * 18 + "ADD NEW ENROLLMENT")
        print("=" * 60)
        
        try:
            # Display available members
            self.cursor.execute("SELECT Member_ID, Name FROM Member WHERE Membership_Status = 'Active'")
            members = self.cursor.fetchall()
            if members:
                print("\nActive Members:")
                for member in members[:10]:  # Show first 10
                    print(f"  {member[0]}. {member[1]}")
                if len(members) > 10:
                    print(f"  ... and {len(members) - 10} more")
            
            member_id = input("\nEnter Member ID: ").strip()
            
            # Display available programs
            self.cursor.execute("SELECT Program_ID, Program_Name, Fee FROM Program")
            programs = self.cursor.fetchall()
            if programs:
                print("\nAvailable Programs:")
                for prog in programs:
                    print(f"  {prog[0]}. {prog[1]} (Fee: RM {prog[2]:.2f})")
            
            program_id = input("\nEnter Program ID: ").strip()
            
            enrollment_date = input("Enter enrollment date (YYYY-MM-DD) or press Enter for today: ").strip()
            if not enrollment_date:
                enrollment_date = datetime.now().strftime('%Y-%m-%d')
            
            print("\nEnrollment Status:")
            print("1. Active")
            print("2. Completed")
            print("3. Cancelled")
            status_choice = input("Choose enrollment status (1-3): ").strip()
            status_map = {"1": "Active", "2": "Completed", "3": "Cancelled"}
            enrollment_status = status_map.get(status_choice, "Active")
            
            print("\nPayment Status:")
            print("1. Paid")
            print("2. Pending")
            print("3. Partial")
            payment_choice = input("Choose payment status (1-3): ").strip()
            payment_map = {"1": "Paid", "2": "Pending", "3": "Partial"}
            payment_status = payment_map.get(payment_choice, "Pending")

            query = """INSERT INTO Enrollment (Member_ID, Program_ID, Enrollment_Date, 
                       Enrollment_Status, Payment_Status)
                       VALUES (%s, %s, %s, %s, %s)"""
            
            values = (member_id, program_id, enrollment_date, enrollment_status, payment_status)
            self.cursor.execute(query, values)
            self.connection.commit()
            
            enrollment_id = self.cursor.lastrowid
            print(f"\n✓ Enrollment added successfully!")
            print(f"✓ Enrollment ID: {enrollment_id}")
            print(f"✓ Status: {enrollment_status} / Payment: {payment_status}")
            print("=" * 60)
            
        except Error as e:
            print(f"\n✗ Error adding enrollment: {e}")
            self.connection.rollback()
    
    def update_enrollment(self):
        """Update enrollment information"""
        print("\n" + "=" * 60)
        print(" " * 18 + "UPDATE ENROLLMENT")
        print("=" * 60)
        
        try:
            enrollment_id = input("Enter Enrollment ID to update: ").strip()
            
            query = """SELECT e.Enrollment_ID, m.Name, p.Program_Name, 
                       e.Enrollment_Status, e.Payment_Status
                       FROM Enrollment e
                       JOIN Member m ON e.Member_ID = m.Member_ID
                       JOIN Program p ON e.Program_ID = p.Program_ID
                       WHERE e.Enrollment_ID = %s"""
            self.cursor.execute(query, (enrollment_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"\n✗ Enrollment ID {enrollment_id} not found!")
                return
            
            print(f"\nCurrent Enrollment Details:")
            print(f"  Member: {result[1]}")
            print(f"  Program: {result[2]}")
            print(f"  Enrollment Status: {result[3]}")
            print(f"  Payment Status: {result[4]}")
            
            print("\nWhat would you like to update?")
            print("1. Enrollment Status")
            print("2. Payment Status")
            print("3. Cancel")
            
            choice = input("\nEnter choice (1-3): ").strip()
            
            if choice == '3':
                print("Update cancelled.")
                return
            
            if choice == '1':
                print("\nNew Enrollment Status:")
                print("1. Active")
                print("2. Completed")
                print("3. Cancelled")
                status_choice = input("Choose status (1-3): ").strip()
                status_map = {"1": "Active", "2": "Completed", "3": "Cancelled"}
                new_value = status_map.get(status_choice, "Active")
                query = "UPDATE Enrollment SET Enrollment_Status = %s WHERE Enrollment_ID = %s"
                field = "Enrollment Status"
            elif choice == '2':
                print("\nNew Payment Status:")
                print("1. Paid")
                print("2. Pending")
                print("3. Partial")
                payment_choice = input("Choose status (1-3): ").strip()
                payment_map = {"1": "Paid", "2": "Pending", "3": "Partial"}
                new_value = payment_map.get(payment_choice, "Pending")
                query = "UPDATE Enrollment SET Payment_Status = %s WHERE Enrollment_ID = %s"
                field = "Payment Status"
            else:
                print("✗ Invalid choice!")
                return
            
            self.cursor.execute(query, (new_value, enrollment_id))
            self.connection.commit()
            
            print(f"\n✓ Enrollment ID {enrollment_id} updated successfully!")
            print(f"✓ {field} updated to: {new_value}")
            print("=" * 60)
            
        except Error as e:
            print(f"\n✗ Error updating enrollment: {e}")
            self.connection.rollback()
    
    def delete_enrollment(self):
        """Delete an enrollment"""
        print("\n" + "=" * 60)
        print(" " * 18 + "DELETE ENROLLMENT")
        print("=" * 60)
        
        try:
            enrollment_id = input("Enter Enrollment ID to delete: ").strip()
            
            query = """SELECT e.Enrollment_ID, m.Name, p.Program_Name, e.Enrollment_Status
                       FROM Enrollment e
                       JOIN Member m ON e.Member_ID = m.Member_ID
                       JOIN Program p ON e.Program_ID = p.Program_ID
                       WHERE e.Enrollment_ID = %s"""
            self.cursor.execute(query, (enrollment_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"\n✗ Enrollment ID {enrollment_id} not found!")
                return
            
            print(f"\nEnrollment Details:")
            print(f"  Member: {result[1]}")
            print(f"  Program: {result[2]}")
            print(f"  Status: {result[3]}")
            print("\n⚠ WARNING: This will also delete related payment records!")
            
            confirm = input("\nAre you sure you want to delete this enrollment? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                self.cursor.execute("DELETE FROM Enrollment WHERE Enrollment_ID = %s", (enrollment_id,))
                self.connection.commit()
                print(f"\n✓ Enrollment ID {enrollment_id} deleted successfully!")
                print("=" * 60)
            else:
                print("\n✗ Delete operation cancelled.")
                
        except Error as e:
            print(f"\n✗ Error deleting enrollment: {e}")
            self.connection.rollback()
    
    def view_all_enrollments(self):
        """Display all enrollments in a formatted table"""
        print("\n" + "=" * 120)
        print(" " * 48 + "ALL ENROLLMENTS")
        print("=" * 120)
        
        try:
            query = """SELECT e.Enrollment_ID, m.Name, p.Program_Name, 
                       e.Enrollment_Date, e.Enrollment_Status, e.Payment_Status, p.Category
                       FROM Enrollment e
                       JOIN Member m ON e.Member_ID = m.Member_ID
                       JOIN Program p ON e.Program_ID = p.Program_ID
                       ORDER BY e.Enrollment_Date DESC"""
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if results:
                print(f"\n{'ID':<5} {'Member':<25} {'Program':<25} {'Date':<12} {'Status':<12} {'Payment':<10} {'Category':<15}")
                print("-" * 120)
                
                for row in results:
                    enroll_id = row[0]
                    member = row[1][:24] if row[1] else "N/A"
                    program = row[2][:24] if row[2] else "N/A"
                    date = str(row[3])[:10] if row[3] else "N/A"
                    status = row[4][:11] if row[4] else "N/A"
                    payment = row[5][:9] if row[5] else "N/A"
                    category = row[6][:14] if row[6] else "N/A"
                    
                    print(f"{enroll_id:<5} {member:<25} {program:<25} {date:<12} {status:<12} {payment:<10} {category:<15}")
                
                print(f"\nTotal Enrollments: {len(results)}")
                print("=" * 120)
            else:
                print("\n✗ No enrollments found in the database.")
                print("=" * 120)
                
        except Error as e:
            print(f"\n✗ Error viewing enrollments: {e}")