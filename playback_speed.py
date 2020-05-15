# This Python file uses the following encoding: utf-8


class PlaybackSpeed:
    def setSpeed1x(self):
        self.Fs_adj = int(round(self.Fs))
        self.media_player.setPlaybackRate(1.0)
        self.timer_length = 1000
        self.plot_refresh_rate = self.Fs_adj / 20

    def setSpeed05x(self):
        self.Fs_adj = int(round(self.Fs / 2))
        self.media_player.setPlaybackRate(0.5)
        self.timer_length = 2000
        self.plot_refresh_rate = self.Fs_adj / 20

    def setSpeed025x(self):
        self.Fs_adj = int(round(self.Fs/4))
        self.media_player.setPlaybackRate(0.25)
        self.timer_length = 4000
        self.plot_refresh_rate = self.Fs_adj/20
