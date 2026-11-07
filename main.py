from sprites import *
import pygame
import random

###
pygame.init()
screen = pygame.display.set_mode((800, 720))
pygame.display.set_caption("Fall Farmer")
clock = pygame.Clock()

###
def load_image(image_path: str) -> pygame.Surface:
    return

def short_num(num: int):
    abbr = ["k", "m", "b", "t"]

total_fruit = 5

###
player = Player(pygame.Surface((48, 48), pygame.SRCALPHA))

###
board = pygame.Rect(0, 0, 520, screen.height)

###
upgrade_box = pygame.Rect(board.topright, (screen.width - board.width, screen.height))
item_box = pygame.Rect(upgrade_box.left, 0, upgrade_box.width, screen.height // (screen.height // 80 + 1))


###
game_start = True
game_over = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ###
    if game_start and not game_over:

        ###
        screen.fill("orchid")
        pygame.draw.rect(screen, "skyblue", board)
        pygame.draw.rect(screen, "lightblue", upgrade_box)

        ###
        for y in range(screen.height // (screen.height // item_box.height + 1)):
            pygame.draw.rect(screen, "orange", item_box, 4)
            item_box.top = item_box.height * y







        for i in range(total_fruit):
            fruit_image = pygame.Surface((24, 24), pygame.SRCALPHA)
            fruit_image.fill("red")
            fruit = Fruit(fruit_image, (random.randint(0, board.right - fruit_image.width)))

        
        for fruit in Fruit.fruits.sprites():
            if not screen.get_rect().contains(fruit.rect):
                fruit.kill()


        ###
        collected = pygame.sprite.spritecollide(player, Fruit.fruits, False)
        for fruit in collected:
            if player.fruit_num < player.fruit_cap:
                player.fruit_num += 1
                fruit.kill()







        ###
        Fruit.fruits.draw(screen)
        player.rect.clamp_ip(board)
        screen.blit(player.image, (player.rect.left, screen.get_rect().bottom - player.rect.height))
        pygame.display.flip()

        ###
        dt = clock.tick(60) / 1000
        Fruit.fruits.update(dt)
        player.update(dt)
    
    else:
        if not game_start:
            screen.fill("red")
            pygame.display.flip()

        else:
            screen.fill("white")
            pygame.display.flip()


    

    
pygame.quit()