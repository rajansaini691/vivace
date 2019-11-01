"""
A library of computations whose results are shared by multiple processing units

"""

from numpy.fft import fft
from numpy import absolute
from numpy import column_stack
import numpy as np

def get_fourier(audio_buffer, samplerate):
    """
    Calculates the fourier transform of a given audio buffer and returns a 
    mapping between frequency and amplitude

    Preconditions:
     - Audio buffer size is a power of two
     - Audio buffer has nonzero length

    Returns: 
     - Numpy array of data points of the form (frequency, amplitude)
       - Can be used to construct a spectrogram
    """
    n = int(len(audio_buffer) / 2)
    y = absolute(fft(audio_buffer) / 1000)
    y = y[0:n]
    t = np.linspace(0, samplerate / 2, n)

    fourier = np.column_stack((t,y))
    return fourier
