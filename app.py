# This is the starting point of the app
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from Frontend.start_page import *

if __name__ == '__main__':
    pass

# Create the application
app = QApplication([])
startpage = startPage(app)

sys.exit(app.exec_())

