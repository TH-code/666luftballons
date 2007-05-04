'''Simple data loader module.

Loads data files from the "data" directory shipped with a game.

Enhancing this to handle caching etc. is left as an exercise for the reader.
'''

import os
import sys
import pygame
from animation import Animation

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))

if hasattr(sys, 'frozen'):
    data_dir = os.path.join(os.path.dirname(sys.executable), 'data')

cache = {}

def filepath(filename):
    '''Determine the path to a file in the data directory.
    '''
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):
    '''Open a file in the data directory.

    "mode" is passed as the second arg to open().
    '''
    return open(os.path.join(data_dir, filename), mode)

def load_graphic(filename):
    global cache
    if filename in cache:
        return cache[filename]
    image = pygame.image.load(os.path.join(data_dir, 'graphics', filename))
    image.convert_alpha()
    cache[filename] = image
    return image

def load_frames(name, frames):
    return [load_graphic('%s-%s.png' % (name, frame)) for frame in frames]

    
def load_animation(name, frames, fps):
    return Animation(load_frames(name, frames), fps)

def load_numerals():
    chars = dict(
        [(str(i), load_graphic(str(i) + '.png'))
         for i in  range(0, 10)])
    chars[':'] = load_graphic('dp.png')
    return chars

def load_characters():
    chars = dict(
        [(str(i), load_graphic('s' + str(i) + '.png'))
         for i in  range(0, 10)])

    chars.update(dict(
        [(chr(i),
          load_graphic(chr(i) + '.png')) for i in range(97, 123)]))
    chars['.'] = load_graphic('point-letters.png')
    return chars


class DummySound(object):
    def play(self):
        pass

def load_sfx(name):
    try:
        return pygame.mixer.Sound(os.path.join(data_dir, 'audio', name + '.ogg'))
    except pygame.error:
        return DummySound()

