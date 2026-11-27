from tkinter import filedialog
import pygame

pygame.init()

screen = pygame.display.set_mode((900, 720))
pygame.display.set_caption("Pixel Painter App")
screen_rect = screen.get_rect()
clock = pygame.time.Clock()

# Pixel Class
class Pixel(pygame.Rect):
    pixel_array = []

    def draw_pixels(surface: pygame.Surface):
        for pixel in Pixel.pixel_array:
            pygame.draw.rect(surface, pixel.color, pixel.rect)

    def __init__(self, rect: pygame.Rect, color: pygame.Color):
        Pixel.pixel_array.append(self)

        self.rect = rect
        self.color = color

# Top Menu
menubar = pygame.Rect(0, 0, screen_rect.width, screen_rect.bottom - 660)
menu_label = {
    "File": ["Open", "Save"],
    "Edit": ["Clear"]
}

# Side Panel
sidebar = pygame.Rect((menubar.bottomleft), (screen_rect.right - 660, screen_rect.height - menubar.height))

# Canvas
canvas_window = pygame.Rect((sidebar.topright), (660, 660))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    # Draw Components
    pygame.draw.rect(screen, "black", menubar, 4)

    # Menubar Logic

    pygame.draw.rect(screen, "blue", sidebar, 4)
    pygame.draw.rect(screen, "gray", canvas_window, 4)

    

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()