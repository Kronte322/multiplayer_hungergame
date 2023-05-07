import src.back.server_client.Message as Message


class Messenger:
    def __init__(self, connection):
        self.connection = connection

    def SendSetActiveServersOnUserLobbyMessage(self, list_with_active_servers):
        self.connection.AddMessage(Message.SetActiveServersOnUserLobbyMessage(list_with_active_servers))

    def SendSetActiveServersOnUserClientMessage(self, list_with_active_servers):
        self.connection.AddMessage(Message.SetActiveServersOnUserClientMessage(list_with_active_servers))

    def SendAddActiveServerOnServerLobbyMessage(self, address):
        self.connection.AddMessage(Message.AddActiveServerOnServerLobbyMessage(address))

    def SendSetSeedOnPlayerMessage(self, seed_of_generation):
        self.connection.AddMessage(Message.SetSeedOnPlayerMessage(seed_of_generation))

    def SendSetPlayersOnClient(self, players):
        self.connection.AddMessage(Message.SetPlayersOnClient(players))

    def SendSetGameObjectsOnClientMessage(self, game_objects):
        self.connection.AddMessage(Message.SetGameObjectsOnClientMessage(game_objects))


class PlayerClientMessenger(Messenger):
    def __init__(self, connection, client):
        super().__init__(connection)
        self.client = client

    def SendMovePlayerLeftOnTheServer(self):
        self.connection.AddMessage(Message.MovePlayerLeftOnTheServer(self.client.GetUser().GetUserId()))

    def SendMovePlayerRightOnTheServer(self):
        self.connection.AddMessage(Message.MovePlayerRightOnTheServer(self.client.GetUser().GetUserId()))

    def SendMovePlayerUpOnTheServer(self):
        self.connection.AddMessage(Message.MovePlayerUpOnTheServer(self.client.GetUser().GetUserId()))

    def SendMovePlayerDownOnTheServer(self):
        self.connection.AddMessage(Message.MovePlayerDownOnTheServer(self.client.GetUser().GetUserId()))

    def SendInitPlayerOnServerMessage(self):
        self.connection.AddMessage(
            Message.InitPlayerOnServerMessage(self.client.GetUser().GetUserId(), self.client.GetCharacter()))

    def SendLeaveMessage(self):
        self.connection.AddMessage(Message.LeaveMessage(self.client.GetUser().GetUserId()))

    def SendAddAttackMessage(self, side):
        self.connection.AddMessage(Message.AddAttackMessage(self.client.GetUser().GetUserId(), side))
