CREATE DATABASE fitlife_groupd;
USE fitlife_groupd;

CREATE TABLE Member (
    Member_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Contact_Details VARCHAR(15),
    Email VARCHAR(100),
    Date_of_Birth DATE,
    Gender CHAR(1),
    Membership_Type VARCHAR(20) NOT NULL,
    Membership_Start DATETIME,
    Membership_End DATETIME,
    Membership_Status VARCHAR(10)
);

CREATE TABLE StandardMember (
    Member_ID INT PRIMARY KEY,
    Monthly_Limit INT,
    Discount_Rate DECIMAL(5,2),
    Access_Level VARCHAR(20),
    Reward_Points INT,
    FOREIGN KEY (Member_ID) REFERENCES Member(Member_ID)
);

CREATE TABLE PremiumMember (
    Member_ID INT PRIMARY KEY,
    Personal_Trainer VARCHAR(100),
    Spa_Access TINYINT(1),
    Premium_Discount DECIMAL(5,2),
    Priority_Booking TINYINT(1),
    FOREIGN KEY (Member_ID) REFERENCES Member(Member_ID)
);

CREATE TABLE Trainer (
    Trainer_ID INT AUTO_INCREMENT PRIMARY KEY,
    Full_Name VARCHAR(100) NOT NULL,
    Specialization VARCHAR(100),
    Certification_Level VARCHAR(20),
    Contact_Details VARCHAR(15),
    Trainer_Type VARCHAR(20)
);

CREATE TABLE YogaTrainer (
    Trainer_ID INT PRIMARY KEY,
    Yoga_Level VARCHAR(20),
    Preferred_Style VARCHAR(50),
    Meditation_Training TINYINT(1),
    Years_Yoga_Experience INT,
    FOREIGN KEY (Trainer_ID) REFERENCES Trainer(Trainer_ID)
);

CREATE TABLE PhysioTrainer (
    Trainer_ID INT PRIMARY KEY,
    Medical_License VARCHAR(50),
    Specialized_Area VARCHAR(100),
    Years_Physio_Experience INT,
    Clinic_Affiliation VARCHAR(100),
    FOREIGN KEY (Trainer_ID) REFERENCES Trainer(Trainer_ID)
);

CREATE TABLE FitnessTrainer (
    Trainer_ID INT PRIMARY KEY,
    Strength_Certification VARCHAR(50),
    Years_Fitness_Experience INT,
    Max_Class INT,
    Special_Skills VARCHAR(200),
    FOREIGN KEY (Trainer_ID) REFERENCES Trainer(Trainer_ID)
);

CREATE TABLE Program (
    Program_ID INT AUTO_INCREMENT PRIMARY KEY,
    Program_Name VARCHAR(100) NOT NULL,
    Category VARCHAR(40),
    Duration_Weeks INT,
    Fee DECIMAL(8,2),
    Trainer_ID INT,
    FOREIGN KEY (Trainer_ID) REFERENCES Trainer(Trainer_ID)
);

CREATE TABLE `Class` (
    Class_ID INT AUTO_INCREMENT PRIMARY KEY,
    Schedule_DateTime DATETIME,
    Room VARCHAR(20),
    Max_Capacity INT,
    Program_ID INT,
    Trainer_ID INT,
    FOREIGN KEY (Program_ID) REFERENCES Program(Program_ID),
    FOREIGN KEY (Trainer_ID) REFERENCES Trainer(Trainer_ID)
);

CREATE TABLE Enrollment (
    Enrollment_ID INT AUTO_INCREMENT PRIMARY KEY,
    Enrollment_Date DATETIME,
    Enrollment_Status VARCHAR(40),
    Payment_Status VARCHAR(40),
    Member_ID INT,
    Program_ID INT,
    FOREIGN KEY (Member_ID) REFERENCES Member(Member_ID),
    FOREIGN KEY (Program_ID) REFERENCES Program(Program_ID)
);

CREATE TABLE Payment (
    Payment_ID INT AUTO_INCREMENT PRIMARY KEY,
    Amount DECIMAL(8,2),
    Payment_Date DATETIME,
    Payment_Type VARCHAR(20),
    Reference_No VARCHAR(40),
    Member_ID INT,
    Enrollment_ID INT,
    FOREIGN KEY (Member_ID) REFERENCES Member(Member_ID),
    FOREIGN KEY (Enrollment_ID) REFERENCES Enrollment(Enrollment_ID)
);

