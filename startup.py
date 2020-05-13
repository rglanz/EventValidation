# Launches the GUI

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel,\
                            QSlider
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtCore import Qt
from pyqtgraph import GraphicsLayoutWidget
import sys
from file_dialog import FileDialog
from playback_control import PlaybackControl
from discard_event import DiscardEvent
from slider_handle import SliderHandle


class GUIWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 30, 900, 900)

        # QMedia object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # QVideo object
        self.videoWidget = QVideoWidget()

        # Plot object
        self.plotWindow = GraphicsLayoutWidget()
        self.plotWindow.ci.layout.setContentsMargins(0, 0, 0, 0)
        self.plotWindow.ci.layout.setSpacing(0)
        self.plotWindow.setBackground(None)
        self.plotWidget = self.plotWindow.addPlot(0, 0)
        self.plotWidget.setLabel('bottom', "Time (s)")
        self.plotWidget.setXRange(-0.5, 0.5)
        self.plotWidget.hideAxis('left')
        self.plotWidget.hideButtons()
        self.plotWidget.setMouseEnabled(x=False, y=False)

        # Buttons
        self.videoBtn = QPushButton('Open Video')
        self.videoBtn.clicked.connect(lambda: FileDialog.open_video(self))

        self.eventIndexBtn = QPushButton('Event Index')
        self.eventIndexBtn.setEnabled(False)
        self.eventIndexBtn.clicked.connect(lambda: FileDialog.open_event_times(self))

        self.timeSeriesBtn = QPushButton('Time Series')
        self.timeSeriesBtn.setEnabled(False)
        self.timeSeriesBtn.clicked.connect(lambda: FileDialog.open_time_series(self))

        self.prevBtn = QPushButton('Prev')
        self.prevBtn.setEnabled(False)
        self.prevBtn.clicked.connect(lambda: PlaybackControl.prev_button_pressed(self))

        self.nextBtn = QPushButton('Next')
        self.nextBtn.setEnabled(False)
        self.nextBtn.clicked.connect(lambda: PlaybackControl.next_button_pressed(self))

        self.replayBtn = QPushButton('Play') # Is set to 'Play' until first playback occurs
        self.replayBtn.setEnabled(False)
        self.replayBtn.clicked.connect(lambda: PlaybackControl.replay_button_pressed(self))

        self.saveBtn = QPushButton('Save')
        self.saveBtn.setEnabled(False)
        self.saveBtn.clicked.connect(lambda: DiscardEvent.saveDiscardLog(self))

        self.discardBtn = QPushButton('Discard Event')
        self.discardBtn.setEnabled(False)
        self.discardBtn.clicked.connect(lambda: DiscardEvent.updateDiscardLog(self))

        self.undoBtn = QPushButton('Undo')
        self.undoBtn.setEnabled(False)
        self.undoBtn.clicked.connect(lambda: DiscardEvent.undoDiscard(self))

        # Slider
        self.eventSlider = QSlider(Qt.Horizontal)
        self.eventSlider.setFixedWidth(600)
        self.eventSlider.setSingleStep(1)
        self.eventSlider.setValue(0)
        self.eventSlider.setMinimum(0)
        self.eventSlider.setMaximum(20)
        self.eventSlider.setTickInterval(1)
        self.eventSlider.setTickPosition(QSlider.TicksBelow)
        self.eventSlider.valueChanged.connect(lambda: SliderHandle.slider_changed(self))
        self.eventSlider.sliderReleased.connect(lambda: SliderHandle.slider_released(self))
        self.eventSlider.setEnabled(False)

        # EventID label
        self.eventID = 0
        self.eventIDLabel = QLabel('')

        # File buttons layout
        fileBoxLayout = QVBoxLayout()
        fileBoxLayout.addWidget(self.videoBtn)
        fileBoxLayout.addWidget(self.eventIndexBtn)
        fileBoxLayout.addWidget(self.timeSeriesBtn)

        # Video controls layout
        controlBoxLayout = QHBoxLayout()
        controlBoxLayout.addWidget(self.prevBtn)
        controlBoxLayout.addWidget(self.nextBtn)
        controlBoxLayout.addWidget(self.replayBtn)

        discardBoxLayout = QGridLayout()
        discardBoxLayout.setContentsMargins(0, 0, 0, 0)
        discardBoxLayout.addLayout(controlBoxLayout, 0, 0, 1, 3)
        discardBoxLayout.addWidget(self.saveBtn, 1, 0, 1, 1)
        discardBoxLayout.addWidget(self.discardBtn, 1, 1, 1, 1)
        discardBoxLayout.addWidget(self.undoBtn, 1, 2, 1, 1)

        # Assemble layout
        GUILayout = QGridLayout()
        GUILayout.setContentsMargins(0, 0, 0, 0)
        GUILayout.addWidget(self.videoWidget, 0, 0, 8, 9, alignment=Qt.AlignCenter)
        GUILayout.addWidget(self.plotWindow, 8, 0, 1, 9, alignment=Qt.AlignCenter)
        GUILayout.addWidget(self.eventSlider, 9, 0, 1, 9, alignment=Qt.AlignCenter)
        GUILayout.addWidget(self.eventIDLabel, 10, 0, 1, 9, alignment=Qt.AlignCenter)
        GUILayout.addLayout(fileBoxLayout, 11, 0, 2, 3)
        GUILayout.addLayout(discardBoxLayout, 11, 3, 2, 6)
        GUILayout.setRowStretch(0, 10)
        GUILayout.setRowStretch(7, 2)
        GUILayout.setRowStretch(9, 1)
        GUILayout.setRowStretch(10, 1)

        self.setLayout(GUILayout)
        self.mediaPlayer.setVideoOutput(self.videoWidget)

    # Key presses
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_1:
            FileDialog.open_video(self)
        if event.key() == Qt.Key_2:
            FileDialog.open_event_times(self)
        if event.key() == Qt.Key_3:
            FileDialog.open_time_series(self)

        if event.key() == Qt.Key_Right:
            if self.nextBtn.isEnabled():
                PlaybackControl.next_button_pressed(self)
        elif event.key() == Qt.Key_Left:
            if self.prevBtn.isEnabled():
                PlaybackControl.prev_button_pressed(self)
        elif event.key() == Qt.Key_R:
            if self.replayBtn.isEnabled():
                PlaybackControl.replay_button_pressed(self)

        elif event.key() == Qt.Key_S:
                if self.saveBtn.isEnabled():
                    DiscardEvent.saveDiscardLog(self)
        elif event.key() == Qt.Key_D:
            if self.discardBtn.isEnabled():
                DiscardEvent.updateDiscardLog(self)
        elif event.key() == Qt.Key_U:
            if self.undoBtn.isEnabled():
                DiscardEvent.undoDiscard(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUIWindow()
    window.show()
    sys.exit(app.exec_())
