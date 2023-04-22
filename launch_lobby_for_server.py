from src.back.server_client.Server import LobbyForServers
from src.back.server_client.ServerConfig import *

address_of_the_server = (LOBBY_FOR_SERVERS_IP_ADDRESS, LOBBY_FOR_SERVERS_PORT)

server = LobbyForServers(address_of_the_server)
server.StartServer()
