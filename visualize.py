import Global_Var as Global_Var
import numpy as np
from physics.phys_utils import get_E_level, get_B_level
import pygame

grid_spacing = Global_Var.GRID_SPACING
width_start = Global_Var.PLAYABLE_TL[0]
height_start = Global_Var.PLAYABLE_TL[1]
width = Global_Var.PLAYABLE_WIDTH
height = Global_Var.PLAYABLE_HEIGHT

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

def draw_polarity_marker(surface, position, value, min_value, max_value):
    """
    Draws a marker based on polarity: a cross (X) for positive value and a dot for negative value.

    :param surface: The Pygame surface to draw on.
    :param position: The position to draw the marker as (x, y).
    :param value: The value to determine polarity.
    :param min_value: The minimum value for normalization.
    :param max_value: The maximum value for normalization.
    """
    # Map value to color
    color = magnitude_to_color(abs(value), min_value, max_value)


    if value >= 0:
        # Draw a cross (X) for positive values
        offset = 5  # Length of the cross arms
        pygame.draw.line(surface, color, (position[0] - offset, position[1] - offset),
                         (position[0] + offset, position[1] + offset), 2)
        pygame.draw.line(surface, color, (position[0] - offset, position[1] + offset),
                         (position[0] + offset, position[1] - offset), 2)
    else:
        # Draw a dot for negative values
        pygame.draw.circle(surface, color, position, 5)


def visualize_B(screen):
    """
    Visualize the Magnetic Field (B-field) on the provided screen layer by drawing polarity markers.

    :param screen: The layer to draw on
    """
    # Initialize min and max magnitude values for normalization
    min_magnitude = float('inf')
    max_magnitude = float('-inf')

    # First loop: Compute min and max magnitudes of the B field
    for x in range(width_start, width_start + width, grid_spacing):
        for y in range(height_start, height_start + height, grid_spacing):
            poi = np.array([x, y])
            b_field = get_B_level(poi)  # Scalar value
            magnitude = abs(b_field)  # Take the absolute value for magnitude
            min_magnitude = min(min_magnitude, magnitude)
            max_magnitude = max(max_magnitude, magnitude)

    # Second loop: Visualize the B field with polarity markers
    for x in range(width_start, width_start + width, grid_spacing):
        for y in range(height_start, height_start + height, grid_spacing):
            poi = np.array([x, y])
            b_field = get_B_level(poi)  # Scalar value

            # Draw polarity marker (dot or cross) based on the scalar value
            draw_polarity_marker(screen, poi, b_field, min_magnitude, max_magnitude)


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
            magnitude = np.linalg.norm(e_field)
            min_magnitude = min(min_magnitude, magnitude)
            max_magnitude = max(max_magnitude, magnitude)

    for x in range(width_start, width_start + width, grid_spacing):
        for y in range(height_start, height_start + height, grid_spacing):
            poi = np.array([x, y])
            e_field = get_E_level(poi)
            draw_vector(screen, poi, e_field, min_magnitude, max_magnitude, scale=15)


def magnitude_to_color(magnitude, min_magnitude, max_magnitude, clip_percentage=0.1):
    """
    Map a magnitude to an RGB color, clipping the max magnitude at a specified percentage.

    :param magnitude: The magnitude to map to a color.
    :param min_magnitude: The minimum magnitude in the range.
    :param max_magnitude: The maximum magnitude in the range.
    :param clip_percentage: The percentage of the range at which to clip the maximum magnitude.
    :return: An RGB tuple representing the color.
    """
    # Calculate the effective max magnitude for normalization (clipped)
    clipped_max = min_magnitude + clip_percentage * (max_magnitude - min_magnitude)

    # Clamp magnitude to the clipped maximum
    magnitude = min(magnitude, clipped_max)

    # Ensure no divide by 0 error
    if (clipped_max - min_magnitude == 0): clipped_max += 1

    # Normalize magnitude between min_magnitude and clipped_max
    norm = (magnitude - min_magnitude) / (clipped_max - min_magnitude)
    norm = np.clip(norm, 0, 1)  # Ensure norm is in the range [0, 1]

    # Map normalized value to an RGB gradient (blue -> red)
    r = int(norm * 255)
    g = int((1 - norm) * 255)
    b = 0

    return (r, g, b)