import sqlite3


class GameHistory:
    def __init__(self, tablename="GameHistory", game_id="GameID", user_1="Player1", user_2="Player2",
                 user_win="Winner"):
        self.__tablename = tablename
        self.__game_id =game_id
        self.__user_1 = user_1
        self.__user_2 = user_2
        self.__user_win = user_win

        conn = sqlite3.connect('GameHistory.db')
        print("Opened database successfully")
        str1 = "CREATE TABLE IF NOT EXISTS " + self.__tablename + "(" + self.__game_id + " " + "INTEGER PRIMARY KEY AUTOINCREMENT ,"
        str1 += " " + self.__user_1 + " TEXT    NOT NULL ,"
        str1 += " " + self.__user_2 + " TEXT    NOT NULL ,"
        str1 += " " + self.__user_win + " TEXT    NOT NULL)"
        conn.execute(str1)
        print("Table created successfully")
        conn.commit()
        conn.close()

    def insert_players(self, player1, player2, winner):
        try:
            conn = sqlite3.connect('GameHistory.db')
            print("Opened database successfully")  # check if worked
            str_insert = f"INSERT INTO {self.__tablename} ({self.__user_1}, {self.__user_2}, {self.__user_win})" \
                         f" VALUES ('{player1}', '{player2}', {winner}')"
            print(str_insert)
            conn.execute(str_insert)
            conn.commit()
            conn.close()
            print("Record created successfully")
            return True
        except:
            print("Failed to insert game")
            return False

    def update_wins(self):
        pass
