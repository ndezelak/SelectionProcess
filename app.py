# This is the starting point of the app
import sys
import os
from PyQt5.QtWidgets import QApplication, QStyleFactory
from Frontend.start_page import startPage
from Frontend.main_page import *
import Data.globals as globals

def main():
    # Get app directory
    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    globals.home_dir = dir
    # Create the application
    app = QApplication([])
    app.setStyle(QStyleFactory.create("fusion"))
    #Create the start page
    startpage = startPage(app)
    #mainpage = mainPage(app)
    # Stop when app is closed
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()