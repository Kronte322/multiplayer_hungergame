"""File contains class that process all events"""

import pygame
import src.front.Menus
import src.back.Config
from src.back.Config import *
from abc import ABC, abstractmethod
import pygame_gui


class Event(ABC):
    @abstractmethod
    def ProcessEvent(self):
        pass


class WindowEvent(Event):
    def __init__(self, event):
        self.event = event

    @abstractmethod
    def ProcessEvent(self):
        pass

    def UpdateEvent(self, event):
        self.event = event


class UIWindowEvent(WindowEvent):
    def __init__(self, event, ui):
        super().__init__(event)
        self.ui = ui

    @abstractmethod
    def ProcessEvent(self):
        pass


class QuitGameEvent(WindowEvent):
    def __init__(self, event):
        super().__init__(event)

    def ProcessEvent(self):
        if self.event.type == pygame.QUIT:
            src.back.Config.RUNNING = False


class UIWindowMapEvent(UIWindowEvent):
    def __init__(self, event, ui, mappa):
        super().__init__(event, ui)
        self.mappa = mappa

    @abstractmethod
    def ProcessEvent(self):
        pass


class ShowAnswerEvent(UIWindowMapEvent):
    def __init__(self, event, ui, mappa):
        super().__init__(event, ui, mappa)

    def ProcessEvent(self):
        if self.event.type == pygame_gui.UI_BUTTON_PRESSED:
            if self.event.ui_element == self.ui.show_answer_button:
                self.mappa.ShowAnswer()


class OpenInGameMenuEvent(UIWindowEvent):
    def __init__(self, event, ui):
        super().__init__(event, ui)

    def ProcessEvent(self):
        if self.event.type == pygame_gui.UI_BUTTON_PRESSED:
            if self.event.ui_element == self.ui.menu_button:
                src.front.Menus.MenuUI.InGameMenu()


class KeyboardEvent(Event):
    def __init__(self, keys):
        self.keys = keys

    @abstractmethod
    def ProcessEvent(self):
        pass

    def UpdatePressedKeys(self, keys):
        self.keys = keys


class PlayerKeyboardEvent(KeyboardEvent):
    def __init__(self, keys, player):
        super().__init__(keys)
        self.player = player

    @abstractmethod
    def ProcessEvent(self):
        pass


class MapPlayerKeyboardEvent(PlayerKeyboardEvent):
    def __init__(self, keys, player, mappa):
        super().__init__(keys, player)
        self.mappa = mappa

    @abstractmethod
    def ProcessEvent(self):
        pass

    def UpdateMap(self, mappa):
        self.mappa = mappa


class PlayerMoveLeftEvent(MapPlayerKeyboardEvent):
    def __init__(self, keys, player, mappa):
        super().__init__(keys, player, mappa)

    def ProcessEvent(self):
        if self.keys[pygame.K_a]:
            self.player.MoveLeft(self.mappa)


class PlayerMoveRightEvent(MapPlayerKeyboardEvent):
    def __init__(self, keys, player, mappa):
        super().__init__(keys, player, mappa)

    def ProcessEvent(self):
        if self.keys[pygame.K_d]:
            self.player.MoveRight(self.mappa)


class PlayerMoveUpEvent(MapPlayerKeyboardEvent):
    def __init__(self, keys, player, mappa):
        super().__init__(keys, player, mappa)

    def ProcessEvent(self):
        if self.keys[pygame.K_w]:
            self.player.MoveUp(self.mappa)


class PlayerMoveDownEvent(MapPlayerKeyboardEvent):
    def __init__(self, keys, player, mappa):
        super().__init__(keys, player, mappa)

    def ProcessEvent(self):
        if self.keys[pygame.K_s]:
            self.player.MoveDown(self.mappa)


class EventDistributor(ABC):
    @abstractmethod
    def ProcessEvents(self, list_with_events):
        pass


class UIEventDistributor(EventDistributor):
    def __init__(self, ui):
        self.ui = ui

    def ProcessEvents(self, list_with_events):
        for event in list_with_events:
            event.ProcessEvent()


class MapUIEventDistributor(UIEventDistributor):
    def __init__(self, ui, mappa):
        super().__init__(ui)
        self.mappa = mappa

    def ProcessEvents(self, list_with_events):
        for event in list_with_events:
            event.ProcessEvent(self.mappa)


class PlayerEventDistributor(EventDistributor):
    def __init__(self, player):
        self.player = player

    def ProcessEvents(self, list_with_events):
        for event in list_with_events:
            event.ProcessEvent()
        pass


class MapPlayerEventDistributor(PlayerEventDistributor):
    def __init__(self, player, mappa):
        super().__init__(player)
        self.mappa = mappa

    def ProcessEvents(self, list_with_events):
        for event in list_with_events:
            event.ProcessEvent(self.mappa)

# class EventDistributor:
#     """class that control all events"""
#
#     def __init__(self, player, mappa, ui):
#         """initialization of the class"""
#
#         self.player = player
#         self.mappa = mappa
#         self.ui = ui
#
#     def ProcessKeys(self):
#         """this function processing keyboards events"""
#
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_ESCAPE]:
#             src.back.Config.STATE = IN_GAME_MENU_STATE
#             src.front.Menus.MenuUI.InGameMenu()
#         if keys[pygame.K_w]:
#             self.player.MoveUp(self.mappa)
#         if keys[pygame.K_a]:
#             self.player.MoveLeft(self.mappa)
#         if keys[pygame.K_s]:
#             self.player.MoveDown(self.mappa)
#         if keys[pygame.K_d]:
#             self.player.MoveRight(self.mappa)
#
#     def ProcessEvents(self):
#         """this function window events"""
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 src.back.Config.RUNNING = False
#             self.ui.ProcessEvents(event, self.mappa)
