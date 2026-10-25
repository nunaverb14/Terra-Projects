import pygame
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Projectile Sprite Class
class Projectile(pygame.sprite.Sprite):
    # Projectile Groups
    shots = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    bouncers = pygame.sprite.Group()
    mines = pygame.sprite.Group()

    # Projectile Creation 
    def __init__(self, shot, position, target, speed):
        pygame.sprite.Sprite.__init__(self)
        self.add(Projectile.shots)


        # Type Classification
        self.type = shot
        self.bounce = 0
        if self.type == 0:
            self.image = pygame.image.load(resource_path("images/Mine.png"))
            self.add(Projectile.mines)
        elif self.type == 1:
            self.image = pygame.image.load(resource_path("images/Bullet.png"))
            self.add(Projectile.bullets)
        elif self.type == 2:
            self.image = pygame.image.load(resource_path("images/Bouncing.png"))
            self.add(Projectile.bouncers)
            self.bounce = 1

        # Projectile Image
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = position

        

        # Movement Planning
        self.target = target
        self.speed = speed
        self.direction = pygame.Vector2(self.target) - pygame.Vector2(self.rect.center)
        self.direction = self.direction.normalize() if self.direction.length_squared() > 0 else pygame.Vector2()


    # Update Projectile Movement
    def update(self, box):
        # Mine Clearing
        if self.type == 0:
            if len(Projectile.shots) == len(Projectile.mines):
                self.kill()
        # Bullet Movement
        else:
            self.rect.centerx += self.direction.x * 10
            self.rect.centery += self.direction.y * 10

            # Projectile Autokill
            if not self.rect.colliderect(box):
                # Bounce Projectiles
                if self.bounce:
                    self.bounce -= 1
                    if self.rect.left < box.left or self.rect.right > box.right:
                        self.direction.x *= -1
                    if self.rect.top < box.top or self.rect.bottom > box.bottom:
                        self.direction.y *= -1
                else:
                    self.kill()

        


