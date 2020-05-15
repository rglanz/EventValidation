# This Python file uses the following encoding: utf-8

import numpy as np
from PyQt5.QtWidgets import QMessageBox


class TimeSeriesSegmentation:
    def __init__(self):
        self.time_series_error_code = 0

        if len(self.time_series_data) != self.video_n_frames:
            time_series_error_message = QMessageBox()
            time_series_error_message.setWindowTitle('Import Time Series')
            time_series_error_message.setText("Time Series length does not match Video length." +
                                              "\nTime Series not loaded.")
            time_series_error_message.setDetailedText("Time Series Length: " + str(len(self.time_series_data)) +
                                                      "\nVideo Length: " + str(int(self.video_n_frames)))

            time_series_error_message.exec_()
            self.time_series_error_code = 1
        else:
            TimeSeriesSegmentation.createEpochs(self)

    def createEpochs(self):
        self.time_series_epochs = np.zeros([self.event_length, int(round(self.Fs))-1])
        for iEpoch in np.arange(0, self.event_length):
            if (self.frame_times[iEpoch] >= int(round(self.Fs/2)) and
                self.frame_times[iEpoch] + int(round(self.Fs/2))-1 < len(self.time_series_data)):
                start_index = self.frame_times[iEpoch] - int(round(self.Fs/2))
                end_index = self.frame_times[iEpoch] + int(round(self.Fs/2))-1

            elif self.frame_times[iEpoch] < int(round(self.Fs/2)):
                start_index = 0
                end_index = int(round(self.Fs))-1

            elif self.frame_times[iEpoch] + int(round(self.Fs/2))-1 > len(self.time_series_data):
                start_index = len(self.time_series_data) - (int(round(self.Fs))-1)
                end_index = len(self.time_series_data)

            self.time_series_epochs[iEpoch, :] = self.time_series_data[start_index:end_index]

            # TODO: match plotting with event time if boundary conditions are violated