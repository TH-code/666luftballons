import pygame
import math

_movement = {
    0:(0,1),
    1:(1,1),
    2:(1,0),
    3:(1,-1),
    4:(0,-1),
    -3:(-1,-1),
    -2:(-1,0),
    -1:(-1,1)}

class Sun(pygame.sprite.Sprite):
    def __init__(self, animation):
        super(Sun, self).__init__()
        self.animation = animation
        self.rect = self.image.get_rect()
        self.distance = 750 - self.rect.width
        self.rect.left = 621
        self.rect.top = 5
        self.target = (self.rect.left, self.rect.top)
        self.clock = pygame.time.Clock()
        self.time_passed = 0
        self.step_time = 1000 / 800.0

        self._rotation = 0

    def get_rotation(self):
        return self._rotation

    def set_rotation(self, value):
        self._rotation = value
        if self._rotation < 0:
            self._rotation = 3
        elif self._rotation > 3:
            self._rotation = 0
    rotation = property(get_rotation, set_rotation)
        
    @property
    def image(self):
        return self.animation.image

    def update(self):
        self.time_passed += self.clock.tick()
        if (self.rect.left, self.rect.top) == self.target:
            self.time_passed = 0
            self.rotation = 0
            return
        while self.time_passed > self.step_time:
            self.time_passed -= self.step_time

            x_difference = self.target[0] - self.rect.left
            y_difference = self.target[1] - self.rect.top

            angle = math.degrees(
                math.atan2(x_difference, y_difference))
            direction = int(angle/45)

            self.rect.move_ip(_movement[direction])

    def rotate(self, direction):
        size = self.distance
        if self.rotation == 0 and direction == 1:
            self.rect.left = size
            self.rect.top = size
        elif self.rotation == 1 and direction == 1:
            self.rect.left = 0
            self.rect.top = size
        elif self.rotation == 2 and direction == 1:
            self.rect.left = 0
            self.rect.top = 0
        elif self.rotation == 3 and direction == 1:
            self.rect.left = size
            self.rect.top = 0
        elif self.rotation == 0 and direction == -1:
            self.rect.left = 0
            self.rect.top = 0
        elif self.rotation == 3 and direction == -1:
            self.rect.left = 0
            self.rect.top = size
        elif self.rotation == 2 and direction == -1:
            self.rect.left = size
            self.rect.top = size
        elif self.rotation == 1 and direction == -1:
            self.rect.left = size
            self.rect.top = 0

        self.rotation = self.rotation + direction
