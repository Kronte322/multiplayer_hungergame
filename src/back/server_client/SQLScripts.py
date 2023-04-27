GET_ACTIVE_SERVERS_SQL_SCRIPT = 'SELECT ip_address, port FROM st.server WHERE state = \'online\''
GET_ALL_SERVERS_SQL_SCRIPT = 'SELECT * FROM st.server'
GET_ADDRESSES_OF_OFFLINE_SERVERS = 'SELECT ip_address, port FROM st.server WHERE state = \'offline\''
GET_ALL_RANKS_SQL_SCRIPT = 'SELECT * FROM st.rank'


def SET_SERVER_ONLINE(server_id):
    return 'UPDATE st.server SET state =\'online\' WHERE server_id = ' + str(server_id) + ';'


def GET_OFFLINE_SERVER_WITH_IP(ip_address):
    return 'SELECT ip_address, port FROM st.server WHERE ip_address = \'' + ip_address + '\' AND state = \'offline\';'


def SET_SERVER_OFFLINE(server_id):
    return 'UPDATE st.server SET state =\'offline\' WHERE server_id = ' + str(server_id) + ';'


def SET_ACTiVE_PLAYERS_ON_SERVER(ip_address, port, num_of_players):
    return 'UPDATE st.server SET players_cnt =' + str(num_of_players) + ' WHERE ip_address = ' + str(
        ip_address) + ', port = ' + str(port)


def GET_SERVER_ID(ip_address, port):
    return 'SELECT server_id FROM st.server WHERE ip_address = \'' + ip_address + '\' AND port = ' + str(port) + ';'


def SET_GAME_TO_ONLINE_SERVER(ip_address, port, game_id):
    return 'UPDATE st.server SET game_id = ' + str(game_id) + ' WHERE ip_address = ' + str(
        ip_address) + ', port = ' + str(port)


def GET_USER_ID(user_nm, user_password):
    test = 'SELECT user_id FROM st.user WHERE email_nm = \'' + user_nm + '\' AND password = \'' + user_password + '\''
    return 'SELECT user_id FROM st.user WHERE email_nm = \'' + user_nm + '\' AND password = \'' + user_password + '\''


def GET_NICKNAME(user_id):
    return 'SELECT nick_nm FROM st.player WHERE user_id = ' + str(user_id) + ';'


def ADD_NEW_USER(user_nm, user_password):
    test = 'INSERT INTO st.user(email_nm, password) VALUES (\'' + user_nm + '\', \'' + user_password + '\');'
    return 'INSERT INTO st.user(email_nm, password) VALUES (\'' + user_nm + '\', \'' + user_password + '\');'


def ADD_NEW_PLAYER(user_id, nick_name):
    test = 'INSERT INTO st.player(user_id, nick_nm) VALUES (\'' + str(user_id) + '\', \'' + nick_name + '\');'
    return 'INSERT INTO st.player(user_id, nick_nm) VALUES (\'' + str(user_id) + '\', \'' + nick_name + '\');'
