import pygame
import random
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

###
class Fruit(pygame.sprite.Sprite):
    ###
    fruits = pygame.sprite.Group()
    stats = {
        "color": ("red", "orange", "yellow", "darkgreen", "black"),
        "name": ("apple", "orange", "fruit", "fruit", "fruit"),
        "speed": [2, 0, 0, 0, 0],
        "price": [2, 5, 13, 19, 25],
        "golden": [0, 0, 0, 0, 0],
    }

    ###
    def load_images(images: list[str]):
        for image in images:
            image = pygame.image.load(resource_path(image))
        Fruit.stats.update("images", images)

    ###
    def __init__(self, fruit: int, pos: list[int] | tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.add(Fruit.fruits)
        self.type = fruit

        self.speed = self.stats.get("speed")[self.type]
        self.price = self.stats.get("price")[self.type]
        self.golden = True if random.random() <= Fruit.stats.get("golden")[self.type] else False


        self.image = self.stats.get("images")[self.type] if Fruit.stats.get("images", False) else pygame.Surface((24, 24), pygame.SRCALPHA) 
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill(Fruit.stats.get("color")[self.type]) if not Fruit.stats.get("images", False) else 0
        pygame.draw.rect(self.image, "gold", (0, 0, self.rect.width, self.rect.height), 4) if self.golden else 0


    ###
    def update(self, dt):
        self.rect.centery += self.speed

###
class Player(pygame.sprite.Sprite):

    ###
    def __init__(self, image: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 5

    ###
    def update(self, dt: int | float):
        ###
        if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_KP_4]:
            self.rect.centerx -= self.speed
        if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_KP_6]:
            self.rect.centerx += self.speed