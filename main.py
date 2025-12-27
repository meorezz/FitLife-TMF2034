"""
FitLife Wellness Centre Database Application
Main Entry Point
Author: Team D - Member 2 (Backend Developer)
"""

from database.db_connection import FitLifeDB
from operations.member_ops import MemberOperations
from operations.trainer_ops import TrainerOperations
from operations.program_ops import ProgramOperations
from operations.class_ops import ClassOperations
from operations.enrollment_ops import EnrollmentOperations
from operations.payment_ops import PaymentOperations
from utils.menu import Menu
import sys


def main():
    """Main application function"""
    print("\n" + "=" * 60)
    print(" " * 15 + "FITLIFE WELLNESS CENTRE")
    print(" " * 12 + "Database Management System")
    print("=" * 60)
    
    # Initialize database connection
    db = FitLifeDB()
    
    # Initialize operation modules
    member_ops = MemberOperations(db)
    trainer_ops = TrainerOperations(db)
    program_ops = ProgramOperations(db)
    class_ops = ClassOperations(db)
    enrollment_ops = EnrollmentOperations(db)
    payment_ops = PaymentOperations(db)
    menu = Menu()
    
    # Main application loop
    while True:
        try:
            menu.display_main_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                # Member Management
                while True:
                    menu.display_member_menu()
                    sub_choice = input("\nEnter your choice (1-6): ").strip()
                    
                    if sub_choice == '1':
                        member_ops.add_member()
                    elif sub_choice == '2':
                        member_ops.update_member()
                    elif sub_choice == '3':
                        member_ops.delete_member()
                    elif sub_choice == '4':
                        member_ops.view_all_members()
                    elif sub_choice == '5':
                        member_ops.search_member()
                    elif sub_choice == '6':
                        break
                    else:
                        print("✗ Invalid choice! Please try again.")
                    
                    input("\nPress Enter to continue...")
            
            elif choice == '2':
                # Trainer Management
                while True:
                    menu.display_trainer_menu()
                    sub_choice = input("\nEnter your choice (1-6): ").strip()
                    
                    if sub_choice == '1':
                        trainer_ops.add_trainer()
                    elif sub_choice == '2':
                        trainer_ops.update_trainer()
                    elif sub_choice == '3':
                        trainer_ops.delete_trainer()
                    elif sub_choice == '4':
                        trainer_ops.view_all_trainers()
                    elif sub_choice == '5':
                        trainer_ops.search_trainer()
                    elif sub_choice == '6':
                        break
                    else:
                        print("✗ Invalid choice! Please try again.")
                    
                    input("\nPress Enter to continue...")
            
            elif choice == '3':
                # Program Management
                while True:
                    menu.display_program_menu()
                    sub_choice = input("\nEnter your choice (1-6): ").strip()
                    
                    if sub_choice == '1':
                        program_ops.add_program()
                    elif sub_choice == '2':
                        program_ops.update_program()
                    elif sub_choice == '3':
                        program_ops.delete_program()
                    elif sub_choice == '4':
                        program_ops.view_all_programs()
                    elif sub_choice == '5':
                        program_ops.search_program()
                    elif sub_choice == '6':
                        break
                    else:
                        print("✗ Invalid choice! Please try again.")
                    
                    input("\nPress Enter to continue...")
            
            elif choice == '4':
                # Class Management
                while True:
                    menu.display_class_menu()
                    sub_choice = input("\nEnter your choice (1-5): ").strip()
                    
                    if sub_choice == '1':
                        class_ops.add_class()
                    elif sub_choice == '2':
                        class_ops.update_class()
                    elif sub_choice == '3':
                        class_ops.delete_class()
                    elif sub_choice == '4':
                        class_ops.view_all_classes()
                    elif sub_choice == '5':
                        break
                    else:
                        print("✗ Invalid choice! Please try again.")
                    
                    input("\nPress Enter to continue...")
            
            elif choice == '5':
                # Enrollment Management
                while True:
                    menu.display_enrollment_menu()
                    sub_choice = input("\nEnter your choice (1-5): ").strip()
                    
                    if sub_choice == '1':
                        enrollment_ops.add_enrollment()
                    elif sub_choice == '2':
                        enrollment_ops.update_enrollment()
                    elif sub_choice == '3':
                        enrollment_ops.delete_enrollment()
                    elif sub_choice == '4':
                        enrollment_ops.view_all_enrollments()
                    elif sub_choice == '5':
                        break
                    else:
                        print("✗ Invalid choice! Please try again.")
                    
                    input("\nPress Enter to continue...")
            
            elif choice == '6':
                # Payment Management
                while True:
                    menu.display_payment_menu()
                    sub_choice = input("\nEnter your choice (1-5): ").strip()
                    
                    if sub_choice == '1':
                        payment_ops.add_payment()
                    elif sub_choice == '2':
                        payment_ops.update_payment()
                    elif sub_choice == '3':
                        payment_ops.delete_payment()
                    elif sub_choice == '4':
                        payment_ops.view_all_payments()
                    elif sub_choice == '5':
                        break
                    else:
                        print("✗ Invalid choice! Please try again.")
                    
                    input("\nPress Enter to continue...")
            
            elif choice == '7':
                # About System
                menu.display_about()
                input("\nPress Enter to continue...")
            
            elif choice == '8':
                # Exit
                print("\n" + "=" * 60)
                print("Thank you for using FitLife Wellness Centre System!")
                print("=" * 60)
                db.close_connection()
                sys.exit(0)
            
            else:
                print("✗ Invalid choice! Please enter a number between 1-8.")
                input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n✗ Operation cancelled by user.")
            confirm = input("Do you want to exit? (yes/no): ").strip().lower()
            if confirm == 'yes':
                db.close_connection()
                sys.exit(0)
        
        except Exception as e:
            print(f"\n✗ An unexpected error occurred: {e}")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()