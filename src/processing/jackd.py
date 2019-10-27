"""
Starts a jack client

 - Passes audio playing from system programs to the main audio processor
 - We'll test this by rendering a simple FFT in-house
 - Updates a sample array every audio frame
   - Keeps the audio reads independent from the time to process the data and
     write to the pixel map
   - Should be a buffer of multiple frames so we can analyze history
"""

import sys
import signal
import os
import jack
import threading
from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt
import struct

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

"""
Set up Jack client
"""
client = jack.Client(JACK_NAME)

@client.set_samplerate_callback
def samplerate(samplerate):
    global fs
    fs = samplerate

@client.set_process_callback
def process(frames):
    for i in client.inports:
        buf = i.get_buffer()
        audio_buffer[:] = buf

client.inports.register("input_1")

with client:
    # Connect to pulseaudio
    pulse = client.get_ports(name_pattern = "Pulse", is_output=True)

    if not pulse:
        raise RuntimeError("No physical capture ports")

    for src, dest in zip(pulse, client.inports):
        client.connect(src, dest)

    """
    Fourier stuff
    """
    try:
        while True:
            if len(audio_buffer) > 0:
                arr = struct.unpack('f', audio_buffer)
                #print(fft(audio_buffer))
    except KeyboardInterrupt:
        print("Closing Jack!")
