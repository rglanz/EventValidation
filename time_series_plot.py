# This Python file uses the following encoding: utf-8

import pyqtgraph as pg
import numpy as np


class TimeSeriesPlot:
    def __init__(self):
        if hasattr(self, 'time_series_epochs'):
            if self.discard_log[self.event_ID]:
                penColor = (0, 0, 0)
            else:
                penColor = (220, 220, 220)

            self.time_series_line = self.plot_widget.plot(np.linspace(-0.5, 0.5, 99), self.time_series_epochs[0, :],
                                                       pen=pg.mkPen(color=penColor, width=1))
            self.center_line.setMovable(True)

    def updateTimeSeries(self):
        if hasattr(self, 'time_series_epochs'):
            if hasattr(self, 'time_series_line'):
                self.time_series_line.clear()

            if self.discard_log[self.event_ID]:
                penColor = (0, 0, 0)
            else:
                penColor = (220, 220, 220)

            self.time_series_line = self.plot_widget.plot(np.linspace(-0.5, 0.5, 99),
                                                          self.time_series_epochs[self.event_ID, :],
                                                          pen=pg.mkPen(color=penColor, width=1))
