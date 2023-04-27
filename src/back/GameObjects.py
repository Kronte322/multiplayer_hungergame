from src.back.Config import *
from abc import ABC, abstractmethod
import uuid


class Object(ABC):
    @abstractmethod
    def Update(self):
        pass

    @abstractmethod
    def GetId(self):
        pass

    @abstractmethod
    def ShouldBeDeleted(self):
        pass


class Death(Object):
    def __init__(self, position):
        self.position = position
        self.id = uuid.uuid4()
        self.num_of_sprite = 0
        self.passed_frames = 1

    def GetId(self):
        return self.id

    def Update(self):
        self.passed_frames += 1
        if self.passed_frames % FREAQ_OF_DEATH_ANIMATION == 0:
            self.passed_frames = 1
            self.num_of_sprite += 1

    def GetSpriteId(self):
        return SPRITE_ID_FOR_DEATH + str(self.num_of_sprite)

    def ShouldBeDeleted(self):
        return self.num_of_sprite >= NUM_OF_SPRITES_FOR_DEATH_ANIMATION - 1

    def GetPositionOfCenter(self):
        return self.position[0] + DEFAULT_SIZE_OF_CHARACTER // 2, self.position[1] + DEFAULT_SIZE_OF_CHARACTER // 2

    def GetPosition(self):
        return self.position


positions_of_DefaultSwordAttack_according_to_side = {LEFT: (-DEFAULT_SIZE_OF_ATTACK // 2, 0),
                                                     RIGHT: (DEFAULT_SIZE_OF_ATTACK // 2, 0),
                                                     UP: (0, -DEFAULT_SIZE_OF_ATTACK // 2),
                                                     DOWN: (0, DEFAULT_SIZE_OF_ATTACK // 2)}


class AttackObject(Object, ABC):

    @abstractmethod
    def GetHitPoints(self):
        pass

    @abstractmethod
    def GetPositionOfCenter(self):
        pass

    @abstractmethod
    def GetSpriteId(self):
        pass

    @abstractmethod
    def GetRadiusOfHit(self):
        pass


class DefaultSwordAttack(AttackObject):
    def __init__(self, player, user_id, side, damage):
        self.player = player
        self.user_id = user_id
        self.player.MuteAttack()
        self.player.MuteMove()
        self.position = (player.GetPosition()[0] + positions_of_DefaultSwordAttack_according_to_side[side][0],
                         player.GetPosition()[1] + positions_of_DefaultSwordAttack_according_to_side[side][1])
        self.side = side
        if self.side in [LEFT, RIGHT]:
            self.player.SetSide(self.side)
        self.num_of_sprites = NUM_OF_SPRITES_FOR_ATTACK
        self.num_of_sprite = 0
        self.num_of_passed_frames = 1
        self.freq = player.GetAttackSpeed()
        self.hit_radius = 30
        self.damage = damage
        self.id = uuid.uuid4()

    def GetUserId(self):
        return self.user_id

    def GetDamage(self):
        return self.damage

    def Update(self):
        self.num_of_passed_frames += 1
        if self.num_of_passed_frames % self.freq == 0:
            self.num_of_passed_frames = 1
            self.num_of_sprite += 1

    def ShouldBeDeleted(self):
        return self.num_of_sprite >= self.num_of_sprites - 1

    def Delete(self):
        self.player.SetCooldownForAttack(COOLDOWN_FOR_ATTACK)
        self.player.UnMuteAttack()
        self.player.UnMuteMove()

    def GetPosition(self):
        return self.position

    def GetHitPoints(self):
        if self.num_of_sprite == 3 and self.num_of_passed_frames == 1:
            return [(self.position[0] + DEFAULT_SIZE_OF_ATTACK // 2, self.position[1] + DEFAULT_SIZE_OF_ATTACK // 2)]
        return []

    def GetRadiusOfHit(self):
        return self.hit_radius

    def GetPositionOfCenter(self):
        return self.position[0] + DEFAULT_SIZE_OF_ATTACK // 2, self.position[1] + DEFAULT_SIZE_OF_ATTACK // 2

    def GetId(self):
        return self.id

    def GetSpriteId(self):
        return SPRITE_ID_FOR_ATTACK + self.side + str(self.num_of_sprite)
