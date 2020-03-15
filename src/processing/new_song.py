from enum import Enum
from processing.feature_extraction import get_band


class _States(Enum):
    # When a song is playing
    NORMAL = 1

    # When we dip below a threshold
    DIP = 2

    # Established silence (start taking an average)
    SILENCE = 3


class NewSongDetector:
    """
    Raises a flag when a new song is being detected
    """
    def __init__(self):
        # Rolling average of amplitude
        self.average_amplitude = 0

        # Number of frames seen (to calculate amplitude)
        self.acc_frames = 0

        # Model with an FSM
        self.state = _States.NORMAL

    def update(self, fft):
        """
        Accepts an audio buffer

        Returns
            True if a new song has started
            False while the existing song continues to play
        """
        """
         - Keep track of the average amplitude
         - If we dip below some fraction of the average amplitude, count the
           number of frames we remain below (without pulling the average down).
         - If we stay below for a specified number of frames, raise the SILENCE
           flag.
         - When we are below the silence threshold, keep a new rolling average
           going to get the average silence level. Once we exceed that level,
           raise the NEW_SONG flag and go back to the NORMAL state
        """
        # Calculate amplitude of signal
        amplitude = get_band(fft, 0, 800)

        if self.state == _States.NORMAL:
            # Number of frames seen since entering this state
            self.acc_frames += 1

            # Update rolling average
            self.average_amplitude *= self.acc_frames - 1
            self.average_amplitude += amplitude
            self.average_amplitude /= self.acc_frames

            # Dipping below threshold
            print(self.average_amplitude)
            if amplitude < self.average_amplitude / 4:
                print("below")
                return True

        return False
