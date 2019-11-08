
class VBass:
    """
i   Calculates the total amount of "bass" in the signal as a value between 0
    and 1
    """
    # We are lowpassing the signal with this cutoff frequency (in Hz)
    CUTOFF = 150

    # Stores the maximum amplitude seen, to help with normalization
    max_bass = 0.1

    def get_bass(self, fft, event_list):
        """
        Parameters:
            fft             The fourier transform of the signal

            event_list      Stores the events that occurred. This function
                            updates the BASS attribute (a value between 0 and
                            1)
        """
        # TODO If not accurate, use the buffer directly (rather than an FFT)

        # Sum amplitudes of frequencies below the cutoff frequency
        bass_amplitude = 0
        for x in fft:
            if x[0] < self.CUTOFF:
                bass_amplitude += x[1]

        if bass_amplitude > self.max_bass:
            self.max_bass = bass_amplitude

        event_list.BASS = bass_amplitude / self.max_bass

        assert 0 <= event_list.BASS <= 1, \
            "Normalized BASS value {event_list.BASS} is out of range"
