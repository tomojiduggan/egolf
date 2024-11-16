import Global_Var as Global_Var
import numpy as np
from physics.phys_utils import coulomb_sim_at_poi
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
