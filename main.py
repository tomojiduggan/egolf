import Global_Var as Global_Var
from physics.phys_utils import *

import pygame
import numpy as np
from physics.props import *

from visualize import visualize_E

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()
pygame.display.set_caption('E-Golf!')

# Define constants for the screen width and height
SCREEN_WIDTH = Global_Var.SCREEN_WIDTH
SCREEN_HEIGHT = Global_Var.SCREEN_HEIGHT
DELTA_T = Global_Var.DELTA_T

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# TESTING
player = PLAYER(np.array([40, 40]))
staticCharge = POINT_CHARGE(np.array([200, 200]), 1, False)
#wall = WALL(np.array([10, 200]), np.array([600, 220]))
#wall = WALL(np.array([290, 10]), np.array([320, 500]))
wall = WALL(np.array([10, 200]), np.array([600, 220]))
print(wall.position, wall.width, wall.height)
player.velocity = np.array([18, 12])

# myWire = WIRE(np.zeros(2), np.array([100, 0]), 1)
# print(myWire.b_field(np.array([50, 20])))
# print(myWire.b_field(np.array([50, -20])))


def run():
    for object in ALL_PROPS:
        object.update()
        player.handle_collisions()
        object.draw(screen)

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))
    run()


    # Draw every 
    # Draw a solid blue circle in the center
    # pygame.draw.circle(screen, (0, 0, 255), (600, 400), 20)
    # myCharge.update(force)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
