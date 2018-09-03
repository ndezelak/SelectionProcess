# TODO: Should this be inside main_page as a slot?
from PyQt5.QtWidgets import QInputDialog, QWidget, QMessageBox
class string_matcher_page(QWidget):
    def __init__(self):
        super().__init__()
    def get_item(self,window=[],window_title="",text="",items=[]):
        item,ok = QInputDialog.getItem(window,window_title,text,items,0,False)
        if item and ok:
            return item
        else:
            return -1
    def display_error(self,window=[],window_title="",text=""):
        QMessageBox.critical(window,window_title,text)