CREATE TABLE TrainerAssignmentHistory (
    History_ID INT AUTO_INCREMENT PRIMARY KEY,
    Trainer_ID INT,
    Program_Category VARCHAR(40),
    Start_Date DATE,
    End_Date DATE,
    FOREIGN KEY (Trainer_ID) REFERENCES Trainer(Trainer_ID)
);

INSERT INTO Member (Member_ID, Name, Contact_Details, Email, Date_of_Birth, Gender, Membership_Type, Membership_Start, Membership_End, Membership_Status) VALUES
(1001, 'Alice Chan', '60123456789', 'alicechan@gmail.com', '1990-05-15', 'F', 'Premium', '2025-11-01 00:00:00', '2026-11-01 23:59:59', 'Active'),
(1002, 'Farhan Hakim', '60175044704', 'farhanhakim23@gmail.com', '1985-11-20', 'M', 'Standard', '2025-10-10 00:00:00', '2026-04-10 23:59:59', 'Active'),
(1003, 'Carlos Sugang', '60186318332', 'carlossugang24@gmail.com', '2000-02-28', 'M', 'Premium', '2024-12-01 00:00:00', '2025-12-01 23:59:59', 'Active'),
(1004, 'David Chai', '60183785187', 'davidchai69@gmail.com', '1975-08-01', 'M', 'Standard', '2025-11-15 00:00:00', '2025-12-15 23:59:59', 'Pending'),
(1005, 'Evelyn Wong', '60165454679', 'evelynwong@gmail.com', '1998-04-10', 'F', 'Standard', '2025-09-01 00:00:00', '2026-03-01 23:59:59', 'Active');

INSERT INTO StandardMember (Member_ID, Monthly_Limit, Discount_Rate, Access_Level, Reward_Points) VALUES
(1002, 8, 5.00, 'Basic', 120),
(1004, 10, 5.00, 'Basic', 45),
(1005, 12, 7.50, 'Basic', 200);

INSERT INTO PremiumMember (Member_ID, Personal_Trainer, Spa_Access, Premium_Discount, Priority_Booking) VALUES
(1001, 'Dayang Rifa', 1, 15.00, 1),
(1003, 'Hector Wong', 1, 15.00, 1);

INSERT INTO Trainer (Trainer_ID, Full_Name, Specialization, Certification_Level, Contact_Details, Trainer_Type) VALUES
(1, 'Dayang Rifa', 'Yoga and Flexibility', 'RYT-500', '60123581728', 'Yoga'),
(2, 'David Chai', 'Weightlifting Coach', 'NASM-CPT', '60111000871', 'Fitness'),
(3, 'Hector Wong', 'Cardio and HIIT', 'Group Fit Lv. 2', '60113952338', 'Fitness'),
(4, 'Mia Crystal', 'Rehabilitation Specialist', 'Physio Assistant', '60145911406', 'Physio'),
(5, 'Luke Chiang', 'Nutrition and Wellness', 'Certified Wellness Coach', '60159577139', 'Fitness');

INSERT INTO YogaTrainer (Trainer_ID, Yoga_Level, Preferred_Style, Meditation_Training, Years_Yoga_Experience) VALUES
(1, 'Advanced', 'Hatha Yoga', 1, 8);

INSERT INTO PhysioTrainer (Trainer_ID, Medical_License, Specialized_Area, Years_Physio_Experience, Clinic_Affiliation) VALUES
(4, 'MYS-PA-2019-4567', 'Sports Rehabilitation', 6, 'Sarawak Sports Clinic');

INSERT INTO FitnessTrainer (Trainer_ID, Strength_Certification, Years_Fitness_Experience, Max_Class, Special_Skills) VALUES
(2, 'NASM-CPT, CSCS', 10, 15, 'Powerlifting, Olympic Lifting'),
(3, 'ACE Group Fitness', 7, 25, 'HIIT, Circuit Training, Bootcamp'),
(5, 'Wellness Coach Cert', 5, 20, 'Nutrition Planning, Lifestyle Coaching');

