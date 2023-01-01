"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/12/21 17:31
@Site    : 
@File    : mir_info_test.py
@Software: PyCharm
@Remark  : 用于测试解析STDF的MIR数据
"""
import unittest

from app_test.test_utils.wrapper_utils import Tester
from common.app_variable import TestVariable
from common.stdf_interface.stdf_parser import SemiStdfUtils


class StdfInfoCase(unittest.TestCase):
    """
    从STDF数据中解析信息数据
    GROUP
    """

    def test_something(self):
        self.assertEqual(True, True)

    @Tester(
        [],
        exec_time=True,
    )
    def test_load_stdf_data(self):
        """
        TODO:
            WIR中 HEAD_NUM 赋值为233的是BLUE号 -> 蓝膜号, 测试数据转为STDF的时候指定HEAD_NUM=233为蓝膜号
            Only For Me
        :return:
        """
        info = SemiStdfUtils.get_lot_info_by_semi_ate(TestVariable.STDF_PATH)
        self.assertEqual(True, True if info else False)
        for each in info:
            print(each)
