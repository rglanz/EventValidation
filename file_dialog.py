# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtCore import QUrl, Qt, QRect
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
    def openVideo(self):
        # Open video dialog box
        video_dialog = QFileDialog()
        video_dialog.setNameFilters(["Videos (*.mp4 *.avi *.mov *.flv *.wmv)"])
        video_dialog.selectNameFilter("Videos (*.mp4 *.avi *.mov *.flv *.wmv)")
        video_dialog.exec_()
        self.video_path = video_dialog.selectedFiles()

        if len(self.video_path) != 0:
            self.video_path = self.video_path[0]    # Convert list to string

            # Load first frame
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_path)))
            self.media_player.setPosition(0)
            self.media_player.play()
            self.media_player.pause()

            # Open-CV for meta data
            self.video_object = cv2.VideoCapture(self.video_path)
            self.Fs = self.video_object.get(cv2.CAP_PROP_FPS)
            self.video_height = self.video_object.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.video_width = self.video_object.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.video_n_frames = self.video_object.get(cv2.CAP_PROP_FRAME_COUNT)
            self.plot_refresh_rate = self.Fs/20

            # Re-size video widget
            self.video_widget.setFixedHeight(self.video_height)
            self.video_widget.setFixedWidth(self.video_width)
            self.plot_window.setFixedWidth(self.video_width)

            # Re-center GUI
            _, _, gui_width, gui_height = self.frameGeometry().getRect()
            self.setGeometry(int(round(0.5*(self.screen_width - gui_width))),
                             int(round(0.25*(self.screen_height - gui_height))), gui_width, self.screen_height)

            # Re-size slider
            self.event_slider.setFixedWidth(self.video_width)

            # Update video label
            _, self.video_file_name = os.path.split(self.video_path)
            self.setWindowTitle(self.video_file_name)

            # Enable event times button
            self.event_times_menu_action.setEnabled(True)

    def openEventTimes(self):
        event_times_dialog = QFileDialog(self)
        event_times_dialog.setNameFilters(["Text (*.csv)"])
        event_times_dialog.selectNameFilter("Text (*.csv)")
        event_times_dialog.exec_()
        self.event_times_path = event_times_dialog.selectedFiles()

        if len(self.event_times_path) != 0:
            self.event_times_path = self.event_times_path[0]    # Convert list to string

            # Load event times
            with open(self.event_times_path, 'r', encoding='utf-8-sig') as f:
                self.event_times_data = np.genfromtxt(f, dtype=float, delimiter=',')
            self.event_length = len(self.event_times_data)

            # Update event label
            self.event_ID_label.setText('Event 0  of ' + str(self.event_length - 1))

            # Enable time-series button
            self.time_series_menu_action.setEnabled(True)

            # Enable playback speed
            self.speed_1x_action.setEnabled(True)
            self.speed_05x_action.setEnabled(True)
            self.speed_025x_action.setEnabled(True)

            # Enable play/replay button
            self.replay_button.setEnabled(True)
            self.replay_button.repaint()

            # Draw center line (time-lag 0)
            self.center_line = self.plot_widget.addLine(x=0, y=None, pen=pg.mkPen('k', width=1, style=Qt.DashLine),
                                                        movable=False, hoverPen=pg.mkPen('b', width=1,
                                                        style=Qt.DashLine), bounds=[-0.5, 0.5])
            self.center_line.sigPositionChangeFinished.connect(lambda: TimeAdjust.centerLineAdjusted(self))

            # Video segmentation
            VideoSegmentation.__init__(self)

            # Enable event slider
            SliderHandle.__init__(self)

            # Check for existing discard log
            DiscardEvent.__init__(self)

    def openTimeSeries(self):
        time_series_dialog = QFileDialog(self)
        time_series_dialog.setNameFilters(["Text (*.csv)"])
        time_series_dialog.selectNameFilter("Text (*.csv)")
        time_series_dialog.exec_()
        self.time_series_path = time_series_dialog.selectedFiles()

        if len(self.time_series_path) != 0:
            self.time_series_path = self.time_series_path[0]    # Convert list to string

            with open(self.time_series_path, 'r', encoding='utf-8-sig') as f:
                self.time_series_data = np.genfromtxt(f, dtype=float, delimiter=',')

            TimeSeriesSegmentation.__init__(self)
            TimeSeriesPlot.__init__(self)
