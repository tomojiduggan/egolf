import pygame
import button
import sys
from Global_Var import * 
from physics.props import *
import numpy as np
from runlevel import getLevel
from map_design import free_design_screen
# from game_design import draw_game

from visualize import visualize_E
from runlevel import getLevel
from map_design import free_design_screen

from load_images import *




pygame.init()
# Screen dimensions
SCREEN_WIDTH = Global_Var.SCREEN_WIDTH
SCREEN_HEIGHT = Global_Var.SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Electromagnetic Golf")
# Colors
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

ROWS = 15
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 4
level = 0
current_tile = 0

img_list = []
minus_charge_img = pygame.image.load('pictures/minu_charge.png').convert_alpha()
minus_charge_img = pygame.transform.scale(minus_charge_img, (TILE_SIZE, TILE_SIZE))
plus_charge_img = pygame.image.load('pictures/plus_charge.png').convert_alpha()
minus_charge_img = pygame.transform.scale(plus_charge_img, (TILE_SIZE, TILE_SIZE))
solenoid_img = pygame.image.load('pictures/solenoid.png').convert_alpha()
solenoid_img = pygame.transform.scale(solenoid_img, (TILE_SIZE, TILE_SIZE))
img_list = [minus_charge_img, plus_charge_img,solenoid_img]
# Fonts
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 20)

# Button dimensions
button_width, button_height = 100, 50
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = (SCREEN_HEIGHT - button_height) // 2

# Game state
game_state = "title"
game_level = "level1.json"


run = True
paused = False
render_E_simulation = False

# Button functions
def pause_game():
    print("Pausing the game...")
    # Add code here to pause the game, e.g., freeze the game loop or display a pause screen.

def back_to_title():
    global game_state
    print("Returning to title screen...")
    game_state = 'start_page'
        
def game_stop(): 
    n = len(ALL_PROPS)
    for i in range(n):
        ALL_PROPS.pop()

def game_restart():
    game_stop()
    getLevel(game_level)

# Game pages
#create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * MAX_COLS
	world_data.append(r)

#create ground
for tile in range(0, MAX_COLS):
	world_data[ROWS - 1][tile] = 0


#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#create function for drawing background


#draw grid
def draw_grid():
	#vertical lines
	for c in range(MAX_COLS + 1):
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE , 0), (c * TILE_SIZE, SCREEN_HEIGHT))
	#horizontal lines
	for c in range(ROWS + 1):
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


#function for drawing the world tiles
def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				screen.blit(img_list[tile], (x * TILE_SIZE, y * TILE_SIZE))




def draw_title_screen():
    """Draw the title screen with a Start button."""
    global game_state 
    screen.blit(background_image, (0, 0))  # Draw the background
    if start_button.draw(screen):  # If the button is clicked
        game_state = 'start_page'

def draw_start_page():
    """Draw the start page."""
    global game_state  
    screen.fill(WHITE)
    if new_game.draw(screen):
        game_state = "game"
        game_level = "level1.json"
        getLevel(game_level)
    if free_design.draw(screen):
        game_state = "free_design"

# FREE DESIGN SECTION
props_list = []
# Create the free design screen
def free_design_screen():
    """Draw the free design screen."""
    global game_state, props_list
    screen.fill(WHITE)

    # Draw existing props
    for prop in props_list:
        prop.draw(screen)
    
    button_list = [add_wire_button, add_charge_button, add_solenoid_button, add_block_button, add_back_button, add_save_button]

    # Initialize game state
    current_tile = -1

    # Draw buttons and check interactions
    for button_count, button in enumerate(button_list):
        if button.draw(screen):  # Draw the button and check if clicked
            current_tile = button_count  # Update current selected tile if clicked 
            # Call the corresponding function based on the button clicked
            if current_tile == 0:  # Restart Button
                wire = WIRE((100, 100), (150, 150), 2)
                props_list.append(wire)
            elif current_tile == 1:  # Pause Button
                charge = POINT_CHARGE((200, 200), 1, False)
                props_list.append(charge)
            elif current_tile == 2:  # Place Button
                solenoid = SOLENOID(50, 1, [0,0,1], [200,200])
                props_list.append(solenoid)
            elif current_tile == 3:  # Swap Button
                pass
            elif current_tile == 4:  # Extra Action Button E
                back_to_title()
            elif current_tile == 5:  # Extra Action Button B
                pass
    # Highlight the selected button with a gray border
    if current_tile != -1:  
        pygame.draw.rect(screen, GRAY, button_list[current_tile].rect,3)  # Add padding around the button
    # Update the display
    pygame.display.flip()
    

