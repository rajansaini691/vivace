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
from enum import Enum
from threading import Lock

"""
Configuration - TODO Put in global configuration file
"""
JACK_NAME = "vivace"
AUDIO_BUFFER_SIZE = 4096

"""
Exposed data
"""
audio_buffer = []           # Raw audio buffer coming from Jack
audio_spectrograph = []     # Array of data points storing FFT
fs = None                   # Global samplerate for data coming in
buffer_size = None          # Size of audio buffer

"""
State management
    ERR - Jack client is currently in an error state
    UNINIT - Client has not yet been initialized
    READY - Client can be read from
"""
JACK_STATES = Enum('JACK_STATES', 'ERR UNINIT READY')
jack_state = JACK_STATES.UNINIT
buffer_lock = Lock()

def init_jack():
    """
    Starts a jack client that grabs live data from PulseAudio
    """
    # Ensure only one jack client gets created
    if(jack_state != JACK_STATES.UNINIT): 
        raise RuntimeError("Only one jack client should be made")

    """
    Set up Jack client
    """
    client = jack.Client(JACK_NAME)

    # Accept input from a single audio source
    client.inports.register("input_1")

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
        buffer_lock.acquire() 
        for i in client.inports:
            global audio_buffer
            audio_buffer = i.get_array()
        buffer_lock.release()

    client.blocksize = self.AUDIO_BUFFER_SIZE

    # Starts jack client
    client.activate()

    # Connect our client to pulseaudio
    pulse = client.get_ports(name_pattern = "Pulse", is_output=True)

    if not pulse:
        jack_state = JACK_STATES.ERR
        raise RuntimeError("PulseAudio not running")

    for src, dest in zip(pulse, client.inports):
        client.connect(src, dest)

    jack_state = JACK_STATES.READY

def get_audio_buffer():
    buffer_lock.acquire()
    
    # Copy audio buffer to new buffer safely
    cur_buf = audio_buffer

    buffer_lock.release()
    return cur_buf
