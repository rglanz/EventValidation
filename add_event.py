# This Python file uses the following encoding: utf-8

from PyQt5.Qt import Qt
import pyqtgraph as pg
import numpy as np
from video_segmentation import VideoSegmentation
from time_series_segmentation import TimeSeriesSegmentation
from time_series_plot import TimeSeriesPlot
from save_output import SaveOutput


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
            self.event_times_data_orig = np.insert(self.event_times_data_orig, self.event_ID, np.NaN)

            # Update discard log
            self.discard_log = np.insert(self.discard_log, self.event_ID, 0)

            # Update flagged events
            self.event_flags = np.insert(self.event_flags, self.event_ID, 0)

            # Save output
            SaveOutput.saveData(self)

        elif new_event_time > original_event_time:
            # Update event times
            self.event_times_data = np.insert(self.event_times_data, self.event_ID + 1, new_event_time)
            self.event_times_data_orig = np.insert(self.event_times_data_orig, self.event_ID + 1, np.NaN)

            # Update discard log
            self.discard_log = np.insert(self.discard_log, self.event_ID + 1, 0)

            # Update flagged events
            self.event_flags = np.insert(self.event_flags, self.event_ID + 1, 0)

            # Update event ID
            self.event_ID += 1
            self.last_event_ID = np.zeros([np.shape(self.event_times_data)[0]], dtype=np.int)
            self.last_event_ID[self.event_ID] = 1

            # Save output
            SaveOutput.saveData(self)

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
