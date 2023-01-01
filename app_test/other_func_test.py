"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/12/26 14:48
@Site    : 
@File    : other_func_test.py
@Software: PyCharm
@Remark  : 
"""
import unittest

import pandas as pd

from app_test.test_utils.wrapper_utils import Tester


class QtUiCase(unittest.TestCase):

    @Tester()
    def test_drop_duplicate(self):
        df = pd.DataFrame([{"A": 1, "B": 1}, {"A": 1, "B": 2}, {"A": 1, "B": 1}, {"A": 1, "B": 2}, {"A": 2, "B": 2}])
        print(df[["A", "B"]].drop_duplicates())

    @Tester()
    def test_pandas_dict_data(self):
        data = {
            1: [1, 2, 3],
            2: [1, 2, 3],
            3: [1, 2, 3],
        }
        print(pd.DataFrame(data))

    @Tester()
    def test_pandas_list_data(self):
        data = [
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
        ]
        print(pd.DataFrame(data))
