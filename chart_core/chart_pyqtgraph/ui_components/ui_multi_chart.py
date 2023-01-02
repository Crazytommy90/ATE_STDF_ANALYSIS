#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : ui_multi_chart.py
@Author  : Link
@Time    : 2023/1/2 12:32
@Mark    : 
"""
import datetime as dt

from typing import List

from PySide2 import QtGui
from PySide2.QtCore import Slot, Qt
from PySide2.QtWidgets import QMainWindow, QPushButton, QSpinBox, QWidget, QLayout

from chart_core.chart_pyqtgraph.core.mixin import ChartType
from chart_core.chart_pyqtgraph.ui_components.chart_trans_bar import TransBarChart
from chart_core.chart_pyqtgraph.ui_components.chart_trans_scatter import TransScatterChart
from chart_core.chart_pyqtgraph.ui_components.chart_visual_map import VisualMapChart
from chart_core.chart_pyqtgraph.ui_components.ui_unit_chart import UnitChartWindow
from chart_core.chart_pyqtgraph.ui_designer.ui_multi_chart import Ui_MainWindow, QGuiApplication, QCloseEvent
from common.li import Li
from ui_component.ui_app_variable import UiGlobalVariable


class MultiChartWindow(QMainWindow, Ui_MainWindow):
    temp: list = None

    def __init__(self, li: Li, parent=None, icon=None):
        super(MultiChartWindow, self).__init__(parent)
        self.li = li
        self.setupUi(self)
        self.setWindowTitle("Multi Chart Window")
        self.action_signal_binding.setChecked(Qt.Checked)

        # 添加缩小按钮
        self.pushButton = QPushButton("", self)
        self.pushButton.setShortcut("Ctrl+-")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pyqt/source/images/lc_zoomout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        # 添加放大按钮
        self.pushButton_2 = QPushButton("", self)
        self.pushButton_2.setShortcut("Ctrl++")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pyqt/source/images/lc_zoomin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)

        # 添加Width SpinBox
        self.unit_chart_width = QSpinBox(self)
        self.unit_chart_width.setMaximum(2000)
        self.unit_chart_width.setMinimum(500)
        self.unit_chart_width.setSingleStep(100)
        self.unit_chart_width.setPrefix("ChartWidth: ")

        # 添加Height SpinBox
        self.unit_chart_height = QSpinBox(self)
        self.unit_chart_height.setMaximum(2000)
        self.unit_chart_height.setMinimum(300)
        self.unit_chart_height.setSingleStep(100)
        self.unit_chart_height.setPrefix("ChartHeight: ")

        self.unit_chart_width.setValue(UiGlobalVariable.GraphPlotWidth)
        self.unit_chart_height.setValue(UiGlobalVariable.GraphPlotHeight)

        # 添加到状态栏
        self.toolBar.addWidget(self.unit_chart_width)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.unit_chart_height)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.pushButton)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.pushButton_2)
        self.toolBar.addSeparator()

        self.pushButton.pressed.connect(self._on_pushButton_pressed)
        self.pushButton_2.pressed.connect(self._on_pushButton_2_pressed)
        self.unit_chart_width.valueChanged.connect(self.resize_update)
        self.unit_chart_height.valueChanged.connect(self.resize_update)

    def set_width_height(self):
        self.unit_chart_width.setValue(UiGlobalVariable.GraphPlotWidth)
        self.unit_chart_height.setValue(UiGlobalVariable.GraphPlotHeight)

    @staticmethod
    def clearLayout(layout: QLayout):
        for i in range(layout.count()):
            layout.itemAt(i).widget().deleteLater()

    @Slot()
    def on_action_signal_binding_triggered(self):
        if self.action_signal_binding.isChecked():
            for each in self.temp:  # type:UnitChartWindow
                each.action_signal_binding.setChecked(Qt.Checked)
        else:
            for each in self.temp:  # type:UnitChartWindow
                each.action_signal_binding.setChecked(Qt.Unchecked)

    @Slot()
    def _on_pushButton_pressed(self):
        self.unit_chart_width.setValue(
            self.unit_chart_width.value() - 100
        )
        self.unit_chart_height.setValue(
            self.unit_chart_height.value() - 50
        )

    @Slot()
    def _on_pushButton_2_pressed(self):
        self.unit_chart_width.setValue(
            self.unit_chart_width.value() + 100
        )
        self.unit_chart_height.setValue(
            self.unit_chart_height.value() + 50
        )

    def resize_update(self):
        self.widget.setFixedSize(
            self.unit_chart_width.value(), len(self.temp) * self.unit_chart_height.value()
        )
        for each in self.temp:  # type:UnitChartWindow
            each.set_resize_update(self.unit_chart_width.value(), self.unit_chart_height.value())

    def clear(self):
        if self.temp is None:
            self.temp = list()
        else:
            self.temp.clear()
        self.clearLayout(self.verticalLayout_3)
        # self.widget.resize(
        #     self.unit_chart_width, self.unit_chart_height
        # )

    def set_data(self, test_id_list: List[int], chart_type: ChartType):
        if not test_id_list:
            return
        self.clear()

        for test_id in test_id_list:
            plot = None
            if chart_type == ChartType.TransBar:
                bar_chart = TransBarChart(self.li)
                bar_chart.set_data(test_id)  # TEST_ID == 1
                bar_chart.set_range_self()
                bar_chart.set_df_chart()
                bar_chart.set_line_self()
                self.verticalLayout_3.addWidget(bar_chart)
                plot = bar_chart
            if chart_type == ChartType.TransScatter:
                scatter_chart = TransScatterChart(self.li)
                scatter_chart.set_data(test_id)  # TEST_ID == 1
                scatter_chart.set_range_self()
                scatter_chart.set_df_chart()
                scatter_chart.set_line_self()
                self.verticalLayout_3.addWidget(scatter_chart)
                plot = scatter_chart
            if chart_type == ChartType.VisualMap:
                visual_map_chart = VisualMapChart(self.li)
                visual_map_chart.set_data(test_id)
                visual_map_chart.set_front_chart()
                self.verticalLayout_3.addWidget(visual_map_chart)
                plot = visual_map_chart

            if plot is None:
                return
            self.temp.append(plot)
        self.resize_update()

    @Slot()
    def on_action_copy_image_triggered(self):
        try:
            pixmap = QWidget.grab(self.widget)
            QGuiApplication.clipboard().setPixmap(pixmap)
            self.mdi_space_message_emit("SUCCESS: 已将Image复制到剪贴板@" + dt.datetime.now().strftime("%H:%M:%S"))
        except Exception as err:
            self.mdi_space_message_emit(repr(err))

    @Slot(str)
    def mdi_space_message_emit(self, message: str):
        """
        append message
        :param message:
        :return:
        """
        self.statusbar.showMessage("==={}==={}===".format(dt.datetime.now().strftime("%H:%M:%S"), message))

    def closeEvent(self, event: QCloseEvent) -> None:
        self.clear()
        self.li = None
        super(MultiChartWindow, self).closeEvent(event)
