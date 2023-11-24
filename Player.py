from math import *
import pygame
from utils import *

class Player(pygame.sprite.Sprite):
    """
    Sprite of the player.
    """
    def __init__(self):
        """
        Creates the player's sprite, using the image in the spritesheet in the position
        defined in the module Constants.
        """
        super().__init__()

        self.velocity = Vector2d(0, 0)
        self.max_speed = cts.player_max_speed/cts.FPS
        self.rotation_speed = cts.player_rotation_speed/cts.FPS
        self.rotate_slow = 10
        self.direction = Vector2d.unit(0, 1)
        self.accelerating = True
        self.accel_magnitude = cts.player_accel_magnitude

        self.invincible = True
        self.invincible_counter = 3*cts.FPS

        self.shoots_per_second = cts.shoots_per_second
        self.show_laser = cts.player_show_laser
        self.image = self._get_image()
        self.rect  = self.image.get_rect()
        
        self.radius = 15
        

        # ---- Position the sprite in the middle of the screen ---- #
        self.rect.x = cts.screen_size[0]//2 - self.image.get_width()//2
        self.rect.y = cts.screen_size[1]//2 - self.image.get_height()//2

        # ---- If shoot is True, will create a laser (function get_shoot) ---- #
        self.shoot = False
        self._shoot_counter = 0

        self.position_x = self.rect.x
        self.position_y = self.rect.y

        self.remove = False

    def draw(self, screen):
        """
        Draw the player's sprite on the screen
        :param screen: pygame.Surface
        """

        if self.show_laser:
            laser_init = (self.rect.x + 25, self.rect.y + 25)
            laser_end  = (laser_init[0] + 2000*self.direction.x, laser_init[1] + 2000*self.direction.y)
            pygame.draw.line(screen, cts.red , laser_init, laser_end)

        screen.blit(self.image, [self.rect.x, self.rect.y])

    def update(self, keys):
        """
        Update the state of the player's sprite every frame.
        :param keys: Keys
        """
        
        self.change_state(keys)

        self._shoot_counter -= 1 if self._shoot_counter > 0 else 0
        self.invincible_counter -=1 if self.invincible_counter > 0 else 0
        if self.invincible_counter == 0:
            self.invincible = False

        if self.accelerating:
            self.acceleration = self.accel_magnitude * self.direction 
            self.velocity = self.velocity +  self.acceleration * (1/cts.FPS)
            if self.velocity.magnitude > self.max_speed:
                self.velocity = self.velocity.normalize(self.max_speed)

        self.position_x += self.velocity.x
        self.position_y += self.velocity.y

        self._teleport()

        self.rect.x = self.position_x
        self.rect.y = self.position_y

    def change_state(self, keys_state):
        """
        Change the player's state according to the pressed keys.
        """
        if not isinstance(keys_state, Keys):
            raise ValueError('keys_state must be an instance of Keys')

        if keys_state.K_UP:
            self.accelerating = True
        else:
            self.accelerating = False

        if keys_state.K_LEFT and not keys_state.K_RIGHT:

            if self.rotate_slow > 0 and not self.accelerating:
                self.direction = self.direction.rotate(-self.rotation_speed / 2)
                self.rotate_slow -= 1 if self.rotate_slow > 0 else 0
            else:
                self.direction = self.direction.rotate(-self.rotation_speed)
            
        elif keys_state.K_RIGHT and not keys_state.K_LEFT:

            if self.rotate_slow and not self.accelerating:
                self.rotate_slow -= 1 if self.rotate_slow > 0 else 0
                self.direction = self.direction.rotate(self.rotation_speed/2)
            else:
                self.direction = self.direction.rotate(self.rotation_speed)
        
        else:
            self.rotate_slow = 10

        if keys_state.K_SPACE and self._shoot_counter == 0:
            self._shoot_counter = cts.FPS // self.shoots_per_second
            self.shoot = True     

        self.image = self._get_image()

    def reset_state(self):
        self.velocity = Vector2d(0, 0)
        self.position_x = cts.screen_size[0]//2 - self.image.get_width()//2
        self.position_y = cts.screen_size[1]//2 - self.image.get_height()//2

        self.invincible = True
        self.invincible_counter = 3*cts.FPS

    def get_shoot(self):
        """
        If the player has shoot a laser, returns the Laser instance with its coordinates
        in front of the player's sprite.
        If the player's attribute shoot is Falser, raise an Error (because the player
        has no shooted).

        :return: Laser
        """
        if self.shoot:

            # ---- Find the position where will be generate the Laser ---- #
            x_shoot = self.rect.x + self.image.get_width()//2
            y_shoot = self.rect.y + self.image.get_height()//2
            self.corrector = 20 * self.direction
            shooted_laser = Laser(x_shoot, y_shoot, self.direction)
            

            self.shoot = False

            return shooted_laser

        else:
            raise ValueError('Player has not shooted.')

    def _get_image(self):
        """
        Return the properly image for the sprite, according with the state of the
        sprite.
        """
        angle = round(self.direction.angle * (180/cts.PI))

        size_image = 50
        if self.accelerating:
            x_image, y_image = 50, 0
        else:
            x_image, y_image =  0, 0


        image = pygame.Surface([size_image, size_image], pygame.SRCALPHA)
        if self.invincible and self.invincible_counter % 20 in [0, 1, 2, 3, 4, 5, 6, 7]:
            return image
        else:
            image.blit(cts.sprite_sheet, (0, 0), (x_image, y_image, size_image, size_image))

            orig_rect = image.get_rect()
            rot_image = pygame.transform.rotate(image, -angle)
            rot_rect = orig_rect.copy()
            rot_rect.center = rot_image.get_rect().center
            rot_image = rot_image.subsurface(rot_rect).copy()
        
            return rot_image

    def _teleport(self):
        """
        Once the sprite get out of the screen by a side, change the position of the
        Sprite in the opposite side.
        """
        if self.position_x + self.image.get_width() < 0:
            self.position_x = cts.screen_size[0]
        elif self.position_x > cts.screen_size[0]:
            self.position_x = -self.image.get_width()

        if self.position_y + self.image.get_height() < 0:
            self.position_y = cts.screen_size[1]
        elif self.position_y > cts.screen_size[1]:
            self.position_y = -self.image.get_height()


