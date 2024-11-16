import pygame
import button
import sys
import Global_Var as Global_Var

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
button_font = pygame.font.Font(None, 36)

# Button dimensions
button_width, button_height = 200, 50
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = (SCREEN_HEIGHT - button_height) // 2

# Game state
game_state = "title"

# Load background image
background_image = pygame.image.load("pictures/screen_cov.webp")  # Replace with your file path
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to fit the screen

start_button_image = pygame.image.load("pictures/start_btn.png")
start_button = button.Button((SCREEN_WIDTH - start_button_image.get_width() * 0.5)// 2, SCREEN_HEIGHT-70, start_button_image, 0.5)
def draw_title_screen():
    """Draw the title screen with a Start button."""
    screen.blit(background_image, (0, 0))  # Draw the background
    if start_button.draw(screen):  # If the button is clicked
        return True
    return False

def draw_game():
    """Draw the game screen."""
    screen.fill(WHITE)
    game_text = font.render("Game Screen", True, BLACK)
    game_rect = game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(game_text, game_rect)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update screen based on the current state
    if game_state == "title":
        if draw_title_screen():
            game_state = "game"  # Transition to the game state

    elif game_state == "game":
        draw_game()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

'''
clock = pygame.time.Clock()
FPS = 60





#create display window
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 900
LOWER_MARGIN = 720-SCREEN_HEIGHT
SIDE_MARGIN = 1024-SCREEN_WIDTH

#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#pygame.display.set_caption('Button Demo')
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('EM-Golf')































#load button images
restart_img = pygame.image.load('Button_images/restart_btn.png').convert_alpha()
pause_img = pygame.image.load('Button_images/pause_btn.png').convert_alpha()
place_img = pygame.image.load('Button_images/place_btn.png').convert_alpha()
swap_img = pygame.image.load('Button_images/swap_btn.png').convert_alpha()
E_img = pygame.image.load('Button_images/E_btn.png').convert_alpha()
B_img = pygame.image.load('Button_images/B_btn.png').convert_alpha()

#create button instances
#start_button = button.Button(100, 200, start_img, 0.8)
#exit_button = button.Button(450, 200, exit_img, 0.8)
restart_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN -70, restart_img, 0.3)
pause_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 70, pause_img, 0.3)


'''
'''
def draw_bg():
	screen.fill(())
	width = sky_img.get_width()
	for x in range(4):
		screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
		screen.blit(mountain_img, ((x * width) - scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
		screen.blit(pine1_img, ((x * width) - scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
		screen.blit(pine2_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))
'''

'''
#game loop
run = True
while run:

	screen.fill((202, 228, 241))

	if start_button.draw(screen):
		print('START')
	if exit_button.draw(screen):
		print('EXIT')
    

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
'''