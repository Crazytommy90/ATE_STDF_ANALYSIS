#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : sync_semi_field.py
@Author  : Link
@Time    : 2022/12/16 22:47
@Mark    : 
"""

from Semi_ATE import STDF

import pandas as pd

cols = ["ATR", "BPS", "DTR", "EPS", "FAR", "FTR", "GDR", "HBR", "MIR", "MPR", "MRR", "PCR", "PGR", "PIR", "PLR", "PMR",
        "PRR", "PTR", "RDR", "SBR", "SDR", "TSR", "WCR", "WIR", "WRR", "CDR", "CNR", "PSR", "NMR", "SSR", "STR", "VUR"]

if __name__ == '__main__':
    record = []
    for col in cols:
        temp = getattr(STDF, col)
        temp_record: dict = temp().fields
        for key, item in temp_record.items():
            keys = ["TYPE", "KEY"]
            values = [col, key]
            for item_key, item_item in item.items():
                keys.append(item_key)
                values.append(item_item)
            record.append(
                dict(zip(keys, values))
            )
    df = pd.DataFrame(record)
    df.to_csv("synchronization.csv", index=False)
