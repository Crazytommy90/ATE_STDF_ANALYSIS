#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : app.py
@Author  : Link
@Time    : 2022/12/16 21:24
@Mark    :
@Version : V3.0
@START_T : 20220814
@RELEASE :
"""

import sys

from PySide2.QtCore import Signal, QObject
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QApplication

from ui_component.ui_main.ui_main import Application, Main_Ui

import warnings

warnings.filterwarnings("ignore")


class Stream(QObject):
    conn = True
    newText = Signal(str)

    def write(self, text):
        if not self.conn:
            return
        self.newText.emit(str(text))
        # 实时刷新界面
        QApplication.processEvents()


class main_ui(Main_Ui):

    def __init__(self, parent=None, license_control=False):
        super(main_ui, self).__init__(parent=parent, license_control=license_control)
        self.setWindowTitle("STDF Data Analysis System")
        self.sd = Stream()
        self.se = Stream()
        self.sd.newText.connect(self.outputWritten)
        self.se.newText.connect(self.outputWritten)
        sys.stdout = self.sd
        sys.stderr = self.se

    def outputWritten(self, text: str):
        """
        根据规则来打印合适颜色的信息
        :param text:
        :return:
        """
        self.text_browser.split_append(text)

    def closeEvent(self, a0: QCloseEvent) -> None:
        sys.stdout.conn = False
        sys.stderr.conn = False
        sys.exit(0)


if __name__ == '__main__':
    """
    开源版
    """
    import multiprocessing
    from ui_component.ui_app_variable import UiGlobalVariable

    UiGlobalVariable.GraphUseLocalColor = True
    multiprocessing.freeze_support()
    app = Application(sys.argv)
    app.setApplicationName("IC DATA ANALYSIS")
    try:
        win = main_ui(license_control=False)
        app.setWindowIcon(win.icon)
        win.show()
        sys.exit(app.exec_())
    except Exception as err:
        sys.stdout = None
        print(err)
    finally:
        print('Program is dead.')
