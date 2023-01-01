"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/11/25 15:04
@Site    : 
@File    : log_utils.py
@Software: PyCharm
@Remark  : 
"""
from typing import List

from loguru import logger
from prettytable import PrettyTable

logger_config = logger.add('logger.log', level="INFO", retention='14 days')


class Print:
    DEBUG = True

    @staticmethod
    def info(string):
        print('\033[1;36m{}\033[0m'.format(string))

    @staticmethod
    def debug(string):
        logger.debug(string)

    @staticmethod
    def record(string):
        logger.info(string)

    @staticmethod
    def success(string):
        logger.success(string)

    @staticmethod
    def warning(string):
        logger.warning(string)

    @staticmethod
    def danger(string):
        logger.error(string)

    @staticmethod
    def PASS():
        Print.success("""
******************************************
******  @@@@     @    @@@@@  @@@@@  ******
******  @   @   @ @   @      @      ******
******  @@@@   @@@@@  @@@@@  @@@@@  ******
******  @      @   @      @      @  ******
******  @      @   @  @@@@@  @@@@@  ******
******************************************
        """)

    @staticmethod
    def FAIL():
        Print.warning("""
******************************************
******  @@@@@    @      @    @      ******
******  @       @ @     @    @      ******
******  @@@@@  @@@@@    @    @      ******
******  @      @   @    @    @      ******
******  @      @   @    @    @@@@@  ******
******************************************
        """)

    @staticmethod
    def print_table(data_list: List[dict]):
        table = PrettyTable()
        # table.title = 'Calculation Ptr'
        for index, each in enumerate(data_list):
            if index == 0:
                table.field_names = each.keys()
            table.add_row(each.values())
        print(table)


if __name__ == '__main__':
    Print.PASS()
