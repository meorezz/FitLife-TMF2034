"""
Trainer Operations Module
Handles all CRUD operations for Trainers
"""

from mysql.connector import Error


class TrainerOperations:
    """Class to handle trainer-related database operations"""
    
    def __init__(self, db):
        """Initialize with database connection"""
        self.db = db
        self.cursor = db.get_cursor()
        self.connection = db.get_connection()
    
    def add_trainer(self):
        """Add a new trainer to the database"""
        print("\n" + "=" * 60)
        print(" " * 20 + "ADD NEW TRAINER")
        print("=" * 60)
        
        try:
            name = input("Enter trainer full name: ").strip()
            if not name:
                print("✗ Name cannot be empty!")
                return
            
            specialization = input("Enter specialization: ").strip()
            cert_level = input("Enter certification level: ").strip()
            contact = input("Enter contact details: ").strip()

            query = """INSERT INTO Trainer (Full_Name, Specialization, Certification_Level, Contact_Details)
                       VALUES (%s, %s, %s, %s)"""
            
            values = (name, specialization, cert_level, contact)
            self.cursor.execute(query, values)
            self.connection.commit()
            
            trainer_id = self.cursor.lastrowid
            print(f"\n✓ Trainer '{name}' added successfully!")
            print(f"✓ Trainer ID: {trainer_id}")
            print("=" * 60)
            
        except Error as e:
            print(f"\n✗ Error adding trainer: {e}")
            self.connection.rollback()
    
    def update_trainer(self):
        """Update existing trainer information"""
        print("\n" + "=" * 60)
        print(" " * 20 + "UPDATE TRAINER")
        print("=" * 60)
        
        try:
            trainer_id = input("Enter Trainer ID to update: ").strip()
            
            self.cursor.execute("SELECT Full_Name, Specialization FROM Trainer WHERE Trainer_ID = %s", 
                              (trainer_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"\n✗ Trainer ID {trainer_id} not found!")
                return
            
            print(f"\nCurrent Trainer: {result[0]}")
            print(f"Specialization: {result[1]}")
            print("\nWhat would you like to update?")
            print("1. Full Name")
            print("2. Specialization")
            print("3. Certification Level")
            print("4. Contact Details")
            print("5. Cancel")
            
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '5':
                print("Update cancelled.")
                return
            
            if choice == '1':
                new_value = input("Enter new full name: ").strip()
                query = "UPDATE Trainer SET Full_Name = %s WHERE Trainer_ID = %s"
                field = "Full Name"
            elif choice == '2':
                new_value = input("Enter new specialization: ").strip()
                query = "UPDATE Trainer SET Specialization = %s WHERE Trainer_ID = %s"
                field = "Specialization"
            elif choice == '3':
                new_value = input("Enter new certification level: ").strip()
                query = "UPDATE Trainer SET Certification_Level = %s WHERE Trainer_ID = %s"
                field = "Certification Level"
            elif choice == '4':
                new_value = input("Enter new contact details: ").strip()
                query = "UPDATE Trainer SET Contact_Details = %s WHERE Trainer_ID = %s"
                field = "Contact Details"
            else:
                print("✗ Invalid choice!")
                return
            
            self.cursor.execute(query, (new_value, trainer_id))
            self.connection.commit()
            
            print(f"\n✓ Trainer ID {trainer_id} updated successfully!")
            print(f"✓ {field} updated to: {new_value}")
            print("=" * 60)
            
        except Error as e:
            print(f"\n✗ Error updating trainer: {e}")
            self.connection.rollback()
    
    def delete_trainer(self):
        """Delete a trainer from the database"""
        print("\n" + "=" * 60)
        print(" " * 20 + "DELETE TRAINER")
        print("=" * 60)
        
        try:
            trainer_id = input("Enter Trainer ID to delete: ").strip()
            
            self.cursor.execute("SELECT Full_Name, Specialization FROM Trainer WHERE Trainer_ID = %s", 
                              (trainer_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"\n✗ Trainer ID {trainer_id} not found!")
                return
            
            print(f"\nTrainer Details:")
            print(f"  Name: {result[0]}")
            print(f"  Specialization: {result[1]}")
            print("\n⚠ WARNING: This will also affect all classes assigned to this trainer!")
            
            confirm = input("\nAre you sure you want to delete this trainer? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                self.cursor.execute("DELETE FROM Trainer WHERE Trainer_ID = %s", (trainer_id,))
                self.connection.commit()
                print(f"\n✓ Trainer ID {trainer_id} deleted successfully!")
                print("=" * 60)
            else:
                print("\n✗ Delete operation cancelled.")
                
        except Error as e:
            print(f"\n✗ Error deleting trainer: {e}")
            self.connection.rollback()
    
    def view_all_trainers(self):
        """Display all trainers in a formatted table"""
        print("\n" + "=" * 100)
        print(" " * 40 + "ALL TRAINERS")
        print("=" * 100)
        
        try:
            query = """SELECT Trainer_ID, Full_Name, Specialization, 
                       Certification_Level, Contact_Details 
                       FROM Trainer ORDER BY Trainer_ID"""
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if results:
                print(f"\n{'ID':<5} {'Name':<30} {'Specialization':<25} {'Certification':<20} {'Contact':<15}")
                print("-" * 100)
                
                for row in results:
                    trainer_id = row[0]
                    name = row[1][:29] if row[1] else "N/A"
                    spec = row[2][:24] if row[2] else "N/A"
                    cert = row[3][:19] if row[3] else "N/A"
                    contact = row[4][:14] if row[4] else "N/A"
                    
                    print(f"{trainer_id:<5} {name:<30} {spec:<25} {cert:<20} {contact:<15}")
                
                print(f"\nTotal Trainers: {len(results)}")
                print("=" * 100)
            else:
                print("\n✗ No trainers found in the database.")
                print("=" * 100)
                
        except Error as e:
            print(f"\n✗ Error viewing trainers: {e}")
    
    def search_trainer(self):
        """Search for trainers by name or specialization"""
        print("\n" + "=" * 60)
        print(" " * 20 + "SEARCH TRAINER")
        print("=" * 60)
        
        try:
            print("\nSearch by:")
            print("1. Name")
            print("2. Specialization")
            choice = input("Enter choice (1-2): ").strip()
            
            if choice == '1':
                search_term = input("Enter trainer name to search: ").strip()
                query = """SELECT Trainer_ID, Full_Name, Specialization, Certification_Level 
                           FROM Trainer WHERE Full_Name LIKE %s"""
            elif choice == '2':
                search_term = input("Enter specialization to search: ").strip()
                query = """SELECT Trainer_ID, Full_Name, Specialization, Certification_Level 
                           FROM Trainer WHERE Specialization LIKE %s"""
            else:
                print("✗ Invalid choice!")
                return
            
            self.cursor.execute(query, (f"%{search_term}%",))
            results = self.cursor.fetchall()
            
            if results:
                print(f"\n{'ID':<5} {'Name':<30} {'Specialization':<25} {'Certification':<20}")
                print("-" * 85)
                
                for row in results:
                    print(f"{row[0]:<5} {row[1]:<30} {row[2]:<25} {row[3]:<20}")
                
                print(f"\nFound {len(results)} trainer(s)")
                print("=" * 60)
            else:
                print(f"\n✗ No trainers found matching '{search_term}'")
                print("=" * 60)
                
        except Error as e:
            print(f"\n✗ Error searching trainers: {e}")