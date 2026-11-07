import pygame

###
class Fruit(pygame.sprite.Sprite):
    ###
    fruits = pygame.sprite.Group()
    stats = {
        "color": ("red", "orange", "yellow", "darkgreen"),
        "price": (5, 7, 10, 15),
    }

    def load_images(images: list):
        Fruit.stats.update("images", images)

    ###
    def __init__(self, fruit: int, pos: list[int] | tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.add(Fruit.fruits)
        self.type = fruit

        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft)
        self.image.fill(Fruit.stats.get("color")[self.type])

    def update(self, dt):
        self.rect.centery -= 2 * dt



###
class Player(pygame.sprite.Sprite):

    ###
    def __init__(self, image: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.image.fill("gold")

        self.speed = 2

        self.fruit_cap = 1
        self.fruit_num = 0




    def update(self, dt: int | float):
        ###
        if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_KP_4]:
            self.rect.centerx -= self.speed
        if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_KP_6]:
            self.rect.centerx += self.speed

