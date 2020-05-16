# This Python file uses the following encoding: utf-8

from PyQt5.QtCore import QTimer
from playback_timer import PlaybackTimer
from time_series_plot import TimeSeriesPlot


class PlaybackControl:
    def nextButtonPressed(self):
        # Update event ID
        if self.event_ID < self.event_length - 1:
            self.event_ID += 1

        # Update buttons
        QTimer.singleShot(10, lambda: PlaybackControl.disableButtons(self))

        # Update event label
        self.event_ID_label.setText('Event ' + str(self.event_ID) + ' of ' + str(self.event_length - 1))
        self.event_ID_label.repaint()

        # Update time-series plot
        if hasattr(self, 'time_series_data'):
            TimeSeriesPlot.updateTimeSeries(self)

        # Update slider
        self.event_slider.setValue(self.event_ID)

        # Update center line
        if self.discard_log[self.event_ID]:
            self.center_line.setMovable(True)
            self.center_line.setPen(color=(0, 0, 0))
        else:
            self.center_line.setMovable(False)
            self.center_line.setPen(color=(220, 220, 220))

        # Play media
        PlaybackTimer.__init__(self)

    def prevButtonPressed(self):
        # Update event ID
        if self.event_ID > 0:
            self.event_ID -= 1

        # Update buttons
        QTimer.singleShot(10, lambda: PlaybackControl.disableButtons(self))

        # Update event label
        self.event_ID_label.setText('Event ' + str(self.event_ID) + ' of ' + str(self.event_length - 1))
        self.event_ID_label.repaint()

        # Update time-series plot
        if hasattr(self, 'time_series_data'):
            TimeSeriesPlot.updateTimeSeries(self)

        # Update center line
        if self.discard_log[self.event_ID]:
            self.center_line.setMovable(True)
            self.center_line.setPen(color=(0, 0, 0))
        else:
            self.center_line.setMovable(False)
            self.center_line.setPen(color=(220, 220, 220))

        # Update slider
        self.event_slider.setValue(self.event_ID)

        # Play media
        PlaybackTimer.__init__(self)

    def replayButtonPressed(self):
        # Update label on first playback
        if self.playback_speed == 1:
            self.replay_button.setText("Replay")
        elif self.playback_speed == 0.5:
            self.replay_button.setText("Replay (0.5x)")
        elif self.playback_speed == 0.25:
            self.replay_button.setText("Replay (0.25x)")

        # Update buttons
        QTimer.singleShot(10, lambda: PlaybackControl.disableButtons(self))

        # Play media
        PlaybackTimer.__init__(self)

    def disableButtons(self):
        self.next_button.setEnabled(False)
        self.prev_button.setEnabled(False)
        self.replay_button.setEnabled(False)
        self.discard_button.setEnabled(False)
        self.event_slider.setEnabled(False)
