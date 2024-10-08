from dataclasses import replace
import numpy as np
from PyQt5.QtCore import QObject
from app.state.app_state import TimeSeriesState


class TimeSeriesModel(QObject):
    def __init__(self, state_manager):
        super().__init__()
        self.state_manager = state_manager

    @property
    def timeseries_state(self) -> TimeSeriesState:
        return self.state_manager.get_state().timeseries

    def load_timeseries(self):
        path = self.timeseries_state.path
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                data = np.genfromtxt(f, dtype=float, delimiter=",")

            self.state_manager.update_state(
                timeseries=TimeSeriesState(loaded=True, path=path, data=data)
            )
            return True
        except Exception as e:
            print(f"Timeseries failed to load: {e}")
            state = replace(self.timeseries_state, loaded=False)
            self.state_manager.update_state(timeseries=state)
            return False
