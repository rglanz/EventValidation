# Undo a discard event

import numpy as np

class UndoDiscard:
    def restore_event(self):
        self.discardLog[self.eventID] = 1
        self.discardLog.astype(int)

        file_name = self.videoFileName[0]
        np.savetxt(file_name[0:-4] + '_discard_log.csv', self.discardLog, delimiter=',', fmt='%i')
