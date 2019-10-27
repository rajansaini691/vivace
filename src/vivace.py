import numpy as np

# TODO Move to own configuration file
"""""""""""""""""""""""""""""""""""""""""""""""

Configurations

"""""""""""""""""""""""""""""""""""""""""""""""

# Number of RGB pixels being rendered
NUM_PIXELS = 1000

# The RGB pixel map getting rendered. 
# Ex: [(0x00, 0x00, 0x00), (0xFF, 0xFF, 0xFF)] is rendered as black, white
pixel_map = [(0x00, 0x00, 0x00)] * NUM_PIXELS

"""""""""""""""""""""""""""""""""""""""""""""""

The grand loop

"""""""""""""""""""""""""""""""""""""""""""""""
while True:
    # Do the processing
    for i in range(0, NUM_PIXELS, 2):
        pixel_map[i] = (0xFF, 0xFF, 0xFF) 

    # Do the rendering
    print(pixel_map)     # A poor man's rendering :)

