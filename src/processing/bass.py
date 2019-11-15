
class VBass:
    """
i   Measures the total amount of "bass" in the current audio snapshot.
    The unexposed functions test different ways to normalize this value.
    """
    # We are lowpassing the signal with this cutoff frequency (in Hz)
    CUTOFF = 80

    # Stores the maximum amplitude seen, to help with normalization
    max_bass = 0.1

    def _get_bass_max(self, fft):
        """
        Measures the bass by comparing the current amount with the maximum
        value seen
        """
        # Sum amplitudes of frequencies below the cutoff frequency
        bass_amplitude = 0
        for x in fft:
            if x[0] < self.CUTOFF:
                bass_amplitude += x[1]

        if bass_amplitude > self.max_bass:
            self.max_bass = bass_amplitude

        return bass_amplitude / self.max_bass

    def _get_bass_proportional(self, fft):
        """
        Normalizes the current amount of bass by the total amplitude of the
        current audio buffer (rather keeping track of a max value)
        """
        # Gets total signal amplitude and bass amplitude
        bass_amplitude = 0.0
        total_amplitude = 0.1
        for x in fft:
            if x[0] < self.CUTOFF:
                bass_amplitude += x[1]
            total_amplitude += x[1]

        return bass_amplitude / total_amplitude

    def get_bass(self, fft, event_list):
        """
        Parameters:
            fft             The fourier transform of the signal

            event_list      Stores the events that occurred. This function
                            updates the BASS attribute (a value between 0 and
                            1)
        """
        # TODO If not accurate, use the buffer directly (rather than an FFT)

        event_list.BASS = self._get_bass_max(fft)

        assert 0 <= event_list.BASS <= 1, \
            "Normalized BASS value %f is out of range" % (event_list.BASS)
