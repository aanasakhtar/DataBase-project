from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QMessageBox,QButtonGroup, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView, QAbstractItemView
import sys
import pyodbc

def show_message(parent, title, message):
    # Utility function to show a message box
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec()

screens = []


class DatabaseConnection:
    def __init__(self):
        # self.server = "DESKTOP-CHMOJM3\SQLEXPRESS" # Anas
        self.server = 'DESKTOP-9QAGOMJ\SQLSERVER1' # Hamza
        # self.server = 'LAPTOP-N8UU3FAP\\SQLSERVER1' #Zoraiz
        self.database = 'DbFinal'
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        # Connect to the database
        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes'
        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()

    def get_cursor(self):
        # Return the cursor for executing queries
        return self.cursor

    def get_connection(self):
        # Return the database connection
        return self.connection

db = DatabaseConnection()


############################################ MODULE 1 ################################################### 

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Main_screen.ui', self)

        # Initialize the shared database connection
        self.db = DatabaseConnection()  # Create a shared database connection

        # Connect buttons to their corresponding functions
        self.CreateAccount_Button.clicked.connect(self.open_create_account)
        self.Signin_Customer_Button.clicked.connect(self.open_sign_in)
        self.Signin_Librarian_Button.clicked.connect(self.open_sign_in)

    def open_create_account(self):
        # Pass the shared database connection to CreateAccount
        self.creatingAcc = CreateAccount(self.db)
        self.creatingAcc.show()

    def open_sign_in(self):
        # Pass the shared database connection to SignIn
        self.signIn = SignIn(self.db)
        screens.append(self.signIn)
        self.signIn.show()



            
class CreateAccount(QtWidgets.QMainWindow):  
    def __init__(self, db_connection: DatabaseConnection):
        super().__init__() 
        # Load the .ui file
        uic.loadUi('Create_account.ui', self)
        self.resize(600, 400)

        # Store the DatabaseConnection instance directly
        self.db = db_connection  # Keep the entire DatabaseConnection object
        self.cursor = db_connection.get_cursor()  # Access the cursor from the DatabaseConnection object

        self.usernameF = self.findChild(QtWidgets.QLineEdit, "Username")
        self.passwordF = self.findChild(QtWidgets.QLineEdit, "password")
        self.cPasswordF = self.findChild(QtWidgets.QLineEdit, "c_password")
        self.passwordF.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.cPasswordF.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        
        self.submitBtn = self.findChild(QtWidgets.QPushButton, "submit")
        self.submitBtn.clicked.connect(self.create_account)

    def create_account(self):
        username = self.usernameF.text()
        password = self.passwordF.text()
        c_password = self.cPasswordF.text()

        if not username or not password or not c_password:
            show_message(self, "Error", "All fields must be filled.")
            return

        if password != c_password:
            show_message(self,"Error", "Passwords do not match.")
            return

        for i in username:
            if not i.isalpha():
                show_message(self, "Error", "Username only contains alphabets.")
                return
        
        check_query = """
                        SELECT COUNT(*)
                        FROM Member_Info
                        WHERE Member_Name = ?
                    """
        cursor = self.db.get_cursor()  # Reuse the cursor from the shared connection
        cursor.execute(check_query, (username,))
        result = cursor.fetchone()

        if result[0] > 0:
            show_message(self, "Error", "Username already exists.")
            return
        
        try:
            # Insert data into the database
            self.add_to_database(username, password)
            show_message(self, "Success", "Account created successfully!")
        except Exception as e:
            show_message(self, "Error", f"Failed to create account: {e}")

    def add_to_database(self, username, password):
        # Use the cursor directly
        cursor = self.db.get_cursor()  # Access the cursor from the DatabaseConnection object
        
        sql_query = """
            INSERT INTO Member_Info(Member_Name, Member_Password, Member_Status)
            VALUES (?, ?, ?)
        """
        cursor.execute(sql_query, (username, password, "Active"))

        self.db.get_connection().commit()  # Commit using the shared connection

        self.close()



    


