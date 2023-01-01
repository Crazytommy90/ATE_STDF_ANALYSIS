"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2021/11/18 16:22
@Software: PyCharm
@File    : mdi_data_concat.py
@Remark  : 引用引用
"""
from typing import Dict

from PySide2.QtWidgets import QWidget, QListWidgetItem, QCheckBox
from PySide2.QtCore import Slot, Qt, Signal

from ui_component.ui_common.ui_utils import MdiLoad
from ui_component.ui_main.ui_designer.ui_mdi_data_contact import Ui_Form

import pandas as pd


class ContactWidget(QWidget, Ui_Form):
    id_cache = None
    mdi_cache = None
    dataSignal = Signal(pd.DataFrame)  # 送出SummaryCore
    messageSignal = Signal(str)  # 追加文本信息

    def __init__(self, parent=None, icon=None):
        super(ContactWidget, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(icon)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def insert(self, mdi_cache: Dict[int, MdiLoad]):
        self.listWidget.clear()
        self.comboBox.clear()
        self.id_cache = {}
        self.mdi_cache = mdi_cache
        items = []
        for each in mdi_cache.values():
            # if not each.mdi.have_cache_data:
            #     continue
            box = QCheckBox(each.name)  # 实例化一个QCheckBox，吧文字传进去item
            items.append(each.name)
            self.id_cache[each.name] = each.mdi_count
            item = QListWidgetItem()  # 实例化一个Item，QListWidget，不能直接加入QCheckBox
            self.listWidget.addItem(item)  # 把QListWidgetItem加入QListWidget
            self.listWidget.setItemWidget(item, box)  # 再把QCheckBox加入QListWidgetItem
        self.comboBox.addItems(items)

    @Slot()
    def on_pushButton_pressed(self):
        self.get_choose_mdi()
        self.close()

    def get_choose_mdi(self):
        """
        emit一个SummaryCore
        """
        choose_mdi = []
        for i in range(self.listWidget.count()):
            item = self.listWidget.itemWidget(self.listWidget.item(i))  # type: QCheckBox
            if item.isChecked():
                choose_mdi.append(self.id_cache[item.text()])

        new_summary_list = []
        for each_id in choose_mdi:
            mdi = self.mdi_cache[each_id].mdi
            if mdi.summary.ready is False:
                return self.messageSignal.emit("有mdi中的数据并未做载入动作")
            new_summary_list.append(mdi.summary.summary_df)

        self.dataSignal.emit(pd.concat(new_summary_list))
        self.messageSignal.emit("Concat数据传送完成")
