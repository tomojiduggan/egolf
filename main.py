# Import the pygame module
import Global_Var

import pygame
import numpy as np
import gc

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

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

DELTA_T = 0.05 # seconds

class POINT_CHARGE:
    def __init__(self, position, charge, movable): # position is numpy array length 2
        self.position = position
        self.charge = charge
        self.movable = movable
        self.velocity = np.zeros(2)
        self.acceleration = np.zeros(2)
    
    def e_field(self, r):
        return self.charge * (r-self.position) / (np.linalg.norm(r-self.position))

    def update(self, force): # force is np array
        if(not self.movable):
            print("Warning: Trying to move non-movable")
            return 

        self.acceleration = force # say mass is 1
        self.velocity += self.acceleration * DELTA_T
        self.position += self.velocity * DELTA_T
    
def net_E(r):
    sum_E = np.zeros(2)
    for object in gc.get_objects():
        if isinstance(POINT_CHARGE):
            sum_E += object.e_field(r)
        # 
            

myCharge = POINT_CHARGE(np.array([40, 40]), 1, True)
staticCharge = POINT_CHARGE(np.array([200, 40]), 1, False)

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    # myCharge.update(force)
    pygame.draw.circle(screen, (0, 0, 255), (600, 400), 20)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