class SignIn(QtWidgets.QMainWindow):
    def __init__(self, db):
        super().__init__()
        # Load the .ui file
        uic.loadUi('Sign_in.ui', self)

        # Store the database connection object
        self.db = db
        self.librarian_id = None  # Initialize librarian_id

        self.usernameF = self.findChild(QtWidgets.QLineEdit, "Enter_Username_Edit")
        self.passwordF = self.findChild(QtWidgets.QLineEdit, "Enter_Password_Edit")
        self.passwordF.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        
        self.signinBtn = self.findChild(QtWidgets.QPushButton, "signinBtn")  # Ensure button is connected
        self.signinBtn.clicked.connect(self.signin)

    def signin(self):
        self.username = self.usernameF.text()
        self.password = self.passwordF.text()
        if "." in self.username:
            self.signInAsLibrarian(self.username, self.password)
        else:
            self.signInAsMember(self.username, self.password)

    def signInAsLibrarian(self, username, password):
        if not username or not password:
            show_message(self, "Error", "Please enter both username and password.")
            return
    
        sql_query = """
            select Librarian_ID, Librarian_Password from Library_Staff where Librarian_Name = ?
        """
        cursor = self.db.get_cursor()  # Use the cursor from DatabaseConnection
        cursor.execute(sql_query, (username,))
        result = cursor.fetchone()

        if result is None:
            show_message(self, "Error", "No username found")
            return
        if password != result[1]:  # Use the second column (password) to check
            show_message(self, "Error", "Incorrect Password")
            return

        self.librarian_id = result[0]
        self.openLibrarianScreen()


    def openLibrarianScreen(self):
        self.librarianScreen = Admin_or_Librarian(self.db, self.librarian_id)  # Pass db and librarian_id to the screen
        screens.append(self.librarianScreen)
        self.librarianScreen.show()

    def signInAsMember(self, username, password):
        sql_query = """
            SELECT Member_Password, Member_Status FROM Member_Info WHERE Member_Name = ?
        """
        cursor = self.db.get_cursor()  # Correctly retrieve the cursor here
        try:
            cursor.execute(sql_query, (username,))
            result = cursor.fetchone()
            
            if result is None:
                show_message(self, "Error", "No username found")
                return
            if result[1] == "Inactive":
                show_message(self, "Warning", "User is blocked")
                return
            if password != result[0]:
                show_message(self, "Error", "Incorrect Password")
                return
            
            self.openMemberScreen()
        except Exception as e:
            show_message(self, "Error", f"Database error: {e}")


    def openMemberScreen(self): 
        self.memberScreen = MemberScreen(self.usernameF.text(), self.db)  # Pass db to Member screen
        screens.append(self.memberScreen)
        self.memberScreen.show()
    




############################################ MODULE 2 ################################################### 

class Admin_or_Librarian(QtWidgets.QMainWindow):  
    def __init__(self, db_connection: DatabaseConnection, librarian_id):
        super().__init__() 
        uic.loadUi('Admin_or_Librarian.ui', self)

        # Store the shared DatabaseConnection object
        self.db_connection = db_connection
        self.librarian_id = librarian_id

        # To store same instances for future use
        self.inventory_window = None
        self.members_window = None

        # Connect buttons
        self.Inventory_Button.clicked.connect(self.open_inventory)
        self.Members_Button.clicked.connect(self.open_members)

        self.LogOut_Button.clicked.connect(self.logout_lib)

    def open_inventory(self):
        if self.inventory_window is None:
            # Pass the DatabaseConnection object to the Inventory window
            self.inventory_window = Inventory(self.db_connection, self.librarian_id)
        self.inventory_window.show()

    def open_members(self):
        if self.members_window is None:
            # Pass the DatabaseConnection object to the Members window
            self.members_window = Members(self.db_connection)
        self.members_window.show()
    
    def logout_lib(self):
        for screen in screens:
            screen.close()
        self.close()
        


class Inventory(QtWidgets.QMainWindow):
    def __init__(self, db_connection: DatabaseConnection, librarian_id, parent=None):
        super().__init__(parent)  # Pass the parent to the parent class constructor
        uic.loadUi('Inventory.ui', self)

        # Store the shared DatabaseConnection object
        self.db_connection = db_connection
        self.librarian_id = librarian_id

        # To store same instances for future use
        self.room_inventory_window = None
        self.book_inventory_window = None

        # Connect buttons
        self.RoomInventory_Button.clicked.connect(self.open_room_inventory)
        self.BookInventory_Button.clicked.connect(self.open_book_inventory)

    def open_room_inventory(self):
        if self.room_inventory_window is None:
            # Pass the full DatabaseConnection object to the Room_inventory window
            self.room_inventory_window = Room_inventory(self.db_connection)
        self.room_inventory_window.show()

    def open_book_inventory(self):
        if self.book_inventory_window is None:
            # Pass both db_connection and librarian_id to the Book_Inventory window
            self.book_inventory_window = Book_Inventory(self.db_connection, self.librarian_id)
        self.book_inventory_window.show()



