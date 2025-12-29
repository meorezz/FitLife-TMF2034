
CREATE DATABASE IF NOT EXISTS fitlife_wellness;
USE fitlife_wellness;


DROP TABLE IF EXISTS Payment;
DROP TABLE IF EXISTS Enrollment;
DROP TABLE IF EXISTS Class;
DROP TABLE IF EXISTS Program;
DROP TABLE IF EXISTS Trainer;
DROP TABLE IF EXISTS Member;


CREATE TABLE Member (
    Member_ID INT(10) AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Contact_Details VARCHAR(15),
    Email VARCHAR(100),
    Date_of_Birth DATE,
    Gender CHAR(1),
    Membership_Type VARCHAR(20),
    Membership_Start DATETIME,
    Membership_End DATETIME,
    Membership_Status VARCHAR(10)
);


CREATE TABLE Trainer (
    Trainer_ID INT(10) AUTO_INCREMENT PRIMARY KEY,
    Full_Name VARCHAR(100) NOT NULL,
    Specialization VARCHAR(100),
    Certification_Level VARCHAR(20),
    Contact_Details VARCHAR(15)
);


CREATE TABLE Program (
    Program_ID INT(10) AUTO_INCREMENT PRIMARY KEY,
    Program_Name VARCHAR(100) NOT NULL,
    Category VARCHAR(40),
    Duration_Weeks INT(2),
    Fee DECIMAL(8,2)
);


CREATE TABLE Class (
    Class_ID INT(10) AUTO_INCREMENT PRIMARY KEY,
    Program_ID INT(10),
    Trainer_ID INT(10),
    Schedule_DateTime DATETIME,
    Room VARCHAR(20),
    Max_Capacity INT(5),
    FOREIGN KEY (Program_ID) REFERENCES Program(Program_ID) ON DELETE CASCADE,
    FOREIGN KEY (Trainer_ID) REFERENCES Trainer(Trainer_ID) ON DELETE CASCADE
);


CREATE TABLE Enrollment (
    Enrollment_ID INT(10) AUTO_INCREMENT PRIMARY KEY,
    Member_ID INT(10),
    Program_ID INT(10),
    Enrollment_Date DATETIME,
    Enrollment_Status VARCHAR(40),
    Payment_Status VARCHAR(40),
    FOREIGN KEY (Member_ID) REFERENCES Member(Member_ID) ON DELETE CASCADE,
    FOREIGN KEY (Program_ID) REFERENCES Program(Program_ID) ON DELETE CASCADE
);

CREATE TABLE Payment (
    Payment_ID INT(10) AUTO_INCREMENT PRIMARY KEY,
    Member_ID INT(10),
    Enrollment_ID INT(10),
    Amount DECIMAL(8,2),
    Payment_Date DATETIME,
    Payment_Type VARCHAR(20),
    Reference_No VARCHAR(40),
    FOREIGN KEY (Member_ID) REFERENCES Member(Member_ID) ON DELETE CASCADE,
    FOREIGN KEY (Enrollment_ID) REFERENCES Enrollment(Enrollment_ID) ON DELETE CASCADE
);


INSERT INTO Member (Name, Contact_Details, Email, Date_of_Birth, Gender, Membership_Type, Membership_Start, Membership_End, Membership_Status) VALUES
('Sarah Johnson', '0123456789', 'sarah.j@email.com', '1995-05-15', 'F', 'Premium', '2024-01-01', '2025-01-01', 'Active'),
('Michael Chen', '0187654321', 'michael.chen@email.com', '1988-08-20', 'M', 'Standard', '2024-03-15', '2024-12-15', 'Active'),
('Emily Wong', '0198765432', 'emily.w@email.com', '1992-12-10', 'F', 'Premium', '2024-02-01', '2025-02-01', 'Active'),
('David Lee', '0176543210', 'david.lee@email.com', '1985-03-25', 'M', 'Standard', '2023-11-01', '2024-11-01', 'Expired'),
('Jessica Tan', '0165432109', 'jessica.tan@email.com', '1990-07-18', 'F', 'Premium', '2024-04-10', '2025-04-10', 'Active'),
('Robert Kumar', '0154321098', 'robert.k@email.com', '1987-09-05', 'M', 'Standard', '2024-05-20', '2025-05-20', 'Active'),
('Amanda Lim', '0143210987', 'amanda.lim@email.com', '1993-11-30', 'F', 'Premium', '2024-06-01', '2025-06-01', 'Active'),
('Christopher Ng', '0132109876', 'chris.ng@email.com', '1991-02-14', 'M', 'Standard', '2024-01-15', '2025-01-15', 'Active');


