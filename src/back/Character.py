"""File contains player class"""
import src.back.Config
from abc import ABC


class Character(ABC):
    """class for an entity that is controlled by the player"""

    def __init__(self, name, speed, size, health):
        """initialize player"""

        self.name = name
        self.speed = speed
        self.size = size
        self.health = health
        self.position = [0, 0]
        self.side = src.back.Config.RIGHT

    def GetName(self):
        return self.name

    def GetSpeed(self):
        return self.speed

    def GetSize(self):
        return self.size

    def GetHealth(self):
        return self.health

    def GetPosition(self):
        """this function gives position of player on the screen"""

        return self.position

    def SetPosition(self, position):
        self.position = position

    def GetSide(self):
        return self.side

    def GetStandHitBox(self):
        return self.position[0] + self.size / 2, self.position[1] + self.size

    def GetHitBoxForLeftMovement(self):
        return [(self.position[0] - self.speed, self.position[1] + self.size),
                (self.position[0] - self.speed, self.position[1] + self.size / 2)]

    def GetHitBoxForRightMovement(self):
        return [(self.position[0] + self.speed + self.size, self.position[1] + self.size),
                (self.position[0] + self.speed + self.size, self.position[1] + self.size / 2)]

    def GetHitBoxForUpMovement(self):
        return [(self.position[0], self.position[1] - self.speed + self.size / 2),
                (self.position[0] + self.size, self.position[1] - self.speed + self.size / 2)]

    def GetHitBoxForDownMovement(self):
        return [(self.position[0], self.position[1] + self.speed + self.size),
                (self.position[0] + self.size, self.position[1] + self.speed + self.size)]

    def MoveLeft(self):
        """this function moves player to the left"""

        if self.side == src.back.Config.RIGHT:
            self.side = src.back.Config.LEFT
        self.position[0] -= self.speed

    def MoveRight(self):
        """this function moves player to the right"""

        if self.side == src.back.Config.LEFT:
            self.side = src.back.Config.RIGHT
        self.position[0] += self.speed

    def MoveUp(self):
        """this function moves player to the up"""

        self.position[1] -= self.speed

    def MoveDown(self):
        """this function moves player to the down"""

        self.position[1] += self.speed


class Knight(Character):
    def __init__(self):
        super().__init__(src.back.Config.KNIGHT_NAME, src.back.Config.KNIGHT_MOVEMENT_SPEED,
                         src.back.Config.KNIGHT_SIZE, src.back.Config.KNIGHT_HEALTH)
