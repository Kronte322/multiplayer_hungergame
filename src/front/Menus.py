"""File contains menu"""
import pygame_menu
from src.back.Config import *
from abc import ABC


class Menu(ABC):
    """class that contains all menus UI"""

    def __init__(self, display):
        self.display = display
        self.menu = None

    def ProcessMenu(self):
        self.menu.mainloop(self.display)

    def Close(self):
        self.menu.close()

    @staticmethod
    def ReturnOnlyValue(key, value):
        return value


class StartMenu(Menu):
    def __init__(self, display, start_process):
        super().__init__(display)
        self.menu = pygame_menu.Menu(WELCOME_CONDITION_STRING, SIZE_OF_MENUS[0], SIZE_OF_MENUS[1],
                                     theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.button(LOG_IN_STRING, start_process.MoveToLogInProcess)
        self.menu.add.button(REGISTRATION_STRING, start_process.MoveToRegisterProcess)
        self.menu.add.button(QUIT_CONDITION_STRING, pygame_menu.events.EXIT)


class LogInMenu(Menu):
    def __init__(self, display, log_in_process):
        super().__init__(display)
        self.menu = pygame_menu.Menu(WELCOME_CONDITION_STRING, SIZE_OF_MENUS[0], SIZE_OF_MENUS[1],
                                     theme=pygame_menu.themes.THEME_BLUE)

        self.menu.add.text_input(USER_NM_INPUT, onchange=log_in_process.SetUserName)
        self.menu.add.text_input(PASSWORD_INPUT, onchange=log_in_process.SetUserPassword, password=True)
        self.menu.add.button(LOG_IN_STRING, log_in_process.LogIn)
        self.menu.add.button(BACK_CONDITION_STRING, log_in_process.MoveToOnStartProcess)
        self.label = None

    def AddAnIncorrectInputInscription(self):
        self.label = self.menu.add.label(WRONG_LOG_IN)

    def RemoveAnIncorrectInputInscription(self):
        try:
            self.menu.remove_widget(self.label)
        except:
            pass

    def IsThereIncorrectInputInscription(self):
        return self.label is not None


class RegisterUserMenu(Menu):
    def __init__(self, display, register_process):
        super().__init__(display)
        self.menu = pygame_menu.Menu(WELCOME_CONDITION_STRING, SIZE_OF_MENUS[0], SIZE_OF_MENUS[1],
                                     theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.text_input(USER_NM_INPUT, onchange=register_process.SetUserName)
        self.menu.add.text_input(NICK_NAME_INPUT, onchange=register_process.SetUserNickName)
        self.menu.add.text_input(PASSWORD_INPUT, onchange=register_process.SetUserPassword, password=True)

        self.menu.add.button(REGISTRATION_STRING, register_process.Register)
        self.menu.add.button(BACK_CONDITION_STRING, register_process.MoveToOnStartProcess)
        self.label = None

    def AddAnIncorrectInputInscription(self):
        self.label = self.menu.add.label(WRONG_LOG_IN)

    def RemoveAnIncorrectInputInscription(self):
        self.menu.remove_widget(self.label)

    def IsThereIncorrectInputInscription(self):
        return self.label is not None


class LobbyMenu(Menu):
    def __init__(self, display, lobby_process):
        super().__init__(display)
        self.menu = pygame_menu.Menu(WELCOME_CONDITION_STRING, SIZE_OF_MENUS[0], SIZE_OF_MENUS[1],
                                     theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.button(lobby_process.GetUser().GetNickName(), lobby_process.MoveToProfileProcess)
        self.menu.add.button(PLAY_CONDITION_STRING, lobby_process.MoveToServerSelectionProcess)
        self.menu.add.button(BACK_CONDITION_STRING, lobby_process.MoveToOnStartProcess)
        self.menu.add.button(QUIT_CONDITION_STRING, pygame_menu.events.EXIT)


class ServerSelectionMenu(Menu):
    def __init__(self, display, server_selection_process):
        super().__init__(display)
        self.menu = pygame_menu.Menu(WELCOME_CONDITION_STRING, SIZE_OF_MENUS[0], SIZE_OF_MENUS[1],
                                     theme=pygame_menu.themes.THEME_BLUE)

        def SetServerAddress(key, value):
            server_selection_process.SetServerAddress(value)

        def SetCharacter(key, value):
            server_selection_process.SetCharacter(value)

        selector = self.menu.add.selector(title=PICK_SERVER_STRING,
                                          items=[(str(address), address) for address in
                                                 server_selection_process.GetActiveServers() + [('0', 0)]],
                                          onchange=SetServerAddress)
        SetServerAddress(selector.get_items()[0][0], selector.get_items()[0][1])
        self.menu.add.selector(title=CHARACTER_SELECTION_STRING, items=SET_WITH_CHARACTERS, onchange=SetCharacter)
        self.menu.add.button(CONNECT_BUTTON_STRING, server_selection_process.LaunchGameSession)
        self.menu.add.button(BACK_CONDITION_STRING, server_selection_process.MoveToLobbyProcess)
        self.menu.add.button(QUIT_CONDITION_STRING, pygame_menu.events.EXIT)
        self.label = None

    def AddAnIncorrectInputInscription(self):
        self.label = self.menu.add.label(WRONG_SERVER_SELECTION)

    def RemoveAnIncorrectInputInscription(self):
        self.menu.remove_widget(self.label)

    def IsThereIncorrectInputInscription(self):
        return self.label is not None
