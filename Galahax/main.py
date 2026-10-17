from background import Star
from sprites import *
from images import *
import sprites
import images
import background
import pygame

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((768, 768))
clock = pygame.time.Clock()
    # print(pygame.font.get_fonts())
cambriamath = pygame.font.SysFont("cambriamath", 24, True)

# Game vars initialization
score = 0
level = 0
game_over = False

# Player Creation
player_image = create_image(images._player)
player = Player(player_image.convert_alpha())
player.rect.center = (384, 384)

# Debug
# #######################################
# # Random Led & Led Shot
# led_image = create_image(images._led)
# enemy = Enemy(led_image, 1, retro_palette[5])
# enemy.rect.center = (100, 100)

# led_shot_image = create_image(images._led_shot)
# enemy_shot = Projectile(led_shot_image, 0, 0, 0)
# enemy_shot.rect.center = (150, 100)

# # Full Palette
# palette_image = pygame.transform.scale_by(create_image(images._test), 2)
# palette_ = Projectile(palette_image, 0, 0, 0)
# palette_.rect.center = (500, 500)

# # Color Sprite Change
# '''
# palette = list(player_image.get_palette())
# palette[6] = retro_palette[4]
# player_image.set_palette(palette)
# player.image = player_image.convert_alpha()
# '''
# #######################################

# Start Game
running = True
while running:
    # Check for screen close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Variable Testing
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_i]:
                pass
    
    ##############
    if not game_over:
        # Setup background
        screen.fill((48, 48, 48))
        Star.star_effect(100, "green")

        # Draw player stats
        pygame.draw.rect(screen, player.status_color, (0, 0, player.health * 2, 25))
        player_bar = pygame.draw.rect(screen, "white", (0, 0, 200, 25), 2, 2)
        player_stat = cambriamath.render(str(player.health), True, "grey")
        screen.blit(player_stat, (player_bar.centerx - player_stat.width / 2, player_bar.centery - player_stat.height / 2))

        # Draw score
            # pygame.draw.rect(screen, player.status_color, (0, 0, player.health, 25))
        player_bar = pygame.draw.rect(screen, "white", (0, 25, 200, 25), 2, 2)
        player_stat = cambriamath.render(f"Score: {score}", True, "grey")
        screen.blit(player_stat, (player_bar.centerx - player_stat.width / 2, player_bar.centery - player_stat.height / 2))

        # Enemy Summoning
        if len(Enemy.enemies) == 0:
            pygame.time.wait(50)
            level += 1
            led_total = level
            for i in range(led_total):  
                led_image = create_image(images._led)
                led = Enemy(led_image, 1, retro_palette[5])
                led.rect.center = (700 / (10) * (i % 10) + 50, 100 + int(i / 10) * 50)

        # Enemy Collision Detection and Score
        for enemy in Enemy.enemies:
            hit_list = pygame.sprite.spritecollide(enemy, Projectile.player_shots, True, pygame.sprite.collide_rect_ratio(3/4))
            for shot in hit_list:
                enemy.kill()
                score += 1

        # Player Coliision Detection and Health
        hit_list = pygame.sprite.spritecollide(player, Projectile.led_shots, True, pygame.sprite.collide_rect_ratio(3/4))
        for shot in hit_list:
            player.health -= 2
            if player.health <= 0:
                game_over = True

        # Update sprites
        player.update()
        Enemy.enemies.update()
        Projectile.shots.update()

        # Draw sprites to screen
        Projectile.shots.draw(screen)
        Enemy.enemies.draw(screen)
        screen.blit(player.image, player.rect.center)

        # Update display and timer
        pygame.display.flip()
        clock.tick(min(240, 30 * (int(level / 5) + 2)))

    else:
        # Create Game Over Message
        fade = pygame.Surface((screen.width, screen.height), pygame.SRCALPHA)
        fade.fill((255, 255, 255, 128))
        screen.blit(fade, fade.get_rect().topleft)
        exit = False

        ############
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    exit = True
                ###########
                if event.type == pygame.KEYDOWN:
                    #############
                    if pygame.key.get_pressed()[pygame.K_q]:
                        running = False
                        exit = True
                    
                    #############
                    if pygame.key.get_pressed()[pygame.K_r]:
                        game_over = False
                        score = 0
                        level = 0
                        Enemy.enemies.empty()
                        Projectile.shots.empty()
                        player.health = 100

                        exit = True
            
            ###############
            game_text = pygame.transform.scale_by(cambriamath.render("Game Over\n\nPress 'r' to restart or 'q' to quit", False, "green"), 1.5)
            screen.blit(game_text, (screen.width / 2 - game_text.width / 2, screen.height / 2 - game_text.height / 2))

            pygame.display.flip()
            clock.tick(120)


pygame.quit()


