import sys
from balloon import BalloonFactory, BalloonGenerator
from field import Field, Pop, TimedSprite
from foot import Foot, GodlyCloud
import data
from gameinfo import GameInfo, ScoreSystem, Timer
from animation import Animation
import pygame
from background import Sun
from spiral import Spiral
from clouds import Clouds
from highscore import HighScores

class Game(object):
    def run(self, screen):
        from keys import *

        pop_sound = data.load_sfx('pop')
        combo_sound = data.load_sfx('combo')
        highscore_sound = data.load_sfx('highscore')
        gameover_sound = data.load_sfx('pthrrrt')

        spritecollide = pygame.sprite.spritecollide

        # start with game setup
        field_size = 8
        square_size = 90
        clock = pygame.time.Clock()
        background = data.load_graphic('backgroundfade.png')
        screen.blit(background, (0, 0))
        loading = data.load_graphic('loading-4.png')
        screen.blit(loading, (10, 10))
        pygame.display.update()

        # create balloon types
        balloon_types = ('red', 'green', 'black', 'blue', 'purple')
        balloon_factories = []
        for type in balloon_types:
            balloon_frames = data.load_frames('balloon-'+type, range(140, 145))
            balloon_frames.extend(
                data.load_frames('balloon-'+type, range(1, 5)))
            normal = balloon_frames
            normal.extend(list(reversed(normal)))
            balloon_factories.append(
                BalloonFactory(
                    Animation(normal, 12),
                    data.load_animation('balloon-fire-'+type, range(1, 20), 8),
                    type))

        # create a playing field
        field = Field(size=field_size, square_size=square_size)
        field.rect.top = 48 
        balloon_generator = BalloonGenerator(field, balloon_factories)

        godly_cloud = GodlyCloud(
            data.load_graphic('cloud-foot.png'),
            data.load_graphic('leg.png'),
            square_size,
            field_size,
            droprange=(0, field_size * square_size))


        timer = Timer(1000 * 60 * 3)

        score = ScoreSystem(field=field, balloon_types=balloon_types)
        score_animations = {}
        for type in balloon_types:
            score_animations[type] = {
                'normal': Animation(
                    [data.load_graphic(type + '-alpha.png')], 1),
                'next': Animation(
                    [data.load_graphic(type + '-inactive.png')], 1),
                'scored': data.load_animation(type, range(1, 10), 14)}

        numerals = data.load_numerals()
        letters = data.load_characters()

        game_info = GameInfo(score=score, timer=timer,
                             score_animations=score_animations,
                             numerals=numerals,
                             timer_banner=data.load_graphic('time.png'),
                             combo_banner=data.load_graphic('combo-banner.png'),
                             score_banner=data.load_graphic('score-banner.png'),
                            )

        sun = Sun(Animation(data.load_frames('sun', range(1, 13)), 6))
        background_objects = pygame.sprite.RenderUpdates(sun)

        clouds = Clouds(data.load_frames('cloud', range(1, 16)))

        combo_index = 0

        spiral = Spiral(Animation(data.load_frames('whirl-cw', range(1, 19)), 30),
                        Animation(data.load_frames('whirl-ccw', range(1, 19)), 30))
        spiral_sprites = pygame.sprite.RenderUpdates(spiral)

        timer.start()

        game_over = data.load_graphic('game-over.png')
        highscore = data.load_graphic('highscore.png')
        name = data.load_graphic('name.png')

        pop_image = data.load_graphic('pop.png')
        combo_image = data.load_graphic('combo.png')

        timed_sprites = pygame.sprite.RenderUpdates()

        screen.blit(background, (0, 0))
        pygame.display.update()
        # run game loop
        while True:
            clock.tick(80)

            rotation = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT:
                        godly_cloud.move(TO_LEFT)
                    elif event.key == K_RIGHT:
                        godly_cloud.move(TO_RIGHT)
                    elif event.key in DROP_KEYS:
                        godly_cloud.foot.drop()
                    elif event.key in ROTATE_RIGHT_KEYS:
                        rotation = TO_RIGHT
                    elif event.key in ROTATE_LEFT_KEYS:
                        rotation = TO_LEFT
                    elif event.key in QUIT_KEYS:
                        return

            if rotation is not None:
                spiral.rotate(rotation)
                field.rotate(rotation)
                #sun.rotate(rotation)

                screenshot = screen.copy()
                for i in range(20):
                    spiral_sprites.clear(screen, screenshot)
                    spiral_sprites.update()
                    updates = spiral_sprites.draw(screen)
                    pygame.display.update(updates)
                    clock.tick(80)
                spiral_sprites.clear(screen, screenshot)
                pygame.display.update(updates)

            timer.update()

            if timer.expired:
                highscores = HighScores('666luftballons')
                highscores.load()
                if highscores.is_highscore(score.score):
                    rect = pygame.Rect(highscore.get_rect())
                    rect.centerx = field_size * square_size / 2
                    rect.centery = 768 / 2
                    screen.blit(highscore, rect)
                    pygame.display.update()
                    clock.tick(1000)

                    name_rect = pygame.Rect(name.get_rect())
                    name_rect.left = 760
                    name_rect.top = 550
                    screen.blit(name, name_rect)

                    highscore_sound.play()
                    pygame.display.update()

                    # Setup text entry
                    letter_a_rect = letters['a'].get_rect()
                    letter_width = letter_a_rect.width
                    letter_height = letter_a_rect.height
                    name_entry = pygame.Surface((letter_width, letter_height))

                    name_chars = list('...')
                    cursor_index = 0
                    blink_time = 400
                    time_passed = 0
                    blink = False
                    blink_image = pygame.Surface(
                        (letter_width, letter_height)).convert_alpha()
                    blink_image.fill((0, 0, 0, 0))

                    text_entry_left = 817
                    text_entry_top = 620

                    screenshot = screen.copy()
                    while True:
                        time_passed += clock.tick(80)

                        screen.blit(screenshot, (0, 0))
                        if time_passed > blink_time:
                            time_passed = 0
                            blink = not blink

                        for i, c in enumerate(name_chars):
                            rect = pygame.Rect(letter_a_rect)
                            rect.left = text_entry_left + letter_width * i
                            rect.top = text_entry_top

                            if blink and i == cursor_index:
                                surface = blink_image
                            else:
                                surface = letters[c]
                            screen.blit(surface, rect)
                        
                        pygame.display.update([pygame.Rect(text_entry_left,
                                                           text_entry_top,
                                                           3 * letter_width,
                                                           letter_height)])
                         

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                return
                            elif event.type == pygame.KEYDOWN:
                                key = pygame.key.name(event.key)
                                if key in letters:
                                    name_chars[cursor_index] = key
                                    cursor_index += 1
                                    if cursor_index >= len(name_chars):
                                        highscores.add_score(
                                            ''.join(name_chars), score.score)
                                        highscores.save()
                                        return
                else:
                    rect = pygame.Rect(game_over.get_rect())
                    rect.centerx = field_size * square_size / 2
                    rect.centery = 768 / 2
                    screen.blit(game_over, rect)
                    pygame.display.update()
                    gameover_sound.play()
                    pygame.time.wait(2500)
                    return
            
            background_objects.clear(screen, background)
            clouds.clear(screen, background)
            field.clear(screen, background)
            timed_sprites.clear(screen, background)
            godly_cloud.clear(screen, background)
            game_info.clear(screen, background)

            balloon_generator.update()
            field.update()
            clouds.update()
            background_objects.update()
            timed_sprites.update()
            game_info.update()
            godly_cloud.update()

            # Check for a balloon squash
            for balloon in spritecollide(godly_cloud.foot, field,
                                         dokill=False):
                pop_sound.play()
                if score.add(balloon): # Combo
                    timed_sprites.add(TimedSprite(
                        combo_image, 1600, (878, 650)))
                    combo_sound.play()
                godly_cloud.foot.pull_up()
                timed_sprites.add(Pop(pop_image, 200, balloon.rect.center))
                balloon.kill()

            updates = []
            updates.extend(clouds.draw(screen))
            updates.extend(background_objects.draw(screen))
            updates.extend(field.draw(screen))
            updates.extend(timed_sprites.draw(screen))
            updates.extend(godly_cloud.draw(screen))
            updates.extend(game_info.draw(screen))
            pygame.display.update(updates)