class Room_inventory(QtWidgets.QMainWindow):
    def __init__(self, db_connection: DatabaseConnection, parent=None):
        super().__init__(parent)
        uic.loadUi('Room_inventory.ui', self)

        # Accessing widgets from the UI
        self.room_table = self.findChild(QtWidgets.QTableWidget, 'Room_Table')
        self.update_button = self.findChild(QtWidgets.QPushButton, 'Update_Button')
        self.time_slots_button = self.findChild(QtWidgets.QPushButton, 'TimeSlots_Button')

        # Store the shared DatabaseConnection object
        self.db_connection = db_connection

        # To store same instances for future use
        self.time_slots_window = None

        # Connect button clicks to their respective methods
        self.update_button.clicked.connect(self.update_room)
        self.time_slots_button.clicked.connect(self.open_time_slots)

        self.populate_room_table()

        # Allow row selection by default
        self.room_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    def populate_room_table(self):
        # Get the cursor from DatabaseConnection
        cursor = self.db_connection.get_cursor()
        
        # Query to fetch room details along with the username of the person who booked the room
        query = """
        SELECT r.Room_No, r.Room_Availability, r.Capacity, m.Member_Name
        FROM Rooms r
        LEFT JOIN Bookings b ON r.Room_No = b.Room_No AND r.Time_Slot = b.Booking_Time_Slot
        LEFT JOIN Member_Info m ON b.Member_ID = m.Member_ID
        """
        
        # Execute the query and fetch all results
        cursor.execute(query)
        rooms = cursor.fetchall()  # Get all rows from the query

        # Clear the table before populating it with new data
        self.room_table.clearContents()
        self.room_table.setRowCount(0)

        # Populate the table with room data
        for row_idx, room in enumerate(rooms):
            room_no, availability, capacity, booked_by = room

            # Create table items for each column
            room_no_item = QtWidgets.QTableWidgetItem(str(room_no))
            availability_item = QtWidgets.QTableWidgetItem(availability)
            booked_by_item = QtWidgets.QTableWidgetItem(booked_by if booked_by else '')
            capacity_item = QtWidgets.QTableWidgetItem(str(capacity))

            # Add items to the respective columns
            self.room_table.insertRow(row_idx)  # Dynamically add a row for each entry
            self.room_table.setItem(row_idx, 0, room_no_item)
            self.room_table.setItem(row_idx, 1, availability_item)
            self.room_table.setItem(row_idx, 2, booked_by_item)
            self.room_table.setItem(row_idx, 3, capacity_item)

        # Set the table as read-only while allowing row selection
        self.room_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.room_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.room_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)


    def update_room(self):
        cursor = self.db_connection.get_cursor()  # Get the cursor from DatabaseConnection
        selected_row = self.room_table.currentRow()

        if selected_row != -1:
            # Get the room number and availability from the selected row in the table
            room_no = self.room_table.item(selected_row, 0).text()  # Room number (first column)
            availability = self.room_table.item(selected_row, 1).text()  # Availability status (second column)

            # Fetch the corresponding time slot for the selected room from the Rooms table
            fetch_time_slot_query = """
            SELECT Time_Slot
            FROM Rooms
            WHERE Room_No = ? AND Room_Availability = 'Booked'
            """
            cursor.execute(fetch_time_slot_query, (room_no,))
            time_slot = cursor.fetchone()

            # If no time slot is found, show an error
            if time_slot is None:
                QtWidgets.QMessageBox.warning(self, "Invalid Action", "Room is not booked or time slot is missing.")
                return
            
            time_slot = time_slot[0]  # Extract the time slot from the result


            if availability == "Booked":
                try:
                    # Remove the booking for the specific time slot from the Bookings table
                    delete_query = """
                    DELETE FROM Bookings
                    WHERE Room_No = ? AND Booking_Time_Slot = ?
                    """
                    cursor.execute(delete_query, (room_no, time_slot))
                    self.db_connection.get_connection().commit()  # Commit the delete operation

                    # Update the Room_Availability to 'Available' for that specific room and time slot
                    # Here we ensure that we update the correct room and time slot in the Rooms table
                    update_query = """
                    UPDATE Rooms
                    SET Room_Availability = 'Available'
                    WHERE Room_No = ? AND Time_Slot = ?
                    """
                    cursor.execute(update_query, (room_no, time_slot))
                    self.db_connection.get_connection().commit()  # Commit the update operation

                    # Update the table in the UI (change the availability of the selected row)
                    self.room_table.item(selected_row, 1).setText("Available")  # Update the availability for the specific time slot
                    self.room_table.setItem(selected_row, 2, QtWidgets.QTableWidgetItem(""))  # Clear the 'BookedBy' field

                    QtWidgets.QMessageBox.information(self, "Room Updated", f"Room {room_no} for time slot {time_slot} is now available.")

                except Exception as e:
                    self.db_connection.get_connection().rollback()  # Rollback in case of error
                    QtWidgets.QMessageBox.warning(self, "Error", f"Failed to update room: {str(e)}")
            else:
                QtWidgets.QMessageBox.warning(self, "Invalid Action", "Room is not booked.")


    def open_time_slots(self):
        # Get the selected row index
        selected_row = self.room_table.currentRow()

        # If a row is selected
        if selected_row != -1:  
            # Get the room number from the selected row
            self.selected_room_no = self.room_table.item(selected_row, 0).text()  # Get the room number

            # Temporarily disable selection mode when opening the time slots window
            self.room_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

            # Show the TimeSlots window if it hasn't been shown yet
            if self.time_slots_window is None:
                self.time_slots_window = QtWidgets.QMainWindow()  # Create the TimeSlots window
                uic.loadUi('time_slots.ui', self.time_slots_window)  # Load the UI

            # Now populate the time slots table in the UI
            self.populate_time_slots()

            # Show the TimeSlots window
            self.time_slots_window.show()

            # Re-enable row selection mode after showing the time slots window
            self.room_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)


    def populate_time_slots(self):
        # Access the table widget in the time slots window
        time_slots_table = self.time_slots_window.findChild(QtWidgets.QTableWidget, 'tableWidget')

        # Get the selected row from the room inventory screen
        selected_row = self.room_table.currentRow()

        # Get the room number for the selected row (the first column of the selected row)
        room_no = self.room_table.item(selected_row, 0).text()

        # Get cursor from the database connection
        cursor = self.db_connection.get_cursor()

        # Query to fetch the TimeSlots for the selected RoomNo
        cursor.execute("""
            SELECT Time_Slot, Room_Availability
            FROM Rooms
            WHERE Room_No = ?
        """, (room_no,))

        # Fetch all time slots for the selected room
        rows = cursor.fetchall()  # Fetch all rows for the selected room

        # Clear the time slots table before populating it with new data
        time_slots_table.clearContents()
        time_slots_table.setRowCount(0)

        # Set the row count in the time slots table widget
        time_slots_table.setRowCount(len(rows))

        # Loop through the fetched rows and populate the time slots table widget
        for row_idx, row in enumerate(rows):
            time_slots = row[0]  # Time slots string (e.g., "09:00:00 to 10:00:00")
            booked = row[1]  # Room availability status (e.g., 'Booked' or 'Available')

            # Split the TimeSlots string to extract StartTime and EndTime
            start_time, end_time = time_slots.split(' to ')

            # Slot ID will start from 1 and auto-increment for each time slot
            slot_id = row_idx + 1

            # Populate the table with the time slot details
            time_slots_table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(slot_id)))  # Slot ID
            time_slots_table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(start_time))  # Start Time
            time_slots_table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(end_time))    # End Time
            time_slots_table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(booked)))  # Room Availability (Booked/Available)

        # Make the time slots table uneditable and unselectable
        time_slots_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        time_slots_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)


