#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : li.py
@Author  : Link
@Time    : 2022/12/23 20:35
@Mark    : 
"""
import os
import time
from multiprocessing import Process
from typing import List, Dict, Union, Tuple

import pandas as pd
from PySide2.QtCore import QObject, Signal

from app_test.test_utils.wrapper_utils import Time
from common.app_variable import DataModule, PtmdModule, ToChartCsv, GlobalVariable
from common.cal_interface.capability import CapabilityUtils
from parser_core.stdf_parser_file_write_read import ParserData
from report_core.openxl_utils.utils import OpenXl


class SummaryCore:
    """
    1. 每个文件解析完成后, 会有各个Summary和子数据
    2. Summary会经过组合后生成 SummaryDf
        SummaryDf -> by start_time 排序
        | ID  | R | LOT_ID | SB_LOT_ID | FLOW_ID | QTY | PASS | YIELD | PASS_VERIFY | ... |
        | ··· | Y | ······ |
        | ··· | N |
        | ···

        df_dict ->
        {
            逻辑需要优化, 数据要在需要的时候才从HDF5中读取·
        }
    3. 组合新的Limit数据,注意测试项目和TEST_ID的对应即可
    4. SummaryDf 展示在Tree上
        Group By: LOT_ID -> FLOW_ID ? -> SB_LOT_ID ?
            groupby之后 使用min(START_TIME), max(FINISH_TIME), sum(QTY), sum(PASS)
        给到Tree的数据:
            [
                {
                | ID  | LOT_ID | ...
                children:
                    [ {
                    | ID  | LOT_ID | ...
                    }, ... ]
                },
                {
                | ID  | LOT_ID | ...
                children:
                    [ {
                    | ID  | LOT_ID | ...
                    }, ... ]
                }
            ]
    5. 从Tree中拿到IDS, 汇整为NowSummaryDf, 并拿到Group信息后汇整为 GROUP列
        会有两份数据, 1. NowSummaryDf 2. NowDfs->将df_dict中的数据按需求contact起来
    6. 支持多个window来汇整数据
    """
    ready: bool = False
    summary_df: pd.DataFrame = None

    def set_data(self, summary: Union[list, pd.DataFrame]):
        """
        后台必然默认传送一个元组, 拆包为三份数据,并且传来的summary_df已经经过排序
        而且这个返回的数据是比较重要的!!!@后期是需要用在服务器缓存中的
        """
        if not summary:
            return
        if isinstance(summary, list):
            self.summary_df = pd.DataFrame(summary)
        else:
            self.summary_df = summary
        self.ready = True
        return self.ready

    def get_summary_tree(self):
        """
        SummaryDf 展示在Tree上
        :return:
        """
        tree_dict_list = list()
        for key, e_df in self.summary_df.groupby("LOT_ID"):  # type:str, pd.DataFrame
            key = str(key)
            qty = e_df["QTY"].sum()
            pass_qty = e_df["PASS"].sum()
            if qty == 0:
                pass_yield = "0.0%"
            else:
                pass_yield = '{}%'.format(round(pass_qty / qty * 100, 2))
            tree_dict = {
                "LOT_ID": key,
                "QTY": qty,
                "PASS": pass_qty,
                "YIELD": pass_yield,
                "START_T": e_df["START_T"].min(),
                "children": e_df.to_dict(orient="records")
            }
            tree_dict_list.append(tree_dict)

        return tree_dict_list

    def add_custom_node(self, ids: List[int], new_lot_id: str):
        """
        将多个数据组合为一个自定义的LOT, 比如两个版本的数据对比, 将一部分分为版本A(LOT_A), 另一部分分为版本B(LOT_B)
        {
            'FILE_PATH': '',
            'FILE_NAME': '',
            'ID': 100000,
            'LOT_ID': '',
            'SBLOT_ID': '',
            "WAFER_ID": "",
            "BLUE_FILM_ID": "",
            'TEST_COD': '',
            'FLOW_ID': '',
            'PART_TYP': '',
            'JOB_NAM': '',
            'TST_TEMP': '',
            'NODE_NAM': '',
            'SETUP_T': 1620734064,
            'START_T': 1620734070,
            'SITE_CNT': 1,
            'QTY': 2534,
            'PASS': 2534,
            'YIELD': '100.0%',
            'PART_FLAG': 0,
            'READ_FAIL': True
            'HDF5_PATH': ""
            },
        """
        if self.summary_df is None:
            return

        summary_info = self.summary_df[self.summary_df.ID.isin(ids)]
        new_id = self.summary_df["ID"].max() + 1
        file_path = []
        file_name = []
        part_flag = []
        read_fail = []
        qty, pass_qty = 0, 0
        for row in summary_info.itertuples():
            each_path = getattr(row, "HDF5_PATH")
            each_part_flag = getattr(row, "PART_FLAG")
            each_read_file = getattr(row, "READ_FAIL")
            each_file = os.path.split(each_path)[-1]
            prr = ParserData.load_prr_df(each_path)
            yield_data = ParserData.get_yield_data(prr)
            qty += yield_data["QTY"]
            pass_qty += yield_data["PASS"]
            file_path.append(each_path)
            file_name.append(each_file)
            part_flag.append(each_part_flag)
            read_fail.append(each_read_file)
        file_path_str = ";".join(file_path)
        file_name_str = ";".join(file_name)
        part_flag_str = ";".join(part_flag)
        read_fail_str = ";".join(read_fail)
        if qty == 0:
            pass_yield = "0.0%"
        else:
            pass_yield = '{}%'.format(round(pass_qty / qty * 100, 2))
        self.summary_df.loc[len(self.summary_df.index)] = [
            "",  # FILE_PATH
            file_name_str,  # FILE_NAME
            new_id,  # ID
            new_lot_id,  # LOT_ID
            new_lot_id,  # SB_LOT_ID
            "all",  # LOT_ID
            "all",  # WAFER_ID
            'all',  # BLUE_FILM_ID
            'all',  # FLOW_ID
            'all',  # PART_TYPE
            'all',  # JOB_NAME
            '~',  # TST_TEMP
            '~',  # NODE_NAM
            summary_info.SETUP_T.min(),  # SETUP_T
            summary_info.START_T.min(),  # START_T
            '~',  # SITE_CNT
            qty,  # QTY
            pass_qty,  # PASS
            pass_yield,  # YIELD
            part_flag_str,  # PART_FLAG
            read_fail_str,  # READ_FAIL
            file_path_str  # HDF5_PATH
        ]

    def load_select_data(self, ids: List[int], quick: bool = False, sample_num: int = 1E4):
        """
        返回数据
        整理出一个比较完整的 ptmd 的整合dict
        重复的ptmd_dict就选用最新的
        主要给每个单元的Prr给一个ID用于数据链接
        难度就是将载入的多份数据组合为一份数据
        :param ids:
        :param quick:
        :param sample_num:
        :return:
        """
        id_module_dict = {}
        select_summary = self.summary_df[self.summary_df.ID.isin(ids)]
        for select in select_summary.itertuples():
            ID = getattr(select, "ID")

            select_paths = getattr(select, "HDF5_PATH").split(";")

            if len(select_paths) == 1:
                data_module = ParserData.load_hdf5_analysis(
                    getattr(select, "HDF5_PATH"), int(getattr(select, "PART_FLAG")),
                    int(getattr(select, "READ_FAIL")),
                    unit_id=ID,
                )

            else:
                part_flag = getattr(select, "PART_FLAG").split(";")
                read_fail = getattr(select, "READ_FAIL").split(";")
                data_modules = []
                for index in range(len(select_paths)):
                    data_module = ParserData.load_hdf5_analysis(
                        select_paths[index], int(part_flag[index]), int(read_fail[index]),
                        unit_id=index,
                    )
                    data_modules.append(data_module)
                data_module = ParserData.contact_data_module(data_modules, unit_id=ID, update_id=True)

            id_module_dict[ID] = data_module
        return select_summary, id_module_dict

    # def get_bin_summary(self, ids: List[int], group_params: Union[list, None], da_group_params: Union[list, None]):
    #     """
    #     bin和bin_map这类数据是不需要完全载入详细数据集参数的, 所以数据临时即可取得
    #     :param da_group_params: 根据Site或是Head(不考虑)的分组
    #     :param group_params: 根据Summary的分组
    #     :param ids:
    #     :return: 返回可以直接被Plot的数据
    #     """


