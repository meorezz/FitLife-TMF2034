A comprehensive database management system for FitLife Wellness Centre that handles members, trainers, programs, classes, enrollments, and payments.
Team D - Group 6

JILL ALBRIGHT GABRIEL (104554)
AUDREY CHAN HUI JING (103447)
MUHAMAD NASIH SYAHMI BIN MISRAZIFF (99855)
MOHAMAD SYAKIRUL ASYRAAF BIN ABDULLAH MAZIDI (99754)
MEOR HAZRUL HAKIM BIN MEOR HARMAN (84477)

FitLife_Database_System/
│
├── main.py                          # Main application entry point
│
├── database/
│   ├── __init__.py                  # Package initializer
│   └── db_connection.py             # Database connection handler
│
├── operations/
│   ├── __init__.py                  # Package initializer
│   ├── member_ops.py                # Member CRUD operations
│   ├── trainer_ops.py               # Trainer CRUD operations
│   ├── program_ops.py               # Program CRUD operations
│   ├── class_ops.py                 # Class CRUD operations
│   ├── enrollment_ops.py            # Enrollment CRUD operations
│   └── payment_ops.py               # Payment CRUD operations
│
├── utils/
│   ├── __init__.py                  # Package initializer
│   └── menu.py                      # Menu display utilities
│
├── setup_database.sql               # Database setup script
└── README.md                        