# Provide back-end to the file dialog buttons

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtCore import QUrl, Qt
import cv2  # must be installed as headless, or will collide with Qt
import numpy as np
import pyqtgraph as pg
import os
from video_segmentation import VideoSegmentation
from time_series_segmentation import TimeSeriesSegmentation
from time_series_plot import TimeSeriesPlot
from discard_event import DiscardEvent
from slider_handle import SliderHandle
from time_adjust import TimeAdjust


class FileDialog:
    def open_video(self):
        # Open video dialog box
        video_dialog = QFileDialog()
        video_dialog.setNameFilters(["Videos (*.mp4 *.avi *.mov *.flv *.wmv)"])
        video_dialog.selectNameFilter("Videos (*.mp4 *.avi *.mov *.flv *.wmv)")
        video_dialog.exec_()
        self.video_fullfile_name = video_dialog.selectedFiles()

        if len(self.video_fullfile_name) != 0:
            self.eventIndexBtn.setEnabled(True)

            # Load first frame
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_fullfile_name[0])))
            self.mediaPlayer.setPosition(0)
            self.mediaPlayer.play()
            self.mediaPlayer.pause()

            # Open-CV for meta data
            self.video_object = cv2.VideoCapture(self.video_fullfile_name[0])
            self.Fs = self.video_object.get(cv2.CAP_PROP_FPS)
            self.videoHeight = self.video_object.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.videoWidth = self.video_object.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.videoNFrames = self.video_object.get(cv2.CAP_PROP_FRAME_COUNT)

            # Re-size video widget
            self.videoWidget.setFixedHeight(self.videoHeight)
            self.videoWidget.setFixedWidth(self.videoWidth)
            self.plotWindow.setFixedWidth(self.videoWidth)

            # Re-size slider
            self.eventSlider.setFixedWidth(self.videoWidth)

            # Update video label
            _, video_path = os.path.splitdrive(self.video_fullfile_name[0])
            self.video_path, self.video_filename = os.path.split(video_path)
            self.setWindowTitle(self.video_filename)

    def open_event_times(self):
        event_times_dialog = QFileDialog(self)
        event_times_dialog.setNameFilters(["Text (*.csv)"])
        event_times_dialog.selectNameFilter("Text (*.csv)")
        event_times_dialog.exec_()
        self.event_times_file_path = event_times_dialog.selectedFiles()

        if len(self.event_times_file_path) != 0:
            with open(self.event_times_file_path[0], 'r', encoding='utf-8-sig') as f:
                self.eventTimesData = np.genfromtxt(f, dtype=float, delimiter=',')

            self.timeSeriesBtn.setEnabled(True)
            self.replayBtn.setEnabled(True)
            self.replayBtn.repaint()

            self.center_line = self.plotWidget.addLine(x=0, y=None, pen=pg.mkPen('k', width=1, style=Qt.DashLine),
                                                       movable=True, hoverPen=pg.mkPen('b', width=1, style=Qt.DashLine),
                                                       bounds=[-0.5, 0.5])
            self.center_line.sigPositionChangeFinished.connect(lambda: TimeAdjust.centerLineAdjusted(self))

            VideoSegmentation.create_epochs(self)
            SliderHandle.__init__(self)

            # Check for existing discard log
            DiscardEvent.__init__(self)

            # Update eventID label
            self.eventIDLabel.setText('Event 0  of ' + str(self.eventLength - 1))

    def open_time_series(self):
        time_series_dialog = QFileDialog(self)
        time_series_dialog.setNameFilters(["Text (*.csv)"])
        time_series_dialog.selectNameFilter("Text (*.csv)")
        time_series_dialog.exec_()
        time_series_file_name = time_series_dialog.selectedFiles()

        if len(time_series_file_name) != 0:
            with open(time_series_file_name[0], 'r', encoding='utf-8-sig') as f:
                self.timeSeriesData = np.genfromtxt(f, dtype=float, delimiter=',')

            TimeSeriesSegmentation.check_length(self)
            if self.timeSeriesErrorCode == 0:
                TimeSeriesSegmentation.create_epochs(self)
                TimeSeriesPlot.update_time_series(self)
