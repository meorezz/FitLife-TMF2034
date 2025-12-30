USE fitlife_groupd;


INSERT INTO Member (Name, Contact_Details, Email, Date_of_Birth, Gender, Membership_Type, Membership_Start, Membership_End, Membership_Status)
VALUES ('New Name', '6012...', 'email@example.com', '1999-01-01', 'M', 'Standard', NOW(), DATE_ADD(NOW(), INTERVAL 6 MONTH), 'Active');

-- UPDATE 
UPDATE Member
SET Membership_Status = 'Active',
    Contact_Details = '6012...'
WHERE Member_ID = 1002;


DELETE FROM Payment WHERE Member_ID = 1002;
DELETE FROM Enrollment WHERE Member_ID = 1002;
DELETE FROM MemberClassAttendance WHERE Member_ID = 1002;
DELETE FROM StandardMember WHERE Member_ID = 1002;
DELETE FROM PremiumMember WHERE Member_ID = 1002;
DELETE FROM Member WHERE Member_ID = 1002;

-- TRAINER (base)
INSERT INTO Trainer (Full_Name, Specialization, Certification_Level, Contact_Details, Trainer_Type)
VALUES ('New Trainer', 'Strength', 'NASM-CPT', '6013...', 'Fitness');

UPDATE Trainer
SET Contact_Details = '6013...', Certification_Level = 'NASM-CPT'
WHERE Trainer_ID = 2;

-- Delete dependent rows first (Program, Class, subtype tables)
DELETE FROM Program WHERE Trainer_ID = 2;
DELETE FROM `Class` WHERE Trainer_ID = 2;
DELETE FROM YogaTrainer WHERE Trainer_ID = 2;
DELETE FROM PhysioTrainer WHERE Trainer_ID = 2;
DELETE FROM FitnessTrainer WHERE Trainer_ID = 2;
DELETE FROM Trainer WHERE Trainer_ID = 2;

-- PROGRAM
INSERT INTO Program (Program_Name, Category, Duration_Weeks, Fee, Trainer_ID)
VALUES ('New Program', 'Yoga', 8, 399.00, 1);

UPDATE Program
SET Fee = 450.00, Duration_Weeks = 10
WHERE Program_ID = 1;

-- Delete enrollments + classes referencing program first
DELETE FROM Enrollment WHERE Program_ID = 1;
DELETE FROM `Class` WHERE Program_ID = 1;
DELETE FROM Program WHERE Program_ID = 1;

-- CLASS
INSERT INTO `Class` (Schedule_DateTime, Room, Max_Capacity, Program_ID, Trainer_ID, Class_Status)
VALUES ('2026-01-10 09:00:00', 'Studio A', 20, 1, 1, 'Active');

UPDATE `Class`
SET Room = 'Studio B', Class_Status = 'Cancelled'
WHERE Class_ID = 9;

DELETE FROM MemberClassAttendance WHERE Class_ID = 9;
DELETE FROM `Class` WHERE Class_ID = 9;

-- ENROLLMENT
INSERT INTO Enrollment (Enrollment_Date, Enrollment_Status, Payment_Status, Member_ID, Program_ID)
VALUES (NOW(), 'Active', 'Pending', 1005, 2);

UPDATE Enrollment
SET Payment_Status = 'Paid'
WHERE Enrollment_ID = 7;

-- Delete payments linked first
DELETE FROM Payment WHERE Enrollment_ID = 7;
DELETE FROM Enrollment WHERE Enrollment_ID = 7;

-- PAYMENT
INSERT INTO Payment (Amount, Payment_Date, Payment_Type, Reference_No, Member_ID, Enrollment_ID)
VALUES (480.00, NOW(), 'Card', 'REFNEW-2026', 1002, 3);

UPDATE Payment
SET Amount = 500.00
WHERE Payment_ID = 3;

DELETE FROM Payment WHERE Payment_ID = 3;

-- ATTENDANCE
INSERT INTO MemberClassAttendance (Member_ID, Class_ID, Attendance_Status, Checkin_Time)
VALUES (1001, 10, 'Attended', NOW());

