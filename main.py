from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QMessageBox, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

# server = "DESKTOP-CHMOJM3\SQLEXPRESS" # Anas
# server = 'DESKTOP-9QAGOMJ\SQLSERVER1' # Hamza
server = 'LAPTOP-N8UU3FAP\\SQLSERVER1' #Zoraiz
database = "DbFinal"
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'


def show_message(parent, title, message):
    """Utility function to show a message box."""
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec()

# Replace these with your own database connection details

############################################ MODULE 1 ################################################### 

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Main_screen.ui', self)
        
        self.CreateAccount_Button.clicked.connect(self.open_create_account)
        self.Signin_Customer_Button.clicked.connect(self.open_sign_in)
        self.Signin_Librarian_Button.clicked.connect(self.open_sign_in)
    def open_create_account(self):
       self.creatingAcc = CreateAccount()
       self.creatingAcc.show()

    def open_sign_in(self):
        self.signIn = SignIn()
        self.signIn.show()


            
class CreateAccount(QtWidgets.QMainWindow):  
    def __init__(self):
        super().__init__() 
        # Load the .ui file
        uic.loadUi('Create_account.ui', self)
        self.resize(600, 400)

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
            connection = pyodbc.connect(connection_string)

            cursor = connection.cursor()

            cursor = connection.cursor()
            cursor.execute(check_query, (username,))
            result = cursor.fetchone()
            if result[0] > 0:
                show_message(self, "Error", "Username already exists.")
            try:
                # Insert data into the database
                self.add_to_database(username, password)
                show_message(self, "Success", "Account created successfully!")
            except Exception as e:
                show_message(self, "Error", f"Failed to create account: {e}")

    def add_to_database(self, username, password): # Not made yet
        # Database connection
        connection = pyodbc.connect(connection_string)

        cursor = connection.cursor()

        cursor = connection.cursor()

        sql_query = """
            insert into Member_Info(Member_Name, Member_Password, Member_Status)
            values (?,?,?)
            """

        cursor.execute(sql_query, (username, password, "Active"))
        connection.commit()

    


