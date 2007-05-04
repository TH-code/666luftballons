import pygame
import random

class Clouds(pygame.sprite.RenderUpdates):
    def __init__(self, clouds):
        super(Clouds, self).__init__()
        self.clouds_gfx = clouds
        self.layers = 6
        self.layer_distance = 600 / self.layers
        self.speeds = range(6, 12)

        self.creat_clouds()
        for sprite in self.sprites():
            sprite.rect.centerx = random.randrange(0, 1024, 4)

    def update(self):
        super(Clouds, self).update()
        self.creat_clouds()

    def creat_clouds(self):
        if len(self.sprites()) < self.layers:
            used_layers = set([s.layer for s in self.sprites()])
            empty_layers = set(range(self.layers)).difference(used_layers)
            
            for layer in empty_layers:
                cloud = Cloud(random.choice(self.clouds_gfx),
                              random.choice(self.speeds),
                              random.choice([-1, 1]),
                              layer)
                cloud.rect.top = 100 + layer * self.layer_distance
                self.add(cloud)

class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, speed, direction, layer):
        super(Cloud, self).__init__()
        self.image = image
        self.rect = image.get_rect()
        self.speed = speed
        self.layer = layer

        self.clock = pygame.time.Clock()
        self.time_passed = 0
        self.step_time = 1000.0 / speed
        self.direction = direction
        if self.direction == 1:
            self.rect.right = 0
        else:
            self.rect.left = 1024

    def update(self):
        self.time_passed += self.clock.tick()
        if (self.direction == 1 and self.rect.left > 1024) or \
           (self.direction != 1 and self.rect.right < 0):
            self.kill()
        while self.time_passed > self.step_time:
            self.time_passed -= self.step_time
            self.rect.centerx += self.direction
