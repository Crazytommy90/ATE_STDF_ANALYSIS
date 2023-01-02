#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : ui_unit_chart.py
@Author  : Link
@Time    : 2023/1/2 12:32
@Mark    : 
"""
import datetime as dt

from PySide2 import QtGui
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QGuiApplication, QKeyEvent
from PySide2.QtWidgets import QMainWindow, QWidget, QPushButton, QSpinBox

from chart_core.chart_pyqtgraph.ui_designer.ui_unit_chart import Ui_MainWindow
from ui_component.ui_app_variable import UiGlobalVariable, QtPlotAllUse


class UnitChartWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(UnitChartWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Unit Chart Window")
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

    def set_resize_update(self, width, height):
        self.unit_chart_width.setValue(width)
        self.unit_chart_height.setValue(height)
        self.resize_update()

    def resize_update(self):
        self.resize(self.unit_chart_width.value(), self.unit_chart_height.value())

    @Slot()
    def on_action_copy_image_triggered(self):
        try:
            pixmap = QWidget.grab(self.centralWidget())
            QGuiApplication.clipboard().setPixmap(pixmap)
            # filename = QFileDialog.getSaveFileName(self, caption='保存成图片', filter='png(*.png);;jpg(*.jpg)')
            # save_file = filename[0]
            # pixmap.save(save_file)
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

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Control:
            QtPlotAllUse.MultiSelect = True
        super(UnitChartWindow, self).keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Control:
            QtPlotAllUse.MultiSelect = False
        super(UnitChartWindow, self).keyReleaseEvent(event)
