from essentia.standard import SingleBeatLoudness


class BeatDetector:
    """
    Computes presence of a beat
    """
    def __init__(self, buffer_size=1024, fs=44100, window_frames=5,
                 beat_frames=2):
        """
        Parameters:
            buffer_size     Number of samples in each frame (power of 2, like
                            1024)
            fs              Samplerate (usually 44100)
            window_frames   Number of frames per beat window (usually small;
                            library default is 5)
            beat_frames     Number of frames to compute the energy (smaller
                            than window_frames, library default is 2)
        """
        # Constants
        self.BUFFER_SIZE = buffer_size

        # The Essentia algorithm
        beat_duration = beat_frames * buffer_size / fs
        window_duration = window_frames * buffer_size / fs
        self.beat_alg = SingleBeatLoudness(
                beatDuration=beat_duration,
                beatWindowDuration=window_duration
        )

        # Stores previous values of the audio buffer for higher accuracy
        self.buffer = buffer_size * (window_frames + beat_frames) * [0]

    def process(self, audio_buffer):
        """
        Test of Essentia library (should refactor once working)
        """
        self.buffer = self.buffer[self.BUFFER_SIZE:] + audio_buffer

        # Run algorithm
        return self.beat_alg(self.buffer)[0]
