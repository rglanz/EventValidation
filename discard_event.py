# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QMessageBox, QPushButton
import numpy as np
import os
from time_series_plot import TimeSeriesPlot


class DiscardEvent:
    def __init__(self):
        # Check for existing discard log
        self.discard_file_path = self.video_path[0:-4] + "_discard_log.csv"

        if os.path.isfile(self.discard_file_path):
            project_file_message = QMessageBox()
            project_file_message.setWindowTitle('Discard Log')
            project_file_message.setText('An existing discard log for this video was found.')
            project_file_message.addButton(QPushButton('Overwrite'), QMessageBox.YesRole)
            project_file_message.addButton(QPushButton('Load discard log'), QMessageBox.NoRole)
            project_file_message.setDefaultButton(QMessageBox.Yes)

            user_response = project_file_message.exec_()

            if user_response == 1:  # Load discard log
                self.discard_log = np.genfromtxt(self.discard_file_path, dtype='int')
            elif user_response == 0: # Overwrite
                self.discard_log = np.ones([self.event_length, 1], dtype='int')

        else:
            self.discard_log = np.ones([self.event_length, 1], dtype='int')

    def discardEvent(self):
        if self.discard_button.isChecked():
            # Update Log
            self.discard_log[self.event_ID] = 0
            np.savetxt(self.discard_file_path, self.discard_log, delimiter=',', fmt='%i')

            # Freeze center line
            self.center_line.setMovable(False)
            self.center_line.setPen(color=(220, 220, 220))

            # Update time-series plot
            TimeSeriesPlot.updateTimeSeries(self)

        else:
            self.discard_log[self.event_ID] = 1
            np.savetxt(self.discard_file_path, self.discard_log, delimiter=',', fmt='%i')

            # Release center line
            self.center_line.setMovable(True)
            self.center_line.setPen(color=(0, 0, 0))

            # Update time-series plot
            TimeSeriesPlot.updateTimeSeries(self)
