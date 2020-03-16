import rendering.rendering_conf as rendering_conf

# TODO Put in own file
def combine_colors(proportion, old, new):
    """
    Returns a new color combining the two, where proportion is the percentage
    of the new color we want to keep
    """
    combined = []
    for i in range(3):
        combined.append(min(
            255,
            int((1-proportion) * old[i] + proportion*new[i])
        ))
    return combined


# TODO Better docs, variable naming
# TODO Grab pixel map length from rendering_conf instead (easy fix)
def draw_overlay(pixel_map, color, strength):
    """
    Draws a simple overlay
    """
    # TODO Refactor to simplify

    # Overlay radius
    overlay_radius = 16

    # Halfway mark
    halfway_mark = rendering_conf.CENTER

    # Number of pixels away from the center
    dist = rendering_conf.NUM_PIXELS * strength
    dist /= 4       # Scale the distance down

    # Indices of overlay centroids
    left = int(halfway_mark - dist)
    right = int(halfway_mark + dist)

    for i in range(overlay_radius * 2):
        l_index = int(left - overlay_radius + i)
        r_index = int(right - overlay_radius + i)

        # Strength of overlay at current pixel
        proportion = 1 - (abs(i - overlay_radius) / overlay_radius)

        # Write left overlay
        if 0 < l_index < rendering_conf.NUM_PIXELS:
            new_color = combine_colors(proportion, pixel_map[l_index], color)
            pixel_map[l_index] = new_color

        # Write right overlay
        if 0 < r_index < rendering_conf.NUM_PIXELS:
            new_color = combine_colors(proportion, pixel_map[r_index], color)
            pixel_map[r_index] = new_color
