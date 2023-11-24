from random import randint
from utils import *
from SpaceObject import *
import Constants as cts


class Meteor(SpaceObject):
    """
    Sprites for the lasers shooted by the player.
    """
    def __init__(self, size_meteor, speed_asteroid='normal'):
        if size_meteor == 'big':
            x_position, y_position = (0, 50)
            size = 100
            self.score_value = 20
        elif size_meteor == 'medium':
            x_position, y_position = (100, 50)
            size = 60
            self.score_value = 50
        elif size_meteor == 'small':
            x_position, y_position = (100, 110)
            self.score_value = 100
            size = 30

        super().__init__(x_position, y_position, size)

        self.size = size_meteor
        self.position_x = randint(0, cts.screen_size[0])
        self.position_y = randint(0, cts.screen_size[1])
        self.radius = 5/12 * self.sprite_size
        self.rotation_speed = random()/25

        # ------ The metheor can't be generated in the Player's position  ------ #
        while 1*cts.screen_size[0]//10 < self.position_x < 9*cts.screen_size[0]//10 and \
              1*cts.screen_size[1]//10 < self.position_y < 9*cts.screen_size[1]//10:
                self.position_x = randint(0, cts.screen_size[0])
                self.position_y = randint(0, cts.screen_size[1])

        speed = (1 - random()/2) * cts.metheor_max_speed
        speed = speed/cts.FPS
        if speed_asteroid == 'slow':
            speed *= 0.2
            self.rotation_speed *= 0.5
        self.velocity = speed*Vector2d.unit_random()

    def remove_meteor(self):
        explosion = Explosion(self.position_x, self.position_y, self.size)
        explosion.velocity = 0.75 * self.velocity
        explosion.rotation_speed = 0.75*self.rotation_speed

        self.remove = True
        if self.size == 'big':
            meteor1, meteor2 = Meteor('medium'), Meteor('medium')

            rot1, rot2 = 1-random()/2, 1-random()/2
            meteor1.velocity = self.velocity.rotate(rot1)
            meteor2.velocity = self.velocity.rotate(-rot2)
            meteor1.position_x, meteor1.position_y = self.position_x, self.position_y
            meteor2.position_x, meteor2.position_y = self.position_x, self.position_y

            return explosion, meteor1, meteor2

        elif self.size == 'medium':
            meteor1, meteor2 = Meteor('small'), Meteor('small')
            rot1, rot2 = random(), random()
            meteor1.velocity = self.velocity.rotate(rot1)
            meteor2.velocity = self.velocity.rotate(-rot2)
            meteor1.position_x, meteor1.position_y = self.position_x, self.position_y
            meteor2.position_x, meteor2.position_y = self.position_x, self.position_y
            return explosion, meteor1, meteor2

        else:
            return explosion, 


class Explosion(SpaceObject):

    def __init__(self, x_position, y_position, size):
        if size == 'big':
            self.scale = 0.85
            self.scale_augment = 0.025
        elif size == 'medium':
            self.scale = 0.5
            self.scale_augment = 0.02
        elif size == 'small':
            self.scale = 0.15
            self.scale_augment = 0.015
        else:
            raise ValueError('Unknown size for Explosion.')

        self.explosion_counter = 0

        super().__init__(0, 150, 100)
        self.position_x = x_position
        self.position_y = y_position
        
        

    def update(self):
        self.scale += self.scale_augment

        self.explosion_counter += 1
        self.image = self._get_image()
        if self.explosion_counter % 9 == 0:
            self.sprite_x_pos += 100

        if self.explosion_counter > 35:
            self.remove = True

        super().update()

    def _get_image(self):
        image = super()._get_image()
        scaled_size = int(self.scale * self.sprite_size)
        image = pygame.transform.scale(image, (scaled_size, scaled_size))
        image.convert_alpha()
        image.set_alpha(255)
        return image
