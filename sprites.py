import pygame

# Tile Sprite Class
class Tile(pygame.sprite.Sprite):
    # Tile Groups
    tiles = pygame.sprite.Group()
    grass_tiles = pygame.sprite.Group()
    water_tiles = pygame.sprite.Group()

    def __init__(self, tile):
        pygame.sprite.Sprite.__init__(self)
        self.add(Tile.tiles)

        # Tile Sprite Properties
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.type = tile

        color = 0
        outline = 0
        # Grass Tile Setup
        if self.type == 0:
            self.add(Tile.grass_tiles)
            color = "#00C000"
            outline = "#00ff00"
        # Water Tile Setup
        elif self.type == 1:
            self.add(Tile.water_tiles)
            color = "#0000C0"
            outline = "#0000ff"
        
        self.image.fill(color)
        pygame.draw.rect(self.image, outline, self.rect, 5)





    def update(self):
        pass