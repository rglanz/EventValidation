# Provides back-end for video control buttons

from PyQt5.QtCore import QTimer
from playback_timer import PlaybackTimer
from time_series_plot import TimeSeriesPlot


class PlaybackControl:
    def next_button_pressed(self):
        # Update buttons
        QTimer.singleShot(10, lambda: PlaybackControl.disable_buttons(self))

        # Update event label
        if self.eventID < self.eventLength - 1:
            self.eventID += 1
            self.eventIDLabel.setText('Event ' + str(self.eventID) + ' of ' + str(self.eventLength - 1))
            self.eventIDLabel.repaint()

        # Update time-series plot
        if hasattr(self, 'timeSeriesData'):
            TimeSeriesPlot.update_time_series(self)

        # Update slider
        self.eventSlider.setValue(self.eventID)

        # Play video clip
        PlaybackTimer.__init__(self)

    def prev_button_pressed(self):
        # Update buttons
        QTimer.singleShot(10, lambda: PlaybackControl.disable_buttons(self))

        # Update event label
        if self.eventID > 0:
            self.eventID -= 1
            self.eventIDLabel.setText('Event ' + str(self.eventID) + ' of ' + str(self.eventLength - 1))
            self.eventIDLabel.repaint()

        # Update time-series plot
        if hasattr(self, 'timeSeriesData'):
            TimeSeriesPlot.update_time_series(self)

        # Update slider
        self.eventSlider.setValue(self.eventID)

        # Play video clip
        PlaybackTimer.__init__(self)

    def replay_button_pressed(self):
        # Update label on first playback
        self.replayBtn.setText('Replay')

        # Update buttons
        QTimer.singleShot(10, lambda: PlaybackControl.disable_buttons(self))

        # Update time-series plot
        if hasattr(self, 'timeSeriesData'):
            TimeSeriesPlot.update_time_series(self)

        # Play video clip
        PlaybackTimer.__init__(self)

    def disable_buttons(self):
        self.nextBtn.setEnabled(False)
        self.prevBtn.setEnabled(False)
        self.replayBtn.setEnabled(False)
        self.discardBtn.setEnabled(False)
        self.undoBtn.setEnabled(False)
        self.eventSlider.setEnabled(False)

