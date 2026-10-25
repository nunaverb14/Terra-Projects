# File for games sprites including projectile, player, enemy, and boss
from images import *
import images
import pygame
import random

# Class for player sprite
class Player(pygame.sprite.Sprite):

    # Initializes player with image and speed
    def __init__(self, image, speed = 5):
        pygame.sprite.Sprite.__init__(self)

        # Player image
        self.image = image
        self.rect = self.image.get_rect()

        # Player attributes
        self.speed = speed
        self.health = 100
        self.lives = 3
        self.status_color = "green"

        # Player Shooting vars
        self.last_shot = 0

    # Shoots projectile from player position
    def shoot(self):
        shot = Projectile(create_image(images._player_shot).convert_alpha(), 0, 0, -5)
        shot.add(Projectile.player_shots)
        shot.rect.centerx = self.rect.centerx + shot.rect.w / 2
        shot.rect.centery = self.rect.centery
        
    # Updates player position and shooting
    def update(self):
        # Player movement using WASD, Arrows, and NumPad
        if pygame.key.get_pressed()[pygame.K_w] + pygame.key.get_pressed()[pygame.K_UP] + pygame.key.get_pressed()[pygame.K_KP_8]:
            self.rect.y -= self.speed
        if pygame.key.get_pressed()[pygame.K_a] + pygame.key.get_pressed()[pygame.K_LEFT] + pygame.key.get_pressed()[pygame.K_KP_4]:
            self.rect.x -= self.speed
        if pygame.key.get_pressed()[pygame.K_s] + pygame.key.get_pressed()[pygame.K_DOWN] + pygame.key.get_pressed()[pygame.K_KP_2]:
            self.rect.y += self.speed
        if pygame.key.get_pressed()[pygame.K_d] + pygame.key.get_pressed()[pygame.K_RIGHT] + pygame.key.get_pressed()[pygame.K_KP_6]:
            self.rect.x += self.speed
        
        self.rect.clamp_ip(pygame.display.get_surface().get_rect().move(-self.rect.w / 2, -self.rect.h / 2))
        
        # Player shooting using Space, Enter, and NumPad
        if pygame.key.get_pressed()[pygame.K_SPACE] + pygame.key.get_pressed()[pygame.K_RETURN] + pygame.key.get_pressed()[pygame.K_KP_ENTER]:
            now = pygame.time.get_ticks()
            if (now - self.last_shot) >= 500:
                self.last_shot = now
                self.shoot()

        # Update player health bar        
        self.status_color = "green" if self.health >= 75 else "yellow" if self.health >= 25 else "red"


# Class for enemy sprite
class Enemy(pygame.sprite.Sprite):

    # Enemy Group
    enemies = pygame.sprite.Group()
    leds = pygame.sprite.Group()
    piezos = pygame.sprite.Group()

    # Initializes enemy with image, speed, and shooting interval
    def __init__(self, image, part, color):
        pygame.sprite.Sprite.__init__(self)
        self.add(Enemy.enemies)

        ###############
        if part == 1:
            self.add(Enemy.leds)
        elif part == 2:
            self.add(Enemy.piezos)

        # Enemy attributes
        self.image = pygame.transform.rotate(image, 180)
        self.color = color
        palette = list(self.image.get_palette())
        palette[11] = self.color
        self.image.set_palette(palette)
        self.rect = self.image.get_rect()
        self.health = 5

        # Enemy shooting vars
        self.last_shot = pygame.time.get_ticks()


    ##############
    def shoot(self):

        shot = Projectile(pygame.Surface((48, 48)), 1, 0, 3)

        if shot in Projectile.led_shots:
            shot.image = create_image(images._led_shot)
        elif shot in Projectile.piezo_shots:
            shot.image = create_image(images._piezo_shot)

        palette = list(shot.image.get_palette())
        palette[11] = self.color
        shot.image.set_palette(palette)

        shot.rect.centerx = self.rect.centerx + shot.rect.w / 2
        shot.rect.centery = self.rect.centery

    # Enemy shooting at a random interval bet
    def update(self):
        now = pygame.time.get_ticks()
        if (now - self.last_shot) >= random.randint(1000, 10000):
            if not random.randint(-20, 20):
                self.last_shot = now
                self.shoot()


# Class for projectile sprite
class Projectile(pygame.sprite.Sprite):

    # Projectile Groups
    shots = pygame.sprite.Group()
    led_shots = pygame.sprite.Group()
    piezo_shots = pygame.sprite.Group()
    player_shots = pygame.sprite.Group()

    # Initializes projectile with image, group, and speed
    def __init__(self, image, group, x_speed, y_speed):
        pygame.sprite.Sprite.__init__(self)
        self.add(Projectile.shots)
        if group == 1:
            Projectile.led_shots.add(self)
        elif group == 2:
            Projectile.piezo_shots.add(self)
        
        # Projectile attributes
        self.image = image
        self.rect = self.image.get_rect()
        self.x_speed = x_speed
        self.y_speed = y_speed

    # Updates projectile position and status
    def update(self):
        # Moves projectile by x and y speed
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Removes the projectile from all groups when offscreen
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()