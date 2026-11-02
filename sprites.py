import pygame
import random

random.seed("Hello-World")

# Tile Sprite Class
class Tile(pygame.sprite.Sprite):
    # Tile Groups
    tiles = pygame.sprite.Group()
    grass_tiles = pygame.sprite.Group()
    water_tiles = pygame.sprite.Group()

    # Create Tile with Type and Postition
    def __init__(self, tile: int, pos: tuple | list):
        pygame.sprite.Sprite.__init__(self)
        self.add(Tile.tiles)

        # Tile Sprite Attributes
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self._type = tile
        self.type = tile
        self.time = 0

    # Tile Type Property
    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, val: int):
        # Tile Data
        stats = {
            "group":    [Tile.grass_tiles,  Tile.water_tiles],
            "color":    ["#008000",     "#000080"],
            "outline":  ["#00ff00",     "#0000ff"],
            "health":   [0,                 1],                    # Not Implemented
            "spread":   [0,                 0.1],
            "range":    [0,                 3],
            "coins":    [0,                 1],
        }
        # Set Tile Attributes
        self.remove(stats["group"][self._type])
        self._type = val
        self.range = stats["range"][self.type]
        self.spread = stats["spread"][self._type]
        self.coins = stats["coins"][self.type]
        self.add(stats["group"][self._type])
        self.image.fill(stats["color"][self._type])
        pygame.draw.rect(self.image, stats["outline"][self._type], self.image.get_rect(), 2, 4)

    # Tile Update Function
    def update(self, dt: int | float):
        # Don't Update Grass
        if self.type == 0:
            return

        # Update Every Second
        self.time += dt
        if self.time >= 1.0:
            # Get Tile Grid Position
            pos = Tile.tiles.sprites().index(self) 
            x, y = pos % 20, pos // 20
            # Random Spread
            for y1 in range(y - self.range // 2, y + self.range // 2 + 1):
                for x1 in range(x - self.range // 2, x + self.range // 2 + 1):
                   if random.random() < self.spread:
                    Tile.tiles.sprites()[(20 * y1 + x1) % 400].type = 1
            self.time -= 1.0


# Tower Sprite Class
class Tower(pygame.sprite.Sprite):
    # Tower Groups
    towers = pygame.sprite.Group()

    # Initialize Tower with Type and Position
    def __init__(self, tower: int, pos: tuple | list):
        pygame.sprite.Sprite.__init__(self)
        self.add(Tower.towers)

        # Tile Sprite Attributes
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.type = tower
        self.active = False
        self.shot_time = 0

        # Tower Data
        stats = {
            "type":     ["Cannon",  "Laser",    "Sniper"],
            "color":    ["gray",    "yellow",   "black"],
            "cost":     [25,        100,        500],
            "speed":    [350,       200,        500],
            "range":    [5,         5,          9],
            "attack":   [-0,         -0,          -0],             # Not Implemented
            "health":   [-0,         -0,          -0]              # Not Implemented
        }
        # Set Tower Attributes
        rect = pygame.Rect(0, 0, 32, 32)
        rect.center = self.image.get_rect().center
        pygame.draw.rect(self.image, stats["color"][self.type], rect, 4)
        self.name = stats["type"][self.type]
        self.attack = stats["attack"][self.type]
        self.speed = stats["speed"][self.type] / 1000
        self.range = stats["range"][self.type]
        self.health = stats["health"][self.type]
        self.price = stats["cost"][self.type]

    # Tower Update Function
    def update(self, dt: int | float):
        # Test for Grass Tile
        tile_type = pygame.sprite.spritecollide(self, Tile.tiles.sprites(), False)[0].type
        # Set Mode
        if tile_type == 0:
            self.active = True
        else:
            self.active = False

        # Update Every Second
        self.shot_time += dt
        if self.shot_time >= self.speed:
            if self.active:
                # Get Tile Position
                tile = pygame.sprite.spritecollide(self, Tile.tiles.sprites(), False)[0]
                pos = Tile.tiles.sprites().index(tile)
                x, y = pos % 20, pos // 20

                # Get Closest Water Tile
                distance = min((pygame.Vector2(self.rect.center).distance_to(Tile.tiles.sprites()[(20 * pygame.math.clamp(y1, 0, 19) + pygame.math.clamp(x1, 0, 19)) % 400].rect.center)
                            for y1 in range(y - self.range // 2, y + self.range // 2 + 1) 
                            for x1 in range(x - self.range // 2, x + self.range // 2 + 1)
                            if Tile.tiles.sprites()[(20 * pygame.math.clamp(y1, 0, 19) + pygame.math.clamp(x1, 0, 19)) % 400].type != 0), default=0)

                # Shoot at Water Tile
                for tile in Tile.tiles.sprites():
                    if pygame.Vector2(self.rect.center).distance_to(tile.rect.center) == distance and tile.type != 0:
                        shot = Projectile(self.type, self.rect.center, tile.rect)
                        break

            self.shot_time -= self.speed


# Projectile Sprite Class
class Projectile(pygame.sprite.Sprite):
    # Projectile Groups
    shots = pygame.sprite.Group()
    cannon_shots = pygame.sprite.Group()
    laser_shots = pygame.sprite.Group()
    sniper_shots = pygame.sprite.Group()

    #Initialize Projectile with Type, Position and Target
    def __init__(self, shot: int, pos: tuple | list, target: pygame.Rect):
        pygame.sprite.Sprite.__init__(self)
        self.add(Projectile.shots)

        # Projectile Sprite Attributes
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.type = shot
        self.target = target.centerx, target.centery

        # Projectile Data
        stats = {
            "group":    [Projectile.cannon_shots,   Projectile.laser_shots,    Projectile.sniper_shots],
            "color":    ["#ffffff",             "#ffff00",              "#000000"],
            "speed":    [3,                         5,                         11],
            "distance": [1,                         2,                         4]
        }
        # Set Projectile Attributes
        self.speed = stats["speed"][self.type]
        self.distance = stats["distance"][self.type]
        self.add(stats["group"][self.type])
        pygame.draw.circle(self.image, stats["color"][self.type], self.image.get_rect().center, 8, 4)

        # Movement Planning
        self.direction = pygame.Vector2(self.target) - pygame.Vector2(self.rect.center)
        self.step = self.direction.length() / ((self.direction.length() + 1) // self.speed + 1)
        self.direction = self.direction.normalize() if self.direction.length_squared() > 0 else pygame.Vector2()


    # Projectile Update Function
    def update(self, dt: int | float):        
        # Move Towards Target
        self.rect.left += self.direction.x * self.step
        self.rect.top += self.direction.y * self.step
        # Kill After Hitting Target Count
        if self.distance <= 0:
            self.kill()