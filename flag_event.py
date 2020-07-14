# This Python file uses the following encoding: utf-8

from save_output import SaveOutput


class FlagEvent:
    def __init__(self):
        if self.flag_button.isChecked():
            self.event_flags[self.event_ID] = 1

            # Save output
            SaveOutput.saveData(self)

        else:
            self.event_flags[self.event_ID] = 0

            # Save output
            SaveOutput.saveData(self)
