"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2021/12/14 15:03
@Software: PyCharm
@File    : ui_jmp_select.py
@Remark  :
"""
from typing import List

from PySide2.QtWidgets import QWidget, QListWidgetItem, QCheckBox

from ui_component.ui_app_variable import UiGlobalVariable
from ui_component.ui_main.ui_designer.ui_jmp_select import Ui_Form
from PySide2.QtCore import Slot, Signal, Qt



class JmpSelect(QWidget, Ui_Form):
    itemSignal = Signal(list)  # 传送父子数据给TreeWidget

    def __init__(self, parent=None, icon=None):
        super(JmpSelect, self).__init__(parent)
        self.setupUi(self)
        if icon:
            self.setWindowIcon(icon)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("")
        self.init_choose_items()

    def init_choose_items(self):
        """ 初始化JMP select items """
        for each in UiGlobalVariable.JMP_MULTI_SELECT:
            box = QCheckBox(each)
            item = QListWidgetItem()
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, box)

    def get_choose_items(self) -> List[int]:
        choose_index = []
        for i in range(self.listWidget.count()):
            item = self.listWidget.itemWidget(self.listWidget.item(i))  # type: QCheckBox
            if item.isChecked():
                choose_index.append(i)
        return choose_index

    @Slot()
    def on_pushButton_pressed(self):
        items = self.get_choose_items()
        if items:
            self.itemSignal.emit(items)
            self.hide()


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication, QWidget

    app = QApplication(sys.argv)
    win = JmpSelect()
    win.show()
    sys.exit(app.exec_())
