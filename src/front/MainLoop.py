"""File contains main game loop"""

import sys
import pygame
import src.back.Config
from src.back.UI import Ui
from src.back.Config import *
from src.back import Map
from src.back import Player
from src.back.EventDistributor import EventDistributor


def ProcessingLoop(screen):
    """this function performs main game loop"""

    # over 30 row but its main loop ().()
    sys.setrecursionlimit(DEEP_OF_RECURSION)

    if src.back.Config.DIFFICULTY == 5:
        src.back.Config.SIZE_OF_MAP = SET_WITH_SIZES[3][1]

    mappa = None
    player = None

    if src.back.Config.MAPPA is None:
        mappa = Map.Map()
        player = Player.Player()
        mappa.SpawnPosition()
        src.back.Config.MAPPA = mappa
        src.back.Config.PLAYER = player

    else:
        mappa = src.back.Config.MAPPA
        player = src.back.Config.PLAYER

    ui = Ui()
    event_distributor = EventDistributor(player, mappa, ui)

    clock = pygame.time.Clock()

    while src.back.Config.RUNNING:
        time_delta = clock.tick(FRAMES_PER_SEC)

        event_distributor.ProcessEvents()
        event_distributor.ProcessKeys()

        screen.fill(COLOR_FOR_BACKGROUND)

        mappa.SetCurrentRoom(player.GetPosition())
        mappa.Render(screen)

        player.Render(screen)

        ui.Blit(time_delta, screen=screen)

        pygame.display.flip()

    pygame.quit()
