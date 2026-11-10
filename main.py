import pygame

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((560, 560))
pygame.display.set_caption("Image Slicer Puzzle Game")
clock = pygame.Clock()

# Game State Vars
game_start = False
game_over = False
game_win = False


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()