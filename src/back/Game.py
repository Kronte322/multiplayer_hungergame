"""File contains initialization of the game"""
import time

import pygame

import src.back.Config
import src.back.Processes as Processes
import src.back.server_client.ServerConfig as ServerConfig
import src.front.EventDistributor as EventDistributor
from src.back.Controller import Controller
from src.back.Map import Map
from src.back.server_client.Client import PlayerClient
from src.front.Render import Render
from src.front.UI import Ui
from src.front.Window import Window


class Game:
    """this class represents application stages"""

    @staticmethod
    def StartTheGame():
        """this method starts the game"""

        window = Window()
        Processes.OnStartProcess(window.GetDisplay())

    @staticmethod
    def StartGameSession(display, user, character, server_address):
        """this method starts game session"""

        client = None
        try:
            client = PlayerClient(server_address, user, character)
        except:
            EventDistributor.ServerSelectionProcess(display, user)

        while True:
            time.sleep(1 / ServerConfig.TICK_RATE)
            if client.GetSeedOfGeneration() is not None:
                mappa = Map(client.GetSeedOfGeneration())
                mappa.SetCurrentRooms()
                break
        render = Render(display, mappa, client)
        controller = Controller(client.GetConnection().GetMessenger(), user, display)
        keyboard_distributor = EventDistributor.PlayerKeyboardEventDistributor(controller)
        mouse_distributor = EventDistributor.MouseEventDistributor(controller)
        ui = Ui()
        window_distributor = EventDistributor.WindowEventDistributor(controller, ui)
        clock = pygame.time.Clock()

        while src.back.Config.RUNNING:
            time_delta = clock.tick(src.back.Config.FRAMES_PER_SEC)
            is_dead = client.GetPlayers()[client.GetUser().GetUserId()].IsDead()
            window_distributor.ProcessEvents(is_dead)
            keyboard_distributor.ProcessEvents()
            mouse_distributor.ProcessEvents()
            render.Draw()
            if is_dead:
                ui.Blit(time_delta, display)
            pygame.display.flip()
