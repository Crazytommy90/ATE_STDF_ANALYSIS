#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : my_text_browser.py
@Author  : Link
@Time    : 2022/10/22 20:55
@Mark    : 
"""
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QTextBrowser

import datetime as dt


class Print:
    INFO = "00"
    ERROR = "01"
    WARNING = "02"
    DEBUG = "03"

    @staticmethod
    def info(text: str):
        print("{}:==={}==={}".format(Print.INFO, dt.datetime.now().strftime("%H:%M:%S"), text))

    @staticmethod
    def error(text: str):
        print("{}:==={}==={}".format(Print.ERROR, dt.datetime.now().strftime("%H:%M:%S"), text))

    @staticmethod
    def warning(text: str):
        print("{}:==={}==={}".format(Print.WARNING, dt.datetime.now().strftime("%H:%M:%S"), text))

    @staticmethod
    def debug(text: str):
        print("{}:==={}==={}".format(Print.DEBUG, dt.datetime.now().strftime("%H:%M:%S"), text))


class UiMessage:
    code: str = "00"
    string: str = ""
    dut: int = 0
    color = "#000000"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if self.code == Print.ERROR:
            self.color = "#FF0000"
            return
        if self.code == Print.WARNING:
            self.color = "#AFAF00"
            return
        if self.code == Print.DEBUG:
            self.color = "#0000FF"
            return

    @staticmethod
    def info(text: str, dut: int = 0):
        return UiMessage(code=Print.INFO, dut=dut, string=text)

    @staticmethod
    def error(text: str, dut: int = 0):
        return UiMessage(code=Print.ERROR, dut=dut, string=text)

    @staticmethod
    def warning(text: str, dut: int = 0):
        return UiMessage(code=Print.WARNING, dut=dut, string=text)

    @staticmethod
    def debug(text: str, dut: int = 0):
        return UiMessage(code=Print.DEBUG, dut=dut, string=text)


class MQTextBrowser(QTextBrowser):
    skip_output = {'\n'}

    def __init__(self, parent=None):
        super(MQTextBrowser, self).__init__(parent)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setLineWrapMode(MQTextBrowser.NoWrap)
        self.setUndoRedoEnabled(True)

    def split_append(self, text: str):
        if text in self.skip_output:
            return
        text_split = text.split(':', 1)
        if len(text_split) == 1:
            string = text_split[0]
            self.append(string)
            return
        code, string = text_split
        mes = UiMessage(code=code, string=string)
        self.m_append(mes)

    def m_append(self, mes: UiMessage):
        string = "<font color=\"{}\">{}</font>".format(mes.color, mes.string)
        self.append(string)
