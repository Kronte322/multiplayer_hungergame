"""File contains in-game UI class"""

import pygame
import pygame_gui
from src.back.Config import *


class Ui:
    def __init__(self):
        """initialize in-game user interface"""

        self.manager = pygame_gui.UIManager(SIZE_OF_DISPLAY)
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(PLACE_OF_RESTART_BUTTON, SIZE_OF_RESTART_BUTTON),
            text=RETRY_CONDITION_STRING,
            manager=self.manager)

    def ProcessEvents(self, event, controller):
        """this function processing events for UI"""

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.restart_button:
                controller.Respawn()

        self.manager.process_events(event)

    def Blit(self, time_delta, screen):
        """function for blit UI on screen"""

        self.manager.update(time_delta)
        self.manager.draw_ui(screen)



