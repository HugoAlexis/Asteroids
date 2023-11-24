import pygame
from utils import Vector2d
import Constants as cts


class SpaceObject(pygame.sprite.Sprite):
    """
    Class for the different sprites in the game, representing an object in the space, 
    wich return to the screen when it get out from a side.
    """

    def __init__(self, sprite_x, sprite_y, sprite_size):
        """
        Create the new sprite whit physics in the space. Uses the spritesheet in the 
        constants module to take the image whit coordinates (sprite_x, sprite_y), whit 
        an image of size sprite_size.
        :param sprite_x: int
        :param sprite_y: int
        :param sprit_size: int
        :return: None
        """
        super().__init__()

        self.sprite_x_pos = sprite_x
        self.sprite_y_pos = sprite_y
        self.sprite_size  = sprite_size

        self.velocity = Vector2d(0, 0)
        self.direction = Vector2d.unit(0, 1)
        self.position_x = 0 
        self.position_y = 0
        self.rotation_speed = 0

        self.image = self._get_image()
        self.rect = self.image.get_rect()
        self.radius = sprite_size // 2

        self.remove = False     # -> If True, the sprite will be removed the next 
                                #    iteration of the main loop.

    @property
    def center(self):
        """
        Return the coordinates for the center of the image's sprite, in the coordinate
        system of the screen.
        :return: (int, int)
        """
        x = self.rect.x + self.image.get_width()
        y = self.rect.y + self.image.get_height()
        return x, y
    

    def update(self):
        """
        Update the state of the Sprite (This function is called every iteration
        of the main loop, while playing).
        """
        self.position_x += self.velocity.x
        self.position_y += self.velocity.y

        self.direction = self.direction.rotate(self.rotation_speed)

        self._teleport()

        self.image = self._get_image()
        self.rect.x = self.position_x
        self.rect.y = self.position_y

    def _get_image(self):
        """
        Transform and return the image for the sprite. (If it need to rotate the image, 
        it is done by its center).
        """
        angle = round(self.direction.angle * (180/cts.PI))

        size_image = self.sprite_size
        x_image = self.sprite_x_pos
        y_image = self.sprite_y_pos
        image = pygame.Surface([size_image, size_image], pygame.SRCALPHA)
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
