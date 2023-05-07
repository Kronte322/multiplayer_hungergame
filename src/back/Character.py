"""File contains player class"""

import src.back.Config
from abc import ABC


class Character(ABC):
    """class for an entity that is controlled by the player"""

    def __init__(self, name, speed, size, health, attack_speed, damage, health_regeneration, regeneration_cooldown,
                 regeneration_speed):
        """initialize player"""

        self.name = name
        self.speed = speed
        self.size = size
        self.health = health
        self.health_regeneration = health_regeneration
        self.max_health = health
        self.position = [0, 0]
        self.side = src.back.Config.RIGHT
        self.can_attack = True
        self.can_move = True
        self.regeneration_cooldown = 0
        self.value_of_regeneration_cooldown = regeneration_cooldown
        self.regeneration_speed = regeneration_speed
        self.regeneration_ticks = 0
        self.attack_speed = attack_speed
        self.damage = damage
        self.radius_of_hit_box = size // 2
        self.is_dead = False
        self.cooldown_for_attack = 0

    def RegenerateHealth(self):
        self.health = min(self.max_health, self.health + self.health_regeneration)

    def Update(self):
        self.Regenerate()
        self.DecreaseCooldownForAttack()

    def Regenerate(self):
        self.regeneration_cooldown = max(0, self.regeneration_cooldown - 1)
        if self.regeneration_cooldown == 0:
            self.regeneration_ticks += 1
            if self.regeneration_ticks == self.regeneration_speed:
                self.regeneration_ticks = 0
                self.RegenerateHealth()

    def Dead(self):
        self.is_dead = True
        self.can_move = False
        self.can_attack = False

    def IsDead(self):
        return self.is_dead

    def SetCooldownForAttack(self, value):
        self.cooldown_for_attack = value

    def DecreaseCooldownForAttack(self):
        if self.cooldown_for_attack > 0:
            self.cooldown_for_attack -= 1

    def GetDamage(self):
        return self.damage

    def SetDamage(self, damage):
        self.damage = damage

    def GetRadiusOfHitBox(self):
        return self.radius_of_hit_box

    def DecreaseHealth(self, value):
        self.regeneration_cooldown = self.value_of_regeneration_cooldown
        self.health -= value
        if self.health <= 0:
            self.Dead()

    def GetMaxHealth(self):
        return self.max_health

    def SetMaxHealth(self, health):
        self.max_health = health

    def GetAttackSpeed(self):
        return self.attack_speed

    def CanAttack(self):
        return self.can_attack and self.cooldown_for_attack == 0

    def MuteAttack(self):
        self.can_attack = False

    def UnMuteAttack(self):
        self.can_attack = True
        test = 10

    def UnMuteMove(self):
        self.can_move = True

    def CanMove(self):
        return self.can_move

    def MuteMove(self):
        self.can_move = False

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

    def SetSide(self, side):
        self.side = side

    def GetPositionOfCenter(self):
        return self.position[0] + self.size / 2, self.position[1] + self.size / 2

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
                         src.back.Config.KNIGHT_SIZE, src.back.Config.KNIGHT_HEALTH,
                         src.back.Config.KNIGHT_ATTACK_SPEED, src.back.Config.KNIGHT_DAMAGE,
                         src.back.Config.KNIGHT_REGENERATION, src.back.Config.KNIGHT_REGENERATION_COOLDOWN,
                         src.back.Config.KNIGHT_REGENERATION_SPEED)
