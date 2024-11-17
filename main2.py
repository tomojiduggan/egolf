import pygame
import button
import sys
import Global_Var as Global_Var
from physics.props import WIRE, POINT_CHARGE, SOLENOID
import numpy as np
from runlevel import getLevel

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

# Load background image
background_image = pygame.image.load("pictures/screen_cov.webp")  # Replace with your file path
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to fit the screen
start_button_image = pygame.image.load("pictures/start_btn.png")
free_design_image = pygame.image.load("pictures/place_btn.png")
start_button = button.Button((SCREEN_WIDTH - start_button_image.get_width() * 0.5)// 2, SCREEN_HEIGHT-70, start_button_image, 0.5)
start_game_image = pygame.image.load("pictures/start_btn.png")
# load start page buttons
game_img = pygame.image.load('pictures/game.jpg')
new_game = button.Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, game_img, 0.06)
free_design_image = pygame.image.load('pictures/map_design.jpg')
free_design = button.Button(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 , free_design_image, 0.06)
# load design page buttons
add_wire_image = pygame.image.load('pictures/add_wire.png')
add_wire_button = button.Button(50, SCREEN_HEIGHT - 100, add_wire_image, 0.04)
add_charge_image = pygame.image.load('pictures/add_charge.png')
add_charge_button = button.Button(150, SCREEN_HEIGHT - 100, add_charge_image, 0.04)
add_solenoid_image = pygame.image.load('pictures/add_solenoid.png')
add_solenoid_button = button.Button(250, SCREEN_HEIGHT - 100, add_solenoid_image, 0.04)
add_block_image = pygame.image.load('pictures/add_block.png')
add_block_button = button.Button(350, SCREEN_HEIGHT - 100, add_block_image, 0.04)
add_back_image = pygame.image.load('pictures/back.png')
back_button = button.Button(650, SCREEN_HEIGHT - 100, add_back_image, 0.04)
add_back_button = button.Button(450, SCREEN_HEIGHT - 100, add_back_image, 0.04)
add_save_image = pygame.image.load('pictures/save.png')
add_save_button = button.Button(550, SCREEN_HEIGHT - 100, add_save_image, 0.04)
# load game play button images
restart_img = pygame.image.load('pictures/restart_btn.png', ).convert_alpha()
restart_button = button.Button(50, SCREEN_HEIGHT - 100, restart_img, 0.3)
pause_img = pygame.image.load('pictures/pause_btn.png').convert_alpha()
pause_button = button.Button(150, SCREEN_HEIGHT - 100, pause_img, 0.3)
place_img = pygame.image.load('pictures/place_btn.png').convert_alpha()
place_button = button.Button(250, SCREEN_HEIGHT - 100, place_img, 0.3)
swap_img = pygame.image.load('pictures/swap_btn.png').convert_alpha()
swap_button = button.Button(350, SCREEN_HEIGHT - 100, swap_img, 0.3)
E_img = pygame.image.load('pictures/E_btn.png').convert_alpha()
E_button = button.Button(450, SCREEN_HEIGHT - 100, E_img, 0.3)
B_img = pygame.image.load('pictures/B_btn.png').convert_alpha()
B_button = button.Button(550, SCREEN_HEIGHT - 100, B_img, 0.3)

run = True
paused = False

# Button functions
def pause_game():
    print("Pausing the game...")
    # Add code here to pause the game, e.g., freeze the game loop or display a pause screen.

def back_to_title():
    global game_state
    print("Returning to title screen...")
    game_state = 'start_page'
    
    
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
    if free_design.draw(screen):
        game_state = "free_design"


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
    
def draw_game():
    """Draw the game screen."""
    global paused  # Ensure `paused` is accessible
    
    # Clear the screen
    screen.fill(WHITE)
    
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
                print("Restarting the game...")
            elif current_tile == 1:  # Pause Button
                paused = not paused
                pause_game() if paused else print("Game Resumed")
            elif current_tile == 2:  # Place Button
                print("Placing charge...")
            elif current_tile == 3:  # Swap Button
                print("Swapping objects...")
            elif current_tile == 4:  # Extra Action Button E
                print("Performing extra action E...")
            elif current_tile == 5:  # Extra Action Button B
                print("Performing extra action B...")
                # extra_action_B()

    # Highlight the selected tile with a gray border
    if current_tile != -1:  # Only highlight if a button is selected
        pygame.draw.rect(screen, GRAY, button_list[current_tile].rect, 3)

    # Update the display
    pygame.display.flip()



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

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()


