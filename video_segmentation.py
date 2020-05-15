# This Python file uses the following encoding: utf-8

import numpy as np


class VideoSegmentation:
    def __init__(self):
        # Convert event times to frame numbers
        self.frame_times = np.round(self.event_times_data * self.Fs)
        self.frame_times = self.frame_times.astype(int)

        self.frame_index = np.zeros([self.event_length, 2])

        for iEvent in np.arange(0, self.event_length):
            self.frame_index[iEvent, :] = np.array([self.frame_times[iEvent] - int(round(self.Fs/2)),
                                                    self.frame_times[iEvent] + int(round(self.Fs/2))])
        # Handle boundary conditions
        self.frame_index[self.frame_index < 0] = 0    # Trim first event
        self.frame_index[self.frame_index > self.video_n_frames] = self.video_n_frames    # Trim last event
        self.frame_index = self.frame_index.astype(int)
