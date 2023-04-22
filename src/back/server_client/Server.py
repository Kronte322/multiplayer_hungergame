import _thread
import uuid
from src.back.server_client.Connections import *
import src.back.server_client.Client
import time
import random


def GenerateUniqueId():
    return uuid.uuid4()


class Server(ABC):
    def __init__(self, address):
        self.address = address
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def GetAddress(self):
        return self.address

    @abstractmethod
    def StartServer(self):
        pass


class LobbyForServers(Server):
    def __init__(self, address):
        super().__init__(address)
        self.connected_servers = {}
        self.StartServer()

    def GetConnectedServers(self):
        return self.connected_servers

    def AddConnectedServer(self, address):
        if address not in self.connected_servers:
            self.connected_servers[address] = address

    def DeleteConnectedServer(self, address):
        if address in self.connected_servers:
            self.connected_servers.pop(address)

    def StartServer(self):
        try:
            self.soc.bind((self.address[0], self.address[1]))
        except socket.error as error:
            print(str(error))

        self.soc.listen()

        print(START_LOBBY_FOR_SERVERS_MESSAGE)
        count = 0
        while True:
            conn, addr = self.soc.accept()
            if count == 0:
                connection = ServerLobbyForUserLobbyConnection(conn, self)
                count += 1
                _thread.start_new_thread(connection.ProcessThread, ())
            else:
                connection = ServerLobbyConnection(conn, self)
                _thread.start_new_thread(connection.ProcessThread, ())
            print(CONNECTED_MESSAGE, addr)


class LobbyForUsers(Server):
    def __init__(self, address, address_of_lobby_for_servers):
        super().__init__(address)
        self.address_of_lobby_for_servers = address_of_lobby_for_servers
        self.connected_servers = {}
        self.connected_users = {}
        self.StartServer()

    def GetConnectedServers(self):
        return self.connected_servers

    def AddConnectedUser(self, connection):
        self.connected_users[connection] = connection

    def SetConnectedServers(self, connected_servers):
        self.connected_servers = connected_servers

    def StartServer(self):
        client = src.back.server_client.Client.UserLobbyAsClient(self.address_of_lobby_for_servers, self)
        try:
            self.soc.bind((self.address[0], self.address[1]))
        except socket.error as error:
            print(str(error))

        self.soc.listen()

        print(START_LOBBY_FOR_SERVERS_MESSAGE)

        while True:
            conn, addr = self.soc.accept()
            connection = UserLobbyConnection(conn, self)
            _thread.start_new_thread(connection.ProcessThread, ())
            print(CONNECTED_MESSAGE, addr)


class GameServer(Server):
    def __init__(self, address, address_of_lobby_for_servers):
        super().__init__(address)
        self.address_of_lobby_for_servers = address_of_lobby_for_servers
        self.messages = []
        self.seed_of_generation = time.time()
        self.num_of_connected_players = 0
        self.received_players = 0
        self.StartServer()

    def AddMessage(self, message):
        self.messages.append(message)

    def GetSeedOfGeneration(self):
        return self.seed_of_generation

    def StartServer(self):
        try:
            self.soc.bind((self.address[0], self.address[1]))
        except socket.error as error:
            print(str(error))

        self.soc.listen()

        client = src.back.server_client.Client.GameServerAsClient(self.address_of_lobby_for_servers, self)

        print(START_GAME_SERVER_MESSAGE)
        _thread.start_new_thread(self.UpdateMessages, ())

        while True:
            conn, addr = self.soc.accept()
            connection = GameServerConnection(conn, self)
            _thread.start_new_thread(connection.ProcessThread, ())
            print(CONNECTED_MESSAGE, addr)

    def UpdateMessages(self):
        while True:
            time.sleep(1 / TICK_RATE)
            if self.num_of_connected_players != 0:
                if self.received_players == self.num_of_connected_players:
                    self.received_players = 0
                    self.messages.clear()
