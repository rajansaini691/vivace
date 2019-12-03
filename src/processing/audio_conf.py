"""
Stores audio configurations
"""

TEST_VAR = 10

# The name of the audio client
NAME = "vivace"

# Size of the audio buffer (in bytes)
BUFFER_SIZE = 1024

# Global samplerate (set to None to let the system decide)
SAMPLERATE = None

# Audio source to connect to
# Set to "system" to get input from mic; set to "Pulse" to analyze internal
# audio
SOURCE_NAME = "Pulse"
