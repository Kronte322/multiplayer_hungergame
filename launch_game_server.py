"""File contains launch of game server"""

import socket

import src.back.Config as Config
import src.back.DBconnection.DBclient as DBclient
from src.back.server_client.Server import GameServer


def GetIpAddress():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


db_con = DBclient.DBConnection()
address_of_the_server = db_con.GetOfflineServersWithIp(GetIpAddress())[0]

server = GameServer(address_of_the_server, Config.SIZE_OF_MAP)
server.StartServer()
