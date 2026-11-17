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
screen = pygame.display.set_mode((768, 768), pygame.SRCALPHA)
pygame.display.set_caption("Image Slicer Puzzle Game")
clock = pygame.Clock()
click = False

# Game Fonts
# Roboto Mono with Regular, Bold, Italic, Bold Italic
roboto_mono = pygame.font.SysFont("ROBOTOMONO", 36)
font1 = None
font2 = None

# Image Vars
image_path = None
_image_path = None
image = pygame.Surface((540, 540), pygame.SRCALPHA)
image_chosen = False
change_image = False
complete = False
images_completed = 0

# Difficulty & Tile Vars
selected_mode = 0
tile_sizes = ["Easy", "Meduim", "Hard", "Insane", "Nightmare"]
tile_num = 2
tiles_shuffled = False

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

    # Draw Screen Areas
    screen.fill("white")
    side_menu = pygame.Rect(image.get_rect().topright, (screen.get_rect().width - image.get_rect().width, screen.height))
    bottom_menu = pygame.Rect(image.get_rect().bottomleft, (screen.width, screen.height - image.height))
    change_box = pygame.Rect((bottom_menu.left + 8, bottom_menu.top + 8), (bottom_menu.width / 3, bottom_menu.height / 2 - 16))
    text = roboto_mono.render("Change Image", True, "black")
    pygame.draw.rect(screen, "lightgray", side_menu)
    pygame.draw.rect(screen, "darkgray", side_menu, 8)
    pygame.draw.rect(screen, "lightgray", bottom_menu)
    pygame.draw.rect(screen, "darkgray", bottom_menu, 8)
    pygame.draw.rect(screen, "black", change_box, 8)
    screen.blit(text, text.get_rect(center=change_box.center))
    # Draw Tiles on Bottom
    Tile.tiles.draw(screen)

    # Image Changing Box
    if (change_box.collidepoint(mouse_pos) or (image.get_rect().collidepoint(mouse_pos) and not image_path)) and click:
        click = False
        image_path = None
        change_image = True

    # Game Mode Logic
    for i in range(len(tile_sizes)):
        # Mode Text
        roboto_mono.point_size = 22
        level_text = roboto_mono.render(f"Mode: {tile_sizes[i]}", True, "black" if not selected_mode == i else (64, 64, 64))
        level_rect = level_text.get_rect(centerx=side_menu.centerx, top=i * level_text.height * 2 + 16)
        pygame.draw.line(screen, "black", level_rect.bottomleft, level_rect.bottomright, 2)
        screen.blit(level_text, level_rect)

        # Change Mode
        if level_rect.collidepoint(mouse_pos) and click:
            click = False
            selected_mode = i
            image_path = None
            # Mode Tile Sizes
            if selected_mode == 0:
                tile_num = 2
            if selected_mode == 1:
                tile_num = 4
            if selected_mode == 2:
                tile_num = 6
            if selected_mode == 3:
                tile_num = 10
            if selected_mode == 4:
                tile_num = 15
            # Reset Image
            image.fill("white")

    if not image_path:
        tiles_shuffled = False
        image_chosen = False
        # Default Image
        image.fill((64, 64, 64, 32))
        pygame.draw.rect(image, (64, 64, 64, 128), image.get_rect(), 8)
        text = roboto_mono.render("Choose Image", True, (0, 0, 0, 32))
        image.blit(text, text.get_rect(midbottom = image.get_rect().center))
        # Image Selection or Mode Change 
        path = choose_image() if change_image else ""
        if path:
            change_image = False
            _image_path = path
        if _image_path:
            image_path = _image_path
        screen.blit(image, image.get_rect())
    else:
        if not image_chosen:
            # Place Selected Image
            image_chosen = True
            _image = pygame.image.load(image_path).convert()
            _image = pygame.transform.smoothscale_by(_image, 540 / max(_image.width, _image.height))
            image.fill("white")
            image.blit(_image, _image.get_rect(center=image.get_rect().center))
            screen.blit(image, image.get_rect())
            # Reset Tile Group
            Tile.tiles.empty()
            Tile.deselect()
        else:
            if not tiles_shuffled:
                # Create Tiles
                tiles = []
                w = h = 540 // tile_num
                for i in range(tile_num * tile_num):
                    x = i % tile_num
                    y = i // tile_num
                    tile = Tile(image.subsurface((x * w, y * h, w, h)), (x * w, y * h,))

                # Shuffle Tile Position (twice cus y not)
                shuffle_pos = [tile.rect.topleft for tile in Tile.tiles.sprites()]
                random.shuffle(shuffle_pos)
                random.shuffle(shuffle_pos)
                for tile in Tile.tiles.sprites():
                    tile.set_pos(shuffle_pos[Tile.tiles.sprites().index(tile)])

                tiles_shuffled = True
                complete = False

            for tile in Tile.tiles.sprites():
                # Draw Outline of Selected Tile
                if tile == Tile.selected_tile:
                    pygame.draw.rect(screen, "blue", tile.rect, 5)

                # Select and Switch Tiles
                if tile.rect.collidepoint(mouse_pos) and click:
                    click = False
                    Tile.select(tile)
                    if selected_mode < 2 and tile.placed:
                        Tile.deselect()
                        overlay = pygame.Surface((tile.rect.width, tile.rect.height), pygame.SRCALPHA)
                        overlay.fill((0, 255, 0, 32))
                        screen.blit(overlay, tile.rect.topleft)

    # Draw and Update Tiles
    Tile.tiles.update(selected_mode)
    # Completed Image Overlay
    if all(tile.original_pos == tile.current_pos for tile in Tile.tiles.sprites()) and image_chosen:
        overlay = pygame.Surface((540, 540), pygame.SRCALPHA)
        overlay.fill((0, 255, 0, 32))
        screen.blit(overlay)
        # Completed Image Counter
        if not complete and tiles_shuffled:
            complete = True
            images_completed += 1
        # Counter Text
        text = roboto_mono.render(f"{images_completed} Images Completed", True, "black", "white")
        screen.blit(text, text.get_rect(center=image.get_rect().center))

    # Image Outline
    pygame.draw.rect(screen, "black", (0, 0, 540, 540), 4)

    # Update Display and Time
    pygame.display.flip()
    clock.tick(60)

pygame.quit()