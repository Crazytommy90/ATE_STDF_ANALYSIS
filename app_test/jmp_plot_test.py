"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/12/20 11:23
@Site    : 
@File    : jmp_plot_test.py
@Software: PyCharm
@Remark  : 
"""
import unittest

from app_test.test_utils.mixins import Hdf5DataLoad


class JmpPlotCase(unittest.TestCase, Hdf5DataLoad):
    """
    使用单元的DataFrame
    专业的数据分析标杆
    1. 将数据导出到csv中, 按照之前的格式
    2. 将数据的规格线放入到table中
    3. 生成数据的时候自动放入规格限
    """
    def load_jmp_csv_data(self):
        """
        带坐标的测试数据
        :return:
        """
        pass

    def test_scatter_plot(self):
        pass

    def test_bin_mapping_plot(self):
        """
        hbin
        sbin
        tno
        :return:
        """
        pass

    def test_visual_mapping_plot(self):
        """

        :return:
        """
        pass

    def test_trans_bar_plot(self):
        pass

    def test_pareto_plot(self):
        pass

    def test_distribution_plot(self):
        pass

    def test_box_plot(self):
        pass

    def test_box_scatter_plot(self):
        pass

    def test_linear(self):
        """
        线性回归
        :return:
        """
        pass

    def test_multi_plot(self):
        pass
