#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : jmp_script_factory.py
@Author  : Link
@Time    : 2022/3/27 16:50
@Mark    : 集合类
"""


class JmpScript:

    def __init__(self):
        pass

    @staticmethod
    def factory(*args: str):
        return ";\n".join(args)
