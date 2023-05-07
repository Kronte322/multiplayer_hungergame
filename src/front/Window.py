import pygame
from src.back.Config import *


class Window:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(CAPTION)
        self.display = pygame.display.set_mode(SIZE_OF_DISPLAY)

    def GetDisplay(self):
        return self.display
