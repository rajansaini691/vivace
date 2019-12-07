from abc import ABC, abstractmethod


class NormalizedFeature(ABC):
    """
    Abstract class for all features that require some degree of normalization
    with respect to their maximum value

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
        Update the feature with the given raw audio data

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
