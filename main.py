from sprite import *
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Color Fighter")
clock = pygame.time.Clock()

roboto_mono = pygame.font.SysFont("ROBOTOMONO", 24)

player1 = Player((0, screen.get_rect().bottom), ["w", "a", "s", "d", "q", "e"])
player1_images = []
for i in range(6):
    surf = pygame.Surface((24, 32))
    surf.fill("red")
    surf.blit(roboto_mono.render(str(i), True, "white"))
    player1_images.append(surf)
player1.set(1, player1_images)

player2 = Player((screen.get_rect().right, screen.get_rect().bottom), ["i", "j", "k", "l", "u", "o"])
player2_images = []
for i in range(6):
    surf = pygame.Surface((24, 32))
    surf.fill("blue")
    surf.blit(roboto_mono.render(str(i), True, "white"))
    player2_images.append(surf)
player2.set(2, player2_images)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    for player in Player.players.sprites():
        player.rect.clamp_ip(screen.get_rect())

        surf = pygame.transform.scale_by(pygame.Surface((32, 8)), 5)
        surf.fill("white")
        pygame.draw.rect(surf, "black", ((0, 0), surf.size), 2)
        text = roboto_mono.render(str(player.health), True, "green")
        surf.blit(text, text.get_rect(center=surf.get_rect().center ))

        i = Player.players.sprites().index(player)
        screen.blit(surf, (0 if not i % 2 else screen.get_rect().right - surf.width, 48 * (i // 2)))



    Player.players.draw(screen)
    pygame.display.flip()

    dt = clock.tick(60) / 1000
    Player.players.update(dt)


pygame.quit()
    