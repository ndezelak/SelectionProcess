from PyQt5.QtWidgets import QWidget,QLabel, QTextEdit, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSlot
import Data.globals as globals
from Data.data_structures import Field_of_Study
from Backend.output_utils import save_project
import copy
class edit_field_of_study(QWidget):
    def __init__(self, parent, item_index = []):
        super().__init__()
        self.parent = parent
        self.item_index = item_index
        self.initialize()
        globals.current_session_buffer = copy.deepcopy(globals.current_session)

    def initialize(self):
        self.setWindowTitle("Einstellungen des Studiengänges")

        label_name = QLabel("Name")
        label_tags = QLabel("Tags")

        self.text_name = QTextEdit()
        self.text_tag = QTextEdit()

        button_ok = QPushButton("OK")
        button_ok.clicked.connect(self.ok_clicked)

        main_layout = QVBoxLayout()
        main_layout.addWidget(label_name)
        main_layout.addWidget(self.text_name)
        main_layout.addWidget(label_tags)
        main_layout.addWidget(self.text_tag)
        main_layout.addWidget(button_ok)

        if self.item_index !=[]:
            self.text_name.setText(globals.current_session_buffer.fields_of_study[self.item_index].name)
            self.text_tag.setText("\n".join(globals.current_session_buffer.fields_of_study[self.item_index].tags))

        self.setLayout(main_layout)
        self.show()
    # A new field of study is to be added
    @pyqtSlot()
    def ok_clicked(self):
        tag_list = self.text_tag.toPlainText().split("\n")
        # When an item is being edited
        if self.item_index != []:
            self.parent.main_display.takeItem(self.parent.main_display.currentRow())
            globals.current_session_buffer.fields_of_study[self.item_index] = Field_of_Study(name=self.text_name.toPlainText(),
                                                   tags=tag_list)
        # When a new item is being added
        else:
            globals.current_session_buffer.fields_of_study.append(Field_of_Study(name=self.text_name.toPlainText(),
                                                   tags=tag_list))
        # Updated display
        self.parent.main_display.addItem(self.text_name.toPlainText())
        self.parent.main_display.setCurrentRow(self.parent.main_display.count()-1)
        self.parent.tag_display.setText(self.text_tag.toPlainText())
        self.hide()

