"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/12/20 11:25
@Site    : 
@File    : mixins.py
@Software: PyCharm
@Remark  : 
"""

from common.app_variable import TestVariable as TestVar, DataModule
from common.li import Li, SummaryCore
from parser_core.stdf_parser_file_write_read import ParserData


class CsvDataLoad:
    load: bool = False
    df_module: DataModule = None

    def load_data(self):
        """
        正式环境中, 解析stdf之前的时候记得先查看是否有缓存
        :return:
        """
        if self.load:
            return
        self.df_module = ParserData.load_csv()
        if self.df_module is None:
            raise Exception("ParserData.load_csv fail!")
        self.load = True


class Hdf5DataLoad:
    """
        从HDF5文件中读取数据
        """
    load: bool = False
    df_module: DataModule = None
    summary: SummaryCore = None
    li: Li = None

    def load_data(self):
        """
        正式环境中, 解析stdf之前的时候记得先查看是否有缓存HDF5文件
        :return:
        """
        if self.load:
            return
        ID = 1
        self.df_module = ParserData.load_hdf5_test(TestVar.HDF5_PATH, ID)
        self.df_module.prr_df.set_index(["ID", "PART_ID"], inplace=True)
        self.df_module.dtp_df.set_index(["TEST_ID", "ID", "PART_ID"], inplace=True)
        if self.df_module is None:
            raise Exception("ParserData.load_hdf5 fail!")
        self.summary = SummaryCore()
        self.li = Li()
        summary_list = [
            {
                "FILE_PATH": "DEMO",
                "FILE_NAME": "DEMO",
                "ID": ID,
                "LOT_ID": "DEMO",
                "SBLOT_ID": "DEMO",
                "WAFER_ID": "WAFER",
                "BLUE_FILM_ID": "",
                'TEST_COD': 'CP1',
                'FLOW_ID': 'R0',
                'PART_TYP': 'ESP32',
                'JOB_NAM': 'TEST_DEMO',
                'TST_TEMP': '25',
                'NODE_NAM': 'Python',
                'SETUP_T': 0,
                'START_T': 0,
                'SITE_CNT': 0,
                **ParserData.get_yield(self.df_module.prr_df, 0, 1),
                "PART_FLAG": "0",
                "READ_FAIL": "1",
                "HDF5_PATH": TestVar.HDF5_PATH,
            }
        ]
        self.summary.set_data(summary_list)
        self.li.set_data(*self.summary.load_select_data([1]))
        self.load = True
