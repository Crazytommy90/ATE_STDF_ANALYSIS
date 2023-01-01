"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/5/23 15:46
@Software: PyCharm
@File    : data_create_interface.py
@Remark  :
"""
from Semi_ATE import STDF

from common.stdf_interface.stdf_def_interface import Mir, Wir, STDF_FLAG, Pir, STDF_TYPE, Mrr


class StdfWrite:

    def __call__(self, func):
        def wrapper(ctx, *args, **kwargs):
            if ctx.f is None:
                return None
            return func(ctx, *args, **kwargs)

        return wrapper


class StdfSystem:
    have_data = False
    f = None
    save_path = None

    def open(self, path: str):
        if self.f is not None:
            raise Exception("f Have Been Opened")
        self.have_data = False
        self.save_path = path
        self.f = open(path, mode="wb")

    def save(self):
        if self.f is None:
            raise Exception("Error Open Fail")
        self.f.close()
        self.f = None

    @StdfWrite()
    def far(self):
        record = STDF.FAR()
        self.f.write(record.__repr__())

    @StdfWrite()
    def atr(self, cmd_line='SAVE AS WITH PYTHON STDF CONVERT'):
        record = STDF.ATR()
        record.set_value('CMD_LINE', cmd_line)
        self.f.write(record.__repr__())

    @StdfWrite()
    def mir(self, mir: Mir):
        record = STDF.MIR()
        for each in filter(lambda m: not m.startswith('__') and not callable(getattr(mir, m)), dir(mir)):
            data = getattr(mir, each)
            if isinstance(data, STDF_FLAG):
                data = data.u8
            record.set_value(each, data)
        self.f.write(record.__repr__())

    @StdfWrite()
    def wir(self, wir: Wir):
        record = STDF.WIR()
        for each in filter(lambda m: not m.startswith('__') and not callable(getattr(wir, m)), dir(wir)):
            data = getattr(wir, each)
            if isinstance(data, STDF_FLAG):
                data = data.u8
            record.set_value(each, data)
        self.f.write(record.__repr__())

    @StdfWrite()
    def pir(self, pir: Pir):
        self.have_data = True
        record = STDF.PIR()
        record.set_value("HEAD_NUM", pir.HEAD_NUM)
        record.set_value("SITE_NUM", pir.SITE_NUM)
        self.f.write(record.__repr__())

    @StdfWrite()
    def ptr(self, ptr: STDF_TYPE):
        record = STDF.PTR()
        for each in filter(lambda m: not m.startswith('__') and not callable(getattr(ptr, m)), dir(ptr)):
            data = getattr(ptr, each)
            if isinstance(data, STDF_FLAG):
                data = data.u8
            record.set_value(each, data)

        self.f.write(record.__repr__())

    @StdfWrite()
    def prr(self, prr: STDF_TYPE):
        record = STDF.PRR()
        for each in filter(lambda m: not m.startswith('__') and not callable(getattr(prr, m)), dir(prr)):
            data = getattr(prr, each)
            if isinstance(data, STDF_FLAG):
                data = data.u8
            record.set_value(each, data)
        self.f.write(record.__repr__())

    @StdfWrite()
    def mrr(self, mrr: Mrr):
        record = STDF.MRR()
        record.set_value("FINISH_T", mrr.FINISH_T)
        self.f.write(record.__repr__())
