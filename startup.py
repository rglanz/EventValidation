# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QSlider, QAction, QMainWindow, \
                            QMessageBox, QDesktopWidget
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPalette
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg
import sys
from file_dialog import FileDialog
from playback_control import PlaybackControl
from discard_event import DiscardEvent
from slider_handle import SliderHandle
from playback_speed import PlaybackSpeed


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        _, _, self.screen_width, self.screen_height = QDesktopWidget().screenGeometry(-1).getRect()
        self.setGeometry(0.25*self.screen_width, 0.125*self.screen_height,
                         0.50*self.screen_width, 0.75*self.screen_height)

        self.createGUIStyle()
        self.createGUIElements()
        self.createGUILayout()

    def createGUIStyle(self):
        self.palette = QPalette()

        self.palette.setColor(QPalette.Background, Qt.white)
        self.palette.setColor(QPalette.WindowText, Qt.black)
        self.palette.setColor(self.menuBar().backgroundRole(), Qt.white)

        self.setPalette(self.palette)

    def createGUIElements(self):
        # Video object
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)

        # File selection menu bar
        self.menuBar().setNativeMenuBar(False)  # Enable menu bar in mac
        self.file_menu = self.menuBar().addMenu('File')

        self.video_menu_action = QAction(self)
        self.video_menu_action.setText('Video')
        self.file_menu.addAction(self.video_menu_action)
        self.video_menu_action.triggered.connect(lambda: FileDialog.openVideo(self))

        self.event_times_menu_action = QAction(self)
        self.event_times_menu_action.setText('Event Times')
        self.event_times_menu_action.setEnabled(False)
        self.file_menu.addAction(self.event_times_menu_action)
        self.event_times_menu_action.triggered.connect(lambda: FileDialog.openEventTimes(self))

        self.time_series_menu_action = QAction(self)
        self.time_series_menu_action.setText('Time-series (optional)')
        self.time_series_menu_action.setEnabled(False)
        self.file_menu.addAction(self.time_series_menu_action)
        self.time_series_menu_action.triggered.connect(lambda: FileDialog.openTimeSeries(self))
        self.timer_length = 1000

        # Playback speed menu bar
        self.playback_speed_menu = self.menuBar().addMenu('Playback')
        self.playback_speed = 1

        self.speed_1x_action = QAction(self)
        self.speed_1x_action.setText('1.0x Speed')
        self.speed_1x_action.setEnabled(False)
        self.playback_speed_menu.addAction(self.speed_1x_action)
        self.speed_1x_action.triggered.connect(lambda: PlaybackSpeed.setSpeed1x(self))

        self.speed_05x_action = QAction(self)
        self.speed_05x_action.setText('0.5x Speed')
        self.speed_05x_action.setEnabled(False)
        self.playback_speed_menu.addAction(self.speed_05x_action)
        self.speed_05x_action.triggered.connect(lambda: PlaybackSpeed.setSpeed05x(self))

        self.speed_025x_action = QAction(self)
        self.speed_025x_action.setText('0.25x Speed')
        self.speed_025x_action.setEnabled(False)
        self.playback_speed_menu.addAction(self.speed_025x_action)
        self.speed_025x_action.triggered.connect(lambda: PlaybackSpeed.setSpeed025x(self))

        # Hotkeys menu bar
        self.hotkeys_menu = self.menuBar().addAction('Hotkeys')
        self.hotkeys_menu.triggered.connect(self.hotkeysHint)

        # Time-series object
        self.plot_window = GraphicsLayoutWidget()
        self.plot_window.ci.layout.setContentsMargins(0, 0, 0, 0)
        self.plot_window.ci.layout.setSpacing(0)
        self.plot_window.setBackground(None)

        self.plot_widget = self.plot_window.addPlot(0, 0)
        self.plot_widget.setLabel('bottom', "Time (s)")
        self.plot_widget.setXRange(-0.5, 0.5)
        self.plot_widget.hideAxis('left')
        self.plot_widget.hideButtons()
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.setMenuEnabled(False)

        # EventID label
        self.event_ID = 0
        self.event_ID_label = QLabel('')

        # Slider
        self.event_slider = QSlider(Qt.Horizontal)
        self.event_slider.setFixedWidth(600)
        self.event_slider.setValue(0)
        self.event_slider.setRange(0, 20)
        self.event_slider.setSingleStep(1)
        self.event_slider.setTickInterval(1)
        self.event_slider.setTickPosition(QSlider.TicksBelow)
        self.event_slider.setEnabled(False)
        self.event_slider.valueChanged.connect(lambda: SliderHandle.eventSliderChanged(self))
        self.event_slider.sliderReleased.connect(lambda: SliderHandle.eventSliderReleased(self))

        # Buttons
        self.next_button = QPushButton('Next')
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(lambda: PlaybackControl.nextButtonPressed(self))

        self.prev_button = QPushButton('Prev')
        self.prev_button.setEnabled(False)
        self.prev_button.clicked.connect(lambda: PlaybackControl.prevButtonPressed(self))

        self.replay_button = QPushButton('Play') # Is set to 'Play' until first playback occurs
        self.replay_button.setEnabled(False)
        self.replay_button.clicked.connect(lambda: PlaybackControl.replayButtonPressed(self))

        self.discard_button = QPushButton('Discard Event')
        self.discard_button.setEnabled(False)
        self.discard_button.setCheckable(True)
        self.discard_button.setChecked(False)
        self.discard_button.clicked.connect(lambda: DiscardEvent.discardEvent(self))

    def createGUILayout(self):
        # Control layout
        self.control_layout = QGridLayout()
        self.control_layout.addWidget(self.prev_button, 0, 0, 1, 3)
        self.control_layout.addWidget(self.replay_button, 0, 3, 1, 3)
        self.control_layout.addWidget(self.next_button, 0, 6, 1, 3)
        self.control_layout.addWidget(self.discard_button, 1, 6, 1, 3)

        # Media layout
        self.media_layout = QGridLayout()
        self.media_layout.addWidget(self.video_widget, 0, 0, 8, 9, alignment=Qt.AlignCenter)
        self.media_layout.addWidget(self.plot_window, 8, 0, 1, 9, alignment=Qt.AlignCenter)
        self.media_layout.addWidget(self.event_ID_label, 9, 0, 1, 9, alignment=Qt.AlignCenter)
        self.media_layout.addWidget(self.event_slider, 10, 0, 1, 9, alignment=Qt.AlignCenter)
        self.media_layout.addLayout(self.control_layout, 11, 1, 1, 7)
        self.media_layout.setRowStretch(0, 10)
        self.media_layout.setRowStretch(7, 2)
        self.media_layout.setRowStretch(9, 1)
        self.media_layout.setRowStretch(10, 1)

        # Add GUI to layout
        self.media_widget = QWidget()
        self.media_widget.setLayout(self.media_layout)
        self.setCentralWidget(self.media_widget)

    def hotkeysHint(self):
        hotkey_message_box = QMessageBox()
        hotkey_message_box.setWindowTitle('Hotkeys')
        hotkey_message_box.setText("Open video file:  1" +
                                   "\nOpen event times file:  2" +
                                   "\nOpen time-series file:  3"
                                   "\n\nPrevious Event:  Right arrow" +
                                   "\nNext Event:  Left arrow" +
                                   "\nReplay Event:  R" +
                                   "\nDiscard Event (or undo):  D" +
                                   "\n\n1.0x Speed:  ," +
                                   "\n0.5x Speed:  ." +
                                   "\n0.25x Speed:  /")
        hotkey_message_box.exec_()

    def keyPressEvent(self, event):
        # File Editor
        if event.key() == Qt.Key_1:
            FileDialog.openVideo(self)
        if event.key() == Qt.Key_2:
            FileDialog.openEventTimes(self)
        if event.key() == Qt.Key_3:
            FileDialog.openTimeSeries(self)

        # Playback
        if event.key() == Qt.Key_Right:
            if self.next_button.isEnabled():
                PlaybackControl.nextButtonPressed(self)
        elif event.key() == Qt.Key_Left:
            if self.prev_button.isEnabled():
                PlaybackControl.prevButtonPressed(self)
        elif event.key() == Qt.Key_R:
            if self.replay_button.isEnabled():
                PlaybackControl.replayButtonPressed(self)
        # Discard
        elif event.key() == Qt.Key_D:
            if self.discard_button.isEnabled():
                self.discard_button.toggle()
                self.discard_button.repaint()
                DiscardEvent.discardEvent(self)

        # Playback speed
        if event.key() == Qt.Key_Comma:
            if self.speed_1x_action.isEnabled():
                PlaybackSpeed.setSpeed1x(self)
        if event.key() == Qt.Key_Period:
            if self.speed_05x_action.isEnabled():
                PlaybackSpeed.setSpeed05x(self)
        if event.key() == Qt.Key_Slash:
            if self.speed_025x_action.isEnabled():
                PlaybackSpeed.setSpeed025x(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
