"""File contains class that process all events"""

import pygame
import src.front.Menus
import src.back.Config
from src.back.Config import *
from abc import ABC, abstractmethod
from src.back.server_client.Processes import ServerSelectionProcess
import math


class EventDistributor(ABC):
    def __init__(self, controller):
        self.controller = controller

    def LeaveFromGameSession(self):
        self.controller.Leave()
        ServerSelectionProcess(self.controller.GetDisplay(), self.controller.GetUser())


class KeyboardEventDistributor(EventDistributor, ABC):
    def __init__(self, controller):
        super().__init__(controller)
        self.pressed_keys = None

    def Update(self):
        self.pressed_keys = pygame.key.get_pressed()


class PlayerKeyboardEventDistributor(KeyboardEventDistributor):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.set_with_bindings = {pygame.K_a: self.controller.MovePlayerLeft,
                                  pygame.K_d: self.controller.MovePlayerRight, pygame.K_w: self.controller.MovePlayerUp,
                                  pygame.K_s: self.controller.MovePlayerDown,
                                  pygame.K_ESCAPE: self.LeaveFromGameSession}

    def ProcessEvents(self):
        self.Update()
        for key in self.set_with_bindings.keys():
            if self.pressed_keys[key]:
                self.set_with_bindings[key]()


class WindowEventDistributor(EventDistributor):
    def __init__(self, controller, ui):
        super().__init__(controller)
        self.events = None
        self.controller = controller
        self.ui = ui

    def Update(self):
        self.events = pygame.event.get()

    def ProcessEvents(self, flag=False):
        self.Update()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.LeaveFromGameSession()
            if flag:
                self.ui.ProcessEvents(event, self.controller)


class MouseEventDistributor(EventDistributor):
    def __init__(self, controller):
        super().__init__(controller)

    def ProcessEvents(self):
        if pygame.mouse.get_pressed()[0]:
            self.controller.Attack(MouseEventDistributor.GetSideOfAttack())

    @staticmethod
    def GetSideOfAttack():
        side = src.back.Config.RIGHT
        position = pygame.mouse.get_pos()
        player_position = (src.back.Config.SPAWN_POSITION[0] + src.back.Config.KNIGHT_SIZE // 2,
                           src.back.Config.SPAWN_POSITION[1] + src.back.Config.KNIGHT_SIZE // 2)
        if position[0] - player_position[0] == 0:
            if position[1] - player_position[1] > 0:
                return UP
            return DOWN
        tan = (position[1] - player_position[1]) / (position[0] - player_position[0])

        if position[0] - player_position[0] >= 0:
            if tan > 1:
                side = src.back.Config.DOWN
            elif tan < -1:
                side = src.back.Config.UP
            else:
                side = src.back.Config.RIGHT
        else:
            if tan > 1:
                side = src.back.Config.UP
            elif tan < -1:
                side = src.back.Config.DOWN
            else:
                side = src.back.Config.LEFT
        return side
