"""
A library of computations whose results are shared by multiple processing units

"""

from numpy.fft import fft
from numpy import absolute
from numpy import column_stack
import numpy as np
from audio_conf import AudioConf
from vjack import VJack
from time import sleep
import matplotlib.pyplot as plt


def get_fourier(audio_buffer, audio_conf):
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


def get_fourier_plot(audio_buffer, audio_conf):
    """
    Used for efficient plotting and slicing; returns just the fourier
    coefficients
    """
    if(len(audio_buffer) <= 0):
        return None

    n = int(len(audio_buffer) / 2)
    y = absolute(fft(audio_buffer) / 1000)
    y = y[0:n]

    return y


if __name__ == '__main__':
    print("Debugging feature extractor")

    # Init jack client with default configurations
    audio_conf = AudioConf()
    jack = VJack(audio_conf)

    # Set up matplotlib
    plt.ion()   # Allow live plotting
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Initialize plot
    f = np.linspace(0, audio_conf.SAMPLERATE / 2, 2048)
    y = np.zeros(2048)
    fft_line, = ax.plot(f, y)

    while(True):
        # Get audio buffer
        audio_buf = jack.get_audio_buffer()

        if len(audio_buf) <= 0:
            sleep(0.1)
            continue

        # Get each feature
        fft_points = get_fourier_plot(audio_buf, audio_conf)

        # Graph each feature
        fft_line.set_ydata(fft_points)
        fig.canvas.draw()
        fig.canvas.flush_events()
