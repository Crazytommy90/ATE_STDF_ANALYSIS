#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : class_jmp_distribution.py
@Author  : Link
@Time    : 2022/10/6 22:13
@Mark    : Jmp分布图
"""
from chart_core.chart_jmp.jmp_file import JmpFile
from chart_core.chart_jmp.jmp_script_factory import JmpScript


class JmpDistribution:
    """
    分布图
    """

    def __str__(self):
        return self.execute()

    def __repr__(self):
        return self.execute()

    def __init__(self):
        self.config = ""
        self.continuous_distribution = ""
        self.dispatch = ""

    def set_config(self, *strings):
        """
        // By( {':GROUP' if group else ''} ),
        // Stack( 1 ),
        // Automatic Recalc( 1 ),
        // Arrange in Rows( {col} ),
        // {",".join(continuous_dis)}
        """
        self.config += ", ".join(strings)

    def new_continuous_distribution(self, *strings):
        """
        // Column( :"4:OS_SDATA"  ),
        // Horizontal Layout( 1 ),
        // Vertical( 0 ), Outlier Box Plot( 0 ),
        // Capability Analysis( LSL( -0.9 ), USL( -0.2 ) )
        :param strings:
        :return:
        """
        self.continuous_distribution += """
        Continuous Distribution(
            {continuous_distribution}
        ),
        """.format(continuous_distribution=", ".join(strings))

    def new_dispatch(self, *strings):
        """
        // Dispatch(
        //     { :"2:OS_USID_SEL", , "Capability Analysis" },
        //     "长期 Sigma",
        //     OutlineBox,
        //     { Close( 1 ) }
        // )
        :param strings:
        :return:
        """
        self.dispatch += ", ".join(strings) + ", "

    def execute(self):
        return """
        Distribution(
            {config},
            {continuous_distribution},
            SendToReport(
                {dispatch}
            )
        )
        """.format(
            config=self.config, continuous_distribution=self.continuous_distribution, dispatch=self.dispatch
        )
