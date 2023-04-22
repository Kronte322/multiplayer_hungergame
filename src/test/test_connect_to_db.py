import psycopg2

con = psycopg2.connect(
    database='postgres',
    user='postgres',
    password='antisocialplayer',
    host='192.168.0.108',
    port='5432'
)

cursor_obj = con.cursor()
print(con.get_dsn_parameters())
cursor_obj.execute("SELECT * FROM pg_stat_activity")
result = cursor_obj.fetchall()
print(result)

cursor_obj.close()
con.close()
