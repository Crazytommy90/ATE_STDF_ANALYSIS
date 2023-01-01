# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'scan_stdf_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from chart_core.data_qt_module.table_module import ReScanTableWidget


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1290, 532)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 0, 3, 1, 1)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 10, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 5, 1, 1)

        self.dateEdit = QDateEdit(Form)
        self.dateEdit.setObjectName(u"dateEdit")

        self.gridLayout.addWidget(self.dateEdit, 1, 1, 1, 1)

        self.comboBox_5 = QComboBox(Form)
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.gridLayout.addWidget(self.comboBox_5, 1, 4, 1, 1)

        self.radioButton_2 = QRadioButton(Form)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setEnabled(False)

        self.gridLayout.addWidget(self.radioButton_2, 1, 0, 1, 1)

        self.comboBox = QComboBox(Form)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 1, 5, 1, 1)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)

        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 0, 11, 1, 1)

        self.dateEdit_2 = QDateEdit(Form)
        self.dateEdit_2.setObjectName(u"dateEdit_2")

        self.gridLayout.addWidget(self.dateEdit_2, 1, 3, 1, 1)

        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMaximumSize(QSize(200, 16777215))

        self.gridLayout.addWidget(self.lineEdit_2, 1, 11, 1, 1)

        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 0, 4, 1, 1)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMaximumSize(QSize(200, 16777215))

        self.gridLayout.addWidget(self.lineEdit, 1, 10, 1, 1)

        self.checkBox = QCheckBox(Form)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.tableWidget = ReScanTableWidget(Form)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBox = QSpinBox(Form)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimum(30)
        self.spinBox.setMaximum(1000)
        self.spinBox.setValue(100)

        self.horizontalLayout.addWidget(self.spinBox)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout.addWidget(self.label_5)

        self.spinBox_3 = QSpinBox(Form)
        self.spinBox_3.setObjectName(u"spinBox_3")
        self.spinBox_3.setFocusPolicy(Qt.WheelFocus)
        self.spinBox_3.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setMaximum(100000)

        self.horizontalLayout.addWidget(self.spinBox_3)

        self.label_10 = QLabel(Form)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout.addWidget(self.label_10)

        self.spinBox_4 = QSpinBox(Form)
        self.spinBox_4.setObjectName(u"spinBox_4")
        self.spinBox_4.setEnabled(True)
        self.spinBox_4.setFocusPolicy(Qt.NoFocus)
        self.spinBox_4.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_4.setMaximum(10000)

        self.horizontalLayout.addWidget(self.spinBox_4)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.spinBox_2 = QSpinBox(Form)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setFocusPolicy(Qt.NoFocus)
        self.spinBox_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_2.setMaximum(999999999)

        self.horizontalLayout.addWidget(self.spinBox_2)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u540e\u53f0\u89e3\u6790\u811a\u672c\u8bb0\u5f55\u76d1\u63a7", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"FINISH_T", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"LOT_ID(\u56de\u8f66\u641c\u7d22)", None))
        self.label.setText(QCoreApplication.translate("Form", u"SUB_CON", None))
        self.radioButton_2.setText(QCoreApplication.translate("Form", u"\u6309\u7167STDF\u6765\u67e5\u8be2", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"START_T", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"WAFER_ID(\u56de\u8f66\u641c\u7d22)", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"LEVEL_NM", None))
        self.checkBox.setText(QCoreApplication.translate("Form", u"\u663e\u793a\u6240\u6709\u5df2\u5bfc\u5165", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u663e\u793a\u6700\u5927\u884c\u6570", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u5f53\u524d\u9875", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u6700\u5927\u9875", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u67e5\u627e\u6570\u636e\u884c\u6570", None))
        self.spinBox_2.setSuffix(QCoreApplication.translate("Form", u"\u6761\u6570\u636e", None))
    # retranslateUi

