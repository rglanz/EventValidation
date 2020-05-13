# This Python file uses the following encoding: utf-8

import numpy as np
from video_segmentation import VideoSegmentation
from time_series_plot import TimeSeriesPlot
from time_series_segmentation import TimeSeriesSegmentation


class TimeAdjust:
    def centerLineAdjusted(self):
        # Update eventTimesData
        original_event_time = self.eventTimesData[self.eventID]
        new_center_line_position = self.center_line.pos()
        new_event_time = original_event_time + new_center_line_position[0]

        self.eventTimesData[self.eventID] = new_event_time

        # Update frameIndex data
        VideoSegmentation.create_epochs(self)

        # Save Event Times.csv
        np.savetxt(self.event_times_file_path[0], self.eventTimesData)

        # Update Time-series (if applicable)
        if hasattr(self, 'timeSeriesData'):
            TimeSeriesSegmentation.create_epochs(self)
            TimeSeriesPlot.update_time_series(self)

        self.center_line.setPos(0)
