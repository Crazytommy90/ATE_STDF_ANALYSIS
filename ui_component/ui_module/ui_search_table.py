"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/12/22 18:48
@Site    : 
@File    : ui_search_table.py
@Software: PyCharm
@Remark  : 实现在表头做搜索
"""
from typing import List

from PySide2.QtGui import QColor, Qt
from PySide2.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QScrollBar

import pyqtgraph as pg

from ui_component.ui_module.ui_designer.ui_search_table import Ui_Form as SearchForm

pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

"""
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalScrollBar = QScrollBar(Form)
        self.verticalScrollBar.setObjectName(u"verticalScrollBar")
        self.verticalScrollBar.setOrientation(Qt.Vertical)

        self.horizontalLayout.addWidget(self.verticalScrollBar)

"""

class SearchTable(QWidget, SearchForm):
    def __init__(self, parent=None):
        super(SearchTable, self).__init__(parent)
        self.setupUi(self)
        self.gw = pg.GraphicsLayoutWidget()
        self.gw.ci.setContentsMargins(0, 0, 0, 0)
        self.plot = self.gw.addPlot()
        self.horizontalLayout.addWidget(self.gw)

        plot_layout = QHBoxLayout(self.gw)
        plot_layout.setContentsMargins(0, 0, 0, 0)

        self.init_plot()
        self.init_signal()

    def init_plot(self):
        self.gw.setMaximumWidth(20)
        self.plot.setMouseEnabled(x=False, y=False)
        self.plot.setYRange(0, 0)
        self.plot.setXRange(0, 3)
        self.plot.showAxis('bottom', False)
        self.plot.showAxis('left', False)
        self.plot.hideButtons()

        x = self.plot.getAxis("left")
        x.setWidth(0)

    def init_signal(self):
        self.titleTable.itemChanged.disconnect(self.titleTable.handleItemChanged)
        self.titleTable.cellChanged.connect(self.title_change)
        title_header: QHeaderView = self.titleTable.horizontalHeader()
        title_header.sectionResized.connect(self.title_to_data_table_size)
        title_header.sortIndicatorChanged.connect(self.dataTable.sortItems)
        # title_header.sortIndicatorChanged.connect(lambda x: print(x))

    def pre_data_signal(self):
        self.titleTable.horizontalHeader().sectionResized.disconnect(self.title_to_data_table_size)
        self.dataTable.horizontalHeader().sectionResized.connect(self.data_to_title_table_size)
        self.titleTable.cellChanged.disconnect(self.title_change)

    def post_data_signal(self):
        self.dataTable.horizontalHeader().sectionResized.disconnect(self.data_to_title_table_size)
        self.titleTable.horizontalHeader().sectionResized.connect(self.title_to_data_table_size)
        self.titleTable.cellChanged.connect(self.title_change)

    def title_to_data_table_size(self, index, old_size, new_size):
        self.dataTable.horizontalHeader().resizeSection(index, new_size)

    def data_to_title_table_size(self, index, old_size, new_size):
        self.titleTable.horizontalHeader().resizeSection(index, new_size)

    def title_change(self, row, column):
        text = self.titleTable.item(row, column).text()
        print(text)

    def set_data(self, data: List[dict]):
        if not data:
            print("No Data")
            return
        self.pre_data_signal()
        self.dataTable.clear()
        self.titleTable.clear()
        table_head = data[0].keys()
        self.titleTable.setColumnCount(len(table_head))
        self.titleTable.setHorizontalHeaderLabels(table_head)

        self.titleTable.setRowCount(1)
        " titleTable放入一行搜索行 "
        for column in range(len(table_head)):
            item = QTableWidgetItem()
            item.setBackground(QColor("#BEE7E9"))
            self.titleTable.setItem(0, column, item)
        self.dataTable.setData(data)
        self.post_data_signal()


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication

    test_data = [{"A:": 1, "B": 2}, {"A:": 3, "B": 1}, {"A:": 2, "B": 3},
                 {"A:": 1, "B": 2}, {"A:": 3, "B": 1}, {"A:": 2, "B": 3},
                 {"A:": 1, "B": 2}, {"A:": 3, "B": 1}, {"A:": 2, "B": 3},
                 {"A:": 1, "B": 2}, {"A:": 3, "B": 1}, {"A:": 2, "B": 3},
                 {"A:": 1, "B": 2}, {"A:": 3, "B": 1}, {"A:": 2, "B": 3},
                 {"A:": 1, "B": 2}, {"A:": 3, "B": 1}, {"A:": 2, "B": 3},
                 {"A:": 1, "B": 2}, {"A:": 3, "B": 1}, {"A:": 2, "B": 3}, ]
    app = QApplication(sys.argv)
    win = SearchTable()
    win.set_data(test_data)
    win.show()
    sys.exit(app.exec_())
