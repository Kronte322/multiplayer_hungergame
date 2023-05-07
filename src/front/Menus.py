"""File contains menu"""
from abc import ABC

import pygame_menu

import src.back.Config as Config


class Menu(ABC):
    """abstract class for menus"""

    def __init__(self, display):
        self.display = display
        self.menu = None

    def ProcessMenu(self):
        """this method process menu"""

        self.menu.mainloop(self.display)

    def Close(self):
        """this method close the menu"""

        self.menu.close()

    @staticmethod
    def ReturnOnlyValue(key, value):
        """this method returns only value for callback"""

        return value


class StartMenu(Menu):
    """class for start menu"""

    def __init__(self, display, start_process):
        super().__init__(display)
        self.menu = pygame_menu.Menu(Config.WELCOME_CONDITION_STRING, Config.SIZE_OF_MENUS[0], Config.SIZE_OF_MENUS[1],
                                     theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.button(Config.LOG_IN_STRING, start_process.MoveToLogInProcess)
        self.menu.add.button(Config.REGISTRATION_STRING, start_process.MoveToRegisterProcess)
        self.menu.add.button(Config.QUIT_CONDITION_STRING, pygame_menu.events.EXIT)


class LogInMenu(Menu):
    """class for log in menu"""

    def __init__(self, display, log_in_process):
        super().__init__(display)
        self.menu = pygame_menu.Menu(Config.WELCOME_CONDITION_STRING, Config.SIZE_OF_MENUS[0], Config.SIZE_OF_MENUS[1],
                                     theme=pygame_menu.themes.THEME_BLUE)

        self.menu.add.text_input(Config.USER_NM_INPUT, onchange=log_in_process.SetUserName)
        self.menu.add.text_input(Config.PASSWORD_INPUT, onchange=log_in_process.SetUserPassword, password=True)
        self.menu.add.button(Config.LOG_IN_STRING, log_in_process.LogIn)
        self.menu.add.button(Config.BACK_CONDITION_STRING, log_in_process.MoveToOnStartProcess)
        self.label = None

    def AddAnIncorrectInputInscription(self):
        """this method adds message with incorrect input"""

        self.label = self.menu.add.label(Config.WRONG_LOG_IN)

    def RemoveAnIncorrectInputInscription(self):
        """this method removes message with incorrect input"""

        try:
            self.menu.remove_widget(self.label)
        except:
            pass

    def IsThereIncorrectInputInscription(self):
        """this method checks if there message with incorrect input"""

        return self.label is not None


class RegisterUserMenu(Menu):
    """class for register menu"""

    def __init__(self, display, register_process):
        super().__init__(display)
        self.menu = pygame_menu.Menu(Config.WELCOME_CONDITION_STRING, Config.SIZE_OF_MENUS[0], Config.SIZE_OF_MENUS[1],
                                     theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.text_input(Config.USER_NM_INPUT, onchange=register_process.SetUserName)
        self.menu.add.text_input(Config.NICK_NAME_INPUT, onchange=register_process.SetUserNickName)
        self.menu.add.text_input(Config.PASSWORD_INPUT, onchange=register_process.SetUserPassword, password=True)

        self.menu.add.button(Config.REGISTRATION_STRING, register_process.Register)
        self.menu.add.button(Config.BACK_CONDITION_STRING, register_process.MoveToOnStartProcess)
        self.label = None

    def AddAnIncorrectInputInscription(self):
        self.label = self.menu.add.label(Config.WRONG_LOG_IN)

    def RemoveAnIncorrectInputInscription(self):
        self.menu.remove_widget(self.label)

    def IsThereIncorrectInputInscription(self):
        return self.label is not None


class LobbyMenu(Menu):
    """class for lobby menu"""

    def __init__(self, display, lobby_process):
        super().__init__(display)
        self.menu = pygame_menu.Menu(Config.WELCOME_CONDITION_STRING, Config.SIZE_OF_MENUS[0], Config.SIZE_OF_MENUS[1],
                                     theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.button(lobby_process.GetUser().GetNickName(), lobby_process.MoveToProfileProcess)
        self.menu.add.button(Config.PLAY_CONDITION_STRING, lobby_process.MoveToServerSelectionProcess)
        self.menu.add.button(Config.BACK_CONDITION_STRING, lobby_process.MoveToOnStartProcess)
        self.menu.add.button(Config.QUIT_CONDITION_STRING, pygame_menu.events.EXIT)


class ServerSelectionMenu(Menu):
    """class for server selection menu"""

    def __init__(self, display, server_selection_process):
        super().__init__(display)
        self.menu = pygame_menu.Menu(Config.WELCOME_CONDITION_STRING, Config.SIZE_OF_MENUS[0], Config.SIZE_OF_MENUS[1],
                                     theme=pygame_menu.themes.THEME_BLUE)

        def SetServerAddress(key, value):
            server_selection_process.SetServerAddress(value)

        def SetCharacter(key, value):
            server_selection_process.SetCharacter(value)

        selector = self.menu.add.selector(title=Config.PICK_SERVER_STRING,
                                          items=[(str(server[3]) + ' / ' + str(server[2]), (server[0], server[1])) for
                                                 server in server_selection_process.GetActiveServers()] + [
                                                    ('', (0, 0))], onchange=SetServerAddress)
        SetServerAddress(selector.get_items()[0][0], selector.get_items()[0][1])
        self.menu.add.selector(title=Config.CHARACTER_SELECTION_STRING, items=Config.SET_WITH_CHARACTERS,
                               onchange=SetCharacter)
        self.menu.add.button(Config.CONNECT_BUTTON_STRING, server_selection_process.LaunchGameSession)
        self.menu.add.button(Config.BACK_CONDITION_STRING, server_selection_process.MoveToLobbyProcess)
        self.menu.add.button(Config.QUIT_CONDITION_STRING, pygame_menu.events.EXIT)
        self.label = None

    def AddAnIncorrectInputInscription(self):
        self.label = self.menu.add.label(Config.WRONG_SERVER_SELECTION)

    def RemoveAnIncorrectInputInscription(self):
        self.menu.remove_widget(self.label)

    def IsThereIncorrectInputInscription(self):
        return self.label is not None
