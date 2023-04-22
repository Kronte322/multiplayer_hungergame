"""File contains initialization of the game"""

import pygame
from src.front.Menus import MenuUI
from src.back.Config import *
from src.back.Window import Window
from src.back.server_client import Client
from src.back.server_client.ServerConfig import *
import sys


class Game:
    """this class for start the game"""

    def __init__(self):
        """initialization of the object"""
        self.window = Window()
        self.user = Client.UserClient((LOBBY_FOR_USERS_IP_ADDRESS, LOBBY_FOR_USERS_PORT))
        self.game_server_address = None

    def StartTheGame(self):
        MenuUI.ProcessingStartMenu(self.window.GetDisplay(), self)

    def StartGameSession(self):

        sys.setrecursionlimit(DEEP_OF_RECURSION)

    def GetGameServerAddress(self):
        return self.game_server_address

    def SetGameServerAddress(self, address):
        self.game_server_address = address

    def GetUser(self):
        return self.user
