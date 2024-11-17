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

# myWire = WIRE(np.zeros(2), np.array([100, 0]), 1)
# print(myWire.b_field(np.array([50, 20])))
# print(myWire.b_field(np.array([50, -20])))
def startGame():
    player = PLAYER(np.array([40, 40]))

    staticCharge = POINT_CHARGE(np.array([200, 200]), -1, False)
    player.velocity = np.array([50, 20])
    run(player)

def shoot_phase(player):
    for object in ALL_PROPS:
        object.draw(screen)
    # print(pygame.mouse.get_pos())

    
def move_phase(player):
    for object in ALL_PROPS:
        object.update()
        player.handle_collisions()
        object.draw(screen)
    

def run(player):
    while(1):
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if(np.max(player.velocity) == 0):
            shoot_phase(player)
        else:
            move_phase(player)

        pygame.display.flip()

startGame()

pygame.quit()
