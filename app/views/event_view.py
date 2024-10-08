import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QLabel,
    QMessageBox,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)
from app.state.app_state import EventState


class EventView(QWidget):
    def __init__(self, state_manager, event_model, parent=None):
        super().__init__(parent)
        self._state_manager = state_manager
        self._event_model = event_model
        self._events_selected_notified = False
        self._events_loaded_notified = False

        # Components
        self.event_label = QLabel()
        self.set_event_label(0, 0)
        self.event_slider = QSlider(QtCore.Qt.Horizontal)
        self.event_slider.setFixedWidth(600)
        self.event_slider.setSingleStep(1)
        self.event_slider.setTickInterval(1)
        self.event_slider.setTickPosition(QSlider.TicksBelow)
        self.event_slider.setEnabled(False)

        self.load_dialog = QMessageBox()
        self.load_dialog.setText("An existing output file was found. Continue scoring?")
        self.continue_button = QPushButton("Continue")
        self.overwrite_button = QPushButton("Overwrite file")
        self.load_dialog.addButton(self.continue_button, QMessageBox.YesRole)
        self.load_dialog.addButton(self.overwrite_button, QMessageBox.NoRole)
        self.load_dialog.setDefaultButton(self.continue_button)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.event_label, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.event_slider)
        self.setLayout(layout)

        # Signals
        self._state_manager.state_changed.connect(self._on_state_changed)
        self.event_slider.sliderMoved.connect(self._on_slider_moved)
        self.event_slider.sliderReleased.connect(self._on_slider_released)

    @property
    def event_state(self) -> EventState:
        return self._state_manager.get_state().event

    def _on_state_changed(self, state):
        if self.event_state.path and not self._events_selected_notified:
            self._events_selected_notified = True
            self._event_model.load_events()

        if state.playback.files_loaded:
            self.event_slider.setEnabled(True)

            if state.playback.is_playing:
                self.event_slider.setEnabled(False)
            else:
                self.event_slider.setEnabled(True)

        if state.event.loaded:
            self._update_view(state.event)

            if not self._events_loaded_notified:
                self._events_loaded_notified = True
                self._load_dialog()

    def _update_view(self, event_state: EventState):
        self.set_event_label(
            event_state.current_event.idx, self._event_model.n_events - 1
        )
        self.set_event_slider_position(event_state.current_event.idx)
        self.set_event_slider_range(self._event_model.n_events - 1)

    def update_view(self):
        event_state = self._state_manager.get_state().event
        self._update_view(event_state)

    def set_event_label(self, curr: int, n_events: int):
        self.event_label.setText(f"Event {curr} of {n_events}")

    def set_event_slider_position(self, position: int):
        self.event_slider.setValue(position)

    def set_event_slider_range(self, maximum: int):
        self.event_slider.setRange(0, maximum)

    def _on_slider_moved(self, value: int):
        self.set_event_label(value, self._event_model.n_events - 1)

    def _on_slider_released(self):
        value = self.event_slider.value()
        self._event_model.set_current_event(value)

    def _load_dialog(self):
        output_path = self._event_model.get_output_path()
        if os.path.isfile(output_path):
            response = self.load_dialog.exec_()

            if response == 0:
                self._event_model.load_events_from_internal_file()
