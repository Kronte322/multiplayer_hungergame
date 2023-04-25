class ActionHandler:
    def __init__(self, game_server, mappa):
        self.game_server = game_server
        self.mappa = mappa

    def MovePlayerLeft(self, player_id):
        player = self.game_server.GetPlayer(player_id)
        for point in player.GetHitBoxForLeftMovement():
            if not self.mappa.CanStandThere(point):
                return
        player.MoveLeft()

    def MovePlayerRight(self, player_id):
        player = self.game_server.GetPlayer(player_id)
        for point in player.GetHitBoxForRightMovement():
            if not self.mappa.CanStandThere(point):
                return
        player.MoveRight()

    def MovePlayerUp(self, player_id):
        player = self.game_server.GetPlayer(player_id)
        for point in player.GetHitBoxForUpMovement():
            if not self.mappa.CanStandThere(point):
                return
        player.MoveUp()

    def MovePlayerDown(self, player_id):
        player = self.game_server.GetPlayer(player_id)
        for point in player.GetHitBoxForDownMovement():
            if not self.mappa.CanStandThere(point):
                return
        player.MoveDown()
