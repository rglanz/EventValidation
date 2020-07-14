# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QMessageBox, QPushButton
import numpy as np
import os
from time_series_plot import TimeSeriesPlot
from save_output import SaveOutput


class DiscardEvent:
    def discardEvent(self):
        if self.discard_button.isChecked():
            # Update Log
            self.discard_log[self.event_ID] = 1

            # Save output
            SaveOutput.saveData(self)

            # Freeze center line
            self.center_line.setMovable(False)
            self.center_line.setPen(color=(220, 220, 220))

            # Update time-series plot
            TimeSeriesPlot.updateTimeSeries(self)

        else:
            self.discard_log[self.event_ID] = 0

            # Save output
            SaveOutput.saveData(self)

            # Release center line
            self.center_line.setMovable(True)
            self.center_line.setPen(color=(0, 0, 0))

            # Update time-series plot
            TimeSeriesPlot.updateTimeSeries(self)
