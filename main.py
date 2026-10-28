from sprites import *
import pygame

# Pygame Init
pygame.init()
screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption("Disaster Relief")
clock = pygame.time.Clock()

# Game Areas
board = pygame.Rect(0, 0, 500, 500)
board.centerx = screen.width / 2
pixel_size = 25

# Start Game Loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw Backgrounds
    screen.fill("Red")
    pygame.draw.rect(screen, "black", board)

    Tile.tiles.draw(screen)

    for x in range(0, board.w//pixel_size):
        for y in range(board.h//pixel_size):
            pygame.draw.rect(screen, "gray", pygame.Rect(x * pixel_size + board.left, y * pixel_size + board.top, pixel_size, pixel_size), 2)





    # Update Screen
    pygame.display.flip()
    clock.tick(60)


pygame.quit()






