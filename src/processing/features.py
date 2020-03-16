from abc import ABC, abstractmethod
from processing.feature_extraction import get_band


class NormalizedFeature(ABC):
    """
    Abstract class for all features whose strengths need to be bound between 0
    and 1.

    Ex: Measuring the level of bass as a value between 0 and 1, where 1 is the
        highest ever seen level
    """
    highest_value = 0.1

    def __init__(self):
        pass

    @abstractmethod
    def _update(self, signal_data):
        """
        Calculate whatever value this feature was intended to return
        """
        pass

    def process(self, signal_data):
        """
        Update the feature with the given raw audio data, normalizing by the
        highest value seen

        Parameter:
            signal_data         Contains some form of raw audio data (fft,
                                audio buffer)
        """
        measurement = self._update(signal_data)

        assert 0 <= measurement <= 1, \
            "Normalized value %f is out of range" % measurement

        if measurement > self.highest_value:
            self.highest_value = measurement

        return measurement / self.highest_value

    def reset(self):
        self.highest_value = 0.1


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


class MidsFeature(NormalizedFeature):
    """
    Measures the middle of the current spectrogram.
    """

    def _update(self, fft):
        return get_band(fft, 200, 800)

    def process(self, fft):
        return super(MidsFeature, self).process(fft)
