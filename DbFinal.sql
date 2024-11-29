CREATE TABLE Library_Staff (
    Librarian_ID INT PRIMARY KEY,
    Librarian_Name NVARCHAR(50),
    Librarian_Password NVARCHAR(50)
);

CREATE TABLE Member_Info (
    Member_ID INT PRIMARY KEY,
    Member_Name NVARCHAR(50),
    Member_Password NVARCHAR(50),
    Member_Status NVARCHAR(20)
);

CREATE TABLE Books (
    Book_ID INT PRIMARY KEY,
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
    Room_No INT PRIMARY KEY,
    Time_Slot NVARCHAR(50), -- For storing times like "09:00:00 to 10:00:00"
    Room_Availability NVARCHAR(20),
    Capacity INT
);

CREATE TABLE Bookings (
    Member_ID INT,
    Room_No INT,
    Booking_Date DATE,
    Booking_Time_Slot NVARCHAR(50),
    PRIMARY KEY (Member_ID, Room_No, Booking_Date, Booking_Time_Slot),
    FOREIGN KEY (Member_ID) REFERENCES Member_Info(Member_ID),
    FOREIGN KEY (Room_No) REFERENCES Rooms(Room_No)
);

INSERT INTO Library_Staff  (Librarian_ID, Librarian_Name, Librarian_Password)
VALUES 
(1, 'Hamza', 'hmz123'),
(2, 'Humayun', 'hmy123'),
(3, 'Abdullah', 'abd123');

INSERT INTO Member_Info (Member_ID, Member_Name, Member_Password, Member_Status)
VALUES 
(101, 'Hamza', 'hmz123', 'Active'),
(102, 'Humayun', 'hmy123', 'Active'),
(103, 'Marij', 'mrj123', 'Active'),
(104, 'Mustafa', 'mst123', 'Inactive');

INSERT INTO Books (Book_ID, ISBN, Title, Genre, Author, Rating, Availability, AddedBy_Librarian_ID)
VALUES 
(1, 9780131103627, 'The C Programming Language', 'Programming', 'Kernighan & Ritchie', 5, 'Available', 1),
(2, 9780132350884, 'Clean Code', 'Programming', 'Robert C. Martin', 5, 'Available', 2),
(3, 9780201633610, 'Design Patterns', 'Programming', 'Gamma et al.', 5, 'Issued', 1),
(4, 9780451524935, '1984', 'Fiction', 'George Orwell', 4, 'Available', 3),
(5, 9780743273565, 'The Great Gatsby', 'Fiction', 'F. Scott Fitzgerald', 4, 'Available', 2);

INSERT INTO Issued_Books (Member_ID, Book_ID, Issue_Date, Due_Date, Return_Date)
VALUES 
(101, 3, '2024-11-01', '2024-11-15', NULL), -- Book issued by John Doe
(103, 4, '2024-11-05', '2024-11-20', '2024-11-19'); -- Book returned by Michael Brown

INSERT INTO Rooms (Room_No, Time_Slot, Room_Availability, Capacity)
VALUES 
(101, '09:00:00 to 10:00:00', 'Available', 10),
(102, '10:00:00 to 11:00:00', 'Booked', 8),
(103, '11:00:00 to 12:00:00', 'Available', 15),
(104, '12:00:00 to 01:00:00', 'Available', 12),
(105, '01:00:00 to 02:00:00', 'Available', 10);

INSERT INTO Bookings (Member_ID, Room_No, Booking_Date, Booking_Time_Slot)
VALUES 
(101, 102, '2024-11-01', '10:00:00 to 11:00:00'), -- Room booked by John Doe
(104, 105, '2024-11-05', '01:00:00 to 02:00:00'); -- Room booked by Emily Davis

