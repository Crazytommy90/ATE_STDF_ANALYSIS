#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : app.py
@Author  : Link
@Time    : 2020/07/16 21:24
@Mark    :
@Version : V3.0
@START_T : 20200814
@UPDATE_T: 20221224
@RELEASE :


Update Record
    Demo:
        @RELEASE: 2018
            :base
                PyQt5
                QtChart
                Pandas
                stdfExtractor
                Excel Vba
                Matplotlib
            :succeed
                基于调用stdfExtractor二次开发
                成功开启了测试数据持久化的大门
                成功开启将所有的测试数据和测试框架转为STDF存储的大门
                虽然很Low,但是非常Nice (๑•̀ㅂ•́)و✧
    V0.X:
        @RELEASE: 2019
            :base
                Pandas
                PyStdf
                stdfExtractor
                PyqtGraph
                Matplotlib
                PyQt5

                Echarts
                Flask
                Vue-element
                SqlServer
            :except
                可视化单元过于单一,无法链接分析
                解析速度过慢->stdfExtractor对于超过300M的数据支持度不够,大的数据PyStdf过于慢
                数据存入SQL中过于占用空间
                前后端分离开发过于复杂
                过多的前端模块根本无人愿意操作维护
                    example: ftp配置, mir解析规则, cp/ft/wat数据整合, finally data之类

    V1.X:
        @RELEASE: 2020
            :base
                Pandas
                Cpp-Stdf
                Echarts
                Flask
                Vue-element
                SqlServer
                Redis
            :succeed
                彻底删除了Desktop软件, 所有数据都由后台处理, 保证报告数据真实
                数据解析完整
                2022年也同样在稳定运行
            :except
                可视化单元过于单一,无法链接分析
                数据存入SQL中过于占用空间, 硬件成本较高
                前后端分离开发过于复杂
                和MES过于耦合,迁移至Superset框架失败, 继续使用传统Web开发模式


    V2.X:
        @RELEASE: 2021
            :base
                Pandas
                Cpp-Stdf
                PyQt5
                PyqtGraph
                Matplotlib
                JMP

                Flask
                SqlServer
                Redis
            :except
                对数据的修改过于容易, 报告都太漂亮
                plot太容易修饰
                框架一开始就放弃了PAT
                数据格式按照调研基本定死
                升级困难
                虽然后来有限制,但是APP不可避免被传播
            :succeed
                开发到使用时间短, 比从市场购买系统部署更快
                工程师极其易用, 经过多位TE和ATE,QA评估
                探索性可视化
                全面放弃前端Web, 稳定的, 适合设计公司
                解析速度极快, 2G -> 50s
                超过40亿颗数据被Server成功解析(大头都在硬盘(5W), 硬件成本不超过8W)
                HDF5用于存放RawData,SqlServer用于存放summary,prr等
                数据结构易处理, 易于开发后台分析和监控脚本
                解决了WAT数据和CP数据链接困难的问题, 无需请Fab提供坐标对应关系
                硬件的配置和维护成本极低
                大数据统计分析与良率预测

     V3.X:
        @RELEASE: None
        @START_T: 2022
            :base
                Semi-Ate-Stdf
                Pandas
                Cpp-Stdf
                PySide2
                PyqtGraph
                JMP
                Altair

                # fast-api
                # PostgreSQL
                # Redis
            :except
                调试阶段还是使用csv作为数据存储的方案
                不保证解析速度
                解析STDF结构简单, 上层结构复杂了, 而且速度慢了很多···
            :hope
                准确/通用的
                随意传播
                简单且好用
                单元测试覆盖
                性能和内存占用平衡
            :remark
                OpenSource
            :future
                数据解析结构定下来后通过pybind11使用numpy和C++交互(用C++保存为HDF5更好, 不过流式写入还没研究透彻)
                继续深入JMP的机器学习用于大数据分析
                略微优化PyqtGraph, 用于基础调试和一线人员分析
                Altair用于少量数据批次的可视化探索分析. 也许可以移植到fast-api上用于Summary?
                Spotfire?
"""

