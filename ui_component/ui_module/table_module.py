#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : table_module.py
@Author  : Link
@Time    : 2022/5/1 21:39
@Mark    : 
"""
from typing import Union, List, Set, Dict

from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QTableWidgetItem, QTableWidget, QComboBox, QStyledItemDelegate
from pyqtgraph import TableWidget

from common.app_variable import GlobalVariable
from common.func import timestamp_to_str

translate = QtCore.QCoreApplication.translate


class PauseTableWidget(TableWidget):

    def __init__(self, *args, **kwds):
        super(PauseTableWidget, self).__init__(*args, **kwds)

        self.contextMenu.addAction(translate("PauseTableWidget", 'Paste')).triggered.connect(self.paste)

    def get_select_row_set(self, column: int) -> Union[None, set]:
        selection = self.selectedRanges()
        if not selection:
            return None

    def paste(self):
        """
        将剪切板的数据复制到TableWidget中
        先找到选中的行列位置
        再根据数据来进行黏贴
        """
        text = QtWidgets.QApplication.clipboard().text()  # type:str
        split_text_rows = text.split('\n')
        if len(split_text_rows) == 0:
            return
        text_rows = split_text_rows[1:-1]
        selection = self.selectedRanges()
        if not selection:
            return
        selection = selection[0]
        select_row = selection.topRow()
        select_column = selection.leftColumn()

        pause_row = len(text_rows)
        for i in range(pause_row):
            item_row = i + select_row
            row_split_text = text_rows[i].split('\t')
            for j in range(len(row_split_text)):
                item_column = select_column + j
                item = self.item(item_row, item_column)  # type:QtWidgets.QTableWidgetItem
                if item is None:
                    continue
                item.setText(row_split_text[j])

    def keyPressEvent(self, ev):
        if ev.matches(QtGui.QKeySequence.StandardKey.Paste):
            ev.accept()
            self.paste()
        else:
            super().keyPressEvent(ev)


class SearchTableWidget(TableWidget):
    """
    用在需要选取在哪行的table上, 从数据库中获取id, id都是小写
    """
    temp_data = None  # type:List[dict]
    cache_index = None  # type:dict
    q_font = QFont("", 8)

    def setData(self, data):
        self.horizontalHeader().setFont(self.q_font)
        self.setFont(self.q_font)
        self.cache_index = {}
        self.temp_data = data
        self._sorting = False
        super(SearchTableWidget, self).setData(data)
        self.set_cache_index()

    def set_cache_index(self):
        if self.temp_data is None:
            return
        for index, each in enumerate(self.temp_data):
            id_cache = self.cache_index.get(each["METHOD"], None)
            if id_cache is None:
                id_cache = {}
                self.cache_index[each["METHOD"]] = id_cache
            id_cache[each["ID"]] = index

    def get_table_select(self) -> Union[List[dict], None]:
        """
        需要第一列是id
        """
        items = self.selectedItems()
        select_index = set([
            self.row(each) for each in items
        ])
        if not select_index:
            return None
        data = []
        for index in select_index:
            method = self.item(index, 1).text()
            sql_id = int(self.item(index, 0).text())
            index = self.cache_index[method][sql_id]
            data.append(self.temp_data[index])
        return data

    def get_ids(self):
        items = self.selectedItems()
        select_index = set([
            self.row(each) for each in items
        ])
        ids = []
        if not select_index:
            return ids
        for each in select_index:
            ids.append(int(self.item(each, 0).text()))
        return ids


class BaseTableWidget(QTableWidget):
    table_count = 0
    table_head_index = None
    table_head = None
    temp_table_data = None
    q_font = QFont("", 8)

    def clear(self) -> None:
        self.temp_table_data = None
        self.table_count = 0
        super(BaseTableWidget, self).clear()

    def clearContents(self) -> None:
        self.temp_table_data = None
        self.table_count = 0
        super(BaseTableWidget, self).clearContents()

    def set_table_head(self, table_head: List[str]):
        """

        :param table_head:
        :return:
        """
        self.table_head = table_head
        self.table_head_index = {}
        for index, each in enumerate(self.table_head):
            self.table_head_index[each] = index
        self.setColumnCount(len(table_head))
        self.setHorizontalHeaderLabels(table_head)
        self.horizontalHeader().setFont(self.q_font)

    def update_table_data(self, index: int, column: str, item: QTableWidgetItem) -> bool:
        if index >= self.table_count:
            return False
        self.setItem(index, self.table_head_index[column], item)
        return True

    def paste(self):
        text = QtWidgets.QApplication.clipboard().text()  # type:str
        split_text_rows = text.split('\n')
        if len(split_text_rows) == 0:
            return
        text_rows = split_text_rows[1:-1]
        selection = self.selectedRanges()
        if not selection:
            return
        selection = selection[0]
        select_row = selection.topRow()
        select_column = selection.leftColumn()

        pause_row = len(text_rows)
        for i in range(pause_row):
            item_row = i + select_row
            row_split_text = text_rows[i].split('\t')
            for j in range(len(row_split_text)):
                item_column = select_column + j
                item = self.item(item_row, item_column)  # type:QtWidgets.QTableWidgetItem
                if item is None:
                    continue
                item.setText(row_split_text[j])

    def keyPressEvent(self, ev):
        if ev.matches(QtGui.QKeySequence.StandardKey.Paste):
            ev.accept()
            self.paste()
        else:
            super().keyPressEvent(ev)


class ReadOnlyItemDelegate(QStyledItemDelegate):
    """
    委托, 让TableWidget内的Item无法被编辑
    """

    def createEditor(self, parent, option, index):
        return None


class QtTableWidget(BaseTableWidget):
    """
    用在需要读取复测数据的table上, 只能用专用的class
    ReadR 和 PartFlg
    """

    def set_table_data(self, table_data: List[dict]) -> bool:
        """
        第一列设置checkbox, 列名为是否为最后复测，勾选后只会选取这个数据的Fail Result
        TODO: 第二列设置为 PART_TYPE
        第三列设置message, 用来提示使用人员STDF处理进程
        后面列则为MIR相关数据

        :param table_data:
        :return:
        """
        if len(table_data) == 0:
            return False
        self.temp_table_data = table_data
        self.table_count = len(table_data)
        self.setRowCount(self.table_count)
        for row, each_row in enumerate(table_data):

            check_item = QTableWidgetItem()
            check_item.setCheckState(Qt.Unchecked)
            check_item.setText("R_FAIL")
            self.setItem(row, 0, check_item)

            combobox_column = QComboBox()
            combobox_column.addItems(GlobalVariable.PART_FLAGS)
            self.setCellWidget(row, 1, combobox_column)

            for key, item in each_row.items():
                if key in GlobalVariable.SKIP_FILE_TABLE_DATA_HEAD:
                    continue
                if key not in self.table_head_index:
                    continue
                column = self.table_head_index[key]
                if isinstance(item, QTableWidgetItem):
                    self.setItem(row, column, item)
                else:
                    if key[-2:] == "_T":
                        item = QTableWidgetItem(timestamp_to_str(item))
                    else:
                        item = QTableWidgetItem(str(item))
                    self.setItem(row, column, item)
        """
        重置 progressBar
        """
        # self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resizeColumnsToContents()
        self.setFont(self.q_font)
        self.resizeRowsToContents()
        return True

    def get_part_flag(self) -> Dict[int, int]:
        li = dict()
        for row in range(self.table_count):
            combobox = self.cellWidget(row, 1)  # type:QComboBox
            li[row] = combobox.currentIndex()
        return li

    def set_all_part_flag(self, flag: int):
        for row in range(self.table_count):
            combobox = self.cellWidget(row, 1)  # type:QComboBox
            combobox.setCurrentIndex(flag)

    def update_temp_part_data(self):
        if self.temp_table_data is None:
            return
        flag_dict = self.get_part_flag()
        for index, each in enumerate(self.temp_table_data):
            each["PART_FLAG"] = flag_dict[index]

    def get_retest_row(self) -> Set[int]:
        """
        获取选取重测数据的下标
        :return:
        """
        li = set()
        for row in range(self.table_count):
            if self.item(row, 0).checkState() == Qt.Checked:
                li.add(row)
        return li

    def update_temp_r_data(self):
        if self.temp_table_data is None:
            return
        r_set = self.get_retest_row()
        for index, each in enumerate(self.temp_table_data):
            if index in r_set:
                each["READ_FAIL"] = True
            else:
                each["READ_FAIL"] = False

    def set_read_all_r(self, status):
        for row in range(self.table_count):
            self.item(row, 0).setCheckState(status)

    def update_temp_data(self):
        self.update_temp_part_data()
        self.update_temp_r_data()
