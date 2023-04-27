"""File contains launch of game server"""

import socket
from src.back.server_client.Server import GameServer
from src.back.Config import *
from src.back.server_client.DBclient import *


def GetIpAddress():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


db_con = DBConnection()
address_of_the_server = db_con.GetOfflineServersWithIp(GetIpAddress())[0]

server = GameServer(address_of_the_server, SIZE_OF_MAP)
server.StartServer()
