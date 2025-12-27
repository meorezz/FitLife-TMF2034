"""
Program Operations Module
Handles all CRUD operations for Programs
"""

from mysql.connector import Error


class ProgramOperations:
    """Class to handle program-related database operations"""
    
    def __init__(self, db):
        """Initialize with database connection"""
        self.db = db
        self.cursor = db.get_cursor()
        self.connection = db.get_connection()
    
    def add_program(self):
        """Add a new program to the database"""
        print("\n" + "=" * 60)
        print(" " * 20 + "ADD NEW PROGRAM")
        print("=" * 60)
        
        try:
            program_name = input("Enter program name: ").strip()
            if not program_name:
                print("✗ Program name cannot be empty!")
                return
            
            category = input("Enter category: ").strip()
            
            duration = input("Enter duration in weeks: ").strip()
            if not duration.isdigit():
                print("✗ Duration must be a number!")
                return
            
            fee = input("Enter program fee (RM): ").strip()
            try:
                fee = float(fee)
            except ValueError:
                print("✗ Fee must be a valid number!")
                return

            query = """INSERT INTO Program (Program_Name, Category, Duration_Weeks, Fee)
                       VALUES (%s, %s, %s, %s)"""
            
            values = (program_name, category, duration, fee)
            self.cursor.execute(query, values)
            self.connection.commit()
            
            program_id = self.cursor.lastrowid
            print(f"\n✓ Program '{program_name}' added successfully!")
            print(f"✓ Program ID: {program_id}")
            print(f"✓ Fee: RM {fee:.2f}")
            print("=" * 60)
            
        except Error as e:
            print(f"\n✗ Error adding program: {e}")
            self.connection.rollback()
    
    def update_program(self):
        """Update existing program information"""
        print("\n" + "=" * 60)
        print(" " * 20 + "UPDATE PROGRAM")
        print("=" * 60)
        
        try:
            program_id = input("Enter Program ID to update: ").strip()
            
            self.cursor.execute("SELECT Program_Name, Category, Fee FROM Program WHERE Program_ID = %s", 
                              (program_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"\n✗ Program ID {program_id} not found!")
                return
            
            print(f"\nCurrent Program: {result[0]}")
            print(f"Category: {result[1]}")
            print(f"Fee: RM {result[2]:.2f}")
            print("\nWhat would you like to update?")
            print("1. Program Name")
            print("2. Category")
            print("3. Duration (Weeks)")
            print("4. Fee")
            print("5. Cancel")
            
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '5':
                print("Update cancelled.")
                return
            
            if choice == '1':
                new_value = input("Enter new program name: ").strip()
                query = "UPDATE Program SET Program_Name = %s WHERE Program_ID = %s"
                field = "Program Name"
            elif choice == '2':
                new_value = input("Enter new category: ").strip()
                query = "UPDATE Program SET Category = %s WHERE Program_ID = %s"
                field = "Category"
            elif choice == '3':
                new_value = input("Enter new duration (weeks): ").strip()
                if not new_value.isdigit():
                    print("✗ Duration must be a number!")
                    return
                query = "UPDATE Program SET Duration_Weeks = %s WHERE Program_ID = %s"
                field = "Duration"
            elif choice == '4':
                new_value = input("Enter new fee (RM): ").strip()
                try:
                    new_value = float(new_value)
                except ValueError:
                    print("✗ Fee must be a valid number!")
                    return
                query = "UPDATE Program SET Fee = %s WHERE Program_ID = %s"
                field = "Fee"
            else:
                print("✗ Invalid choice!")
                return
            
            self.cursor.execute(query, (new_value, program_id))
            self.connection.commit()
            
            print(f"\n✓ Program ID {program_id} updated successfully!")
            print(f"✓ {field} updated to: {new_value}")
            print("=" * 60)
            
        except Error as e:
            print(f"\n✗ Error updating program: {e}")
            self.connection.rollback()
    
    def delete_program(self):
        """Delete a program from the database"""
        print("\n" + "=" * 60)
        print(" " * 20 + "DELETE PROGRAM")
        print("=" * 60)
        
        try:
            program_id = input("Enter Program ID to delete: ").strip()
            
            self.cursor.execute("SELECT Program_Name, Category, Fee FROM Program WHERE Program_ID = %s", 
                              (program_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"\n✗ Program ID {program_id} not found!")
                return
            
            print(f"\nProgram Details:")
            print(f"  Name: {result[0]}")
            print(f"  Category: {result[1]}")
            print(f"  Fee: RM {result[2]:.2f}")
            print("\n⚠ WARNING: This will also affect all enrollments and classes for this program!")
            
            confirm = input("\nAre you sure you want to delete this program? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                self.cursor.execute("DELETE FROM Program WHERE Program_ID = %s", (program_id,))
                self.connection.commit()
                print(f"\n✓ Program ID {program_id} deleted successfully!")
                print("=" * 60)
            else:
                print("\n✗ Delete operation cancelled.")
                
        except Error as e:
            print(f"\n✗ Error deleting program: {e}")
            self.connection.rollback()
    
    def view_all_programs(self):
        """Display all programs in a formatted table"""
        print("\n" + "=" * 100)
        print(" " * 40 + "ALL PROGRAMS")
        print("=" * 100)
        
        try:
            query = """SELECT Program_ID, Program_Name, Category, 
                       Duration_Weeks, Fee 
                       FROM Program ORDER BY Program_ID"""
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if results:
                print(f"\n{'ID':<5} {'Program Name':<35} {'Category':<25} {'Duration':<10} {'Fee (RM)':<10}")
                print("-" * 100)
                
                for row in results:
                    program_id = row[0]
                    name = row[1][:34] if row[1] else "N/A"
                    category = row[2][:24] if row[2] else "N/A"
                    duration = f"{row[3]} weeks" if row[3] else "N/A"
                    fee = f"{row[4]:.2f}" if row[4] else "0.00"
                    
                    print(f"{program_id:<5} {name:<35} {category:<25} {duration:<10} {fee:<10}")
                
                print(f"\nTotal Programs: {len(results)}")
                print("=" * 100)
            else:
                print("\n✗ No programs found in the database.")
                print("=" * 100)
                
        except Error as e:
            print(f"\n✗ Error viewing programs: {e}")
    
    def search_program(self):
        """Search for programs by name or category"""
        print("\n" + "=" * 60)
        print(" " * 20 + "SEARCH PROGRAM")
        print("=" * 60)
        
        try:
            print("\nSearch by:")
            print("1. Program Name")
            print("2. Category")
            choice = input("Enter choice (1-2): ").strip()
            
            if choice == '1':
                search_term = input("Enter program name to search: ").strip()
                query = """SELECT Program_ID, Program_Name, Category, Duration_Weeks, Fee 
                           FROM Program WHERE Program_Name LIKE %s"""
            elif choice == '2':
                search_term = input("Enter category to search: ").strip()
                query = """SELECT Program_ID, Program_Name, Category, Duration_Weeks, Fee 
                           FROM Program WHERE Category LIKE %s"""
            else:
                print("✗ Invalid choice!")
                return
            
            self.cursor.execute(query, (f"%{search_term}%",))
            results = self.cursor.fetchall()
            
            if results:
                print(f"\n{'ID':<5} {'Program Name':<35} {'Category':<20} {'Duration':<10} {'Fee (RM)':<10}")
                print("-" * 85)
                
                for row in results:
                    duration = f"{row[3]} weeks" if row[3] else "N/A"
                    fee = f"{row[4]:.2f}" if row[4] else "0.00"
                    print(f"{row[0]:<5} {row[1]:<35} {row[2]:<20} {duration:<10} {fee:<10}")
                
                print(f"\nFound {len(results)} program(s)")
                print("=" * 60)
            else:
                print(f"\n✗ No programs found matching '{search_term}'")
                print("=" * 60)
                
        except Error as e:
            print(f"\n✗ Error searching programs: {e}")