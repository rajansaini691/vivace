"""
Different ways to draw a background
"""


# Not a class since we don't need memory
def draw_background(pixel_map, middle_color, end_color, brightness):
    """
    Colors every pixel in the pixel_map with the given brightness and color

    Parameters:
        color           A tuple of hex values of the format (r, g, b)
        brightness      A float from 0 to 1 controlling the brightness
    """
    # Computes the new background color
    background_color = tuple(int(x * brightness) for x in middle_color)

    # Update the pixel map
    for i in range(len(pixel_map)):
        pixel_map[i] = background_color

    middle = int(23 * len(pixel_map) / 60)
    for i in range(middle):
        a = i / middle
        pixel_map[i] = (
                int((a*middle_color[0]+(1-a)*end_color[0])*brightness),
                int((a*middle_color[1]+(1-a)*end_color[1])*brightness),
                int((a*middle_color[2]+(1-a)*end_color[2])*brightness)
        )

    for i in range(len(pixel_map) - middle):
        a = i / (len(pixel_map) - middle)
        pixel_map[i+middle] = (
                int(((1-a)*middle_color[0]+(a)*end_color[0])*brightness),
                int(((1-a)*middle_color[1]+(a)*end_color[1])*brightness),
                int(((1-a)*middle_color[2]+(a)*end_color[2])*brightness)
        )
