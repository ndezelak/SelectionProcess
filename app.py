# This is the starting point of the app
import sys
import os
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtCore import QThread
from Frontend.start_page import startPage
from Frontend.main_page import *
import Data.globals as globals

# Method used by pyinstaller
# Add this line to the spec file: datas=[('Data\startpage_background.png','DATA')],
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def main():
    # Get app directory
    dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    globals.home_dir = dir
    # Create the application
    app = QApplication([])
    app.setStyle(QStyleFactory.create("fusion"))
    app.setWindowIcon(QtGui.QIcon(resource_path('Data/icon.png')))
    QThread.currentThread().setPriority(QThread.HighestPriority)
    #Create the start page
    startpage = startPage(app)
    # Stop when app is closed
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()