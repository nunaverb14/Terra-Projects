# File the holds image data for each sprite
# I didn't feel like using a pixel art editor and exporting every image so i took the hard way
import pygame

# Global Palette for all Sprites
retro_palette = [
    [1, 1, 1],          # 0: Transparent
    [255, 0, 0],        # 1: Red
    [255, 160, 0],      # 2: Orange
    [255, 255, 0],      # 3: Yellow
    [0, 255, 0],        # 4: Lime
    [0, 160, 0],        # 5: Green
    [0, 255, 255],      # 6: Cyan
    [0, 0, 255],        # 7: Blue
    [128, 128, 128],    # 8: Gray
    [255, 255, 255],    # 9: White
    [0, 0, 0]           # 10: Black
                        # 11: Data Color
]

# Sprite Image Data Decoder 
def create_image(image_data, pixel_size = 6):
    width = len(image_data[0])
    height = len(image_data)
    surface = pygame.Surface((width, height), depth=8)

    surface.set_palette(retro_palette + [[0, 0, 0]] * (256 - len(retro_palette)))

    for y, row in enumerate(image_data):
        for x, color_index in enumerate(row):
            surface.set_at((x, y), color_index)

    surface.set_colorkey((1, 1, 1), pygame.SRCALPHA)
    return pygame.transform.scale(surface, (width * pixel_size, height * pixel_size))

    # pygame.image.save_extended(surface, file_name)



# Full Palette Image Data
_test = [
    [1, 1, 1, 2, 2, 3, 3, 3],
    [1, 1, 1, 2, 2, 3, 3, 3],
    [4, 4, 10, 2, 2, 10, 5, 5],
    [4, 4, 10, 10, 10, 10, 5, 5],
    [4, 4, 6, 6, 6, 6, 5, 5],
    [7, 7, 6, 0, 0, 6, 9, 9],
    [7, 7, 8, 0, 0, 8, 9, 9],
    [7, 7, 8, 8, 8, 8, 9, 9]
]

# Player Image Data
_player = [
    [0, 8, 0, 0, 0, 0, 8, 0],
    [8, 8, 0, 8, 8, 0, 8, 8],
    [8, 8, 0, 8, 8, 0, 8, 8],
    [10, 10, 10, 10, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 10, 10, 10],
    [0, 0, 10, 10, 10, 10, 0, 0],
    [0, 0, 0, 10, 10, 0, 0, 0],
    [0, 0, 0, 10, 10, 0, 0, 0],
]

# Player Shot Image Data
_player_shot = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 3, 0, 0, 0],
    [0, 0, 0, 9, 9, 0, 0, 0],
    [0, 0, 0, 9, 9, 0, 0, 0],
    [0, 0, 0, 3, 3, 0, 0, 0],
    [0, 0, 0, 3, 3, 0, 0, 0],
    [0, 0, 0, 3, 3, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

# Led Image Data
_led = [
    [0, 0, 0, 11, 9, 11, 0, 0],
    [0, 0, 0, 9, 9, 11, 0, 0],
    [0, 0, 0, 11, 11, 11, 0, 0],
    [0, 0, 11, 11, 11, 11, 11, 0],
    [0, 0, 0, 8, 0, 8, 0, 0],
    [0, 0, 0, 8, 0, 8, 0, 0],
    [0, 0, 0, 8, 0, 8, 0, 0],
    [0, 0, 0, 8, 0, 0, 0, 0],
]

# Led Shot Image Data
_led_shot = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 11, 11, 0, 0, 0],
    [0, 0, 0, 11, 11, 0, 0, 0],
    [0, 0, 0, 11, 11, 0, 0, 0],
    [0, 0, 0, 11, 11, 0, 0, 0],
    [0, 0, 0, 11, 11, 0, 0, 0],
    [0, 0, 0, 11, 11, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

