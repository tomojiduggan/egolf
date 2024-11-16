# Import the pygame module
import pygame
import numpy as np

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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

DELTA_T = 0.05 # seconds

class POINT_CHARGE:
    def __init__(self, position, charge, movable): # position is numpy array length 3
        self.position = position
        self.charge = charge
        self.movable = movable
        if(movable):
            self.velocity = np.zeros(3)
            self.acceleration = np.zeros(3)

    
    def move(self, position):
        if(not self.movable):
            print("No")
            return
        
        self.position = position

class MOVABLE:
    def __init__(self, position):
        self.position = position
        self.velocity = np.zeros(3)
        self.acceleration = np.zeros(3)




def charge_e_field(q1, q2, r):
    q1 * q2 * r / (np.linalg.norm(r))

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
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
