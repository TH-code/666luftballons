import pygame
from foot import Foot

class TimedSprite(pygame.sprite.Sprite):
    def __init__(self, image, display_time, position):
        super(Pop, self).__init__()
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = position
        self.clock = pygame.time.Clock()
        self.time_passed = 0
        self.display_time = display_time

    def update(self):
        self.time_passed += self.clock.tick()
        if self.time_passed > self.display_time:
            self.kill()

Pop = TimedSprite

class Field(pygame.sprite.RenderUpdates):
    def __init__(self, size, square_size):
        super(Field, self).__init__()
        self.rect = pygame.rect.Rect(
            0, 0, square_size * size, square_size * size)
        self.size = size
        self.square_size = square_size

    def update(self):
        super(Field, self).update()
        for sprite in self.sprites():
            # Move balloons to their proper row height
            sprite.rect.top = self.rect.top + sprite.cell[1] * self.square_size

            # Remove balloons that are to out of the screen
            if sprite.cell[1] < 0 or sprite.cell[1] > self.size:
                sprite.kill()

    def drop_foot(self):
        self.foot.drop()

    @property
    def collided_balloons(self):
        return []

    def add_balloon(self, column, balloon):
        balloon.rect.bottom = self.rect.bottom
        balloon.rect.left = balloon.cell[0] * self.square_size + self.rect.left
        self.add(balloon)

    def rotate(self, direction):
        size = self.size - 1
        for sprite in self.sprites():
            x, y = sprite.cell
            if direction == 1:
                sprite.cell = (size - y, x)
            else:
                sprite.cell = (y, size - x)
            sprite.time_passed = 0
            sprite.rect.left = self.rect.left + self.square_size * sprite.cell[0]
            sprite.rect.top = self.rect.top + self.square_size * sprite.cell[1]
