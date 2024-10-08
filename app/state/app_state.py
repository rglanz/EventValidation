from dataclasses import dataclass, field
from typing import Optional
import numpy as np
from app.utils.schema import Event


@dataclass
class PlaybackState:
    files_loaded: bool = False
    is_playing: bool = False
    rate: float = 1.0


@dataclass
class VideoState:
    loaded: bool = False
    path: str = ""
    fps: float = 0
    width: int = 0
    height: int = 0


@dataclass
class EventState:
    loaded: bool = False
    path: str = ""
    current_event: Optional[Event] = None


@dataclass
class TimeSeriesState:
    loaded: bool = False
    path: str = ""
    data: np.ndarray = field(default_factory=lambda: np.array([]))


@dataclass
class AppState:
    playback: PlaybackState = field(default_factory=PlaybackState)
    video: VideoState = field(default_factory=VideoState)
    event: EventState = field(default_factory=EventState)
    timeseries: TimeSeriesState = field(default_factory=TimeSeriesState)
