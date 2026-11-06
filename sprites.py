import pygame

###
class Fruit(pygame.sprite.Sprite):
    ###
    fruits = pygame.sprite.Group()
    stats = {
        "color": ("red", "orange", "yellow", "darkgreen")
    }

    def load_images(images: list):
        Fruit.stats.update("images", images)

    ###
    def __init__(self, fruit: int):
        pygame.sprite.Sprite.__init__(self)
        self.add(Fruit.fruits)
        self.type = fruit

        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.image.fill(Fruit.stats.get("color")[self.type])

    def update(self, dt):
        pass