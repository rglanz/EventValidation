# This Python file uses the following encoding: utf-8

from PyQt5.Qt import Qt
import pyqtgraph as pg
import numpy as np
from video_segmentation import VideoSegmentation
from time_series_segmentation import TimeSeriesSegmentation
from time_series_plot import TimeSeriesPlot
from playback_control import PlaybackControl


class AddEvent:
    def __init__(self):
        # Freeze main center line
        self.center_line.setMovable(False)

        # Create temporary center line
        self.temporary_center_line = self.plot_widget.addLine(x=0, y=None, pen=pg.mkPen('k', width=1, style=Qt.DashLine),
                                                         movable=True, hoverPen=pg.mkPen('g', width=1,
                                                         style=Qt.DashLine), bounds=[-0.5, 0.5])
        self.temporary_center_line.sigPositionChangeFinished.connect(lambda: AddEvent.temporaryLineAdjusted(self))

    def temporaryLineAdjusted(self):
        # Calculate new event time
        original_event_time = self.event_times_data[self.event_ID]
        temporary_center_line_position = self.temporary_center_line.pos()
        new_event_time = original_event_time + temporary_center_line_position[0]

        if new_event_time <= original_event_time:
            # Update event times
            self.event_times_data = np.insert(self.event_times_data, self.event_ID, new_event_time)
            np.savetxt(self.event_times_path, self.event_times_data)

            # Update discard log
            self.discard_log = np.insert(self.discard_log, self.event_ID, 1)
            np.savetxt(self.discard_file_path, self.discard_log, delimiter=',', fmt='%i')

        elif new_event_time > original_event_time:
            # Update event times
            self.event_times_data = np.insert(self.event_times_data, self.event_ID + 1, new_event_time)
            np.savetxt(self.event_times_path, self.event_times_data)

            # Update discard log
            self.discard_log = np.insert(self.discard_log, self.event_ID + 1, 1)
            np.savetxt(self.discard_file_path, self.discard_log, delimiter=',', fmt='%i')

            # Update event ID
            self.event_ID += 1

        # Update event label
        self.event_length += 1
        self.event_ID_label.setText('Event ' + str(self.event_ID) + ' of ' + str(self.event_length - 1))
        self.event_ID_label.repaint()

        # Hide temporary line
        self.temporary_center_line.setPos(0)
        self.temporary_center_line.setMovable(False)
        self.temporary_center_line.setPen(pg.mkPen(None))
        self.temporary_center_line.setHoverPen(pg.mkPen(None))

        # Re-enable center line
        self.center_line.setMovable(True)

        # Update frameIndex data
        VideoSegmentation.__init__(self)

        # Update Time-series
        TimeSeriesSegmentation.createEpochs(self)
        TimeSeriesPlot.updateTimeSeries(self)

    def altReleased(self):
        # Hide temporary line
        self.temporary_center_line.setPos(0)
        self.temporary_center_line.setMovable(False)
        self.temporary_center_line.setPen(pg.mkPen(None))
        self.temporary_center_line.setHoverPen(pg.mkPen(None))

        # Re-enable center line
        self.center_line.setMovable(True)
