import pygame
import data

class HelpScreen(object):
    def run(self, screen):
        from keys import *
        background = data.load_graphic('help.png')
        screen.blit(background, (0, 0))
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
