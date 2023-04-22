from src.back.server_client.Server import GameServer
from src.back.server_client.ServerConfig import *

game_server_port = int(input())

address_of_the_lobby_server = (LOBBY_FOR_SERVERS_IP_ADDRESS, LOBBY_FOR_SERVERS_PORT)
address_of_the_server = (GAME_SERVER_IP_ADDRESS, game_server_port)

server = GameServer(address_of_the_server, address_of_the_lobby_server)
