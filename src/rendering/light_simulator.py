import glwindow
import moderngl
import struct

from rendering.rendering_conf import RenderingConf
"""
Simulates the LED strip for testing
"""


class _LED:
    # The only aspect that should change is the color
    """
    Simulates a single LED
    """
    def __init__(self, ctx, pos, width):
        # Shaders & Program

        self.prog = ctx.program(
            vertex_shader="""
                #version 330

                in vec2 position;

                void main() {
                    gl_Position = vec4(position, 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 330

                uniform vec3 color;
                out vec4 frag_color;

                void main() {
                    frag_color = vec4(color, 1.0);
                }
            """
        )

        x = pos[0]
        y = pos[1]
        width = 0.01

        # Draws the square via two triangles
 
        self.vbo_1 = ctx.buffer(struct.pack(
            '6f',
            x + width/2, y + width/2,
            x + width/2, y - width/2,
            x - width/2, y - width/2,
        ))

        self.vbo_2 = ctx.buffer(struct.pack(
            '6f',
            x + width/2, y + width/2,
            x - width/2, y - width/2,
            x - width/2, y + width/2
        ))

        self.vao_1 = ctx.simple_vertex_array(self.prog, self.vbo_1, 'position')
        self.vao_2 = ctx.simple_vertex_array(self.prog, self.vbo_2, 'position')

        self.pos = self.prog.get('position', None)
        self.color = self.prog.get('color', None)

    def draw(self, rgb):
        self.color.value = (1.0, 1.0, 1.0)
        self.vao_1.render()
        self.vao_2.render()


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

        # The window doing the rendering
        self.wnd = glwindow.window((800, 600))

        # The context that we write to
        self.ctx = moderngl.create_context()

        def getPos(i):
            """
            Calculates the position of the LED as an (x,y) coordinate, where x
            and y belong to (-1,1).

            Parameters:
                i       Ranges from 0 to 1 and represents how far the desired
                        LED is along the strip
            """
            if i < 1/3.0:
                # Left wall
                return (-0.9, (6*i - 1)*0.95)
            elif i < 2/3.0:
                # Top wall
                return (((i - 1/3.0) * 6 - 1)*0.9, 0.95)
            else:
                # Right wall
                return (0.9, ((i - 2/3.0) * 6 - 1)*0.95)

        # Init LED objects
        n = rendering_conf.NUM_PIXELS       # More concise
        self.leds = [_LED(self.ctx, getPos(i/n), self.LED_WIDTH)
                     for i in range(n)]

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
        self.ctx.clear(0, 0, 0)
    
        for i, pixel in enumerate(pixel_map):
            self.leds[i].draw(pixel)

        self.wnd.update()