class Laser(pygame.sprite.Sprite):
    """
    Class for the lasers of the ships.
    """

    def __init__(self, x, y, direction):
        """
        Creates a new laser shoot in the position (x, y) in the coordinate system of 
        the screen, moving in the direction passed as parameter.
        :param x: int
        :param y: int
        :param direction: Vector2d
        """
        if not isinstance(direction, Vector2d):
            raise ValueError('direction must be a Vector2d.')
        elif not Vector2d.unitary:
            raise ValueError('Vector2d for direction must be unitary')

        super().__init__()
        self.direction = direction
        self.sprite_sheet = pygame.image.load(cts.spritesheet_laser)
        self.image = self._get_image()

        self.rect = self.image.get_rect()
        self.rect.x = x - self.image.get_width()//2 
        self.rect.y = y - self.image.get_height()//2
        self.radius = 4

        self.position_x = self.rect.x 
        self.position_y = self.rect.y 

        self.speed = cts.laser_speed / cts.FPS

        self.remove = False

    def update(self):
        """
        Update the state (position) of the Laser each frame.
        """
        self.position_x += self.direction.x * self.speed
        self.position_y += self.direction.y * self.speed

        self.rect.x = self.position_x
        self.rect.y = self.position_y

        if not - cts.screen_size[0] < self.position_x < 2*cts.screen_size[0] or\
           not - cts.screen_size[1] < self.position_y < 2*cts.screen_size[1]:

            self.remove = True

    def _get_image(self):
        """
        Return the propperly image for the sprite, according with the state of
        the instace.
        """

        angle = round(self.direction.angle * (180/cts.PI))
        x_image, y_image =  0, 0
        size_image = 15

        image = pygame.Surface([size_image, size_image], pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x_image, y_image, size_image, size_image))

        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, -angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

