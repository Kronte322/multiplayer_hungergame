from src.back.server_client.Server import GameServer
from src.back.Config import *
from src.back.server_client.DBclient import *

db_con = DBConnection()
address_of_the_server = db_con.GetAddressesOfOfflineServers()[0]

server = GameServer(address_of_the_server, SIZE_OF_MAP)
server.StartServer()
