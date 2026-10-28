from sprites import *
import pygame
import random

random.seed("Hello World")

# Pygame Init
pygame.init()
screen = pygame.display.set_mode((960, 768))
pygame.display.set_caption("Disaster Relief")
clock = pygame.time.Clock()

# Game Areas

# Game Board
board = pygame.Rect(0, 0, 640, 640)
pixel_size = 32
item_size = 96

for x in range(0, board.w // pixel_size):
    for y in range(board.h // pixel_size):
        Tile(0, (x * pixel_size + board.left, y * pixel_size + board.top))


# Tower Shop
shop = pygame.Rect(board.right, 0, screen.width - board.width, screen.height)
item_box = pygame.Rect(shop.topleft, (shop.width, item_size))


# Tower Info
info = pygame.Rect(0, board.bottom, board.width, screen.height - board.height)


# Start Game Loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw Backgrounds
    screen.fill("black")
    pygame.draw.rect(screen, "#202020", board)
    pygame.draw.rect(screen, "#202020", shop)
    pygame.draw.rect(screen, "#2e2e2e", info)

    for i in range(shop.height // item_size):
        item_box.top = i * item_size
        pygame.draw.rect(screen, "#404040", item_box, 5)

    # Update Screen
    Tile.tiles.draw(screen)
    Tower.towers.draw(screen)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()






