#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : poll.py
@Author  : Link
@Time    : 2022/6/4 14:40
@Mark    : 
"""
import datetime as dt
from typing import List

from PySide2 import QtGui
from PySide2.QtCore import Qt
from PySide2.QtGui import QGuiApplication, QCloseEvent, QResizeEvent, QKeyEvent
from PySide2.QtWidgets import QWidget, QLayout, QMainWindow
from pyqtgraph.dockarea import DockArea, Dock

from pyqtgraph.graphicsItems.ViewBox import axisCtrlTemplate_pyside2
from pyqtgraph.graphicsItems.PlotItem import plotConfigTemplate_pyside2
from pyqtgraph.imageview import ImageViewTemplate_pyside2

from chart_core.chart_pyqtgraph.gui.line_chart import Ui_Form
from chart_core.chart_pyqtgraph.gui.ui_chart_window import Ui_MainWindow
from chart_core.chart_pyqtgraph.trans_bar import TransBarChart
from chart_core.chart_pyqtgraph.trans_scatter import TransScatterChart
from chart_core.chart_pyqtgraph.visual_map import VisualMapChart
from common.li import Li
from ui_component.ui_app_variable import UiGlobalVariable, QtPlotAllUse


def clearLayout(layout: QLayout):
    for i in range(layout.count()):
        layout.itemAt(i).widget().deleteLater()


class ChartsUi(QWidget, Ui_Form):
    temp: list = None

    def __init__(self, li: Li, parent=None):
        super(ChartsUi, self).__init__(parent)
        self.li = li
        self.setupUi(self)
        self.setWindowTitle("绘图区")
        self.pushButton.pressed.connect(self.save_widget_pix)
        self.c_type = None
        self.scale = 1.0
        self.child_max_width = 1000

    def set_data(self, test_id_list: List[int], c_type: str):
        if not test_id_list:
            return
        self.temp = list()
        length = len(test_id_list)
        self.c_type = c_type
        if self.c_type == 'visual_map':
            self.widget.setFixedHeight(length * UiGlobalVariable.GraphPlotHeight * 0.93)
        else:
            self.widget.setFixedHeight(length * UiGlobalVariable.GraphPlotHeight)
        self.scale = UiGlobalVariable.GraphPlotHeight / UiGlobalVariable.GraphPlotWidth
        self.child_max_width = UiGlobalVariable.GraphPlotWidth

        for test_id in test_id_list:
            plot = None
            if self.c_type == 'trans_bar':
                bar_chart = TransBarChart(self.li)
                bar_chart.set_data(test_id)  # TEST_ID == 1
                bar_chart.set_range_self()
                bar_chart.set_df_chart()
                bar_chart.set_line_self()
                self.verticalLayout.addWidget(bar_chart.widget(UiGlobalVariable.GraphPlotWidth))
                plot = bar_chart
            if self.c_type == 'scatter':
                scatter_chart = TransScatterChart(self.li)
                scatter_chart.set_data(test_id)  # TEST_ID == 1
                scatter_chart.set_range_self()
                scatter_chart.set_df_chart()
                scatter_chart.set_line_self()
                self.verticalLayout.addWidget(scatter_chart.widget(UiGlobalVariable.GraphPlotWidth))
                plot = scatter_chart
            if self.c_type == 'visual_map':
                visual_map_chart = VisualMapChart(self.li)
                visual_map_chart.set_data(test_id)
                visual_map_chart.set_front_chart()
                self.verticalLayout.addWidget(visual_map_chart)
                plot = visual_map_chart

            if plot is None:
                return

            self.temp.append(plot)

    def resize_update(self, width):
        if self.c_type == "visual_map":
            height = width * 0.93
        else:
            height = width * self.scale
        for each in self.temp:  # type:QWidget
            each.resize(width, height)
        self.widget.setFixedHeight(height * len(self.temp))

    def clear(self):
        if self.temp is None:
            return
        self.temp.clear()
        clearLayout(self.verticalLayout)

    def save_widget_pix(self):
        try:
            pixmap = QWidget.grab(self.widget)
            QGuiApplication.clipboard().setPixmap(pixmap)
            # filename = QFileDialog.getSaveFileName(self, caption='保存成图片', filter='png(*.png);;jpg(*.jpg)')
            # save_file = filename[0]
            # pixmap.save(save_file)
            self.setWindowTitle("已将Image复制到剪贴板@" + dt.datetime.now().strftime("%H:%M:%S"))
        except Exception as err:
            self.setWindowTitle(repr(err))

    def closeEvent(self, event: QCloseEvent) -> None:
        self.clear()
        super(ChartsUi, self).closeEvent(event)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        if self.temp is None:
            pass
        else:
            width = a0.size().width()
            if self.c_type == "visual_map":
                self.resize_update(width)
            elif width < self.child_max_width:
                self.resize_update(width)
        super(ChartsUi, self).resizeEvent(a0)


class HideDock(Dock):

    def close(self):
        self.hide()


class ChartDockWindow(QMainWindow, Ui_MainWindow):
    """
    停靠ChartsUi
    TODO:
        1. 一个MDI只有一个ChartDockWindow
        2. 提前规划好
    """

    def __init__(self, li: Li, parent=None, icon=None, space_nm=1):
        super(ChartDockWindow, self).__init__(parent)
        self.setupUi(self)
        self.li = li
        self.parent = parent
        self.space_nm = space_nm
        if icon is not None:
            self.setWindowIcon(icon)
        self.title = "载入空间: {} -> Chart Widget".format(space_nm)
        self.setWindowTitle(self.title)
        self.area = DockArea()
        self.setCentralWidget(self.area)

        """ 暂时先定义四个位置, 来容纳四种图形, 反正这个是不常用的 """

        self.qt_distribution = ChartsUi(self.li, self)
        self.dock_qt_distribution = HideDock("横向分布图", size=(250, 400), closable=True)
        self.dock_qt_distribution.addWidget(self.qt_distribution)
        self.area.addDock(self.dock_qt_distribution)

        self.qt_visual_map = ChartsUi(self.li, self)
        self.dock_qt_visual_map = HideDock("参数性Map", size=(300, 400), closable=True)
        self.dock_qt_visual_map.addWidget(self.qt_visual_map)
        self.area.addDock(self.dock_qt_visual_map, "right", self.dock_qt_distribution)

        self.qt_scatter = ChartsUi(self.li, self)
        self.dock_qt_scatter = HideDock("散点图", size=(250, 400), closable=True)
        self.dock_qt_scatter.addWidget(self.qt_scatter)
        self.area.addDock(self.dock_qt_scatter, "right", self.dock_qt_distribution)

        self.dock_qt_distribution.hide()
        self.dock_qt_visual_map.hide()
        self.dock_qt_scatter.hide()

    def clear(self):
        self.parent = None
        self.qt_distribution.clear()
        self.qt_visual_map.clear()
        self.qt_scatter.clear()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Control:
            QtPlotAllUse.MultiSelect = True
        super(ChartDockWindow, self).keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Control:
            QtPlotAllUse.MultiSelect = False
        super(ChartDockWindow, self).keyReleaseEvent(event)