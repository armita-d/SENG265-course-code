import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from controller import Controller, IllegalOperationException

class ProductGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.setWindowTitle("Products")

        layout1 = QGridLayout()

        label_code = QLabel("Product Code")
        self.text_code = QLineEdit()
        self.text_code.setInputMask('00000000')
        label_description = QLabel("Description")
        self.text_description = QLineEdit()
        label_price = QLabel("Price")
        self.text_price = QLineEdit()

        layout1.addWidget(label_code, 0, 0)
        layout1.addWidget(self.text_code, 0, 1)
        layout1.addWidget(label_description, 1, 0)
        layout1.addWidget(self.text_description, 1, 1)
        layout1.addWidget(label_price, 2, 0)
        layout1.addWidget(self.text_price, 2, 1)

        layout2 = QHBoxLayout()

        self.button_clear = QPushButton("Clear")
        label_search_code = QLabel("Code:")
        self.text_search_code = QLineEdit()
        self.text_search_code.setInputMask('00000000')
        self.button_search = QPushButton("Search")
        self.button_search.setEnabled(False)
        layout2.addWidget(self.button_clear)
        layout2.addWidget(label_search_code)
        layout2.addWidget(self.text_search_code)
        layout2.addWidget(self.button_search)

        layout3 = QVBoxLayout()

        top_widget = QWidget()
        top_widget.setLayout(layout1)
        bottom_widget = QWidget()
        bottom_widget.setLayout(layout2)
        layout3.addWidget(top_widget)
        layout3.addWidget(bottom_widget)
        widget = QWidget()
        widget.setLayout(layout3)

        self.setCentralWidget(widget)

        # define widgets' initial state
        self.text_code.setEnabled(False)
        self.text_description.setEnabled(False)
        self.text_price.setEnabled(False)
        self.button_clear.setEnabled(True)
        self.button_search.setEnabled(False)

        # handle text change to enable/disable buttons
        self.text_search_code.textChanged.connect(self.search_code_text_changed)

        # connect the buttons' clicked signals to the slots below
        self.button_clear.clicked.connect(self.clear_button_clicked)
        self.button_search.clicked.connect(self.search_button_clicked)

    def search_code_text_changed(self):
        if self.text_search_code.text():
            self.button_search.setEnabled(True)
        else:
            self.button_search.setEnabled(False)

    def clear_button_clicked(self):
        ''' clear the fields '''
        # TODO: clear the QLineEdits' text in the products screen
        self.text_code.setText("")
        self.text_description.setText("")
        self.text_price.setText("")
        self.text_search_code.setText("")

        self.text_code.setEnabled(True)
        self.text_description.setEnabled(True)
        self.text_text.setEnabled(True)
        self.button_search.setEnabled(False)
        self.button_create.setEnabled(False)
    def search_button_clicked(self):
        ''' search product '''



        key = self.text_search_code.text()
        product = self.controller.search_product(key)

        if product:
        # fill product fields and disable editing
            self.text_code.setText(product.code)
            self.text_description.setText(product.description)
            self.text_price.setText(str(product.price))
            self.text_code.setEnabled(False)
            self.text_description.setEnabled(False)
            self.text_price.setEnabled(False)

        # disable search until Clear clicked
            self.button_search.setEnabled(False)
        else:
            QMessageBox.warning(self, "Search", f"No product found with code {key}.")
            self.clear_button_clicked()
        # TODO: First, get the key from the search text. Then call controller.search_product()


        # after storing the returned product in a variable, check this variable
        # TODO: if you found a product with that code, show it in the QLineEdits
        # and do not allow the texts to be edited
        # also, do not allow more searches (let the Clear button allow searches back again)
 




        # TODO: if you have not found a product, show a warning message and clear the fields afterwards



def create_button_clicked(self):
    """ Add new product """
    code = self.text_code.text()
    description = self.text_description.text()
    price_text = self.text_price.text()

    try:
        price = float(price_text)                       # convert price to float
        self.controller.create_product(code, description, price)  # add product
        QMessageBox.information(self, "Create", f"Product {code} created successfully!")
        self.clear_button_clicked()                     # clear fields after success

    except ValueError:
        QMessageBox.warning(self, "Create", "Invalid price. Please enter a number.")

    except IllegalOperationException as e:
        QMessageBox.warning(self, "Create", str(e))    # warn if code already exists 

app = QApplication(sys.argv)
window = ProductGUI()
window.show()
app.exec()
