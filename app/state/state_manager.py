from PyQt5.QtCore import QObject, pyqtSignal
from app.state import AppState


class StateManager(QObject):
    state_changed = pyqtSignal(AppState)

    def __init__(self):
        super().__init__()
        self._state = AppState()

    def get_state(self) -> AppState:
        return self._state

    def update_state(self, **kwargs):
        state_changed = False
        for key, value in kwargs.items():
            if hasattr(self._state, key):
                current_value = getattr(self._state, key)
                if current_value != value:
                    setattr(self._state, key, value)
                    state_changed = True

        if state_changed:
            self.state_changed.emit(self._state)
