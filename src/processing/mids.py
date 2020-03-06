from processing.feature import NormalizedFeature
from processing.feature_extraction import get_band


class MidsFeature(NormalizedFeature):
    """
    Measures the middle of the current spectrogram.
    """

    def _update(self, fft):
        return get_band(fft, 200, 800)

    def process(self, fft):
        return super(MidsFeature, self).process(fft)
