'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''

import data
import os
import pygame
from startscreen import StartScreen
from optparse import OptionParser

def main(fullscreen=False):
    parser = OptionParser()
    parser.add_option('-f', '--fullscreen', action="store_true",
                      dest='fullscreen',
                      help='Play the game in fullscreen mode')
    options, args = parser.parse_args()

    pygame.init()
    try:
        pygame.mixer.music.load(os.path.join(data.data_dir, 'audio', 'background-zacht.ogg'))
        pygame.mixer.music.play(-1)
    except pygame.error:
        pass

    size = (1024, 768)

    if fullscreen or options.fullscreen:
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(size)


    startscreen = StartScreen()
    while True:
        next_screen = startscreen.run(screen)
        if next_screen is None:
            break
        next_screen.run(screen)
