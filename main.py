import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Improved Car Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load images
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'according_to_your_path name')

background = pygame.image.load(os.path.join(image_path, 'road.png'))
player_img = pygame.image.load(os.path.join(image_path, 'player_car.png'))
obstacle_img = pygame.image.load(os.path.join(image_path, 'obstacle_car.png'))

# Scale images
background = pygame.transform.scale(background, (width, height))
player_img = pygame.transform.scale(player_img, (60, 100))
obstacle_img = pygame.transform.scale(obstacle_img, (60, 100))

# Player car
player_width = 60
player_height = 100
player_x = width // 2 - player_width // 2
player_y = height - player_height - 20
player_speed = 7

# Obstacles
obstacle_width = 60
obstacle_height = 100
obstacle_speed = 5
num_obstacles = 3
obstacles = []

for _ in range(num_obstacles):
    obstacle = {
        'x': random.randint(50, width - obstacle_width - 50),
        'y': random.randint(-height, -obstacle_height),
        'speed': random.randint(5, 8)
    }
    obstacles.append(obstacle)

# Scrolling background
bg_y1 = 0
bg_y2 = -height
bg_speed = 5

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# Game loop
clock = pygame.time.Clock()
running = True
score = 0
high_score = 0

def draw_background():
    global bg_y1, bg_y2
    window.blit(background, (0, bg_y1))
    window.blit(background, (0, bg_y2))
    bg_y1 += bg_speed
    bg_y2 += bg_speed
    if bg_y1 >= height:
        bg_y1 = -height
    if bg_y2 >= height:
        bg_y2 = -height

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)

def show_menu():
    window.fill(BLACK)
    draw_text("Car Game", 64, WHITE, width // 2, height // 4)
    draw_text("Press SPACE to start", 32, WHITE, width // 2, height // 2)
    draw_text(f"High Score: {high_score}", 32, WHITE, width // 2, height * 3 // 4)

def show_game_over():
    window.fill(BLACK)
    draw_text("Game Over", 64, RED, width // 2, height // 4)
    draw_text(f"Score: {score}", 32, WHITE, width // 2, height // 2)
    draw_text("Press SPACE to play again", 32, WHITE, width // 2, height * 3 // 4)

def reset_game():
    global player_x, player_y, obstacles, score
    player_x = width // 2 - player_width // 2
    player_y = height - player_height - 20
    obstacles = []
    for _ in range(num_obstacles):
        obstacle = {
            'x': random.randint(50, width - obstacle_width - 50),
            'y': random.randint(-height, -obstacle_height),
            'speed': random.randint(5, 8)
        }
        obstacles.append(obstacle)
    score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == MENU or game_state == GAME_OVER:
                    game_state = PLAYING
                    reset_game()

    if game_state == PLAYING:
        # Move player car
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_width - 50:
            player_x += player_speed

        # Move obstacles
        for obstacle in obstacles:
            obstacle['y'] += obstacle['speed']
            if obstacle['y'] > height:
                obstacle['y'] = random.randint(-height, -obstacle_height)
                obstacle['x'] = random.randint(50, width - obstacle_width - 50)
                obstacle['speed'] = random.randint(5, 8)
                score += 1

        # Check for collision
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], obstacle_width, obstacle_height)
            if player_rect.colliderect(obstacle_rect):
                game_state = GAME_OVER
                if score > high_score:
                    high_score = score

        # Draw everything
        draw_background()
        window.blit(player_img, (player_x, player_y))
        for obstacle in obstacles:
            window.blit(obstacle_img, (obstacle['x'], obstacle['y']))
        draw_text(f"Score: {score}", 36, WHITE, width - 100, 30)

    elif game_state == MENU:
        show_menu()

    elif game_state == GAME_OVER:
        show_game_over()

    # Update display
    pygame.display.flip()

    # Set the game's FPS
    clock.tick(60)

# Quit the game
pygame.quit()