#!/usr/bin/env python3

from inputs.jack_wrapper import VJack
from processing.processor import VProcessor
from processing.plot_features import graph_features
from rendering.renderer import VRenderer
from outputs.light_simulator import VSimulator
import rendering.rendering_conf as rendering_conf
from outputs.rpi import VSocket
from events import VEvents
from time import process_time, sleep
import argparse


def main_vivace_thd(output_target_str="simulator"):
    """""""""""""""""""""""""""""""""""""""""""""""

    Initializations

    """""""""""""""""""""""""""""""""""""""""""""""

    # Wrapper for jack client to get live audio data
    jack = VJack()

    # Stores the events
    event_list = VEvents()

    # Updates the event list
    processor = VProcessor()

    # Updates the pixel map
    renderer = VRenderer()

    # Draws or transmits the pixel map, depending on the desired target
    output_target = None
    if output_target_str == "simulator":
        output_target = VSimulator()
    elif output_target_str == "socket":
        output_target = VSocket()

    assert(output_target is not None)

    # The RGB pixel map getting rendered.
    # Ex: [(0x00, 0x00, 0x00), (0xFF, 0xFF, 0xFF)] is rendered as black, white
    pixel_map = [(0x00, 0x00, 0x00)] * rendering_conf.NUM_PIXELS

    # Keeps track of the current time to keep writes consistent
    curr_time = process_time()

    """""""""""""""""""""""""""""""""""""""""""""""

    The grand loop

    """""""""""""""""""""""""""""""""""""""""""""""
    while True:
        # Reset stopwatch
        curr_time = process_time()

        # Reads
        audio_buf = jack.get_audio_buffer()

        # Processing
        processor.update_event_list(audio_buf, event_list)

        # Rendering (Test output to LEDs)
        renderer.update_pixel_map(event_list, pixel_map)
        output_target.write(pixel_map)

        # Sleep for remainder of loop time
        delta_t = process_time() - curr_time
        sleep(rendering_conf.WRITE_PERIOD - delta_t)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="vivace")
    parser.add_argument(
                        '-o', '--output', nargs='?', default='simulator',
                        choices=['simulator', 'features', 'socket', 'chip']
    )
    args = parser.parse_args()
    output = args.output
    if output == 'simulator':
        main_vivace_thd(output_target_str='simulator')
    elif output == 'features':
        graph_features()
    elif output == 'socket':
        main_vivace_thd(output_target_str='socket')
    elif output == 'chip':
        # TODO Implement on-chip writing
        exit()
