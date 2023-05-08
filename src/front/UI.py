"""File contains in-game UI class"""

import pygame
import pygame_gui

import src.back.Config as Config


class Ui:
    def __init__(self):
        """initialize in-game user interface"""

        self.manager = pygame_gui.UIManager(Config.SIZE_OF_DISPLAY)
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(Config.PLACE_OF_RESTART_BUTTON, Config.SIZE_OF_RESTART_BUTTON),
            text=Config.RETRY_CONDITION_STRING,
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
