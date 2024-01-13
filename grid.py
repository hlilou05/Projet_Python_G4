import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 30
TILE_SIZE = 20  # Adjust the tile size as needed
GRID_WIDTH = GRID_SIZE * TILE_SIZE
GRID_HEIGHT = GRID_SIZE * TILE_SIZE
BOB_SIZE = TILE_SIZE
FPS = 3

# Create the game window
screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
pygame.display.set_caption("2D Grid Game")

# Load images
tile_image = pygame.image.load("tile.png")
tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))

# Function for changing Bob's color
def colorchange(bob_number):
    if bob_number == 1:
        return pygame.image.load("bob1.png")
    elif bob_number == 2:
        return pygame.image.load("bob2.png")
    elif bob_number == 3:
        return pygame.image.load("bob3.png")
    else:
        # Default to the original image
        return pygame.image.load("bob2.png")

# Function for moving randomly
def move_random(bob_pos):
    choice = random.choice([
        move_right, move_left, move_up, move_down,
        move_northeast, move_northwest, move_southeast, move_southwest
    ])
    return choice(bob_pos)

# Initial position and color of Bobs (centered in their grid cells)
bob_data = [
    (
        random.randint(0, GRID_WIDTH - BOB_SIZE) // BOB_SIZE,
        random.randint(0, GRID_HEIGHT - BOB_SIZE) // BOB_SIZE,
        random.randint(1, 3),  # Assign a random color number (1, 2, or 3)
        1  # Initial level
    )
    for _ in range(15)
]

# Functions for movement
def move_right(bob_pos):
    x, y, color, level = bob_pos
    if x < GRID_SIZE - 1:
        x += 1
    return x, y, color, level

def move_left(bob_pos):
    x, y, color, level = bob_pos
    if x > 0:
        x -= 1
    return x, y, color, level

def move_up(bob_pos):
    x, y, color, level = bob_pos
    if y > 0:
        y -= 1
    return x, y, color, level

def move_down(bob_pos):
    x, y, color, level = bob_pos
    if y < GRID_SIZE - 1:
        y += 1
    return x, y, color, level

def move_northeast(bob_pos):
    x, y, color, level = bob_pos
    if x < GRID_SIZE - 1 and y > 0:
        x += 1
        y -= 1
    return x, y, color, level

def move_northwest(bob_pos):
    x, y, color, level = bob_pos
    if x > 0 and y > 0:
        x -= 1
        y -= 1
    return x, y, color, level

def move_southeast(bob_pos):
    x, y, color, level = bob_pos
    if x < GRID_SIZE - 1 and y < GRID_SIZE - 1:
        x += 1
        y += 1
    return x, y, color, level

def move_southwest(bob_pos):
    x, y, color, level = bob_pos
    if x > 0 and y < GRID_SIZE - 1:
        x -= 1
        y += 1
    return x, y, color, level

# Game loop
clock = pygame.time.Clock()

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the Bobs' positions
    new_bob_data = [move_random(bob_pos) for bob_pos in bob_data]

    # Check for collisions and level up if two Bobs cross the same cell
    bob_positions = set((bob[0], bob[1]) for bob in new_bob_data)
    for i in range(len(new_bob_data)):
        x, y, color, level = new_bob_data[i]
        if (x, y) in bob_positions and level < 3:
            level += 1
            color = random.randint(1, 3)
        new_bob_data[i] = (x, y, color, level)

    # Update the screen
    screen.fill((0, 0, 0))

    # Draw grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            screen.blit(tile_image, (col * TILE_SIZE, row * TILE_SIZE))

    # Draw Bobs (centered in their grid cells)
    for bob_pos in new_bob_data:
        x, y, color, level = bob_pos
        x *= TILE_SIZE
        y *= TILE_SIZE
        x += (TILE_SIZE - BOB_SIZE) // 2  # Offset to center within the cell
        y += (TILE_SIZE - BOB_SIZE) // 2
        bob_image = pygame.transform.scale(colorchange(color), (BOB_SIZE, BOB_SIZE))
        screen.blit(bob_image, (x, y))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
