"""
Stores all of the relevant hardware configuration
"""
# Number of RGB LEDs
NUM_PIXELS = 450

# Number of seconds between writes to the LED strip
MAX_WRITE_PERIOD = 0.03

# Index of the pixel at the "center" of the strip (dependent on how the LEDs
# are set up)
CENTER = int(NUM_PIXELS * 23 / 60)
