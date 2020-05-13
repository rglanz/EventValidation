# Discards the current event. Updates the output csv.

from PyQt5.QtWidgets import QMessageBox
import numpy as np
import os


class DiscardEvent:
    def __init__(self):
        # Check for existing discard log
        self.discard_file_path = self.video_fullfile_name[0]
        self.discard_file_path = self.discard_file_path[0:-4] + "_discard_log.csv"

        if os.path.isfile(self.discard_file_path):
            user_response = QMessageBox.question(self, 'Discard Log', "Use existing discard log for this video?",
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if user_response == QMessageBox.Yes:
                self.discardLog = np.genfromtxt(self.discard_file_path, dtype='int')
            elif user_response == QMessageBox.No:
                self.discardLog = np.ones((self.eventLength, 1))
                self.discardLog.astype(int)

        else:
            self.discardLog = np.ones((self.eventLength, 1))
            self.discardLog.astype(int)

    def updateDiscardLog(self):
        self.discardLog[self.eventID] = 0

        self.saveBtn.setEnabled(True)

    def undoDiscard(self):
        self.discardLog[self.eventID] = 1

    def saveDiscardLog(self):
        np.savetxt(self.discard_file_path, self.discardLog, delimiter=',', fmt='%i')

        self.saveBtn.setEnabled(False)
