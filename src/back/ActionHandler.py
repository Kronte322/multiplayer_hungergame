from src.back.GameObjects import *
import copy
import math


def GetDistance(first_point, second_point):
    return math.sqrt((second_point[0] - first_point[0]) ** 2 + (second_point[1] - first_point[1]) ** 2)


class ActionHandler:
    def __init__(self, game_server, mappa):
        self.game_server = game_server
        self.mappa = mappa
        self.dict_with_processing = {AttackObject: self.ProcessAttackObject}

    def MovePlayerLeft(self, player_id):
        player = self.game_server.GetPlayer(player_id)
        if player.CanMove():
            for point in player.GetHitBoxForLeftMovement():
                if not self.mappa.CanStandThere(point):
                    return
            player.MoveLeft()

    def MovePlayerRight(self, player_id):
        player = self.game_server.GetPlayer(player_id)
        if player.CanMove():
            for point in player.GetHitBoxForRightMovement():
                if not self.mappa.CanStandThere(point):
                    return
            player.MoveRight()

    def MovePlayerUp(self, player_id):
        player = self.game_server.GetPlayer(player_id)
        if player.CanMove():
            for point in player.GetHitBoxForUpMovement():
                if not self.mappa.CanStandThere(point):
                    return
            player.MoveUp()

    def MovePlayerDown(self, player_id):
        player = self.game_server.GetPlayer(player_id)
        if player.CanMove():
            for point in player.GetHitBoxForDownMovement():
                if not self.mappa.CanStandThere(point):
                    return
            player.MoveDown()

    def AddNewAttack(self, user_id, side):
        player = self.game_server.GetPlayer(user_id)
        if player.CanAttack():
            attack = DefaultSwordAttack(player, user_id, side, player.GetDamage())
            self.game_server.AddNewGameObject(attack)

    def ProcessAttackObject(self, attack_object):
        copied = copy.copy(self.game_server.GetPlayers())
        for point in attack_object.GetHitPoints():
            for player_id in copied:
                player = copied[player_id]
                if not player.IsDead():
                    if player_id != attack_object.GetUserId() and GetDistance(player.GetPositionOfCenter(),
                                                                              point) < attack_object.GetRadiusOfHit() + player.GetRadiusOfHitBox():
                        player.DecreaseHealth(attack_object.GetDamage())
                        if player.IsDead():
                            death = Death(player.GetPosition())
                            self.game_server.AddNewGameObject(death)

    def ProcessGameObjects(self):
        copied = copy.copy(self.game_server.GetGameObjects())
        for player_id in self.game_server.GetPlayers():
            self.game_server.GetPlayers()[player_id].DecreaseCooldownForAttack()
        for game_object in copied.values():
            game_object.Update()
            if game_object.ShouldBeDeleted():
                if isinstance(game_object, AttackObject):
                    game_object.Delete()
                self.game_server.DeleteGameObject(game_object.GetId())

            for object_type in self.dict_with_processing:
                if isinstance(game_object, object_type):
                    self.dict_with_processing[object_type](game_object)
