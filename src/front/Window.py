import pygame

import src.back.Config as Config


class Window:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(Config.CAPTION)
        self.display = pygame.display.set_mode(Config.SIZE_OF_DISPLAY)

    def GetDisplay(self):
        return self.display