class Book_Inventory(QtWidgets.QMainWindow):
    def __init__(self, db_connection: DatabaseConnection, librarian_id, parent=None):
        super().__init__(parent)
        uic.loadUi('book_inventory.ui', self)

        self.db_connection = db_connection
        self.librarian_id = librarian_id  # Store the current logged-in librarian ID

        # To store instances for future use
        self.issued_books_window = None
        self.add_book_window = None

        self.books_table = self.findChild(QtWidgets.QTableWidget, 'Books_Table')
        self.add_book_button = self.findChild(QtWidgets.QPushButton, 'AddBook_Button')
        self.issued_books_button = self.findChild(QtWidgets.QPushButton, 'IssuedBooks_Button')

        self.issued_books_button.clicked.connect(self.show_issued_books)
        self.add_book_button.clicked.connect(self.open_add_book_screen)

        self.populate_books_table()

        self.UpdatePB.clicked.connect(self.updateTheBookInventory)

    def populate_books_table(self):
        cursor = self.db_connection.get_cursor()

        # Query to get book details
        query = """
        SELECT ISBN, Title, Genre, Author, Rating, Availability, AddedBy_Librarian_ID
        FROM Books
        """
        cursor.execute(query)
        books = cursor.fetchall()

        # Clear the table before populating it with new data
        self.books_table.clearContents()
        self.books_table.setRowCount(0)

        # Set the row count based on the number of books in the result
        self.books_table.setRowCount(len(books))

        # Populate the table with book data
        for row_idx, book in enumerate(books):
            isbn, title, genre, author, rating, availability, added_by = book

            # Create table items for each column
            isbn_item = QtWidgets.QTableWidgetItem(str(isbn))
            title_item = QtWidgets.QTableWidgetItem(title)
            genre_item = QtWidgets.QTableWidgetItem(genre)
            author_item = QtWidgets.QTableWidgetItem(author)
            rating_item = QtWidgets.QTableWidgetItem(str(rating))
            availability_item = QtWidgets.QTableWidgetItem(availability)
            added_by_item = QtWidgets.QTableWidgetItem(str(added_by))

            # Add items to the respective columns
            self.books_table.setItem(row_idx, 0, isbn_item)
            self.books_table.setItem(row_idx, 1, title_item)
            self.books_table.setItem(row_idx, 2, genre_item)
            self.books_table.setItem(row_idx, 3, author_item)
            self.books_table.setItem(row_idx, 4, rating_item)
            self.books_table.setItem(row_idx, 5, added_by_item)
            self.books_table.setItem(row_idx, 6, availability_item)

        # Set the table as uneditable and disable selection
        self.books_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.books_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)

        # Resize columns to fit contents
        self.books_table.resizeColumnsToContents()


    def show_issued_books(self):
        if self.issued_books_window is None:
            self.issued_books_window = QtWidgets.QMainWindow(self)
            uic.loadUi('Issued_book.ui', self.issued_books_window)

        table_widget = self.issued_books_window.findChild(QtWidgets.QTableWidget, 'tableWidget')

        # Query to fetch issued books data
        query = """
        SELECT 
            b.ISBN,
            b.Title,
            m.Member_Name AS Issued_To,
            ib.Due_Date,
            ib.Issue_Date,
            ib.Return_Date
        FROM 
            Issued_Books ib
        INNER JOIN 
            Books b ON ib.Book_ID = b.Book_ID
        INNER JOIN 
            Member_Info m ON ib.Member_ID = m.Member_ID;
        """

        cursor = self.db_connection.get_cursor()
        cursor.execute(query)
        records = cursor.fetchall()

        # Populate UI
        table_widget.setRowCount(0)  # Clear existing rows
        table_widget.setRowCount(len(records))
        for row_idx, record in enumerate(records):
            for col_idx, data in enumerate(record):
                item = QtWidgets.QTableWidgetItem(str(data) if data is not None else "")
                table_widget.setItem(row_idx, col_idx, item)

        table_widget.resizeColumnsToContents()
        table_widget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table_widget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)

        self.issued_books_window.show()


    def open_add_book_screen(self):
        # Open the Add Book screen with the current librarian ID
        add_book_window = AddBookScreen(self.db_connection, self.librarian_id, parent=self)
        add_book_window.show()

    def updateTheBookInventory(self):
        # Get the currently selected row
        selected_row = self.Books_Table.currentRow()
        
        if selected_row == -1:  # No row selected
            show_message(self, "Error", "No book selected.")
            return

        # Assuming the Book_ID is in the first column
        book_isbn_item = self.Books_Table.item(selected_row, 0)
        if book_isbn_item is None:
            show_message(self, "Error", "Book ID not found in the selected row.")
            return

        book_isbn = book_isbn_item.text()

        cursor = self.db_connection.get_cursor()
        find_query = """
            SELECT Book_ID, Availability FROM Books WHERE ISBN = ? 
        """
        cursor.execute(find_query, (int(book_isbn),))
        result = cursor.fetchone()
        print(int(book_isbn), result)
        if result is None:
            show_message(self, "Error", "Book not found in the database.")
            return

        book_id, availability = result
        if availability == "Available":
            show_message(self, "Info", "Book is already marked as available.")
            return

        # Get the current date
        current_date = QDate.currentDate().toString("yyyy-MM-dd")

        # Updat book to "Available" in Books table
        update_query = """
            UPDATE Books
            SET Availability = 'Available'
            WHERE ISBN = ?
        """
        cursor.execute(update_query, (book_isbn,))

        # Update the return_date in Issued_Books table to current date
        update_return_date_query = """
            UPDATE Issued_Books
            SET Return_Date = ?
            WHERE Book_ID = ?
        """
        cursor.execute(update_return_date_query, (current_date, book_id))

        self.db_connection.get_connection().commit()

        # Refresh the table
        self.populate_books_table()
        show_message(self, "Success", "Book inventory updated successfully.")


