import _thread
import socket
from abc import ABC, abstractmethod

import src.back.server_client.Connections as Connections


class Client(ABC):
    """abstract class for client"""

    def __init__(self, address):
        self.address_of_server = address
        self.address_of_client = None
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @abstractmethod
    def Connect(self):
        pass

    def GetAddressOfTheServer(self):
        return self.address_of_server

    def GetAddressOfClient(self):
        return self.address_of_client


class PlayerClient(Client):
    """class for player client"""

    def __init__(self, address, user, character):
        super().__init__(address)
        self.user = user
        self.character = character
        self.players = None
        self.game_objects = None
        self.seed_of_generation = None
        self.connection = None
        _thread.start_new_thread(self.Connect, ())

    def Connect(self):
        try:
            self.soc.connect((self.address_of_server[0], self.address_of_server[1]))
        except socket.error as e:
            print(e)
            raise e

        self.connection = Connections.PlayerConnection(self.soc, self)
        self.connection.ProcessThread()

    def GetConnection(self):
        return self.connection

    def GetUser(self):
        return self.user

    def SetPlayers(self, players):
        self.players = players

    def GetPlayers(self):
        return self.players

    def SetGameObjects(self, game_objects):
        self.game_objects = game_objects

    def GetGameObjects(self):
        return self.game_objects

    def GetSeedOfGeneration(self):
        return self.seed_of_generation

    def SetSeedOfGeneration(self, seed_of_generation):
        self.seed_of_generation = seed_of_generation

    def GetCharacter(self):
        return self.character
