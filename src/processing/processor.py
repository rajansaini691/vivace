from processing.shared_computations import get_fourier
from processing.audio_conf import AudioConf
from processing.bass import VBass

"""
Takes data coming from an audio buffer and generates a list of events
"""


class VProcessor:

    # TODO Store individual processors here
    # (should be their own classes to hold data between frames)
    bass = VBass()

    def update_event_list(self, audio_buffer, audio_conf: AudioConf,
                          event_list):
        """
        Parameters:
            audio_buffer    Raw audio buffer being passed to speakers

            audio_conf      Stores the configuration of the audio buffer
                            (like the SAMPLERATE, buffer size, etc)

            event_list      A list of events that occurred during the current
                            cycle (being written to)
        """
        # Ensure that the buffer exists before processing anything
        if len(audio_buffer) <= 0:
            return

        fft = get_fourier(audio_buffer, audio_conf)

        # Gets the total amount of bass in the signal
        self.bass.get_bass(fft, event_list)
