"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/5/9 17:45
@Software: PyCharm
@File    : ui_table_load_widget.py
@Remark  : 
"""
from PySide2.QtCore import Slot, Qt, QTimer
from PySide2.QtGui import QColor, QFont
from PySide2.QtWidgets import QWidget, QAbstractItemView, QTableWidget, QMessageBox

from common.app_variable import GlobalVariable
from common.li import Li, SummaryCore
from ui_component.ui_analysis_stdf.ui_designer.ui_table_load import Ui_Form as TableLoadForm
from ui_component.ui_common.ui_utils import QTableUtils, QWidgetUtils
from ui_component.ui_module.table_module import PauseTableWidget

import pyqtgraph as pg

pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class TableLoadWidget(QWidget, TableLoadForm):
    """
    Table
    .setFont(QFont(None, 8));
    .resizeRowsToContents()
    """
    li: Li = None
    summary: SummaryCore = None

    def __init__(self, li: Li, summary: SummaryCore, parent=None):
        super(TableLoadWidget, self).__init__(parent)
        self.setupUi(self)
        self.li = li
        self.summary = summary
        self.setWindowTitle("Data TEST NO&ITEM Analysis")
        self.cpk_info_table = PauseTableWidget(self)  # type:QTableWidget
        self.cpk_info_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.cpk_info_table.setEditable(True)
        # self.cpk_info_table.setFont(QFont("", 8))
        # self.cpk_info_table.horizontalHeader().sectionResized.connect(self.get_head_resize)
        self.horizontalLayout.addWidget(self.cpk_info_table)
        self.gw = pg.GraphicsLayoutWidget()
        self.gw.ci.setContentsMargins(0, 0, 0, 0)
        self.plot = self.gw.addPlot()
        self.horizontalLayout.addWidget(self.gw)
        self.init_plot()
        self.init_table_signal()

    def init_plot(self):
        self.gw.setMaximumWidth(20)
        self.plot.setMouseEnabled(x=False, y=False)
        self.plot.setXRange(-0.2, 2.6)
        self.plot.showAxis('bottom', False)
        self.plot.showAxis('left', False)
        self.plot.hideButtons()

    def init_table_signal(self):
        """
        监控排序信号, 数据载入后会自动排序
        :return:
        """
        self.cpk_info_table.horizontalHeader().sortIndicatorChanged.connect(self.plot_scrollbar)

    def cal_table(self):
        if self.li.capability_key_list is None:
            return
        self.cpk_info_table.setData(self.li.capability_key_list)
        self.cpk_info_table.sortByColumn(GlobalVariable.TEST_ID_COLUMN, Qt.SortOrder.AscendingOrder)
        QWidgetUtils.widget_change_color(widget=self, background_color="#3316C6")

    def plot_scrollbar(self):
        """
        :return:
        """
        QTimer.singleShot(50, self.plot_points)

    def plot_points(self):
        self.plot.clear()
        length = self.cpk_info_table.rowCount()
        self.plot.setYRange(0, length)
        x, y, z, cpk_l, top_fail_l, reject_l = [], [], [], [], [], []
        for index in range(length):
            cpk = float(self.cpk_info_table.item(index, GlobalVariable.CPK_COLUMN).text())
            top_fail = float(self.cpk_info_table.item(index, GlobalVariable.TOP_FAIL_COLUMN).text())
            reject = float(self.cpk_info_table.item(index, GlobalVariable.REJECT_COLUMN).text())
            if GlobalVariable.CPK_LO < cpk < GlobalVariable.CPK_HI:
                x.append(0)
                cpk_l.append(length - index)
                item = self.cpk_info_table.item(index, GlobalVariable.CPK_COLUMN)
                item.setBackground(QColor(250, 194, 5, 50))
            if top_fail > GlobalVariable.TOP_FAIL_LO:
                y.append(1)
                top_fail_l.append(length - index)
                item = self.cpk_info_table.item(index, GlobalVariable.TOP_FAIL_COLUMN)
                item.setBackground(QColor(217, 83, 25, 150))
            if reject > GlobalVariable.REJECT_LO:
                z.append(2)
                reject_l.append(length - index)
                item = self.cpk_info_table.item(index, GlobalVariable.REJECT_COLUMN)
                item.setBackground(QColor(217, 83, 25, 30))

        plot = pg.ScatterPlotItem(symbol='s', size=3, pen=None)
        plot.addPoints(x, cpk_l, pen=(250, 194, 5))
        plot.addPoints(y, top_fail_l, pen=(217, 83, 25))
        plot.addPoints(z, reject_l, pen=(217, 83, 25))
        self.plot.addItem(plot)
        self.cpk_info_table.resizeRowsToContents()

    @Slot(bool)
    def on_checkBox_clicked(self, e):
        if e:
            self.cpk_info_table.sortByColumn(GlobalVariable.TOP_FAIL_COLUMN, Qt.SortOrder.DescendingOrder)
        else:
            self.cpk_info_table.sortByColumn(GlobalVariable.TEST_ID_COLUMN, Qt.SortOrder.AscendingOrder)

    @Slot()
    def on_pushButton_pressed(self):
        new_limit = QTableUtils.get_all_new_limit(self.cpk_info_table)
        if not new_limit:
            return
        print(new_limit)
        if self.message_show("注意,Limit已经更新!!!,如果只看PASS请选择否!"):
            self.li.update_limit(new_limit, False)
        else:
            self.li.update_limit(new_limit, True)

    @Slot()
    def on_pushButton_2_pressed(self):
        new_limit = QTableUtils.get_select_new_limit(self.cpk_info_table)
        print(new_limit)
        if not new_limit:
            return
        print("删除选中项目Limit外的数据")

    @Slot()
    def on_pushButton_4_pressed(self):
        test_ids = QTableUtils.get_table_widget_test_id(self.cpk_info_table)
        if not test_ids:
            return
        print(test_ids)
        print("只对选中项目的数据进行分析")

    def cpk_table_row_hide(self, hide: bool):
        for i in range(self.cpk_info_table.rowCount()):
            self.cpk_info_table.setRowHidden(i, hide)

    @Slot()
    def on_lineEdit_returnPressed(self):
        """
        若可以查询到, 先隐藏所有行
        """
        regex = self.lineEdit.text()
        regex = "*{}*".format(regex)
        items = self.cpk_info_table.findItems(regex, Qt.MatchWildcard)
        if len(items) == 0:
            self.li.QStatusMessage.emit("无法根据筛选条件查询到匹配行@!显示所有行.")
            self.cpk_table_row_hide(False)
            return
        self.cpk_table_row_hide(True)
        for each in items:
            if each.column() not in {GlobalVariable.TEST_NUM_COLUMN, GlobalVariable.TEST_TXT_COLUMN}:
                continue
            self.cpk_info_table.setRowHidden(each.row(), False)

    def message_show(self, text: str) -> bool:
        res = QMessageBox.question(self, '待确认', text,
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.Yes)
        if res == QMessageBox.Yes:
            return True
        else:
            return False
