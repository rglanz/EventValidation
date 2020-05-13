# Provides back-end timer for video and plotting events

from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg


class PlaybackTimer:
    def __init__(self):
        # Start the timer
        self.playbackTimer = QTimer()
        self.playbackTimer.setTimerType(Qt.PreciseTimer)
        self.playbackTimer.start(1000)

        # Control plot
        self.plotTimer = QTimer()
        self.plotTimer.setTimerType(Qt.PreciseTimer)
        self.plotTimer.setInterval(50)
        self.plotTimer.start()

        self.cursorPosition = 0.05
        if hasattr(self, 'line1'):
            self.line1.setValue(self.cursorPosition - 0.5)
        else:
            self.line1 = self.plotWidget.addLine(x=self.cursorPosition - 0.5,
                                                 y=None, pen=pg.mkPen('r', width=2))

        self.plotTimer.timeout.connect(lambda: PlaybackTimer.update_plot(self))
        self.playbackTimer.timeout.connect(lambda: PlaybackTimer.end_plot(self))

        # Control media
        self.mediaPlayer.setPosition(1000 * self.frameIndex[self.eventID, 0] / self.Fs)
        self.mediaPlayer.play()
        self.playbackTimer.timeout.connect(lambda: PlaybackTimer.end_media_playback(self))

        # Update buttons
        self.playbackTimer.timeout.connect(lambda: PlaybackTimer.enable_buttons(self))

    def end_media_playback(self):
        self.mediaPlayer.pause()

    def update_plot(self):
        self.line1.setValue(self.cursorPosition - 0.5)
        self.cursorPosition += 0.05

    def end_plot(self):
        self.plotTimer.stop()
        self.line1.setValue(0.5)
        QTimer.singleShot(10, lambda: PlaybackTimer.restartLine(self))

    def restartLine(self):
        self.line1.setValue(-0.5)

    def enable_buttons(self):
        if self.eventID < self.eventLength - 1:
            self.nextBtn.setEnabled(True)
        elif self.eventID == self.eventLength - 1:
            self.nextBtn.setEnabled(False)

        if self.eventID > 0:
            self.prevBtn.setEnabled(True)
        elif self.eventID <= 0:
            self.prevBtn.setEnabled(False)

        self.replayBtn.setEnabled(True)

        if self.discardLog[self.eventID]:
            self.discardBtn.setEnabled(True)
        else:
            self.discardBtn.setEnabled(False)

        if self.discardLog[self.eventID]:
            self.undoBtn.setEnabled(False)
        else:
            self.undoBtn.setEnabled(True)

        self.eventSlider.setEnabled(True)
