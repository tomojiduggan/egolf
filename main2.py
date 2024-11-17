import pygame
import button
import sys
from Global_Var import * 
from physics.props import *
import numpy as np
from runlevel import getLevel
from map_design import free_design_screen2
# from game_design import draw_game

from visualize import visualize_E, visualize_B
from runlevel import getLevel


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
RED = (255, 0, 0)

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
game_level = 0
game_levels = ["level1.json", "level2.json", "level3.json"]


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
    for prop in ALL_PROPS:
        prop.free()

def game_restart():
    game_stop()
    getLevel(game_levels[game_level])

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
    global game_state, game_level
    game_level = 0
    screen.fill(WHITE)
    if new_game.draw(screen):
        game_stop()
        game_state = "game"
        game_level = 0
        getLevel(game_levels[game_level])
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
            if current_tile == 0:  # Add Wire
                wire = WIRE((100, 100), (150, 150), 2)
                props_list.append(wire)
            elif current_tile == 1:  # Add Charge
                charge = POINT_CHARGE((200, 200), 1, False)
                props_list.append(charge)
            elif current_tile == 2:  # Add Solenoid
                solenoid = SOLENOID(50, (200, 200))
                props_list.append(solenoid)
            elif current_tile == 3:  # Add Block
                pass
            elif current_tile == 4:  # Back to Title
                back_to_title()
            elif current_tile == 5:  # Save (currently no action)
                pass
    # Highlight the selected button with a gray border
    if current_tile != -1:  
        pygame.draw.rect(screen, GRAY, button_list[current_tile].rect,3)  # Add padding around the button
    # Update the display
    pygame.display.flip()

def draw_win_page():
    global game_state
    global game_level
    my_img = pygame.transform.scale_by(win_img, 0.75)
    screen.blit(my_img, ((SCREEN_WIDTH - my_img.get_width()) / 2, (SCREEN_HEIGHT - my_img.get_height()) / 2))
    print(pygame.mouse.get_pos())
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if(pygame.mouse.get_pressed()[0] == 1):
        if(mouse_x > 158 and mouse_x < 354 and mouse_y > 371 and mouse_y < 456):
            # go back
            render_E_simulation = False
            game_stop()
            global game_state
            game_state = "start_page"
        if(mouse_x > 447 and mouse_x < 642 and mouse_y > 371 and mouse_y < 456):
                # next nevel
                game_level += 1
                game_state = "game"
                game_restart()


    pygame.display.flip()


def draw_lose_page():
    global game_state
    global render_E_simulation
    render_E_simulation = False
    global render_B_simulation
    render_B_simulation = False
    screen.blit(lose_img, (0,0))
    if retry_btn.draw(screen): 
         game_state = 'game'
         game_restart()
    # screen.fill(WHITE)
    # lose_text = font.render("LOSE", True, RED)
    # text_rect = lose_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    # screen.blit(lose_text, text_rect)  # Draw the text on the screen
    pygame.display.flip()  # Update the display

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

E_sim_layer = pygame.Surface((PLAYABLE_WIDTH, PLAYABLE_HEIGHT), pygame.SRCALPHA)
B_sim_layer = pygame.Surface((PLAYABLE_WIDTH, PLAYABLE_HEIGHT), pygame.SRCALPHA)

selected_charge = None
def draw_game():
    global render_E_simulation, render_B_simulation, paused, selected_charge

    """Draw the game screen."""
    global paused  # Ensure `paused` is accessible
    global render_E_simulation

    # Clear the screen
    screen.fill(WHITE)

    # The inner playable size excluding the width of bounday is 772x470
    # That is, top left (14, 14) to bot right (786, 484)
    # Draw Boundary
    top_boundary = WALL(np.array([0, 0]), np.array([800, 13]))
    left_boundary = WALL(np.array([0, 0]), np.array([13, 486]))
    bot_boundary = WALL(np.array([0, 484]), np.array([800, 497]))
    right_boundary = WALL(np.array([787, 0]), np.array([800, 486]))

    top_boundary.draw(screen)
    left_boundary.draw(screen)
    bot_boundary.draw(screen)
    right_boundary.draw(screen)

    # Define button list
    button_list = [restart_button, pause_button, swap_button, E_button, B_button,back_button]

    # Initialize game state
    current_tile = -1

    # Draw buttons and check interactions
    for button_count, button in enumerate(button_list):
        if button.draw(screen):  # Draw the button and check if clicked
            current_tile = button_count  # Update current selected tile if clicked
            # Call the corresponding function based on the button clicked
            if current_tile == 0:  # Restart Button
                render_E_simulation = False
                render_B_simulation = False
                game_restart()
            elif current_tile == 1:  # Pause Button
                paused = not paused
                pause_game() if paused else print("Game Resumed")
            elif current_tile == 2:  # Swap Button
                render_E_simulation = False
                render_B_simulation = False
                if selected_charge:
                     selected_charge.swap_sign()
                print("Swapping objects...")
            elif current_tile == 3:  # Extra Action Button E
                print("Plotting the electric field")
                # Turn on/off the electric field
                render_B_simulation = False
                render_E_simulation = not render_E_simulation
                E_sim_layer.fill((0, 0, 0, 0))
                visualize_E(E_sim_layer)
            elif current_tile == 4:  # Extra Action Button B
                render_E_simulation = False
                render_B_simulation = not render_B_simulation
                print(render_B_simulation)
                B_sim_layer.fill((0, 0, 0, 0))
                visualize_B(B_sim_layer)
            elif current_tile == 5: # Back button
                render_E_simulation = False
                render_B_simulation = False
                game_stop()
                global game_state
                game_state = "start_page"
                return
    # Highlight the selected tile with a gray border
    if current_tile != -1:  # Only highlight if a button is selected
        pygame.draw.rect(screen, GRAY, button_list[current_tile].rect, 3)

    if selected_charge:
        selected_charge.draw(screen)
    # Highlight the selected charge
    if selected_charge:
        pygame.draw.rect(screen, GRAY, selected_charge.rect.inflate(4, 4), 3)
    
    for object in ALL_PROPS:
        if(not paused):
            object.update()
            
        object.draw(screen)
        if(isinstance(object, PLAYER)):
            player = object

    if not paused:
        message = player.handle_collisions()
        if message == 'collision':
             game_state = 'over'
        elif message == 'win':
            game_state = 'win'
        if(max(player.velocity) == 0):
            run_launch(player) # draw arrow, make it so clicking within the screen will launch the player

    # Update the display
    pygame.display.flip()


clock = pygame.time.Clock()

def handle_event(object, event):
    global selected_charge
    if (isinstance(object, POINT_CHARGE)):
    # print(selected_charge)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if object.rect.collidepoint(event.pos) and selected_charge == None:
                selected_charge = object
            elif object.rect.collidepoint(event.pos):
                 selected_charge == object
                 selected_charge = None

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "game":
            for object in ALL_PROPS:
                if not (isinstance(object, PLAYER)):
                    handle_event(object,event)
        if game_state == "free_design":
            for object in ALL_PROPS:
                object.handle_event(event)

    # Update screen based on the current state
    if game_state == "title":
        draw_title_screen()
    elif game_state == "start_page":
        draw_start_page()
    elif game_state == "game":
        draw_game()
    elif game_state == "free_design":
        free_design_screen()
    elif game_state == "over":
        draw_lose_page()
    elif game_state == "win":
        draw_win_page()

    if render_E_simulation:
        screen.blit(E_sim_layer, (0, 0))

    if render_B_simulation:
        screen.blit(B_sim_layer, (0, 0))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()