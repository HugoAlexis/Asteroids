import pygame
import Constants as cts
from Enemies import Meteor
from os import system

class MainMenu:

    def __init__(self):
        self.items = ['new_game', 'high_scores', 'exit']
        self.background_app = pygame.image.load(cts.background_image)
        self.background_menu = pygame.image.load(cts.menu_image)
        self.selector = pygame.image.load(cts.selector_image)

        self.item_selected = 0

        self.meteors = pygame.sprite.Group()
        for i in range(8):
            meteor = Meteor('big', 'slow')
            self.meteors.add(meteor)

    def display(self, screen):

        self.meteors.update()

        screen.blit(self.background_app, (0, 0))
        self.meteors.draw(screen)
        screen.blit(self.background_menu, (0, 0))

        item = self.items[self.item_selected]
        pos  = cts.items[item]['pos']
        scale = cts.items[item]['scale']
        selector = pygame.transform.scale(self.selector, scale)
        screen.blit(selector, pos)

    def up(self):
        self.item_selected -= 1
        self.item_selected %= 3

    def down(self):
        self.item_selected += 1
        self.item_selected %= 3

    def enter(self):
        if self.item_selected == 0:
            return 'game'
        elif self.item_selected == 1:
            self.item_selected = 0
            return 'high_scores'
        else:
            return 'quit'


class PauseMenu:

    def __init__(self):
        self.items = ['continue', 'exit']
        self.background = pygame.image.load(cts.pause_image)
        self.selector = pygame.image.load(cts.selector_image)

        self.item_selected = 0

    def display(self, screen):
        screen.blit(self.background, (0, 0))

        item = self.items[self.item_selected]
        pos  = cts.items_paused[item]['pos']
        scale= cts.items_paused[item]['scale']

        selector_image = pygame.transform.scale(self.selector, scale)
        screen.blit(selector_image, pos)

    def up(self):
        self.item_selected -= 1
        self.item_selected %= 2

    def down(self):
        self.item_selected += 1
        self.item_selected %= 2

    def enter(self):
        if self.item_selected == 0:
            return 'game'
        else:
            self.item_selected = 0
            return 'main_menu'

class GameOverMenu:

    def __init__(self):
        self.player_name = ''
        self.background = pygame.image.load(cts.game_over_image).convert_alpha()
        self.font = pygame.font.Font('Fonts/Bitter-Bold.ttf', 25)

    def display(self, screen):
        text = self.font.render('{:<12}'.format(self.player_name), False, cts.black)

        
        screen.blit(self.background, (0, 0))
        screen.blit(text, (390, 290))

    def add_letter(self, ascii_value):
        if len(self.player_name) < 15:
            self.player_name = self.player_name + chr(ascii_value)

    def backspace(self):
        self.player_name = self.player_name[:-1]

    def enter(self, score):
        with open('data/Scores.txt', 'a') as f:
            print(f'{self.player_name:12}|{score:12.0f}', file=f)
        self.__init__()
        return 'main_menu'

class HighScoresMenu:
    
    def __init__(self):
        self.background = pygame.image.load(cts.background_image).convert_alpha()
        self.font = pygame.font.Font('Fonts/Bitter-Bold.ttf', 20)

    def display(self, screen):
        x1, x2, y = 325, 525, 100
        scores = self._load_scores()
        
        screen.blit(self.background, [0, 0])
        for score in scores:
            text_name = self.font.render('{}'.format(score[0]), False, cts.white)
            text_score= self.font.render('{:<10.0f}'.format(score[1]), False, cts.white)
            screen.blit(text_name, [x1, y])
            screen.blit(text_score, [x2, y])
            y += 1.2*text_name.get_height()

    def _load_scores(self):
        scores_file = open('data/Scores.txt', 'r')
        scores = []

        for line in scores_file:
            score_line = line.split('|')
            name_player_score = score_line[0]
            #name_player_score =  name_player_score.replace(' ', '_')
            score_player = int(score_line[1])

            scores.append([name_player_score, score_player])

        scores.sort(key=lambda item: item[1], reverse=True)
        while len(scores) < 10:
            scores.append(['Empty', 0])

        return scores[-10:]
