from sprites import *
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen_rect = screen.get_rect()
pygame.display.set_caption("Color Fighter")
clock = pygame.time.Clock()

roboto_mono = pygame.font.SysFont("ROBOTOMONO", 24)


Platform(None, ((screen.get_rect().left, screen.get_rect().bottom - 1), (screen.width, 1)))
Platform(None, pygame.Rect(screen_rect.centerx - 200, 525, 400, 50))
Platform(None, (200, 300, 200, 50))


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

        surf = pygame.transform.scale_by(pygame.Surface((32, 8), pygame.SRCALPHA), 5)
        surf.fill("white")
        pygame.draw.rect(surf, "black", ((0, 0), surf.size), 2)
        text = roboto_mono.render(str(player.health), True, "green")
        surf.blit(text, text.get_rect(center=surf.get_rect().center ))

        i = Player.players.sprites().index(player)
        screen.blit(surf, (0 if not i % 2 else screen.get_rect().right - surf.width, 48 * (i // 2)))


    for shot in Projectile.shots:
        if not shot.rect.colliderect(screen.get_rect()):
            shot.kill()

        hit = pygame.sprite.spritecollide(shot, Projectile.shots, False)
        if len(hit) > 1:
            shot.kill()
            hit[1].kill()

        hit = pygame.sprite.spritecollide(shot, Player.players, False)
        for player in hit:
            if player.type != shot.type:
                if player.action == 2:
                    if (player.direction + shot.dir):
                        player.health -= 3
                else:
                    player.health -= 3
                shot.kill()
                break

        

    Player.players.draw(screen)
    Projectile.shots.draw(screen)
    Platform.platforms.draw(screen)

    pygame.display.flip()

    dt = clock.tick(60) / 1000
    Platform.platforms.update(dt)
    Player.players.update(dt)
    Projectile.shots.update(dt)


pygame.quit()
