"""
Run this script to debug the feature calculations
"""
import numpy as np
from numpy.fft import fft
from numpy import absolute
from vjack import VJack
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from functools import partial
from feature_extraction import get_bass
from audio_conf import AudioConf


class FeaturePlot:
    """
    Abstracts common behavior between features when plotting them for code
    efficiency
    """
    def __init__(self, update_func, axis, dimension, initial_data=None,
                 buffered=False, buffer_length=100, xlim=None, ylim=None):
        """
        Parameters:

        update_func         The function that generates this feature's data. It
                            must accept an audio_buffer and audio_conf as its
                            arguments.

        axis                Matplotlib axis to be drawn on

        dimension           Number of dimensions being input to the plotter

        initial_data        Example data matching the feature's shape for
                            initialization (if 2D should be a pair of numpy
                            arrays of values along each axis)

        buffered            If set to True, previous values of the feature will
                            be plotted as well. If we buffer, there is no need
                            to pass initial data.

        buffer_length       Number of datapoints to be buffered

        xlim                The x-axis view limits

        ylim                The y-axis view limits
        """
        self.update_func = update_func

        if xlim:
            axis.set_xlim(xlim)
        if ylim:
            axis.set_ylim(ylim)

        self.buffered = buffered

        if buffered:
            self.data = [0] * 100
        else:
            self.data = initial_data

        if dimension == 1:
            self.line, = axis.plot(self.data)
        else:
            self.line, = axis.plot(initial_data[0], initial_data[1])

    def update(self, audio_buffer, audio_conf):
        new_data = self.update_func(audio_buffer, audio_conf)

        if self.buffered:
            self.data = self.data[1:] + [new_data]
        else:
            self.data = new_data

        self.line.set_ydata(self.data)
        return self.line


# New version
def _update_plot(jack: VJack, audio_conf, features, i):
    # Get audio buffer
    audio_buf = jack.get_audio_buffer()
    return [feature.update(audio_buf, audio_conf) for feature in features]

def get_fourier_plot(audio_buffer, audio_conf):
    """
    Calculates the fourier transform optimized for plotting and slicing.

    Returns the coefficients as a pair of numpy arrays, separating the bin
    frequencies from the amplitudes
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
    fig = plt.figure()

    # Init axes
    fft_ax = fig.add_subplot(121)
    bass_ax = fig.add_subplot(122)

    # Init canvas
    fig.show()
    fig.canvas.draw()

    # Initialize plots with data
    f = np.linspace(0, audio_conf.SAMPLERATE / 2, AudioConf.BUFFER_SIZE//2)
    y = np.zeros(AudioConf.BUFFER_SIZE//2)

    fft_feature = FeaturePlot(get_fourier_plot, fft_ax, 2, initial_data=(f, y),
                              xlim=[0, 5000], ylim=[0, 0.5])

    bass_feature = FeaturePlot(get_bass, bass_ax, 1,
                               buffered=True, ylim=[0, 2])

    features = [fft_feature, bass_feature]

    animation_func = partial(_update_plot, jack, audio_conf, features)
    ani = animation.FuncAnimation(
        fig,
        animation_func,
        interval=0,
        blit=True
    )

    plt.show()
