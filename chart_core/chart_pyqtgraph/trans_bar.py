"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/5/12 13:53
@Software: PyCharm
@File    : trans_bar.py
@Remark  : 
"""

import math
from typing import List, Union, Tuple, Any

import numpy as np
import pandas as pd
from PySide2 import QtCore
from pyqtgraph import InfiniteLine, BarGraphItem

from app_test.test_utils.wrapper_utils import Time
from chart_core.chart_pyqtgraph.core.mixin import BasePlot, GraphRangeSignal, MyPlotWidget
from chart_core.chart_pyqtgraph.core.view_box import CustomViewBox
from common.li import Li
from ui_component.ui_app_variable import UiGlobalVariable


class TransBarChart(QtCore.QObject, BasePlot):
    """
    横向柱状图, 用新的数据类型后, 运行时间长的有点过分了/(ㄒoㄒ)/~~
        TODO: rota: 0b000000
            0bX_____ -> select x  选取后筛选X轴的数据
            0b_X____ -> select y  选取后筛选Y轴的数据
            0b__X___ -> lint x    H_L_Limit/AVG 放在X轴 -> 主要数据分布在X上
            0b___X__ -> lint y    H_L_Limit/AVG 放在Y轴 -> 主要数据分布在Y上
            0b____X_ -> zoom x    X轴放大缩小
            0b_____X -> zoom y    Y轴放大缩小
    """

    bar_width: float = 0  # 这个是柱状图的当前宽度
    ticks: list = None  # X轴
    list_bins: Union[Tuple[np.ndarray, Any], np.ndarray] = None
    chart_v_lines: List[InfiniteLine] = None

    def __init__(self, li: Li):
        super(TransBarChart, self).__init__()
        self.li = li
        self.rota = 0b010101
        self.sig = 0 if self.rota & 0b1000 else 1

        self.vb = CustomViewBox()
        self.pw = MyPlotWidget(viewBox=self.vb, enableMenu=False)
        self.pw.closeSignal.connect(self.__del__)
        self.pw.hideButtons()

        self.bg1 = BarGraphItem(x0=[], y=[], y0=[], y1=[], width=[])
        self.bg2 = BarGraphItem(x0=[], y=[], y0=[], y1=[], width=[])

        self.pw.addItem(self.bg1)
        self.pw.addItem(self.bg2)

        self.bottom_axis = self.pw.getAxis("bottom")
        self.bottom_axis.setHeight(60)
        self.left_axis = self.pw.getAxis("left")
        self.left_axis.setWidth(60)

        self.pw.setMouseEnabled(x=False)
        self.vb.select_signal.connect(self.select_range)
        self.li.QChartSelect.connect(self.set_front_chart)
        self.li.QChartRefresh.connect(self.set_front_chart)

        self.chart_v_lines = []

    def init_movable_line(self):
        h_line = InfiniteLine(angle=0, movable=False, label='y={value:0.5f}', labelOpts={'color': (0, 0, 0)})
        self.vb.addItem(h_line, ignoreBounds=True)

        def mouseMoved(evt):
            if self.vb.sceneBoundingRect().contains(evt):
                mouse_point = self.vb.mapSceneToView(evt)
                h_line.setPos(mouse_point.y())

        self.vb.scene().sigMouseMoved.connect(mouseMoved)

    def select_range(self, axs: Union[List[QtCore.QRectF], None]):
        """
        区间选取后触发,更新chart_df
        :return:
        """
        if axs is None:
            """
            show all front
            """
            self.li.set_chart_data(None)
            return
        chart_prr_list = []
        for ax in axs:
            """
            1. 选取X轴
            2. 选取Y轴
            """
            select_start = math.ceil(ax.left() / self.bar_width)
            select_stop = math.ceil(ax.right() / self.bar_width)
            if select_start > len(self.ticks) or select_stop < 0:
                continue

            keys = []
            for i in range(select_start - 1, select_stop):
                if i < 0:
                    continue
                if i == len(self.ticks):
                    break
                key = self.ticks[i]
                keys.append(key)
            for key in keys:
                temp = self.li.to_chart_csv_data.group_df[key]
                if len(temp) == 0:
                    continue
                result_min, result_max = ax.top(), ax.bottom()
                chart_prr = temp[
                    (temp[self.key] > result_min) & (temp[self.key] < result_max)
                    ]
                chart_prr_list.append(chart_prr)

        self.li.set_chart_data(pd.concat(chart_prr_list))

    def set_range_data_to_chart(self, a, ax) -> bool:
        res = super(TransBarChart, self).set_range_data_to_chart(a, ax)
        if res:
            self.set_front_chart()
        return res

    @Time()
    @GraphRangeSignal
    def set_df_chart(self):
        """
        即使某个Group内没有数据, 也要给留出位置
        :return:
        """
        if self.li.to_chart_csv_data.df is None:
            return
        if self.key not in self.li.capability_key_dict:
            return
        for v_line in self.chart_v_lines:
            self.vb.removeItem(v_line)
        self.chart_v_lines.clear()

        self.list_bins = np.linspace(self.p_range.y_min, self.p_range.y_max, UiGlobalVariable.GraphBins)
        columns, x0, y0, y1, y, width, self.bar_width = [], [], [], [], [], [], 0
        chart_v_lines_x_list = []  # 用于在柱状图的底部用一条竖线分割开

        for index, (key, df) in enumerate(self.li.to_chart_csv_data.group_df.items()):
            columns.append(key)
            if self.li.to_chart_csv_data.select_group is not None:
                if key not in self.li.to_chart_csv_data.select_group:
                    continue
            if len(df) == 0:
                # TODO: 注意, 没有数据的地方也要留有位置来可视化
                continue
            temp_dis = df[self.key].value_counts(bins=self.list_bins, sort=False)
            if len(temp_dis) == 0:
                continue
            self.bar_width = max(temp_dis) if max(temp_dis) > self.bar_width else self.bar_width
            chart_v_lines_x_list.append(index + 0.2)
            for bin_index, value in enumerate(temp_dis.values):
                x0.append(index + 0.2)
                y0.append(self.list_bins[bin_index])
                y1.append(self.list_bins[bin_index + 1])
                y.append((self.list_bins[bin_index + 1] + self.list_bins[bin_index]) / 2)
                width.append(value)

        x0 = np.array(x0) * self.bar_width
        if self.li.to_chart_csv_data.chart_df is None:
            brush = (217, 83, 25, 255)
        else:
            brush = (217, 83, 25, 95)
        self.bg1.setOpts(x0=x0, y=y, y0=y0, y1=y1, width=width, brush=brush)
        self.ticks = columns
        ticks = [((idx + 0.2) * self.bar_width, label.replace("|", "\r\n").replace("@", "\r\n"))
                 for idx, label in enumerate(self.ticks)]
        self.bottom_axis.setTicks((ticks, []))
        for v_line_x_data in chart_v_lines_x_list:
            v_line = InfiniteLine(angle=90, movable=False)
            self.vb.addItem(v_line, ignoreBounds=True)
            v_line.setPos(v_line_x_data * self.bar_width)
            self.chart_v_lines.append(v_line)
        if not self.change:
            self.vb.setYRange(self.p_range.y_min, self.p_range.y_max)
            self.change = True

    @Time()
    def set_front_chart(self):
        self.bg2.setOpts(x0=[], y=[], y0=[], y1=[], width=[])
        self.set_df_chart()
        if self.li.to_chart_csv_data.chart_df is None:
            return
        if self.list_bins is None:
            return
        x0, y0, y1, y, width = [], [], [], [], []
        for key, df in self.li.to_chart_csv_data.group_chart_df.items():
            if self.li.to_chart_csv_data.select_group is not None:
                if key not in self.li.to_chart_csv_data.select_group:
                    continue
            if len(df) == 0:
                # TODO: 注意, 没有数据的地方也要留有位置来可视化
                continue
            temp_dis = df[self.key].value_counts(bins=self.list_bins, sort=False)
            if len(temp_dis) == 0:
                continue
            for bin_index, value in enumerate(temp_dis.values):
                x0.append(self.ticks.index(key) + 0.2)
                y0.append(self.list_bins[bin_index])
                y1.append(self.list_bins[bin_index + 1])
                y.append((self.list_bins[bin_index + 1] + self.list_bins[bin_index]) / 2)
                width.append(value)
        x0 = np.array(x0) * self.bar_width
        self.bg2.setOpts(x0=x0, y=y, y0=y0, y1=y1, width=width, brush=(217, 83, 25, 255))
