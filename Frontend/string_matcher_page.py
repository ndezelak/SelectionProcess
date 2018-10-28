# TODO: Should this be inside main_page as a slot?
from PyQt5.QtWidgets import QInputDialog, QWidget, QMessageBox
class string_matcher_page(QWidget):
    def __init__(self,parent_widget):
        super().__init__()
        self.parent_widget = parent_widget

    def get_item(self,window=[],window_title="",text="",items=[]):
        item,ok = QInputDialog.getItem(window,window_title,text,items,0,False)
        if item and ok:
            self.parent_widget.unknown_field_of_study_specified.emit(item)
        else:
            self.parent_widget.unknown_field_of_study_specified.emit(-1)
    def display_error(self,window=[],window_title="",text=""):
        QMessageBox.critical(window,window_title,text)
