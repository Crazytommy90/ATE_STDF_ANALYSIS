"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/5/17 21:09
@Software: PyCharm
@File    : ui_data_group.py
@Remark  : 
"""
from PySide2.QtCore import Qt, Slot, Signal
from PySide2.QtWidgets import QWidget
from pyqtgraph.parametertree import Parameter, ParameterTree

from ui_component.ui_common.my_text_browser import Print
from ui_component.ui_main.ui_designer.ui_setting import Ui_Form
from ui_component.ui_app_variable import UiGlobalVariable
from var_language import language


class SettingWidget(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(SettingWidget, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle("Setting Tool")
        self.jmp_t = ParameterTree()
        self.graph_t = ParameterTree()
        self.jmp_t.hide()
        self.graph_t.hide()
        self.verticalLayout.addWidget(self.jmp_t)
        self.verticalLayout.addWidget(self.graph_t)
        self.init_tree_params(self.jmp_t, UiGlobalVariable.JMP_PARAMS)
        self.init_tree_params(self.graph_t, UiGlobalVariable.GRAPH_PARAMS)
        self.comboBox.addItems(UiGlobalVariable.PLOT_BACKEND)

    def init_tree_params(self, params_tree: ParameterTree, params: list):
        p = Parameter.create(name='params', type='group', children=params)
        p.sigTreeStateChanged.connect(self.change)
        params_tree.setParameters(p, showTop=False)

    def change(self, param, changes):
        for param, change, data in changes:
            key = language.kwargs[param.name()]
            setattr(UiGlobalVariable, key, data)

    @Slot(str)
    def on_comboBox_currentIndexChanged(self, index):
        if index == UiGlobalVariable.PLOT_BACKEND[0]:
            Print.info("JMP->专业的统计学数据分析")
            self.jmp_t.show()
            self.graph_t.hide()
            return
        if index == UiGlobalVariable.PLOT_BACKEND[1]:
            Print.info("QT Graph->快速可视化")
            self.jmp_t.hide()
            self.graph_t.show()
            return

    @Slot()
    def checkbox_changed(self):
        self.group_emit.emit()
        # print(self.get_group_params())
        # print(self.get_da_group_params())
