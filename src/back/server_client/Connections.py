import pickle
import socket
import time
from abc import ABC, abstractmethod

import src.back.server_client.ServerConfig as ServerConfig
from src.back.server_client.Messenger import Messenger, PlayerClientMessenger


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

    def GetMessenger(self):
        return self.messenger

    def AddMessage(self, message):
        self.messages_to_send.append(message)

    def DropThread(self):
        self.connection.close()


class GameServerConnection(Connection):
    def __init__(self, connection, game_server):
        super().__init__(connection)
        self.game_server = game_server
        self.messenger.SendSetSeedOnPlayerMessage(self.game_server.GetSeedOfGeneration())

    def ProcessThread(self):
        while True:
            try:
                time.sleep(1 / ServerConfig.TICK_RATE)
                self.Send()
                self.Receive()
            except socket.error as error:
                print(str(error))
                break
        print(ServerConfig.CONNECTION_LOST_MESSAGE)
        self.connection.close()

    def Send(self):
        self.messenger.SendSetGameObjectsOnClientMessage(self.game_server.GetGameObjects())
        self.messenger.SendSetPlayersOnClient(self.game_server.GetPlayers())
        self.connection.sendall(pickle.dumps(self.messages_to_send))
        self.messages_to_send.clear()

    def Receive(self):
        messages = pickle.loads(self.connection.recv(ServerConfig.NUM_OF_BYTES_TO_RECEIVE))
        for message in messages:
            message.Implement(self)
        pass

    def GetGameServer(self):
        return self.game_server


class PlayerConnection(Connection):
    def __init__(self, connection, player_client):
        super().__init__(connection)
        self.player_client = player_client
        self.messenger = PlayerClientMessenger(self, self.player_client)
        self.messenger.SendInitPlayerOnServerMessage()

    def ProcessThread(self):
        while True:
            try:
                self.Send()
                self.Receive()
            except socket.error as error:
                print(str(error))
                break
        print(ServerConfig.CONNECTION_LOST_MESSAGE)
        self.connection.close()

    def Send(self):
        self.connection.sendall(pickle.dumps(self.messages_to_send))
        self.messages_to_send.clear()

    def Receive(self):
        messages = pickle.loads(self.connection.recv(ServerConfig.NUM_OF_BYTES_TO_RECEIVE))
        for message in messages:
            message.Implement(self)
        pass

    def GetPlayerClient(self):
        return self.player_client
