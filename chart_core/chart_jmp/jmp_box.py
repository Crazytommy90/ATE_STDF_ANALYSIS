#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : jmp_box.py
@Author  : Link
@Time    : 2022/3/27 17:37
@Mark    :
"""


class JmpBox:
    """
    JMP Window,Box
    """

    @staticmethod
    def new_window(*boxes: str, title: str = "Window") -> str:
        return """
        New Window( "{title}",
        {boxes}
        )
        """.format(title=title, boxes=",".join(boxes))

    @staticmethod
    def new_outline_box(*boxes: str, title: str = "Table") -> str:
        return """
        Outline Box( "{title}",
        {boxes}
        )
        """.format(title=title, boxes=",".join(boxes))

    @staticmethod
    def new_v_list_box(*graph_builders) -> str:
        return """
        V List Box(
            {graphs}
        )
        """.format(graphs=";".join(graph_builders))

    @staticmethod
    def new_h_list_box(*graph_builders) -> str:
        return """
        H List Box(
            {graphs}
        )
        """.format(graphs=";".join(graph_builders))

    @staticmethod
    def new_group_box(*graph_builders: str, col: int = 2, title: str = "Table") -> str:
        """
        return: new_outline_box
        """
        temp_h = []
        boxes = []
        for index, arg in enumerate(graph_builders):
            temp_h.append(arg)
            if (index + 1) % col == 0:
                boxes.append(JmpBox.new_h_list_box(*temp_h))
                temp_h.clear()
        return JmpBox.new_outline_box(*boxes, title=title)

    @staticmethod
    def new_group_item(*graph_builders: str, col: int = 2) -> list:
        """
        return: new_outline_box
        """
        temp_h = []
        boxes = []
        for index, arg in enumerate(graph_builders):
            temp_h.append(arg)
            if (index + 1) % col == 0:
                boxes.append(JmpBox.new_h_list_box(*temp_h))
                temp_h.clear()
        return boxes
