"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/12/23 18:12
@Site    : 
@File    : qt_plot_test.py
@Software: PyCharm
@Remark  : PyqtGraph
"""

import unittest

import numpy
import pyqtgraph as pg

from app_test.test_utils.log_utils import Print
from app_test.test_utils.mixins import Hdf5DataLoad
from app_test.test_utils.wrapper_utils import Tester
from chart_core.chart_pyqtgraph.trans_bar import TransBarChart
from chart_core.chart_pyqtgraph.trans_scatter import TransScatterChart
from chart_core.chart_pyqtgraph.visual_map import VisualMapChart

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class QtGraphPlotCase(unittest.TestCase, Hdf5DataLoad):
    """
    使用单元的DataFrame
    """

    @Tester()
    def test_base_plot(self):
        win = pg.GraphicsLayoutWidget(show=True)
        win.resize(10, 600)
        pg.setConfigOptions(antialias=True)
        p1 = win.addPlot()

        p1.setMouseEnabled(x=False, y=False)
        p1.setYRange(0, 100)
        p1.setXRange(0.5, 3)
        p1.showAxis('bottom', False)
        p1.showAxis('left', False)
        p1.hideButtons()

        inf1 = pg.InfiniteLine(movable=False, angle=90, label='  ',
                               labelOpts={'position': 0.1, 'color': (200, 200, 100), 'fill': (200, 200, 200, 150),
                                          'movable': True})
        inf1.setPos([0, 0])
        p1.addItem(inf1)

        pg.exec()

    @Tester(
        ["load_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_load_data(self):
        """

        :return:
        """
        Print.print_table(self.df_module.ptmd_df.to_dict(orient="records"))
        select_summary, id_module_dict = self.summary.load_select_data([1])
        self.li.set_data(select_summary, id_module_dict)
        self.li.concat()

    @Tester(
        ["test_load_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_set_group(self):
        """
        +-----------+-----------+----+--------+----------+----------+--------------+----------+---------+----------+-----------+----------+----------+---------+---------+----------+-------+-------+--------+-----------+-----------+---------------------+-----------+
        | FILE_PATH | FILE_NAME | ID | LOT_ID | SBLOT_ID | WAFER_ID | BLUE_FILM_ID | TEST_COD | FLOW_ID | PART_TYP |  JOB_NAM  | TST_TEMP | NODE_NAM | SETUP_T | START_T | SITE_CNT |  QTY  |  PASS | YIELD  | PART_FLAG | READ_FAIL |      HDF5_PATH      |   GROUP   |
        +-----------+-----------+----+--------+----------+----------+--------------+----------+---------+----------+-----------+----------+----------+---------+---------+----------+-------+-------+--------+-----------+-----------+---------------------+-----------+
        |    DEMO   |    DEMO   | 1  |  DEMO  |   DEMO   |  WAFER   |              |   CP1    |    R0   |  ESP32   | TEST_DEMO |    25    |  Python  |    0    |    0    |    0     | 56963 | 46611 | 81.83% |     0     |     1     | .\test_data\TEST.h5 | DEMO|DEMO |
        +-----------+-----------+----+--------+----------+----------+--------------+----------+---------+----------+-----------+----------+----------+---------+---------+----------+-------+-------+--------+-----------+-----------+---------------------+-----------+

        print(self.li.group_list)
        print(self.li.da_group_list)
        ['DEMO|DEMO']
        ['S012', 'S013', '....']
        :return:
        """
        self.li.calculation_top_fail()
        self.li.calculation_capability()
        self.li.background_generation_data_use_to_chart_and_to_save_csv()
        self.li.set_data_group(
            ["LOT_ID", "SBLOT_ID"],
            ["SITE_NUM"]
        )
        Print.print_table(self.li.select_summary.to_dict(orient="records"))

    @Tester(
        ["test_set_group"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_get_test_id_data(self):
        unit_prr = self.li.get_unit_data_by_group_key('DEMO|DEMO', 'S012')
        unit_dtp_df = self.li.get_unit_data_by_test_id(unit_prr, 1)
        print(self.li.capability_key_dict[1])
        return unit_dtp_df

    @Tester(
        ["test_get_test_id_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_scatter_plot(self, **kwargs):
        """
        good
        :param kwargs:
        :return:
        """
        win = pg.GraphicsLayoutWidget()
        pg.setConfigOptions(antialias=True)
        scatter_chart = TransScatterChart(self.li)
        scatter_chart.set_data(22)  # TEST_ID == 1
        scatter_chart.set_range_self()
        scatter_chart.set_df_chart()
        scatter_chart.set_line_self()
        scatter_chart.pw_show()
        pg.exec()

    @Tester(
        ["test_set_group"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_bin_mapping_plot(self, **kwargs):
        """
        TODO:
            性能达不到要求
            待更新
        :param kwargs:
        :return:
        """
        pass

    @Tester(
        ["test_set_group"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_visual_mapping_plot(self, **kwargs):
        """
        good
        :return:
        """
        win = pg.GraphicsLayoutWidget()
        pg.setConfigOptions(antialias=True)
        visual_map_chart = VisualMapChart(self.li)
        visual_map_chart.set_data(22)
        visual_map_chart.set_front_chart()
        visual_map_chart.pw_show()
        pg.exec()

    @Tester(
        ["test_set_group"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_trans_bar_plot(self, **kwargs):
        """
        good
        :param kwargs:
        :return:
        """
        win = pg.GraphicsLayoutWidget()
        pg.setConfigOptions(antialias=True)
        bar_chart = TransBarChart(self.li)
        bar_chart.set_data(22)  # TEST_ID == 1
        bar_chart.set_range_self()
        bar_chart.set_df_chart()
        bar_chart.set_line_self()
        bar_chart.pw_show()
        pg.exec()

    @Tester(
        ["test_set_group"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_pareto_plot(self):
        """
        暂无太大用处
        :return:
        """
        pass

    @Tester(
        ["test_set_group"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_multi_plot(self):
        """
        success
        :return:
        """
        win = pg.GraphicsLayoutWidget()
        pg.setConfigOptions(antialias=True)

        scatter_chart = TransScatterChart(self.li)
        scatter_chart.set_data(22)  # TEST_ID == 1
        scatter_chart.set_range_self()
        scatter_chart.set_df_chart()
        scatter_chart.set_line_self()
        scatter_chart.pw_show()

        bar_chart = TransBarChart(self.li)
        bar_chart.set_data(22)  # TEST_ID == 1
        bar_chart.set_range_self()
        bar_chart.set_df_chart()
        bar_chart.set_line_self()
        bar_chart.pw_show()

        visual_map_chart = VisualMapChart(self.li)
        visual_map_chart.set_data(22)
        visual_map_chart.set_front_chart()
        visual_map_chart.pw_show()

        pg.exec()
