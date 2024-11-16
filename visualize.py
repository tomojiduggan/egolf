import Global_Var
import numpy as np
from phys_utils import coulomb_sim_at_poi
from utils import draw_vector

grid_spacing = Global_Var.GRID_SPACING
width_start = 0 #TODO
height_start = 0 #TODO
width = Global_Var.SCREEN_WIDTH #TODO: Change to inner window width
height = Global_Var.SCREEN_HEIGHT #TODO: Change to inner window height

def visualize_E(screen, positions, charges):
    """
        Draw the Electric Field on the screen, computed at specific position set by global variables.
        :param screen: The screen object
        :param positions: Array (n, 3) of all the position of charges
        :param charges: Array(n, ) of all the charges
        """
    for x in range(width_start, width_start + width, grid_spacing):
        for y in range(height_start, height_start + height, grid_spacing):
            poi = np.array([x, y])
            e_field = coulomb_sim_at_poi(positions, charges, poi)
            draw_vector(screen, poi, e_field, scale=1)


# FOR COLOR GRADIENT FOR E FIELD
def magnitude_to_color(magnitude, min_magnitude, max_magnitude):
    # Normalize magnitude to range [0, 1]
    norm = (magnitude - min_magnitude) / (max_magnitude - min_magnitude)
    norm = np.clip(norm, 0, 1)

    # Map normalized value to RGB color (blue -> red gradient)
    r = int(norm * 255)
    g = 0
    b = int((1 - norm) * 255)

    return (r, g, b)
