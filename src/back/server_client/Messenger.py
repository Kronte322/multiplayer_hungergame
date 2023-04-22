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
