import pygame

class Spiral(pygame.sprite.Sprite):
    def __init__(self, animation_clock_wise, animation_counter_clock_wise):
        super(Spiral, self).__init__()
        self.animation, self.animation_clock_wise = animation_clock_wise, animation_clock_wise
        self.animation_counter_clock_wise = animation_counter_clock_wise
        self.rect = self.image.get_rect()
        self.rect.centerx = 768/2
        self.rect.centery = 768/2

    def rotate(self, direction):
        if direction < 0:
            self.animation = self.animation_counter_clock_wise
        else:
            self.animation = self.animation_clock_wise
        
    @property
    def image(self):
        return self.animation.image

