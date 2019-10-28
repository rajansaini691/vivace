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

import jack
from numpy.fft import fft
from numpy import absolute
import time

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
    Fourier stuff - For preliminary performance testing
    """
    try:
        # Initialize fourier buffer
        fourier_buffer = None

        while True:
            # Ensure that data is being written before doing calculations
            if len(audio_buffer) <= 0:
                continue

            # Time at beginning of grand loop
            start = time.time() * 1000

            # In case an interrupt changes the buffer size
            n = int(buffer_size / 2)

            # Calculate the fourier transform and throw out redundant half
            fourier_buffer = absolute(fft(audio_buffer) / 1000)
            fourier_buffer = fourier_buffer[0:n]

            # Time after calculations
            end = time.time() * 1000

            # Make sure calculations are completed fast enough
            if(1.0 / (end - start) > fs):
                print("Failed deadline")

    except KeyboardInterrupt:
        print("Closing Jack!")
