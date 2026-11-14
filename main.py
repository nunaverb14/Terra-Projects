from tkinter import filedialog
from sprites import *
import pygame
import random

# Image File Chooser
def choose_image():
    filename = filedialog.askopenfilename(
        title="Choose an image",
        filetypes=[
            ("Images", "*.png *.jpg *.jpeg *.bmp"),
            ("All files", "*.*")
        ]
    )
    return filename

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((768, 768))
pygame.display.set_caption("Image Slicer Puzzle Game")
clock = pygame.Clock()
click = False

# Game Fonts
# Roboto Mono with Regular, Bold, Italic, Bold Italic
roboto_mono = pygame.font.SysFont("ROBOTOMONO", 36)
font1 = None
font2 = None

###
image_path = None
image = pygame.Surface((540, 540), pygame.SRCALPHA)
image_chosen = False

###
tile_num = 3
tiles_shuffled = False

# Game State Vars
game_start = False
game_over = False
game_win = False

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                click = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                click = False

    mouse_pos = pygame.mouse.get_pos()

    screen.fill("white")

    if not image_path:
        image = pygame.Surface((540, 540), pygame.SRCALPHA)
        image.fill((64, 64, 64, 32))
        pygame.draw.rect(image, (64, 64, 64, 128), image.get_rect(), 8)
        text = roboto_mono.render("Choose Image", True, (0, 0, 0, 32))
        image.blit(text, text.get_rect(midbottom = image.get_rect().center))
        change_box = pygame.Rect()
        if image.get_rect().collidepoint(mouse_pos) and click:
            click = False
            _image_path = choose_image()
            if _image_path:
                image_path = _image_path
        screen.blit(image, image.get_rect())
    else:
        if not image_chosen:
            image_chosen = True
            _image = pygame.image.load(image_path).convert()
            _image = pygame.transform.smoothscale_by(_image, 540 / max(_image.width, _image.height))
            image.fill("white")
            image.blit(_image, _image.get_rect(center=image.get_rect().center))
            screen.blit(image, image.get_rect())
        else:
            if not tiles_shuffled:
                tiles = []
                w = h = 540 / tile_num
                for i in range(tile_num * tile_num):
                    x = i % tile_num
                    y = i // tile_num
                    sub_rect = pygame.draw.rect(image, "blue", (x * w, y * h, w, h), 2)
                    tile = Tile(image.subsurface((x * w, y * h, w, h)), sub_rect.topleft)

                shuffle_pos = [tile.rect.topleft for tile in Tile.tiles.sprites()]
                random.shuffle(shuffle_pos)

                for tile in Tile.tiles.sprites():
                    tile.set_pos(shuffle_pos[Tile.tiles.sprites().index(tile)])
                tiles_shuffled = True
            
            pygame.draw.rect(screen, "black", (0, 0, 540, 540), 4)

    Tile.tiles.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()