class AddBookScreen(QtWidgets.QMainWindow):
    def __init__(self, db_connection: DatabaseConnection, librarian_id, parent=None):
        super().__init__(parent)
        uic.loadUi('Add_book.ui', self)

        self.isbn_edit = self.findChild(QtWidgets.QLineEdit, 'Isbn_Edit')
        self.title_edit = self.findChild(QtWidgets.QLineEdit, 'Title_Edit')
        self.genre_combobox = self.findChild(QtWidgets.QComboBox, 'Genre_Combobox')
        self.author_edit = self.findChild(QtWidgets.QLineEdit, 'Author_Edit')
        self.confirm_button = self.findChild(QtWidgets.QPushButton, 'Confirm_Button')

        self.librarian_id = librarian_id
        self.db_connection = db_connection
        self.cursor = self.db_connection.get_cursor()

        # Populate the genre combobox
        self.populate_genre_combobox()

        self.confirm_button.clicked.connect(self.add_book_to_database)

    def populate_genre_combobox(self):
        # Populates the genre combobox with distinct genres from the database
        query = "SELECT DISTINCT genre FROM Books"
        self.cursor.execute(query)
        genres = [row[0] for row in self.cursor.fetchall()]
        self.genre_combobox.addItems(genres)
    
    def add_book_to_database(self):
        isbn = self.isbn_edit.text()
        title = self.title_edit.text()
        genre = self.genre_combobox.currentText()
        author = self.author_edit.text()

        # Check if all required fields are filled
        if not isbn or not title or not genre or not author:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return
        
        availability = "Available"
        
        # Query to insert new book
        query = """
        INSERT INTO Books (ISBN, Title, Genre, Author, Availability, AddedBy_Librarian_ID)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (isbn, title, genre, author, availability, self.librarian_id))
        self.cursor.connection.commit()  # Commit the transaction to the database

        QtWidgets.QMessageBox.information(self, "Success", "Book added successfully.")
        self.close()

        # # Refresh book inventory table in Book_Inventory
        if self.parent():
            self.parent().populate_books_table()


class Members(QtWidgets.QMainWindow):
    def __init__(self, db_connection: DatabaseConnection, parent=None):
        super().__init__(parent)
        uic.loadUi('Members.ui', self)

        # Store the database connection object
        self.db_connection = db_connection
        self.cursor = self.db_connection.get_cursor()  # Use the cursor from the DatabaseConnection object

        # Connect the 'BlockButton' to the block_member function
        self.BlockButton.clicked.connect(self.block_member)

        # Populate the Members table
        self.populate_members_table()

    def populate_members_table(self):
        query = """
        SELECT m.Member_ID, m.Member_Name, m.Member_Password, m.Member_Status, b.Title
        FROM Member_Info m
        LEFT JOIN Issued_Books ib ON m.Member_ID = ib.Member_ID
        LEFT JOIN Books b ON ib.Book_ID = b.Book_ID
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Set row count for the table
        self.Members_Table.setRowCount(len(rows))

        # Loop through the rows and populate the table
        for row_idx, row in enumerate(rows):
            member_id = row[0]
            member_name = row[1]
            member_password = row[2]
            status = row[3]
            book_issued = row[4] if row[4] else 'None'  # If no book issued, display 'None'

            self.Members_Table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(member_id)))  # Users
            self.Members_Table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(member_name))  # Username
            self.Members_Table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(book_issued)))  # Book Title
            self.Members_Table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(status))  # Member_Status

    def block_member(self):
        selected_row = self.Members_Table.currentRow()

        if selected_row != -1:  # If a row is selected
            # Username is used as a unique identification for the query
            username = self.Members_Table.item(selected_row, 1).text()  # Assuming username is in column 1
            current_status = self.Members_Table.item(selected_row, 3).text()  # Assuming status is in column 3

            if current_status != "Inactive":
                # Update the status of the member to 'Inactive' in the database
                query = "UPDATE Member_Info SET Member_Status = ? WHERE Member_Name = ?"
                self.cursor.execute(query, ('Inactive', username))
                self.db_connection.get_connection().commit()  # Commit the transaction to the database

                # Update status in the UI (Table)
                self.Members_Table.item(selected_row, 3).setText("Inactive")
                QtWidgets.QMessageBox.information(self, "Success", f"Member {username} has been blocked.")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "This member is already inactive.")


