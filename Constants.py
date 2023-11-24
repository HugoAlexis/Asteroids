import pygame
from random import choice
from math import pi as PI

pygame.init()

# ----  Some colors  ---- #
black = (  0,  0,  0)
red   = (255,  0,  0)
white = (255,255,255)
blue  = (  0,  0,255)

# ---- Game constants ----#
screen_size = (900, 600)
FPS = 60

# ---- Sprite's files ----#
#sprite_sheet = 'sprites/SpriteSheetGlobal.png'
background_image = 'sprites/BackGround.png'
spritesheet_laser = 'sprites/laser_red.png'
sprite_sheet = pygame.image.load('sprites/SpriteSheetGlobal.png')

sprites_map = {'ship_stopped'     :(  0,  0),
               'ship_moving'      :( 50,  0),
               'big_metheor'      :(  0, 50),
               'medium_metheor'   :[(100,  50), (160, 50)],
               'small_metheor'    :[(100, 110), (130, 110)],
               'initial_explosion':(150, 0),
               }

sprites_size = {'ship_stopped'   :50,
                'ship_moving'    :50,
                'big_metheor'    :100,
                'medium_metheor' :60,
                'small_metheor'  :30,
                'initial_explosion':100
}

def choice_rock():
    return choice(rock_files)


# ---- Player's deffault attributes ---- #
player_size_sprite = 60            # -> pixels
shoots_per_second = 3
player_max_speed = 300             # -> pixels/second
player_rotation_speed = 1.5*PI     # -> rad/second
player_show_laser = False          # -> Show red laser?
player_accel_magnitude = 10        # -> Magnitude of the acceleration for the player.


# ---- Metheor's deffault attributes
metheor_max_speed = 175


# ---- Laser's deffault attributes  ---- #
laser_speed = 500                  # -> Pixels/second


# ------------  Main menu  ------------- #
menu_image     = 'sprites/MainMenu.png'
selector_image = 'sprites/SelectorMenu.png'
pause_image    = 'sprites/PauseMenu.png'
game_over_image= 'sprites/GameOverMenu.png'

items = {'new_game'   : {'pos':(327, 302), 'scale':(231, 6)},
         'high_scores': {'pos':(327, 363), 'scale':(261, 6)},
         'exit'       : {'pos':(327, 421), 'scale':(92, 6)}
         }

# ------------ Pause menu -------------- #
items_paused = {'continue' : {'pos':(345, 361), 'scale':(203, 6)},
                'exit'     : {'pos':(345, 417), 'scale':( 94, 6)}
                }

# --------------  Sounds ---------------- #
big_explosion    = 'Sounds/bangLarge.wav'
medium_explosion = 'Sounds/bangMedium.wav'
small_explosion  = 'Sounds/bangSmall.wav'
background_01    = 'Sounds/beat1.wav'
background_02    = 'Sounds/beat2.wav'
new_live         = 'Sounds/extraShip.wav'
shoot            = 'Sounds/fire.wav'

