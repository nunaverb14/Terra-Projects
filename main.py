from tkinter import filedialog
import pygame

pygame.init()

screen = pygame.display.set_mode((900, 720))
pygame.display.set_caption("Pixel Painter App")
screen_rect = screen.get_rect()
clock = pygame.time.Clock()

monocraft = pygame.font.Font(pygame.font.match_font("Monocraft"))

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

click = False

# Top Menu
show_menu = False
menu_button = -1
menu_item = -1
menubar = pygame.Rect(0, 0, screen_rect.width, screen_rect.bottom - 660)
menu_label = {
    "File": ["Open", "Save"],
    "Edit": ["Clear"],
    "Foo": [],
}

def menu_function(button: str, item:str):
    pass

# Side Panel
sidebar = pygame.Rect((menubar.bottomleft), (screen_rect.right - 660, screen_rect.height - menubar.height))

# Canvas
canvas_window = pygame.Rect((sidebar.topright), (660, 660))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False

    screen.fill("white")
    mouse_pos = pygame.mouse.get_pos()

    

    pygame.draw.rect(screen, "blue", sidebar, 4)
    pygame.draw.rect(screen, "gray", canvas_window, 4)

    # Draw Menubar
    pygame.draw.rect(screen, "black", menubar, 4)

    # Menubar Logic
    for button in menu_label:
        b = list(menu_label.keys()).index(button)

        # Draw Menu Buttons
        button_rect = pygame.draw.rect(screen, "black", ((b * 80, 0), (80, menubar.height)), 2)
        text = monocraft.render(button, False, "black")
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        # Get Menubar Button CLicked
        if button_rect.collidepoint(mouse_pos) and click:
            click = False
            menu_button = b

            if not show_menu:
                show_menu = True

        # Show Menubar Button Menu
        if show_menu and b == menu_button:
            button_menu = pygame.draw.rect(screen, "black", (button_rect.bottomleft, (button_rect.width, 40 * len(menu_label.get(button, [])))))

            for item in menu_label.get(button, []):
                i =  menu_label.get(button, []).index(item)

                item_rect = pygame.draw.rect(screen, "black", ((button_menu.left, button_menu.top + i * 40), (button_menu.width, 40)), 2)
                item_focused = True if item_rect.collidepoint(mouse_pos) else False
                pygame.draw.rect(screen, "darkgray" if item_focused else "black", item_rect)
                text = monocraft.render(item, False, "black" if item_focused else "white")
                text_rect = text.get_rect(center=item_rect.center)
                screen.blit(text, text_rect)

                # Get Menubar Button Menu Item Clicked
                if item_rect.collidepoint(mouse_pos) and click:
                    click = False
                    menu_item = i
                    menu_function(button, item)

            if not (button_rect.collidepoint(mouse_pos) or button_menu.collidepoint(mouse_pos)): 
                show_menu = False
                menu_button = -1
                menu_item = -1



    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()