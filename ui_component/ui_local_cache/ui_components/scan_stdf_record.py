#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : scan_stdf_record.py
@Author  : Link
@Time    : 2022/11/23 22:43
@Mark    : 
"""
import math
from typing import List

from PySide2.QtCore import Slot, Qt, QDate
from PySide2.QtWidgets import QWidget, QAbstractItemView, QTableWidget, QComboBox

from ui_component.ui_local_cache.ui_designer.ui_scan_stdf_widget import Ui_Form as ScanStdfRecordForm
from ui_component.ui_variable import UiGlobalVariable

from web_core.resp import Resp
from workspace_core.core_to_analysis_stdf.stdf_variable import RespUrl, GlobalVariable


class ScanStdfRecordWidget(QWidget, ScanStdfRecordForm):
    """
    用于检测那些STDF数据导入有报错
    """
    ready = False

    def __init__(self, parent=None, icon=None):
        super(ScanStdfRecordWidget, self).__init__()
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle("物料测试数据报表")
        self.resp = Resp()
        if icon:
            self.setWindowIcon(icon)

        self.ui_init()
        self.signal_init()
        self.ui_run()

    def get_filed_list(self, filed="LEVEL_NM", **kwargs):
        api = RespUrl.FIELD_INFO + filed
        data = self.resp.request_data_ana(self.resp.request_get(api, kwargs))
        if data is None:
            return []
        filed_list = data["filed_list"]
        return [each[filed] for each in filed_list]

    def ui_init(self):
        self.spinBox_3.setValue(1)
        self.tableWidget.set_table_head(GlobalVariable.RECORD_HEAD)

        self.dateEdit.setDate(QDate.currentDate().addDays(-60))
        self.dateEdit_2.setDate(QDate.currentDate())
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit_2.setCalendarPopup(True)

    def ui_run(self):
        if self.ready:
            return
        self.comboBox_5.addItems(self.get_filed_list("LEVEL_NM"))
        self.level_nm_change("")
        self.ready = True

    def combobox_changed(self, box: QComboBox, filed: str = "SUB_CON", **kwargs):
        box.blockSignals(True)
        box.clear()
        box.blockSignals(False)
        box.addItems(
            self.get_filed_list(filed, **kwargs)
        )

    def signal_init(self):
        self.comboBox_5.currentIndexChanged[str].connect(self.level_nm_change)

        self.lineEdit.returnPressed.connect(self.search_data)
        self.lineEdit_2.returnPressed.connect(self.search_data)

    def level_nm_change(self, event):
        self.combobox_changed(self.comboBox, "SUB_CON",
                              LEVEL_NM=self.comboBox_5.currentText()
                              )

    def get_resp_params(self):
        return {
            "LEVEL_NM": self.comboBox_5.currentText(),
            "SUB_CON": self.comboBox.currentText(),
            "LOT_ID": self.lineEdit.text(),
            "WAFER_ID": self.lineEdit_2.text(),
            "START_T": self.dateEdit.date().toString("yyyy-MM-dd"),
            "FINISH_T": self.dateEdit_2.date().addDays(1).toString("yyyy-MM-dd"),
            "READ_ALL": self.checkBox.isChecked(),
            "PAGE_SIZE": self.spinBox.value(),
            "CURR_PAGE": self.spinBox_3.value(),
        }

    def params_init(self):
        self.spinBox_3.blockSignals(True)
        self.spinBox_3.setValue(1)
        self.spinBox_3.blockSignals(False)

    @Slot()
    def on_spinBox_3_valueChanged(self):
        print(self.spinBox_3.value())

    def search_data(self):
        """
        检索导入的Record
        :return:
        """
        print("search_data")
        self.params_init()
        api = RespUrl.QT_WEB_RECORD
        data = self.resp.request_data_ana(self.resp.request_get(api, params=self.get_resp_params()))
        if data is None:
            return
        total: int = data["total"]
        max_page = math.ceil(total / self.spinBox.value())
        self.spinBox_3.setMaximum(max_page + 1)
        self.spinBox_4.setMaximum(max_page + 1)
        self.spinBox_2.setValue(total)
        self.tableWidget.set_table_data(data["record_list"])


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QMainWindow, QApplication

    app = QApplication(sys.argv)
    win = ScanStdfRecordWidget()
    win.show()
    sys.exit(app.exec_())
