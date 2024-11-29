from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QMessageBox, QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

# server = "DESKTOP-CHMOJM3\SQLEXPRESS" # Anas
#server = 'DESKTOP-9QAGOMJ\SQLSERVER1' # Hamza
server = 'LAPTOP-N8UU3FAP\SQLSERVER1' #Zoraiz
database = "DbFinal"
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'



# Replace these with your own database connection details
class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Main_screen.ui', self)
        #self.createAccountBtn = self.findChild(QtWidgets.QPushButton, "CreateAccount_Button")
        #self.signInCustomerBtn = self.findChild(QtWidgets.QPushButton, "Signin_Customer_Button")
        #self.signInLibrarianBtn = self.findChild(QtWidgets.QPushButton, "Signin_Librarian_Button")
        
        self.CreateAccount_Button.clicked.connect(self.open_create_account)

    def open_create_account(self):
        # Create and display the Create Account screen
        self.create_account_window =  QtWidgets.QMainWindow()
        uic.load_ui('Create_account.ui', self.create_account_window )
        self.close()  # Close the main window (optional)

        #self.inventory_window = QtWidgets.QMainWindow()  # Create a new QMainWindow
        #uic.loadUi('Inventory.ui', self.inventory_window)  # Load the Inventories UI
        #self.inventory_window.show()  # Show the Inventories window

    #def createAcc(self):
     #   self.creatingAcc = CreateAccount()
      #  self.creatingAcc.show()


        # self.books_tw.itemSelectionChanged.connect(self.enable_buttons)

        # self.booksTableWidget.setRowCount(len(books))
        
        # for i in range(len(books)):
        #     for j in range(5):
        #         item = QtWidgets.QTableWidgetItem(books[i][j])
        #         # Make the items non-editable
        #         item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable) 
        #         self.booksTableWidget.setItem(i,j,item)

        # Connect the search function with the search button.
        # self.search_pb.clicked.connect(self.search)

        # Connect the view function with the view button.
        # self.view_pb.clicked.connect(self.view)

        # Connect the delete function with the delete button.
        # self.delete_pb.clicked.connect(self.delete)

        # Connect the close function with the close button.
        # self.close_pb.clicked.connect(self.close)
    # def booktype(self):
        # for selected_type in self.booktype_rb.buttons():
    #         if selected_type.isChecked():
    #             type_text = selected_type.text()
    #             return type_text
    #     return ""


    # def search(self):
    #     # TO BE IMPLEMENTED
    #     selected_category = self.category_cb.currentText()
    #     title_text = self.title_le.text().lower()
    #     for row in range(self.books_tw.rowCount()):
    #         category = self.books_tw.item(row, 2)
    #         title = self.books_tw.item(row, 1)
    #         book_type = self.books_tw.item(row, 3)
    #         issuance = self.books_tw.item(row, 4)
    #         category_matches = (selected_category == "" or selected_category == category.text())
    #         title_matches = (title_text in title.text().lower() or title_text == "")
    #         type_matches = (book_type.text() == self.booktype() or self.booktype() == "")
    #         if self.issue_cb.isChecked():
    #             if issuance.text() == "True":
    #                 self.books_tw.setRowHidden(row, not (category_matches and title_matches and type_matches))
    #             else:
    #                 self.books_tw.setRowHidden(row, not (category_matches and title_matches and type_matches and False))
                
    #         else:
    #             self.books_tw.setRowHidden(row, not (category_matches and title_matches and type_matches))
    
    # def enable_buttons(self):
    #     if self.books_tw.selectedItems():
    #         self.view_pb.setEnabled(True)
    #         self.delete_pb.setEnabled(True)
    #     else:
    #         self.view_pb.setEnabled(False)
    #         self.delete_pb.setEnabled(False)
    
    
    # def delete(self): 
    #     selected_row = self.books_tw.currentRow()
 #     if selected_row != -1:
    #         conf = QMessageBox()
    #         conf.setIcon(QMessageBox.Icon.Warning)
    #         conf.setText("Are you sure you want to delete this book?")
    #         conf.setWindowTitle("Confirmation Box")
    #         conf.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    #         respnse = conf.exec()
    #         if respnse == QMessageBox.StandardButton.Yes:
    #             self.books_tw.removeRow(selected_row)


    # def close(self):
    #     QtWidgets.QApplication.quit()
            