UPDATE MemberClassAttendance
SET Attendance_Status = 'Absent', Checkin_Time = NULL
WHERE Attendance_ID = 1;

DELETE FROM MemberClassAttendance WHERE Attendance_ID = 1;

-- REPORT QUERIES (Required b(i)-(v))

-- (i) All members list with totals (programs enrolled, classes attended, payments, membership status)
SELECT
    m.Member_ID,
    m.Name,
    m.Membership_Type,
    m.Membership_Status,
    COALESCE(COUNT(DISTINCT e.Program_ID), 0) AS Total_Programs_Enrolled,
    COALESCE(SUM(CASE WHEN a.Attendance_Status='Attended' THEN 1 ELSE 0 END), 0) AS Total_Classes_Attended,
    COALESCE(SUM(p.Amount), 0) AS Total_Payments
FROM Member m
LEFT JOIN Enrollment e ON e.Member_ID = m.Member_ID
LEFT JOIN MemberClassAttendance a ON a.Member_ID = m.Member_ID
LEFT JOIN Payment p ON p.Member_ID = m.Member_ID
GROUP BY m.Member_ID, m.Name, m.Membership_Type, m.Membership_Status
ORDER BY m.Member_ID;

-- (ii) All scheduled classes with date/time, trainer, class status, program category
SELECT
    c.Class_ID,
    DATE_FORMAT(c.Schedule_DateTime, '%Y-%m-%d %H:%i') AS Schedule,
    c.Room,
    c.Max_Capacity,
    c.Class_Status,
    t.Full_Name AS Trainer,
    pr.Program_Name,
    pr.Category AS Program_Category
FROM `Class` c
JOIN Trainer t ON t.Trainer_ID = c.Trainer_ID
JOIN Program pr ON pr.Program_ID = c.Program_ID
ORDER BY c.Schedule_DateTime;

-- (iii) Trainer performance reports
SELECT
    t.Trainer_ID,
    t.Full_Name AS Trainer,
    COUNT(*) AS Total_Classes_Assigned,
    SUM(CASE WHEN c.Class_Status='Cancelled' THEN 1 ELSE 0 END) AS Total_Cancelled,
    SUM(CASE WHEN c.Class_Status='Completed' THEN 1 ELSE 0 END) AS Total_Completed,
    SUM(CASE WHEN c.Class_Status='Active' THEN 1 ELSE 0 END) AS Total_Active
FROM Trainer t
LEFT JOIN `Class` c ON c.Trainer_ID = t.Trainer_ID
GROUP BY t.Trainer_ID, t.Full_Name
ORDER BY Total_Classes_Assigned DESC, t.Full_Name;

-- (iv-a) Quarterly fees (from Payment table)
SELECT
    YEAR(Payment_Date) AS Year,
    QUARTER(Payment_Date) AS Quarter,
    SUM(Amount) AS Total_Fees
FROM Payment
GROUP BY YEAR(Payment_Date), QUARTER(Payment_Date)
ORDER BY Year, Quarter;

-- (iv-b) Annual fees (from Payment table)
SELECT
    YEAR(Payment_Date) AS Year,
    SUM(Amount) AS Total_Fees
FROM Payment
GROUP BY YEAR(Payment_Date)
ORDER BY Year;

-- (v) Top 5 most popular programs
SELECT
    pr.Program_ID,
    pr.Program_Name,
    pr.Category,
    t.Full_Name AS Assigned_Trainer,
    COUNT(DISTINCT e.Member_ID) AS Total_Enrolled_Members
FROM Program pr
LEFT JOIN Enrollment e ON e.Program_ID = pr.Program_ID
LEFT JOIN Trainer t ON t.Trainer_ID = pr.Trainer_ID
GROUP BY pr.Program_ID, pr.Program_Name, pr.Category, t.Full_Name
ORDER BY Total_Enrolled_Members DESC, pr.Program_Name
LIMIT 5;
