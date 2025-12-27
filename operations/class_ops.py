"""
Class Operations Module
Handles all CRUD operations for Classes
"""

from mysql.connector import Error


class ClassOperations:
    """Class to handle class schedule-related database operations"""
    
    def __init__(self, db):
        """Initialize with database connection"""
        self.db = db
        self.cursor = db.get_cursor()
        self.connection = db.get_connection()
    
    def add_class(self):
        """Add a new class schedule"""
        print("\n" + "=" * 60)
        print(" " * 18 + "ADD NEW CLASS SCHEDULE")
        print("=" * 60)
        
        try:
            # Display available programs
            self.cursor.execute("SELECT Program_ID, Program_Name FROM Program")
            programs = self.cursor.fetchall()
            if programs:
                print("\nAvailable Programs:")
                for prog in programs:
                    print(f"  {prog[0]}. {prog[1]}")
            
            program_id = input("\nEnter Program ID: ").strip()
            
            # Display available trainers
            self.cursor.execute("SELECT Trainer_ID, Full_Name FROM Trainer")
            trainers = self.cursor.fetchall()
            if trainers:
                print("\nAvailable Trainers:")
                for trainer in trainers:
                    print(f"  {trainer[0]}. {trainer[1]}")
            
            trainer_id = input("\nEnter Trainer ID: ").strip()
            
            schedule_datetime = input("Enter schedule date and time (YYYY-MM-DD HH:MM:SS): ").strip()
            room = input("Enter room: ").strip()
            
            max_capacity = input("Enter maximum capacity: ").strip()
            if not max_capacity.isdigit():
                print("✗ Capacity must be a number!")
                return

            query = """INSERT INTO Class (Program_ID, Trainer_ID, Schedule_DateTime, 
                       Room, Max_Capacity)
                       VALUES (%s, %s, %s, %s, %s)"""
            
            values = (program_id, trainer_id, schedule_datetime, room, max_capacity)
            self.cursor.execute(query, values)
            self.connection.commit()
            
            class_id = self.cursor.lastrowid
            print(f"\n✓ Class scheduled successfully!")
            print(f"✓ Class ID: {class_id}")
            print(f"✓ Room: {room}")
            print("=" * 60)
            
        except Error as e:
            print(f"\n✗ Error adding class: {e}")
            self.connection.rollback()
    
    def update_class(self):
        """Update class information"""
        print("\n" + "=" * 60)
        print(" " * 20 + "UPDATE CLASS")
        print("=" * 60)
        
        try:
            class_id = input("Enter Class ID to update: ").strip()
            
            query = """SELECT c.Class_ID, p.Program_Name, t.Full_Name, 
                       c.Schedule_DateTime, c.Room, c.Max_Capacity
                       FROM Class c
                       JOIN Program p ON c.Program_ID = p.Program_ID
                       JOIN Trainer t ON c.Trainer_ID = t.Trainer_ID
                       WHERE c.Class_ID = %s"""
            self.cursor.execute(query, (class_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"\n✗ Class ID {class_id} not found!")
                return
            
            print(f"\nCurrent Class Details:")
            print(f"  Program: {result[1]}")
            print(f"  Trainer: {result[2]}")
            print(f"  Schedule: {result[3]}")
            print(f"  Room: {result[4]}")
            print(f"  Capacity: {result[5]}")
            
            print("\nWhat would you like to update?")
            print("1. Schedule Date/Time")
            print("2. Room")
            print("3. Max Capacity")
            print("4. Trainer")
            print("5. Cancel")
            
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '5':
                print("Update cancelled.")
                return
            
            if choice == '1':
                new_value = input("Enter new schedule (YYYY-MM-DD HH:MM:SS): ").strip()
                query = "UPDATE Class SET Schedule_DateTime = %s WHERE Class_ID = %s"
                field = "Schedule"
            elif choice == '2':
                new_value = input("Enter new room: ").strip()
                query = "UPDATE Class SET Room = %s WHERE Class_ID = %s"
                field = "Room"
            elif choice == '3':
                new_value = input("Enter new max capacity: ").strip()
                if not new_value.isdigit():
                    print("✗ Capacity must be a number!")
                    return
                query = "UPDATE Class SET Max_Capacity = %s WHERE Class_ID = %s"
                field = "Max Capacity"
            elif choice == '4':
                self.cursor.execute("SELECT Trainer_ID, Full_Name FROM Trainer")
                trainers = self.cursor.fetchall()
                if trainers:
                    print("\nAvailable Trainers:")
                    for trainer in trainers:
                        print(f"  {trainer[0]}. {trainer[1]}")
                
                new_value = input("\nEnter new Trainer ID: ").strip()
                query = "UPDATE Class SET Trainer_ID = %s WHERE Class_ID = %s"
                field = "Trainer"
            else:
                print("✗ Invalid choice!")
                return
            
            self.cursor.execute(query, (new_value, class_id))
            self.connection.commit()
            
            print(f"\n✓ Class ID {class_id} updated successfully!")
            print(f"✓ {field} updated")
            print("=" * 60)
            
        except Error as e:
            print(f"\n✗ Error updating class: {e}")
            self.connection.rollback()
    
    def delete_class(self):
        """Delete a class schedule"""
        print("\n" + "=" * 60)
        print(" " * 20 + "DELETE CLASS")
        print("=" * 60)
        
        try:
            class_id = input("Enter Class ID to delete: ").strip()
            
            query = """SELECT c.Class_ID, p.Program_Name, c.Schedule_DateTime, c.Room
                       FROM Class c
                       JOIN Program p ON c.Program_ID = p.Program_ID
                       WHERE c.Class_ID = %s"""
            self.cursor.execute(query, (class_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print(f"\n✗ Class ID {class_id} not found!")
                return
            
            print(f"\nClass Details:")
            print(f"  Program: {result[1]}")
            print(f"  Schedule: {result[2]}")
            print(f"  Room: {result[3]}")
            
            confirm = input("\nAre you sure you want to delete this class? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                self.cursor.execute("DELETE FROM Class WHERE Class_ID = %s", (class_id,))
                self.connection.commit()
                print(f"\n✓ Class ID {class_id} deleted successfully!")
                print("=" * 60)
            else:
                print("\n✗ Delete operation cancelled.")
                
        except Error as e:
            print(f"\n✗ Error deleting class: {e}")
            self.connection.rollback()
    
    def view_all_classes(self):
        """Display all classes in a formatted table"""
        print("\n" + "=" * 120)
        print(" " * 50 + "ALL CLASSES")
        print("=" * 120)
        
        try:
            query = """SELECT c.Class_ID, p.Program_Name, t.Full_Name, 
                       c.Schedule_DateTime, c.Room, c.Max_Capacity, p.Category
                       FROM Class c
                       JOIN Program p ON c.Program_ID = p.Program_ID
                       JOIN Trainer t ON c.Trainer_ID = t.Trainer_ID
                       ORDER BY c.Schedule_DateTime"""
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            if results:
                print(f"\n{'ID':<5} {'Program':<25} {'Trainer':<20} {'Schedule':<20} {'Room':<12} {'Capacity':<8} {'Category':<15}")
                print("-" * 120)
                
                for row in results:
                    class_id = row[0]
                    program = row[1][:24] if row[1] else "N/A"
                    trainer = row[2][:19] if row[2] else "N/A"
                    schedule = str(row[3])[:19] if row[3] else "N/A"
                    room = row[4][:11] if row[4] else "N/A"
                    capacity = row[5] if row[5] else 0
                    category = row[6][:14] if row[6] else "N/A"
                    
                    print(f"{class_id:<5} {program:<25} {trainer:<20} {schedule:<20} {room:<12} {capacity:<8} {category:<15}")
                
                print(f"\nTotal Classes: {len(results)}")
                print("=" * 120)
            else:
                print("\n✗ No classes found in the database.")
                print("=" * 120)
                
        except Error as e:
            print(f"\n✗ Error viewing classes: {e}")