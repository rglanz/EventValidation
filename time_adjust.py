# This Python file uses the following encoding: utf-8

import numpy as np
from video_segmentation import VideoSegmentation
from time_series_plot import TimeSeriesPlot
from time_series_segmentation import TimeSeriesSegmentation


class TimeAdjust:
    def centerLineAdjusted(self):
        # Update eventTimesData
        original_event_time = self.event_times_data[self.event_ID]
        new_center_line_position = self.center_line.pos()
        new_event_time = original_event_time + new_center_line_position[0]

        self.event_times_data[self.event_ID] = new_event_time
        np.savetxt(self.event_times_path, self.event_times_data)

        # Update frameIndex data
        VideoSegmentation.__init__(self)

        # Update Time-series (if applicable)
        if hasattr(self, 'time_series_data'):
            TimeSeriesSegmentation.createEpochs(self)
            TimeSeriesPlot.updateTimeSeries(self)

        # Snap center-line back to zero
        self.center_line.setPos(0)