############################################ MODULE 3 ################################################### 

class MemberScreen(QtWidgets.QMainWindow):
    def __init__(self, username, db):
        super().__init__()
        uic.loadUi('Member_or_customer.ui', self)
        self.db = db
        self.SearchIssue_Button.clicked.connect(lambda: self.openSearchScreen(username))
        self.BookRoom_Button.clicked.connect(lambda: self.openBookARoom())
        self.LogoutPB.clicked.connect(self.logout_mem)
    def openSearchScreen(self, username):
        self.searchScreen = SearchScreen(username)
        self.searchScreen.show()
    
    def openBookARoom(self):
        self.bookARoomWindow = BookARoom(self.db)  # Instantiate the BookARoom class
        self.bookARoomWindow.show()  # Show the BookARoom screen

    def logout_mem(self):
        for screen in screens:
            screen.close()
        self.close()

class SearchScreen(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        uic.loadUi("Search.ui", self)
        self.TitleF = self.findChild(QtWidgets.QLineEdit, "TitleLE")
        self.GenreF = self.findChild(QtWidgets.QComboBox, "GenreCB")
        self.AuthorF = self.findChild(QtWidgets.QLineEdit, "AuthorLE")
        self.GenreF.setCurrentIndex(-1)
        
        self.db = DatabaseConnection()
        self.cursor = self.db.get_cursor()

        self.cursor.execute("select Book_ID, ISBN, Title, Genre, Author, Rating, Availability from Books")
        # Fetch all rows and populate the table
        self.BookTW.setColumnCount(7)  # Adjust to match the number of columns in the data
        self.BookTW.setHorizontalHeaderLabels(['Book_ID', 'ISBN', 'Title', 'Genre', 'Author', 'Rating', 'Availability'])
        # self.BookTW.resizeColumnsToContents()  # Automatically adjust column widths
        # Populate the table widget
        for row_index, row_data in enumerate(self.cursor.fetchall()):
            self.BookTW.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):  # No slicing; include all columns
                item = QTableWidgetItem(str(cell_data))
                self.BookTW.setItem(row_index, col_index, item)

        self.SearchPB.clicked.connect(self.search)
        self.ViewPB.clicked.connect(self.view) 
        self.RateABookPB.clicked.connect(self.rateABook)
        self.ViewAllPB.clicked.connect(self.viewAll)
        self.IssuePB.clicked.connect(lambda: self.issue(username))

    def search(self):
        sqlQuery = "select Book_ID, ISBN, Title, Genre, Author, Rating, Availability from Books" 
        parameters = []

        # Add conditions to the WHERE clause only if relevant fields are filled
        conditions = []  # This will hold the conditions (like "Title=?", "Genre=?", etc.)

        if self.TitleF.text():
            conditions.append("Title=?")
            parameters.append(self.TitleF.text())
        
        if self.GenreF.currentText():
            conditions.append("Genre=?")
            parameters.append(self.GenreF.currentText())
        
        if self.AuthorF.text():
            conditions.append("Author=?")
            parameters.append(self.AuthorF.text())

        # If any conditions were added, append them to the query with "WHERE" and "AND"
        if conditions:
            sqlQuery += " WHERE " + " AND ".join(conditions)

        self.cursor.execute(sqlQuery, parameters)

        # Clear existing rows in the table before populating with new data
        self.BookTW.setRowCount(0)

        # Populate table with filtered rows
        for row_index, row_data in enumerate(self.cursor.fetchall()):
            self.BookTW.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):  # No slicing; include all columns
                item = QTableWidgetItem(str(cell_data))
                self.BookTW.setItem(row_index, col_index, item)
    
    def viewAll(self):
        self.BookTW.setRowCount(0)
        self.cursor.execute("select Book_ID, ISBN, Title, Genre, Author, Rating, Availability from Books")

        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(self.cursor.fetchall()):
            self.BookTW.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):  # No slicing; include all columns
                item = QTableWidgetItem(str(cell_data))
                self.BookTW.setItem(row_index, col_index, item)

    def view(self):
        selected_row = self.BookTW.currentRow()
        if selected_row != -1:  # Check if a row is selected
            book_id = self.BookTW.item(selected_row, 0).text()  # Assuming the first column is the book ID
            self.cursor.execute("SELECT * FROM Books WHERE Book_ID = ?", (book_id,))
            book_details = self.cursor.fetchone()
            if book_details:
                # Show the details in a message box or separate window
                details = f"ID: {book_details[0]}\nTitle: {book_details[2]}\nAuthor: {book_details[4]}\nGenre: {book_details[3]}\nAvailability: {book_details[6]}"
                show_message(self, "Book Details", details)
            else:
                show_message(self, "Warning", "Please select a book to view details.")

    def issue(self, username):
        # Issue the selected book to the current user
        selected_row = self.BookTW.currentRow()
        if selected_row != -1:  # Check if a row is selected
            self.cursor.execute("select Member_ID from Member_Info where Member_Name = ?", (username))
            user_id = self.cursor.fetchone()
            user_id = user_id[0]
            book_id = self.BookTW.item(selected_row, 0).text()  # Assuming the first column is the book ID
            self.cursor.execute("SELECT Availability FROM Books WHERE Book_ID = ?", (int(book_id),))
            book_status = self.cursor.fetchone()
            if book_status and book_status[0] == "Available":
                self.cursor.execute("UPDATE Books SET Availability = 'Issued' WHERE Book_ID = ?", (book_id,))
                self.cursor.execute("""
                INSERT INTO Issued_Books (Member_ID, Book_ID, Issue_Date, Due_Date) 
                VALUES (?, ?, GETDATE(), DATEADD(WEEK, 2, GETDATE()))
            """, (user_id, book_id))
                self.db.get_connection().commit()
                show_message(self, "Success", "Book issued successfully!")
                self.BookTW.item(selected_row, 6).setText("Issued")  # Update status in UI
            else:
                show_message(self, "Warning", "The selected book is not available for issuing.")
        else:
            show_message(self, "Warning", "Please select a book to issue.")


    def rateABook(self):
        selected_row = self.BookTW.currentRow()
        if selected_row != -1:  # Check if a row is selected
            book_id = self.BookTW.item(selected_row, 0).text() 
            self.rateScreen = RateScreen(self.db, book_id, self.viewAll)
            self.rateScreen.show()
        else:
            show_message(self, "Warning", "Please select a book to rate.")

