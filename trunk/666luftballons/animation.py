import pygame

class Animation(object):
    def __init__(self, images, fps):
        self.images = images
        self.current_image = 0
        self.animation_frame_rate = fps
        self.animation_time_passed = 0
        self.animation_frame_time = 1000 / self.animation_frame_rate
        self.clock = pygame.time.Clock()

    @property
    def image(self):
        self.animation_time_passed += self.clock.tick()
        while self.animation_time_passed > self.animation_frame_time:
            self.animation_time_passed -= self.animation_frame_time
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
        return self.images[self.current_image]
