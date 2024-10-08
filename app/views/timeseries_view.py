import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from pyqtgraph import GraphicsLayoutWidget
from app.state import TimeSeriesState
from app.utils.schema import Event


class TimeSeriesView(QWidget):
    tmp_vline_created = pyqtSignal(float)
    vline_updated = pyqtSignal(float)

    def __init__(self, state_manager, timeseries_model, parent=None):
        super().__init__(parent)
        self._state_manager = state_manager
        self._timeseries_model = timeseries_model
        self._timeseries_selected_notified = False
        self.timeseries_line = None
        self.vline = None
        self.tmp_vline = None
        self.sweep_vline = None
        self.sweep_timer = QTimer()
        self.sweep_timer.setTimerType(Qt.PreciseTimer)
        self.refresh_rate = 1.0

        # Components
        self.plot_window = GraphicsLayoutWidget()
        self.plot_window.ci.layout.setContentsMargins(0, 0, 0, 0)
        self.plot_window.ci.layout.setSpacing(0)
        self.plot_window.setBackground(None)
        self.plot_window.setMaximumHeight(200)
        self.setMouseTracking(False)

        self.plot_widget = self.plot_window.addPlot(0, 0)
        self.plot_widget.setLabel("bottom", "Time (s)")
        self.plot_widget.setXRange(-0.5, 0.5)
        self.plot_widget.hideAxis("left")
        self.plot_widget.hideButtons()
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.setMenuEnabled(False)

        self.pen = pg.mkPen(color=(0, 0, 0), width=1)
        self.pen_discarded = pg.mkPen(color=(200, 200, 200), width=1)
        self.pen_center = pg.mkPen("k", width=1, style=Qt.DashLine)
        self.pen_hover = pg.mkPen("b", width=1, style=Qt.DashLine)
        self.pen_add = pg.mkPen("g", width=1, style=Qt.DashLine)
        self.pen_sweep = pg.mkPen("r", width=2)
        self.pen_none = pg.mkPen(None)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.plot_window)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Initialization
        self.init_vlines()

        # Signals
        self._state_manager.state_changed.connect(self._on_state_changed)
        self.vline.sigPositionChangeFinished.connect(self.update_vline)
        self.sweep_timer.timeout.connect(self.update_sweep_vline)

    @property
    def timeseries_state(self) -> TimeSeriesState:
        return self._state_manager.get_state().timeseries

    def _on_state_changed(self, state):
        if self.timeseries_state.path and not self._timeseries_selected_notified:
            self._timeseries_selected_notified = True
            self._timeseries_model.load_timeseries()

        if state.timeseries.loaded:
            current_event = state.event.current_event

            self.update_plot(state.timeseries.data, current_event, state.video.fps)

            if state.playback.is_playing:
                self.vline.setMovable(False)
                self.sweep_timer.start(50)
            else:
                if current_event.is_discarded:
                    self.vline.setMovable(False)
                else:
                    self.vline.setMovable(True)
                self.sweep_timer.stop()
                self.sweep_vline.setPos(-0.5)

    def init_vlines(self):
        self.vline = self.plot_widget.addLine(
            x=0,
            y=0,
            pen=self.pen_center,
            movable=False,
            hoverPen=self.pen_hover,
            bounds=[-0.5, 0.5],
        )

        self.sweep_vline = self.plot_widget.addLine(
            x=-0.5, y=0, pen=self.pen_sweep, movable=False, bounds=[-0.5, 0.5]
        )

    def update_plot(self, data: np.ndarray, event: Event, fps: int):
        if self.timeseries_line:
            self.timeseries_line.clear()

        # Calculate indices
        half_window = int(fps / 2)
        start = max(0, event.frame - half_window)
        stop = min(len(data), event.frame + half_window)

        # Slice data
        y = data[start:stop]
        left_pad = max(0, half_window - event.frame)
        right_pad = max(0, (event.frame + half_window) - len(data))
        y = np.pad(y, (left_pad, right_pad), mode="constant", constant_values=np.nan)
        x = np.linspace(-0.5, 0.5, len(y))

        # Plot
        pen = self.pen_discarded if event.is_discarded else self.pen
        self.timeseries_line = self.plot_widget.plot(x, y, pen=pen)
        self.plot_widget.setYRange(np.nanmin(y), np.nanmax(y))

    def update_vline(self):
        self.vline_updated.emit(self.vline.x())
        self.vline.setPos(0)

    def create_tmp_vline(self) -> None:
        self.vline.setMovable(False)

        self.tmp_vline = self.plot_widget.addLine(
            x=0,
            y=0,
            pen=self.pen_center,
            movable=True,
            hoverPen=self.pen_add,
            bounds=[-0.5, 0.5],
        )
        self.tmp_vline.sigPositionChangeFinished.connect(self.create_event)

    def create_event(self):
        self.tmp_vline_created.emit(self.tmp_vline.x())
        self.destroy_tmp_vline()

    def destroy_tmp_vline(self):
        self.tmp_vline.setPos(0)
        self.tmp_vline.setPen(self.pen_none)
        self.tmp_vline.setHoverPen(self.pen_none)
        self.tmp_vline.setMovable(False)

    def update_sweep_vline(self):
        current_position = self.sweep_vline.x()
        step = 0.05 * self.refresh_rate
        self.sweep_vline.setPos(current_position + step)

    def set_refresh_rate(self, rate: float):
        self.refresh_rate = rate
