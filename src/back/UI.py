"""File contains in-game UI class"""

import pygame
import pygame_gui
import src.front.Menus
from src.back.Config import *


class Ui:
    def __init__(self):
        """initialize in-game user interface"""

        self.manager = pygame_gui.UIManager(SIZE_OF_DISPLAY)
        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(PLACE_OF_SETTINGS_BUTTON, SIZE_OF_SETTINGS_BUTTON),
            text=MENU_CONDITION_STRING,
            manager=self.manager)

        self.show_answer_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(PLACE_OF_SHOW_ANSWER_BUTTON, SIZE_OF_SHOW_ANSWER_BUTTON),
            text=ANSWER_BUTTON_STRING,
            manager=self.manager)

    def ProcessEvents(self, event, mappa):
        """this function processing events for UI"""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.menu_button:

                src.front.Menus.Menu.InGameMenu()
            if event.ui_element == self.show_answer_button:
                mappa.ShowAnswer()

        self.manager.process_events(event)

    def Blit(self, time_delta, screen):
        """function for blit UI on screen"""

        self.manager.draw_ui(screen)
        self.manager.update(time_delta)
