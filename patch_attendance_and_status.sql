USE fitlife_groupd;


ALTER TABLE `Class`
    ADD COLUMN IF NOT EXISTS Class_Status ENUM('Active','Cancelled','Completed') NOT NULL DEFAULT 'Active';


CREATE TABLE IF NOT EXISTS MemberClassAttendance (
    Attendance_ID INT AUTO_INCREMENT PRIMARY KEY,
    Member_ID INT NOT NULL,
    Class_ID INT NOT NULL,
    Attendance_Status ENUM('Attended','Absent') NOT NULL DEFAULT 'Attended',
    Checkin_Time DATETIME NULL,
    UNIQUE KEY uq_member_class (Member_ID, Class_ID),
    FOREIGN KEY (Member_ID) REFERENCES Member(Member_ID),
    FOREIGN KEY (Class_ID) REFERENCES `Class`(Class_ID)
);

-- Dummy class statuses 
UPDATE `Class`
SET Class_Status = CASE
    WHEN Class_ID IN (1,2,3,4,5,6) THEN 'Completed'
    WHEN Class_ID IN (9) THEN 'Cancelled'
    ELSE 'Active'
END;

-- Dummy attendance data 
INSERT IGNORE INTO MemberClassAttendance (Member_ID, Class_ID, Attendance_Status, Checkin_Time) VALUES
(1001, 1, 'Attended', '2025-01-05 06:55:00'),
(1001, 3, 'Attended', '2025-01-05 17:55:00'),
(1002, 2, 'Attended', '2025-01-05 08:55:00'),
(1002, 8, 'Attended', '2025-01-08 08:58:00'),
(1003, 4, 'Attended', '2025-01-06 09:55:00'),
(1003, 7, 'Absent',   NULL),
(1004, 2, 'Absent',   NULL),
(1005, 3, 'Attended', '2025-01-05 17:58:00'),
(1005, 6, 'Attended', '2025-01-07 13:55:00');
