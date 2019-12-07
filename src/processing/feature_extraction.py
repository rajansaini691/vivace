"""
The functions in this library look for different features within an
audio signal.

Ex:
 - Finding the signal's fourier transform
 - Calculating the amplitude of the signal when filtered below 80 hz
"""

from numpy.fft import fft
from numpy import absolute
from numpy import column_stack
import numpy as np
import processing.audio_conf as audio_conf


def get_fourier(audio_buffer):
    """
    Calculates the fourier transform of a given audio buffer and returns a
    mapping between frequency and amplitude

    Preconditions:
     - Audio buffer size is a power of two
     - Audio buffer has nonzero length

    Returns:
     - Numpy array of data points of the form (frequency, amplitude)
       - Can be used to construct a spectrogram
     - None if audio_buffer is empty
    """
    if(len(audio_buffer) <= 0):
        return None

    n = int(len(audio_buffer) / 2)
    y = absolute(fft(audio_buffer) / 1000)
    y = y[0:n]
    f = np.linspace(0, audio_conf.SAMPLERATE / 2, n)

    fourier = column_stack((f, y))
    return fourier


def get_band(fft, low, high):
    """
    Gets the total amplitude of frequencies in the given range
    """
    energy = 0
    for f, y in fft:
        if low < f < high:
            energy += y
    return energy


def get_bass(audio_buf):
    # Update each feature's data
    main_fft = get_fourier(audio_buf)
    bass = get_band(main_fft, 0, 80)
    return bass


def get_mids(audio_buf):
    main_fft = get_fourier(audio_buf)
    mids = get_band(main_fft, 200, 800)
    return mids
