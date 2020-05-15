# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QSlider
from playback_control import PlaybackControl


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

            # Update label
            self.event_ID_label.setText('Event ' + str(self.event_ID) + ' of ' + str(self.event_length - 1))
            self.event_ID_label.repaint()

    def eventSliderReleased(self):
        # Play video
        PlaybackControl.replayButtonPressed(self)