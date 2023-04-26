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


class MovePlayerLeftOnTheServer(Message):
    def __init__(self, player_id):
        self.player_id = player_id

    def Implement(self, connection):
        connection.GetGameServer().GetActionHandler().MovePlayerLeft(self.player_id)


class MovePlayerRightOnTheServer(Message):
    def __init__(self, player_id):
        self.player_id = player_id

    def Implement(self, connection):
        connection.GetGameServer().GetActionHandler().MovePlayerRight(self.player_id)


class MovePlayerUpOnTheServer(Message):
    def __init__(self, player_id):
        self.player_id = player_id

    def Implement(self, connection):
        connection.GetGameServer().GetActionHandler().MovePlayerUp(self.player_id)


class MovePlayerDownOnTheServer(Message):
    def __init__(self, player_id):
        self.player_id = player_id

    def Implement(self, connection):
        connection.GetGameServer().GetActionHandler().MovePlayerDown(self.player_id)


class SetPlayersOnClient(Message):
    def __init__(self, players):
        self.players = players

    def Implement(self, connection):
        connection.GetPlayerClient().SetPlayers(self.players)


class InitPlayerOnServerMessage(Message):
    def __init__(self, user_id, character):
        self.character = character
        self.user_id = user_id

    def Implement(self, connection):
        connection.GetGameServer().AddNewPlayer(self.user_id, self.character)


class LeaveMessage(Message):
    def __init__(self, user_id):
        self.user_id = user_id

    def Implement(self, connection):
        connection.GetGameServer().RemovePlayer(self.user_id)


class AddAttackMessage(Message):
    def __init__(self, user_id, side):
        self.user_id = user_id
        self.side = side

    def Implement(self, connection):
        connection.GetGameServer().GetActionHandler().AddNewAttack(self.user_id, self.side)


class SetGameObjectsOnClientMessage(Message):
    def __init__(self, game_objects):
        self.game_objects = game_objects

    def Implement(self, connection):
        connection.GetPlayerClient().SetGameObjects(self.game_objects)
