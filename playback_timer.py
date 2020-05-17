# This Python file uses the following encoding: utf-8

from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg


class PlaybackTimer:
    def __init__(self):
        # Start the timer
        self.media_timer = QTimer()
        self.media_timer.setTimerType(Qt.PreciseTimer)
        self.media_timer.start(self.timer_length)

        # Control plot
        self.plot_timer = QTimer()
        self.plot_timer.setTimerType(Qt.PreciseTimer)
        self.plot_timer.setInterval(50)
        self.plot_timer.start()

        self.cursor_position = self.plot_refresh_rate/100
        if hasattr(self, 'line1'):
            self.line1.setValue(self.cursor_position - 0.5)
        else:
            self.line1 = self.plot_widget.addLine(x=self.cursor_position - 0.5,
                                                 y=None, pen=pg.mkPen('r', width=2))

        self.plot_timer.timeout.connect(lambda: PlaybackTimer.updatePlot(self))
        self.media_timer.timeout.connect(lambda: PlaybackTimer.endPlot(self))

        # Control media
        self.media_player.setPosition(1000 * self.frame_index[self.event_ID, 0] / self.Fs)
        self.media_player.play()
        self.media_timer.timeout.connect(lambda: PlaybackTimer.endMediaPlayback(self))

        # Update buttons
        self.media_timer.timeout.connect(lambda: PlaybackTimer.enableButtons(self))

    def endMediaPlayback(self):
        self.media_player.pause()
        self.media_timer.stop()

    def updatePlot(self):
        self.line1.setValue(self.cursor_position - 0.5)
        self.cursor_position += self.plot_refresh_rate/100

    def endPlot(self):
        self.line1.setValue(0.5)
        self.plot_timer.stop()
        QTimer.singleShot(10, lambda: PlaybackTimer.restartLine(self))

    def restartLine(self):
        self.line1.setValue(-0.5)

    def enableButtons(self):
        if self.event_ID < self.event_length - 1:
            self.next_button.setEnabled(True)
        elif self.event_ID == self.event_length - 1:
            self.next_button.setEnabled(False)

        if self.event_ID > 0:
            self.prev_button.setEnabled(True)
        elif self.event_ID <= 0:
            self.prev_button.setEnabled(False)

        self.replay_button.setEnabled(True)
        self.event_slider.setEnabled(True)

        self.discard_button.setEnabled(True)
        if self.discard_log[self.event_ID]:
            self.discard_button.setChecked(False)
        else:
            self.discard_button.setChecked(True)

        self.speed_1x_action.setEnabled(True)
        self.speed_05x_action.setEnabled(True)
        self.speed_025x_action.setEnabled(True)