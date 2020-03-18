from processing.feature_extraction import get_fourier
from processing.features import BassFeature, MidsFeature
from processing.new_song import NewSongDetector

"""
Takes data coming from an audio buffer and generates a list of events
"""


class VProcessor:

    bass = BassFeature()
    mids = MidsFeature()
    new_song_detector = NewSongDetector()

    def update_event_list(self, audio_buffer, event_list):
        """
        Parameters:
            audio_buffer    Raw audio buffer being passed to speakers

            event_list      A list of events that occurred during the current
                            cycle (being written to)
        """
        # Ensure that the buffer exists before processing anything
        if len(audio_buffer) <= 0:
            return

        fft = get_fourier(audio_buffer)

        # Update features
        event_list.BASS = self.bass.process(fft)
        event_list.MIDS = self.mids.process(fft)
        event_list.NEW_SONG = self.new_song_detector.update(fft)

        # Update higher-level-features
        event_list.KICK = event_list.BASS > 0.2

        # Reset the max value of each normalized feature
        if event_list.NEW_SONG:
            self.bass.reset()
            self.mids.reset()
