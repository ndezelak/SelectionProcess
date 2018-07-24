from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout
from PyQt5.QtCore import *
class newProjectWindow(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.initialize()
        self.parent = parent
    def initialize(self):
        self.setWindowTitle("Project settings")
        button = QPushButton()
        button.setText("OK")
        button.clicked.connect(self.finished)

        grid = QGridLayout()
        grid.addWidget(button,1,0)

        self.setLayout(grid)
        self.show()

    @pyqtSlot()
    def finished(self):
        self.parent.hide()
        self.deleteLater()
