# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QSlider
import numpy as np
from playback_control import PlaybackControl
from time_series_plot import TimeSeriesPlot
from save_output import SaveOutput

class SliderHandle:
    def __init__(self):
        self.event_slider.setRange(0, self.event_length - 1)
        self.event_slider.setTickInterval(round(self.event_length/20))
        self.event_slider.setTickPosition(QSlider.TicksBelow)
        self.event_slider.setVisible(True)
        self.event_slider.setEnabled(True)

    def eventSliderChanged(self):
        if self.event_slider.isSliderDown:
            #Update event ID
            self.event_ID = self.event_slider.value()
            self.last_event_ID = np.zeros([np.shape(self.event_times_data)[0]], dtype=int)
            self.last_event_ID[self.event_ID] = 1

            # Update label
            self.event_ID_label.setText('Event ' + str(self.event_ID) + ' of ' + str(self.event_length - 1))
            self.event_ID_label.repaint()

    def eventSliderReleased(self):
        # Update time-series plot
        if hasattr(self, 'time_series_data'):
            TimeSeriesPlot.updateTimeSeries(self)

        # Play video
        PlaybackControl.replayButtonPressed(self)

        # Save position
        SaveOutput.saveData(self)
