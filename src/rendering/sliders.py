import rendering.rendering_conf as rendering_conf
from rendering.overlay import combine_colors


# TODO Find a better, more descriptive name
class Slider:
    def __init__(self):
        # Length of buffer we must store
        buffer_len = max(rendering_conf.CENTER,
                         rendering_conf.NUM_PIXELS - rendering_conf.CENTER)

        # Stores previous slider values (a copy of half of the pixel map)
        self.buffer = buffer_len * [(0, 0, 0)]

        # Frames between updates
        self.FRAME_DELAY = 2
        self.frames = 0

    def update(self, pixel_map, strength, color):
        for i, pixel in enumerate(pixel_map):
            # Indexes the buffer
            buf_index = abs(rendering_conf.CENTER - i)

            pixel_map[i] = combine_colors(
                strength,
                pixel,
                self.buffer[buf_index]
            )

        if strength < 0.2:
            color = (0, 0, 0)

        # Update speed
        self.frames += 1
        self.frames %= self.FRAME_DELAY

        if self.frames == 0:
            # Move sliders over
            self.buffer.insert(0, color)
            self.buffer.pop()
