# This Python file uses the following encoding: utf-8

import pyqtgraph as pg
import numpy as np
from PyQt5.QtGui import QLinearGradient, QPen, QColor

class TimeSeriesPlot:
    def __init__(self):
        if hasattr(self, 'time_series_epochs'):
            if self.discard_log[self.event_ID]:
                self.time_series_line = self.plot_widget.plot(np.linspace(-0.5, 0.5, 99), self.time_series_epochs[self.event_ID, :],
                                                              pen=pg.mkPen(color=(0, 0, 0), width=1))
            else:
                self.time_series_line = self.plot_widget.plot(np.linspace(-0.5, 0.5, 99), self.time_series_epochs[self.event_ID, :],
                                                              pen=pg.mkPen(color=(220, 220, 220), width=1))

            self.center_line.setMovable(True)

            # Set axes
            y_min = np.min(self.time_series_epochs[self.event_ID, :])
            y_max = np.max(self.time_series_epochs[self.event_ID, :])
            self.plot_widget.setYRange(y_min, y_max)

    def updateTimeSeries(self):
        if hasattr(self, 'time_series_epochs'):
            if hasattr(self, 'time_series_line'):
                self.time_series_line.clear()

            if self.discard_log[self.event_ID]:
                self.time_series_line = self.plot_widget.plot(np.linspace(-0.5, 0.5, 99), self.time_series_epochs[self.event_ID, :],
                                                              pen=pg.mkPen(color=(0, 0, 0), width=1))
            else:
                self.time_series_line = self.plot_widget.plot(np.linspace(-0.5, 0.5, 99), self.time_series_epochs[self.event_ID, :],
                                                              pen=pg.mkPen(color=(220, 220, 220), width=1))

            # Set axes
            y_min = np.min(self.time_series_epochs[self.event_ID, :])
            y_max = np.max(self.time_series_epochs[self.event_ID, :])
            self.plot_widget.setYRange(y_min, y_max)
