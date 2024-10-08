import csv
import os
from dataclasses import asdict, replace
from typing import List, Optional
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal
from app.state.app_state import EventState
from app.utils.schema import Event


class EventModel(QObject):
    event_created = pyqtSignal()

    def __init__(self, state_manager):
        super().__init__()
        self._state_manager = state_manager
        self.events: List[Event] = []
        self.n_events: int = 0

    @property
    def event_state(self) -> EventState:
        return self._state_manager.get_state().event

    def load_events(self):
        path = self.event_state.path
        fps = self._state_manager.get_state().video.fps

        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                raw_events = np.genfromtxt(f, dtype=float, delimiter=",")
                self.events = [
                    Event(idx=i, frame=int(t * fps), time=t, original_time=t)
                    for i, t in enumerate(raw_events)
                ]
                self.n_events = len(self.events)

            self._state_manager.update_state(
                event=EventState(loaded=True, path=path, current_event=self.events[0])
            )
            return True
        except Exception as e:
            print(f"Error loading events: {e}")
            state = replace(self.event_state, loaded=False)
            self._state_manager.update_state(event=state)
            return False

    def _update_event_state(self, event: Event):
        updated_state = replace(self.event_state, current_event=event)
        self._state_manager.update_state(event=updated_state)
        self.save_events()

    def set_current_event(self, idx: int):
        next_event = self.events[idx]
        self._update_event_state(next_event)

    def increment_event(self):
        current_event = self.event_state.current_event
        if current_event.idx < self.n_events - 1:
            next_event = self.events[current_event.idx + 1]
            self._update_event_state(next_event)

    def decrement_event(self):
        current_event = self.event_state.current_event
        if 0 < current_event.idx:
            prev_event = self.events[current_event.idx - 1]
            self._update_event_state(prev_event)

    def create_event(self, time: float):
        current_event = self.event_state.current_event
        fps = self._state_manager.get_state().video.fps

        # Create new event
        new_time = current_event.time + time
        new_index = current_event.idx + (1 if time >= 0 else 0)
        if new_time < 0:
            print("Cannot create an event before time zero")
            return

        new_event = Event(
            idx=new_index,
            frame=int(round(new_time * fps)),
            time=new_time,
            original_time=np.nan,
        )

        # Update events list
        self.events.insert(new_index, new_event)
        self.n_events += 1
        for i in range(new_index + 1, len(self.events)):
            self.events[i].idx = i

        # Update current event state
        if time < 0:
            updated_event = replace(current_event, idx=new_index)
            self._update_event_state(updated_event)
        else:
            self.save_events()

        self.event_created.emit()

    def update_event_time(self, relative_time: float):
        current_event = self.event_state.current_event
        fps = self._state_manager.get_state().video.fps

        new_time = current_event.time + relative_time
        new_frame = int(round(new_time * fps))
        if new_time >= 0:
            updated_event = replace(current_event, time=new_time, frame=new_frame)
            self.events[current_event.idx] = updated_event
            self._update_event_state(updated_event)
        else:
            print("Cannot move an event before time zero.")

    def flag_event(self):
        current_event = self.event_state.current_event
        updated_event = replace(
            current_event, is_flagged=(not current_event.is_flagged)
        )
        self.events[updated_event.idx] = updated_event
        self._update_event_state(updated_event)

    def discard_event(self):
        current_event = self.event_state.current_event
        updated_event = replace(
            current_event, is_discarded=(not current_event.is_discarded)
        )
        self.events[updated_event.idx] = updated_event
        self._update_event_state(updated_event)

    def label_event(self, label: str):
        current_event = self.event_state.current_event
        updated_event = replace(current_event, label=label)
        self.events[updated_event.idx] = updated_event
        self._update_event_state(updated_event)

    def get_output_path(self):
        video_path = self._state_manager.get_state().video.path
        return os.path.splitext(video_path)[0] + "_qs.csv"

    def save_events(self) -> None:
        output_path = self.get_output_path()
        with open(output_path, "w", newline="") as csvfile:
            fieldnames = [
                "id",
                "time",
                "original_time",
                "label",
                "is_flagged",
                "is_discarded",
                "is_current",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            current_event = self.event_state.current_event
            for event in self.events:
                event_dict = asdict(event)
                event_dict["is_current"] = event.idx == current_event.idx
                event_dict["id"] = event_dict.pop("idx")

                # Remove any keys not in fieldnames
                event_dict = {k: v for k, v in event_dict.items() if k in fieldnames}

                writer.writerow(event_dict)

    def load_events_from_internal_file(self):
        file_path = self.get_output_path()
        with open(file_path, "r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            new_events: List[Event] = []
            current_event_idx: Optional[int] = None
            fps = self._state_manager.get_state().video.fps

            for row in reader:
                event = Event(
                    idx=int(row["id"]),
                    time=float(row["time"]),
                    frame=int(round(float(row["time"]) * fps)),
                    original_time=float(row["original_time"]),
                    label=str(row["label"]),
                    is_flagged=row["is_flagged"].lower() == "true",
                    is_discarded=row["is_discarded"].lower() == "true",
                )
                new_events.append(event)

                if row["is_current"].lower() == "true":
                    current_event_idx = event.idx

        self.events = new_events
        if current_event_idx is not None:
            self.set_current_event(current_event_idx)
        elif new_events:
            self._update_event_state(new_events[0])
