"""
Renders the pixel map
"""
from rendering.background import draw_background
from events import VEvents


class VRenderer:

    # TODO Store individual rendering objects here

    BACKGROUND_COLOR = (0, 255, 255)  # Cyan

    def update_pixel_map(self, event_list: VEvents, pixel_conf, pixel_map):
        """
        Parameters:
            event_list      The list of audio events that occurred during the
                            current cycle (being read from)

            pixel_conf      Stores the global configuration of the LED system
                            (like the number of LEDs, spacing, etc)

            pixel_map       An RGB array of pixels corresponding to the
                            LEDs (being written to)
        """
        if event_list.ON:
            print("ON")

        # TODO Delete when rendering is started
        for i in range(len(pixel_map)):
            pixel_map[i] = (0xFF, 0xFF, 0xFF)

        # Draw background modulated by amount of bass
        draw_background(pixel_map, self.BACKGROUND_COLOR, event_list.BASS)
