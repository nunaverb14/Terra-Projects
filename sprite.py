import pygame

class Player(pygame.sprite.Sprite):
    players = pygame.sprite.Group()
    num = 0

    def __init__(self, pos:int, controls:list):
        pygame.sprite.Sprite.__init__(self)
        self.add(self.players)

        self.image = pygame.Surface((24*3, 32*3), pygame.SRCALPHA)
        self.image.fill("black")
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)

        self.images = None

        self.num = Player.num
        Player.num += 1

        self.health = 100
        self.controls = controls
        self.controls = list(pygame.key.key_code(key) for key in controls)
        self.direction = -(2 * (self.num % 2) - 1)

        self.type = -1
        self.action = 0

        self._attackable = True

        self.jump_timer = 0
        self.attack_timer = 0
        self.shoot_timer = 0

        self.jump_anim_timer = 0
        self.attack_anim_timer = 0
        self.shoot_anim_timer = 0
        # self.last_block_time = 0
    
    def set(self, char, images: list | tuple):
        for i in range(len(images)):
            images[i] = pygame.transform.smoothscale_by(images[i], 3)

        self.images = images
        self.type = char

    def jump(self):
        if not self.action:
            self.action = 1
            self.image = self.images[1]
            self._y = self.rect.top
            self._vy = -self.rect.height / 2

    def block(self):
        if not self.action:
            self.action = 2
            self._attackable = False
            self.image = self.images[2]

    def attack(self):
        if not self.action:
            self.action = 3
            self.image = self.images[3]

    def shoot(self):
        if not self.action:
            self.action = 4
            self.image = self.images[4]
            Projectile()


    def update(self, dt):
        now = pygame.time.get_ticks()

        # W: 0
        if pygame.key.get_pressed()[self.controls[0]] and now - self.jump_timer >= 50:
            self.jump_timer = now
            self.jump()
        # S: 2
        if pygame.key.get_pressed()[self.controls[2]]:
            self.block()
        # A: 1
        if pygame.key.get_pressed()[self.controls[1]]:
            self.rect.centerx += -10
            self.image = pygame.transform.flip(self.images[0], True, False)
            self.direction = -1
        # D: 3
        if pygame.key.get_pressed()[self.controls[3]]:
            self.rect.centerx += 10
            self.image = self.images[0]
        # Q: 4
        if pygame.key.get_pressed()[self.controls[4]]:
            self.attack()
        # E: 5
        if pygame.key.get_pressed()[self.controls[5]]:
            self.shoot()


        # jump
        if self.action == 1 and now - self.jump_anim_timer >= 20:
            self.jump_anim_timer = now

            self._vy += 5
            self.rect.y += self._vy                
        
            if self.rect.y >= self._y:
                self.rect.y = self._y
                self.velocity_y = 0
                self.action = 0

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
