

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
    overlay_radius = 8

    # Halfway mark
    halfway_mark = 113 * len(pixel_map) / 300

    # Number of pixels away from the center
    dist = halfway_mark * strength

    dist /= 2

    # Color centroids
    left = int(halfway_mark - dist)
    right = int(halfway_mark + dist)

    for i in range(overlay_radius * 2):
        l_index = int(left + i - overlay_radius)
        r_index = int(right + i - overlay_radius)

        if 0 < l_index < len(pixel_map):
            proportion = 1 - (abs(i - overlay_radius) / overlay_radius)
            new_color = combine_colors(proportion, pixel_map[l_index], color)
            pixel_map[l_index] = new_color
            pixel_map[r_index] = new_color

    pixel_map[left] = color
    pixel_map[right] = color
