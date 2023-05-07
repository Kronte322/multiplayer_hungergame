from src.back.DBconnection.DBclient import *


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.db_con = DBConnection()

    def GetNickName(self):
        return self.db_con.GetUserNickName(self.user_id)

    def GetUserId(self):
        return self.user_id
