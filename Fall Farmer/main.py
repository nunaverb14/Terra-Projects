from sprites import *
import pygame
import random

###
pygame.init()
screen = pygame.display.set_mode((800, 720))
pygame.display.set_caption("Fall Farmer")
clock = pygame.Clock()

cas_mono32 = pygame.font.SysFont(pygame.font.match_font("Cascadia Mono"), 32)

###
click = False

###
def load_image(image_path: str) -> pygame.Surface:
    return

###
def short_num(num: int):
    abbr = ["k", "m", "b", "t"]

###
money = 0
total_fruit = 5
current_fruit = 0
last_drop = 0
drop_delay = 0
drop_range = 0
golden_price = 2

###
player_image = pygame.Surface((48, 48), pygame.SRCALPHA)
player_image.fill("gold")
player = Player(player_image)
player.rect.topleft = (player.rect.left, screen.get_rect().bottom - player.rect.height)

###
board = pygame.Rect(0, 0, 520, screen.height)

###
upgrade_box = pygame.Rect(board.topright, (screen.width - board.width, screen.height))
item_box = pygame.Rect(upgrade_box.left, 0, upgrade_box.width, screen.height // (screen.height // 160 + 1))
selected_fruit = 0
###
upgrades = {
    "labels": ["Tasty", "Heavy", "More", "Golden", "Not"],
    "price": [5, 25, 80, 1000, 1000000],
    "amount": [30, 25, 20, 10, 1],
    "apple": [0, 0, 0, 0, 0],
    "orange": [0, 0, 0, 0, 0],
}

###
intro = False
game_start = False
game_over = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ###
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                click = True

    ###
    if game_start and not game_over:

        ###
        screen.fill("orchid")
        pygame.draw.rect(screen, "skyblue", board)
        pygame.draw.rect(screen, "lightblue", upgrade_box)

        ###
        text = cas_mono32.render(f"${money}", False, "black")
        text_rect = text.get_rect(topleft = (screen.get_rect().left + 8, screen.get_rect().top + 8))
        screen.blit(text, text_rect)

        ###
        for y in range(screen.height // item_box.height):
            ###
            y -= 1
            mouse_pos = pygame.mouse.get_pos()
            item_box = pygame.draw.rect(screen, Fruit.stats.get("color")[selected_fruit] if item_box.collidepoint(mouse_pos) else "black", item_box, 4)
            
            ###
            if click:
                click = True
                if item_box.collidepoint(mouse_pos) and click:
                    click = False
                    ###
                    if upgrades.get(list(upgrades.keys())[selected_fruit + 3])[y] < 1:
                        ###
                        if money >= upgrades.get("price")[y]:
                            ###
                            money -= upgrades.get("price")[y]
                            upgrades.get(list(upgrades.keys())[selected_fruit + 3])[y] = \
                                (upgrades.get(list(upgrades.keys())[selected_fruit + 3])[y] * upgrades.get("amount")[y] + 1) / upgrades.get("amount")[y]
                            upgrades.get("price")[y] = int(upgrades.get("price")[y] * (1 + upgrades.get(list(upgrades.keys())[selected_fruit + 3])[y] * 0.8))

                            if y == 0:
                                Fruit.stats.get("price")[selected_fruit] *= 1.2
                            if y == 1:
                                Fruit.stats.get("speed")[selected_fruit] += 0.15
                                drop_range += 35
                            if y == 2:
                                total_fruit += 2
                            if y == 3:
                                Fruit.stats.get("golden")[selected_fruit] += 0.05
                                golden_price += 2
                            if y == -1:
                                game_over = True
                                pygame.time.wait(2000)

            ###
            if upgrades.get(list(upgrades.keys())[selected_fruit + 3])[y] >= 1:
                upgrades.get("price")[y] = "Max"

            ###
            text = cas_mono32.render(f"{upgrades.get("labels")[y]} {Fruit.stats.get("name")[selected_fruit].title()}s", False, "black")
            text_rect = text.get_rect(midleft = (item_box.left + 64, item_box.centery - text.height))
            screen.blit(text, text_rect)

            ###
            text = cas_mono32.render(f"Price: {upgrades.get("price")[y]}", False, "black")
            text_rect = text.get_rect(midleft = (item_box.left + 16, item_box.centery + text.height * 1.5))
            screen.blit(text, text_rect)

            ###
            text = cas_mono32.render(f"{str(int(upgrades.get(list(upgrades.keys())[selected_fruit + 3])[y] * upgrades.get("amount")[y])):<.2} / {upgrades.get("amount")[y]}", False, "black")
            text_rect = text.get_rect(midright = (item_box.right - 16, item_box.centery + text.height * 1.5))
            screen.blit(text, text_rect)

            ###
            item_image = pygame.transform.scale(pygame.Surface((24, 24), pygame.SRCALPHA), (32, 32))
            item_image.fill(Fruit.stats.get("color")[selected_fruit])
            image_rect = item_image.get_rect(midleft = (item_box.left + 16, item_box.centery - text.height))
            screen.blit(item_image, image_rect)
            
            ###
            y += 1

            ###
            item_box.top = item_box.height * y
        
        ###
        now = pygame.time.get_ticks()
        if len(Fruit.fruits.sprites()) < total_fruit or current_fruit < total_fruit:
            if now - last_drop > drop_delay:
                drop_delay = (random.randrange(1000 - drop_range, 5000 - drop_range * 5, 250))
                last_drop = now
                current_fruit += 1
                fruit = Fruit(0, (random.randint(8, board.right - 32), -32))

            ###
            if current_fruit != len(Fruit.fruits.sprites()):
                current_fruit = len(Fruit.fruits.sprites())

        ###
        for fruit in Fruit.fruits.sprites():
            if fruit.rect.top > screen.get_rect().bottom + fruit.rect.height + 4:
                current_fruit -= 1
                fruit.kill()

        ###
        collected = pygame.sprite.spritecollide(player, Fruit.fruits, True)
        for fruit in collected:
            money += round(fruit.price * (golden_price if fruit.golden else 1))

        ###
        player.rect.clamp_ip(board)
        screen.blit(player.image, player.rect)
        Fruit.fruits.draw(screen)
        pygame.display.flip()

        ###
        dt = clock.tick(60) / 1000
        Fruit.fruits.update(dt)
        player.update(dt)
    
    else:
        ###
        if not game_start:

            if not intro:
                screen.fill("red")
                ###
                text = cas_mono32.render("WE give you Apples", False, "green")
                text_rect = text.get_rect(topleft = (screen.get_rect().left + 8, screen.get_rect().top))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(1000)

                ###
                text = cas_mono32.render("YOU give us praise", False, "green")
                text_rect = text.get_rect(topright = (screen.get_rect().right - 8, screen.get_rect().top + 32))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(1000)

                ###
                text = cas_mono32.render("WE need sacrifce", False, "green")
                text_rect = text.get_rect(topleft = (screen.get_rect().left + 8, screen.get_rect().top + 64))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(1000)

                text = cas_mono32.render("YOU go find it", False, "green")
                text_rect = text.get_rect(topright = (screen.get_rect().right - 8, screen.get_rect().top + 96))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(1000)

                ###
                text = cas_mono32.render("click to continue", False, "white")
                text_rect = text.get_rect(midbottom = screen.get_rect().midbottom)
                screen.blit(text, text_rect)
                intro = True

            if click:
                intro = False
                click = False
                game_start = True

        ###
        else:
            
            if not intro:
                screen.fill("orange")
                ###
                text = cas_mono32.render("WE give you Apples", False, "purple")
                text_rect = text.get_rect(topleft = (screen.get_rect().left + 8, screen.get_rect().top))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(1000)
                
                ###
                text = cas_mono32.render("YOU ask for more", False, "purple")
                text_rect = text.get_rect(topright = (screen.get_rect().right - 8, screen.get_rect().top + 32))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(1000)
                
                ###
                text = cas_mono32.render("WE can not give", False, "purple")
                text_rect = text.get_rect(topleft = (screen.get_rect().left + 8, screen.get_rect().top + 64))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(1000)
                
                text = cas_mono32.render("YOU will come back", False, "green")
                text_rect = text.get_rect(topright = (screen.get_rect().right - 8, screen.get_rect().top + 96))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(1000)

                intro = True
            
            if click:
                click = False
                running = False
   
        pygame.display.flip()

pygame.quit()