# Import the pygame module
import Global_Var as Global_Var

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

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class POINT_CHARGE:
    def __init__(self, position, charge, movable): # position is numpy array length 2
        self.position = position
        self.charge = charge
        self.movable = movable
        self.velocity = np.zeros(2)
        self.acceleration = np.zeros(2)
    
    def e_field(self, r):
        return self.charge * (r-self.position) / (np.linalg.norm(r-self.position))

    def get_force(self):
        e_force = self.charge * net_E(self.position)
        b = net_B(self.position)
        b_force = np.array([self.velocity[1] * b, -self.velocity[0] * b])

        return e_force + b_force

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
        self.vec_l = end - start
        self.current = current
 
    def b_field(self, r):
        x1_r = r - self.start
        x2_r = r - self.end
        c1 = np.dot(x1_r, self.vec_l) / np.linalg.norm(x1_r)
        c2 = -np.dot(x2_r, self.vec_l) / np.linalg.norm(x2_r)
        norm_b_phi = self.current / (np.linalg.norm(self.vec_l)) * (c1 + c2)
        # Finding orientation (to find sign) using cross product
        cross_prod = x1_r[0] * self.vec_l[1] - x1_r[1] * self.vec_l[0]
        if(cross_prod > 0):
            return norm_b_phi
        elif(cross_prod < 0):
            return -norm_b_phi
        else:
            return 0
        
    def current_swap(self):
        self.current *= -1

    
def net_E(r):
    sum_E = np.zeros(2)
    for object in gc.get_objects():
        if isinstance(object, POINT_CHARGE):
            # ignore the e field of the moving charge
            # assume there is only one moving charge
            if(not object.movable):
                sum_E += object.e_field(r)
    return sum_E
        # E-field of other objects...

def net_B(r):
    sum_B = 0
    for object in gc.get_objects():
        if isinstance(object, WIRE):
            sum_B += object.b_field(r)
    return sum_B

            


# TESTING
myCharge = POINT_CHARGE(np.array([40, 40]), 1, True)
staticCharge = POINT_CHARGE(np.array([200, 40]), 1, False)
print(myCharge.get_force())

myWire = WIRE(np.zeros(2), np.array([100, 0]), 1)
print(myWire.b_field(np.array([50, 20])))
print(myWire.b_field(np.array([50, -20])))




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
