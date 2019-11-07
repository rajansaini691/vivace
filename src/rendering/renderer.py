"""
Renders the pixel map
"""


class VRenderer:

    # TODO Store individual rendering objects

    def update_pixel_map(self, event_list, light_conf, pixel_map):
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
