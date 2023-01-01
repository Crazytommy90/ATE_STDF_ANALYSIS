"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/5/6 11:38
@Software: PyCharm
@File    : select1.py
@Remark  :
"""
import pandas as pd
from pyqtgraph import ViewBox, Point

"""
This example demonstrates the creation of a plot with 
DateAxisItem and a customized ViewBox. 
"""

import numpy as np

import pyqtgraph as pg
from PySide2 import QtCore
import pyqtgraph.functions as fn


class CustomViewBox(pg.ViewBox):
    select_signal = QtCore.Signal(object)

    def __init__(self, *args, **kwds):
        kwds['enableMenu'] = False
        pg.ViewBox.__init__(self, *args, **kwds)
        self.setMouseMode(self.RectMode)

    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.MouseButton.RightButton:
            ev.ignore()
            # self.autoRange()

    def wheelEvent(self, ev, axis=None):
        if axis is None:
            ev.ignore()
            return
        super().wheelEvent(ev, axis)

    ## reimplement mouseDragEvent to disable continuous axis zoom
    def mouseDragEvent(self, ev, axis=None):
        # print(ev.button())
        if axis is not None and ev.button() in [QtCore.Qt.MouseButton.RightButton, QtCore.Qt.MouseButton.MiddleButton]:
            ev.ignore()
        else:
            self._mouseDragEvent(ev, axis=axis)

    def _mouseDragEvent(self, ev, axis=None):
        ev.accept()  ## we accept all buttons

        pos = ev.pos()
        lastPos = ev.lastPos()
        dif = pos - lastPos
        dif = dif * -1

        ## Ignore axes if mouse is disabled
        mouseEnabled = np.array(self.state['mouseEnabled'], dtype=np.float64)
        mask = mouseEnabled.copy()
        if axis is not None:
            mask[1 - axis] = 0.0

        if ev.button() in [QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.MouseButton.MiddleButton]:
            if self.state['mouseMode'] == ViewBox.RectMode and axis is None:
                if ev.isFinish():  ## This is the final move in the drag; change the view scale now
                    print("finish")
                    self.rbScaleBox.hide()
                    ax = QtCore.QRectF(Point(ev.buttonDownPos(ev.button())), Point(pos))  # 这个是坐标数据
                    ax = self.childGroup.mapRectFromParent(ax)  # 换算成实际数据
                    self.select_signal.emit(ax)
                    # self.showAxRect(ax)
                    self.axHistoryPointer += 1
                    self.axHistory = self.axHistory[:self.axHistoryPointer] + [ax]
                else:
                    ## update shape of scale box
                    self.updateScaleBox(ev.buttonDownPos(), ev.pos())
            else:
                tr = self.childGroup.transform()
                tr = fn.invertQTransform(tr)
                tr = tr.map(dif * mask) - tr.map(Point(0, 0))

                x = tr.x() if mask[0] == 1 else None
                y = tr.y() if mask[1] == 1 else None

                self._resetTarget()
                if x is not None or y is not None:
                    self.translateBy(x=x, y=y)
                self.sigRangeChangedManually.emit(self.state['mouseEnabled'])


class CustomTickSliderItem(pg.TickSliderItem):
    def __init__(self, *args, **kwds):
        pg.TickSliderItem.__init__(self, *args, **kwds)

        self.all_ticks = {}
        self._range = [0, 1]

    def setTicks(self, ticks):
        for tick, pos in self.listTicks():
            self.removeTick(tick)

        for pos in ticks:
            tickItem = self.addTick(pos, movable=False, color="#333333")
            self.all_ticks[pos] = tickItem

        self.updateRange(None, self._range)

    def updateRange(self, vb, viewRange):
        origin = self.tickSize / 2.
        length = self.length

        lengthIncludingPadding = length + self.tickSize + 2

        self._range = viewRange

        for pos in self.all_ticks:
            tickValueIncludingPadding = (pos - viewRange[0]) / (viewRange[1] - viewRange[0])
            tickValue = (tickValueIncludingPadding * lengthIncludingPadding - origin) / length

            # Convert from np.bool_ to bool for setVisible
            visible = bool(tickValue >= 0 and tickValue <= 1)

            tick = self.all_ticks[pos]
            tick.setVisible(visible)

            if visible:
                self.setTickValue(tick, tickValue)


app = pg.mkQApp()

axis = pg.DateAxisItem(orientation='bottom')
vb = CustomViewBox()
# vb.select_signal.connect(lambda x: print(x))


pw = pg.PlotWidget(viewBox=vb, axisItems={'bottom': axis}, enableMenu=False,
                   title="PlotItem with DateAxisItem, custom ViewBox and markers on x axis<br>Menu disabled, mouse behavior changed: left-drag to zoom, right-click to reset zoom")

dates = np.arange(8) * (3600 * 24 * 356)
df = pd.DataFrame({"x": dates, "y": [1, 6, 2, 4, 3, 5, 6, 8]})
curve = pw.plot(x=df["x"].to_numpy(), y=df["y"].to_numpy(), symbol='o', symbolBrush=(187, 26, 95))
curve.sigClicked.connect(lambda x:print(x))
new_curve = pw.plot(x=None, y=None, symbol='o', symbolBrush=(187, 26, 95, 100))


def select_range(ax: QtCore.QRectF):
    """
    只看x
    :param ax:
    :return:
    """
    print(ax)
    new_curve.setData(x=df["x"].to_numpy(), y=df["y"].to_numpy(), clear=True, symbolBrush=(187, 26, 95, 30))
    temp_df = df[(df.x > ax.left()) & (df.x < ax.right())]
    curve.setData(x=temp_df["x"].to_numpy(), y=temp_df["y"].to_numpy(), clear=True)
    # pw.plot(x=temp_df["x"].to_numpy(), y=temp_df["y"].to_numpy(), symbol='o', symbolBrush=(187, 26, 95))


vb.select_signal.connect(select_range)

# Using allowAdd and allowRemove to limit user interaction
tickViewer = CustomTickSliderItem(allowAdd=False, allowRemove=False)
vb.sigXRangeChanged.connect(tickViewer.updateRange)
pw.plotItem.layout.addItem(tickViewer, 4, 1)

tickViewer.setTicks([dates[0], dates[2], dates[-1]])

pw.show()
pw.setWindowTitle('pyqtgraph example: customPlot')

r = pg.PolyLineROI([(0, 0), (10, 10)])
pw.addItem(r)

if __name__ == '__main__':
    pg.exec()
