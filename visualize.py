import Global_Var as Global_Var
import numpy as np
from physics.phys_utils import get_E_level
import pygame

# def draw_vector(surface, start, vector, color=(44, 242, 34), scale=1):
#     end = (start[0] + vector[0] * scale, start[1] + vector[1] * scale)
#     pygame.draw.line(surface, color, start, end, 2)
#     pygame.draw.circle(surface, color, end, 3)

def draw_vector(surface, start, vector, min_magnitude, max_magnitude, scale=1):
    # Normalize the vector to have a magnitude of 1
    magnitude = np.linalg.norm(vector)
    if magnitude != 0:
        unit_vector = vector / magnitude  # Normalize the vector
    else:
        unit_vector = np.array([0, 0])  # Avoid division by zero if vector has zero magnitude

    # Scale the unit vector to the desired length (scale)
    end = (start[0] + unit_vector[0] * scale, start[1] + unit_vector[1] * scale)

    # Map magnitude to color
    color = magnitude_to_color(magnitude, min_magnitude, max_magnitude)

    # Draw the vector (line and circle at the end)
    pygame.draw.line(surface, color, start, end, 2)
    pygame.draw.circle(surface, color, end, 3)

grid_spacing = Global_Var.GRID_SPACING
width_start = Global_Var.PLAYABLE_TL[0]
height_start = Global_Var.PLAYABLE_TL[1]
width = Global_Var.PLAYABLE_WIDTH
height = Global_Var.PLAYABLE_HEIGHT

def visualize_E(screen):
    """
        Draw the Electric Field on the screen, computed at specific position set by global variables.
        :param screen: The layer to draw on
    """
    min_magnitude = float('inf')
    max_magnitude = float('-inf')

    for x in range(width_start, width_start + width, grid_spacing):
        for y in range(height_start, height_start + height, grid_spacing):
            poi = np.array([x, y])
            e_field = get_E_level(poi)
            print(e_field)
            magnitude = np.linalg.norm(e_field)
            print(e_field, magnitude)
            min_magnitude = min(min_magnitude, magnitude)
            max_magnitude = max(max_magnitude, magnitude)

    for x in range(width_start, width_start + width, grid_spacing):
        for y in range(height_start, height_start + height, grid_spacing):
            poi = np.array([x, y])
            e_field = get_E_level(poi)
            draw_vector(screen, poi, e_field, min_magnitude, max_magnitude, scale=15)

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
