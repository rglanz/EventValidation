# This Python file uses the following encoding: utf-8


class PlaybackSpeed:
    def setSpeed1x(self):
        self.playback_speed = 1

        self.Fs_adj = int(round(self.Fs))
        self.media_player.setPlaybackRate(1.0)
        self.timer_length = 1000
        self.plot_refresh_rate = self.Fs_adj / 20

        self.replay_button.setText("Replay")

    def setSpeed05x(self):
        self.playback_speed = 0.5

        self.Fs_adj = int(round(self.Fs / 2))
        self.media_player.setPlaybackRate(0.5)
        self.timer_length = 2000
        self.plot_refresh_rate = self.Fs_adj / 20

        self.replay_button.setText("Replay (0.5x)")

    def setSpeed025x(self):
        self.playback_speed = 0.25

        self.Fs_adj = int(round(self.Fs/4))
        self.media_player.setPlaybackRate(0.25)
        self.timer_length = 4000
        self.plot_refresh_rate = self.Fs_adj/20

        self.replay_button.setText("Replay (0.25x)")
