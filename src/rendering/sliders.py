import rendering.rendering_conf as rendering_conf
from rendering.overlay import combine_colors


# TODO Find a better, more descriptive name
class Slider:
    def __init__(self):
        # Length of buffer we must store - the sliders should disappear halfway
        # anyway
        self.buffer_len = int(
            max(
                rendering_conf.CENTER,
                rendering_conf.NUM_PIXELS - rendering_conf.CENTER
            ) / 2
        )

        # Stores previous slider values (a copy of half of the pixel map)
        self.buffer = self.buffer_len * [(0, 0, 0)]

        # Frames between updates
        self.FRAME_DELAY = 1
        self.frames = 0

        # Pixels travelled every frame
        self.SPEED = 1

    def update(self, pixel_map, strength, kick, color):
        # Sliders should come out of the ends of the strip at a high velocity.
        # They should also fade as they reach the center.

        # Update the buffer
        for i in range(self.buffer_len):
            decay = 1 - i / self.buffer_len
            decay /= 2

            # Left
            pixel_map[i] = combine_colors(
                strength * decay,
                pixel_map[i],
                self.buffer[i]
            )

            # Right
            # Indexes pixel map
            r = rendering_conf.NUM_PIXELS - i - 1
            pixel_map[r] = combine_colors(
                    strength * decay,
                    pixel_map[r],
                    self.buffer[i]
            )

        if not kick:
            color = (0, 0, 0)

        # Update speed
        self.frames += 1
        self.frames %= self.FRAME_DELAY

        if self.frames == 0:
            # Move sliders over
            # self.buffer.insert(0, [color] * self.SPEED)
            self.buffer = [color] * self.SPEED + self.buffer[:-self.SPEED]
