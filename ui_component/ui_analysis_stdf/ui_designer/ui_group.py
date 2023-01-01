# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'group.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(234, 641)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.groupBox = QGroupBox(self.splitter)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(16777215, 300))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.listView = QListView(self.groupBox)
        self.listView.setObjectName(u"listView")
        self.listView.setMaximumSize(QSize(16777215, 160))

        self.verticalLayout_2.addWidget(self.listView)

        self.listView_2 = QListView(self.groupBox)
        self.listView_2.setObjectName(u"listView_2")
        self.listView_2.setMaximumSize(QSize(16777215, 120))

        self.verticalLayout_2.addWidget(self.listView_2)

        self.splitter.addWidget(self.groupBox)
        self.groupBox_2 = QGroupBox(self.splitter)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.listView_3 = QListView(self.groupBox_2)
        self.listView_3.setObjectName(u"listView_3")
        self.listView_3.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_3.addWidget(self.listView_3)

        self.pushButton = QPushButton(self.groupBox_2)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_3.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.groupBox_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_3.addWidget(self.pushButton_2)

        self.splitter.addWidget(self.groupBox_2)

        self.verticalLayout.addWidget(self.splitter)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Setting", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Group By", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"ChartData By Group", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\u9009\u53d6\u9879\u76ee\u52fe\u9009", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"\u9009\u53d6\u9879\u76ee\u53d6\u6d88\u52fe\u9009", None))
    # retranslateUi

