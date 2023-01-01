#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : trans_scatter.py
@Author  : Link
@Time    : 2022/6/4 11:00
@Mark    : 
"""

import math
from typing import Union, List

import numpy as np
import pandas as pd

from PySide2 import QtCore
from pyqtgraph import ScatterPlotItem, InfiniteLine

from chart_core.chart_pyqtgraph.core.mixin import BasePlot, GraphRangeSignal, MyPlotWidget
from chart_core.chart_pyqtgraph.core.view_box import CustomViewBox, pg
from common.li import Li
from ui_component.ui_app_variable import UiGlobalVariable


class TransScatterChart(QtCore.QObject, BasePlot):
    """
    散点图
        TODO: rota: 0b000000
            0bX_____ -> select x  选取后筛选X轴的数据
            0b_X____ -> select y  选取后筛选Y轴的数据
            0b__X___ -> lint x    H_L_Limit/AVG 放在X轴 -> 主要数据分布在X上
            0b___X__ -> lint y    H_L_Limit/AVG 放在Y轴 -> 主要数据分布在Y上
            0b____X_ -> zoom x    X轴放大缩小
            0b_____X -> zoom y    Y轴放大缩小
    """
    list_bins = None  # 用来提升性能
    scatter_list: list = None  # 用于缓存plot
    scatter_front_list: list = None  # 用于缓存plot
    scatter_size: int = 7
    brush_cache: dict = None

    def __init__(self, li: Li):
        super(TransScatterChart, self).__init__()
        self.li = li
        self.rota = 0b010101
        self.sig = 0 if self.rota & 0b1000 else 1
        self.vb = CustomViewBox()

        self.pw = MyPlotWidget(viewBox=self.vb, enableMenu=False)
        self.pw.closeSignal.connect(self.__del__)
        self.pw.hideButtons()
        self.pw.addLegend(colCount=4)

        self.bottom_axis = self.pw.getAxis("bottom")
        self.bottom_axis.setHeight(60)
        self.left_axis = self.pw.getAxis("left")
        self.left_axis.setWidth(60)

        # self.pw.setMouseEnabled(x=False)
        self.vb.select_signal.connect(self.select_range)
        self.li.QChartSelect.connect(self.set_front_chart)
        self.li.QChartRefresh.connect(self.set_front_chart)
        if UiGlobalVariable.GraphUseLocalColor:
            color = pg.colormap.get('./colors/CET-C6.csv')
        else:
            color = pg.colormap.get("CET-C6")
        self.c = color.getLookupTable(alpha=True)

        self.scatter_list = list()
        self.scatter_front_list = list()
        self.brush_cache = dict()

    def init_movable_line(self):
        v_line = InfiniteLine(angle=90, movable=False, label='x={value:0.0f}', labelOpts={'color': (0, 0, 0)})
        h_line = InfiniteLine(angle=0, movable=False, label='y={value:0.5f}', labelOpts={'color': (0, 0, 0)})
        self.vb.addItem(v_line, ignoreBounds=True)
        self.vb.addItem(h_line, ignoreBounds=True)

        def mouseMoved(evt):
            if self.vb.sceneBoundingRect().contains(evt):
                mouse_point = self.vb.mapSceneToView(evt)
                v_line.setPos(mouse_point.x())
                h_line.setPos(mouse_point.y())

        self.vb.scene().sigMouseMoved.connect(mouseMoved)

    def select_range(self, axs: Union[List[QtCore.QRectF], None]):
        if axs is None:
            self.li.set_chart_data(None)
            return
        chart_prr_list = []
        for ax in axs:
            part_id_min, part_id_max = ax.left(), ax.right()
            result_min, result_max = ax.top(), ax.bottom()
            temp = self.li.to_chart_csv_data.df
            chart_prr = temp[
                ((temp.index > part_id_min) & (temp.index < part_id_max)) & (
                        (temp[self.key] > result_min) & (temp[self.key] < result_max))
                ]
            chart_prr_list.append(chart_prr)

        self.li.set_chart_data(pd.concat(chart_prr_list))

    @GraphRangeSignal
    def set_df_chart(self):
        """

        :return:
        """
        if self.li.to_chart_csv_data.df is None:
            return
        if self.key not in self.li.capability_key_dict:
            return
        if len(self.li.df_module.prr_df) > 3E3:
            self.scatter_size = 5
        if UiGlobalVariable.GraphPlotScatterSimple:
            if not self.change:
                self.list_bins = 5
            else:
                self.list_bins = int(
                    abs(self.p_range.x_max - self.p_range.x_min) // UiGlobalVariable.GraphPlotScatterSimpleNum
                )
        try:
            self.pw.plotItem.legend.clear()
        except RuntimeError:
            pass
        for each in self.scatter_list:
            each.clear()
            each.hide()

        color_square_nm = math.ceil(pow(len(self.li.to_chart_csv_data.group_df), 0.5))
        color_split_nm = 512 / 2 ** color_square_nm
        color_list = self.c[::int(color_split_nm)]

        for index, (key, df) in enumerate(self.li.to_chart_csv_data.group_df.items()):
            if self.li.to_chart_csv_data.select_group is not None:
                if key not in self.li.to_chart_csv_data.select_group:
                    continue
            idx = int(index % color_split_nm)
            if UiGlobalVariable.GraphPlotScatterSimple:
                x = np.array(df.index)
                x = x[::self.list_bins + 1]
                result = df[self.key][::self.list_bins + 1]
            else:
                x = np.array(df.index)
                result = df[self.key]
            brush = list(color_list[idx])
            if self.li.to_chart_csv_data.chart_df is None:
                brush[3] = 255
                self.brush_cache[key] = brush
            else:
                brush[3] = 85
            if index >= len(self.scatter_list):
                plot = ScatterPlotItem(symbol='o', hoverable=False,
                                       size=self.scatter_size, pen=None, name=key, brush=tuple(brush))
                plot.addPoints(x, result)
                self.scatter_list.append(plot)
                self.pw.addItem(plot)
            else:
                plot = self.scatter_list[index]
                plot.setData(x, result, clear=True, brush=tuple(brush))  # x.to_numpy(), y.to_numpy()
                self.pw.plotItem.legend.addItem(plot, name=key)
                plot.show()

        if not self.change:
            self.vb.setYRange(self.p_range.y_min, self.p_range.y_max)
            self.change = True

        if not self.line_init:
            self.init_movable_line()
            self.line_init = True

    @GraphRangeSignal
    def set_front_chart(self):
        """
        不加入legend
        :return:
        """
        self.set_df_chart()
        for each in self.scatter_front_list:
            each.clear()
        if self.li.to_chart_csv_data.chart_df is None:
            return

        for index, (key, df) in enumerate(self.li.to_chart_csv_data.group_chart_df.items()):
            if self.li.to_chart_csv_data.select_group is not None:
                if key not in self.li.to_chart_csv_data.select_group:
                    continue
            if len(df) == 0:
                continue
            if UiGlobalVariable.GraphPlotScatterSimple:
                x = np.array(df.index)  # & 0XFFFFFF
                x = x[::self.list_bins + 1]
                result = df[self.key][::self.list_bins + 1]
            else:
                x = np.array(df.index)  # & 0XFFFFFF
                result = df[self.key]
            brush = self.brush_cache[key]
            if index >= len(self.scatter_front_list):
                plot = ScatterPlotItem(symbol='o', size=self.scatter_size, pen=None, brush=tuple(brush))
                plot.addPoints(x, result)
                self.scatter_front_list.append(plot)
                self.pw.addItem(plot)
            else:
                plot = self.scatter_front_list[index]
                plot.setData(x, result, clear=True, brush=tuple(brush))  # x.to_numpy(), y.to_numpy()
                plot.show()
