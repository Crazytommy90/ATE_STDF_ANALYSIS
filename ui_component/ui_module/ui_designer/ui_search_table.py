# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'search_table.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ui_component.ui_module.table_module import PauseTableWidget


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(918, 449)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, -1, -1, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleTable = PauseTableWidget(Form)
        self.titleTable.setObjectName(u"titleTable")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleTable.sizePolicy().hasHeightForWidth())
        self.titleTable.setSizePolicy(sizePolicy)
        self.titleTable.setMaximumSize(QSize(16777214, 66))
        self.titleTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.titleTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.titleTable.horizontalHeader().setVisible(True)
        self.titleTable.verticalHeader().setVisible(False)
        self.titleTable.verticalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.titleTable)

        self.dataTable = PauseTableWidget(Form)
        self.dataTable.setObjectName(u"dataTable")
        self.dataTable.horizontalHeader().setVisible(False)
        self.dataTable.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.dataTable)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi

