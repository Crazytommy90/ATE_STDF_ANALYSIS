#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : stdf_parser_func.py
@Author  : Link
@Time    : 2022/12/18 23:09
@Mark    : 
"""


class PrrPartFlag:
    FirstTest = 0b1 << 1


class DtpTestFlag:
    TestFailed = 0b1 << 7

    @staticmethod
    def test_failed(TEST_FLG):
        return TEST_FLG & DtpTestFlag.TestFailed


class DtpOptFlag:
    PatValid = 0b1 << 1

    @staticmethod
    def unknown_must_1(OPT_FLAG):
        return OPT_FLAG & DtpOptFlag.PatValid


class DtpParmFlag:
    pass


class PtmdParmFlag:
    EqualLowLimit = 0b1 << 6
    EqualHighLimit = 0b1 << 7
    ThenLowLimit = 0b0 << 6
    ThenHighLimit = 0b0 << 7

    @staticmethod
    def equal_low_limit_pass(PARM_FLG):
        return PARM_FLG & PtmdParmFlag.EqualLowLimit

    @staticmethod
    def equal_high_limit_pass(PARM_FLG):
        return PARM_FLG & PtmdParmFlag.EqualHighLimit

    @staticmethod
    def set_equal_low_limit_pass(PARM_FLG, boolean: bool):
        if boolean:
            return PARM_FLG | PtmdParmFlag.EqualLowLimit if boolean else PtmdParmFlag.ThenLowLimit
        else:
            return PARM_FLG & ~(PtmdParmFlag.EqualLowLimit if boolean else PtmdParmFlag.ThenLowLimit)

    @staticmethod
    def set_equal_high_limit_pass(PARM_FLG, boolean: bool):
        if boolean:
            return PARM_FLG | PtmdParmFlag.EqualHighLimit if boolean else PtmdParmFlag.ThenHighLimit
        else:
            return PARM_FLG & ~(PtmdParmFlag.EqualHighLimit if boolean else PtmdParmFlag.ThenHighLimit)


class PtmdOptFlag:
    NoLowLimit = 0b1 << 6
    NoHighLimit = 0b1 << 7

    LowLimit = 0b0 << 6
    HighLimit = 0b0 << 7

    @staticmethod
    def no_low_limit(OPT_FLAG):
        return OPT_FLAG & PtmdOptFlag.NoLowLimit

    @staticmethod
    def no_high_limit(OPT_FLAG):
        return OPT_FLAG & PtmdOptFlag.NoHighLimit

    @staticmethod
    def set_no_low_limit(PARM_FLG, boolean: bool):
        if boolean:
            return PARM_FLG | PtmdOptFlag.NoLowLimit if boolean else PtmdOptFlag.LowLimit
        else:
            return PARM_FLG & ~(PtmdOptFlag.NoLowLimit if boolean else PtmdOptFlag.LowLimit)

    @staticmethod
    def set_no_high_limit(PARM_FLG, boolean: bool):
        if boolean:
            return PARM_FLG | PtmdOptFlag.NoHighLimit if boolean else PtmdOptFlag.HighLimit
        else:
            return PARM_FLG & ~(PtmdOptFlag.NoHighLimit if boolean else PtmdOptFlag.HighLimit)
