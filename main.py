# import pygame
# import random
# import sys

# # Initialize Pygame
# pygame.init()

# # Screen dimensions
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600

# # Colors
# WHITE = (255, 255, 255)
# BLUE = (135, 206, 250)
# RED = (255, 0, 0)

# # Game setup
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Flying Bird vs Rockets")
# clock = pygame.time.Clock()
# FPS = 60

# # Player (Bird) settings
# player_width = 60
# player_height = 60
# player_x = SCREEN_WIDTH // 2 - player_width // 2
# player_y = 10  # Positioned at the top of the screen
# player_speed = 7

# # Enemy (Rocket) settings
# enemy_width = 40
# enemy_height = 60
# enemy_speed = 5
# enemy_spawn_time = 1500  # Milliseconds between spawns

# # Scoring
# score = 0
# font = pygame.font.Font(None, 36)

# # Load images with transparency
# player_image = pygame.image.load("player.png")
# player_image = pygame.transform.scale(player_image, (player_width, player_height))

# enemy_image = pygame.image.load("enemy.png")
# enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))

# # Enemy list
# enemies = []

# # Add an event to spawn enemies
# SPAWN_ENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(SPAWN_ENEMY, enemy_spawn_time)

# # Function to draw the player
# def draw_player(x, y):
#     screen.blit(player_image, (x, y))

# # Function to draw enemies
# def draw_enemies(enemy_list):
#     for enemy in enemy_list:
#         screen.blit(enemy_image, (enemy["x"], enemy["y"]))

# # Function to update enemy positions
# def update_enemies(enemy_list):
#     global score
#     for enemy in enemy_list[:]:
#         enemy["y"] -= enemy_speed  # Move enemies upwards
#         if enemy["y"] + enemy_height < 0:  # Enemy moves off-screen
#             enemy_list.remove(enemy)
#             score += 1  # Increment score

# # Collision detection
# def check_collision(player_rect, enemy_list):
#     for enemy in enemy_list:
#         enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)
#         if player_rect.colliderect(enemy_rect):
#             return True
#     return False

# # Game loop
# running = True
# while running:
#     screen.fill(BLUE)  # Background color

#     # Event handling
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == SPAWN_ENEMY:
#             # Spawn an enemy at a random x position
#             enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
#             enemy_y = SCREEN_HEIGHT  # Spawn from the bottom
#             enemies.append({"x": enemy_x, "y": enemy_y})

#     # Player movement
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT] and player_x > 0:
#         player_x -= player_speed
#     if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
#         player_x += player_speed

#     # Draw player
#     draw_player(player_x, player_y)

#     # Update and draw enemies
#     update_enemies(enemies)
#     draw_enemies(enemies)

#     # Collision detection
#     player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
#     if check_collision(player_rect, enemies):
#         message = font.render("Game Over! Press Q to quit.", True, RED)
#         screen.blit(message, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
#         pygame.display.flip()
#         pygame.time.delay(2000)
#         running = False

#     # Display score
#     score_text = font.render(f"Score: {score}", True, WHITE)
#     screen.blit(score_text, (10, 10))

#     # Update the screen
#     pygame.display.flip()
#     clock.tick(FPS)

# # Quit the game
# pygame.quit()
# sys.exit()


import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flying Bird vs Rockets")
clock = pygame.time.Clock()
FPS = 60

# Player (Bird) settings
player_width = 60
player_height = 60
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = 10  # Positioned at the top of the screen
player_speed = 7
invincible = False  # For shield power-up
invincible_timer = 0

# Enemy (Rocket) settings
enemy_width = 40
enemy_height = 60
enemy_speed = 5
enemy_spawn_time = 1500  # Milliseconds between spawns

# Power-Up (Shield) settings
power_up_width = 30
power_up_height = 30
power_up_spawn_time = 10000  # Spawn every 10 seconds
power_up_position = None  # Initially, no power-up

