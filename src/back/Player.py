"""File contains player class"""
import src.back.Config
from src.back.Config import *
import pygame


class Player:
    """class for an entity that is controlled by the player"""

    def __init__(self, character=None, side=RIGHT,
                 hit_box=((SPAWN_POSITION[0], SPAWN_POSITION[1]), (SIZE_OF_CHARACTER, SIZE_OF_CHARACTER))):
        """initialize player"""

        self.speed = SPEED_OF_CHARACTER
        self.side = side
        self.character = character
        if self.character is None:
            self.character = src.back.Config.CHARACTER

        self.hit_box = pygame.Rect(hit_box[0], hit_box[1])

        self.image = pygame.Surface(
            (SIZE_OF_CHARACTER, SIZE_OF_CHARACTER), flags=pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.image_of_character = pygame.image.load(PATH_TO_CHARACTER_PNG + self.character + '.png')
        self.image_of_character = pygame.transform.scale(
            self.image_of_character, (SIZE_OF_CHARACTER, SIZE_OF_CHARACTER))

        self.image.blit(self.image_of_character, (0, 0))

        if self.side == 'left':
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

    def GetPosition(self):
        """this function gives position of player on the screen"""

        return [self.hit_box.x + SIZE_OF_CHARACTER // 2, self.hit_box.y + SIZE_OF_CHARACTER]

    def MoveLeft(self, mappa):
        """this function moves player to the left"""

        if self.side == RIGHT:
            self.side = LEFT
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
        if mappa.CanStandThere(
                (self.hit_box.x - self.speed, self.hit_box.y + SIZE_OF_CHARACTER)):
            self.hit_box.x -= self.speed
        if self.hit_box.x <= self.moveBox[0]:
            self.hit_box.x += self.speed
            mappa.MoveMap([self.speed, 0])

    def MoveRight(self, mappa):
        """this function moves player to the right"""

        if self.side == LEFT:
            self.side = RIGHT
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
        if mappa.CanStandThere(
                (self.hit_box.x + SIZE_OF_CHARACTER + self.speed,
                 self.hit_box.y + SIZE_OF_CHARACTER)):
            self.hit_box.x += self.speed
        if self.hit_box.x >= self.moveBox[2] - SIZE_OF_CHARACTER:
            self.hit_box.x -= self.speed
            mappa.MoveMap([-self.speed, 0])

    def MoveUp(self, mappa):
        """this function moves player to the up"""

        if mappa.CanStandThere(
                (
                        self.hit_box.x,
                        self.hit_box.y + SIZE_OF_CHARACTER - self.speed - 8)):
            if mappa.CanStandThere((self.hit_box.x + SIZE_OF_CHARACTER,
                                    self.hit_box.y + SIZE_OF_CHARACTER - self.speed - 8)):
                self.hit_box.y -= self.speed
        if self.hit_box.y <= self.moveBox[1]:
            self.hit_box.y += self.speed
            mappa.MoveMap([0, self.speed])

    def MoveDown(self, mappa):
        """this function moves player to the down"""

        if mappa.CanStandThere(
                (self.hit_box.x, self.hit_box.y + SIZE_OF_CHARACTER + self.speed)):
            if mappa.CanStandThere((self.hit_box.x + SIZE_OF_CHARACTER,
                                    self.hit_box.y + SIZE_OF_CHARACTER + self.speed)):
                self.hit_box.y += self.speed
        if self.hit_box.y >= self.moveBox[3] - SIZE_OF_CHARACTER:
            self.hit_box.y -= self.speed
            mappa.MoveMap([0, -self.speed])

    def Render(self, screen):
        """draw player on the screen"""

        screen.blit(self.image, (self.hit_box.x, self.hit_box.y))
