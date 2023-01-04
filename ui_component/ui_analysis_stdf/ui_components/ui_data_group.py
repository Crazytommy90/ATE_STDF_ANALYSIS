"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/5/17 21:09
@Software: PyCharm
@File    : ui_data_group.py
@Remark  : 
"""
from typing import Union

from PySide2.QtCore import Qt, Slot, Signal
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QWidget

from common.li import Li
from ui_component.ui_analysis_stdf.ui_designer.ui_group import Ui_Form
from ui_component.ui_app_variable import UiGlobalVariable


class DataGroupWidget(QWidget, Ui_Form):
    group_item_list = QStandardItemModel()
    da_group_item_list = QStandardItemModel()
    group_data_list = QStandardItemModel()

    def __init__(self, li: Li, parent=None):
        super(DataGroupWidget, self).__init__(parent)
        self.li = li
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle("Setting Tool")
        self.listView.setModel(self.group_item_list)
        self.listView_2.setModel(self.da_group_item_list)
        self.listView_3.setModel(self.group_data_list)
        self.init_listView()
        self.init_listView_2()
        self.group_item_list.itemChanged.connect(self.checkbox_changed)
        self.da_group_item_list.itemChanged.connect(self.checkbox_changed)
        self.group_data_list.itemChanged.connect(self.group_data_changed)

    def init_listView(self):
        """
        初始化Group By,后面放在ini中维护
        :return:
        """
        self.group_item_list.clear()
        for index, each in enumerate(UiGlobalVariable.SUMMARY_GROUP):

            item = QStandardItem(each)
            if index == 0:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            item.setCheckable(True)
            self.group_item_list.appendRow(item)

    def init_listView_2(self):
        """
        初始化Group By,后面放在ini中维护
        :return:
        """
        self.da_group_item_list.clear()
        for index, each in enumerate(UiGlobalVariable.DATA_GROUP):
            item = QStandardItem(each)
            item.setCheckState(Qt.Unchecked)
            item.setCheckable(True)
            self.da_group_item_list.appendRow(item)

    def init_listView_3(self):
        if self.li.to_chart_csv_data is None:
            return
        if self.li.to_chart_csv_data.group_df is None:
            return
        self.group_data_list.itemChanged.disconnect(self.group_data_changed)
        self.group_data_list.clear()
        for key in self.li.to_chart_csv_data.group_df.keys():
            item = QStandardItem(key)
            item.setCheckState(Qt.Checked)
            item.setCheckable(True)
            self.group_data_list.appendRow(item)
        self.group_data_list.itemChanged.connect(self.group_data_changed)

    def get_group_params(self) -> Union[list, None]:
        """
        获取Group By
        :return:
        """
        group_list = []
        for i in range(len(UiGlobalVariable.SUMMARY_GROUP)):
            temp = self.group_item_list.item(i)  # type:QStandardItem
            if temp.checkState() == Qt.Checked:
                group_list.append(temp.text())
        return group_list if group_list else None

    def get_da_group_params(self) -> Union[list, None]:
        """
        获取Group By
        :return:
        """
        group_list = []
        for i in range(len(UiGlobalVariable.DATA_GROUP)):
            temp = self.da_group_item_list.item(i)  # type:QStandardItem
            if temp.checkState() == Qt.Checked:
                group_list.append(temp.text())
        return group_list if group_list else None

    def get_group_select_params(self) -> Union[list, None]:
        group_set = set()
        for i in range(len(self.li.to_chart_csv_data.group_df)):
            temp = self.group_data_list.item(i)  # type:QStandardItem
            if temp.checkState() == Qt.Checked:
                group_set.add(temp.text())
        return group_set if group_set else None

    @Slot()
    def checkbox_changed(self):
        self.li.set_data_group(self.get_group_params(), self.get_da_group_params())
        self.init_listView_3()

    @Slot()
    def group_data_changed(self):
        self.li.to_chart_csv_data.select_group = self.get_group_select_params()
        self.li.refresh_chart()

    @Slot()
    def on_pushButton_pressed(self):
        self.group_data_list.itemChanged.disconnect(self.group_data_changed)
        for index in self.listView_3.selectedIndexes():
            temp = self.group_data_list.item(index.row())
            temp.setCheckState(Qt.Checked)
        self.group_data_list.itemChanged.connect(self.group_data_changed)
        self.group_data_changed()

    @Slot()
    def on_pushButton_2_pressed(self):
        self.group_data_list.itemChanged.disconnect(self.group_data_changed)
        for index in self.listView_3.selectedIndexes():
            temp = self.group_data_list.item(index.row())
            temp.setCheckState(Qt.Unchecked)
        self.group_data_list.itemChanged.connect(self.group_data_changed)
        self.group_data_changed()


