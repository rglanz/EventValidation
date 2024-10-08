import math
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget


class PlaybackView(QWidget):
    discard_button_toggled = pyqtSignal(bool)
    flag_button_toggled = pyqtSignal(bool)

    def __init__(self, state_manager, parent=None):
        super().__init__(parent)
        self._state_manager = state_manager
        self._updating_discard_button_state = False
        self._updating_flag_button_state = False
        self.playback_rate = 1

        # Components
        self.next_button = QPushButton("Next")
        self.prev_button = QPushButton("Prev")
        self.play_button = QPushButton("Play")
        self.discard_button = QPushButton("Discard Event")
        self.flag_button = QPushButton("Flag Event")
        self.buttons = [
            self.next_button,
            self.prev_button,
            self.play_button,
            self.discard_button,
            self.flag_button,
        ]

        # Layout
        layout = QGridLayout()
        layout.addWidget(self.prev_button, 0, 0, 1, 3)
        layout.addWidget(self.play_button, 0, 3, 1, 3)
        layout.addWidget(self.next_button, 0, 6, 1, 3)
        layout.addWidget(self.discard_button, 1, 6, 1, 3)
        layout.addWidget(self.flag_button, 1, 0, 1, 3)
        self.setLayout(layout)

        # Initialize
        self.discard_button.setCheckable(True)
        self.flag_button.setCheckable(True)
        self.disable_buttons()

        # Signals
        self._state_manager.state_changed.connect(self._on_state_changed)

    def _on_state_changed(self, state):
        if state.playback.files_loaded:
            self.enable_buttons()
            if state.event.current_event and state.event.current_event.is_discarded:
                self.disable_buttons()

            self.update_discard_button_state(state.event.current_event.is_discarded)
            self.update_flag_button_state(state.event.current_event.is_flagged)

            if state.playback.is_playing:
                self.disable_buttons()

    def enable_buttons(self):
        for button in self.buttons:
            button.setEnabled(True)

    def disable_buttons(self):
        for button in self.buttons:
            button.setEnabled(False)

    def update_discard_button_state(self, is_discarded: bool):
        self._updating_discard_button_state = True
        self.discard_button.setChecked(is_discarded)
        if is_discarded:
            self.discard_button.setEnabled(True)
        self._updating_discard_button_state = False

    def on_discard_button_toggled(self, checked):
        if not self._updating_discard_button_state:
            self.discard_button_toggled.emit(checked)

    def update_flag_button_state(self, is_flagged: bool):
        self._updating_flag_button_state = True
        self.flag_button.setChecked(is_flagged)
        self._updating_flag_button_state = False

    def on_flag_button_toggled(self, checked):
        if not self._updating_flag_button_state:
            self.flag_button_toggled.emit(checked)

    def set_playback_rate(self, rate: float):
        if not math.isclose(rate, 1.0):
            self.play_button.setText(f"Play ({round(rate, 2)}x)")
        else:
            self.play_button.setText("Play")

        self.playback_rate = rate
