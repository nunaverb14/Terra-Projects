from sprite import *
import pygame

screen = pygame.display.set_mode(640, 640)
pygame.display.set_caption("Color Fighter")
clock = pygame.time.Clock()

player1 = Player()
player2 = Player()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")



    Player.players.draw(screen)
    pygame.display.flip()

    dt = clock.tick(60) / 1000
    Player.players.update(dt)


pygame.quit()
    