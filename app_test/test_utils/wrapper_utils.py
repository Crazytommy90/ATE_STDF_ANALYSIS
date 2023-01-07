"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/12/20 11:24
@Site    : 
@File    : wrapper_utils.py
@Software: PyCharm
@Remark  : 
"""

import time
from app_test.test_utils.log_utils import Print
from common.app_variable import GlobalVariable


class Tester:

    def __init__(self,
                 args: list = None,
                 over_on: bool = False,  # 失效继续测试
                 exec_time: bool = False,  # 打开测试时间
                 skip_args_time: bool = False,  # 排除掉执行args中的函数的时间
                 ):
        """

        :param args: 传入类中function的name -> 在函数的**kwargs中取值
        :param over_on:
        :param exec_time:
        """
        self.args = args
        self.over_on: bool = over_on
        self.exec_time: bool = exec_time
        self.skip_args_time: bool = skip_args_time

    def __call__(self, func):

        def wrapper(ctx, **kwargs):

            start = 0
            if self.exec_time:
                start = time.perf_counter()
            if self.args:
                for per_func_name in self.args:
                    if not hasattr(ctx, per_func_name):
                        Print.warning("No function name : {}".format(per_func_name))
                        continue
                    per_func = getattr(ctx, per_func_name)
                    res = per_func()
                    if res is not None:
                        kwargs[per_func_name] = res
            if self.skip_args_time:
                start = time.perf_counter()
            # try:
            res = func(ctx, **kwargs)
            # except Exception as err:
            #     Print.danger(str(err))
            #     return False

            if self.exec_time:
                use_time = round(time.perf_counter() - start, 3)
                Print.info("func: {} exec time: {}.".format(func.__name__, use_time))
            return res

        return wrapper


class Time:

    def __call__(self, func):
        def wrapper(ctx, *args, **kwargs):
            if not GlobalVariable.DEBUG:
                return func(ctx, *args, **kwargs)
            start = time.perf_counter()
            res = func(ctx, *args, **kwargs)
            use_time = round(time.perf_counter() - start, 3)
            Print.info("func: {} exec time: {}.".format(func.__name__, use_time))
            return res

        return wrapper
