import pygame


def draw_vector(surface, start, vector, color=(44, 242, 34), scale=1):
    end = (start[0] + vector[0] * scale, start[1] + vector[1] * scale)
    pygame.draw.line(surface, color, start, end, 2)
    pygame.draw.circle(surface, color, end, 3)