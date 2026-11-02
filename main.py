from sprites import *
import pygame

random.seed("Hello-World")

# Pygame Init
pygame.init()
screen = pygame.display.set_mode((960, 768))
pygame.display.set_caption("Disaster Relief")
clock = pygame.time.Clock()

# Game Fonts
robotomono_24 = pygame.font.Font(pygame.font.match_font("robotomono", True), 24)

# Game Areas
# Game Board
board = pygame.Rect(0, 0, 640, 640)
pixel_size = 32
item_size = 96
# Create Tiles
for x in range(0, board.w // pixel_size):
    for y in range(board.h // pixel_size):
        Tile(0, (x * pixel_size + board.left, y * pixel_size + board.top))
# Choose "Random" Starting Tiles
for tile in random.choices(Tile.tiles.sprites(), k=2):
    tile.type = 1

# Shop
shop = pygame.Rect(board.right, 0, screen.width - board.width, screen.height)
item_box = pygame.Rect(shop.topleft, (shop.width, item_size))
item_image = pygame.Surface((32, 32), pygame.SRCALPHA)
item_rect = item_image.get_rect(left=shop.left + item_size / 4)

selected_tower = -1
selected_image = pygame.Surface((32, 32), pygame.SRCALPHA)
selected_rect = selected_image.get_rect()

# Info
info = pygame.Rect(0, board.bottom, board.width, screen.height - board.height)
num_towers = 3
towers_data = {
    "color":    ["gray",    "yellow", "black"]  + ["white"] * 6,
    "name":     ["Cannon",  "Laser", "Sniper"]   + ["Demo"] * 6,
    "info":     ["Shoots",  "Blasts", "Shoots"]   + ["Attacks"] * 6,        # Not Implemented
}

# Game Vars
clicked = False
money = 45
game_start = False
game_over = False
game_win = False


# Start Game Loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Improved Click Registering
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if game_start:
                    if board.collidepoint(event.pos):
                        clicked = True
                else:
                    time_offset = pygame.time.get_ticks()
                    game_start = True
    # Start Game
    if game_start and not game_over:
        # Deselect Shop Tower
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            selected_tower = -1
        
        # Draw Backgrounds
        screen.fill("black")
        pygame.draw.rect(screen, "#202020", board)
        pygame.draw.rect(screen, "#2e2e2e", info)
        pygame.draw.rect(screen, "#202020", shop)
        
        # Draw Tiles on Bottom
        Tile.tiles.draw(screen)

        # Game Over Conditions
        # All Tower Disabled and No Money
        if len(Tower.towers) >= 1:
            if all(tower.active == 0 for tower in Tower.towers) and money < 25:
                game_over = True
        # All Grass Tiles
        if all(tile.type == 0 for tile in Tile.tiles):
            game_over = True
            game_win = True
        # All Water Tiles
        else:
            if all(tile.type == 1 for tile in Tile.tiles):
                game_over = True
            time = (pygame.time.get_ticks() - time_offset) / 1000

        # Money and Time Text
        info_text = robotomono_24.render(f"Money: ${money:<6}", True, "white")
        info_rect = screen.blit(info_text, info_text.get_rect(top=board.bottom + 8, right=board.right - 8))
        info_text = robotomono_24.render(f"Time: {time:<6.1f}", True, "white")
        info_rect = screen.blit(info_text, info_text.get_rect(top=info_rect.bottom, left=info_rect.left))

        # Shop Layout
        for i in range(shop.height // item_size):
            # Tower Boxes and Labels
            item_box.top = i * item_size
            item_rect.centery = i * item_size + item_box.height / 2
            item_text = robotomono_24.render(towers_data.get("name")[i] + " Tower", True, "gray")

            # Tower Selection
            if item_box.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                selected_tower = i

            # Current Towers
            if selected_tower >= 0 and selected_tower < num_towers:
                tower = Tower(selected_tower, (-1000, -1000))
                tower.kill()
                # Tower Placement Preview
                for tile in Tile.tiles.sprites():
                    if tile.rect.collidepoint(pygame.mouse.get_pos()):
                        selected_rect.topleft = tile.rect.topleft

                        selected_image = tower.image
                        screen.blit(selected_image, selected_rect)

                # Tower Data Text
                info_text = robotomono_24.render(f"Tower:{tower.name:^6} Cost:{tower.price:^6}", True, "white")
                info_rect = screen.blit(info_text, info_text.get_rect(top=board.bottom + 8, left=board.left + 8))
                info_text = robotomono_24.render(f"Speed:{tower.speed:^6.2f} Range:{tower.range:^6}", True, "white")
                screen.blit(info_text, info_text.get_rect(top=info_rect.bottom, left=info_rect.left))

                # Tower Placement and Transaction
                if clicked and board.collidepoint(pygame.mouse.get_pos()):
                    tower = Tower(selected_tower, selected_rect.topleft)
                    # Tower Overlap Prevention
                    if len(pygame.sprite.spritecollide(tower, Tower.towers, False)) > 1 or money < tower.price:
                        tower.kill()
                    else:
                        money -= tower.price
                    clicked = False
                            
            # Draw Tower Boxes, Labels, and Images 
            pygame.draw.rect(screen, towers_data.get("color")[i] if item_box.collidepoint(pygame.mouse.get_pos()) or selected_tower * item_size == item_box.top  else "#404040", item_box, 5)
            pygame.draw.rect(screen, towers_data.get("color")[i], item_rect)
            screen.blit(item_text, item_text.get_rect(center=(item_box.left + item_box.width / 2, i * item_size + item_box.height / 2)))

        # Projectile Collision Detection
        for tile in Tile.tiles.sprites():
            for shot in pygame.sprite.spritecollide(tile, Projectile.shots, False):
                if tile.type != 0:
                    shot.distance -= 1
                    money += tile.coins
                    tile.type = 0
                    break

        # Offscreen Projectile Deletion
        for shot in Projectile.shots:
            if not board.colliderect(shot.rect):
                shot.kill()

        # Update Sprites and Screen
        Tower.towers.draw(screen)
        Projectile.shots.draw(screen)

        # Update Sprites Using dt
        dt = clock.tick(60) / 1000
        Tile.tiles.update(dt)
        Tower.towers.update(dt)
        Projectile.shots.update(dt)
        pygame.display.flip()
    else:
        # Start Screen
        if not game_over:
            screen_text = robotomono_24.render("Click To Play", True, "white")
            screen.blit(screen_text, screen_text.get_rect(center=screen.get_rect().center))
            pygame.display.flip()
        # Game Over Screens
        else:
            # Screen Overlay
            overlay = pygame.Surface(screen.size, pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 217))
            screen.blit(overlay)
            if game_win:
                # Game Win Text
                screen_text = robotomono_24.render("You have fended off the water but...", True, "red")
                text_rect = screen.blit(screen_text, screen_text.get_rect(centerx=screen.get_rect().centerx, top=screen.get_rect().centery - screen_text.height * 2))
                screen_text = robotomono_24.render("Like the rain it will be back...", True, "red")
                text_rect = screen.blit(screen_text, screen_text.get_rect(centerx=text_rect.centerx, top=screen.get_rect().centery))
                screen_text = robotomono_24.render("Next time with friends...", True, "red")
                text_rect = screen.blit(screen_text, screen_text.get_rect(centerx=text_rect.centerx, top=screen.get_rect().centery + screen_text.height * 2))
            else:
                # Game Lose Text
                screen_text = robotomono_24.render("You were unsuccessful in fending off the water", True, "red")
                text_rect = screen.blit(screen_text, screen_text.get_rect(centerx=screen.get_rect().centerx, top=screen.get_rect().centery - screen_text.height * 2))
                screen_text = robotomono_24.render("Your yard is now a muddy swamp :( ...", True, "red")
                text_rect = screen.blit(screen_text, screen_text.get_rect(centerx=text_rect.centerx, top=screen.get_rect().centery))
                screen_text = robotomono_24.render("Better luck next time...", True, "red")
                text_rect = screen.blit(screen_text, screen_text.get_rect(centerx=text_rect.centerx, top=screen.get_rect().centery + screen_text.height * 2))

            pygame.display.flip()
            quit = False

            # Quit Loop
            while not quit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        quit = True
                        break
                    elif event.type == pygame.KEYDOWN:
                        running = False
                        quit = True

pygame.quit()