import psycopg2
from src.back.DBconnection.SQLScripts import *
from src.back.server_client.ServerConfig import *
from src.back.DBconnection.DBConfig import *


class DBConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                database=DB_NAME,
                user=DB_USER,
                password=DB_USER_PASSWORD,
                host=DB_IP_ADDRESS,
                port=DB_PORT
            )
        except Exception:
            raise CONNECTION_TO_DB_FAILED_MESSAGE
        self.cursor = self.connection.cursor()

    def Close(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def GetActiveServers(self):
        self.cursor.execute(GET_ACTIVE_SERVERS_SQL_SCRIPT)
        return self.cursor.fetchall()

    def GetAllServers(self):
        self.cursor.execute(GET_ALL_SERVERS_SQL_SCRIPT)
        return self.cursor.fetchall()

    def GetRanks(self):
        self.cursor.execute(GET_ALL_RANKS_SQL_SCRIPT)
        return self.cursor.fetchall()

    def SetServerOnline(self, server_id):
        self.cursor.execute(SET_SERVER_ONLINE(server_id))
        self.connection.commit()

    def SetServerOffline(self, server_id):
        self.cursor.execute(SET_SERVER_OFFLINE(server_id))
        self.connection.commit()

    def GetServerId(self, ip_address, port):
        self.cursor.execute(GET_SERVER_ID(ip_address, port))
        return self.cursor.fetchall()[0][0]

    def SetGameToOnlineServer(self, ip_address, port, game_id):
        self.cursor.execute(SET_GAME_TO_ONLINE_SERVER(ip_address, port, game_id))
        self.connection.commit()

    def GetOfflineServersWithIp(self, ip_address):
        self.cursor.execute(GET_OFFLINE_SERVER_WITH_IP(ip_address))
        return self.cursor.fetchall()

    def GetAddressesOfOfflineServers(self):
        self.cursor.execute(GET_ADDRESSES_OF_OFFLINE_SERVERS)
        return self.cursor.fetchall()

    def SetActivePlayersOnServer(self, ip_address, port, num_of_players):
        self.cursor.execute(SET_ACTiVE_PLAYERS_ON_SERVER(ip_address, port, num_of_players))
        self.connection.commit()

    def GetUserId(self, user_nm, user_password):
        self.cursor.execute(GET_USER_ID(user_nm, user_password))
        return self.cursor.fetchall()[0][0]

    def AddNewUser(self, user_nm, user_password):
        self.cursor.execute(ADD_NEW_USER(user_nm, user_password))
        self.connection.commit()

    def AddNewPlayer(self, user_id, nick_name):
        self.cursor.execute(ADD_NEW_PLAYER(user_id, nick_name))
        self.connection.commit()

    def GetUserNickName(self, user_id):
        self.cursor.execute(GET_NICKNAME(user_id))
        return self.cursor.fetchall()[0][0]
