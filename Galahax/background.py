#File for background classes and action

import pygame
import random

# Class for starry effect 
class Star(pygame.Rect):
    stars = []

    def star_effect(count, color = "white"):
        for i in range(count):
            if len(Star.stars) < count:
                x = random.randint(1, 767)
                y = random.randint(1, 192)
                size = random.choice((1, 2, 1, 3, 2, 1))
                y_speed = random.randint(3, 5) if size <= 2 else 1
                Star(x, y, size, 0, y_speed)
        Star.move_bg(color)

    def move_bg(color):
        for star in Star.stars:
            star.move_ip(star.x_speed, star.y_speed)
            if star.x < 0 or star.x > 768 or star.y < 0 or star.y > 768:
                Star.stars.remove(star)
            else:
                pygame.draw.rect(pygame.display.get_surface(), color, star)


    def __init__(self, x, y, size, x_speed, y_speed):
        Star.stars.append(self)
        self.centerx = x
        self.centery = y
        self.width = size
        self.height = size
        self.x_speed = x_speed
        self.y_speed = y_speed
