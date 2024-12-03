CREATE TABLE Library_Staff (
    Librarian_ID INT IDENTITY(1,1) PRIMARY KEY,
    Librarian_Name NVARCHAR(50),
    Librarian_Password NVARCHAR(50)
);

CREATE TABLE Member_Info (
    Member_ID int IDENTITY(1,1) PRIMARY KEY,
    Member_Name NVARCHAR(50),
    Member_Password NVARCHAR(50),
    Member_Status NVARCHAR(20)
);

CREATE TABLE Books (
    Book_ID int IDENTITY(1,1) PRIMARY KEY,
    ISBN BIGINT, -- To handle larger ISBN values
    Title NVARCHAR(100),
    Genre NVARCHAR(50),
    Author NVARCHAR(100),
    Rating INT,
    Availability NVARCHAR(20),
    AddedBy_Librarian_ID INT,
    FOREIGN KEY (AddedBy_Librarian_ID) REFERENCES Library_Staff(Librarian_ID)
);

CREATE TABLE Issued_Books (
    Member_ID INT,
    Book_ID INT,
    Issue_Date DATE,
    Due_Date DATE,
    Return_Date DATE,
    PRIMARY KEY (Member_ID, Book_ID),
    FOREIGN KEY (Member_ID) REFERENCES Member_Info(Member_ID),
    FOREIGN KEY (Book_ID) REFERENCES Books(Book_ID)
);

CREATE TABLE Rooms (
    Room_No INT,                      -- First column of the composite key
    Time_Slot NVARCHAR(50),           -- Second column of the composite key
    Room_Availability NVARCHAR(20),
    Capacity INT,
    PRIMARY KEY (Room_No, Time_Slot)  -- Composite primary key
);

CREATE TABLE Bookings (
    Booking_ID INT IDENTITY PRIMARY KEY, -- Unique ID for each booking
    Member_ID INT,                      -- Foreign key to Members table
    Room_No INT,                        -- Foreign key part 1
    Booking_Time_Slot NVARCHAR(50),     -- Foreign key part 2
    Booking_Date DATE,
    FOREIGN KEY (Room_No, Booking_Time_Slot) 
        REFERENCES Rooms (Room_No, Time_Slot) -- Reference composite key
);


-- Insert Library Staff
SET IDENTITY_INSERT Library_Staff ON;
INSERT INTO Library_Staff (Librarian_ID, Librarian_Name, Librarian_Password)
VALUES 
(1, 'Hamza.boghani', 'hmz123'),
(2, 'Humayun.riaz', 'hmy123'),
(3, 'Abdullah.khan', 'abd123');
SET IDENTITY_INSERT Library_Staff off;
-- Insert Members
SET IDENTITY_INSERT Member_Info ON;
INSERT INTO Member_Info (Member_ID, Member_Name, Member_Password, Member_Status)
VALUES 
(101, 'Hamza Mahser', 'hmz123', 'Active'),
(102, 'Humayun Abuzar', 'hmy123', 'Active'),
(103, 'Marij Malik', 'mrj123', 'Active'),
(104, 'Mustafa Azhar', 'mst123', 'Inactive'); -- Ensure these IDs exist for reference
SET IDENTITY_INSERT Member_Info off;
-- Insert Books
SET IDENTITY_INSERT Books ON;
INSERT INTO Books (Book_ID, ISBN, Title, Genre, Author, Rating, Availability, AddedBy_Librarian_ID)
VALUES 
(1, 9780131103627, 'The C Programming Language', 'Programming', 'Kernighan & Ritchie', 5, 'Available', 1),
(2, 9780132350884, 'Clean Code', 'Programming', 'Robert C. Martin', 5, 'Available', 2),
(3, 9780201633610, 'Design Patterns', 'Programming', 'Gamma et al.', 5, 'Issued', 1),
(4, 9780451524935, '1984', 'Fiction', 'George Orwell', 4, 'Available', 3),
(5, 9780743273565, 'The Great Gatsby', 'Fiction', 'F. Scott Fitzgerald', 4, 'Available', 2); -- Ensure AddedBy_Librarian_ID exists
SET IDENTITY_INSERT Books off;
-- Insert Issued Books
-- Ensure that Member_ID and Book_ID exist in the respective tables
INSERT INTO Issued_Books (Member_ID, Book_ID, Issue_Date, Due_Date, Return_Date)
VALUES 
(101, 3, '2024-11-01', '2024-11-15', NULL), -- Member_ID=101 and Book_ID=3 exist
(103, 4, '2024-11-05', '2024-11-20', '2024-11-19'); -- Member_ID=103 and Book_ID=4 exist

