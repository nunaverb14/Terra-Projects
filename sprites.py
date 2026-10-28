import pygame

# Tile Sprite Class
class Tile(pygame.sprite.Sprite):
    # Tile Groups
    tiles = pygame.sprite.Group()
    grass_tiles = pygame.sprite.Group()
    water_tiles = pygame.sprite.Group()

    def __init__(self, tile, pos):
        pygame.sprite.Sprite.__init__(self)
        self.add(Tile.tiles)

        # Tile Sprite Properties
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.type = tile
        
        stats = {
            "group":    [Tile.grass_tiles,  Tile.water_tiles],
            "color":    ["#008000",     "#000080"],
            "outline":  ["#00ff00",     "#0000ff"],
            "health":   [0,                 1]
        }

        self.add(stats["group"][self.type])
        self.image.fill(stats["color"][self.type])
        pygame.draw.rect(self.image, stats["outline"][self.type], self.image.get_rect(), 2)


    def update(self):
        pass






# Tower Sprite Class
class Tower(pygame.sprite.Sprite):
    # Tower Groups
    towers = pygame.sprite.Group()

    def __init__(self, tower):
        pygame.sprite.Sprite.__init__(self)
        self.add(Tower.towers)

        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.type = tower

        stats = {
            "color":    ["#2e2020", "#2e2e20",      "#20202e"],
            "attack":   [1,             3,              5],
            "speed":    [250,           300,            500],
            "health":   [3,             5,              10]
        }

        self.image.fill(stats["color"][self.type])
        self.attack = stats["attack"][self.type]
        self.speed = stats["speed"][self.type]
        self.health = stats["health"][self.type]


    def update(self):
        pass