INSERT INTO Program (Program_ID, Program_Name, Category, Duration_Weeks, Fee, Trainer_ID) VALUES
(1, 'Morning Yoga Flow', 'Yoga', 8, 350.00, 1),
(2, 'Power Strength Training', 'Strength', 12, 480.00, 2),
(3, 'HIIT Bootcamp', 'Cardio', 6, 300.00, 3),
(4, 'Pilates Core', 'Pilates', 10, 420.00, 1),
(5, 'CrossFit Fundamentals', 'CrossFit', 8, 500.00, 2),
(6, 'Rehabilitation Therapy', 'Physio', 12, 650.00, 4),
(7, 'Weight Loss Program', 'Weight Management', 12, 550.00, 5),
(8, 'Senior Wellness', 'General Fitness', 8, 320.00, 5);

INSERT INTO `Class` (Class_ID, Schedule_DateTime, Room, Max_Capacity, Program_ID, Trainer_ID) VALUES
(1, '2025-01-05 07:00:00', 'Studio A', 20, 1, 1),
(2, '2025-01-05 09:00:00', 'Gym Floor', 15, 2, 2),
(3, '2025-01-05 18:00:00', 'Studio B', 25, 3, 3),
(4, '2025-01-06 10:00:00', 'Studio A', 18, 4, 1),
(5, '2025-01-06 17:00:00', 'CrossFit Zone', 12, 5, 2),
(6, '2025-01-07 14:00:00', 'Rehab Room', 8, 6, 4),
(7, '2025-01-07 07:00:00', 'Studio A', 20, 1, 1),
(8, '2025-01-08 09:00:00', 'Gym Floor', 15, 2, 2),
(9, '2025-01-08 18:00:00', 'Studio B', 25, 3, 3),
(10, '2025-01-09 08:00:00', 'Gym Floor', 20, 7, 5);

INSERT INTO Enrollment (Enrollment_ID, Enrollment_Date, Enrollment_Status, Payment_Status, Member_ID, Program_ID) VALUES
(1, '2025-11-05 10:30:00', 'Active', 'Paid', 1001, 1),
(2, '2025-11-06 14:20:00', 'Active', 'Paid', 1001, 3),
(3, '2025-10-15 09:45:00', 'Active', 'Paid', 1002, 2),
(4, '2025-12-03 11:00:00', 'Active', 'Paid', 1003, 4),
(5, '2025-12-10 16:30:00', 'Active', 'Paid', 1003, 1),
(6, '2025-11-20 13:15:00', 'Active', 'Paid', 1005, 3),
(7, '2025-12-01 10:00:00', 'Active', 'Pending', 1004, 2),
(8, '2025-11-25 15:45:00', 'Active', 'Paid', 1002, 7),
(9, '2025-12-15 12:30:00', 'Active', 'Paid', 1005, 6),
(10, '2025-12-20 14:00:00', 'Active', 'Partial', 1001, 7);

INSERT INTO Payment (Payment_ID, Amount, Payment_Date, Payment_Type, Reference_No, Member_ID, Enrollment_ID) VALUES
(1, 350.00, '2025-11-05 10:35:00', 'Card', 'REF001-2025', 1001, 1),
(2, 300.00, '2025-11-06 14:25:00', 'Online', 'REF002-2025', 1001, 2),
(3, 480.00, '2025-10-15 09:50:00', 'Bank Transfer', 'REF003-2025', 1002, 3),
(4, 420.00, '2025-12-03 11:05:00', 'Card', 'REF004-2025', 1003, 4),
(5, 350.00, '2025-12-10 16:35:00', 'Card', 'REF005-2025', 1003, 5),
(6, 300.00, '2025-11-20 13:20:00', 'Online', 'REF006-2025', 1005, 6),
(7, 550.00, '2025-11-25 15:50:00', 'Card', 'REF007-2025', 1002, 8),
(8, 650.00, '2025-12-15 12:35:00', 'Bank Transfer', 'REF008-2025', 1005, 9),
(9, 275.00, '2025-12-20 14:05:00', 'Card', 'REF009-2025', 1001, 10);

INSERT INTO TrainerAssignmentHistory (History_ID, Trainer_ID, Program_Category, Start_Date, End_Date) VALUES
(1, 1, 'Yoga', '2024-01-01', '2025-12-31'),
(2, 2, 'Strength', '2024-01-01', '2025-12-31'),
(3, 3, 'Cardio', '2024-06-01', '2025-12-31'),
(4, 4, 'Physio', '2024-03-01', '2025-12-31'),
(5, 5, 'Weight Management', '2024-09-01', '2025-12-31');
