#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : chart_visual_map.py
@Author  : Link
@Time    : 2022/6/5 10:31
@Mark    : 
"""
import math

from PySide2 import QtWidgets
from PySide2.QtGui import QResizeEvent, QCloseEvent
from PySide2.QtWidgets import QWidget
from pyqtgraph import GraphicsLayoutWidget, ImageItem, ColorBarItem, colormap, HistogramLUTItem, InfiniteLine

import numpy as np

from chart_core.chart_pyqtgraph.core.visual.visual import *

from chart_core.chart_pyqtgraph.ui_components.ui_unit_chart import UnitChartWindow
from common.li import Li
from ui_component.ui_app_variable import UiGlobalVariable


class VisualMapChart(UnitChartWindow):
    """
    不加入limit, 最小单元是GROUP, 不通过SITE去分组
    """
    key: int = None  # 显示的测试项目
    li: Li = None
    x_min: int = 0
    y_min: int = 0
    x_max: int = 0
    y_max: int = 0
    bottom_ticks: list = None
    left_ticks: list = None

    def __init__(self, li: Li):
        super(VisualMapChart, self).__init__()
        self.li = li

        self.widGet = QWidget()
        self.pw = GraphicsLayoutWidget()
        self.gridLayout = QtWidgets.QVBoxLayout(self.widGet)
        self.label = QtWidgets.QLabel()
        font = self.label.font()
        font.setPointSize(15)
        self.label.setFont(font)
        self.gridLayout.addWidget(self.label)
        self.gridLayout.addWidget(self.pw)
        self.setCentralWidget(self.widGet)
        if UiGlobalVariable.GraphUseLocalColor:
            color = colormap.get('./colors/CET-D8.csv')
        else:
            color = colormap.get("CET-D8")
        self.c = color
        self.li.QChartSelect.connect(self.li_chart_signal)
        self.li.QChartRefresh.connect(self.li_chart_signal)

    def li_chart_signal(self):
        if self.action_signal_binding.isChecked():
            self.set_front_chart()

    def set_data(self, key: int):
        """
        :param key: TEST_ID
        :return:
        """
        if self.li is None:
            raise Exception("first set li")
        row = self.li.capability_key_dict.get(key, None)
        if row is None:
            return
        self.key = key
        title = str(row["TEST_NUM"]) + ":" + row["TEST_TXT"]
        self.set_title(title)
        self.label.setText(title)
        self.init_coord()

    def pw_show(self):
        self.show()

    def set_title(self, title: str = "PlotItem with CustomAxisItem, CustomViewBox"):
        self.setWindowTitle(title)

    def init_coord(self):
        self.x_min, self.y_min = self.li.to_chart_csv_data.df.X_COORD.min(), self.li.to_chart_csv_data.df.Y_COORD.min()
        self.x_max, self.y_max = self.li.to_chart_csv_data.df.X_COORD.max(), self.li.to_chart_csv_data.df.Y_COORD.max()

    def set_front_chart(self):
        if self.key not in self.li.capability_key_dict:
            return
        if self.li.to_chart_csv_data.chart_df is None:
            data_df = self.li.to_chart_csv_data.df
        else:
            data_df = self.li.to_chart_csv_data.chart_df
        if data_df is None:
            return
        map_group = data_df.groupby("GROUP")
        x, y = self.x_max - self.x_min + 1, self.y_max - self.y_min + 1
        self.pw.clear()
        if len(map_group) > 25:
            print("选取的Mapping数据过多了")
            return
        row = math.ceil(math.sqrt(len(map_group)))
        items = []
        _min, _max = data_df[self.key].min(), data_df[self.key].max()
        diff = _max - _min
        if diff <= 0:
            self.label.setText("无有效数据")
            return
        rounding = diff / 1E9
        for index, (key, df) in enumerate(map_group):
            data = np.full([x, y], np.nan)
            coord_to_np(
                df.X_COORD.to_numpy() - self.x_min,
                df.Y_COORD.to_numpy() - self.y_min,
                df[self.key].to_numpy(),
                data
            )
            t_row, t_col = divmod(index, row)
            im = ImageItem(image=data)

            items.append(im)
            plot_item = self.pw.addPlot(t_row, t_col, 1, 1, title=key)

            plot_item.getViewBox().invertY(True)
            plot_item.addItem(im)
            plot_item.setMouseEnabled(x=False, y=False)
        bar = ColorBarItem(
            values=(data_df[self.key].quantile(0.05), data_df[self.key].quantile(0.95)),
            limits=(_min, _max),  # start with full range...
            rounding=rounding,
            width=10,
            colorMap=self.c)
        bar.setImageItem(items)
        # manually adjust reserved space at top and bottom to align with plot
        bar.getAxis('bottom').setHeight(21)
        bar.getAxis('top').setHeight(31)
        self.pw.addItem(bar, 0, row + 1, 2, 1)  # large bar spanning both rows
        # isoLine = InfiniteLine(angle=0, movable=True, pen='g')
        # bar.vb.addItem(isoLine)
        # bar.vb.setMouseEnabled(y=False)  # makes user interaction a little easier
        # isoLine.setValue(0.0022)

    def __del__(self):
        try:
            self.li.QChartSelect.disconnect(self.set_front_chart)
        except RuntimeError:
            pass
        try:
            self.li.QChartRefresh.disconnect(self.set_front_chart)
        except RuntimeError:
            pass

    def closeEvent(self, event: QCloseEvent) -> None:
        self.__del__()
        super(VisualMapChart, self).closeEvent(event)
