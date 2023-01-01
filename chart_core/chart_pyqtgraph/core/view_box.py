"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/12/23 17:09
@Site    : 
@File    : view_box.py
@Software: PyCharm
@Remark  : 
"""

import numpy as np
import pyqtgraph as pg
from PySide2 import QtCore
from pyqtgraph import ViewBox, Point
import pyqtgraph.functions as fn

from ui_component.ui_app_variable import QtPlotAllUse


class CustomViewBox(pg.ViewBox):
    """
    重写了ViewBox中 选取区间的功能
    """
    select_signal = QtCore.Signal(object)
    ax_s = None

    def __init__(self, *args, **kwargs):
        kwargs['enableMenu'] = False
        pg.ViewBox.__init__(self, *args, **kwargs)
        self.setMouseMode(self.RectMode)
        self.ax_s = []

    # def keyPressEvent(self, ev: QKeyEvent):
    #     if ev.key() == QtCore.Qt.Key_Control:
    #         QtPlotAllUse.multi_select = True
    #     super(CustomViewBox, self).keyPressEvent(ev)
    # 
    # def keyReleaseEvent(self, ev):
    #     if ev.key() == QtCore.Qt.Key_Control:
    #         QtPlotAllUse.multi_select = False
    #     super(CustomViewBox, self).keyReleaseEvent(ev)

    def mouseClickEvent(self, ev):
        """
        :param ev:
        :return:
        """
        if ev.button() == QtCore.Qt.MouseButton.RightButton:
            ev.ignore()
            self.select_signal.emit(None)  # clear select

    def wheelEvent(self, ev, axis=None):
        """

        :param ev:
        :param axis:
        :return:
        """
        if axis is None:
            ev.ignore()
            return
        super().wheelEvent(ev, axis)

    def mouseDragEvent(self, ev, axis=None):
        """
        重写鼠标拽取绘制事件
        :param ev:
        :param axis:
        :return:
        """
        if axis is not None and ev.button() in [QtCore.Qt.MouseButton.RightButton,
                                                QtCore.Qt.MouseButton.MiddleButton]:
            ev.ignore()
        else:
            self._mouseDragEvent(ev, axis=axis)

    def _mouseDragEvent(self, ev, axis=None):
        ev.accept()
        pos = ev.scenePos()
        dif = pos - ev.lastScenePos()
        dif = dif * -1

        mouse_enabled = np.array(self.state['mouseEnabled'], dtype=np.float64)
        mask = mouse_enabled.copy()
        if axis is not None:
            mask[1 - axis] = 0.0

        if ev.button() in [QtCore.Qt.MouseButton.LeftButton, QtCore.Qt.MouseButton.MiddleButton]:
            if self.state['mouseMode'] == ViewBox.RectMode and axis is None:
                if ev.isFinish():
                    self.rbScaleBox.hide()
                    ax = QtCore.QRectF(Point(ev.buttonDownScenePos(ev.button())), Point(pos))
                    ax = self.childGroup.mapRectFromScene(ax)
                    if QtPlotAllUse.MultiSelect is False:
                        self.ax_s.clear()
                        self.ax_s.append(ax)
                        self.select_signal.emit(self.ax_s)
                    else:
                        self.ax_s.append(ax)
                        self.select_signal.emit(self.ax_s)
                    self.axHistoryPointer += 1
                    self.axHistory = self.axHistory[:self.axHistoryPointer] + [ax]
                else:
                    self.updateScaleBox(ev.buttonDownScenePos(), ev.scenePos())
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
