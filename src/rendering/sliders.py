import rendering.rendering_conf as rendering_conf
from rendering.overlay import combine_colors


# TODO Find a better, more descriptive name
class Slider:
    def __init__(self):
        # Stores the previous values
        self.buffer = int(rendering_conf.NUM_PIXELS / 2) * [(0, 0, 0)]

    def update(self, pixel_map, strength, color):
        halfway = 23 * len(pixel_map) / 60
        extreme = 23 * (len(pixel_map) - 1) / 60    # Better name
        for i, pixel in enumerate(pixel_map):
            buf_index = int(halfway * (1 - abs(i - extreme) / (extreme)))

            pixel_map[i] = combine_colors(
                strength,
                pixel_map[i],
                self.buffer[buf_index]
            )

        if strength < 0.4:
            color = (0, 0, 0)
        self.buffer = self.buffer[1:] + [color]
