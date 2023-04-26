import socket
from src.back.server_client.Connections import *
import _thread
from abc import ABC, abstractmethod
from src.back.server_client.DBclient import *
from src.back.server_client.Messenger import Messenger


class Client(ABC):
    def __init__(self, address):
        self.address_of_server = address
        self.address_of_client = None
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_disconnected = False

    @abstractmethod
    def Connect(self):
        pass

    def GetAddressOfTheServer(self):
        return self.address_of_server

    def GetAddressOfClient(self):
        return self.address_of_client

    def Disconnect(self):
        self.is_disconnected = True

    def IsDisconnected(self):
        return self.is_disconnected


class PlayerClient(Client):
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
        # try:
        self.soc.connect((self.address_of_server[0], self.address_of_server[1]))
        # except socket.error as e:
        #     print(e)
        #     pass
        self.connection = PlayerConnection(self.soc, self)
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
