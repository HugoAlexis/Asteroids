from math import sqrt, sin, cos, acos
import pygame
from random import random
import Constants as cts


class Vector2d:
    """
    A mathematical 2 dimensional vector (immutable).
    """

    def __init__(self, x, y):
        """
        Creates a new 2 dimensional vector with coordinates x, y
        """
        self._coordinates = (x, y)
        self._magnitude = abs(sqrt(x**2 + y**2))
        self._unitary = False

        if self._magnitude < 0.001:
            self._unitary = True

        if self._magnitude != 0:
            if x <= 0:
                self._angle = acos(y/self._magnitude)
            else:
                self._angle = acos(-y/self._magnitude) + cts.PI
        else:
            self._angle = None

    @property
    def angle(self):
        return self._angle
    
    @property
    def x(self):
        return self._coordinates[0]

    @property
    def y(self):
        return self._coordinates[1]

    @property
    def magnitude(self):
        return self._magnitude
    
    @property
    def unitary(self):
        return self._unitary
    
    @staticmethod
    def unit(x, y):
        magnitude = sqrt(x**2 + y**2)

        x = x/magnitude
        y = y/magnitude

        return Vector2d(x, y)

    @staticmethod
    def unit_random():
        x = random() - 0.5
        y = random() - 0.5

        return Vector2d.unit(x, y)

    def __str__(self):
        return '({}, {})'.format(self._coordinates[0], self._coordinates[1])

    def __index__(self, index):
        if index == 0:
            return self._coordinates[0]
        elif index == 1:
            return self._coordinates[1]
        else:
            raise IndexError('Idex must be 0 or 1 for a Vector2d.')

    def __mul__(self, other):
        x = other * self.x
        y = other * self.y

        return Vector2d(x, y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y

        return Vector2d(x, y)

    def __rmul__(self, other):
        return self.__mul__(other)

    def rotate(self, angle):
        x_rot = cos(angle)*self.x - sin(angle)*self.y
        y_rot = sin(angle)*self.x + cos(angle)*self.y


        return Vector2d(x_rot, y_rot)

    def normalize(self, norm=1):
        x = self.x
        y = self.y

        return norm * Vector2d.unit(x, y)


class Keys():

    def __init__(self):
        self.QUIT = False

        self._K_LEFT = False
        self._K_RIGHT = False
        self._K_SPACE = False
        self._K_UP = False

        self.last_key_pressed = None

    def catch_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.QUIT = True
            elif event.type == pygame.KEYDOWN:
                self.last_key_pressed = event.key
                
                if event.key == pygame.K_RIGHT:
                    self.K_RIGHT = True
                elif event.key == pygame.K_LEFT:
                    self.K_LEFT = True
                elif event.key == pygame.K_SPACE:
                    self.K_SPACE = True
                elif event.key == pygame.K_UP:
                    self.K_UP  = True
            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_RIGHT:
                    self.K_RIGHT = False
                elif event.key == pygame.K_LEFT:
                    self.K_LEFT = False
                elif event.key == pygame.K_SPACE:
                    self.K_SPACE = False
                elif event.key == pygame.K_UP:
                    self.K_UP  = False

        if self.QUIT:
            return 'exit'
        else:
            return None

    def get_last_key(self):
        last = self.last_key_pressed
        self.last_key_pressed = None

        return last
    @property
    def K_UP(self):
        return self._K_UP

    @K_UP.setter
    def K_UP(self, state_key):
        if not isinstance(state_key, bool):
            raise ValueError('State of key must be bool.')
        else:
            self._K_UP = state_key

    @property
    def K_LEFT(self):
        return self._K_LEFT

    @K_LEFT.setter
    def K_LEFT(self, state_key):
        if not isinstance(state_key, bool):
            raise ValueError('State of key must be bool.')
        else:
            self._K_LEFT = state_key
    
    @property
    def K_RIGHT(self):
        return self._K_RIGHT

    @K_RIGHT.setter
    def K_RIGHT(self, state_key):
        if not isinstance(state_key, bool):
            raise ValueError('State of key must be bool')
        else:
            self._K_RIGHT =  state_key

    @property
    def K_SPACE(self):
        return self._K_SPACE

    @K_SPACE.setter
    def K_SPACE(self, state_key):
        if not isinstance(state_key, bool):
            raise ValueError('State of key must be bool')
        else:
            self._K_SPACE = state_key


class Sounds:
    
    background01 = pygame.mixer.Sound(cts.background_01)
    background02 = pygame.mixer.Sound(cts.background_02)
    shoot_sound = pygame.mixer.Sound(cts.shoot)
    big_explosion_sound = pygame.mixer.Sound(cts.big_explosion)
    medium_explosion_sound = pygame.mixer.Sound(cts.medium_explosion)
    small_explosion_sound = pygame.mixer.Sound(cts.small_explosion)
    new_live_sound = pygame.mixer.Sound(cts.new_live)

    @classmethod
    def background(cls, index):
        if index == 1:
            cls.background01.play()
        else:
            cls.background02.play()

    @classmethod
    def shoot(cls):
        cls.shoot_sound.play()

    @classmethod
    def big_explosion(cls):
        cls.big_explosion_sound.play()

    @classmethod
    def medium_explosion(cls):
        cls.medium_explosion_sound.play()

    @classmethod
    def small_explosion(cls):
        cls.small_explosion_sound.play()

    @classmethod
    def new_live(cls):
        cls.new_live_sound.play()

def remove_sprites(*args):
    """
    Remove the sprites with the property remove==True, from all the goups
    passed in the parameters.
    """
    for sprites_group in args:
        list_sprites = list(sprites_group)

        for sprite in list_sprites:
            if sprite.remove:
                sprites_group.remove(sprite)
