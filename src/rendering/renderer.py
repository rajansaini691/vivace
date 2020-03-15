"""
Renders the pixel map
"""
from rendering.background import draw_background
from rendering.overlay import draw_overlay
from events import VEvents
from rendering.sliders import Slider
import random
import colorsys


class VRenderer:

    # TODO Store individual rendering objects here
    slider = Slider()

    BACKGROUND_MIDDLE_COLOR = (0, 127, 127)  # Cyan
    BACKGROUND_END_COLOR = (126, 66, 1)   # Orange

    # TODO Come up with a better name than overlay
    OVERLAY_COLOR = (126, 66, 1)     # Orange

    SLIDER_COLOR = (124, 54, 193)      # Purple

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
        draw_background(pixel_map, self.BACKGROUND_MIDDLE_COLOR,
                        self.BACKGROUND_END_COLOR, event_list.BASS)
        draw_overlay(pixel_map, self.OVERLAY_COLOR, event_list.MIDS)
        self.slider.update(pixel_map, event_list.BASS, self.SLIDER_COLOR)

        if(event_list.NEW_SONG):
            hues = [(x/3 + random.uniform(0, 1), 0.75, 0.4) for x in range(3)]
            colors = []
            for rgb in hues:
                rgb = colorsys.hsv_to_rgb(*rgb)
                rgb = tuple([int(x * 255) for x in rgb])
                colors.append(rgb)

            self.BACKGROUND_MIDDLE_COLOR = colors[0]
            self.OVERLAY_COLOR = colors[1]
            self.SLIDER_COLOR = colors[2]
            self.BACKGROUND_MIDDLE_COLOR = self.SLIDER_COLOR
            print("NEW SONG")
