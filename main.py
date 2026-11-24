from sprites import *
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen_rect = screen.get_rect()
pygame.display.set_caption("Color Fighter")
clock = pygame.time.Clock()

roboto_mono = pygame.font.SysFont("ROBOTOMONO", 24)

ground = Platform(None, ((screen.get_rect().left, screen.get_rect().bottom - 1), (screen.width, 1)))
center = Platform(None, pygame.Rect(screen_rect.centerx - 200, 525, 400, 50))
left = Platform(None, (200, 300, 200, 50))
right = Platform(None, (900, 300, 200, 50))

Player.set_images(screen, ["Ice_Sprite.png", "Fire_Sprite.png"])
# debug {
# player1_images = []
# surf1 = pygame.Surface((24 * 3, 32 * 2))
# for i in range(6):
#     surf1.fill("blue")
#     text = roboto_mono.render(str(i), True, "white")
#     surf1.blit(text, ((24 * (i % 3), 32 * (i // 3)), (24, 32)))
#     player1_images.append(surf1)

# player2_images = []
# surf2 = pygame.Surface((24 * 3, 32 * 2))
# for i in range(6):
#     surf2.fill("red")
#     text = roboto_mono.render(str(i), True, "white")
#     surf2.blit(text, ((12 * (i % 3), 16 * (i // 3)), (24, 32)))
#     player2_images.append(surf2)

# Player.set_images(screen, [surf1, surf2])
# }

sprite = pygame.image.load(resource_path("images/Ice_Sprite.png"))

player1 = Player((0, screen.get_rect().bottom), ["w", "a", "s", "d", "q", "e"])
player2 = Player((screen.get_rect().right, screen.get_rect().bottom), ["i", "j", "k", "l", "u", "o"])
player1.set(0)
player2.set(1)

game_start = True
game_over = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    if game_start and not game_over:
        for player in Player.players.sprites():
            player.rect.clamp_ip(screen.get_rect())

            surf = pygame.transform.scale_by(pygame.Surface((32, 8), pygame.SRCALPHA), 5)
            surf.fill("white")
            pygame.draw.rect(surf, "black", ((0, 0), surf.size), 2)
            text = roboto_mono.render(str(player.health), True, "green")
            surf.blit(text, text.get_rect(center=surf.get_rect().center ))

            i = Player.players.sprites().index(player)
            screen.blit(surf, (0 if not i % 2 else screen.get_rect().right - surf.width, 48 * (i // 2)))


            if player.health <= 0:
                winner = not player.num
                game_over = True
        

        for shot in Projectile.shots:
            if not shot.rect.colliderect(screen.get_rect()):
                shot.kill()

            hit = pygame.sprite.spritecollide(shot, Projectile.shots, False)
            if len(hit) > 1:
                shot.kill()
                hit[1].kill()

            hit = pygame.sprite.spritecollide(shot, Player.players, False)
            for player in hit:
                if player.num != shot.parent:
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

        dt = clock.tick(60) / 1000
        Platform.platforms.update(dt)
        Player.players.update(dt)
        Projectile.shots.update(dt)
    else:
        if not game_start:
            pass
        else:
            print(f" Winner: Player {winner + 1}")


    # for i in range(6):
    #     sprite.blit(roboto_mono.render(str(i), True, "white"), ((24 * (i % 3), 32 * (i // 3))))
    #     screen.blit(sprite.subsurface(((24 * (i % 3), 32 * (i // 3))), (24, 32)), ((48 * (i % 3), 64 * (i // 3))))
    # screen.blit(sprite, (500, 50))
    pygame.display.flip()

    


pygame.quit()