class CreateAccount(QtWidgets.QMainWindow):  
    def _init_(self):
        super()._init_() 
        # Load the .ui file
        uic.loadUi('Create_account.ui', self)

        self.usernameF = self.findChild(QtWidgets.QLineEdit, "Username")
        self.passwordF = self.findChild(QtWidgets.QLineEdit, "password")
        self.cPasswordF = self.findChild(QtWidgets.QLineEdit, "c_password")
        self.submitBtn = self.findChild(QtWidgets.QPushButton, "submit")

        self.submitBtn.clicked.connect(self.create_account)

    def create_account(self):
            username = self.usernameF.text()
            password = self.passwordF.text()
            c_password = self.cPasswordF.text()

            if not username or not password or not c_password:
                self.show_message("Error", "All fields must be filled.")
                return

            if password != c_password:
                self.show_message("Error", "Passwords do not match.")
                return

            try:
                # Insert data into the database
                self.add_to_database(username, password)
                self.show_message("Success", "Account created successfully!")
            except Exception as e:
                self.show_message("Error", f"Failed to create account: {e}")

    def add_to_database(self, username, password): # Not made yet
        # Database connection
        pass

    def show_message(self, title, message):
        """Utility function to show a message box."""
        pass
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()





class Admin_or_Librarian(QtWidgets.QMainWindow):  
    def __init__(self):
        super().__init__() 
        uic.loadUi('Admin_or_Librarian.ui', self)

        # Connect buttons
        self.Inventory_Button.clicked.connect(self.open_inventory)
        self.Members_Button.clicked.connect(self.open_members)

    def open_inventory(self):
        """Open the Inventories window."""
        self.inventory_window = QtWidgets.QMainWindow()  # Create a new QMainWindow
        uic.loadUi('Inventory.ui', self.inventory_window)  # Load the Inventories UI
        self.inventory_window.show()  # Show the Inventories window

    def open_members(self):
        """Open the Members window."""
        self.members_window = QtWidgets.QMainWindow()  # Create a new QMainWindow
        uic.loadUi('Members.ui', self.members_window)  # Load the Members UI
        self.members_window.show()  # Show the Members window