-- Insert Rooms
-- Insert time slots with more "Booked" statuses

INSERT INTO Rooms (Room_No, Time_Slot, Room_Availability, Capacity)
VALUES 
(101, '09:00:00 to 10:00:00', 'Available', 10),
(101, '10:00:00 to 11:00:00', 'Booked', 10),
(101, '11:00:00 to 12:00:00', 'Booked', 10),
(101, '12:00:00 to 13:00:00', 'Booked', 10),
(101, '13:00:00 to 14:00:00', 'Available', 10),
(101, '14:00:00 to 15:00:00', 'Available', 10),

(102, '09:00:00 to 10:00:00', 'Booked', 10),
(102, '10:00:00 to 11:00:00', 'Booked', 10),
(102, '11:00:00 to 12:00:00', 'Booked', 10),
(102, '12:00:00 to 13:00:00', 'Available', 10),
(102, '13:00:00 to 14:00:00', 'Available', 10),
(102, '14:00:00 to 15:00:00', 'Available', 10),

(103, '09:00:00 to 10:00:00', 'Available', 8),
(103, '10:00:00 to 11:00:00', 'Available', 8),
(103, '11:00:00 to 12:00:00', 'Booked', 8),
(103, '12:00:00 to 13:00:00', 'Booked', 8),
(103, '13:00:00 to 14:00:00', 'Booked', 8),
(103, '14:00:00 to 15:00:00', 'Available', 8),

(104, '09:00:00 to 10:00:00', 'Booked', 10),
(104, '10:00:00 to 11:00:00', 'Booked', 10),
(104, '11:00:00 to 12:00:00', 'Available', 10),
(104, '12:00:00 to 13:00:00', 'Booked', 10),
(104, '13:00:00 to 14:00:00', 'Available', 10),
(104, '14:00:00 to 15:00:00', 'Available', 10),

(105, '09:00:00 to 10:00:00', 'Booked', 10),
(105, '10:00:00 to 11:00:00', 'Booked', 10),
(105, '11:00:00 to 12:00:00', 'Booked', 10),
(105, '12:00:00 to 13:00:00', 'Available', 10),
(105, '13:00:00 to 14:00:00', 'Available', 10),
(105, '14:00:00 to 15:00:00', 'Available', 10);


-- Insert Bookings
-- Ensure that Member_ID and Room_No exist in the respective tables
-- Insert new bookings for the "Booked" time slots
INSERT INTO Bookings (Member_ID, Room_No, Booking_Date, Booking_Time_Slot)
VALUES 
(101, 101, '2024-11-01', '10:00:00 to 11:00:00'), -- Member 101 booked Room 101
(102, 101, '2024-11-01', '11:00:00 to 12:00:00'), -- Member 102 booked Room 101
(103, 101, '2024-11-01', '12:00:00 to 13:00:00'), -- Member 103 booked Room 101

(104, 102, '2024-11-02', '09:00:00 to 10:00:00'), -- Member 104 booked Room 102
(101, 102, '2024-11-02', '10:00:00 to 11:00:00'), -- Member 105 booked Room 102
(101, 102, '2024-11-02', '11:00:00 to 12:00:00'), -- Member 106 booked Room 102

(102, 103, '2024-11-03', '11:00:00 to 12:00:00'), -- Member 107 booked Room 103
(103, 103, '2024-11-03', '12:00:00 to 13:00:00'), -- Member 108 booked Room 103
(104, 103, '2024-11-03', '13:00:00 to 14:00:00'), -- Member 109 booked Room 103

(101, 104, '2024-11-04', '09:00:00 to 10:00:00'), -- Member 110 booked Room 104
(102, 104, '2024-11-04', '10:00:00 to 11:00:00'), -- Member 111 booked Room 104
(103, 104, '2024-11-04', '12:00:00 to 13:00:00'), -- Member 112 booked Room 104

(104, 105, '2024-11-05', '09:00:00 to 10:00:00'), -- Member 113 booked Room 105
(101, 105, '2024-11-05', '10:00:00 to 11:00:00'), -- Member 114 booked Room 105
(102, 105, '2024-11-05', '11:00:00 to 12:00:00'); -- Member 115 booked Room 105