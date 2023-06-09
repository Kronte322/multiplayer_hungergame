"""File contains class that process all events"""
import time
from abc import ABC

import pygame

import src.back.Config
import src.back.Config as Config
import src.front.Menus
from src.back.Processes import ServerSelectionProcess


class EventDistributor(ABC):
    def __init__(self, controller):
        self.controller = controller

    def LeaveFromGameSession(self):
        self.controller.Leave()
        time.sleep(0.1)
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
        position = pygame.mouse.get_pos()
        player_position = (src.back.Config.SPAWN_POSITION[0] + src.back.Config.KNIGHT_SIZE // 2,
                           src.back.Config.SPAWN_POSITION[1] + src.back.Config.KNIGHT_SIZE // 2)
        if position[0] - player_position[0] == 0:
            if position[1] - player_position[1] > 0:
                return Config.UP
            return Config.DOWN
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
