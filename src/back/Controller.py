class Controller:
    def __init__(self, messenger, user, display):
        self.messanger = messenger
        self.user = user
        self.display = display

    def GetUser(self):
        return self.user

    def GetDisplay(self):
        return self.display

    def MovePlayerLeft(self):
        self.messanger.SendMovePlayerLeftOnTheServer()

    def MovePlayerRight(self):
        self.messanger.SendMovePlayerRightOnTheServer()

    def MovePlayerUp(self):
        self.messanger.SendMovePlayerUpOnTheServer()

    def MovePlayerDown(self):
        self.messanger.SendMovePlayerDownOnTheServer()

    def Leave(self):
        self.messanger.SendLeaveMessage()

    def Attack(self, side):
        self.messanger.SendAddAttackMessage(side)

    def Respawn(self):
        self.messanger.SendInitPlayerOnServerMessage()
