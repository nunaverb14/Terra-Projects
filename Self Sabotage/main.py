import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

box = pygame.Rect(100, 100, 400, 400)
turn = 0

cannon = pygame.Surface((32, 32), pygame.SRCALPHA)
cannon_rect = cannon.get_rect(center=(200,200))
cannon.fill("red")

player = pygame.Surface((32, 32), pygame.SRCALPHA)
player_rect = player.get_rect(center=(300,300))
player.fill("green")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("purple")
    pygame.draw.rect(screen, "blue", box)

    if turn:
        if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP]:
            player_rect.centery -= 5
        if pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]:
            player_rect.centery += 5
        if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
            player_rect.centerx -= 5
        if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
            player_rect.centerx += 5

        player_rect.clamp_ip(box)

        screen.blit(player, player_rect.topleft)
    else:
        pygame.transform.rotate(cannon, )
        screen.blit(cannon, cannon_rect.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()