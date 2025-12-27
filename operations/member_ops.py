"""
Member Operations Module
Handles all CRUD operations for Members
"""

from mysql.connector import Error


class MemberOperations:
    """Class to handle member-related database operations"""
    
    def __init__(self, db):
        """Initialize with database connection"""
        self.db = db
        self.cursor = db.get_cursor()
        self.connection = db.get_connection()
    
    def add_member(self):
        """Add a new member to the database"""
        print("\n" + "=" * 60)
        print(" " * 20 + "ADD NEW MEMBER")
        print("=" * 60)
        
        try:
            # Collect member information
            name = input("Enter member name: ").strip()
            if not name:
                print("✗ Name cannot be empty!")
                return
            
            contact = input("Enter contact details (phone): ").strip()
            email = input("Enter email: ").strip()
            dob = input("Enter date of birth (YYYY-MM-DD): ").strip()
            
            gender = input("Enter gender (M/F): ").strip().upper()
            while gender not in ['M', 'F']:
                print("✗ Invalid gender! Please enter M or F.")
                gender = input("Enter gender (M/F): ").strip().upper()
            
            print("\nMembership Types:")
            print("1. Standard")
            print("2. Premium")
            mem_choice = input("Choose membership type (1-2): ").strip()
            mem_type = "Standard" if mem_choice == "1" else "Premium"
            
            mem_start = input("Enter membership start date (YYYY-MM-DD): ").strip()
            mem_end = input("Enter membership end date (YYYY-MM-DD): ").strip()
            
            print("\nMembership Status:")
            print("1. Active")
            print("2. Inactive")
            print("3. Expired")
            status_choice = input("Choose status (1-3): ").strip()
            status_map = {"1": "Active", "2": "Inactive", "3": "Expired"}
            mem_status = status_map.get(status_choice, "Active")
            
            # Insert into database
            query = """INSERT INTO Member (Name, Contact_Details, Email, Date_of_Birth, 
                       Gender, Membership_Type, Membership_Start, Membership_End, Membership_Status)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            values = (name, contact, email, dob, gender, mem_type, mem_start, mem_end, mem_status)
            self.cursor.execute(query, values)
            self.connection.commit()
            
            member_id = self.cursor.lastrowid
            print(f"\n✓ Member '{name}' added successfully!")
            print(f"✓ Member ID: {member_id}")
            print("=" * 60)
            
        except Error as e:
            print(f"\n✗ Error adding member: {e}")
            self.connection.rollback()
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
    
    def update_member(self):
        """Update existing member information"""
        print("\n" + "=" * 60)
        print(" " * 20 + "UPDATE MEMBER")
        print("=" * 60)
        
        try:
            member_id = input("Enter Member ID to update: ").strip()
            
            # Check if member exists
            self.cursor.execute("SELECT Name, Membership_Type FROM Member WHERE Member_ID = %s", 
                              (member_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"\n✗ Member ID {member_id} not found!")
                return
            
            print(f"\nCurrent Member: {result[0]} ({result[1]} Membership)")
            print("\nWhat would you like to update?")
            print("1. Contact Details")
            print("2. Email")
            print("3. Membership Type")
            print("4. Membership Status")
            print("5. Membership End Date")
            print("6. Cancel")
            
            choice = input("\nEnter choice (1-6): ").strip()
            
            if choice == '6':
                print("Update cancelled.")
                return
            
            if choice == '1':
                new_value = input("Enter new contact details: ").strip()
                query = "UPDATE Member SET Contact_Details = %s WHERE Member_ID = %s"
                field = "Contact Details"
            elif choice == '2':
                new_value = input("Enter new email: ").strip()
                query = "UPDATE Member SET Email = %s WHERE Member_ID = %s"
                field = "Email"
            elif choice == '3':
                print("1. Standard")
                print("2. Premium")
                mem_choice = input("Choose new membership type (1-2): ").strip()
                new_value = "Standard" if mem_choice == "1" else "Premium"
                query = "UPDATE Member SET Membership_Type = %s WHERE Member_ID = %s"
                field = "Membership Type"
            elif choice == '4':
                print("1. Active")
                print("2. Inactive")
                print("3. Expired")
                status_choice = input("Choose new status (1-3): ").strip()
                status_map = {"1": "Active", "2": "Inactive", "3": "Expired"}
                new_value = status_map.get(status_choice, "Active")
                query = "UPDATE Member SET Membership_Status = %s WHERE Member_ID = %s"
                field = "Membership Status"
            elif choice == '5':
                new_value = input("Enter new membership end date (YYYY-MM-DD): ").strip()
                query = "UPDATE Member SET Membership_End = %s WHERE Member_ID = %s"
                field = "Membership End Date"
            else:
                print("✗ Invalid choice!")
                return
            
            self.cursor.execute(query, (new_value, member_id))
            self.connection.commit()
            
            print(f"\n✓ Member ID {member_id} updated successfully!")
            print(f"✓ {field} updated to: {new_value}")
            print("=" * 60)
            
        except Error as e:
            print(f"\n✗ Error updating member: {e}")
            self.connection.rollback()
    
    def delete_member(self):
        """Delete a member from the database"""
        print("\n" + "=" * 60)
        print(" " * 20 + "DELETE MEMBER")
        print("=" * 60)
        
        try:
            member_id = input("Enter Member ID to delete: ").strip()
            
            # Check if member exists
            self.cursor.execute("SELECT Name, Email FROM Member WHERE Member_ID = %s", 
                              (member_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"\n✗ Member ID {member_id} not found!")
                return
            
            print(f"\nMember Details:")
            print(f"  Name: {result[0]}")
            print(f"  Email: {result[1]}")
            print("\n⚠ WARNING: This will also delete all related enrollments and payments!")
            
            confirm = input("\nAre you sure you want to delete this member? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                self.cursor.execute("DELETE FROM Member WHERE Member_ID = %s", (member_id,))
                self.connection.commit()
                print(f"\n✓ Member ID {member_id} deleted successfully!")
                print("=" * 60)
            else:
                print("\n✗ Delete operation cancelled.")
                
        except Error as e:
            print(f"\n✗ Error deleting member: {e}")
            self.connection.rollback()
    
    def view_all_members(self):
        """Display all members in a formatted table"""
        print("\n" + "=" * 120)
        print(" " * 50 + "ALL MEMBERS")
        print("=" * 120)
        
        try:
            query = """SELECT Member_ID, Name, Email, Contact_Details, 
                       Membership_Type, Membership_Status, Membership_End 
                       FROM Member ORDER BY Member_ID"""
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if results:
                print(f"\n{'ID':<5} {'Name':<25} {'Email':<30} {'Contact':<15} {'Type':<10} {'Status':<10} {'End Date':<12}")
                print("-" * 120)
                
                for row in results:
                    member_id = row[0]
                    name = row[1][:24] if row[1] else "N/A"
                    email = row[2][:29] if row[2] else "N/A"
                    contact = row[3][:14] if row[3] else "N/A"
                    mem_type = row[4][:9] if row[4] else "N/A"
                    status = row[5][:9] if row[5] else "N/A"
                    end_date = str(row[6])[:10] if row[6] else "N/A"
                    
                    print(f"{member_id:<5} {name:<25} {email:<30} {contact:<15} {mem_type:<10} {status:<10} {end_date:<12}")
                
                print(f"\nTotal Members: {len(results)}")
                print("=" * 120)
            else:
                print("\n✗ No members found in the database.")
                print("=" * 120)
                
        except Error as e:
            print(f"\n✗ Error viewing members: {e}")
    
    def search_member(self):
        """Search for members by name"""
        print("\n" + "=" * 60)
        print(" " * 20 + "SEARCH MEMBER")
        print("=" * 60)
        
        try:
            search_term = input("Enter member name to search: ").strip()
            
            query = """SELECT Member_ID, Name, Email, Membership_Type, Membership_Status 
                       FROM Member WHERE Name LIKE %s"""
            self.cursor.execute(query, (f"%{search_term}%",))
            results = self.cursor.fetchall()
            
            if results:
                print(f"\n{'ID':<5} {'Name':<30} {'Email':<30} {'Type':<10} {'Status':<10}")
                print("-" * 90)
                
                for row in results:
                    print(f"{row[0]:<5} {row[1]:<30} {row[2]:<30} {row[3]:<10} {row[4]:<10}")
                
                print(f"\nFound {len(results)} member(s)")
                print("=" * 60)
            else:
                print(f"\n✗ No members found matching '{search_term}'")
                print("=" * 60)
                
        except Error as e:
            print(f"\n✗ Error searching members: {e}")