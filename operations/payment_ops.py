"""
Payment Operations Module
Handles all CRUD operations for Payments
"""

from mysql.connector import Error
from datetime import datetime
import random
import string


class PaymentOperations:
    """Class to handle payment-related database operations"""
    
    def __init__(self, db):
        """Initialize with database connection"""
        self.db = db
        self.cursor = db.get_cursor()
        self.connection = db.get_connection()
    
    def generate_reference_no(self):
        """Generate a unique reference number"""
        timestamp = datetime.now().strftime('%Y%m%d')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"REF{timestamp}-{random_str}"
    
    def add_payment(self):
        """Add a new payment record"""
        print("\n" + "=" * 60)
        print(" " * 18 + "ADD NEW PAYMENT")
        print("=" * 60)
        
        try:
            # Display pending enrollments
            query = """SELECT e.Enrollment_ID, m.Name, p.Program_Name, p.Fee, e.Payment_Status
                       FROM Enrollment e
                       JOIN Member m ON e.Member_ID = m.Member_ID
                       JOIN Program p ON e.Program_ID = p.Program_ID
                       WHERE e.Payment_Status IN ('Pending', 'Partial')"""
            self.cursor.execute(query)
            pending = self.cursor.fetchall()
            
            if pending:
                print("\nPending/Partial Payments:")
                for enroll in pending:
                    print(f"  Enrollment ID {enroll[0]}: {enroll[1]} - {enroll[2]} (RM {enroll[3]:.2f}) [{enroll[4]}]")
            
            member_id = input("\nEnter Member ID: ").strip()
            enrollment_id = input("Enter Enrollment ID: ").strip()
            
            # Get program fee for reference
            self.cursor.execute("""SELECT p.Fee FROM Enrollment e 
                                 JOIN Program p ON e.Program_ID = p.Program_ID 
                                 WHERE e.Enrollment_ID = %s""", (enrollment_id,))
            fee_result = self.cursor.fetchone()
            if fee_result:
                print(f"\nProgram Fee: RM {fee_result[0]:.2f}")
            
            amount = input("Enter payment amount: RM ").strip()
            try:
                amount = float(amount)
            except ValueError:
                print("✗ Amount must be a valid number!")
                return
            
            payment_date = input("Enter payment date (YYYY-MM-DD) or press Enter for today: ").strip()
            if not payment_date:
                payment_date = datetime.now().strftime('%Y-%m-%d')
            
            print("\nPayment Type:")
            print("1. Cash")
            print("2. Credit/Debit Card")
            print("3. Bank Transfer")
            print("4. Online Payment")
            type_choice = input("Choose payment type (1-4): ").strip()
            type_map = {"1": "Cash", "2": "Card", "3": "Bank Transfer", "4": "Online"}
            payment_type = type_map.get(type_choice, "Cash")
            
            reference_no = input("Enter reference number or press Enter for auto-generate: ").strip()
            if not reference_no:
                reference_no = self.generate_reference_no()

            query = """INSERT INTO Payment (Member_ID, Enrollment_ID, Amount, Payment_Date, 
                       Payment_Type, Reference_No)
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            
            values = (member_id, enrollment_id, amount, payment_date, payment_type, reference_no)
            self.cursor.execute(query, values)
            self.connection.commit()
            
            payment_id = self.cursor.lastrowid
            print(f"\n✓ Payment recorded successfully!")
            print(f"✓ Payment ID: {payment_id}")
            print(f"✓ Amount: RM {amount:.2f}")
            print(f"✓ Reference: {reference_no}")
            print("=" * 60)
            
        except Error as e:
            print(f"\n✗ Error adding payment: {e}")
            self.connection.rollback()
    
    def update_payment(self):
        """Update payment information"""
        print("\n" + "=" * 60)
        print(" " * 18 + "UPDATE PAYMENT")
        print("=" * 60)
        
        try:
            payment_id = input("Enter Payment ID to update: ").strip()
            
            query = """SELECT p.Payment_ID, m.Name, p.Amount, p.Payment_Type, p.Reference_No
                       FROM Payment p
                       JOIN Member m ON p.Member_ID = m.Member_ID
                       WHERE p.Payment_ID = %s"""
            self.cursor.execute(query, (payment_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"\n✗ Payment ID {payment_id} not found!")
                return
            
            print(f"\nCurrent Payment Details:")
            print(f"  Member: {result[1]}")
            print(f"  Amount: RM {result[2]:.2f}")
            print(f"  Type: {result[3]}")
            print(f"  Reference: {result[4]}")
            
            print("\nWhat would you like to update?")
            print("1. Amount")
            print("2. Payment Type")
            print("3. Reference Number")
            print("4. Cancel")
            
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == '4':
                print("Update cancelled.")
                return
            
            if choice == '1':
                new_value = input("Enter new amount: RM ").strip()
                try:
                    new_value = float(new_value)
                except ValueError:
                    print("✗ Amount must be a valid number!")
                    return
                query = "UPDATE Payment SET Amount = %s WHERE Payment_ID = %s"
                field = "Amount"
            elif choice == '2':
                print("\nPayment Type:")
                print("1. Cash")
                print("2. Credit/Debit Card")
                print("3. Bank Transfer")
                print("4. Online Payment")
                type_choice = input("Choose payment type (1-4): ").strip()
                type_map = {"1": "Cash", "2": "Card", "3": "Bank Transfer", "4": "Online"}
                new_value = type_map.get(type_choice, "Cash")
                query = "UPDATE Payment SET Payment_Type = %s WHERE Payment_ID = %s"
                field = "Payment Type"
            elif choice == '3':
                new_value = input("Enter new reference number: ").strip()
                query = "UPDATE Payment SET Reference_No = %s WHERE Payment_ID = %s"
                field = "Reference Number"
            else:
                print("✗ Invalid choice!")
                return
            
            self.cursor.execute(query, (new_value, payment_id))
            self.connection.commit()
            
            print(f"\n✓ Payment ID {payment_id} updated successfully!")
            print(f"✓ {field} updated to: {new_value}")
            print("=" * 60)
            
        except Error as e:
            print(f"\n✗ Error updating payment: {e}")
            self.connection.rollback()
    
    def delete_payment(self):
        """Delete a payment record"""
        print("\n" + "=" * 60)
        print(" " * 18 + "DELETE PAYMENT")
        print("=" * 60)
        
        try:
            payment_id = input("Enter Payment ID to delete: ").strip()
            
            query = """SELECT p.Payment_ID, m.Name, p.Amount, p.Reference_No
                       FROM Payment p
                       JOIN Member m ON p.Member_ID = m.Member_ID
                       WHERE p.Payment_ID = %s"""
            self.cursor.execute(query, (payment_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"\n✗ Payment ID {payment_id} not found!")
                return
            
            print(f"\nPayment Details:")
            print(f"  Member: {result[1]}")
            print(f"  Amount: RM {result[2]:.2f}")
            print(f"  Reference: {result[3]}")
            
            confirm = input("\nAre you sure you want to delete this payment? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                self.cursor.execute("DELETE FROM Payment WHERE Payment_ID = %s", (payment_id,))
                self.connection.commit()
                print(f"\n✓ Payment ID {payment_id} deleted successfully!")
                print("=" * 60)
            else:
                print("\n✗ Delete operation cancelled.")
                
        except Error as e:
            print(f"\n✗ Error deleting payment: {e}")
            self.connection.rollback()
    
    def view_all_payments(self):
        """Display all payments in a formatted table"""
        print("\n" + "=" * 120)
        print(" " * 50 + "ALL PAYMENTS")
        print("=" * 120)
        
        try:
            query = """SELECT p.Payment_ID, m.Name, p.Amount, p.Payment_Date, 
                       p.Payment_Type, p.Reference_No
                       FROM Payment p
                       JOIN Member m ON p.Member_ID = m.Member_ID
                       ORDER BY p.Payment_Date DESC"""
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if results:
                print(f"\n{'ID':<5} {'Member':<30} {'Amount (RM)':<12} {'Date':<12} {'Type':<15} {'Reference':<25}")
                print("-" * 120)
                
                total_amount = 0
                for row in results:
                    payment_id = row[0]
                    member = row[1][:29] if row[1] else "N/A"
                    amount = f"{row[2]:.2f}" if row[2] else "0.00"
                    date = str(row[3])[:10] if row[3] else "N/A"
                    p_type = row[4][:14] if row[4] else "N/A"
                    reference = row[5][:24] if row[5] else "N/A"
                    
                    print(f"{payment_id:<5} {member:<30} {amount:<12} {date:<12} {p_type:<15} {reference:<25}")
                    total_amount += float(row[2]) if row[2] else 0
                
                print("-" * 120)
                print(f"Total Payments: {len(results)}")
                print(f"Total Amount Collected: RM {total_amount:.2f}")
                print("=" * 120)
            else:
                print("\n✗ No payments found in the database.")
                print("=" * 120)
                
        except Error as e:
            print(f"\n✗ Error viewing payments: {e}")