import pygame
import os
import sys

def resource_path(relative_path: str):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Player(pygame.sprite.Sprite):
    players = pygame.sprite.Group()
    num = 0
    images = []

    def set_images(screen, images: tuple[str, ...]):
        for image in images:
            sheet = pygame.image.load(resource_path("images/" + image)).convert_alpha()
            sprites = []
            for i in range(6):
                image = sheet.subsurface((24 * (i % 3), 32 * (i // 3)), (24, 32))
                image = pygame.transform.smoothscale_by(image, 4)
                sprites.append(image)
            
            Player.images.append(sprites)
    
    def __init__(self, pos:int, controls:list):
        pygame.sprite.Sprite.__init__(self)
        self.add(self.players)

        self.image = pygame.Surface((24*4, 32*4), pygame.SRCALPHA)
        self.image.fill("black")
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)

        self.images = []
        self._image = None

        self.num = Player.num
        Player.num += 1

        self.health = 100
        self.controls = controls
        self.controls = list(pygame.key.key_code(key) for key in controls)
        self.direction = -(2 * (self.num % 2) - 1)

        self.type = -1
        self.action = 0

        self.attackable = True
        self.vy = 0
        self.on_ground = True

        self.image_timer = 0
        self.jump_timer = 0
        self.block_timer = 0
        self.attack_timer = 0
        self.shoot_timer = 0

        self.jump_anim_timer = 0
        self.attack_anim_timer = 0
        self.shoot_anim_timer = 0

    
    def set(self, char):
        self.images = Player.images[char]
        self.type = char
        self._image = self.images[3]

    def jump(self):
        if not self.action:
            self.action = 1
            self.vy = -self.rect.height / 5
            self._image = self.images[0]
            
    def block(self):
        if not self.action:
            self.action = 2
            self.attackable = False
            self._image = self.images[4]

    def attack(self):
        if not self.action:
            self.action = 3
            hit = pygame.sprite.spritecollide(self, Player.players, False)
            for player in hit:
                if player != self:
                    if player.action != 2:
                        player.health -= 5
            self._image = self.images[2]

    def shoot(self):
        if self.action <= 1:
            Projectile(self.type, self.rect.midright if self.direction == 1 else self.rect.midleft, self.direction, self.num)
            self._image = self.images[1]


    def update(self, dt):
        now = pygame.time.get_ticks()

        if not self.action:
         if now - self.image_timer >= 1000:
            self.image_timer = now
            self._image = self.images[3]

        # W: 0
        if pygame.key.get_pressed()[self.controls[0]] and self.on_ground:
            self.jump()
        # S: 2
        if pygame.key.get_pressed()[self.controls[2]]:
            self.block()
        # A: 1
        if pygame.key.get_pressed()[self.controls[1]]:
            self.rect.centerx += -10
            self.image = self.images[3]
            self.direction = -1
        # D: 3
        if pygame.key.get_pressed()[self.controls[3]]:
            self.rect.centerx += 10
            self.image = self.images[3]
            self.direction = 1
        # Q: 4
        if pygame.key.get_just_pressed()[self.controls[4]]:
            self.attack()
        # E: 5
        if pygame.key.get_pressed()[self.controls[5]] and now - self.shoot_timer >= 750:
            self.shoot_timer = now
            self.shoot()

        self.on_ground = False
        self.vy += 1.375
        self.rect.y += self.vy

        for platform in pygame.sprite.spritecollide(self, Platform.platforms, False):
            if self.vy > 0:
                self.rect.bottom = platform.rect.top
                self.vy = 0
                self.on_ground = True

        # jump
        if self.action == 1 and now - self.jump_anim_timer >= 50:
            self.jump_anim_timer = now
            self.on_ground = False

            self.vy += 1.375
            self.rect.y += self.vy

            for platform in pygame.sprite.spritecollide(self, Platform.platforms, False):
                if self.vy > 0:
                    self.rect.bottom = platform.rect.top
                    self.vy = 0
                    self.on_ground = True

            if self.on_ground:
                self.action = 0

        # block
        if self.action == 2:
            if now - self.block_timer >= 1000:
                self.block_timer = now
                self.action = 0
        # attack
        elif self.action == 3:
            if now - self.attack_timer >= 350:
                self.attack_timer = now
                self.action = 0
            pass

        self.image = self._image if self.direction == 1 else pygame.transform.flip(self._image, True, False)

class Projectile(pygame.sprite.Sprite):
    shots = pygame.sprite.Group()
    images = None

    @staticmethod
    def set_images(images):
        pass

    def __init__(self, char:int, pos:tuple[int, int], dir:int, parent:int):
        pygame.sprite.Sprite.__init__(self)
        self.add(Projectile.shots)

        self._image = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.image = self._image
        self.rect = self.image.get_rect(center=pos)
        pygame.draw.circle(self._image, "pink", self.image.get_rect().center, 7)

        self.type = char
        self.parent = parent

        self.pos = pos
        self.dir = dir
        self.rot = 0

    def update(self, dt):
        self.rect.x += 5 * self.dir
        self.rot += 5
        self.image = pygame.transform.rotate(pygame.transform.smoothscale_by(self._image, 1 + abs((self.rot % 360 + 1) - 180) / 180), self.rot)
        self.rect.y = self.pos[1] - self.image.get_rect().height / 2

class Platform(pygame.sprite.Sprite):
    platforms = pygame.sprite.Group()

    def __init__(self, image: pygame.Surface | None, rect: pygame.Rect):
        pygame.sprite.Sprite.__init__(self)
        self.add(Platform.platforms)

        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface((self.rect.size))
        self.image.fill("pink")

    def update(self, dt):
        pass
