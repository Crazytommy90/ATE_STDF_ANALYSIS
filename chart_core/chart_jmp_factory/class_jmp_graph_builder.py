#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : class_jmp_graph_builder.py
@Author  : Link
@Time    : 2022/10/7 12:03
@Mark    : 
"""


class JmpGraphBuilder:
    """
    横向分布图
    """
    def __str__(self):
        return self.execute()

    def __repr__(self):
        return self.execute()

    def __init__(self):
        self.config = ""
        self.dispatch = ""

    def set_config(self, *strings):
        """
        // Size( 1085, 320 ),
        // Show Control Panel( 0 ),
        // Legend Position( "Inside Right" ),
        // Variables( Group X( :"GROUP" ), Overlay( :GROUP ), X( :"DA_GROUP" ), Y( :"1:OS_PID_SEL" ) ),
        // Elements( Histogram( X, Y, Legend( 5 ) ) ),
        """
        self.config += ", ".join(strings)

    def new_dispatch(self, *strings):
        """
        // Dispatch(
        //     , "2:OS_USID_SEL", ScaleBox,
        //     {Format( "Fixed Dec", 12, 5 ), Min( -1.075 ), Max( -0.025000000000000022 ), Inc( 0.02333333333333333 ), Minor Ticks( 0 ),
        //     Add Ref Line( -0.9, "Solid", "Medium Dark Red", "下限值(-0.9)", 1 ), Add Ref Line( -0.2, "Solid", "Dark Red", "上限值(-0.2)", 1 ),
        //     Add Ref Line( -0.76154, "Solid", "Medium Dark Blue", "良品均值(-0.76154)", 1 )}
        // )
        :param strings:
        :return:
        """
        self.dispatch += ", ".join(strings) + ", "

    def execute(self):
        return """
        Graph Builder(
            {config},
            
            SendToReport(
                {dispatch}
            )
        )
        """.format(
            config=self.config, dispatch=self.dispatch
        )

