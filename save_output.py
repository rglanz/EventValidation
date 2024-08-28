# This Python file uses the following encoding: utf-8

import pandas as pd
import numpy as np
import os
from PyQt5.QtWidgets import QMessageBox, QPushButton, QSlider


class SaveOutput:
    def __init__(self):
        self.output_path = self.video_path[0:-4] + '_output.pkl'
        self.output_path_csv = self.video_path[0:-4] + '_output.csv'

        if os.path.isfile(self.output_path):
            project_file_message = QMessageBox()
            project_file_message.setWindowTitle('Output File')
            project_file_message.setText('An existing output file for this video was found.')
            project_file_message.addButton(QPushButton('Overwrite'), QMessageBox.YesRole)
            project_file_message.addButton(QPushButton('Load output file'), QMessageBox.NoRole)
            project_file_message.setDefaultButton(QMessageBox.Yes)

            user_response = project_file_message.exec_()

            if user_response == 1:  # Load discard log
                self.output_df = pd.read_pickle(self.output_path)

                # Create numpy arrays to modify
                self.event_times_data_orig = self.output_df["Orig. Time"].to_numpy(dtype=np.float64)
                self.event_times_data = self.output_df["Adj. Time"].to_numpy(dtype=np.float64)
                self.discard_log = self.output_df["Discarded"].to_numpy(dtype=int)
                self.event_flags = self.output_df["Flagged"].to_numpy(dtype=int)
                self.last_event_ID = self.output_df["Last Event"].to_numpy(dtype=int)

                # Update event ID
                self.event_ID = np.where(self.last_event_ID == 1)[0][0]
                self.event_length = len(self.event_times_data)

                # Set event label
                self.event_ID_label.setText('Event ' + str(self.event_ID) + ' of ' + str(self.event_length - 1))
                self.event_ID_label.repaint()

                # Update center line
                if self.discard_log[self.event_ID]:
                    self.center_line.setMovable(True)
                    self.center_line.setPen(color=(0, 0, 0))
                else:
                    self.center_line.setMovable(False)
                    self.center_line.setPen(color=(220, 220, 220))

                # Update slider
                self.event_slider.setRange(0, self.event_length - 1)
                self.event_slider.setTickInterval(round(self.event_length / 20))
                self.event_slider.setTickPosition(QSlider.TicksBelow)
                self.event_slider.setVisible(True)
                self.event_slider.setEnabled(True)
                self.event_slider.setValue(self.event_ID)

                # Refresh frame
                self.media_player.setPosition(np.round(1000 * self.event_times_data[self.event_ID] / self.Fs) - \
                                              1000 * int(np.round(0.5 * self.Fs)))
                self.media_player.play()
                self.media_player.pause()

            elif user_response == 0: # Overwrite
                # Create numpy arrays to modify

                self.discard_log = np.zeros([np.shape(self.event_times_data)[0]], dtype=int)
                self.last_event_ID = np.zeros([np.shape(self.event_times_data)[0]], dtype=int)
                self.last_event_ID[self.event_ID] = 1
                self.event_flags = np.zeros([np.shape(self.event_times_data)[0]], dtype=int)

                # Create dataframe
                self.output_df = pd.DataFrame({"Orig. Time": self.event_times_data_orig,
                                               "Adj. Time": self.event_times_data,
                                               "Discarded": self.discard_log,
                                               "Flagged": self.event_flags,
                                               "Last Event": self.last_event_ID})

                # Save dataframe
                self.output_df.to_pickle(self.output_path)
                self.output_df.to_csv(self.output_path_csv, sep=',', na_rep=np.nan, index_label="Event")
        else:
            # Create numpy arrays to modify
            self.discard_log = np.zeros([np.shape(self.event_times_data)[0]], dtype=int)
            self.last_event_ID = np.zeros([np.shape(self.event_times_data)[0]], dtype=int)
            self.last_event_ID[self.event_ID] = 1
            self.event_flags = np.zeros([np.shape(self.event_times_data)[0]], dtype=int)

            # Create dataframe
            self.output_df = pd.DataFrame({"Orig. Time": self.event_times_data_orig,
                                           "Adj. Time": self.event_times_data,
                                           "Discarded": self.discard_log,
                                           "Flagged": self.event_flags,
                                           "Last Event": self.last_event_ID})
            # Save dataframe
            self.output_df.to_pickle(self.output_path)
            self.output_df.to_csv(self.output_path_csv, sep=',', na_rep=np.nan, index_label="Event")

    def saveData(self):
        # Update dataframe
        self.output_df = pd.DataFrame({"Orig. Time": self.event_times_data_orig,
                                       "Adj. Time": self.event_times_data,
                                       "Discarded": self.discard_log,
                                       "Flagged": self.event_flags,
                                       "Last Event": self.last_event_ID})

        # Save dataframe
        self.output_df.to_pickle(self.output_path)
        self.output_df.to_csv(self.output_path_csv, sep=',', na_rep=np.nan, index_label="Event")
