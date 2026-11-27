import pygame

class Tile(pygame.sprite.Sprite):
    # Tile Group
    tiles = pygame.sprite.Group()
    selected_tile = None

    # Tile Selection Method
    @staticmethod
    def select(tile, selected_mode):
        # Select New Tile
        if not Tile.selected_tile:
            Tile.selected_tile = tile
        else:
            if selected_mode < 2 and tile.placed:
                return
            else:
                # Switch Selected Tiles
                topleft = Tile.selected_tile.current_pos
                Tile.selected_tile.set_pos(tile.rect.topleft)
                tile.set_pos(topleft)
                Tile.selected_tile = None

    # Tile Deselect Method
    @staticmethod
    def deselect():
        Tile.selected_tile = None    

    # Intialize Tile with Image and Position
    def __init__(self, image: pygame.Surface, pos):
        pygame.sprite.Sprite.__init__(self)
        Tile.tiles.add(self)
        # Image Vars
        self.image: pygame.Surface = image.copy()
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)
        # Postition Vars
        self.original_pos = pos
        self.current_pos = pos
        self.placed = False

    # Change Tile Postion
    def set_pos(self, pos):
        self.current_pos = pos
        self.rect.topleft = self.current_pos

    # Update Tile for Correct Placement
    def update(self):
        if self.current_pos == self.original_pos and not self.placed:
            self.placed = True