#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : pandas_sql.py
@Author  : Link
@Time    : 2022/12/23 23:52
@Mark    : 用来缓存解析的文件记录的
         @BAT: SQL的坏处, 会改动的人很少. 考虑还是使用csv作为SQL存档
"""
import sqlite3
from typing import Union

from common.app_variable import GlobalVariable
from pandas import DataFrame
from sqlalchemy import create_engine


class SqlEngine:
    """
    存数据
    """

    def __init__(self):
        self.engine = create_engine(
            "sqlite:///{}?check_same_thread=False".format(GlobalVariable.SQLITE_PATH), echo=True
        )

    def insert_into_sql_by_table_name(self, df: DataFrame, table_name: str):
        table_name = table_name.lower()
        with self.engine.begin() as conn:
            df.to_sql(table_name, conn, index=False, if_exists='append', chunksize=1000)


class SqlLite:

    @staticmethod
    def dict_factory(cursor, row):
        # 将游标获取的数据处理成字典返回
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def connect():
        # 建立和数据库sample.db的连接
        conn = sqlite3.connect(GlobalVariable.SQLITE_PATH)
        # 使得查询结果以字典形式返回
        conn.row_factory = SqlLite.dict_factory
        # 创建游标以用于执行sql
        cursor = conn.cursor()
        return conn, cursor

    def exe_sql(self, sql, **kwargs) -> bool:
        conn, cursor = self.connect()
        try:
            # 可以执行多条语句
            # cursor.executescript(sql, **kwargs)
            # 只能执行一条语句
            cursor.execute(sql, **kwargs)
        except Exception as e:
            print('execute sql exception: ', e)
            return False
        finally:
            cursor.close()
            conn.close()
        return True

    def get_all(self, sql, **kwargs):
        conn, cursor = self.connect()
        try:
            cursor.execute(sql, **kwargs)
            datasets = cursor.fetchall()
            return datasets
        except Exception as e:
            print('get all exception: ', e)
        finally:
            cursor.close()
            conn.close()

    def select(self, table: str, end=None, *select, **where):
        sql = "select %s from %s where %s "
        if end:
            sql += end
        selects = ','.join(select)
        wheres = ' and '.join(["%s=%%(%s)s" % (key, key) for key in where])
        return self.get_all(sql % (selects, table, wheres), **where)

    def get_one(self, sql, **kwargs):
        """

        :param sql:
        :return:
        """
        conn, cursor = self.connect()
        try:
            cursor.execute(sql, **kwargs)
            res = cursor.fetchone()
            return res
        except Exception as e:
            print('get one exception: ', e)
        finally:
            cursor.close()
            conn.close()

    def select_one_or_none(self, table: str, end=None, *select, **where) -> Union[dict, None]:
        """
        只返回一个结果或是None
        """
        sql = "select %s from %s where %s "
        if end:
            sql += end
        selects = ','.join(select)
        wheres = ' and '.join(["%s=%%(%s)s" % (key, key) for key in where])
        result = self.get_one(sql % (selects, table, wheres), **where)
        return result

    def update(self, table: str, where: dict, **kwargs) -> bool:
        """
        这种写法 where 中 不能有和 data一样的key 然后value又不一样的
        所以以id为where比较好用 id是唯一不可改变的
        """
        sql = "update %s set %s where %s"
        update_cols = ','.join(["%s=%%(%s)s" % (key, key) for key in kwargs])
        wheres = ' and '.join(["%s=%%(%s)s" % (key, key) for key in where])
        return self.exe_sql(sql % (table, update_cols, wheres), **{**kwargs, **where})
