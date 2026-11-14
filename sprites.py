import pygame

class Tile(pygame.sprite.Sprite):
    # Tile Group
    tiles = pygame.sprite.Group()

    def __init__(self, image: pygame.Surface, pos):
        pygame.sprite.Sprite.__init__(self)
        Tile.tiles.add(self)

        self.image: pygame.Surface = image.copy()
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)

        self.origanl_pos = pos
        self.current_pos = pos

    def set_pos(self, pos):
        self.current_pos = pos
        self.rect.topleft = self.current_pos

    def update(self):
        pass

    


