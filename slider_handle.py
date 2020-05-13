# Controls slider behavior

from PyQt5.QtWidgets import QSlider
from playback_control import PlaybackControl


class SliderHandle:
    def __init__(self):
        self.eventSlider.setRange(0, self.eventLength - 1)
        self.eventSlider.setTickInterval(round(self.eventLength/20))
        self.eventSlider.setTickPosition(QSlider.TicksBelow)
        self.eventSlider.setVisible(True)
        self.eventSlider.setEnabled(True)

    def slider_changed(self):
        if self.eventSlider.isSliderDown:
            #Update eventID
            self.eventID = self.eventSlider.value()

            # Update label
            self.eventIDLabel.setText('Event ' + str(self.eventID) + ' of ' + str(self.eventLength - 1))
            self.eventIDLabel.repaint()

    def slider_released(self):
        # Play video
        PlaybackControl.replay_button_pressed(self)