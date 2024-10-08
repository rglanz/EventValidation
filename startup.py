import logging
import sys
from dataclasses import replace
from typing import Any, Dict
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QGridLayout,
    QMainWindow,
    QWidget,
)
from app.models import EventModel, TimeSeriesModel, VideoModel
from app.state import StateManager
from app.views import (
    EventView,
    FileView,
    LabelView,
    PlaybackView,
    TimeSeriesView,
    VideoView,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class MainWindow(QMainWindow):
    WINDOW_WIDTH_RATIO = 0.50
    WINDOW_HEIGHT_RATIO = 0.67
    WINDOW_X_RATIO = 0.25
    WINDOW_Y_RATIO = 0.16
    VIDEO_MAX_HEIGHT_RATIO = 0.5

    def __init__(self, parent: QWidget = None) -> None:
        super(MainWindow, self).__init__(parent)
        logging.info("Initializing MainWindow")

        self.screen_width, self.screen_height = self._get_screen_dimensions()
        self.playback_rate: float = 1.0
        self.hotkeys: Dict[int, Any] = {}

        self._initialize_components()
        self._setup_ui()
        self._setup_signals()
        self._setup_hotkeys()

        logging.info("MainWindow initialization complete")

    def _initialize_components(self) -> None:
        logging.info("Initializing components")
        self.state_manager = StateManager()

        # Models
        self.video_model = VideoModel(self.state_manager)
        self.event_model = EventModel(self.state_manager)
        self.timeseries_model = TimeSeriesModel(self.state_manager)

        # Views
        self.file_view = FileView(self.state_manager)
        self.video_view = VideoView(self.state_manager, self.video_model)
        self.event_view = EventView(self.state_manager, self.event_model)
        self.timeseries_view = TimeSeriesView(self.state_manager, self.timeseries_model)
        self.playback_view = PlaybackView(self.state_manager)
        self.label_view = LabelView()

    def _setup_ui(self) -> None:
        logging.info("Setting up UI")
        self.setWindowTitle("QuickScore")
        self._set_window_geometry()
        self._setup_layout()

    @staticmethod
    def _get_screen_dimensions() -> tuple[int, int]:
        screen = QDesktopWidget().screenGeometry(-1)
        return screen.width(), screen.height()

    def _set_window_geometry(self) -> None:
        width = int(self.WINDOW_WIDTH_RATIO * self.screen_width)
        height = int(self.WINDOW_HEIGHT_RATIO * self.screen_height)
        x = int(self.WINDOW_X_RATIO * self.screen_width)
        y = int(self.WINDOW_Y_RATIO * self.screen_height)
        self.setGeometry(x, y, width, height)

        max_video_height = int(self.VIDEO_MAX_HEIGHT_RATIO * self.screen_height)
        self.video_view.set_max_height(max_video_height)

    def _setup_layout(self) -> None:
        main_layout = QGridLayout()
        main_layout.addWidget(self.video_view, 0, 0, 8, 9, alignment=Qt.AlignCenter)
        main_layout.addWidget(
            self.timeseries_view.plot_window, 8, 0, 1, 9, alignment=Qt.AlignCenter
        )
        main_layout.addWidget(self.event_view, 9, 0, 1, 9, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.playback_view, 11, 1, 1, 7)

        main_layout.setRowStretch(0, 10)
        main_layout.setRowStretch(7, 2)
        main_layout.setRowStretch(9, 1)
        main_layout.setRowStretch(11, 1)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _setup_signals(self) -> None:
        logging.info("Setting up signals")

        # Video
        self.video_view.video_resized.connect(self.resize_window)

        # Events
        self.event_model.event_created.connect(self.event_view.update_view)

        # TimeSeries
        self.timeseries_view.vline_updated.connect(self.event_model.update_event_time)
        self.timeseries_view.tmp_vline_created.connect(self.event_model.create_event)

        # Playback
        self.playback_view.next_button.pressed.connect(self.handle_next)
        self.playback_view.prev_button.pressed.connect(self.handle_prev)
        self.playback_view.play_button.pressed.connect(self.start_timer)
        self.playback_view.discard_button.toggled.connect(
            self.playback_view.on_discard_button_toggled
        )
        self.playback_view.discard_button_toggled.connect(
            self.event_model.discard_event
        )
        self.playback_view.flag_button.toggled.connect(
            self.playback_view.on_flag_button_toggled
        )
        self.playback_view.flag_button_toggled.connect(self.event_model.flag_event)

    def resize_window(self, width: int) -> None:
        logging.info(f"Resizing window to width: {width}")
        new_x = int(0.5 * self.screen_width - 0.5 * width)
        new_height = int(self.WINDOW_HEIGHT_RATIO * self.screen_height)
        self.setGeometry(
            new_x, int(self.WINDOW_Y_RATIO * self.screen_height), width, new_height
        )

    def handle_next(self) -> None:
        self.event_model.increment_event()
        self.start_timer()

    def handle_prev(self) -> None:
        self.event_model.decrement_event()
        self.start_timer()

    def show_label_dialog(self):
        if self.state_manager.get_state().event.current_event:
            response = self.label_view.exec_()
            if response:
                label = self.label_view.parse_label()
                self.event_model.label_event(label)

    def _setup_hotkeys(self) -> None:
        self.hotkeys = {
            Qt.Key_1: self.file_view.select_video,
            Qt.Key_2: self.file_view.select_events,
            Qt.Key_3: self.file_view.select_timeseries,
            Qt.Key_Left: self.handle_prev,
            Qt.Key_Right: self.handle_next,
            Qt.Key_Alt: self.timeseries_view.create_tmp_vline,
            Qt.Key_Comma: lambda: self.set_playback_rate(1.0),
            Qt.Key_Period: lambda: self.set_playback_rate(0.5),
            Qt.Key_Slash: lambda: self.set_playback_rate(0.25),
            Qt.Key_Space: self.start_timer,
            Qt.Key_F: self.event_model.flag_event,
            Qt.Key_D: self.event_model.discard_event,
            Qt.Key_Shift: self.show_label_dialog,
        }

    def start_timer(self) -> None:
        if not self.state_manager.get_state().event.current_event.is_discarded:
            msec = int(round(1000 / self.playback_rate))
            QTimer.singleShot(msec, Qt.PreciseTimer, self.stop_timer)
            playback_state = replace(
                self.state_manager.get_state().playback, is_playing=True
            )
            self.state_manager.update_state(playback=playback_state)

    def stop_timer(self) -> None:
        playback_state = replace(
            self.state_manager.get_state().playback, is_playing=False
        )
        self.state_manager.update_state(playback=playback_state)

    def set_playback_rate(self, rate: float) -> None:
        self.playback_rate = rate
        self.video_model.set_playback_rate(self.playback_rate)
        self.timeseries_view.set_refresh_rate(self.playback_rate)
        self.playback_view.set_playback_rate(self.playback_rate)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if not self.state_manager.get_state().playback.is_playing:
            key = event.key()
            if key in self.hotkeys:
                self.hotkeys[key]()
            else:
                super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Alt:
            self.timeseries_view.destroy_tmp_vline()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            self.handle_next()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
