"""File contains initialization of the game"""
import time
import pygame
from src.back.Window import Window
from src.back.server_client.Processes import *
from src.front.Render import Render
from src.back.server_client.Client import PlayerClient
from src.back.Map import Map
from src.back.Controller import Controller
from src.back.EventDistributor import *


class Game:
    """this class for start the game"""

    @staticmethod
    def StartTheGame():
        window = Window()
        OnStartProcess(window.GetDisplay())

    @staticmethod
    def StartGameSession(display, user, character, server_address):
        client = PlayerClient(server_address, user, character)
        while True:
            time.sleep(1 / TICK_RATE)
            if client.GetSeedOfGeneration() is not None:
                mappa = Map(client.GetSeedOfGeneration())
                mappa.SetCurrentRooms()
                break
        render = Render(display, mappa, client)
        controller = Controller(client.GetConnection().GetMessenger())
        keyboard_distributor = PlayerKeyboardEventDistributor(controller)
        clock = pygame.time.Clock()
        while src.back.Config.RUNNING:
            clock.tick(FRAMES_PER_SEC)
            keyboard_distributor.ProcessEvents()
            render.Draw()
