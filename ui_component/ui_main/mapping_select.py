"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2021/12/14 15:03
@Software: PyCharm
@File    : mapping_select.py
@Remark  : 
"""

from PySide2.QtWidgets import QWidget
from ui_component.ui_main.ui_designer.ui_mapping_select import Ui_Form
from PySide2.QtCore import Slot, Signal, Qt


class MappingSelect(QWidget, Ui_Form):
    SOFT_BIN = 1
    HARD_BIN = 2
    FIRST_FAIL = 3
    CORR = 4
    bin_signal = Signal(int)

    def __init__(self, parent=None, icon=None):
        super(MappingSelect, self).__init__(parent)
        self.setupUi(self)
        if icon:
            self.setWindowIcon(icon)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    @Slot()
    def on_pushButton_pressed(self):
        self.bin_signal.emit(MappingSelect.SOFT_BIN)

    @Slot()
    def on_pushButton_2_pressed(self):
        self.bin_signal.emit(MappingSelect.HARD_BIN)

    @Slot()
    def on_pushButton_3_pressed(self):
        self.bin_signal.emit(MappingSelect.FIRST_FAIL)

    @Slot()
    def on_pushButton_4_pressed(self):
        self.bin_signal.emit(MappingSelect.CORR)


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication, QWidget

    app = QApplication(sys.argv)
    win = MappingSelect()
    win.show()
    sys.exit(app.exec_())