# State where clicking will launch ball
def run_launch(player):
    mouse_pos = pygame.mouse.get_pos()
    direction = np.array(mouse_pos) - player.position
    norm = np.linalg.norm(direction)
    if pygame.mouse.get_pressed()[0] == 1 and norm < 100:
        player.velocity = LAUNCH_SPEED * direction / np.linalg.norm(direction)


# Simulation Code
# Controlled by buttons
render_E_simulation = False
render_B_simulation = False

E_sim_layer = pygame.Surface((400, 400), pygame.SRCALPHA)
B_sim_layer = pygame.Surface((400, 400), pygame.SRCALPHA)


def draw_game():
    global render_E_simulation, render_B_simulation

    """Draw the game screen."""
    global paused  # Ensure `paused` is accessible
    global render_E_simulation

    # Clear the screen
    screen.fill(WHITE)

    # The inner playable size excluding the width of bounday is 772x470
    # That is, top left (14, 14) to bot right (786, 484)
    # Draw Boundary
    top_boundary = WALL(np.array([11, 11]), np.array([789, 13]))
    left_boundary = WALL(np.array([11, 11]), np.array([13, 486]))
    bot_boundary = WALL(np.array([13, 484]), np.array([789, 486]))
    right_boundary = WALL(np.array([787, 11]), np.array([789, 486]))

    top_boundary.draw(screen)
    left_boundary.draw(screen)
    bot_boundary.draw(screen)
    right_boundary.draw(screen)

    # Define button list
    button_list = [restart_button, pause_button, place_button, swap_button, E_button, B_button,back_button]

    # Initialize game state
    current_tile = -1

    # Draw buttons and check interactions
    for button_count, button in enumerate(button_list):
        if button.draw(screen):  # Draw the button and check if clicked
            current_tile = button_count  # Update current selected tile if clicked
            # Call the corresponding function based on the button clicked
            if current_tile == 0:  # Restart Button
                game_restart()
            elif current_tile == 1:  # Pause Button
                paused = not paused
                pause_game() if paused else print("Game Resumed")
            elif current_tile == 2:  # Place Button
                print("Placing charge...")
            elif current_tile == 3:  # Swap Button
                print("Swapping objects...")
            elif current_tile == 4:  # Extra Action Button E
                print("Plotting the electric field")
                # Turn on/off the electric field
                render_E_simulation = not render_E_simulation
                print(render_E_simulation)
                # After toggle if it is off state, clear the screen
                if not render_E_simulation:
                    E_sim_layer.fill((0, 0, 0, 0))

            elif current_tile == 5:  # Extra Action Button B
                print("Performing extra action B...")
                # extra_action_B()
            elif current_tile == 6: # Back button
                game_stop()
                global game_state
                game_state = "start_page"
                return
    # Highlight the selected tile with a gray border
    if current_tile != -1:  # Only highlight if a button is selected
        pygame.draw.rect(screen, GRAY, button_list[current_tile].rect, 3)

    for object in ALL_PROPS:
        if(not paused):
            object.update()
            
        object.draw(screen)
        if(isinstance(object, PLAYER)):
            player = object

    if not paused:
        player.handle_collisions()
        if(max(player.velocity) == 0):
            run_launch(player) # draw arrow, make it so clicking within the screen will launch the player

    # Update the display
    pygame.display.flip()


def draw_B_sim_layer():
    #TODO
    pass

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update screen based on the current state
    if game_state == "title":
        draw_title_screen()
    elif game_state == "start_page":
        draw_start_page()
    elif game_state == "game":
        draw_game()
    elif game_state == "free_design":
        free_design_screen()

    if render_E_simulation:
        visualize_E(E_sim_layer)
        screen.blit(E_sim_layer, (0, 0))
    if render_B_simulation:
        draw_B_sim_layer()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()