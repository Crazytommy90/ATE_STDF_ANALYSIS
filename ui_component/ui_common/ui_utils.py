#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : utils.py
@Author  : Link
@Time    : 2022/4/30 21:52
@Mark    :
"""
from typing import List, Union, Dict, Tuple

from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt, QTimer
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QHeaderView, QTableWidget

from common.app_variable import GlobalVariable
from common.func import timestamp_to_str


class TreeUtils:
    @staticmethod
    def set_data_to_tree(tree_widget: QTreeWidget, data_list: List[dict], is_checked: bool):
        tree_widget.blockSignals(True)
        tree_widget.clear()
        tree_widget.setColumnCount(len(GlobalVariable.LOT_TREE_HEAD))
        tree_widget.setHeaderLabels(GlobalVariable.LOT_TREE_HEAD)
        tree_widget.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        TreeUtils.data_item_to_tree(tree_widget, data_list, is_checked)
        tree_widget.blockSignals(False)

    @staticmethod
    def data_item_to_tree(tree_widget: QTreeWidget, data_list: List[dict], is_checked: bool):
        """
        确定的结构, 不要用到dict
        :param tree_widget:
        :param data_list:
        :param is_checked:
        :return:
        """

        for node in data_list:
            node_item = QTreeWidgetItem(tree_widget)
            for column, key in enumerate(GlobalVariable.LOT_TREE_HEAD):
                if key not in node:
                    continue
                text = node[key]
                if key[-2:] == "_T":
                    text = timestamp_to_str(text)
                if not isinstance(text, str):
                    text = str(text)
                node_item.setText(column, text)
            node_item.setCheckState(0, Qt.Checked if is_checked else Qt.Unchecked)
            if "children" in node:
                TreeUtils.data_item_to_tree(node_item, node["children"], is_checked)

    @staticmethod
    def set_select_tree_data(tree_widget: QTreeWidget, data: List[dict], is_checked=True):
        """
        内嵌循环
        :param tree_widget:
        :param data:
        :param is_checked:
        :return:
        """
        tree_widget.blockSignals(True)
        tree_widget.clear()
        tree_widget.setColumnCount(GlobalVariable.LOT_TREE_HEAD_LENGTH)
        tree_widget.setHeaderLabels(GlobalVariable.LOT_TREE_HEAD)
        TreeUtils.data_item_to_tree(tree_widget, data, is_checked)

    @staticmethod
    def item_set_check_state(node: QTreeWidgetItem, check_state: Qt.CheckState):
        node.setCheckState(0, check_state)
        if not node.childCount():
            return
        for i in range(node.childCount()):
            c_node = node.child(i)
            TreeUtils.item_set_check_state(c_node, check_state)

    @staticmethod
    def parent_set_check_state(node: QTreeWidgetItem):
        """
        进来的node, 下面一定是all check& all no check, 所以只需要逐层往上遍历即可
        """
        if node.parent() is None:
            return
        parent = node.parent()
        checked = 0
        for i in range(parent.childCount()):
            if parent.child(i).checkState(0) == Qt.Checked:
                checked += 1
        if checked == 0:
            parent.setCheckState(0, Qt.Unchecked)
        elif checked == parent.childCount():
            parent.setCheckState(0, Qt.Checked)
        else:
            parent.setCheckState(0, Qt.PartiallyChecked)

        TreeUtils.parent_set_check_state(parent)

    @staticmethod
    def tree_item_change(tree_widget: QTreeWidget, e: QTreeWidgetItem):
        """
        需要适配多层, 只能对第一个进行选取
        :param tree_widget:
        :param e:
        :return:
        """
        tree_widget.blockSignals(True)
        TreeUtils.item_set_check_state(e, e.checkState(0))
        TreeUtils.parent_set_check_state(e)
        tree_widget.blockSignals(False)

    @staticmethod
    def get_tree_ids(tree_widget: QTreeWidget):
        item = QTreeWidgetItemIterator(tree_widget)
        ids = []
        while item.value():
            if item.value().checkState(0) == Qt.Checked:
                t = item.value().text(0)
                if t == '':
                    pass
                else:
                    ids.append(int(t))
            item = item.__iadd__(1)
        return ids


class QTableUtils:
    @staticmethod
    def get_table_widget_test_id(table_widget: QTableWidget) -> Union[List[int], None]:
        """
        还是按照小工具的方式, 先获取选中的测试项的行,
        再遍历获取TEST_ID,返回
        :return:
        """
        items = table_widget.selectedItems()
        select_index = set([
            table_widget.row(each) for each in items
        ])
        if not select_index:
            return None
        select_index = sorted(list(select_index))
        test_ids = []
        for index in select_index:
            test_id = int(table_widget.item(index, GlobalVariable.TEST_ID_COLUMN).text())
            test_ids.append(test_id)
        return test_ids

    @staticmethod
    def get_select_new_limit(table_widget: QTableWidget,
                             ) -> Union[None, Dict[int, Tuple[float, float, str, str]]]:
        test_ids = QTableUtils.get_table_widget_test_id(table_widget)
        if test_ids is None:
            print("未选取测试项目无法进行临时数据生成!")
            return
        limit_new = {}
        for index in range(table_widget.rowCount()):
            test_id = int(table_widget.item(index, GlobalVariable.TEST_ID_COLUMN).text())
            if test_id not in test_ids:
                continue
            limit_min = float(table_widget.item(index, GlobalVariable.LO_LIMIT_COLUMN).text())
            limit_max = float(table_widget.item(index, GlobalVariable.HI_LIMIT_COLUMN).text())
            l_type = table_widget.item(index, GlobalVariable.LO_LIMIT_TYPE_COLUMN).text()
            h_type = table_widget.item(index, GlobalVariable.HI_LIMIT_TYPE_COLUMN).text()
            limit_new[test_id] = (limit_min, limit_max, l_type, h_type)
        return limit_new

    @staticmethod
    def get_all_new_limit(table_widget: QTableWidget,
                          ) -> Dict[int, Tuple[float, float, str, str]]:
        limit_new = {}
        for index in range(table_widget.rowCount()):
            test_id = int(table_widget.item(index, GlobalVariable.TEST_ID_COLUMN).text())
            limit_min = float(table_widget.item(index, GlobalVariable.LO_LIMIT_COLUMN).text())
            limit_max = float(table_widget.item(index, GlobalVariable.HI_LIMIT_COLUMN).text())
            l_type = table_widget.item(index, GlobalVariable.LO_LIMIT_TYPE_COLUMN).text()
            h_type = table_widget.item(index, GlobalVariable.HI_LIMIT_TYPE_COLUMN).text()
            limit_new[test_id] = (limit_min, limit_max, l_type, h_type)
        return limit_new


class QWidgetUtils:
    @staticmethod
    def widget_change_color(widget: QWidget, background_color: str = "#333333"):
        """
        给widget改变背景色, 改变前 widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        :param widget:
        :param background_color:
        :return:
        """
        widget.setStyleSheet("background-color: %s;" % background_color)
        QTimer.singleShot(500, lambda: widget.setStyleSheet(""))


class MdiLoad:
    mdi_count = None  # type:int
    mdi = None  # type:QWidget
    name = None  # type:str

    def __init__(self, mdi_count: int, mdi: QWidget, name: str):
        self.mdi_count = mdi_count
        self.mdi = mdi
        self.name = name