class Inventory(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Inventory.ui', self)  # Load the Inventories UI

        # Connect buttons
        self.RoomInventory_Button.clicked.connect(self.open_room_inventory)
        self.BookInventory_Button.clicked.connect(self.open_book_inventory)

    def open_room_inventory(self):
        """Open the RoomInventory window."""
        self.room_inventory_window = QtWidgets.QMainWindow()  # Create a new QMainWindow
        uic.loadUi('Room_inventory.ui', self.room_inventory_window)  # Load the RoomInventory UI
        self.room_inventory_window.show()  # Show the RoomInventory window

    def open_book_inventory(self):
        """Open the BookInventory window."""
        self.book_inventory_window = QtWidgets.QMainWindow()  # Create a new QMainWindow
        uic.loadUi('book_inventory.ui', self.book_inventory_window)  # Load the BookInventory UI
        self.book_inventory_window.show()  # Show the BookInventory window

class Members(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Members.ui', self)  # Load the Members UI

        # Connect buttons
        self.BlockButton.clicked.connect(self.block_member)

        # Database connection string (adjust this according to your database)
        self.conn = pyodbc.connect('DRIVER={SQL Server};'
                                   'SERVER=your_server_name;'
                                   'DATABASE=your_database_name;'
                                   'UID=your_username;'
                                   'PWD=your_password')
        self.cursor = self.conn.cursor()

    def block_member(self):
        """Block the selected member by changing their status to 'Inactive' and close the window."""
        selected_row = self.Members_Table.currentRow()  # Get the selected row in the table

        if selected_row != -1:  # Check if a row is selected
            # Get the ISBN of the selected member from the first column (assuming it's the ISBN)
            isbn = self.Members_Table.item(selected_row, 0).text()
            current_status = self.Members_Table.item(selected_row, 3).text()  # Status is in the 4th column (index 3)

            if current_status != "Inactive":  # Check if the member is not already inactive
                # SQL query to update the status of the member to 'Inactive'
                query = "UPDATE Members SET Status = ? WHERE ISBN = ?"
                self.cursor.execute(query, ('Inactive', isbn))
                self.conn.commit()  # Commit the transaction

                # Update the status in the table (for UI purposes)
                self.Members_Table.item(selected_row, 3).setText("Inactive")
            # Close the Members window after blocking
            self.close()

#CUSTOMER SCREENN!!!!!
    # Connect buttons
    #     self.SearchIssue_Button.clicked.connect(self.open_search_issue)
    #     self.BookRoom_Button.clicked.connect(self.open_book_room)

    # def open_search_issue(self):
    #     """Open the Search Issue window."""
    #     self.search_issue_window = QtWidgets.QMainWindow()  # Create a new QMainWindow
    #     uic.loadUi('SearchIssue.ui', self.search_issue_window)  # Load the Search Issue UI
    #     self.search_issue_window.show()  # Show the Search Issue window

    # def open_book_room(self):
    #     """Open the Book Room window."""
    #     self.book_room_window = QtWidgets.QMainWindow()  # Create a new QMainWindow
    #     uic.loadUi('BookRoom.ui', self.book_room_window)  # Load the Book Room UI
    #     self.book_room_window.show()  # Show the Book Room window

    

# class ViewBook(QtWidgets.QMainWindow):  
#     def _init_(self, isbn,title,category,type,issuance):
#         super()._init_() 
#         # Load the .ui file
#         uic.loadUi('ViewBook.ui', self)

#         self.findChild(QtWidgets.QLineEdit, 'ISBNLineEdit').setText(isbn)
#         self.findChild(QtWidgets.QLineEdit, 'TitleLineEdit').setText(title)
#         self.findChild(QtWidgets.QLineEdit, 'CategoryLineEdit').setText(category)

#         if type == "Reference Book": 
#             self.findChild(QtWidgets.QRadioButton, "RefBookRadioButton").setChecked(True)
#             self.findChild(QtWidgets.QRadioButton, "TextBookRadioButton").setChecked(False)
#             self.findChild(QtWidgets.QRadioButton, "JournalRadioButton").setChecked(False)
#         elif type == "Text Book": 
#             self.findChild(QtWidgets.QRadioButton, "RefBookRadioButton").setChecked(False)
#             self.findChild(QtWidgets.QRadioButton, "TextBookRadioButton").setChecked(True)
#             self.findChild(QtWidgets.QRadioButton, "JournalRadioButton").setChecked(False)
#         else: 
#             self.findChild(QtWidgets.QRadioButton, "RefBookRadioButton").setChecked(False)
#             self.findChild(QtWidgets.QRadioButton, "TextBookRadioButton").setChecked(False)
#             self.findChild(QtWidgets.QRadioButton, "JournalRadioButton").setChecked(True)

#         self.findChild(QtWidgets.QRadioButton, "RefBookRadioButton").setEnabled(False)
#         self.findChild(QtWidgets.QRadioButton, "TextBookRadioButton").setEnabled(False)
#         self.findChild(QtWidgets.QRadioButton, "JournalRadioButton").setEnabled(False)
            
#         if issuance:
#             self.findChild(QtWidgets.QCheckBox, "IssuedCheckBox").setChecked(True)
#         self.findChild(QtWidgets.QCheckBox, "IssuedCheckBox").setEnabled(False)
            #         self.make_form_read_only()

#     def make_form_read_only(self):
#         for widget in self.findChildren(QtWidgets.QWidget):
#             if isinstance(widget, (QtWidgets.QLineEdit, QtWidgets.QTextEdit)):
#                 widget.setReadOnly(True)
#             elif isinstance(widget, (QtWidgets.QComboBox, QtWidgets.QPushButton)):
#                 widget.setEnabled(False)



app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = UI() # Create an instance of our 
window.show()
app.exec() # Start the application

##