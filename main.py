import pygame
from Player import *
from utils import *
from Constants import *
from Menus import *


class Game:
    """
    Control all the game (not the app).
    """

    def __init__(self):
        """
        Create a new game, with all the sprites for the game, the lives and the score.
        """
        self._score = 0
        self._lives = 3

        self._player = Player()
        self._background = pygame.image.load(cts.background_image).convert()
        self._background = pygame.transform.scale(self._background, cts.screen_size)

        self._all_sprites = pygame.sprite.Group()
        self._meteors = pygame.sprite.Group()
        self._lasers = pygame.sprite.Group()

        self._sound_counter = 1

        self._generate_meteors()

    @property
    def game_over(self):
        """
        Retunr True is the player don't have more lives (lives == 0).
        """
        if not self._lives:
            return True

        else:
            return False
    
    @property
    def score(self):
        """
        Return the score of the game.
        """
        return self._score
    

    def update(self, keys):
        """
        Update the state of the game, according with the pressed keys of the
        keyboard. If the player has pressed the close button in the window, 
        return 'quit', otherwise return 'game'.
        """
        self._play_background_sound()

        self._all_sprites.update()
        self._player.update(keys)

        if self._player.shoot:
            Sounds.shoot()
            laser = self._player.get_shoot()

            self._lasers.add(laser)
            self._all_sprites.add(laser)

        self._precess_colisions()

        if not len(self._meteors):
            self._generate_meteors()

        if keys.QUIT:
            return 'quit'
        else:
            return 'game'

    def new_game(self):
        self.__init__()

    def display_frame(self, screen):

        screen.blit(self._background, (0, 0))
        self._player.draw(screen)
        self._all_sprites.draw(screen)
        self._display_lives(screen)
        self._display_score(screen)

    def _play_background_sound(self):
        self._sound_counter -= 1
        if self._sound_counter % 180 == 0:
            Sounds.background(0)
        elif self._sound_counter % 180 == 90:
            Sounds.background(1)
        
        if self._sound_counter == 0:
            self._sound_counter = 179

    def _precess_colisions(self):
        for laser in self._lasers:
            meteors_shoted = pygame.sprite.spritecollide(laser, self._meteors, False, pygame.sprite.collide_circle)

            if meteors_shoted:
                laser.remove = True
                self._increase_score(meteors_shoted[-1].score_value)

                if meteors_shoted[-1].size == 'big':
                    Sounds.big_explosion()

                elif meteors_shoted[-1].size == 'medium':
                    Sounds.medium_explosion()

                else:
                    Sounds.small_explosion()

                new_objects = meteors_shoted[-1].remove_meteor()
                for o in new_objects:
                    if isinstance(o, Meteor):
                        self._meteors.add(o)
                    self._all_sprites.add(o)

        remove_sprites(self._all_sprites, self._lasers, self._meteors)

        if pygame.sprite.spritecollide(self._player, self._meteors, False, pygame.sprite.collide_circle):
            if not self._player.invincible:
                self._lives -= 1
                self._player.reset_state()
    
            if not self._lives:
                quit_app = True


    def _display_lives(self, screen):
        size_image = sprites_size['ship_stopped']
        x_image, y_image = cts.sprites_map['ship_stopped']

        image = pygame.Surface([size_image, size_image], pygame.SRCALPHA)
        image.blit(cts.sprite_sheet, (0, 0), (x_image, y_image, size_image, size_image))

        image = pygame.transform.rotate(image, 180)
        image = pygame.transform.scale(image, (35, 35))
        
        display_in_x = 10
        display_in_y = 30
        for live in range(self._lives):   
            screen.blit(image, [display_in_x, display_in_y])
            display_in_x += 1.1 * image.get_width() 

    def _display_score(self, screen):
        font = pygame.font.Font('Fonts/Bitter-Bold.ttf', 20)
        score_text = font.render('{:<10.0f}'.format(self._score), True, cts.white)
        screen.blit(score_text, [20, 5])

    def _generate_meteors(self):
        new_metheors = choice([5, 6])
        for _ in range(new_metheors):
            meteor = Meteor('big')
            self._meteors.add(meteor)
            self._all_sprites.add(meteor)

    def _increase_score(self, score_added):
        last_score = self._score
        self._score += score_added

        if self._score % 10000 < last_score % 10000:
            self._lives += 1
            Sounds.new_live()

def main():
    pygame.init()

    screen = pygame.display.set_mode(cts.screen_size)
    pygame.display.set_caption('Space shoot')
    clock = pygame.time.Clock()

    keys = Keys()
    game = Game()
    main_menu = MainMenu()
    paused_menu = PauseMenu()
    game_over_menu = GameOverMenu()
    high_scores_menu = HighScoresMenu()

    app_running = True
    app_state = 'main_menu'

    while app_running:

        exit_value = keys.catch_events(pygame.event.get())
        if exit_value == 'exit':
            app_state = 'quit'

        elif app_state == 'main_menu':

            key_pressed = keys.get_last_key()
            if key_pressed == pygame.K_UP:
                main_menu.up()
            elif key_pressed == pygame.K_DOWN:
                main_menu.down()
            elif key_pressed == pygame.K_RETURN:
                app_state = main_menu.enter()
                game.new_game()            

            main_menu.display(screen)

        elif app_state == 'high_scores':
            high_scores_menu.display(screen)
            if keys.get_last_key() == pygame.K_ESCAPE:
                app_state = 'main_menu'


        if app_state == 'game':
            app_state = game.update(keys)
            game.display_frame(screen)
            if game.game_over:
                app_state = 'game_over' 
            if keys.get_last_key() == pygame.K_ESCAPE:
                app_state = 'paused_menu'
        

        elif app_state == 'paused_menu':
            last_key = keys.get_last_key()
            if last_key == pygame.K_UP:
                paused_menu.up()
            elif last_key == pygame.K_DOWN:
                paused_menu.down()
            elif last_key == pygame.K_RETURN:
                app_state = paused_menu.enter()
                if app_state == 'main_menu':
                    game.new_game()
            game.display_frame(screen)
            paused_menu.display(screen)

        elif app_state == 'game_over':
            game_over_menu.display(screen)
            key_pressed = keys.get_last_key()
            if key_pressed is not None:
                if 97 <= key_pressed <= 122:
                    letter_ascii = key_pressed
                    if pygame.key.get_pressed()[-22] or pygame.key.get_pressed()[-20]:
                        letter_ascii -= 32
                    game_over_menu.add_letter(letter_ascii)
                elif key_pressed == pygame.K_SPACE:
                    game_over_menu.add_letter(95)
                
                elif key_pressed == pygame.K_BACKSPACE:
                    game_over_menu.backspace()

                elif key_pressed == pygame.K_RETURN:
                    app_state = game_over_menu.enter(game.score)



        elif app_state == 'quit':
            app_running = False
            

        
        pygame.display.flip()
        clock.tick(cts.FPS)

    pygame.quit()


if __name__ == '__main__':
    main()