from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox
import sys

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__() #
        # Load the .ui file
        uic.loadUi('Lab02.ui', self) # UIs here 

        self.view_book = None

        self.CategoryComboBox.setCurrentIndex(-1)
        self.booktype_rb = QtWidgets.QButtonGroup(self)

        self.booktype_rb.addButton(self.findChild(QtWidgets.QRadioButton, "RefBookRadioButton"))
        self.booktype_rb.addButton(self.findChild(QtWidgets.QRadioButton, "TextBookRadioButton"))
        self.booktype_rb.addButton(self.findChild(QtWidgets.QRadioButton, "JournalRadioButton"))
        # accessing the elements:
        self.category_cb = self.findChild(QtWidgets.QComboBox, "CategoryComboBox")
        self.title_le = self.findChild(QtWidgets.QLineEdit, "TitleLineEdit")
        self.books_tw = self.findChild(QtWidgets.QTableWidget, "booksTableWidget")
        self.search_pb = self.findChild(QtWidgets.QPushButton, "SearchPushButton")
        self.issue_cb = self.findChild(QtWidgets.QCheckBox, "IssuedCheckBox")
        self.view_pb = self.findChild(QtWidgets.QPushButton, "ViewPushButton")
        self.delete_pb = self.findChild(QtWidgets.QPushButton, "DeletePushButton")
        self.close_pb = self.findChild(QtWidgets.QPushButton, "ClosePushButton")

        self.view_pb.setEnabled(False)
        self.delete_pb.setEnabled(False)

        self.books_tw.itemSelectionChanged.connect(self.enable_buttons)
    
 
       
        # self.booksTableWidget.setRowCount(len(books))
        # for i in range(len(books)):
        #     for j in range(5):
        #         item = QtWidgets.QTableWidgetItem(books[i][j])
        #         # Make the items non-editable
        #         item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable) 
        #         self.booksTableWidget.setItem(i,j,item)
        # Connect the search function with the search button.
        self.search_pb.clicked.connect(self.search)

        # Connect the view function with the view button.
        self.view_pb.clicked.connect(self.view)

        # Connect the delete function with the delete button.
        self.delete_pb.clicked.connect(self.delete)

        # Connect the close function with the close button.
        self.close_pb.clicked.connect(self.close)
    def booktype(self):
        for selected_type in self.booktype_rb.buttons():
            if selected_type.isChecked():
                type_text = selected_type.text()
                return type_text
        return ""


    def search(self):
        # TO BE IMPLEMENTED
        selected_category = self.category_cb.currentText()
        title_text = self.title_le.text().lower()
        for row in range(self.books_tw.rowCount()):
            category = self.books_tw.item(row, 2)
            title = self.books_tw.item(row, 1)
            book_type = self.books_tw.item(row, 3)
            issuance = self.books_tw.item(row, 4)
            category_matches = (selected_category == "" or selected_category == category.text())
            title_matches = (title_text in title.text().lower() or title_text == "")
            type_matches = (book_type.text() == self.booktype() or self.booktype() == "")
            if self.issue_cb.isChecked():
                if issuance.text() == "True":
                    self.books_tw.setRowHidden(row, not (category_matches and title_matches and type_matches))
                else:
                    self.books_tw.setRowHidden(row, not (category_matches and title_matches and type_matches and False))
                
            else:
                self.books_tw.setRowHidden(row, not (category_matches and title_matches and type_matches))
    
    def enable_buttons(self):
        if self.books_tw.selectedItems():
            self.view_pb.setEnabled(True)
            self.delete_pb.setEnabled(True)
        else:
            self.view_pb.setEnabled(False)
            self.delete_pb.setEnabled(False)
    
    def view(self):
        selected_row = self.books_tw.currentRow()
        isbn = self.books_tw.item(selected_row, 0).text()
        title = self.books_tw.item(selected_row, 1).text()
        category = self.books_tw.item(selected_row, 2).text()
        type = self.books_tw.item(selected_row, 3).text()
        issuance = self.books_tw.item(selected_row, 0).text()

        self.view_book = ViewBook(isbn, title, category, type, issuance)
        self.view_book.show()
    def delete(self): 
        selected_row = self.books_tw.currentRow()
        if selected_row != -1:
            conf = QMessageBox()
            conf.setIcon(QMessageBox.Icon.Warning)
            conf.setText("Are you sure you want to delete this book?")
            conf.setWindowTitle("Confirmation Box")
            conf.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            respnse = conf.exec()
            if respnse == QMessageBox.StandardButton.Yes:
                self.books_tw.removeRow(selected_row)


    def close(self):
        QtWidgets.QApplication.quit()
            

class ViewBook(QtWidgets.QMainWindow):  
    def __init__(self, isbn,title,category,type,issuance):
        super().__init__() 
        # Load the .ui file
        uic.loadUi('ViewBook.ui', self)

        self.findChild(QtWidgets.QLineEdit, 'ISBNLineEdit').setText(isbn)
        self.findChild(QtWidgets.QLineEdit, 'TitleLineEdit').setText(title)
        self.findChild(QtWidgets.QLineEdit, 'CategoryLineEdit').setText(category)

        if type == "Reference Book": 
            self.findChild(QtWidgets.QRadioButton, "RefBookRadioButton").setChecked(True)
            self.findChild(QtWidgets.QRadioButton, "TextBookRadioButton").setChecked(False)
            self.findChild(QtWidgets.QRadioButton, "JournalRadioButton").setChecked(False)
        elif type == "Text Book": 
            self.findChild(QtWidgets.QRadioButton, "RefBookRadioButton").setChecked(False)
            self.findChild(QtWidgets.QRadioButton, "TextBookRadioButton").setChecked(True)
            self.findChild(QtWidgets.QRadioButton, "JournalRadioButton").setChecked(False)
        else: 
            self.findChild(QtWidgets.QRadioButton, "RefBookRadioButton").setChecked(False)
            self.findChild(QtWidgets.QRadioButton, "TextBookRadioButton").setChecked(False)
            self.findChild(QtWidgets.QRadioButton, "JournalRadioButton").setChecked(True)

        self.findChild(QtWidgets.QRadioButton, "RefBookRadioButton").setEnabled(False)
        self.findChild(QtWidgets.QRadioButton, "TextBookRadioButton").setEnabled(False)
        self.findChild(QtWidgets.QRadioButton, "JournalRadioButton").setEnabled(False)
            
        if issuance:
            self.findChild(QtWidgets.QCheckBox, "IssuedCheckBox").setChecked(True)
        self.findChild(QtWidgets.QCheckBox, "IssuedCheckBox").setEnabled(False)
            

        self.make_form_read_only()

    def make_form_read_only(self):
        for widget in self.findChildren(QtWidgets.QWidget):
            if isinstance(widget, (QtWidgets.QLineEdit, QtWidgets.QTextEdit)):
                widget.setReadOnly(True)
            elif isinstance(widget, (QtWidgets.QComboBox, QtWidgets.QPushButton)):
                widget.setEnabled(False)
        
        
        



app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = UI() # Create an instance of our 
window.show()
app.exec() # Start the application

