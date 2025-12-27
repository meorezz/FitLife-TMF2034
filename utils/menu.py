"""
Menu Display Utility Module
Handles all menu displays for the FitLife application
"""


class Menu:
    """Class to handle menu displays"""
    
    @staticmethod
    def clear_screen():
        """Clear the screen (simplified version)"""
        print("\n" * 2)
    
    def display_main_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 60)
        print(" " * 20 + "MAIN MENU")
        print("=" * 60)
        print("  1. Member Management")
        print("  2. Trainer Management")
        print("  3. Program Management")
        print("  4. Class Management")
        print("  5. Enrollment Management")
        print("  6. Payment Management")
        print("  7. About System")
        print("  8. Exit")
        print("=" * 60)
    
    def display_member_menu(self):
        """Display member management submenu"""
        print("\n" + "=" * 60)
        print(" " * 18 + "MEMBER MANAGEMENT")
        print("=" * 60)
        print("  1. Add New Member")
        print("  2. Update Member")
        print("  3. Delete Member")
        print("  4. View All Members")
        print("  5. Search Member")
        print("  6. Back to Main Menu")
        print("=" * 60)
    
    def display_trainer_menu(self):
        """Display trainer management submenu"""
        print("\n" + "=" * 60)
        print(" " * 17 + "TRAINER MANAGEMENT")
        print("=" * 60)
        print("  1. Add New Trainer")
        print("  2. Update Trainer")
        print("  3. Delete Trainer")
        print("  4. View All Trainers")
        print("  5. Search Trainer")
        print("  6. Back to Main Menu")
        print("=" * 60)
    
    def display_program_menu(self):
        """Display program management submenu"""
        print("\n" + "=" * 60)
        print(" " * 17 + "PROGRAM MANAGEMENT")
        print("=" * 60)
        print("  1. Add New Program")
        print("  2. Update Program")
        print("  3. Delete Program")
        print("  4. View All Programs")
        print("  5. Search Program")
        print("  6. Back to Main Menu")
        print("=" * 60)
    
    def display_class_menu(self):
        """Display class management submenu"""
        print("\n" + "=" * 60)
        print(" " * 18 + "CLASS MANAGEMENT")
        print("=" * 60)
        print("  1. Add New Class")
        print("  2. Update Class")
        print("  3. Delete Class")
        print("  4. View All Classes")
        print("  5. Back to Main Menu")
        print("=" * 60)
    
    def display_enrollment_menu(self):
        """Display enrollment management submenu"""
        print("\n" + "=" * 60)
        print(" " * 15 + "ENROLLMENT MANAGEMENT")
        print("=" * 60)
        print("  1. Add New Enrollment")
        print("  2. Update Enrollment")
        print("  3. Delete Enrollment")
        print("  4. View All Enrollments")
        print("  5. Back to Main Menu")
        print("=" * 60)
    
    def display_payment_menu(self):
        """Display payment management submenu"""
        print("\n" + "=" * 60)
        print(" " * 17 + "PAYMENT MANAGEMENT")
        print("=" * 60)
        print("  1. Add New Payment")
        print("  2. Update Payment")
        print("  3. Delete Payment")
        print("  4. View All Payments")
        print("  5. Back to Main Menu")
        print("=" * 60)
    
    def display_about(self):
        """Display about information"""
        print("\n" + "=" * 60)
        print(" " * 18 + "ABOUT SYSTEM")
        print("=" * 60)
        print("\n  FitLife Wellness Centre Database System")
        print("  Version: 1.0")
        print("  Developed by: Team D - Group 6")
        print("\n  Team Members:")
        print("    - JILL ALBRIGHT GABRIEL (104554)")
        print("    - AUDREY CHAN HUI JING (103447)")
        print("    - MUHAMAD NASIH SYAHMI BIN MISRAZIFF (99855)")
        print("    - MOHAMAD SYAKIRUL ASYRAAF BIN ABDULLAH MAZIDI (99754)")
        print("    - MEOR HAZRUL HAKIM BIN MEOR HARMAN (84477)")
        print("\n  Course: TMF2034 - Database Concept and Design")
        print("  Semester: 1, 2025/2026")
        print("  Lecturer: CHIU PO CHAN")
        print("\n  Description:")
        print("    This system manages members, trainers, programs,")
        print("    classes, enrollments, and payments for FitLife")
        print("    Wellness Centre.")
        print("=" * 60)