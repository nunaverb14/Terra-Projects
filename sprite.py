import pygame

class Player(pygame.sprite.Sprite):
    players = pygame.sprite.Group()
    num = 0

    def __init__(self, pos:int, controls:list):
        pygame.sprite.Sprite.__init__(self)
        self.add(self.players)

        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.image.fill("black")
        self.rect = self.image.get_rect(topleft=pos)

        self.images = None

        self.num = Player.num
        Player.num += 1

        self.health = 100
        self.controls = controls
        self.direction = -2 * (self.num % 2) - 1
        print(self.direction)

        self.type = -1

        self._attackable = True

        self.jump_timer = 0
        self.attack_timer = 0
        self.shoot_timer = 0
        # self.last_block_time = 0
    
    def set(self, char, images):
        self.images = images
        self.type = char

    def jump(self):
        self.action = 1
        self.image = self.images[0]

    def block(self):
        self.action = 2
        self.attackable = False
        self.image = self.images[1]

    def attack(self):
        self.action = 3
        self.image = self.images[2]

    def shoot(self):
        self.action = 4
        self.image = self.images[4]
        Projectile()


    def update(self, dt):
        if pygame.key.get_pressed(self.controls[0]):
            self.jump()
        if pygame.key.get_pressed(self.controls[1]):
            self.block()
        if pygame.key.get_pressed(self.controls[2]):
            self.rect.centerx -= 5
            self.image = pygame.transform.flip(self.images[1], True, False)
            self.direction = -1
        if pygame.key.get_pressed(self.controls[3]):
            self.rect.centerx += 5
        if pygame.key.get_pressed(self.controls[4]):
            self.attack()
        if pygame.key.get_pressed(self.controls[5]):
            self.shoot()

        now = pygame.time.get_ticks()

        # jump
        if self.action == 1 and now - self.jump_timer >= 1000:
            self.jump_timer = now
            self.action = 0
            pass

        # block
        if self.action == 2:
            self.action = 0
            pass
        # attack
        elif self.action == 3 and now - self.attack_timer >= 350:
            self.attack_timer = now
            self.action = 0
            pass
        # shoot
        elif self.action == 4 and now - self.shoot_timer >= 500:
            self.shoot_timer = now
            Projectile()
            self.action = 0
            pass



class Projectile:
    def __init__(self):
        pass
