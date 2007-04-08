import pygame

class GodlyCloud(pygame.sprite.RenderUpdates):

    def __init__(self, cloud, foot, square_size, max_column, droprange,
                 offset=0):
        super(GodlyCloud, self).__init__()
        self.column = 0
        self.max_column = max_column
        self.foot = Foot(foot, square_size, droprange, offset)
        self.add(Cloud(cloud, square_size, offset))
        self.add(self.foot)


    def move(self, direction):
        if self.foot.dropping or self.foot.pulling_up:
            return
        if 0 <= (self.column + direction) < self.max_column:
            self.column += direction

        for sprite in self.sprites():
            sprite.column = self.column

class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, square_size, offset=0):
        super(Cloud, self).__init__()
        self.image = image
        self.square_size = square_size
        self.column = 0
        self.offset = offset

    @property
    def rect(self):
        rect = pygame.Rect(self.image.get_rect())
        rect.centerx = self.column * self.square_size + (self.square_size / 2) + self.offset
        return rect

class Foot(pygame.sprite.Sprite):

    def __init__(self, image, square_size, droprange, offset):
        super(Foot, self).__init__()
        self._image = image
        self.rect = self._image.get_rect()
        self.droprange = droprange
        self.descent_speed = 1400
        self.ascent_speed = 1400
        self.clock = pygame.time.Clock()
        self.time_passed = 0
        self.direction = 0
        self.column = 0
        self.max_column = 8
        self.square_size = square_size
        self.drop_depth = 0
        self.offset = offset

    def get_speed(self):
        return self.pixel_step_time * 1000

    def set_speed(self, speed):
        self.pixel_step_time = 1000.0 / speed

    speed = property(get_speed, set_speed)

    dropping = property(lambda self: self.direction == 1)
    pulling_up = property(lambda self: self.direction == -1)

    @property
    def image(self):
        image_rect = self._image.get_rect()
        offset = image_rect.bottom -self.drop_depth
        visible = pygame.Rect(image_rect)
        visible.height = self.drop_depth
        visible = visible.move(0, offset)
        return self._image.subsurface(visible.clip(image_rect))

    def get_rect(self):
        rect = pygame.Rect(
            0, 0,
            self._image.get_rect().width, self.drop_depth)
        rect.centerx = self.column * self.square_size + self.square_size / 2 + self.offset
        return rect

    def set_rect(self, value):
        self._rect = value
    rect = property(get_rect, set_rect)

    def reset_clock(self):
        self.time_passed = 0
        self.clock.tick()

    def drop(self):
        self.reset_clock()
        self.direction = 1
        self.speed = self.descent_speed

    def pull_up(self):
        self.reset_clock()
        self.direction = -1
        self.speed = self.ascent_speed

    def stop(self):
        self.direction = 0

    def move(self, direction):
        if self.direction != 0:
            return
        if 0 <= (self.column + direction) < self.max_column:
            self.column += direction

    def update(self):
        direction = self.direction
        if direction != 0:
            self.time_passed += self.clock.tick()
            while self.time_passed > self.pixel_step_time:
                self.time_passed -= self.pixel_step_time
                self.drop_depth += direction
        if self.drop_depth> self.droprange[1]:
            self.drop_depth= self.droprange[1]
            self.pull_up()
        elif self.drop_depth < self.droprange[0]:
            self.drop_depth = 0
            self.stop()
