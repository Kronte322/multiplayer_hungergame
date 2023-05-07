from src.back.server_client.User import *
import src.back.Game as Game
import src.front.Menus as Menus
from src.back.Config import *


class LogInProcess:
    def __init__(self, display):
        self.display = display
        self.user_nm = None
        self.user_password = None
        self.user_id = None
        self.db_con = DBConnection()
        self.menu = Menus.LogInMenu(display, self)
        self.menu.ProcessMenu()

    def LogIn(self):
        try:
            self.user_id = self.db_con.GetUserId(self.user_nm, self.user_password)
            if self.user_id is None:
                raise WRONG_LOG_IN
            if self.menu.IsThereIncorrectInputInscription():
                self.menu.RemoveAnIncorrectInputInscription()
            self.MoveToLobbyProcess()
        except Exception as e:
            print(e)
            if self.menu.IsThereIncorrectInputInscription():
                self.menu.RemoveAnIncorrectInputInscription()
            self.menu.AddAnIncorrectInputInscription()

    def SetUserName(self, user_nm):
        self.user_nm = user_nm

    def SetUserPassword(self, password):
        self.user_password = password

    def MoveToOnStartProcess(self):
        self.db_con.Close()
        self.menu.Close()
        OnStartProcess(self.display)

    def MoveToLobbyProcess(self):
        self.db_con.Close()
        self.menu.Close()
        LobbyProcess(self.display, User(self.user_id))


class OnStartProcess:
    def __init__(self, display):
        self.display = display
        self.menu = Menus.StartMenu(self.display, self)
        self.menu.ProcessMenu()

    def MoveToLogInProcess(self):
        self.menu.Close()
        LogInProcess(self.display)

    def MoveToRegisterProcess(self):
        self.menu.Close()
        RegisterProcess(self.display)


class RegisterProcess:
    def __init__(self, display):
        self.display = display
        self.db_con = DBConnection()
        self.user_nm = None
        self.user_password = None
        self.user_nick_name = None
        self.country = None
        self.city = None
        self.menu = Menus.RegisterUserMenu(self.display, self)
        self.menu.ProcessMenu()

    def Register(self):
        try:
            self.db_con.AddNewUser(self.user_nm, self.user_password)
            self.db_con.AddNewPlayer(self.db_con.GetUserId(self.user_nm, self.user_password), self.user_nick_name)
            if self.menu.IsThereIncorrectInputInscription():
                self.menu.RemoveAnIncorrectInputInscription()
            self.MoveToOnStartProcess()
        except Exception as e:
            print(e)
            if self.menu.IsThereIncorrectInputInscription():
                self.menu.RemoveAnIncorrectInputInscription()
            self.menu.AddAnIncorrectInputInscription()

    def SetUserName(self, user_nm):
        self.user_nm = user_nm

    def SetUserPassword(self, password):
        self.user_password = password

    def SetUserNickName(self, user_nick):
        self.user_nick_name = user_nick

    def SetCountryName(self, user_nm):
        self.user_nm = user_nm

    def MoveToOnStartProcess(self):
        self.menu.Close()
        self.db_con.Close()
        OnStartProcess(self.display)

    def SetCityName(self, city):
        self.city = city


class LobbyProcess:
    def __init__(self, display, user):
        self.display = display
        self.user = user
        self.db_con = DBConnection()
        self.menu = Menus.LobbyMenu(self.display, self)
        self.menu.ProcessMenu()

    def MoveToProfileProcess(self):
        pass

    def GetUser(self):
        return self.user

    def MoveToServerSelectionProcess(self):
        self.menu.Close()
        self.db_con.Close()
        ServerSelectionProcess(self.display, self.user)

    def MoveToOnStartProcess(self):
        self.menu.Close()
        self.db_con.Close()
        OnStartProcess(self.display)


class ServerSelectionProcess:
    def __init__(self, display, user):
        self.display = display
        self.user = user
        self.db_con = DBConnection()
        self.server_address = None
        self.character = Knight
        self.menu = Menus.ServerSelectionMenu(self.display, self)
        self.menu.ProcessMenu()

    def GetActiveServers(self):
        test = self.db_con.GetActiveServers()
        return self.db_con.GetActiveServers()

    def SetServerAddress(self, address):
        self.server_address = address

    def MoveToGameProcess(self):
        if self.server_address is None:
            if self.menu.IsThereIncorrectInputInscription():
                self.menu.RemoveAnIncorrectInputInscription()
            self.menu.AddAnIncorrectInputInscription()
        else:
            pass

    def MoveToLobbyProcess(self):
        self.menu.Close()
        self.db_con.Close()
        LobbyProcess(self.display, self.user)

    def LaunchGameSession(self):
        self.menu.Close()
        self.db_con.Close()
        Game.Game.StartGameSession(self.display, self.user, self.character, self.server_address)

    def SetCharacter(self, character):
        self.character = character
