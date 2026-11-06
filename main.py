from sprites import *
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
    screen.fill("gold")

    ###
    Fruit.fruits.draw(screen)
    pygame.display.flip()

    ###
    dt = clock.tick(60) / 1000
    Fruit.fruits.update(dt)

    
pygame.quit()