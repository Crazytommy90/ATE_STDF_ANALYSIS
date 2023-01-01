#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : qcus.py
@Author  : Link
@Time    : 2022/12/10 20:49
@Mark    : 
"""
import time

from PySide2.QtCore import Qt, qExp, qFastCos
from PySide2.QtGui import QPen, QBrush, QColor

from PySide2 import QtGui
from qcustomplot_pyside2 import *

import sys
from PySide2.QtWidgets import QApplication
import numpy as np

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    customPlot = QCustomPlot()
    customPlot.resize(800, 600)
    customPlot.setWindowTitle('Quadratic Demo')
    customPlot.setSelectionRectMode(QCP.SelectionRectMode.srmSelect)

    # create graph and assign data to it:

    graph0 = customPlot.addGraph()
    graph0.setSelectable(QCP.SelectionType.stMultipleDataRanges)
    graph0.setPen(QPen(Qt.blue))
    graph0.setBrush(QBrush(QColor(0, 0, 255, 20)))

    graph1 = customPlot.addGraph()
    graph1.setSelectable(QCP.SelectionType.stMultipleDataRanges)
    graph1.setPen(QPen(Qt.red))

    x = np.full([251], 0.0)
    y0 = np.full([251], 0.0)
    y1 = np.full([251], 0.0)

    for i in range(251):
        x[i] = i
        y0[i] = qExp(-i / 150) * qFastCos(i / 10)
        y1[i] = qExp(-i / 150)

    start = time.time()
    graph0.setData(x, y0)
    graph1.setData(x, y1)
    graph0.rescaleAxes()
    graph1.rescaleAxes(True)
    end = time.time()
    print('用时: {}秒'.format(end - start))

    # give the axes some labels:
    customPlot.xAxis.setLabel("x")
    customPlot.yAxis.setLabel("y")

    customPlot.setInteractions(
        QCP.Interactions(QCP.iRangeDrag | QCP.iSelectPlottables | QCP.iMultiSelect)
    )

    customPlot.show()
    # Create and show the form
    # Run the main Qt loop
    res = app.exec_()
    customPlot = None
    sys.exit(res)
