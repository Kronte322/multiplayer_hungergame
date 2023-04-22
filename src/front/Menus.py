"""File contains menu"""
import pygame_menu
from src.back.Config import *
import src.back.Config
import src.front.MainLoop


class MenuUI:
    """class that contains all menus UI"""

    @staticmethod
    def SetCharacter(key, value):
        """function for character selection"""

        src.back.Config.CHARACTER = value

    @staticmethod
    def ReturnOnlyValue(key, value):
        return value

    @staticmethod
    def ProcessingStartMenu(display, game):
        """this function perform start menu"""
        src.back.Config.STATE = START_MENU_STATE
        start_menu = pygame_menu.Menu(WELCOME_CONDITION_STRING, SIZE_OF_MENUS[0], SIZE_OF_MENUS[1],
                                      theme=pygame_menu.themes.THEME_BLUE)
        start_menu.add.selector(CHARACTER_SELECTION_STRING, SET_WITH_CHARACTERS, onchange=MenuUI.SetCharacter)

        selector = start_menu.add.selector(title=PICK_SERVER_STRING,
                                           items=[(str(server_address), server_address) for server_address in
                                                  game.GetUser().GetActiveServers()] + [('0', 0)],
                                           onchange=game.SetGameServerAddress)
        selector.set_onchange(MenuUI.ReturnOnlyValue)

        def OnUpdateFunc(selected, widget, menu):
            selector.update_items([(str(server_address), server_address) for server_address in
                                   game.GetUser().GetActiveServers()] + [('0', 0)])

        selector.set_onselect(OnUpdateFunc)
        start_menu.add.button(CONNECT_BUTTON_STRING, game.StartGameSession)
        start_menu.mainloop(display)

    @staticmethod
    def ProcessingEndMenu(display):
        """this function perform end menu"""

        src.back.Config.STATE = END_GAME_MENU_STATE
        end_menu = pygame_menu.Menu(WIN_CONDITION_STRING, SIZE_OF_MENUS[0], SIZE_OF_MENUS[1],
                                    theme=pygame_menu.themes.THEME_BLUE)
        end_menu.add.button(QUIT_CONDITION_STRING, pygame_menu.events.EXIT)
        end_menu.mainloop(display)

    @staticmethod
    def SettingsMenu(display):
        """this function perform settings menu"""

        settings_menu = pygame_menu.Menu(SETTINGS_CONDITION_STRING, SIZE_OF_MENUS[0], SIZE_OF_MENUS[1],
                                         theme=pygame_menu.themes.THEME_BLUE)
        settings_menu.add.button(BACK_CONDITION_STRING, MenuUI.ProcessingStartMenu, display)
        settings_menu.mainloop(display)

    @staticmethod
    def InGameMenu(display):
        """this function perform in-game menu"""

        src.back.Config.STATE = IN_GAME_MENU_STATE

        in_game_menu = pygame_menu.Menu(MENU_CONDITION_STRING, SIZE_OF_MENUS[0], SIZE_OF_MENUS[1],
                                        theme=pygame_menu.themes.THEME_BLUE)

        def MyDisable():
            src.back.Config.STATE = IN_GAME_STATE
            in_game_menu.disable()

        in_game_menu.add.button(RESUME_CONDITION_STRING, MyDisable)
        in_game_menu.add.button(QUIT_CONDITION_STRING, pygame_menu.events.EXIT)
        in_game_menu.mainloop(display)
