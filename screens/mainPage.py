import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from screens.ui.mainUI import Ui_MainWindow  # Import the class from converted .py file

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # Sets up all widgets defined in the .ui file

    def 

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())