INSERT INTO Trainer (Full_Name, Specialization, Certification_Level, Contact_Details) VALUES
('Alex Martinez', 'Yoga & Flexibility', 'Advanced', '0111222333'),
('Rachel Green', 'Strength Training', 'Expert', '0122333444'),
('Kevin Park', 'Cardio & HIIT', 'Advanced', '0133444555'),
('Linda Brown', 'Pilates', 'Expert', '0144555666'),
('James Wilson', 'CrossFit', 'Advanced', '0155666777'),
('Maria Garcia', 'Dance Fitness', 'Intermediate', '0166777888');


INSERT INTO Program (Program_Name, Category, Duration_Weeks, Fee) VALUES
('Morning Yoga Flow', 'Yoga', 8, 350.00),
('Power Strength Training', 'Strength', 12, 480.00),
('HIIT Bootcamp', 'Cardio', 6, 300.00),
('Pilates Core', 'Pilates', 10, 420.00),
('CrossFit Fundamentals', 'CrossFit', 8, 500.00),
('Zumba Dance Party', 'Dance', 6, 280.00),
('Weight Loss Program', 'Weight Management', 12, 550.00),
('Senior Wellness', 'General Fitness', 8, 320.00);


INSERT INTO Class (Program_ID, Trainer_ID, Schedule_DateTime, Room, Max_Capacity) VALUES
(1, 1, '2024-12-28 07:00:00', 'Studio A', 20),
(2, 2, '2024-12-28 09:00:00', 'Gym Floor', 15),
(3, 3, '2024-12-28 18:00:00', 'Studio B', 25),
(4, 4, '2024-12-29 10:00:00', 'Studio A', 18),
(5, 5, '2024-12-29 17:00:00', 'CrossFit Zone', 12),
(6, 6, '2024-12-30 19:00:00', 'Studio C', 30),
(1, 1, '2024-12-30 07:00:00', 'Studio A', 20),
(2, 2, '2024-12-31 09:00:00', 'Gym Floor', 15),
(3, 3, '2025-01-02 18:00:00', 'Studio B', 25),
(7, 2, '2025-01-03 08:00:00', 'Gym Floor', 20);


INSERT INTO Enrollment (Member_ID, Program_ID, Enrollment_Date, Enrollment_Status, Payment_Status) VALUES
(1, 1, '2024-12-01', 'Active', 'Paid'),
(1, 3, '2024-12-05', 'Active', 'Paid'),
(2, 2, '2024-12-02', 'Active', 'Paid'),
(3, 4, '2024-12-03', 'Active', 'Paid'),
(3, 1, '2024-12-10', 'Active', 'Paid'),
(5, 5, '2024-12-04', 'Active', 'Paid'),
(6, 3, '2024-12-15', 'Active', 'Pending'),
(7, 6, '2024-12-20', 'Active', 'Paid'),
(8, 2, '2024-12-08', 'Active', 'Paid'),
(1, 7, '2024-12-12', 'Active', 'Partial');


INSERT INTO Payment (Member_ID, Enrollment_ID, Amount, Payment_Date, Payment_Type, Reference_No) VALUES
(1, 1, 350.00, '2024-12-01', 'Card', 'REF001-2024'),
(1, 2, 300.00, '2024-12-05', 'Online', 'REF002-2024'),
(2, 3, 480.00, '2024-12-02', 'Bank Transfer', 'REF003-2024'),
(3, 4, 420.00, '2024-12-03', 'Card', 'REF004-2024'),
(3, 5, 350.00, '2024-12-10', 'Card', 'REF005-2024'),
(5, 6, 500.00, '2024-12-04', 'Online', 'REF006-2024'),
(7, 8, 280.00, '2024-12-20', 'Cash', 'REF007-2024'),
(8, 9, 480.00, '2024-12-08', 'Card', 'REF008-2024'),
(1, 10, 275.00, '2024-12-12', 'Card', 'REF009-2024');


SELECT 'Members' as Table_Name, COUNT(*) as Record_Count FROM Member
UNION ALL
SELECT 'Trainers', COUNT(*) FROM Trainer
UNION ALL
SELECT 'Programs', COUNT(*) FROM Program
UNION ALL
SELECT 'Classes', COUNT(*) FROM Class
UNION ALL
SELECT 'Enrollments', COUNT(*) FROM Enrollment
UNION ALL
SELECT 'Payments', COUNT(*) FROM Payment;

COMMIT;