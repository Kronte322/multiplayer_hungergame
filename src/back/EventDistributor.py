"""File contains class that process all events"""

import pygame
import src.front.Menus
import src.back.Config
from src.back.Config import *
from abc import ABC, abstractmethod


class EventDistributor(ABC):
    @abstractmethod
    def ProcessEvents(self):
        pass


class KeyboardEventDistributor(EventDistributor, ABC):
    def __init__(self):
        self.pressed_keys = None

    def Update(self):
        self.pressed_keys = pygame.key.get_pressed()

    def Foo(self):
        pass


class PlayerKeyboardEventDistributor(KeyboardEventDistributor):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.set_with_bindings = {pygame.K_a: self.controller.MovePlayerLeft,
                                  pygame.K_d: self.controller.MovePlayerRight, pygame.K_w: self.controller.MovePlayerUp,
                                  pygame.K_s: self.controller.MovePlayerDown}

    def ProcessEvents(self):
        self.Update()
        for key in self.set_with_bindings.keys():
            if self.pressed_keys[key]:
                self.set_with_bindings[key]()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                src.back.Config.RUNNING = False

