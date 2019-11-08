from processing.vjack import VJack
from processing.processor import VProcessor
from processing.audio_conf import AudioConf
from rendering.renderer import VRenderer
from rendering.rendering_conf import RenderingConf
from events import VEvents
from time import process_time, sleep

"""""""""""""""""""""""""""""""""""""""""""""""

Configurations

"""""""""""""""""""""""""""""""""""""""""""""""
audio_conf = AudioConf()
rendering_conf = RenderingConf()

"""""""""""""""""""""""""""""""""""""""""""""""

Initializations

"""""""""""""""""""""""""""""""""""""""""""""""

# Wrapper for jack client to get live audio data
jack = VJack(audio_conf)

event_list = VEvents()

processor = VProcessor()

renderer = VRenderer()

# The RGB pixel map getting rendered.
# Ex: [(0x00, 0x00, 0x00), (0xFF, 0xFF, 0xFF)] is rendered as black, white
pixel_map = [(0x00, 0x00, 0x00)] * rendering_conf.NUM_PIXELS

# Keeps track of the current time to keep writes consistent
prev_time = None
curr_time = process_time()

"""""""""""""""""""""""""""""""""""""""""""""""

The grand loop

"""""""""""""""""""""""""""""""""""""""""""""""
while True:
    # Reset stopwatch
    prev_time = curr_time
    curr_time = process_time()

    # Reads
    audio_buf = jack.get_audio_buffer()

    # Processing
    processor.update_event_list(audio_buf, audio_conf, event_list)

    # Rendering
    renderer.update_pixel_map(event_list, rendering_conf, pixel_map)

    # Writes (Test output to LEDs)

    # Sleep for remainder of loop time
    delta_t = process_time() - curr_time
    sleep(rendering_conf.WRITE_PERIOD - delta_t)
