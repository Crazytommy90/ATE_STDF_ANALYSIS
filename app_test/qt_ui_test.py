"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/12/20 11:22
@Site    :
@File    : qt_ui_test.py
@Software: PyCharm
@Remark  :
"""
import os
import sys
import pickle
import unittest

from PySide2.QtCore import Qt, QTimer
from PySide2.QtWidgets import QApplication
from PySide2.QtTest import QTest

from app_test.test_utils.log_utils import Print
from app_test.test_utils.mixins import Hdf5DataLoad
from app_test.test_utils.wrapper_utils import Tester
from chart_core.chart_pyqtgraph.poll import ChartDockWindow
from common.app_variable import TestVariable
from common.li import SummaryCore, Li
from common.stdf_interface.stdf_parser import SemiStdfUtils
from ui_component.ui_analysis_stdf.ui_components.ui_data_group import DataGroupWidget
from ui_component.ui_analysis_stdf.ui_components.ui_file_load_widget import FileLoadWidget
from ui_component.ui_analysis_stdf.ui_components.ui_table_load_widget import TableLoadWidget
from ui_component.ui_analysis_stdf.ui_components.ui_tree_load_widget import TreeLoadWidget
from ui_component.ui_analysis_stdf.ui_stdf import StdfLoadUi
from ui_component.ui_common.ui_console import ConsoleWidget
from ui_component.ui_main.ui_main import Main_Ui
from ui_component.ui_main.ui_setting import SettingWidget

QtUiCaseAuto = False


class QtUiCase(unittest.TestCase, Hdf5DataLoad):
    """
    测试UI是否可以应对工程师使用
    """
    li: Li = Li()
    summary: SummaryCore = SummaryCore()

    @Tester()
    def test_console_ui(self):
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        my_win = ConsoleWidget()
        my_win.show()
        app.exec_()

    @Tester()
    def test_setting_ui(self):
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        win = SettingWidget()
        win.show()
        app.exec_()

    def test_stdf_load_ui(self):
        """
        选取数据
        :return:
        """
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        win = FileLoadWidget(self.summary)
        win.directory_select_test(TestVariable.STDF_FILES_PATH)
        win.show()
        if QtUiCaseAuto:
            QTest.mouseClick(win.pushButton, Qt.LeftButton)
            QTest.mouseClick(win.pushButton_3, Qt.LeftButton)
            QTest.mouseClick(win.comboBox, Qt.LeftButton)
            QTimer.singleShot(1000, lambda: win.close())
        app.exec_()
        self.assertEqual(True, win.summary.ready)

    @Tester(
        ["test_stdf_load_ui"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_stdf_tree_ui(self):
        """
        将数据处理后加载到Tree上用于选取
        :return:
        """
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        win = TreeLoadWidget(li=self.li, summary=self.summary)
        win.set_tree()
        win.show()
        # TODO: pushButton后的操作和解析可以改成多线程, 传递一个进度条
        if QtUiCaseAuto:
            # win.summary.add_custom_node(TreeUtils.get_tree_ids(win.treeWidget), "TEST")
            # win.set_tree()
            QTimer.singleShot(0, lambda: QTest.mouseClick(win.pushButton, Qt.LeftButton))
            # QTimer.singleShot(3000, lambda: win.close())
        app.exec_()
        Print.print_table(win.li.capability_key_list)

    @Tester(
        ["test_stdf_tree_ui"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_table_capability_ui(self):
        """
        加载从TreeLoad中选取的数据, 并解析
        测试改变Limit后重算Rate
        测试删除选中limit外的数据 -> 变慢了好多啊
        测试只对选中的数据进行分析
        :return:
        """
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        win = TableLoadWidget(self.li, self.summary)
        win.cal_table()
        if QtUiCaseAuto:
            "更改limit后重算yield"
        win.show()
        app.exec_()

    @Tester(
        ["test_stdf_tree_ui"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_group_load(self):
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        win = DataGroupWidget(self.li)
        win.checkbox_changed()
        win.show()
        app.exec_()

    @Tester(

    )
    def test_main_ui_stdf(self):
        """

        :return:
        """
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        win = StdfLoadUi()
        if QtUiCaseAuto:
            "更改limit后重算yield"
        win.show()
        app.exec_()

    @Tester(

    )
    def test_ui_stdf_save_CsvOrXlsx(self):
        """
        数据保存为csv/(xlsx -> 用excel打开csv并调用vba)
        使用pandas的unstack看好用不.
        :return:
        """
        pass

    @Tester(

    )
    def test_ui_stdf_show_limit(self):
        """
        Limit之间的差异
        :return:
        """
        pass

    @Tester(

    )
    def test_app_ui(self):
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        app.setApplicationName("IC DATA ANALYSIS")
        win = Main_Ui(license_control=False)
        win.show()
        app.exec_()


class QtUiHdf5Case(unittest.TestCase, Hdf5DataLoad):
    """
    数据解析, 给UI传递参数, 简单测试
    """
    li: Li = Li()
    summary: SummaryCore = SummaryCore()

    def test_something(self):
        self.assertEqual(True, True)

    @Tester(
        [],
        exec_time=True,
        skip_args_time=True,
    )
    def test_stdf_read(self):
        """
        原始STDF数据
        :return:
        """
        print(SemiStdfUtils.get_lot_info_by_semi_ate(TestVariable.STDF_PATH))

    @Tester(
        [],
        exec_time=True,
        skip_args_time=True,
    )
    def test_stdf_load_ui(self, **kwargs):
        """
        原始STDF数据
        :param kwargs:
        :return:
        """

    @Tester(
        [],
        exec_time=True,
        skip_args_time=True,
    )
    def test_tree_load(self, **kwargs):
        pass

    def load_table_data(self):
        if not os.path.exists(TestVariable.TABLE_PICKLE_PATH):
            Print.warning("No Path")
            self.assertEqual(True, False)
        with open(TestVariable.TABLE_PICKLE_PATH, 'rb') as file:
            li = pickle.loads(file.read())
        return li

    @Tester(
        ["load_table_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_read_table_data(self, **kwargs):
        li = kwargs.get("load_table_data")
        if li is None:
            Print.warning("No Data")
            self.assertEqual(True, False)
        Print.print_table(li)
        self.li.capability_key_list = li

    @Tester(
        ["test_read_table_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_table_load(self):
        app = QApplication(sys.argv)
        win = TableLoadWidget(self.li, self.summary)
        win.cal_table()
        win.show()
        app.exec_()

    @Tester()
    def test_chart_dock_widget(self):
        app = QApplication(sys.argv)
        win = ChartDockWindow(self.li)
        win.show()
        app.exec_()
