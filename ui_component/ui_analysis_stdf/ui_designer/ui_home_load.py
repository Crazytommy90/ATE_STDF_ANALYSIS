# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home_load.ui'
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
        MainWindow.resize(1154, 663)
        self.action_capability = QAction(MainWindow)
        self.action_capability.setObjectName(u"action_capability")
        icon = QIcon()
        icon.addFile(u":/pyqt/source/images/entirecolumn.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_capability.setIcon(icon)
        self.action_sava_data = QAction(MainWindow)
        self.action_sava_data.setObjectName(u"action_sava_data")
        icon1 = QIcon()
        icon1.addFile(u":/pyqt/source/images/Save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_sava_data.setIcon(icon1)
        self.action_dock_structure = QAction(MainWindow)
        self.action_dock_structure.setObjectName(u"action_dock_structure")
        icon2 = QIcon()
        icon2.addFile(u":/pyqt/source/images/graphicfilterpopart.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_dock_structure.setIcon(icon2)
        self.action_limit = QAction(MainWindow)
        self.action_limit.setObjectName(u"action_limit")
        icon3 = QIcon()
        icon3.addFile(u":/pyqt/source/images/excel.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.action_limit.setIcon(icon3)
        self.action_console = QAction(MainWindow)
        self.action_console.setObjectName(u"action_console")
        self.action_console.setCheckable(True)
        icon4 = QIcon()
        icon4.addFile(u":/pyqt/source/images/python.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_console.setIcon(icon4)
        self.action_processing_report = QAction(MainWindow)
        self.action_processing_report.setObjectName(u"action_processing_report")
        icon5 = QIcon()
        icon5.addFile(u":/pyqt/source/images/lc_dbformrename.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_processing_report.setIcon(icon5)
        self.action_qt_scatter = QAction(MainWindow)
        self.action_qt_scatter.setObjectName(u"action_qt_scatter")
        icon6 = QIcon()
        icon6.addFile(u":/pyqt/source/images/lc_linestyle.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_qt_scatter.setIcon(icon6)
        self.action_qt_visual_map = QAction(MainWindow)
        self.action_qt_visual_map.setObjectName(u"action_qt_visual_map")
        icon7 = QIcon()
        icon7.addFile(u":/pyqt/source/images/lc_objectcatalog.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_qt_visual_map.setIcon(icon7)
        self.action_qt_distribution_trans = QAction(MainWindow)
        self.action_qt_distribution_trans.setObjectName(u"action_qt_distribution_trans")
        icon8 = QIcon()
        icon8.addFile(u":/pyqt/source/images/lc_aligndown.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_qt_distribution_trans.setIcon(icon8)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.RightToolBarArea, self.toolBar)

        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_sava_data)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_dock_structure)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_console)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_limit)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_processing_report)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_qt_scatter)
        self.toolBar.addAction(self.action_qt_distribution_trans)
        self.toolBar.addAction(self.action_qt_visual_map)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_capability.setText(QCoreApplication.translate("MainWindow", u"capability", None))
#if QT_CONFIG(tooltip)
        self.action_capability.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u751f\u6210\u5236\u7a0b\u80fd\u529b\u62a5\u544a</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.action_sava_data.setText(QCoreApplication.translate("MainWindow", u"sava_data", None))
#if QT_CONFIG(tooltip)
        self.action_sava_data.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4fdd\u5b58\u4e3acsv&amp;excel</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.action_dock_structure.setText(QCoreApplication.translate("MainWindow", u"dock_structure", None))
#if QT_CONFIG(tooltip)
        self.action_dock_structure.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4fdd\u5b58\u89c6\u56fe\u7ed3\u6784</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.action_limit.setText(QCoreApplication.translate("MainWindow", u"limit\u6bd4\u8f83", None))
#if QT_CONFIG(tooltip)
        self.action_limit.setToolTip(QCoreApplication.translate("MainWindow", u"\u663e\u793aLimit\u95f4\u7684\u5dee\u5f02\u6027", None))
#endif // QT_CONFIG(tooltip)
        self.action_console.setText(QCoreApplication.translate("MainWindow", u"console", None))
#if QT_CONFIG(tooltip)
        self.action_console.setToolTip(QCoreApplication.translate("MainWindow", u"\u663e\u793a&\u9690\u85cfPython Console", None))
#endif // QT_CONFIG(tooltip)
        self.action_processing_report.setText(QCoreApplication.translate("MainWindow", u"\u5236\u7a0b\u80fd\u529b\u62a5\u544a", None))
#if QT_CONFIG(tooltip)
        self.action_processing_report.setToolTip(QCoreApplication.translate("MainWindow", u"\u5236\u7a0b\u80fd\u529b\u62a5\u544a", None))
#endif // QT_CONFIG(tooltip)
        self.action_qt_scatter.setText(QCoreApplication.translate("MainWindow", u"scatter", None))
#if QT_CONFIG(tooltip)
        self.action_qt_scatter.setToolTip(QCoreApplication.translate("MainWindow", u"\u6563\u70b9\u56fe", None))
#endif // QT_CONFIG(tooltip)
        self.action_qt_visual_map.setText(QCoreApplication.translate("MainWindow", u"visual_map", None))
        self.action_qt_distribution_trans.setText(QCoreApplication.translate("MainWindow", u"distribution_trans", None))
#if QT_CONFIG(tooltip)
        self.action_qt_distribution_trans.setToolTip(QCoreApplication.translate("MainWindow", u"\u6a2a\u5411\u5206\u5e03\u56fe", None))
#endif // QT_CONFIG(tooltip)
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