class SignIn(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() 
        # Load the .ui file
        uic.loadUi('Sign_in.ui', self)
        self.usernameF = self.findChild(QtWidgets.QLineEdit, "Enter_Username_Edit")
        self.passwordF = self.findChild(QtWidgets.QLineEdit, "Enter_Password_Edit")
        self.passwordF.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.signinBtn.clicked.connect(self.signin)

    def signin(self):
        self.username = self.usernameF.text()
        self.password = self.passwordF.text()
        if "." in self.username:
            self.signInAsLibrarian(self.username, self.password)
        else:
            self.signInAsMember(self.username, self.password)
    def signInAsLibrarian(self, username, password):
        # Database connection
        connection = pyodbc.connect(connection_string)

        cursor = connection.cursor()

        cursor = connection.cursor()

        sql_query = """
            select Librarian_Password from Library_Staff where Librarian_Name = ?
            """

        cursor.execute(sql_query, (username))
        result = cursor.fetchone()
        if result is None:
            show_message(self, "Error", "No username found")
            return
        if password != result[0]:
            show_message(self, "Error", "Incorrect Password")
            return

        self.openLibrarianScreen()
    def openLibrarianScreen(self):
       self.librarianScreen = Admin_or_Librarian()
       self.librarianScreen.show()
    
    def signInAsMember(self, username, password):
        # Database connection
        connection = pyodbc.connect(connection_string)

        cursor = connection.cursor()

        cursor = connection.cursor()

        sql_query = """
            select Member_Password from Member_Info where Member_Name = ?
            """

        cursor.execute(sql_query, (username))
        result = cursor.fetchone()
        if result is None:
            show_message(self, "Error", "No username found")
            return
        
        if password != result[0]:
            show_message(self, "Error", "Incorrect Password")
            return
        
        self.openMemberScreen()
    def openMemberScreen(self): 
       self.memberScreen = MemberScreen(self.usernameF.text())
       print(self.usernameF.text())
       self.memberScreen.show()


############################################ MODULE 2 ################################################### 

class Admin_or_Librarian(QtWidgets.QMainWindow):  
    def __init__(self):
        super().__init__() 
        uic.loadUi('Admin_or_Librarian.ui', self)

        # To store same instances for future use
        self.inventory_window = None
        self.members_window = None

        # Connect buttons
        self.Inventory_Button.clicked.connect(self.open_inventory)
        self.Members_Button.clicked.connect(self.open_members)

    def open_inventory(self):
        if self.inventory_window is None:
            self.inventory_window = Inventory(self)
        self.inventory_window.show()

    def open_members(self):
        if self.members_window is None:
            self.members_window = Members(self)
        self.members_window.show()


class Inventory(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Inventory.ui', self)

        # To store same instances for future use
        self.room_inventory_window = None
        self.book_inventory_window = None

        self.RoomInventory_Button.clicked.connect(self.open_room_inventory)
        self.BookInventory_Button.clicked.connect(self.open_book_inventory)

    def open_room_inventory(self):
        if self.room_inventory_window is None:
            self.room_inventory_window = Room_inventory(self)
        self.room_inventory_window.show()

    def open_book_inventory(self):
        if self.book_inventory_window is None:
            self.book_inventory_window = Book_Inventory(self)
        self.book_inventory_window.show()


class Room_inventory(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Room_inventory.ui', self)

        # Accessing widgets from the UI
        self.room_table = self.findChild(QtWidgets.QTableWidget, 'Room_Table')
        self.update_button = self.findChild(QtWidgets.QPushButton, 'Update_Button')
        self.time_slots_button = self.findChild(QtWidgets.QPushButton, 'TimeSlots_Button')

        # To store same instances for future use
        self.time_slots_window = None

        # Connect button clicks to their respective methods
        self.update_button.clicked.connect(self.update_room)
        self.time_slots_button.clicked.connect(self.open_time_slots)

    def update_room(self):
        # Update the room's availability and clear the 'BookedBy' field
        selected_row = self.room_table.currentRow()
        if selected_row != -1:
            # Get the room number and current availability
            room_no = self.room_table.item(selected_row, 0).text()
            availability = self.room_table.item(selected_row, 1).text()

            if availability == "Booked":
                # Update the room in the database
                query = """
                UPDATE Rooms
                SET Availability = 'Available', BookedBy = NULL
                WHERE RoomNo = ?
                """
                self.cursor.execute(query, room_no)
                self.connection.commit()

                # Update the table in the UI
                self.room_table.item(selected_row, 1).setText("Available")
                self.room_table.setItem(selected_row, 2, QtWidgets.QTableWidgetItem(""))


    def open_time_slots(self):
        # Check if the time_slots_window instance already exists
        if self.time_slots_window is None:
            # Create the TimeSlots window only once
            self.time_slots_window = QtWidgets.QMainWindow()  # Create the window instance
            uic.loadUi('TimeSlots.ui', self.time_slots_window)  # Load the UI
        self.time_slots_window.show()  # Show the existing window



class Book_Inventory(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('book_inventory.ui', self)

        self.books_table = self.findChild(QtWidgets.QTableWidget, 'Books_Table')
        self.add_book_button = self.findChild(QtWidgets.QPushButton, 'AddBook_Button')
        self.issued_books_button = self.findChild(QtWidgets.QPushButton, 'IssuedBooks_Button')

        self.issued_books_button.clicked.connect(self.show_issued_books)
        self.add_book_button.clicked.connect(self.open_add_book_screen)

        # To store same instances for future use
        self.issued_books_window = None

    def show_issued_books(self):
        if self.issued_books_window is None:
            self.issued_books_window = QtWidgets.QMainWindow()
            uic.loadUi('IssuedBooks.ui', self.issued_books_window)
        self.issued_books_window.show()

    def open_add_book_screen(self):
        self.add_book_window = AddBookScreen() # New instance each time
        self.add_book_window.show()

class AddBookScreen(QtWidgets.QMainWindow):
    def __init__(self, librarian_id):
        super().__init__()
        uic.loadUi('AddBook.ui', self)

        self.isbn_edit = self.findChild(QtWidgets.QLineEdit, 'Isbn_Edit')
        self.title_edit = self.findChild(QtWidgets.QLineEdit, 'Title_Edit')
        self.genre_combobox = self.findChild(QtWidgets.QComboBox, 'Genre_Combobox')
        self.author_edit = self.findChild(QtWidgets.QLineEdit, 'Author_Edit')
        self.confirm_button = self.findChild(QtWidgets.QPushButton, 'Confirm_Button')

        # Store the librarian's ID for future use
        self.librarian_id = librarian_id

        self.confirm_button.clicked.connect(self.add_book_to_database)

        # Populate Genre combobox
        self.genre_combobox.addItems(["Programming","Fiction"])

    def add_book_to_database(self):
        # Get inputs from the form
        isbn = self.isbn_edit.text()
        title = self.title_edit.text()
        genre = self.genre_combobox.currentText()
        author = self.author_edit.text()

        # Get the current librarian ID
        librarian_id = self.librarian_id
        
        # Set initial values for rating and availability
        rating = None # NULL value for rating
        availability = 'Available'

        query = """
        INSERT INTO Books (isbn, title, genre, author, rating, added_by, availability)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (isbn, title, genre, author, rating, librarian_id, availability)

        self.cursor.execute(query, values)
        self.connection.commit()



class Members(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Members.ui', self)

        self.BlockButton.clicked.connect(self.block_member)

    def block_member(self):
        """Block the selected member by changing their status to 'Inactive' and close the window."""
        selected_row = self.Members_Table.currentRow()

        if selected_row != -1: # If a row is selected
            # ISBN is used as unique identification for query
            isbn = self.Members_Table.item(selected_row, 0).text()
            current_status = self.Members_Table.item(selected_row, 3).text()

            if current_status != "Inactive":
                # Update the status of member to 'Inactive' in database
                query = "UPDATE Members SET Status = ? WHERE ISBN = ?"
                self.cursor.execute(query, ('Inactive', isbn))
                self.conn.commit()  # Commit the transaction

                # Update the status in UI purposes
                self.Members_Table.item(selected_row, 3).setText("Inactive")


############################################ MODULE 3 ################################################### 

class MemberScreen(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        uic.loadUi('Member_or_customer.ui', self)
        self.SearchIssue_Button.clicked.connect(lambda: self.openSearchScreen(username))
        self.BookRoom_Button.clicked.connect(lambda: self.openBookARoomScreen)
    def openSearchScreen(self, username):
        self.searchScreen = SearchScreen(username)
        self.searchScreen.show()
    def openBookARoomScreen():
        pass

class SearchScreen(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        uic.loadUi("Search.ui", self)
        self.TitleF = self.findChild(QtWidgets.QLineEdit, "TitleLE")
        self.GenreF = self.findChild(QtWidgets.QComboBox, "GenreCB")
        self.AuthorF = self.findChild(QtWidgets.QLineEdit, "AuthorLE")
        self.GenreF.setCurrentText("")

        self.connection = pyodbc.connect(connection_string)

        self.cursor = self.connection.cursor()

        self.cursor = self.connection.cursor()

        self.cursor.execute("select * from Books")

        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(self.cursor.fetchall()):
            self.BookTW.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.BookTW.setItem(row_index, col_index, item)

        self.SearchPB.clicked.connect(self.search)
        self.ViewPB.clicked.connect(self.view) # Yet to be completed (needs test)
        self.RateABookPB.clicked.connect(lambda: self.rateABook) # Yet to be completed

        print(username)
        self.ViewAllPB.clicked.connect(self.viewAll)
        self.IssuePB.clicked.connect(lambda: self.issue(username))

        self.LogoutPB.clicked.connect(self.loggingOut)

    def search(self):
        sqlQuery = "select * from Books where "
        parameters = []
        if self.TitleF.text():
            sqlQuery+="and Title=? "
            parameters.append(self.TitleF.text())
        if self.GenreF.text():
            sqlQuery+="and Genre=? "
            parameters.append(self.GenreF.text())
        if self.AuthorF.text():
            sqlQuery+="and Author=? "
            parameters.append(self.AuthorF.text())

        self.cursor.execute(sqlQuery, parameters)
    
    def viewAll(self):
        self.cursor.execute("select * from Books")

        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(self.cursor.fetchall()):
            self.BookTW.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.bookTW.setItem(row_index, col_index, item)

    def view(self):
        """View detailed information about the selected book."""
        selected_row = self.BookTW.currentRow()
        if selected_row != -1:  # Check if a row is selected
            book_id = self.BookTW.item(selected_row, 0).text()  # Assuming the first column is the book ID
            self.cursor.execute("SELECT * FROM Books WHERE Book_ID = ?", (book_id,))
            book_details = self.cursor.fetchone()
            if book_details:
                # Show the details in a message box or separate window
                details = f"ID: {book_details[0]}\nTitle: {book_details[1]}\nAuthor: {book_details[2]}\nGenre: {book_details[3]}\nStatus: {book_details[4]}"
                show_message(self, "Book Details", details)
            else:
                show_message(self, "Warning", "Please select a book to view details.")

    def issue(self, username):
        """Issue the selected book to the current user."""
        selected_row = self.BookTW.currentRow()
        if selected_row != -1:  # Check if a row is selected
            self.cursor.execute("select Member_ID from Member_Info where Member_Name = ?", (username))
            user_id = self.cursor.fetchone()
            user_id = user_id[0]
            book_id = self.BookTW.item(selected_row, 0).text()  # Assuming the first column is the book ID
            self.cursor.execute("SELECT Availability FROM Books WHERE Book_ID = ?", (book_id,))
            book_status = self.cursor.fetchone()
            if book_status and book_status[0] == "Available":
                self.cursor.execute("UPDATE Books SET Availability = 'Issued' WHERE Book_ID = ?", (book_id,))
                self.cursor.execute("""
                INSERT INTO Issued_Books (Member_ID, Book_ID, Issue_Date, Due_Date) 
                VALUES (?, ?, GETDATE(), DATEADD(WEEK, 2, GETDATE()))
            """, (user_id, book_id))
                self.connection.commit()
                show_message(self, "Success", "Book issued successfully!")
                self.BookTW.item(selected_row, 4).setText("Issued")  # Update status in UI
            else:
                show_message(self, "Warning", "The selected book is not available for issuing.")
        else:
            show_message(self, "Warning", "Please select a book to issue.")
    def loggingOut(self):
        self.mainScreen = UI()
        self.mainScreen.show()
    







app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = UI() # Create an instance of our 
window.show()
app.exec() # Start the application
