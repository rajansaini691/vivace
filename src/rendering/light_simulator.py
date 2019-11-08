import pygame as pg
from rendering.rendering_conf import RenderingConf
"""
Simulates the LED strip for testing
"""


class VSimulator:
    """
    Uses pygame to simulate writes to the LED strip
    """
    def __init__(self, rendering_conf: RenderingConf):
        # Window parameters
        self.WIDTH = 800
        self.HEIGHT = 600

        # LED parameters
        self.LED_WIDTH = 5
        self.LED_SPACING = 5

        # Number of LEDs on each wall
        self.LEFT_WALL = self.HEIGHT / (self.LED_WIDTH + self.LED_SPACING)
        self.RIGHT_WALL = self.LEFT_WALL
        self.TOP_WALL = self.WIDTH / (self.LED_WIDTH + self.LED_SPACING)

        pg.display.init()

        # The surface that we write to
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))

        pg.display.set_caption("Vivace Simulator")

    def write(self, pixel_map):
        """
        Renders the given pixel map

        Parameters:
            pixel_map       An array of RGB values corresponding to the lights
                            on the LED strip
                            For example, [(0x00,0x00,0x00),(0xFF,0xFF,0xFF)]
                            will be rendered as (BLACK, WHITE)
        """
        # Draw background
        self.screen.fill((0, 0, 0))

        for i, pixel in enumerate(pixel_map):
            x = None
            y = None

            if i < self.LEFT_WALL:
                # Left wall
                x = self.LED_SPACING
                y = self.HEIGHT - i * (self.LED_WIDTH + self.LED_SPACING)
            elif i < self.LEFT_WALL + self.TOP_WALL:
                # Top wall
                x = (self.LED_SPACING + (i - self.LEFT_WALL)
                     * (self.LED_WIDTH + self.LED_SPACING))
                y = self.LED_SPACING
            else:
                # Right wall
                x = self.WIDTH - (self.LED_SPACING + self.LED_WIDTH)
                y = (self.LED_SPACING + (i - (self.TOP_WALL + self.LEFT_WALL))
                     * (self.LED_WIDTH + self.LED_SPACING))

            pg.draw.rect(self.screen, pixel, (x, y, self.LED_WIDTH,
                         self.LED_WIDTH))

        pg.display.flip()
