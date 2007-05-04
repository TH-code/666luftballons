import pygame
import random
import time

class Balloon(pygame.sprite.Sprite):
    def __init__(self, normal_animation, fire_animation, cell, type):
        super(Balloon, self).__init__()
        self.normal_animation = normal_animation
        self.fire_animation = fire_animation
        self.current_animation = self.normal_animation
        self.image = self.normal_animation.image
        self.rect = self.image.get_rect()
        self.clock = pygame.time.Clock()
        self.time_passed = 0
        self.time_before_fire = 1800
        self.cell = cell
        self.step_time = 2200
        self.type = type

    def update(self):
        self.time_passed += self.clock.tick()
        if self.time_passed > self.time_before_fire:
            self.current_animation = self.fire_animation

        while self.time_passed > self.step_time:
            self.time_passed -= self.step_time
            self.cell = (self.cell[0], self.cell[1] - 1)
            self.current_animation = self.normal_animation

        self.image = self.current_animation.image

    def __eq__(self, other):
        return self.type == other.type

class BalloonFactory(object):
    def __init__(self, normal_animation, fire_animation, type):
        self.normal_animation = normal_animation
        self.fire_animation = fire_animation
        self.type = type

    def __call__(self, cell):
        return Balloon(self.normal_animation, self.fire_animation, cell, self.type)

class BalloonGenerator(object):
    def __init__(self, field, balloon_factories):
        self.field = field
        self.balloon_factories = balloon_factories

    def create_balloon(self, column):
        factory = random.choice(self.balloon_factories)
        return factory(cell=(column, self.field.size - 1))

    def update(self):
        sprites = self.field.sprites()
        if len(sprites) > 14:
            return
        available_columns = set(range(self.field.size))
        for sprite in sprites:
            if sprite.cell[1] > 6:
                available_columns.discard(sprite.cell[0])
        if available_columns:
            column = random.choice(list(available_columns))
            self.field.add_balloon(column, self.create_balloon(column))
