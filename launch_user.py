from src.back.server_client.Client import UserClient
from src.back.server_client.ServerConfig import *

address_of_the_server = (LOBBY_FOR_USERS_IP_ADDRESS, LOBBY_FOR_USERS_PORT)

user = UserClient(address_of_the_server)
user.Connect()
