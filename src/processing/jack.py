"""
Starts a jack client. This is one of the ways we can pass input to the main
audio processor. We'll debug this by rendering a simple FFT in-house, but the 
data should be passed over to the main processor. The safest way to do this is
to update an array every process callback, which the processor can then read
from. This keeps the audio reads independent from the output time. A possible
problem with this approach is that there is no way to maintain a history for
Fourier analysis. Perhaps we can store a buffer of multiple frames? 
"""