class RateScreen(QMainWindow):
    def __init__(self, db_connection: DatabaseConnection, book_id, viewAll):
        super().__init__()
        uic.loadUi("Rate_a_book.ui", self)  # Load the UI for the "Rate a Book" screen
        
        # Initialize database connection and book ID
        self.db = db_connection
        self.book_id = book_id
        self.viewAll = viewAll
        
        
        # Set up QButtonGroup for radio buttons (rating)
        self.rating_group = QButtonGroup(self)
        self.rating_group.addButton(self.radioButton, 1)  # ID 1 for 1-star
        self.rating_group.addButton(self.radioButton_2, 2)  # ID 2 for 2-stars
        self.rating_group.addButton(self.radioButton_3, 3)  # ID 3 for 3-stars
        self.rating_group.addButton(self.radioButton_4, 4)  # ID 4 for 4-stars
        self.rating_group.addButton(self.radioButton_5, 5)  # ID 5 for 5-stars

        self.selected_rating = None

        # Connect the rating group to the updateRating method
        self.rating_group.idToggled.connect(self.updateRating)

        # Connect buttons to respective functions
        self.Yes_Btn.clicked.connect(lambda: self.setRating(self.selected_rating, self.book_id))
        self.No_Btn.clicked.connect(self.cancelRating)

    def updateRating(self, button_id, checked):
        if checked:  # Only update if the button is selected (checked)
            self.selected_rating = button_id

    def setRating(self, rating, book_id):
        if self.selected_rating is None:
            show_message(self, "Error", "Please select a rating!")
            return
        # Perform the database update
        cursor = self.db.get_connection().cursor()
        cursor.execute("select Rating from Books where Book_ID = ?", (int(book_id), ))
        prev_rating = cursor.fetchone()
        new_rating = (int(prev_rating[0]) + int(rating)) / 2
        cursor.execute("UPDATE Books SET Rating = ? WHERE Book_ID = ?", (new_rating, int(book_id)))
        self.db.get_connection().commit()

        # Show success message
        show_message(self, "Success", "Rating added, thank you!")
        self.viewAll()
        self.close()

    def cancelRating(self):
        self.close()




