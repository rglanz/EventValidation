# Segments time series into epochs based on event times.

import numpy as np
from PyQt5.QtWidgets import QMessageBox


class TimeSeriesSegmentation:
    def check_length(self):
        self.timeSeriesErrorCode = 0

        if len(self.timeSeriesData) != self.videoNFrames:
            time_series_error_message = QMessageBox()
            time_series_error_message.setWindowTitle('Import Time Series')
            time_series_error_message.setText("Time Series length does not match Video length." +
                                              "\nTime Series not loaded.")

            video_frames_int = int(self.videoNFrames)
            time_series_error_message.setDetailedText("Time Series Length: " + str(len(self.timeSeriesData)) +
                                                      "\nVideo Length: " + str(video_frames_int))

            time_series_error_message.exec_()
            self.timeSeriesErrorCode = 1

    def create_epochs(self):
        self.timeSeriesEpochs = np.zeros([self.eventLength, 99])
        for iEpoch in np.arange(0, self.eventLength):
            if (self.frameTimes[iEpoch] >= 50 and
                self.frameTimes[iEpoch] + 49 < len(self.timeSeriesData)):
                start_index = self.frameTimes[iEpoch] - 50
                end_index = self.frameTimes[iEpoch] + 49

            elif self.frameTimes[iEpoch] < 50:
                start_index = 0
                end_index = 99

            elif self.frameTimes[iEpoch] + 49 >= len(self.timeSeriesData):
                start_index = len(self.timeSeriesData) - 99
                end_index = len(self.timeSeriesData)

            self.timeSeriesEpochs[iEpoch, :] = self.timeSeriesData[start_index:end_index]
