from projectile import *
import projectile
import pygame



# Pygame init
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

# Load Text
font_lc32 = pygame.font.SysFont("lucidaconsole", 32)
font_lc24 = pygame.font.SysFont("lucidaconsole", 24)

# Game Setup
box = pygame.Rect(50, 50, 500, 500)
turn = 0
level = 1
game = 1

# Shooting Setup
shot_speed = 1
last_shot = 0
total_shots = 1
shots = total_shots
bullets = 1
bouncers = 0
mines = 0

# Cannon Setup
cannon = pygame.image.load(resource_path("images/Cannon.png"))
cannon.set_colorkey((255, 255, 255))
cannon_rect = cannon.get_rect(center=box.topleft)

cannon_speed = 2
cannon_pointer = list(box.center)
pointer_speed = 10

# Player Setup
player = pygame.image.load(resource_path("images/Player.png"))
player.set_colorkey((255, 255, 255))
player_rect = player.get_rect(center=box.center)
lives = 7

# Game Initialization
running = True
while running:
    if game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        # Draw Background
        screen.fill("black")
        box.center = (screen.width / 2, screen.height / 2)
        pygame.draw.rect(screen, "purple", box)

        # Player Screen
        if turn:
            # Player Controls
            if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_KP_8]:
                player_rect.centery -= 5
            if pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_KP_2]:
                player_rect.centery += 5
            if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_KP_4]:
                player_rect.centerx -= 5
            if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_KP_6]:
                player_rect.centerx += 5

            player_rect.clamp_ip(box)

            # Projectile Shot Delay
            now = pygame.time.get_ticks()
            if now - switch_time >= 3000:
                Projectile.shots.update(box)
                # Collison Detection
                for shot in Projectile.shots:
                    if player_rect.colliderect(shot.rect):
                        shot.kill()
                        lives -= 1
                # Game Over
                if lives <= 0:
                    game = 0

            # Game Reset
            if len(Projectile.shots) == len(Projectile.mines) or len(Projectile.shots) == 0:
                level += 1
                total_shots = level
                shots = total_shots
                bullets = total_shots
                # Level 10 Difficulty Increase
                if level > 10:
                    # Add mines
                    bullets = total_shots * 0.8 // 1
                    mines = total_shots - bullets
                    shot_speed = 2
                # Level 15 Difficulty Increase
                if level > 15:
                    cannon_speed = 5
                    pointer_speed = 15
                    # Shrink Box
                    if box.w > 300:
                        box.w -= 10
                    if box.h > 300:
                        box.h -= 10
                # Level 20 Difficulty Increase
                if level > 20:
                    # Add Bouncing Bullets
                    bullets = total_shots * 0.7 // 1
                    mines = total_shots * 0.2 // 1
                    bouncers = total_shots - bullets - mines
                    shot_speed = 3
                    pointer_speed = 20
                
                turn = 0
                cannon_rect.center = box.topleft
                player_rect.center = box.center

                pygame.time.delay(250)

            # Draw Player Screen
            text = font_lc32.render(f"Level {level}    Lives: {lives}", True, "pink")
            screen.blit(text, text.get_rect(midtop= (box.centerx, box.top / 2 - text.height / 2)))
            screen.blit(player, player_rect.topleft)

            # Draw Countdown
            if now - switch_time < 3000:
                text = font_lc32.render(f"{3 - (now - switch_time) / 1000:.1f}", False, "white")
                screen.blit(text, text.get_rect(center= box.center))

        # Shooting Screen
        else:
            # Cannon Rotation
            cannonVec = pygame.Vector2(cannon_rect.center)
            pointVec = pygame.Vector2(cannon_pointer)
            direction = pointVec - cannonVec
            angle = pygame.Vector2(0, -1).angle_to(direction)
            rotated = pygame.transform.rotate(cannon, -angle)
            rotated_rect = rotated.get_rect()

            # Cannon Movement
            if cannon_rect.centerx <= box.left:
                cannon_rect.move_ip(0, cannon_speed)
                cannon_rect.centerx = box.left

            if cannon_rect.centery >= box.bottom:
                cannon_rect.move_ip(cannon_speed, 0)
                cannon_rect.centery = box.bottom

            if cannon_rect.centerx >= box.right:
                cannon_rect.move_ip(0, -cannon_speed)
                cannon_rect.centerx = box.right

            if cannon_rect.centery <= box.top:
                cannon_rect.move_ip(-cannon_speed, 0)
                cannon_rect.centery = box.top

            # Cannon Pointer Movement
            if cannon_rect.centerx == box.left or cannon_rect.centerx == box.right:
                cannon_pointer[0] = box.centerx
                cannon_pointer[1] += pointer_speed
                if cannon_pointer[1] <= box.top or cannon_pointer[1] >= box.bottom:
                    pointer_speed *= -1

            if cannon_rect.centery == box.top or cannon_rect.centery == box.bottom:
                cannon_pointer[1] = box.centery
                cannon_pointer[0] += pointer_speed
                if cannon_pointer[0] <= box.left or cannon_pointer[0] >= box.right:
                    pointer_speed *= -1

            now = pygame.time.get_ticks()

            # Mine Placing Preview
            mouse_pos = pygame.mouse.get_pos()
            if bullets + bouncers == 0:
                pygame.draw.circle(screen, "black", mouse_pos, 16, 6)

            # Cannon Shooting
            if pygame.mouse.get_pressed()[0] and now - last_shot >= 500:
                last_shot = now

                # Regular Bullet Shooting
                if bullets > 0:
                    bullets -= 1 
                    shot = Projectile(1, cannon_rect.center, cannon_pointer, shot_speed)
                    shot.rect.center = cannon_rect.center
                # Bouncing Bullet Shooting
                elif bouncers > 0:
                    bouncers -= 1
                    shot = Projectile(2, cannon_rect.center, cannon_pointer, shot_speed)
                    shot.rect.center = cannon_rect.center
                # Mine Placing
                elif mines > 0: 
                    mines -= 1
                    shot = Projectile(0, mouse_pos, mouse_pos, 0)
                    shot.rect.center = mouse_pos

                    # Mine Placement Proxmity Detection
                    if len(pygame.sprite.spritecollide(shot, Projectile.mines, False, pygame.sprite.collide_circle_ratio(1.25))) > 1:
                        shot.kill()
                        mines += 1
                        shots += 1
                shots -= 1

            # PLayer Screen Activation
            if shots == 0:
                switch_time = pygame.time.get_ticks()
                turn = 1

            # Draw Shooting Screen
            text = font_lc24.render(f"Bullets: {bullets:.0f} | Bouncing: {bouncers:.0f} | Mines: {mines:.0f}", True, "red")
            screen.blit(text, text.get_rect(midtop= (box.centerx, box.top / 2 - text.height / 2)))
            screen.blit(rotated, cannon_rect.topleft)

        Projectile.shots.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    else:
        # Game Over Screen Overlay
        overlay = pygame.Surface(screen.size, pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 128))
        screen.blit(overlay)

        # Game Over Text
        text = font_lc32.render("Game Over", True, "white")
        screen.blit(text, text.get_rect(center=(screen.width / 2, screen.height / 2 - text.height * 1.5)))

        text = font_lc32.render("Press 'r' to restart", True, "white")
        screen.blit(text, text.get_rect(center=(screen.width / 2, screen.height / 2)))

        text = font_lc32.render("Press 'q' to quit", True, "white")
        screen.blit(text, text.get_rect(center=(screen.width / 2, screen.height / 2 + text.height * 1.5)))

        pygame.display.flip()
        quit = 0

        # Game Over Loop
        while not quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    quit = 1

            if pygame.key.get_pressed()[pygame.K_r]:
                # Game Restart
                box = pygame.Rect(50, 50, 500, 500)
                turn = 0
                level = 1
                game = 1

                lives = 7
                Projectile.shots.empty()

                # Shooting Restart
                shot_speed = 1
                last_shot = 0
                total_shots = 1
                shots = total_shots
                bullets = 1
                bouncers = 0
                mines = 0

                quit = 1

            if pygame.key.get_pressed()[pygame.K_q]:
                quit = 1
                running = False


pygame.quit()