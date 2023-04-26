from src.back.server_client.Message import *


class Messenger:
    def __init__(self, connection):
        self.connection = connection

    def SendSetActiveServersOnUserLobbyMessage(self, list_with_active_servers):
        self.connection.AddMessage(SetActiveServersOnUserLobbyMessage(list_with_active_servers))

    def SendSetActiveServersOnUserClientMessage(self, list_with_active_servers):
        self.connection.AddMessage(SetActiveServersOnUserClientMessage(list_with_active_servers))

    def SendAddActiveServerOnServerLobbyMessage(self, address):
        self.connection.AddMessage(AddActiveServerOnServerLobbyMessage(address))

    def SendSetSeedOnPlayerMessage(self, seed_of_generation):
        self.connection.AddMessage(SetSeedOnPlayerMessage(seed_of_generation))

    def SendSetPlayersOnClient(self, players):
        self.connection.AddMessage(SetPlayersOnClient(players))

    def SendSetGameObjectsOnClientMessage(self, game_objects):
        self.connection.AddMessage(SetGameObjectsOnClientMessage(game_objects))


class PlayerClientMessenger(Messenger):
    def __init__(self, connection, client):
        super().__init__(connection)
        self.client = client

    def SendMovePlayerLeftOnTheServer(self):
        self.connection.AddMessage(MovePlayerLeftOnTheServer(self.client.GetUser().GetUserId()))

    def SendMovePlayerRightOnTheServer(self):
        self.connection.AddMessage(MovePlayerRightOnTheServer(self.client.GetUser().GetUserId()))

    def SendMovePlayerUpOnTheServer(self):
        self.connection.AddMessage(MovePlayerUpOnTheServer(self.client.GetUser().GetUserId()))

    def SendMovePlayerDownOnTheServer(self):
        self.connection.AddMessage(MovePlayerDownOnTheServer(self.client.GetUser().GetUserId()))

    def SendInitPlayerOnServerMessage(self):
        self.connection.AddMessage(
            InitPlayerOnServerMessage(self.client.GetUser().GetUserId(), self.client.GetCharacter()))

    def SendLeaveMessage(self):
        self.connection.AddMessage(LeaveMessage(self.client.GetUser().GetUserId()))

    def SendAddAttackMessage(self, side):
        self.connection.AddMessage(AddAttackMessage(self.client.GetUser().GetUserId(), side))
