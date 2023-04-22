import socket
from abc import ABC, abstractmethod
from src.back.server_client.ServerConfig import *
import pickle
from src.back.server_client.Messenger import Messenger
import time


def IsTheServerAlive(address):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((address[0], address[1])) == 0


class Connection(ABC):
    def __init__(self, connection):
        self.connection = connection
        self.messages_to_send = []
        self.messenger = Messenger(self)

    @abstractmethod
    def ProcessThread(self):
        pass

    @abstractmethod
    def Send(self):
        pass

    @abstractmethod
    def Receive(self):
        pass

    def AddMessage(self, message):
        self.messages_to_send.append(message)

    def DropThread(self):
        self.connection.close()


class UserLobbyAsClientConnection(Connection):
    def __init__(self, connection, user_lobby):
        super().__init__(connection)
        self.user_lobby = user_lobby

    def ProcessThread(self):
        while True:
            try:
                print(self.user_lobby.GetConnectedServers())
                time.sleep(SLEEP_TIME)
                self.Send()
                self.Receive()
            except socket.error as error:
                print(str(error))
                break
        print("Connection Lost.")
        self.connection.close()

    def Send(self):
        self.connection.sendall(pickle.dumps(self.messages_to_send))
        self.messages_to_send.clear()

    def Receive(self):
        messages = pickle.loads(self.connection.recv(2048))
        for message in messages:
            message.Implement(self)
        pass

    def GetUserLobby(self):
        return self.user_lobby


class ServerLobbyForUserLobbyConnection(Connection):
    def __init__(self, connection, server_lobby):
        super().__init__(connection)
        self.server_lobby = server_lobby

    def ProcessThread(self):
        while True:
            try:
                self.Send()
                self.Receive()
            except socket.error as error:
                print(str(error))
                break
        print("Connection Lost.")
        self.connection.close()

    def Send(self):
        self.messenger.SendSetActiveServersOnUserLobbyMessage(
            [address for address in self.server_lobby.GetConnectedServers()])
        self.connection.sendall(pickle.dumps(self.messages_to_send))
        self.messages_to_send.clear()

    def Receive(self):
        messages = pickle.loads(self.connection.recv(2048))
        for message in messages:
            message.Implement(self)
        pass

    def GetServerLobby(self):
        return self.server_lobby


class GameServerAsClientConnection(Connection):
    def __init__(self, connection, game_server):
        super().__init__(connection)
        self.game_server_client = game_server

    def ProcessThread(self):
        while True:
            try:
                time.sleep(SLEEP_TIME)
                self.Send()
                self.Receive()
            except socket.error as error:
                print(str(error))
                break
        print("Connection Lost.")
        self.connection.close()

    def Send(self):
        self.messenger.SendAddActiveServerOnServerLobbyMessage(self.game_server_client.GetGameServer().GetAddress())
        self.connection.sendall(pickle.dumps(self.messages_to_send))
        self.messages_to_send.clear()

    def Receive(self):
        messages = pickle.loads(self.connection.recv(2048))
        for message in messages:
            message.Implement(self)
        pass

    def GetGameServerClient(self):
        return self.game_server_client


class ServerLobbyConnection(Connection):
    def __init__(self, connection, server_lobby):
        super().__init__(connection)
        self.server_lobby = server_lobby
        self.address_of_game_server = None

    def ProcessThread(self):
        while True:
            try:
                self.Send()
                self.Receive()
            except socket.error as error:
                if self.address_of_game_server is not None:
                    self.server_lobby.DeleteConnectedServer(self.address_of_game_server)
                print(str(error))
                break
        print("Connection Lost.")
        self.connection.close()

    def Send(self):
        self.connection.sendall(pickle.dumps(self.messages_to_send))
        self.messages_to_send.clear()

    def Receive(self):
        messages = pickle.loads(self.connection.recv(2048))
        for message in messages:
            message.Implement(self)
        pass

    def GetServerLobby(self):
        return self.server_lobby

    def GetAddressOfGameServer(self):
        return self.address_of_game_server

    def SetAddressOfGameServer(self, address):
        self.address_of_game_server = address


class UserClientConnection(Connection):
    def __init__(self, connection, user_client):
        super().__init__(connection)
        self.user_client = user_client

    def ProcessThread(self):
        while True:
            try:
                if self.user_client.IsDisconnected():
                    self.DropThread()
                time.sleep(SLEEP_TIME)
                print(self.user_client.GetActiveServers())
                self.Send()
                self.Receive()
            except socket.error as error:
                print(str(error))
                break
        print("Connection Lost.")
        self.connection.close()

    def Send(self):
        self.connection.sendall(pickle.dumps(self.messages_to_send))
        self.messages_to_send.clear()

    def Receive(self):
        messages = pickle.loads(self.connection.recv(2048))
        for message in messages:
            message.Implement(self)
        pass

    def GetUserClient(self):
        return self.user_client


class UserLobbyConnection(Connection):
    def __init__(self, connection, user_lobby):
        super().__init__(connection)
        self.user_lobby = user_lobby

    def ProcessThread(self):
        while True:
            try:
                self.Send()
                self.Receive()
            except socket.error as error:
                print(str(error))
                break
        print("Connection Lost.")
        self.connection.close()

    def Send(self):
        self.messenger.SendSetActiveServersOnUserClientMessage(self.user_lobby.GetConnectedServers())
        self.connection.sendall(pickle.dumps(self.messages_to_send))
        self.messages_to_send.clear()

    def Receive(self):
        messages = pickle.loads(self.connection.recv(2048))
        for message in messages:
            message.Implement(self)
        pass

    def GetUserLobby(self):
        return self.user_lobby


class GameServerConnection(Connection):
    def __init__(self, connection, game_server):
        super().__init__(connection)
        self.game_server = game_server
        self.messenger.SendSetSeedOnPlayerMessage(self.game_server.GetSeedOfGeneration())

    def ProcessThread(self):
        while True:
            try:
                self.Send()
                self.Receive()
            except socket.error as error:
                print(str(error))
                break
        print("Connection Lost.")
        self.connection.close()

    def Send(self):
        self.connection.sendall(pickle.dumps(self.messages_to_send))
        self.messages_to_send.clear()

    def Receive(self):
        messages = pickle.loads(self.connection.recv(2048))
        for message in messages:
            message.Implement(self)
        pass

    def GetGameServer(self):
        return self.game_server


class PlayerClientConnection(Connection):
    def __init__(self, connection, player_client):
        super().__init__(connection)
        self.player_client = player_client

    def ProcessThread(self):
        while True:
            try:
                self.Send()
                self.Receive()
            except socket.error as error:
                print(str(error))
                break
        print("Connection Lost.")
        self.connection.close()

    def Send(self):
        self.connection.sendall(pickle.dumps(self.messages_to_send))
        self.messages_to_send.clear()

    def Receive(self):
        messages = pickle.loads(self.connection.recv(2048))
        for message in messages:
            message.Implement(self)
        pass

    def GetPlayerClient(self):
        return self.player_client
