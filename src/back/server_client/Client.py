import socket
from src.back.server_client.Connections import *
import _thread
from abc import ABC, abstractmethod


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


class UserLobbyAsClient(Client):
    def __init__(self, address, user_lobby):
        super().__init__(address)
        self.user_lobby = user_lobby
        _thread.start_new_thread(self.Connect, ())

    def Connect(self):
        try:
            self.soc.connect((self.address_of_server[0], self.address_of_server[1]))
        except socket.error as e:
            print(e)
            pass
        connection = UserLobbyAsClientConnection(self.soc, self.user_lobby)
        connection.ProcessThread()

    def GetUserLobby(self):
        return self.user_lobby


class UserClient(Client):
    def __init__(self, address):
        super().__init__(address)
        self.active_servers = []
        _thread.start_new_thread(self.Connect, ())

    def Connect(self):
        try:
            self.soc.connect((self.address_of_server[0], self.address_of_server[1]))
        except socket.error as e:
            print(e)
            pass
        connection = UserClientConnection(self.soc, self)
        connection.ProcessThread()

    def GetActiveServers(self):
        return self.active_servers

    def SetActiveServers(self, active_servers):
        self.active_servers = active_servers


def PingServer(address, time_out=2):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.settimeout(time_out)
    try:
        soc.connect((address[0], address[1]))
    except:
        return False
    soc.close()
    return True


class GameServerAsClient(Client):
    def __init__(self, address, game_server):
        super().__init__(address)
        self.game_server = game_server
        _thread.start_new_thread(self.Connect, ())

    def Connect(self):
        try:
            self.soc.connect((self.address_of_server[0], self.address_of_server[1]))
        except socket.error as e:
            print(e)
            pass
        connection = GameServerAsClientConnection(self.soc, self)
        connection.ProcessThread()

    def GetGameServer(self):
        return self.game_server


class PlayerClient(Client):
    def __init__(self, address, player):
        super().__init__(address)
        self.player = player
        self.seed_of_generation = None
        _thread.start_new_thread(self.Connect, ())

    def Connect(self):
        try:
            self.soc.connect((self.address_of_server[0], self.address_of_server[1]))
        except socket.error as e:
            print(e)
            pass
        connection = GameServerAsClientConnection(self.soc, self)
        connection.ProcessThread()

    def GetPlayer(self):
        return self.player

    def GetSeedOfGeneration(self):
        return self.seed_of_generation

    def SetSeedOfGeneration(self, seed_of_generation):
        self.seed_of_generation = seed_of_generation
