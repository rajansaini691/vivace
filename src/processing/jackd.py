"""
Starts a jack client

 - Passes audio playing from system programs to the main audio processor
 - We'll test this by rendering a simple FFT in-house
 - Updates a sample array every audio frame
   - Keeps the audio reads independent from the time to process the data and
     write to the pixel map
   - Should be a buffer of multiple frames so we can analyze history

  - Latency-Performance tradeoff:
    - High latency is tolerable, as long as the audio and the lights are synced
    - Compute time needs to be measured
"""

import sys
import signal
import os
import jack
import threading
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

"""
Configuration
"""
JACK_NAME = "vivace"

"""
Exposed data
"""
audio_buffer = []           # Raw audio buffer coming from Jack
audio_spectrograph = []     # Array of data points storing FFT
fs = None                   # Global samplerate for data coming in
buffer_size = None          # Size of audio buffer

"""
Set up Jack client
"""
client = jack.Client(JACK_NAME)

@client.set_blocksize_callback
def blocksize(blocksize):
    global buffer_size
    buffer_size = blocksize
    
@client.set_samplerate_callback
def samplerate(samplerate):
    global fs
    fs = samplerate

@client.set_process_callback
def process(frames):
    for i in client.inports:
        global audio_buffer
        audio_buffer = i.get_array()

# Accept input from a single audio source
client.inports.register("input_1")

# TODO Put in a global configuration file
client.blocksize = 4096

# Enable client
with client:
    # Connect our client to pulseaudio
    pulse = client.get_ports(name_pattern = "Pulse", is_output=True)

    if not pulse:
        raise RuntimeError("No physical capture ports")

    for src, dest in zip(pulse, client.inports):
        client.connect(src, dest)

    """
    Fourier stuff
    """
    try:
        # Number of points being graphed (half are redundant)
        n = int(buffer_size / 2)

        # Initialize plotting library
        plt.ion()   # Allow live updating
        fig = plt.figure()
        ax = fig.add_subplot(111)     

        # Initialize input bounds, frequency curve
        t = np.linspace(0, fs/2., n)
        y = np.array(audio_buffer[0:n])
        fft_line, = ax.plot(t, y)

        while True:
            if len(audio_buffer) > 0:
                # In case an interrupt changes the buffer size
                n = int(buffer_size / 2)

                # Calculate the fourier transform and throw out half
                yf = np.abs(np.fft.fft(audio_buffer) / 1000)
                yf = yf[0:n]

                # Draw the new FFT curve
                fft_line.set_ydata(yf)
                fig.canvas.draw()
                fig.canvas.flush_events()
    except KeyboardInterrupt:
        print("Closing Jack!")
