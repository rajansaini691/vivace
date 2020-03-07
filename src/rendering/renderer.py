"""
Renders the pixel map
"""
from rendering.background import draw_background
from rendering.overlay import draw_overlay
from events import VEvents
from rendering.sliders import Slider


class VRenderer:

    # TODO Store individual rendering objects here
    slider = Slider()

    BACKGROUND_COLOR = (0, 255, 255)  # Cyan

    # TODO Come up with a better name than overlay
    OVERLAY_COLOR = (252, 135, 2)     # Orange

    SLIDER_COLOR = (188, 1, 255)      # Purple

    def update_pixel_map(self, event_list: VEvents, pixel_map):
        """
        Parameters:
            event_list      The list of audio events that occurred during the
                            current cycle (being read from)

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
        draw_overlay(pixel_map, self.OVERLAY_COLOR, event_list.MIDS)
        self.slider.update(pixel_map, event_list.BASS, self.SLIDER_COLOR)
