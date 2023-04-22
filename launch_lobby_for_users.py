from src.back.server_client.Server import LobbyForUsers
from src.back.server_client.ServerConfig import *

address_of_the_lobby_server = (LOBBY_FOR_SERVERS_IP_ADDRESS, LOBBY_FOR_SERVERS_PORT)
address_of_the_lobby_users = (LOBBY_FOR_USERS_IP_ADDRESS, LOBBY_FOR_USERS_PORT)

server = LobbyForUsers(address_of_the_lobby_users, address_of_the_lobby_server)
server.StartServer()
