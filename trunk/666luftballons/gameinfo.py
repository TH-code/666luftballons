import pygame
import random
import time

class GameInfo(pygame.sprite.RenderUpdates):
    def __init__(self, score, timer, score_animations, numerals, timer_banner,
                 combo_banner, score_banner):
        super(GameInfo, self).__init__()
        combo_panel = ComboPanel(score, score_animations, combo_banner)
        combo_panel.rect.left = 760

        score_panel = ScorePanel(score, numerals, score_banner)
        score_panel.rect.top = 220
        score_panel.rect.left = 760

        timer_panel = TimerPanel(timer, numerals, timer_banner)
        timer_panel.rect.top = 420
        timer_panel.rect.left = 760

        self.add(combo_panel)
        self.add(score_panel)
        self.add(timer_panel)

class ComboPanel(pygame.sprite.Sprite):
    def __init__(self, score, score_animations, banner):
        super(ComboPanel, self).__init__()
        self.image = banner.copy()
        self.rect = self.image.get_rect()
        self.score_animations = score_animations
        self.score = score
        self.banner = banner

    def update(self):
        self.image = self.banner.copy()
        for i, type in enumerate(self.score.sequence):
            if i < self.score.sequence_index:
                image_type = 'scored'
            elif i == self.score.sequence_index:
                image_type = 'next'
            else:
                image_type = 'normal'
            image = self.score_animations[type][image_type].image
            self.image.blit(image, (i * image.get_rect().width + 49, 50))

class ScorePanel(pygame.sprite.Sprite):
    def __init__(self, score, numerals, banner):
        super(ScorePanel, self).__init__()
        self.image = banner.copy()
        self.banner = banner
        self.rect = self.image.get_rect()
        self.score = score
        self.numerals = numerals

    def update(self):
        self.image = self.banner.copy()
        offset = 220 

        for i, number in enumerate(reversed(
            [s for s in str(self.score.score)])):

            char = self.numerals[number]
            offset -= char.get_rect().width
            self.image.blit(char, (offset - 26, 55))

class TimerPanel(pygame.sprite.Sprite):
    def __init__(self, timer, numerals, banner):
        super(TimerPanel, self).__init__()
        self.image = banner.copy()
        self.banner = banner
        self.rect = self.image.get_rect()
        self.timer = timer
        self.numerals = numerals

    def update(self):
        self.image = self.banner.copy()
        offset = 220

        remaining = time.localtime(self.timer.time_remaining / 1000)
        time_string = time.strftime('%M:%S', remaining)
        
        for i, number in enumerate(reversed(time_string)):
            char = self.numerals[number]
            offset -= char.get_rect().width
            self.image.blit(char, (offset - 26, 55))

class ScoreSystem(object):
    def __init__(self, field, balloon_types):
        self.field = field
        self.score = 0
        self.balloon_types = balloon_types

        self.choose_sequence()

    def choose_sequence(self):
        self.sequence = []
        self.sequence_index = 0

        visible_balloon_types = [b.type for b in self.field.sprites()]
        if len(visible_balloon_types) < 3:
            visible_balloon_types.extend(self.balloon_types)

        for i in range(3):
            type = random.choice(visible_balloon_types)
            visible_balloon_types.remove(type)
            self.sequence.append(type)

    def add(self, balloon):
        self.score += 5

        if balloon.type == self.sequence[self.sequence_index]:
            if self.sequence_index == len(self.sequence) - 1:
                self.score += 100
                self.choose_sequence()
                return True
            self.sequence_index += 1
        elif self.sequence_index == 1 and balloon.type == self.sequence[0]:
            pass # Do not reset the combo when you get a combo like; green,
                 # red, blue then score green twice (second time would normally
                 # reset the combo to zero).
        else:
            self.sequence_index = 0

class Timer(object):
    def __init__(self, max_time):
        self.clock = pygame.time.Clock()
        self.current_time = 0
        self.max_time = max_time
        self.expired = False

    def start(self):
        self.clock.tick()
        self.current_time = 0
        self.expired = False

    def update(self):
        self.current_time += self.clock.tick()
        if self.current_time > self.max_time:
            self.expired = True

    @property
    def time_remaining(self):
        remaining = self.max_time - self.current_time
        if remaining < 0:
            return 0
        return remaining
