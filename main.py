import pygame

###
pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Fall Farmer")
clock = pygame.Clock()

###


###
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    ###
    screen.fill("orange")

    ###
    pygame.display.flip()
    clock.tick(60)

pygame.quit()