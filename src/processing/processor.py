from jackd import *

"""
Processes an audio file and writes to the pixel map for the given tick

Components:
 - When the user wants to render something, they write to a FIFO of tasks

 1) Grab the audio
   - From a JACK server (only real-time)
     - Helpful for debugging, listening to a variety of songs
   - From an audio file (real-time and preprocessing)
     - We need a directory of audio files, and the path should go into the
       configuration
   - From a browser (in which case rendering will also be done on a browser)
 2) Perform computations shared by all renderers
   - Compute FFT 
   - Determine quality of current tick (Is a kick happening? Did a chord
     change?)
 3) Service rendering requests
   - One service can change color or brightness depending on spectrum being
     used
     - Ex: If a lowpass has been applied, we'll keep the brightness low
   - The background of the entire pixel map will have its brightness depend on
     the presence of a kick; everything else will be overlayed 

   Things that can be modulated on the rendering side:
     - Background brightness
     - Background color
     - Triggering a pulse
       - Each pulse should be its own object that manages its own state
       - Another singleton object manages, creates/destroys, and renders a 
         collection of pulses
       - The processor should be the one telling that object to generate a pulse
     - Triggering a flash of darkness
     - Foreground snake 
       - A different color; moves around the pixel map
       - Either smoothly integrates with the background or has a sharp edge
       - Direction could change based on events
    
    Things that change:
     - Chords
     - Spectral range
     - Amplitude of different spectra
       - For example, the background brightness could be modulated by this
         (different regions corresponding with different frequencies, or
         applying a uniform brightness based on the amplitude of a frequency
         range)
     - Average volume
     - Kick hit (possibly using transient detection)
     - Transients (using a transient detection algorithm)
     - General mid-range volume
     - Differences between left and right channels

 3) Write to pixel map
   - A lot of the modulating things above may do the writing already, and their
     order of writing determines what gets put on top
   - Note: Nothing should persist from the last frame, so either the entire background
     needs to be modulated or we start each frame with a blank slate
"""

