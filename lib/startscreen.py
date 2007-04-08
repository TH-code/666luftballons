import pygame
from game import Game
from credits import CreditsScreen
from highscore import HighScoreScreen
from help import HelpScreen
import data
from foot import Foot, GodlyCloud
from clouds import Clouds

class Button(pygame.sprite.Sprite):
    def __init__(self, normal_image, highlight_image, sound=None):
        super(Button, self).__init__()
        self.image = normal_image
        self.normal_image = normal_image
        self.highlight_image = highlight_image
        self.rect = normal_image.get_rect()
        self.sound = sound

    def select(self):
        self.image = self.highlight_image
        if self.sound is not None:
            self.sound.play()

    def deselect(self):
        self.image = self.normal_image

class StartScreen(object):
    def run(self, screen):
        from keys import *

        select_sound = data.load_sfx('select')

        background = data.load_graphic('startscreen-back-moving.png')
        screen.blit(background, (0, 0))
        pygame.display.update()

        clock = pygame.time.Clock()

        godly_cloud = GodlyCloud(
            data.load_graphic('cloud-foot.png'),
            data.load_graphic('leg.png'),
            190,
            4,
            droprange=(0, 768),
            offset=260)
        godly_cloud.foot.descent_speed = 400

        button_list = []

        start_button_background_1 = Button(
            data.load_graphic('startscreen-bigballoon-1.png'),
            data.load_graphic('startscreen-bigballoon-1.png'))
        start_button_background_1.rect.bottomleft = (16, 762)
        buttons = pygame.sprite.OrderedUpdates(start_button_background_1)

        start_button_background_2 = Button(
            data.load_graphic('startscreen-bigballoon-2.png'),
            data.load_graphic('startscreen-bigballoon-2.png')
        )
        start_button_background_2.rect.bottomleft = (
            start_button_background_1.rect.right,
            start_button_background_1.rect.bottom)
        buttons.add(start_button_background_2)

        start_text = Button(data.load_graphic('startscreen-start.png'),
                            data.load_graphic('startscreen-start-active.png'),
                            data.load_sfx('start-game'))
        start_text.rect.center = (300, 300)
        start_text.select()
        buttons.add(start_text)
        button_list.append(start_text)

        start_button = Button(
            data.load_graphic('startscreen-head.png'),
            data.load_graphic('startscreen-head.png')
        )
        start_button.rect.center = (335, 478)
        buttons.add(start_button)



        credits_button = Button(
            data.load_graphic('startscreen-credits.png'),
            data.load_graphic('startscreen-credits-active.png'),
            data.load_sfx('credits')
        )
        credits_button.rect.center = (542, 172)
        buttons.add(pygame.sprite.RenderUpdates(credits_button))
        button_list.append(credits_button)

        help_button = Button(
            data.load_graphic('startscreen-help.png'),
            data.load_graphic('startscreen-help-active.png'),
            data.load_sfx('help')
        )
        help_button.rect.center = (740, 440)
        buttons.add(pygame.sprite.RenderUpdates(help_button))
        button_list.append(help_button)

        highscore_button = Button(
            data.load_graphic('startscreen-highscore.png'),
            data.load_graphic('startscreen-highscore-active.png'),
            data.load_sfx('highscore')
        )
        highscore_button.rect.center = (934, 273)
        buttons.add(pygame.sprite.RenderUpdates(highscore_button))
        button_list.append(highscore_button)

        clouds = Clouds(data.load_frames('cloud', range(1, 16)))

        spritecollide = pygame.sprite.spritecollide

        head_range = (480, 460)
        head_step_time = 70
        head_direction = 1
        time_passed = 0

        # run game loop
        while True:
            time_passed += clock.tick(80)

            moved = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT:
                        godly_cloud.move(TO_LEFT)
                        moved = True
                    elif event.key == K_RIGHT:
                        godly_cloud.move(TO_RIGHT)
                        moved = True
                    elif event.key in DROP_KEYS:
                        godly_cloud.foot.drop()
                    elif event.key == pygame.K_h:
                        return HelpScreen()
                    elif event.key in QUIT_KEYS:
                        return

            if moved:
                select_sound.play()
                for i, button in enumerate(button_list):
                    if godly_cloud.foot.column == i:
                        button.select()
                    else:
                        button.deselect()

            for button in spritecollide(godly_cloud.foot, buttons,
                                         dokill=False):
                if button is start_text:
                    continue
                elif button is start_button:
                    return Game()
                elif button is credits_button:
                    return CreditsScreen()
                elif button is help_button:
                    return HelpScreen()
                elif button is highscore_button:
                    return HighScoreScreen()
            clouds.clear(screen, background)
            clouds.update()
            buttons.clear(screen, background)
            godly_cloud.clear(screen, background)
            godly_cloud.update()

            if time_passed >= head_step_time:
                start_button.rect.move_ip(0, head_direction)
                time_passed = 0

            if start_button.rect.centery < head_range[1]:
                head_direction = 1
            if start_button.rect.centery > head_range[0]:
                head_direction = -1
            
            buttons.update()
            updates = []
            updates.extend(clouds.draw(screen))
            updates.extend(buttons.draw(screen))
            updates.extend(godly_cloud.draw(screen))
            pygame.display.update(updates)
