import os
from dataclasses import replace
from PyQt5.QtWidgets import QFileDialog, QWidget


class FileView(QWidget):
    def __init__(self, state_manager):
        super().__init__()
        self._state_manager = state_manager
        self.default_dir = ""
        self._files_loaded_notified = False

        # Signals
        self._state_manager.state_changed.connect(self._on_state_changed)

    def _on_state_changed(self, state):
        if self._files_loaded_notified:
            return

        is_video_loaded = state.video.loaded
        is_events_loaded = state.event.loaded
        is_timeseries_loaded = state.timeseries.loaded
        if is_video_loaded and is_events_loaded and is_timeseries_loaded:
            self._files_loaded_notified = True
            playback_state = replace(state.playback, files_loaded=True)
            self._state_manager.update_state(playback=playback_state)

    def select_video(self):
        video_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video",
            self.default_dir,
            filter="Videos (*.mp4 *.avi *.mov *.flv *.wmv)",
        )
        if video_path:
            self.default_dir = os.path.dirname(video_path)
            video_state = replace(
                self._state_manager.get_state().video, path=video_path
            )
            self._state_manager.update_state(video=video_state)
        return video_path

    def select_events(self):
        events_path, _ = QFileDialog.getOpenFileName(
            self, "Select Events File", self.default_dir, filter="CSV Files (*.csv)"
        )
        if events_path:
            event_state = replace(
                self._state_manager.get_state().event, path=events_path
            )
            self._state_manager.update_state(event=event_state)
        return events_path

    def select_timeseries(self):
        timeseries_path, _ = QFileDialog.getOpenFileName(
            self, "Select Timeseries File", self.default_dir, filter="CSV Files (*.csv)"
        )
        if timeseries_path:
            timeseries_state = replace(
                self._state_manager.get_state().timeseries, path=timeseries_path
            )
            self._state_manager.update_state(timeseries=timeseries_state)
        return timeseries_path
