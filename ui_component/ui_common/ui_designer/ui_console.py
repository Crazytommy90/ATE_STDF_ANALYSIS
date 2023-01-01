# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'console.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import pyqtsource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1006, 540)
        self.action_select_run = QAction(MainWindow)
        self.action_select_run.setObjectName(u"action_select_run")
        icon = QIcon()
        icon.addFile(u":/pyqt/source/images/NavOverFlow_Start.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_select_run.setIcon(icon)
        self.action_run_all = QAction(MainWindow)
        self.action_run_all.setObjectName(u"action_run_all")
        icon1 = QIcon()
        icon1.addFile(u":/pyqt/source/images/icon_video.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_run_all.setIcon(icon1)
        self.action_refresh = QAction(MainWindow)
        self.action_refresh.setObjectName(u"action_refresh")
        icon2 = QIcon()
        icon2.addFile(u":/pyqt/source/images/lc_convertinto3d.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_refresh.setIcon(icon2)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.RightToolBarArea, self.toolBar)

        self.toolBar.addAction(self.action_select_run)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_run_all)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_refresh)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_select_run.setText(QCoreApplication.translate("MainWindow", u"select_run", None))
        self.action_run_all.setText(QCoreApplication.translate("MainWindow", u"run_all", None))
        self.action_refresh.setText(QCoreApplication.translate("MainWindow", u"refresh", None))
#if QT_CONFIG(tooltip)
        self.action_refresh.setToolTip(QCoreApplication.translate("MainWindow", u"\u5237\u65b0\u6570\u636e", None))
#endif // QT_CONFIG(tooltip)
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

