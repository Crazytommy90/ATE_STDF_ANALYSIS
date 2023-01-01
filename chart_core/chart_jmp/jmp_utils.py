#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : jmp_utils.py
@Author  : Link
@Time    : 2022/3/27 17:37
@Mark    : 
"""


class JmpUtils:

    @staticmethod
    def send_to_report(*dispatch_args: str) -> str:
        return f"""
        SendToReport(\n{",".join(dispatch_args)}\n)
        """

    @staticmethod
    def outline_box_dis(title: str = "ALL") -> str:
        return f"""
        Dispatch( , "Distributions", OutlineBox, {{Set Title( "{title}" )}} )
        """

    @staticmethod
    def outline_box_gp(title: str = "ALL") -> str:
        return f"""
        Dispatch( , "Graph Builder", OutlineBox, {{Set Title( "{title}" ), Image Export Display( "正常" )}} )
        """

    @staticmethod
    def add_data_filter():
        return """
        Current Data Table() << Data Filter(
        Location( {279, 52} ),
            Add Filter(
                columns( :GROUP, :DA_GROUP, :HARD_BIN, :SOFT_BIN ),
                Display( :GROUP, N Items( 6 ) ),
                Display( :DA_GROUP, N Items( 6 ) ),
                Display( :HARD_BIN, N Items( 6 ) ),
                Display( :SOFT_BIN, N Items( 6 ) ),
            )
        );
        """

