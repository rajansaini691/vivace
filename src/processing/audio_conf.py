
class AudioConf:
    """
    Stores audio configurations
    """
    # The name of the audio client
    NAME = "vivace"

    # Size of the audio buffer (in bytes)
    BUFFER_SIZE = 4096

    # Global samplerate (set to None to let the system decide)
    SAMPLERATE = None
