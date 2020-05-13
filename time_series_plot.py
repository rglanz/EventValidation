# Plots time-series data

import pyqtgraph as pg
import numpy as np


class TimeSeriesPlot:
    def update_time_series(self):
        if hasattr(self, 'timeSeriesEpochs'):
            if self.eventID < 0:
                self.timeSeriesLine = self.plotWidget.plot(np.linspace(-0.5, 0.5, 99), self.timeSeriesEpochs[0, :],
                                                           pen=pg.mkPen('k', width=1))
            elif self.eventID >= 0:
                if hasattr(self, 'timeSeriesLine'):
                    self.timeSeriesLine.clear()

                self.timeSeriesLine = self.plotWidget.plot(np.linspace(-0.5, 0.5, 99),
                                                           self.timeSeriesEpochs[self.eventID, :],
                                                           pen=pg.mkPen('k', width=1))
