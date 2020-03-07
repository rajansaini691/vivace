from processing.feature import NormalizedFeature
from processing.feature_extraction import get_band


class BassFeature(NormalizedFeature):
    """
    Measures the total amount of "bass" in the current audio snapshot.
    """
    # We are lowpassing the signal with this cutoff frequency (in Hz)
    CUTOFF = 80

    def _update(self, fft):
        """
        Measures the bass by comparing the current amount with the maximum
        value seen
        """
        return get_band(fft, 0, 80)

    def process(self, fft):
        """
        Parameters:
            fft             The fourier transform of the signal
        """
        return super(BassFeature, self).process(fft)