# Scoring and levels
score = 0
level = 1
font = pygame.font.Font(None, 36)

# Load images
background_image = pygame.image.load("colored_forest.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (player_width, player_height))

enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))

shield_image = pygame.image.load("fight.png")
shield_image = pygame.transform.scale(shield_image, (power_up_width, power_up_height))

# Load sound effects
collision_sound = pygame.mixer.Sound("collision.mp3")
score_sound = pygame.mixer.Sound("score.mp3")
power_up_sound = pygame.mixer.Sound("power-up.mp3")

# Enemy list
enemies = []

# Add an event to spawn enemies and power-ups
SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, enemy_spawn_time)

SPAWN_POWER_UP = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_POWER_UP, power_up_spawn_time)

# Function to draw the player
def draw_player(x, y):
    screen.blit(player_image, (x, y))

# Function to draw enemies
def draw_enemies(enemy_list):
    for enemy in enemy_list:
        screen.blit(enemy_image, (enemy["x"], enemy["y"]))

# Function to update enemy positions
def update_enemies(enemy_list):
    global score, level, enemy_speed
    for enemy in enemy_list[:]:
        enemy["y"] -= enemy_speed  # Move enemies upwards
        if enemy["y"] + enemy_height < 0:  # Enemy moves off-screen
            enemy_list.remove(enemy)
            score += 1  # Increment score
            pygame.mixer.Sound.play(score_sound)

    # Increase difficulty as score grows
    if score % 10 == 0 and score != 0:  # Every 10 points, increase level
        level += 1
        enemy_speed += 1  # Increase rocket speed

# Collision detection
def check_collision(player_rect, enemy_list):
    for enemy in enemy_list:
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)
        if player_rect.colliderect(enemy_rect):
            return True
    return False

# Check if player gets the power-up
def check_power_up_collision(player_rect, power_up_position):
    if power_up_position:
        power_up_rect = pygame.Rect(power_up_position[0], power_up_position[1], power_up_width, power_up_height)
        if player_rect.colliderect(power_up_rect):
            return True
    return False

# Game loop
running = True
while running:
    screen.blit(background_image, (0, 0))  # Draw the background image

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_ENEMY:
            # Spawn an enemy at a random x position
            enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
            enemy_y = SCREEN_HEIGHT  # Spawn from the bottom
            enemies.append({"x": enemy_x, "y": enemy_y})
        if event.type == SPAWN_POWER_UP:
            # Spawn a shield power-up at a random position
            power_up_x = random.randint(0, SCREEN_WIDTH - power_up_width)
            power_up_y = random.randint(0, SCREEN_HEIGHT - power_up_height)
            power_up_position = (power_up_x, power_up_y)

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - player_height:
        player_y += player_speed

    # Check if player reaches the bottom of the screen
    if player_y >= SCREEN_HEIGHT - player_height:
        message = font.render("You Win! Press Q to quit.", True, GREEN)
        screen.blit(message, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    # Draw player
    draw_player(player_x, player_y)

    # Update and draw enemies
    update_enemies(enemies)
    draw_enemies(enemies)

    # Draw power-up if active
    if power_up_position:
        screen.blit(shield_image, power_up_position)

    # Check for collisions
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    if not invincible and check_collision(player_rect, enemies):
        pygame.mixer.Sound.play(collision_sound)
        message = font.render("Game Over! Press Q to quit.", True, RED)
        screen.blit(message, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    # Check for power-up collision
    if check_power_up_collision(player_rect, power_up_position):
        pygame.mixer.Sound.play(power_up_sound)
        invincible = True
        invincible_timer = pygame.time.get_ticks()  # Start invincibility timer
        power_up_position = None  # Remove the power-up from the screen

    # Handle invincibility timeout
    if invincible and pygame.time.get_ticks() - invincible_timer > 5000:  # 5 seconds of invincibility
        invincible = False

    # Display score and level
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the screen
    pygame.display.flip()
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()
