# Import the pygame module
import Global_Var

import pygame
import numpy as np
import gc

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

# Define constants for the screen width and height
SCREEN_WIDTH = Global_Var.SCREEN_WIDTH
SCREEN_HEIGHT = Global_Var.SCREEN_HEIGHT
DELTA_T = Global_Var.DELTA_T
Q = Global_Var.Q
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))






    

            


# TESTING

positions = np.array([[300, 300], [500, 300]])
charges = np.array([-Q, Q])

# myCharge = POINT_CHARGE(np.array([40, 40]), 1, True)
# staticCharge = POINT_CHARGE(np.array([200, 40]), 1, False)
# print(myCharge.get_force())
#
# myWire = WIRE(np.zeros(2), np.array([100, 0]), 1)
# print(myWire.b_field(np.array([50, 20])))
# print(myWire.b_field(np.array([50, -20])))
    




# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    visualize_E(screen, positions, charges)

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (600, 400), 20)
    # myCharge.update(force)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
