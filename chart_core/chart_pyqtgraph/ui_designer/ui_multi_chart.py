# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'multi_chart.ui'
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
        MainWindow.resize(1176, 571)
        self.action_signal_binding = QAction(MainWindow)
        self.action_signal_binding.setObjectName(u"action_signal_binding")
        self.action_signal_binding.setCheckable(True)
        icon = QIcon()
        icon.addFile(u":/pyqt/source/images/lc_lineendstyle.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_signal_binding.setIcon(icon)
        self.action_copy_image = QAction(MainWindow)
        self.action_copy_image.setObjectName(u"action_copy_image")
        icon1 = QIcon()
        icon1.addFile(u":/pyqt/source/images/Copy.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_copy_image.setIcon(icon1)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1156, 495))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.scrollAreaWidgetContents)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")

        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addWidget(self.widget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.action_signal_binding)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_copy_image)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_signal_binding.setText(QCoreApplication.translate("MainWindow", u"signal_binding", None))
#if QT_CONFIG(tooltip)
        self.action_signal_binding.setToolTip(QCoreApplication.translate("MainWindow", u"\u64cd\u4f5c\u4fe1\u53f7\u7684\u7ed1\u5b9a", None))
#endif // QT_CONFIG(tooltip)
        self.action_copy_image.setText(QCoreApplication.translate("MainWindow", u"copy_image", None))
#if QT_CONFIG(tooltip)
        self.action_copy_image.setToolTip(QCoreApplication.translate("MainWindow", u"\u5c06\u56fe\u50cf\u590d\u5236\u5230\u526a\u8d34\u677f\u4e0a", None))
#endif // QT_CONFIG(tooltip)
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

