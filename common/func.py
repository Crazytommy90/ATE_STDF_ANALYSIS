#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : func.py
@Author  : Link
@Time    : 2022/5/1 23:41
@Mark    : 
"""
import datetime
import json
import os
import pickle
import random
from typing import Union

import pandas as pd
from ui_component.ui_common.my_text_browser import Print

from threading import Lock
lock = Lock()

PART_ID_ADD = 0


def get_part_id_add():
    """
    TODO: > 0xFFFFFF
    :return:
    """
    with lock:
        global PART_ID_ADD
        PART_ID_ADD += 1
        return PART_ID_ADD << 24


def qt_catch_except(func):
    """

    :param func:
    :return:
    """

    def wrapper(ctx, *args, **kwargs):
        try:
            ctx.statusbar.clearMessage()
            return func(ctx, *args, **kwargs)
        except Exception as error:
            Print.error('errorfunc: %s' % func.__name__ + f' 报错信息: {error}')
            ctx.enabled_push_button(True)

    return wrapper


def catch_except(func):
    def wrapper(ctx, *args, **kwargs):
        try:
            return func(ctx, *args, **kwargs)
        except Exception as error:
            Print.error('errorfunc: %s' % func.__name__ + f' 报错信息: {error}')

    return wrapper


def tid_maker():
    """
    生成唯一ID
    :return:
    """
    key_str = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join(
        [str(random.randint(0, 9)) for _ in range(5)])
    return key_str[:20]


def timestamp_to_str(timestamp: int) -> str:
    if timestamp is None:
        return "NULL"
    date_array = datetime.datetime.utcfromtimestamp(timestamp)
    return date_array.strftime("%Y-%m-%d %H:%M:%S")


def get_now_timestamp():
    return int(int(datetime.datetime.now().timestamp()))


def json_dump_to_file(data, file_name, suffix='.json', json_encoder=None):
    """
    用于将数据 保存在json文件中, 用于调试
    :param suffix:
    :param file_name:保存的文件名
    :param data:保存的数据帧
    :param json_encoder:
    :return:
    """
    file_path = os.path.join('cache_test_data', file_name + suffix)
    with open(file_path, 'w') as file_obj:
        if json_encoder:
            json.dump(data, file_obj, cls=json_encoder)
        else:
            json.dump(data, file_obj)


def save_df_to_json(data: pd.DataFrame, save_path: str, file_name: str, suffix='.json'):
    file_path = os.path.join('cache_test_data', save_path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    full_path = os.path.join(file_path, file_name + suffix)
    data.to_json(full_path)


def get_df_by_json(save_path: str, file_name: str, suffix='.json') -> Union[pd.DataFrame, None]:
    file_path = os.path.join('cache_test_data', f'{save_path}/{file_name}{suffix}')
    if not os.path.exists(file_path):
        return None
    return pd.read_json(file_path)


def save_obj_to_pickle(data, save_path: str, file_name: str, suffix='.pkl'):
    file_path = os.path.join('cache_test_data', save_path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    full_path = os.path.join(file_path, file_name + suffix)
    with open(full_path, 'wb') as file_obj:
        data_pik = pickle.dumps(data)
        file_obj.write(data_pik)


def get_obj_by_pickle(save_path: str, file_name: str, suffix='.pkl') -> Union[object, None]:
    file_path = os.path.join('cache_test_data', f'{save_path}/{file_name}{suffix}')
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'rb') as file:
        li = pickle.loads(file.read())
    return li
