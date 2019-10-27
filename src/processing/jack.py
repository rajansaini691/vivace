"""
Starts a jack client

 - Passes audio playing from system programs to the main audio processor
 - We'll test this by rendering a simple FFT in-house
 - Updates a sample array every audio frame
   - Keeps the audio reads independent from the time to process the data and
     write to the pixel map
   - Should be a buffer of multiple frames so we can analyze history
"""
