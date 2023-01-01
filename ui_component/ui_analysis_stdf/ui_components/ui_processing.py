#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : ui_processing.py
@Author  : Link
@Time    : 2022/7/31 13:35
@Mark    : 
"""

from typing import Union

import numpy as np
from PySide2.QtGui import QStandardItemModel, QStandardItem, Qt
from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Slot, QModelIndex

from ui_component.ui_app_variable import UiGlobalVariable
from ui_component.ui_analysis_stdf.ui_designer.ui_processing import Ui_Form

import pyqtgraph as pg
import pandas as pd


class ProcessWidget(QWidget, Ui_Form):
    """
    需要的时候再运行, 即功能打开时运行而不是数据一改变就运行
    """
    select_item_list = QStandardItemModel()
    top_item_list = QStandardItemModel()  # yield, avg, limit ...
    bot_item_list = QStandardItemModel()  # group by item
    li = None

    def __init__(self, parent=None, icon=None):
        super(ProcessWidget, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("制程能力")
        if icon:
            self.setWindowIcon(icon)
        self.listView_3.setModel(self.select_item_list)
        self.listView_2.setModel(self.top_item_list)
        self.listView_2.clicked.connect(self.top_row_change)
        self.listView.setModel(self.bot_item_list)
        self.listView.clicked.connect(self.bot_row_change)
        self.cpk_info_table = pg.TableWidget(self)
        self.verticalLayout.addWidget(self.cpk_info_table)
        self.cpk_info_table.setEditable(True)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 15)

        self.init_listView_3()
        self.init_listView_2()

    def init_listView_3(self):
        self.select_item_list.clear()
        for index, each in enumerate(UiGlobalVariable.PROCESS_VALUE):
            item = QStandardItem(each)
            item.setCheckState(Qt.Unchecked)
            item.setCheckable(True)
            if index == 0:
                item.setCheckState(Qt.Checked)
            self.select_item_list.appendRow(item)

    def get_listView_3_choose_items(self) -> Union[list, None]:
        select_item_list = []
        for index, each in enumerate(UiGlobalVariable.PROCESS_VALUE):
            temp = self.select_item_list.item(index)
            if temp.checkState() == Qt.Checked:
                select_item_list.append(temp.text())
        return select_item_list if select_item_list else None

    def init_listView_2(self):
        self.top_item_list.clear()
        for index, each in enumerate(UiGlobalVariable.PROCESS_TOP_ITEM_LIST):
            item = QStandardItem(each)
            self.top_item_list.appendRow(item)

    def gen_listView(self):
        """
        通过 GROUP 和 DA_GROUP 来做处理
        :return:
        """
        bot_item_list_df = self.li.front_df["GROUP"] + "_" + self.li.front_df["DA_GROUP"]  # type:pd.DataFrame
        bot_item_list = bot_item_list_df.drop_duplicates(keep="first").tolist()
        self.bot_item_list.clear()
        for index, each in enumerate(bot_item_list):
            item = QStandardItem(each)
            self.bot_item_list.appendRow(item)

    def set_data(self, li):
        if self.li is not None:
            self.li.front_df_signal.disconnect(self.set_front_df_process)
        self.li = li
        self.li.front_df_signal.connect(self.set_front_df_process)

    @Slot()
    def set_front_df_process(self):
        """
        将数据显示到前台中. 一般在这里的时候, 数据已经经理了group by阶段了
        :return:
        """
        if self.li is None:
            return False
        self.gen_listView()

    @Slot(QModelIndex)
    def top_row_change(self, model_index: QModelIndex):
        """
        放良率. 和 avg 对比
        :param model_index:
        :return:
        """
        if self.li is None:
            return

        if "GROUP" not in self.li.front_df or "DA_GROUP" not in self.li.front_df:
            return

        if model_index.data() == "yield":
            df_group = self.li.front_df.groupby(["GROUP", "DA_GROUP"])
            yield_data = []  # type:list
            for key, each_df in df_group:
                if not isinstance(key, tuple):
                    item_name = str(key)
                else:
                    item_name = '-'.join([str(ea) for ea in key])
                total = len(each_df)
                fail_num = len(each_df[each_df["FAIL_FLAG"] != 1])
                pass_num = len(each_df) - fail_num
                yield_data.append({
                    "Item": item_name,
                    "Total": total,
                    "Pass": pass_num,
                    "Fail": fail_num,
                    "Yield": "{}%".format(round(pass_num / total * 100, 3)),
                })
            self.cpk_info_table.setData(yield_data)
            return

        if model_index.data() == "data":
            """
            这个稍微复杂一些, 先将数据都获取到, 然后再整理起来
            """
            item_list = self.get_listView_3_choose_items()
            if item_list is None:
                return
            df_group = self.li.front_df.groupby(["GROUP", "DA_GROUP"])
            group_cpk_dict = dict()
            for key, each_df in df_group:
                if not isinstance(key, tuple):
                    item_name = str(key)
                else:
                    item_name = '-'.join([str(ea) for ea in key])
                _cpk_df = each_df[each_df["FAIL_FLAG"] == 1][self.li.front_limit_dict.keys()]
                _mean = _cpk_df.mean()
                _std = _cpk_df.std()
                temp_data_list = []
                for index, item_key in enumerate(self.li.front_limit_dict.keys()):
                    item = self.li.front_limit_dict[item_key]
                    temp_std = _std[item_key]
                    temp_mean = _mean[item_key]
                    if temp_std == 0:
                        cpk = 0
                    else:
                        cpk = round(min(
                            [(item.h_limit - temp_mean) / (3 * temp_std),
                             (temp_mean - item.l_limit) / (3 * temp_std)])
                            , 6)
                    temp_dict = {
                        "SORT": item.test_sort,
                        "TEST_TYPE": item.test_type,
                        "Text": item_key,
                        "UNITS": item.unit,
                        "LO_LIMIT": item.l_limit,
                        "HI_LIMIT": item.h_limit,
                        "LO_LIMIT_TYPE": item.l_limit_type,
                        "HI_LIMIT_TYPE": item.h_limit_type,
                        f"{item_name}_Avg": round(_mean[item_key], 5),
                        f"{item_name}_Stdev": round(_std[item_key], 5),
                        f"{item_name}_Cpk": cpk,
                    }
                    temp_data_list.append(temp_dict)
                group_cpk_dict[item_name] = temp_data_list

            """
            前台展示数据
            """
            data_table_list = []
            for index, key in enumerate(group_cpk_dict.keys()):
                temp_each_data = group_cpk_dict[key]
                if index == 0:
                    for i, row in enumerate(temp_each_data):
                        d = {
                            "SORT": row["SORT"],
                            "TEST_TYPE": row["TEST_TYPE"],
                            "Text": row["Text"],
                            "UNITS": row["UNITS"],
                            "LO_LIMIT": row["LO_LIMIT"],
                            "HI_LIMIT": row["HI_LIMIT"],
                            "LO_LIMIT_TYPE": row["LO_LIMIT_TYPE"],
                            "HI_LIMIT_TYPE": row["HI_LIMIT_TYPE"],
                        }
                        for each in item_list:
                            if each == "mean":
                                d[f"{key}_Avg"] = row[f"{key}_Avg"]
                            if each == "std":
                                d[f"{key}_Stdev"] = row[f"{key}_Stdev"]
                            if each == "cpk":
                                d[f"{key}_Cpk"] = row[f"{key}_Cpk"]
                        data_table_list.append(d)
                else:
                    for i, row in enumerate(temp_each_data):
                        for each in item_list:
                            if each == "mean":
                                data_table_list[i][f"{key}_Avg"] = row[f"{key}_Avg"]
                            if each == "std":
                                data_table_list[i][f"{key}_Stdev"] = row[f"{key}_Stdev"]
                            if each == "cpk":
                                data_table_list[i][f"{key}_Cpk"] = row[f"{key}_Cpk"]
            self.cpk_info_table.setData(data_table_list)
            return

    @Slot(QModelIndex)
    def bot_row_change(self, model_index: QModelIndex):
        """
        放单个数据, 单个数据可以有value类型和diff类型
        :param model_index:
        :return:
        """
        if self.radioButton_2.isChecked():
            group, da_group = model_index.data().split("_")
            df = self.li.front_df[(self.li.front_df["GROUP"] == group) & (self.li.front_df["DA_GROUP"] == da_group)]

            cpk_list = []
            first_fail_dict = {}
            for num in df[df["FAIL_FLAG"] != 1]["FIRST_FAIL"]:
                if num not in first_fail_dict:
                    first_fail_dict[num] = 1
                    continue
                first_fail_dict[num] += 1

            temp_df = df[df["FAIL_FLAG"] == 1][self.li.front_limit_dict.keys()]
            _mean, _min, _max, _std, _median = temp_df.mean(), temp_df.min(), temp_df.max(), temp_df.std(), temp_df.median()
            for key, item in self.li.front_limit_dict.items():
                try:
                    test_num, test_txt = key.split(":", 1)
                except ValueError:
                    raise Exception("重大错误: 测试数据测试项目没有指定TEST_NO和TEST_TEXT,测试程序漏洞@!!!!!")
                reject_qty = 0
                logic_or = []
                if item.l_limit_type == ">":
                    logic_or.append((df[key] <= item.l_limit))
                if item.l_limit_type == ">=":
                    logic_or.append((df[key] < item.l_limit))
                if item.h_limit_type == "<":
                    logic_or.append((df[key] >= item.h_limit))
                if item.h_limit_type == "<=":
                    logic_or.append((df[key] > item.h_limit))
                if item.h_limit_type == "=":
                    logic_or.append((df[key] != item.h_limit))
                if len(logic_or) == 1:
                    items = logic_or[0]
                    reject_qty = len(df.loc[items])
                if len(logic_or) > 1:
                    items = np.logical_or(*logic_or)
                    reject_qty = len(df.loc[items])

                fail_qty = first_fail_dict.get(item.test_num, 0)
                temp_std, temp_mean = _std[key], _mean[key]
                cpk = 0 if temp_std == 0 else round(min([(item.h_limit - temp_mean) / (3 * temp_std),
                                                         (temp_mean - item.l_limit) / (3 * temp_std)]), 6)
                temp_dict = {
                    "SORT": item.test_sort,
                    "TEST_TYPE": item.test_type,
                    "TEST_NUM": test_num,
                    "TEST_TEXT": test_txt,
                    "UNITS": str(item.unit),
                    "LO_LIMIT": item.l_limit,
                    "HI_LIMIT": item.h_limit,
                    "Average": round(_mean[key], 6),
                    "Stdev": round(_std[key], 6),
                    "Cpk": cpk,
                    "Text": key,
                    "Total": len(df),
                    "Fail": fail_qty,
                    "Fail/Total": "{}%".format(round(fail_qty / len(df) * 100, 3)),
                    "Reject": reject_qty,
                    "Reject/Total": "{}%".format(round(reject_qty / len(df) * 100, 3)),
                    "Min": round(_min[key], 6),
                    "Max": round(_max[key], 6),
                    "LO_LIMIT_TYPE": item.l_limit_type,
                    "HI_LIMIT_TYPE": item.h_limit_type,
                }
                cpk_list.append(temp_dict)
            self.cpk_info_table.setData(cpk_list)
            return
        if self.radioButton.isChecked():
            """
            DIFF, 只看均值以及PTR项目
            """
            group, da_group = model_index.data().split("_")
            diff_compare_df = self.li.front_df[
                (self.li.front_df["GROUP"] == group) & (self.li.front_df["DA_GROUP"] == da_group)]
            length = len(diff_compare_df)
            start, stop = int(length * 0.05), int(length * 0.95)

            diff_data_list = []
            df_group = self.li.front_df.groupby(["GROUP", "DA_GROUP"])
            for test_item, test_tuple in self.li.front_limit_dict.items():  # type:str, GlobalVariable.LimitClass
                if test_tuple.test_type == "FTR":
                    continue
                temp_dict = dict()
                diff_data_list.append(temp_dict)
                temp_dict["SORT"] = test_tuple.test_sort
                temp_dict["ITEM"] = test_item
                temp_dict["Unit"] = test_tuple.unit
                temp_dict["LO_LIMIT"] = test_tuple.l_limit
                temp_dict["HI_LIMIT"] = test_tuple.h_limit
                temp_dict["LO_LIMIT_TYPE"] = test_tuple.l_limit_type
                temp_dict["HI_LIMIT_TYPE"] = test_tuple.h_limit_type

                compare_data = np.mean(sorted(diff_compare_df[test_item].to_list())[start: stop])
                for key, each_df in df_group:
                    if not isinstance(key, tuple):
                        item_name = str(key)
                    else:
                        item_name = '-'.join([str(ea) for ea in key])
                    temp_data = each_df[test_item].to_list()
                    temp_length = len(each_df)
                    temp_start, temp_stop = int(temp_length * 0.05), int(temp_length * 0.95)
                    temp_data = sorted(temp_data)[temp_start: temp_stop]
                    temp_data = np.mean(temp_data)
                    gap = compare_data - temp_data
                    temp_dict[item_name] = gap

            self.cpk_info_table.setData(diff_data_list)
            return
