import _thread
import uuid
from src.back.server_client.Connections import *
from src.back.server_client.DBclient import *
from src.back.ActionHandler import ActionHandler
from src.back.Map import Map
import sys
import time


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

    @abstractmethod
    def QuitServer(self):
        pass


class GameServer(Server):
    def __init__(self, address, size_of_map):
        super().__init__(address)
        self.messages = []
        self.seed_of_generation = time.time()
        self.map = Map(self.seed_of_generation, size_of_map)
        self.action_handler = ActionHandler(self, self.map)
        self.num_of_received_players = 0
        self.connected_players = {}
        self.num_of_connected_players = 0
        self.db_client = None

    def GetPlayer(self, player_id):
        return self.connected_players[player_id]

    def GetPlayers(self):
        return self.connected_players

    def GetActionHandler(self):
        return self.action_handler

    def AddMessage(self, message):
        self.messages.append(message)

    def AddNewPlayer(self, user_id, character):
        intermediate = character()
        intermediate.SetPosition(self.map.GetSpawnPositionOfPlayer())
        self.connected_players[user_id] = intermediate

    def GetSeedOfGeneration(self):
        return self.seed_of_generation

    def StartServer(self):
        try:
            self.soc.bind((self.address[0], self.address[1]))
            self.db_client = DBConnection()
        except socket.error as error:
            print(str(error))

        self.soc.listen()
        self.db_client.SetServerOnline(self.db_client.GetServerId(self.address[0], self.address[1]))
        _thread.start_new_thread(self.QuitInput, ())

        print(START_GAME_SERVER_MESSAGE)
        _thread.start_new_thread(self.UpdateMessages, ())

        while True:
            conn, addr = self.soc.accept()
            connection = GameServerConnection(conn, self)
            _thread.start_new_thread(connection.ProcessThread, ())
            self.num_of_connected_players += 1
            # self.db_client.SetActivePlayersOnServer(self.address[0], self.address[1], self.num_of_connected_players)
            print(CONNECTED_MESSAGE, addr)

    def UpdateMessages(self):
        while True:
            time.sleep(1 / TICK_RATE)
            if self.num_of_connected_players != 0:
                if self.num_of_received_players == self.num_of_connected_players:
                    self.num_of_received_players = 0
                    self.messages.clear()

    def QuitServer(self):
        self.soc.close()
        self.db_client.SetServerOffline(self.db_client.GetServerId(self.address[0], self.address[1]))
        self.db_client.Close()
        sys.exit(0)

    def QuitInput(self):
        exit_string = input()
        if exit_string == 'quit':
            self.QuitServer()
