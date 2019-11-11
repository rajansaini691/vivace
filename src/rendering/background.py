"""
Different ways to draw a background
"""


# Not a class since we don't need memory
def draw_background(pixel_map, color, brightness):
    """
    Colors every pixel in the pixel_map with the given brightness and color

    Parameters:
        color           A tuple of hex values of the format (r, g, b)
        brightness      A float from 0 to 1 controlling the brightness
    """
    # Computes the new background color
    background_color = tuple(int(x * brightness) for x in color)

    # Update the pixel map
    for i in range(len(pixel_map)):
        pixel_map[i] = background_color
