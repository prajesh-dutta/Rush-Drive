import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'D:\Python Projects\pythonProject')

background = pygame.image.load(os.path.join(image_path, 'Road.png'))
car_img = pygame.image.load(os.path.join(image_path, 'Car.png'))
obstacle_img = pygame.image.load(os.path.join(image_path, 'Obstacle.png'))

# Scale images
background = pygame.transform.scale(background, (width, height))
car_img = pygame.transform.scale(car_img, (70, 130))
obstacle_img = pygame.transform.scale(obstacle_img, (70, 130))

# Player car
player_width = 70
player_height = 130
player_x = width // 2 - player_width // 2
player_y = height - player_height - 20
player_speed = 5

# Obstacle
obstacle_width = 70
obstacle_height = 130
obstacle_speed = 5
obstacle_x = random.randint(50, width - obstacle_width - 50)
obstacle_y = -obstacle_height

# Scrolling background
bg_y1 = 0
bg_y2 = -height
bg_speed = 5

# Game loop
clock = pygame.time.Clock()
running = True
score = 0

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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player car
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 50:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_width - 50:
        player_x += player_speed

    # Move obstacle
    obstacle_y += obstacle_speed

    # Check for collision
    if player_y < obstacle_y + obstacle_height and player_y + player_height > obstacle_y:
        if player_x < obstacle_x + obstacle_width and player_x + player_width > obstacle_x:
            print(f"Game Over! Score: {score}")
            running = False

    # Reset obstacle when it goes off screen
    if obstacle_y > height:
        obstacle_y = -obstacle_height
        obstacle_x = random.randint(50, width - obstacle_width - 50)
        score += 1

    # Draw scrolling background
    draw_background()

    # Draw player car
    window.blit(car_img, (player_x, player_y))

    # Draw obstacle
    window.blit(obstacle_img, (obstacle_x, obstacle_y))

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    window.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Set the game's FPS
    clock.tick(60)

# Quit the game
pygame.quit()