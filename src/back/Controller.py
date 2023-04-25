class Controller:
    def __init__(self, messenger):
        self.messanger = messenger

    def MovePlayerLeft(self):
        self.messanger.SendMovePlayerLeftOnTheServer()

    def MovePlayerRight(self):
        self.messanger.SendMovePlayerRightOnTheServer()

    def MovePlayerUp(self):
        self.messanger.SendMovePlayerUpOnTheServer()

    def MovePlayerDown(self):
        self.messanger.SendMovePlayerDownOnTheServer()
