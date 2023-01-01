#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : jmp_file.py
@Author  : Link
@Time    : 2022/3/27 17:04
@Mark    : 
"""
import win32api


class JmpFile:
    """
    JMP的文件操作接口
    """

    @staticmethod
    def save_with_run_script(jmp_script, scrip_name="stdf_script.jsl"):
        with open(scrip_name, "w", encoding="utf-8") as f:
            f.write(jmp_script)
        win32api.ShellExecute(0, 'open', scrip_name, '', '', 1)

    @staticmethod
    def load_csv_file(filepath: str):
        """
        读取文件的时候要加入归规格限
        :param filepath:
        :return:
        """
        return """
        Open(
            "{filepath}",
            Import Settings(
                End Of Line( CRLF, CR, LF ),
                End Of Field( Comma, CSV( 1 ) ),
                Strip Quotes( 0 ),
                Use Apostrophe as Quotation Mark( 0 ),
                Use Regional Settings( 0 ),
                Scan Whole File( 1 ),
                Treat empty columns as numeric( 0 ),
                CompressNumericColumns( 0 ),
                CompressCharacterColumns( 0 ),
                CompressAllowListCheck( 0 ),
                Labels( 1 ),
                Column Names Start( 1 ),
                Data Starts( 2 ),
                Lines To Read( "All" ),
                Year Rule( "20xx" )
            )
        );
        Column("HARD_BIN") << Data Type(Character) << Set Modeling Type(Nominal);
        Column("SOFT_BIN") << Data Type(Character) << Set Modeling Type(Nominal);
        """.format(filepath=filepath)

    @staticmethod
    def load_csv_add_specification():
        pass
