from abc import ABC, abstractmethod


class Message(ABC):
    @abstractmethod
    def Implement(self, connection):
        pass


class SetActiveServersOnUserLobbyMessage(Message):
    def __init__(self, list_with_active_servers):
        self.list_with_active_servers = list_with_active_servers

    def Implement(self, connection):
        connection.GetUserLobby().SetConnectedServers(self.list_with_active_servers)


class SetActiveServersOnUserClientMessage(Message):
    def __init__(self, list_with_active_servers):
        self.list_with_active_servers = list_with_active_servers

    def Implement(self, connection):
        connection.GetUserClient().SetActiveServers(self.list_with_active_servers)


class AddActiveServerOnServerLobbyMessage(Message):
    def __init__(self, address):
        self.address = address

    def Implement(self, connection):
        connection.SetAddressOfGameServer(self.address)
        connection.GetServerLobby().AddConnectedServer(self.address)


class SetSeedOnPlayerMessage(Message):
    def __init__(self, seed_of_generation):
        self.seed_of_generation = seed_of_generation

    def Implement(self, connection):
        connection.GetPlayerClient().SetSeedOfGeneration(self.seed_of_generation)
