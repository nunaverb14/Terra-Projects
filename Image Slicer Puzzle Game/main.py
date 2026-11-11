from tkinter import filedialog
import pygame

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
image = None
image_chosen = False

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
                click == False

    screen.fill("white")
    mouse_pos = pygame.mouse.get_pos()

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
    else:
        if not image_chosen:
            image_chosen = True
            image = pygame.image.load(image_path).convert()
            image = pygame.transform.smoothscale_by(image, 540 / max(image.width, image.height))
        else:
            pygame.draw.rect(image, "black", (0, 0, 540, 540), 4)
            pygame.draw.rect(screen, "black", (0, 0, 540, 540), 4)
        

    screen.blit(image, image.get_rect())

    pygame.display.flip()
    clock.tick(60)

pygame.quit()