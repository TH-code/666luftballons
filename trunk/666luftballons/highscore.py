import os
import pygame
import data
import pickle

class HighScores(object):
    def __init__(self, filename):
        self.filename = filename
        self.max_scores = 6
        self.load()

    @property
    def path(self):
        return os.path.expanduser(os.path.join('~', '.' + self.filename))

    def load(self):
        try:
            f = open(self.path, 'rb')
        except IOError:
            self.scores = []
        else:
            self.scores = pickle.load(f)
            f.close()

    def save(self):
        try:
            f = open(self.path, 'wb')
        except IOError:
            return
        else:
            pickle.dump(self.scores, f)
            f.close()

    def is_highscore(self, score):
        if len(self.scores) < self.max_scores:
            return True
        # Check if score is higher than the lowest score
        elif score > self.scores[-1][0]:
            return True
        return False

    def add_score(self, name, score):
        self.scores.append((score, name))
        self.scores.sort()
        self.scores.reverse()
        self.scores = self.scores[:self.max_scores]

class HighScoreScreen(object):
    def run(self, screen):
        from keys import *
        background = data.load_graphic('screen-highscore.png')
        screen.blit(background, (0, 0))

        highscores = HighScores('666luftballons')
        highscores.load()

        chars = data.load_characters()

        top = 140
        row_height = 70
        score_right = 510
        name_left = 540
        for i, (score, name) in enumerate(highscores.scores):
            for j, c in enumerate(reversed(str(score))):
                c_rect = pygame.Rect(chars[c].get_rect())
                c_rect.right = score_right - j * c_rect.width
                c_rect.top = top + i * row_height

                screen.blit(chars[c], c_rect)

            for j, c in enumerate(name):
                c_rect = pygame.Rect(chars[c].get_rect())
                c_rect.left = name_left + j * c_rect.width
                c_rect.top = top + i * row_height

                screen.blit(chars[c], c_rect)

             

        pygame.display.update()
        clock = pygame.time.Clock()
        while True:
            clock.tick(80)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key in DROP_KEYS:
                        return
                    elif event.key in QUIT_KEYS:
                        return
