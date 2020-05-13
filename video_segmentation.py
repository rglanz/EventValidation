# Upon loading of video and event times, create an epoched framework for video times

import numpy as np


class VideoSegmentation:
    def create_epochs(self):
        # Convert event times to frame numbers
        self.frameTimes = self.eventTimesData * self.Fs
        self.frameTimes = self.frameTimes.astype(int)

        self.eventLength = len(self.frameTimes)
        self.frameIndex = np.zeros([self.eventLength, 2])

        for iEvent in np.arange(0, self.eventLength):
            self.frameIndex[iEvent, :] = np.array([self.frameTimes[iEvent] - 50,
                                                   self.frameTimes[iEvent] + 50])
        # Handle boundary conditions
        self.frameIndex[self.frameIndex < 0] = 0    # Trim first event
        self.frameIndex[self.frameIndex > self.videoNFrames] = self.videoNFrames    # Trim last event
        self.frameIndex = self.frameIndex.astype(int)
