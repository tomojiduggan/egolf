import pygame
import button
import sys
import Global_Var as Global_Var
from physics.props import WIRE, POINT_CHARGE, SOLENOID
import numpy as np

pygame.init()
# Screen dimensions
SCREEN_WIDTH = Global_Var.SCREEN_WIDTH
SCREEN_HEIGHT = Global_Var.SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Electromagnetic Golf")
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
# Fonts
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 20)

# Button dimensions
button_width, button_height = 100, 50
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = (SCREEN_HEIGHT - button_height) // 2

# Game state
game_state = "title"

# Props
props_list = []  # List to store created props

# Load background image
background_image = pygame.image.load("pictures/screen_cov.webp")  # Replace with your file path
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to fit the screen
start_button_image = pygame.image.load("pictures/start_btn.png")
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
def restart_game():
    print("Restarting the game...")
    # Add code here to reset the game state, e.g., reset score, position, etc.

def pause_game():
    print("Pausing the game...")
    # Add code here to pause the game, e.g., freeze the game loop or display a pause screen.

def place_object():
    print("Placing object...")
    # Add code here to place an object in the game, e.g., ball or item placement.

def swap_objects():
    print("Swapping objects...")
    # Add code here to swap between two objects in the game.

def extra_action_E():
    print("Performing extra action E...")
    # Add code for whatever action the "E" button triggers.

def extra_action_B():
    print("Performing extra action B...")
    # Add code for whatever action the "B" button triggers.
def back_to_title():
    global game_state
    print("Returning to title screen...")
    game_state = 'start_page'

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

# Create the free design screen
def free_design_screen():
    """Draw the free design screen."""
    global game_state, props_list
    screen.fill(WHITE)

    # Draw existing props
    for prop in props_list:
        if isinstance(prop, WIRE):
            pygame.draw.line(screen, BLACK, prop.start, prop.end, 3)
        elif isinstance(prop, POINT_CHARGE):
            pygame.draw.circle(screen, BLUE, (int(prop.position[0]), int(prop.position[1])), 10)
        elif isinstance(prop, SOLENOID):
            prop.draw(screen)  # Solenoid is an image, so just draw it

    # Draw buttons at the bottom
    add_wire_button.draw(screen)
    add_charge_button.draw(screen)
    add_solenoid_button.draw(screen)
    add_block_button.draw(screen)
    add_back_button.draw(screen)
    add_save_button.draw(screen)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_event(event)

def handle_event(event):
    """Handle events for adding and dragging props."""
    global props_list
    if add_back_button.draw(screen):
        back_to_title()

    if event.type == pygame.MOUSEBUTTONDOWN:
        # Check if any button is clicked to create a prop
        if add_wire_button.rect.collidepoint(event.pos):
            new_wire = WIRE(np.array([100, 100]), np.array([200, 200]), 5)  # Example start and end positions
            props_list.append(new_wire)
        elif add_charge_button.rect.collidepoint(event.pos):
            new_charge = POINT_CHARGE(np.array([300, 300]), 1e-6, True)  # Example position and charge
            props_list.append(new_charge)
        elif add_solenoid_button.rect.collidepoint(event.pos):
            new_solenoid = SOLENOID(10, 1, [0, 0, 1], [500, 500], 'pictures/solenoid.png')
            props_list.append(new_solenoid)
        elif add_block_button.rect.collidepoint(event.pos):
            # Create a block (if needed, you can create a simple rectangle object or other)
            pass  # Block creation code goes here

        # Check if any prop is being clicked for dragging
        for prop in props_list:
            if isinstance(prop, SOLENOID) and prop.rect.collidepoint(event.pos):
                prop.handle_event(event)  # Start dragging

    elif event.type == pygame.MOUSEBUTTONUP:
        # Stop dragging
        for prop in props_list:
            if isinstance(prop, SOLENOID):
                prop.handle_event(event)

    elif event.type == pygame.MOUSEMOTION:
        # Update position if dragging
        for prop in props_list:
            if isinstance(prop, SOLENOID):
                prop.handle_event(event)

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
                restart_game()
            elif current_tile == 1:  # Pause Button
                paused = not paused
                pause_game() if paused else print("Game Resumed")
            elif current_tile == 2:  # Place Button
                place_object()
            elif current_tile == 3:  # Swap Button
                swap_objects()
            elif current_tile == 4:  # Extra Action Button E
                extra_action_E()
            elif current_tile == 5:  # Extra Action Button B
                extra_action_B()
            elif current_tile == 6: 
                back_to_title() # Back Button
    # Highlight the selected button with a gray border

    if current_tile != -1:  
        pygame.draw.rect(screen, GRAY, button_list[current_tile].rect,3)  # Add padding around the button
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


