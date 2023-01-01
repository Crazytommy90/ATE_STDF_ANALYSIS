#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : jmp_factory.py
@Author  : Link
@Time    : 2022/6/4 18:13
@Mark    : 
"""

from chart_core.chart_jmp.jmp_box import JmpBox
from chart_core.chart_jmp.jmp_fit import JmpFit
from chart_core.chart_jmp.jmp_plot import JmpPlot
from chart_core.chart_jmp.jmp_utils import JmpUtils
from chart_core.chart_jmp_factory.class_jmp_factory import NewJmpFactory
from ui_component.ui_app_variable import UiGlobalVariable


class JmpFactory:
    item_dict = {
        0: "distribution_bar",
        1: "distribution_trans_bar",
        2: "comparing",
        3: "scatter",
        4: "scatter_box",
        5: "scatter_line",
        6: "bin_mapping",
        7: "bin_mapping",
        8: "bin_mapping",
        9: "heatmap_visual_map",
        10: "points_visual_map",
        11: "add_data_filter",
    }

    @staticmethod
    def distribution_bar(calculation_capability: dict, title="数据分布图", **kwa) -> str:
        return NewJmpFactory.jmp_distribution(
            capability=calculation_capability, title=title
        )

    @staticmethod
    def distribution_trans_bar(calculation_capability: dict, title="横向分布图", **kwa) -> str:
        return NewJmpFactory.jmp_distribution_trans_bar(
            capability=calculation_capability, title=title
        )

    @staticmethod
    def comparing(calculation_capability: dict, title: str = "比较密度图", **kwa) -> str:
        jmp_script = JmpFit.fit_group(
            *[JmpFit.one_way(arg, JmpUtils.send_to_report(
                JmpFit.fill_color_dis(),
                JmpFit.limit_color_dis(arg)))
              for arg in calculation_capability.values()]
        )
        return jmp_script

    @staticmethod
    def scatter(calculation_capability: dict, title: str = "散点图", **kwa) -> str:
        jmp_script = JmpBox.new_window(JmpBox.new_outline_box(*JmpBox.new_group_item(
            *[JmpPlot.trans_scatter(arg, JmpUtils.send_to_report(
                JmpPlot.trans_scale_dis(arg)))
              for arg in calculation_capability.values()], col=UiGlobalVariable.JmpPlotColumn
        ), title=title))
        return jmp_script

    @staticmethod
    def scatter_box(calculation_capability: dict, title: str = "箱线图(点型)", **kwa) -> str:
        jmp_script = JmpBox.new_window(JmpBox.new_outline_box(*JmpBox.new_group_item(
            *[JmpPlot.trans_box_point(arg, JmpUtils.send_to_report(
                JmpPlot.trans_scale_dis(arg)))
              for arg in calculation_capability.values()], col=UiGlobalVariable.JmpPlotColumn
        ), title=title))
        return jmp_script

    @staticmethod
    def scatter_line(calculation_capability: dict, title: str = "箱线图(线型)", **kwa) -> str:
        jmp_script = JmpBox.new_window(JmpBox.new_outline_box(*JmpBox.new_group_item(
            *[JmpPlot.trans_box(arg, JmpUtils.send_to_report(JmpPlot.trans_scale_dis(arg)))
              for arg in calculation_capability.values()], col=UiGlobalVariable.JmpPlotColumn
        ), title=title))
        return jmp_script

    @staticmethod
    def bin_mapping(calculation_capability: dict, title: str = "Mapping", **kwa) -> str:
        jmp_df = kwa["jmp_df"]
        bin_head = kwa["bin_head"]
        bins = jmp_df[bin_head].drop_duplicates().tolist()
        jmp_script = JmpBox.new_window(JmpBox.new_outline_box(*JmpBox.new_group_item(
            JmpPlot.bin_mapping(bin_head, len(bins), JmpUtils.send_to_report(
                JmpPlot.bin_scale_dis(bins, jmp_df["Y_COORD"].min(), jmp_df["Y_COORD"].max())
            )), col=UiGlobalVariable.JmpPlotColumn
        ), title=bin_head))
        return jmp_script

    @staticmethod
    def heatmap_visual_map(calculation_capability: dict, title: str = "Visual Mapping", **kwa) -> str:
        jmp_df = kwa["jmp_df"]
        y_max = jmp_df["Y_COORD"].max()
        y_min = jmp_df["Y_COORD"].min() - 1
        x_max = jmp_df["X_COORD"].max()
        x_min = jmp_df["X_COORD"].min()
        percent = (y_max - y_min) / (x_max - x_min)
        jmp_script = JmpBox.new_window(
            JmpBox.new_outline_box(
                *JmpBox.new_group_item(
                    *[JmpPlot.trans_visual_heatmap(arg,
                                                   True,
                                                   JmpUtils.send_to_report(JmpPlot.visual_dis(arg, y_max, y_min)),
                                                   percent)
                      for arg in calculation_capability.values()],
                    col=UiGlobalVariable.JmpPlotColumn), title=title))
        return jmp_script

    @staticmethod
    def points_visual_map(calculation_capability, title: str = "Visual Mapping", **kwa) -> str:
        jmp_df = kwa["jmp_df"]
        y_max = jmp_df["Y_COORD"].max()
        y_min = jmp_df["Y_COORD"].min() - 1
        x_max = jmp_df["X_COORD"].max()
        x_min = jmp_df["X_COORD"].min()
        percent = (y_max - y_min) / (x_max - x_min)
        jmp_script = JmpBox.new_window(
            JmpBox.new_outline_box(
                *JmpBox.new_group_item(
                    *[JmpPlot.trans_visual_points(arg,
                                                   True,
                                                   JmpUtils.send_to_report(JmpPlot.visual_dis(arg, y_max, y_min)),
                                                   percent)
                      for arg in calculation_capability.values()],
                    col=UiGlobalVariable.JmpPlotColumn), title=title))
        return jmp_script

    @staticmethod
    def add_data_filter(kwargs: dict, title: str = "Visual Mapping", **kwa) -> str:
        return JmpUtils.add_data_filter()