class BookARoom(QMainWindow):
    def __init__(self, db_connection: DatabaseConnection):
        super().__init__()
        uic.loadUi("Book_a_room.ui", self) 

        self.db = db_connection 
        self.cursor = db_connection.get_cursor()
        self.comboBox_2.currentTextChanged.connect(self.updateTimeSlots)
        self.populateRoomNumbers()  # populates room number combobox
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(10)
        self.pushButton.clicked.connect(self.bookRoom)  

       
    def updateTimeSlots(self):
        self.comboBox.clear() 
        selected_room = self.comboBox_2.currentText() 

    # Checks for a valid room number 
        if selected_room == "Select Room" or not selected_room:
            self.comboBox.addItem("Select Time Slot")
            return

    # gets the time slots for selected room
        self.cursor.execute("""
            SELECT Time_Slot 
            FROM Rooms 
            WHERE Room_No = ? AND Room_Availability = 'Available'
        """, (selected_room,))
    
        time_slots = self.cursor.fetchall()  #stores in time_slots variable

        self.comboBox.addItem("Select Time Slot") # default value 
    
        # Populate the comboBox with available time slots
        for slot in time_slots:
            self.comboBox.addItem(slot[0])  


    def populateAvailableSlots(self):
        selected_room = self.comboBox_2.currentText()  # Get selected room from the dropdown

        if selected_room == "Select Room" or not selected_room:
            self.comboBox.clear()  # Clear the dropdown if no valid room is selected
            self.comboBox.addItem("Select Time Slot")
            return

        self.comboBox.clear()  # Clear the existing items in the dropdown
        self.comboBox.addItem("Select Time Slot")  # Add a default placeholder item

        # Fetch available slots for the selected room
        self.cursor.execute("""
            SELECT DISTINCT Time_Slot 
            FROM Rooms 
            WHERE Room_No = ? AND Room_Availability = 'Available'
        """, (selected_room,))
        available_slots = self.cursor.fetchall()

        # Populate the comboBox with available time slots
        for slot in available_slots:
            self.comboBox.addItem(slot[0])  # Add each available slot

    def limitSpinBoxValue(self):
        if self.spinbox.value()>10:
            self.spinbox.setvalue(10)

    def populateRoomNumbers(self):
        self.comboBox_2.clear()  # Clear the dropdown to avoid duplicates
        self.comboBox_2.addItem("Select Room")  # Add a default placeholder

        # Query to fetch unique room numbers
        self.cursor.execute("""
            SELECT DISTINCT Room_No
            FROM Rooms
        """)
        rooms = self.cursor.fetchall()

        #Populate the comboBox with unique room numbers
        for room in rooms:
            self.comboBox_2.addItem(str(room[0]))


    def bookRoom(self):
        selected_room = self.comboBox_2.currentText()
        selected_slot = self.comboBox.currentText()
        username = self.lineEdit_2.text()
        count_of_people = self.spinBox.value()

        if selected_room == "Select Room" or selected_slot == "Select Time Slot":
            show_message(self, "Error", "Please select a valid room and time slot.")
            return

        if not username:
            show_message(self, "Error", "Please enter a username.")
            return

        self.cursor.execute("""
            SELECT Capacity FROM Rooms WHERE Room_No = ? AND Time_Slot = ? AND Room_Availability = 'Available'
        """, (selected_room, selected_slot))

        room_data = self.cursor.fetchone()

        if room_data is None:
            show_message(self, "Error", "The room or time slot is unavailable or doesn't exist.")
            return

        room_capacity = room_data[0]

        if count_of_people > room_capacity:
            show_message(self, "Error", f"The number of people ({count_of_people}) exceeds the room capacity ({room_capacity}). Please select a valid number of people.")
            return

        # Inserting booking into the database
        
        #Query to check valid member ID
        self.cursor.execute("""
            SELECT Member_ID 
            FROM Member_info 
            WHERE Member_Name = ?
        """, (username,))
        member = self.cursor.fetchone()

        if member is None:
            show_message(self, "Error", "Invalid username. Please enter a valid username.")
            return

        
        member_id = member[0]  

        self.cursor.execute("""
            INSERT INTO Bookings (Member_ID, Room_No, Booking_Date, Booking_Time_Slot)
            VALUES (?, ?, GETDATE(), ?)
        """, (member_id, selected_room, selected_slot))
        self.db.get_connection().commit()

        # Mark the room slot as 'Booked' in Rooms table
        self.cursor.execute("""
            UPDATE Rooms
            SET Room_Availability = 'Booked'
            WHERE Room_No = ? AND Time_Slot = ?
        """, (selected_room, selected_slot))
        self.db.get_connection().commit()

        show_message(self, "Success", "Room booked successfully!")
        self.populateAvailableSlots()  # Refresh available slots


    
app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = UI() # Create an instance of our 
window.show()
app.exec() # Start the application
