
class VEvents:
    """
    Stores a list of audio events and values that occurred
    (Can also contain flags indicating the presence of a higher-level event)
    """
    KICK = False
    ON = False
    # Stores the amount of "bass" in the signal
    BASS = 0.1
    MIDS = 0.1
    NEW_SONG = False
