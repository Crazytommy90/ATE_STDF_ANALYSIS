#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : stdf_data_tuples.py
@Author  : Link
@Time    : 2022/6/17 11:20
@Mark    : 
"""
import collections

PtrTuple = collections.namedtuple("LimitTuple",
                                  [
                                      "TEST_NUM",
                                      "TEST_TXT",
                                      "L_LIMIT",
                                      "H_LIMIT",
                                      "UNITS",
                                      "LO_LIMIT_TYPE",
                                      "HI_LIMIT_TYPE",
                                      "SOFT_BIN",
                                      "SOFT_BIN_NAME",
                                      "HARD_BIN",
                                      "HARD_BIN_NAME",
                                  ]
                                  )

FtrTuple = collections.namedtuple("LimitTuple",
                                  [
                                      "TEST_NUM",
                                      "TEST_TXT",
                                      "SOFT_BIN",
                                      "SOFT_BIN_NAME",
                                      "HARD_BIN",
                                      "HARD_BIN_NAME",
                                  ]
                                  )
