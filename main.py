# Import the pygame module
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
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

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

class WIRE:
    def __init__(self, start, end, current): #start and end are positions of the two ends of the wire 
        self.start = start
        self.end = end
        self.current = current

        
    
    def current_swap(self, current):
        self.current *= -1

    
    
def net_E(r):
    sum_E = np.zeros(2)
    for object in gc.get_objects():
        if isinstance(POINT_CHARGE):
            # ignore the e field of the moving charge
            # assume there is only one moving charge
            if(not object.movable):
                sum_E += object.e_field(r)

        # E-field of other objects...

def net_B(r):
    ...
            

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