class Li(QObject):
    """
    从Tree中得到的确定是需要的数据.
    进到这里面的数据都是数据帧和控制Group的Summary
    """
    select_summary: pd.DataFrame = None
    id_module_dict: Dict[int, DataModule] = None
    df_module: DataModule = None
    # ======================== signal
    QCalculation = Signal()  # capability_key_list 改变的信号
    QMessage = Signal(str)  # 用于全局来调用一个MessageBox, 只做提示
    QStatusMessage = Signal(str)  # 用于全局来调用一个MessageBox, 只做提示

    QChartSelect = Signal()  # 用于刷新选取的数据
    QChartRefresh = Signal()  # 用于重新刷新所有的图
    # ======================== Temp
    capability_key_list: list = None
    capability_key_dict: Dict[int, dict] = None  # key: TEST_ID -> 仅仅用于Show Plot
    top_fail_dict: dict = None

    # ======================== 用于绘图或是capability group
    to_chart_csv_data: ToChartCsv = None
    group_params = None
    da_group_params = None

    def __init__(self):
        super(Li, self).__init__()

    def set_data(self,
                 select_summary: pd.DataFrame,
                 id_module_dict: Dict[int, DataModule]
                 ):
        """

        :param select_summary: Mir&Wir等相关的信息整合的Summary
        :param id_module_dict: 每行Summary都有一个唯一ID, 指向了module数据
        :return:
        """
        self.select_summary = select_summary.copy()
        self.select_summary["GROUP"] = "*"
        self.id_module_dict = id_module_dict

    def concat(self):
        """
        TODO:
            prr_df.set_index(["PART_ID"])
            dtp_df.set_index(["TEST_ID", "PART_ID"])
            dtp_df.TEST_ID <==> dtp_df.TEST_ID
            prr_df.ID <==> select_summary.ID
        active:
            1. 整合进入数据空间的数据, 都contact成一个数据, 关注["ID", "PART_ID"]这两列
            2. 最终concat成为一份数据, 再做计算就清晰多了
        :return:
        """
        if len(self.id_module_dict) == 0:
            return
        data_module_list = []
        for df_id, module in self.id_module_dict.items():
            data_module_list.append(module)
        self.df_module = ParserData.contact_data_module(data_module_list)
        self.df_module.prr_df.set_index(["PART_ID"], inplace=True)
        self.df_module.dtp_df.set_index(["TEST_ID", "PART_ID"], inplace=True)
        self.df_module.prr_df["DA_GROUP"] = "*"

    def calculation_top_fail(self):
        """
        1. 计算top fail
        :return:
        """
        self.top_fail_dict = CapabilityUtils.calculation_top_fail(self.df_module)

    def calculation_capability(self):
        """
        1. 计算reject rate
        2. 计算cpk等
        :return:
        """
        self.capability_key_list = CapabilityUtils.calculation_capability(self.df_module, self.top_fail_dict)
        if self.capability_key_dict is None:
            self.capability_key_dict = dict()
        else:
            self.capability_key_dict.clear()
        for each in self.capability_key_list:
            self.capability_key_dict[each["TEST_ID"]] = each

    @Time()
    def background_generation_data_use_to_chart_and_to_save_csv(self):
        """
        将数据叠起来, 用于数据可视化和导出到JMP和Altair
        :return:
        """
        if self.to_chart_csv_data is None:
            self.to_chart_csv_data = ToChartCsv()
        temp_result = self.df_module.dtp_df[["RESULT"]].unstack(0).RESULT
        self.to_chart_csv_data.df = temp_result

    def background_generation_limit_data_use_to_pat(self):
        """
        用于PAT
        需要提示建议不能在多LOT的Group条件下操作
        :return:
        """
        temp_result = self.df_module.dtp_df[["LO_LIMIT", "HI_LIMIT"]].copy()
        self.to_chart_csv_data.limit = temp_result.unstack(0)

    def set_chart_data(self, chart_df: Union[pd.DataFrame, None]):
        """
        用于pyqtgraph绘图
        :param chart_df:
        :return:
        """
        self.to_chart_csv_data.chart_df = chart_df
        if chart_df is None:
            self.select_chart()
            return
        group_data = {}
        for (group, da_group), df in self.to_chart_csv_data.chart_df.groupby(["GROUP", "DA_GROUP"]):
            key = f"{group}@{da_group}"
            group_data[key] = df
        self.to_chart_csv_data.group_chart_df = group_data
        self.select_chart()

    def set_data_group(self, group_params: Union[list, None], da_group_params: Union[list, None]):
        """
        专注将数据分组
        :param group_params:
        :param da_group_params:
        :return:
        """
        if self.select_summary is None:
            return
        if self.df_module.prr_df is None:
            return
        self.group_params, self.da_group_params = group_params, da_group_params
        if group_params is None:
            temp_column_data = '*'
        else:
            temp_column_data = None
            for index, each in enumerate(group_params):
                if index == 0:
                    temp_column_data = self.select_summary[each].astype(str)
                else:
                    temp_column_data = temp_column_data + "|" + self.select_summary[each].astype(str)

        self.select_summary.loc[:, "GROUP"] = temp_column_data
        if da_group_params is None:
            temp_column_data = '*'
        else:
            temp_column_data = None
            for index, each in enumerate(da_group_params):
                if index == 0:
                    temp_column_data = self.df_module.prr_df[each].astype(str)
                else:
                    temp_column_data = temp_column_data + "|" + self.df_module.prr_df[each].astype(str)
        self.df_module.prr_df.loc[:, "DA_GROUP"] = temp_column_data

        self.background_generation_data_use_to_chart_and_to_save_csv()
        data = pd.merge(self.to_chart_csv_data.df, self.df_module.prr_df, left_index=True, right_index=True)
        self.to_chart_csv_data.df = pd.merge(
            data, self.select_summary[["ID", "GROUP"]], on="ID"
        )

        group_data = {}
        for (group, da_group), df in self.to_chart_csv_data.df.groupby(["GROUP", "DA_GROUP"]):
            key = f"{group}@{da_group}"
            group_data[key] = df
        self.to_chart_csv_data.group_df = group_data
        self.set_chart_data(None)
        self.refresh_chart()
        return True

    def get_unstack_data_to_csv_or_jmp_or_altair(self, test_id_list: List[int]) -> (pd.DataFrame, dict):
        """
        获取选取的测试数据 -> 用于统计分析
        如果 chart_df 是None 就用 df 中的数据
        :param test_id_list:
        :return:
            1. df
            2. calculation_capability
        """
        # if not test_id_list:
        #     raise Exception("get_unstack_data_to_csv_or_jmp_or_altair must have test_id")
        if self.to_chart_csv_data.chart_df is None:
            df = self.to_chart_csv_data.df
        else:
            df = self.to_chart_csv_data.chart_df
        name_dict = {}
        calculation_capability = {}
        for test_id in test_id_list:
            row = self.capability_key_dict[test_id]
            text = str(row["TEST_NUM"]) + ":" + row["TEST_TXT"]
            name_dict[test_id] = text
            calculation_capability[text] = row
        # rename -> key_id rename text
        name_dict["index"] = "PART_ID"
        df = df[GlobalVariable.JMP_SCRIPT_HEAD + test_id_list].copy()
        # {group}@{da_group}
        df["ALL_GROUP"] = df["GROUP"] + "@" + df["DA_GROUP"]
        if self.to_chart_csv_data.select_group is not None:
            df = df[df.ALL_GROUP.isin(self.to_chart_csv_data.select_group)]
        df = df.reset_index().rename(columns=name_dict)
        return df, calculation_capability

    def get_unit_data_by_group_key(self, group_key: str, da_group_key: str) -> pd.DataFrame:
        """
        通过group_key来获取细分的unit_data prr, 用于绘图或是计算
        TODO: 禁止修改
        :param group_key:
        :param da_group_key:
        :return:
        """
        unit_summary = self.select_summary[self.select_summary.GROUP == group_key]
        unit_prr = self.df_module.prr_df[
            (self.df_module.prr_df.ID.isin(unit_summary.ID)) & (self.df_module.prr_df.DA_GROUP == da_group_key)
            ]
        return unit_prr

    def get_chart_data_by_group_key(self, group_key: str, da_group_key: str) -> pd.DataFrame:
        """
        通过group_key来获取细分的unit_data prr, 用于绘图或是计算
        TODO: 禁止修改
        :param group_key:
        :param da_group_key:
        :return:
        """
        unit_summary = self.select_summary[self.select_summary.GROUP == group_key]
        unit_prr = self.df_module.chart_prr[
            (self.df_module.chart_prr.ID.isin(unit_summary.ID)) & (self.df_module.chart_prr.DA_GROUP == da_group_key)
            ]
        return unit_prr

    @Time()
    def get_unit_data_by_test_id(self, unit_prr: pd.DataFrame, test_id: int) -> pd.DataFrame:
        """
        TODO: 根据全局唯一的TEST_ID来获取测试数据(时间过长了) 时间开销20mS
        :param unit_prr:
        :param test_id:
        :return:
        """
        unit_dtp_df = self.df_module.dtp_df.loc[test_id]
        return unit_dtp_df[unit_dtp_df.index.isin(unit_prr.index)]

    def calculation_group(self, group_params: Union[list, None], da_group_params: Union[list, None]):
        """
        分组的制程能力报表
        TODO: future
        :param group_params:
        :param da_group_params:
        :return:
        """

    def update_limit(self, limit_new: Dict[int, Tuple[float, float, str, str]], only_pass: bool = False) -> bool:
        """
        更新Limit并重新计算良率
        TODO: future
        :param limit_new:
        :param only_pass:
        :return:
        """

    def calculation_new_limit(self):
        """
        计算新Limit的制程能力
        TODO: future
        :return:
        """

    def screen_df(self, test_ids: List[int]):
        """
        只看选取的项目 ->TEST_ID isin 即可
        筛选: 底层数据也改为NewData, 数据拆除
        TODO: future
        """

    def drop_data_by_select_limit(self, func: str, limit_new: Dict[str, Tuple[float, float]]) -> bool:
        """
        将选取测试项目limit内的数据删掉, 或是将limit外的数据删掉
        TODO: future
        :param func: Union[inner,outer]
        :param limit_new:
        :return:
        """

    def verify_pass_have_nan(self) -> bool:
        """ PASS的数据中含有空值! 不被允许, 检测的时候要定位到ID, 用来检测程序错误的 """

    def verify_test_no_repetition(self) -> bool:
        """ 除了MPR外有重复的TEST_NO! 检测的时候要定位到ID, 用来检测程序不标准的 """

    def show_limit_diff(self):
        """
        显示导入的STDF见Limit之间的差异
        :return:
        """
        if self.df_module is None:
            return self.QStatusMessage.emit("请先将数据载入到数据空间中!")
        # TODO:使用多进程后台处理(多进程可以实时修改代码,较为方便)
        p = Process(target=OpenXl.excel_limit_run, kwargs={
            'summary_df': self.select_summary,
            "limit_df": self.df_module.ptmd_df,
        })
        p.start()
        # OpenXl.excel_limit_run(self.select_summary, self.df_module.ptmd_df)

    def get_text_by_test_id(self, test_id:int):
        row = self.capability_key_dict[test_id]
        return str(row["TEST_NUM"]) + ":" + row["TEST_TXT"]

    def update(self):
        """
        主要是可以更新Table界面上的制程能力报告, 比如limit更新后重新计算
        :return:
        """
        print("update all QCalculation @emit")
        self.QCalculation.emit()

    def select_chart(self):
        """
        主要是用来选取绘图的数据, 在数据还是处于当前分组的一个状态下
        :return:
        """
        print("select_chart QChartSelect @emit")
        self.QChartSelect.emit()

    def refresh_chart(self):
        """
        这个主要是数据有突然的变化, 比如分组改变了, 触发这个后把绘图的数据刷新重新绘图, 不Select
        :return:
        """
        print("refresh_chart QChartRefresh @emit")
        self.QChartRefresh.emit()
