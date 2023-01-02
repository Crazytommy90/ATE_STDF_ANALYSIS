"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/5/5 11:50
@Software: PyCharm
@File    : chart_sample_line.py
@Remark  : 
"""

import pyqtgraph as pg


class PyqtCanvas:

    @staticmethod
    def set_graph_ui(layout, title: str):
        """
        传入layout 在上面加入pg
        """
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        win = pg.GraphicsLayoutWidget()
        layout.addWidget(win)
        p1 = win.addPlot(title=title)
        p1.showGrid(x=False, y=True)
        p1.showAxis('bottom', False)
        return p1, win

    @staticmethod
    def clear_graphLine_plot(win):
        win.clear()
