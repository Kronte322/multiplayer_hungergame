import _thread
import uuid
from src.back.server_client.Connections import *
from src.back.DBconnection.DBclient import *
from src.back.server_client.ActionHandler import ActionHandler
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
        self.seed_of_generation = time.time()
        self.map = Map(self.seed_of_generation, size_of_map)
        self.action_handler = ActionHandler(self, self.map)
        self.connected_players = {}
        self.game_objects = {}
        self.num_of_connected_players = 0
        self.db_client = None

    def GetPlayer(self, player_id):
        return self.connected_players[player_id]

    def GetPlayers(self):
        return self.connected_players

    def AddNewGameObject(self, game_object):
        self.game_objects[game_object.GetId()] = game_object

    def DeleteGameObject(self, game_object_id):
        self.game_objects.pop(game_object_id)

    def GetGameObjects(self):
        return self.game_objects

    def GetActionHandler(self):
        return self.action_handler

    def AddNewPlayer(self, user_id, character):
        intermediate = character()
        intermediate.SetPosition(self.map.GetSpawnPositionOfPlayer())
        self.connected_players[user_id] = intermediate

    def RemovePlayer(self, user_id):
        self.num_of_connected_players -= 1
        self.connected_players.pop(user_id)
        self.db_client.SetActivePlayersOnServer(self.address[0], self.address[1], self.num_of_connected_players)

    def GetSeedOfGeneration(self):
        return self.seed_of_generation

    def StartServer(self):
        try:
            self.soc.bind((self.address[0], self.address[1]))
            self.db_client = DBConnection()
        except socket.error as error:
            print(str(error))
            return

        self.soc.listen()
        self.db_client.SetServerOnline(self.db_client.GetServerId(self.address[0], self.address[1]))
        _thread.start_new_thread(self.QuitInput, ())
        _thread.start_new_thread(self.ProcessGameObjects, ())

        print(START_GAME_SERVER_MESSAGE)

        while True:
            conn, addr = self.soc.accept()
            connection = GameServerConnection(conn, self)
            _thread.start_new_thread(connection.ProcessThread, ())
            self.num_of_connected_players += 1
            self.db_client.SetActivePlayersOnServer(self.address[0], self.address[1], self.num_of_connected_players)
            print(CONNECTED_MESSAGE, addr)

    def ProcessGameObjects(self):
        while True:
            time.sleep(1 / TICK_RATE)
            self.action_handler.ProcessGameObjects()

    def QuitServer(self):
        self.soc.close()
        self.db_client.SetServerOffline(self.db_client.GetServerId(self.address[0], self.address[1]))
        self.db_client.SetActivePlayersOnServer(self.address[0], self.address[1], 0)
        self.db_client.Close()
        sys.exit(0)

    def QuitInput(self):
        exit_string = input()
        if exit_string == QUIT_SERVER_STRING:
            self.QuitServer()
