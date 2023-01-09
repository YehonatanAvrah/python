import sqlite3
# def update - one for every category or a general one; update wins - need to add


class Users:
    def __init__(self, tablename="Users", user_id="ID", email="email", firstname="firstname", lastname="lastname",
                 username="username", password="password", wins='wins'):
        self.__tablename = tablename
        self.__user_id = user_id
        self.__email = email
        self.__firstname = firstname
        self.__lastname = lastname
        self.__username = username
        self.__password = password
        self.__wins = wins

        conn = sqlite3.connect('Users.db')
        print("Opened database successfully")
        str1 = "CREATE TABLE IF NOT EXISTS " + self.__tablename + "(" + self.__user_id + " " + "INTEGER PRIMARY KEY AUTOINCREMENT ,"
        str1 += " " + self.__email + " TEXT    NOT NULL ,"
        str1 += " " + self.__firstname + " TEXT    NOT NULL ,"
        str1 += " " + self.__lastname + " TEXT    NOT NULL ,"
        str1 += " " + self.__username + " TEXT    NOT NULL ,"
        str1 += " " + self.__password + " TEXT    NOT NULL ,"
        str1 += " " + self.__wins + " INTEGER    NOT NULL)"
        conn.execute(str1)
        print("Table created successfully")
        conn.commit()
        conn.close()

    def insert_user(self, email, firstname, lastname, username, password):
        try:
            conn = sqlite3.connect('Users.db')
            print("Opened database successfully")  # check if worked
            str_insert = f"INSERT INTO {self.__tablename} ({self.__email}, {self.__password}, {self.__firstname}," \
                         f" {self.__lastname}, {self.__username}, {self.__wins}) VALUES ('{email}', '{password}'," \
                         f" '{firstname}', '{lastname}', '{username}', '{0}')"
            print(str_insert)
            conn.execute(str_insert)
            conn.commit()
            conn.close()
            print("Record created successfully")
            return True
        except:
            print("Failed to insert user")
            return False

    def ret_user_by_email_and_pswrd(self, email, pswrd):
        try:
            conn = sqlite3.connect('Users.db')
            print("Opened database successfully") # check if worked
            strsql = f"SELECT * from {self.__tablename} where {self.__email} = '{str(email)}' AND {self.__password} = '{str(pswrd)}'"
            print(strsql)
            cursor = conn.execute(strsql)
            print(cursor)
            row = cursor.fetchone()
            user_data = str([row[1], row[2], row[3], row[4], row[5], row[6]])
            print("User data: " + str(user_data))
            conn.commit()
            conn.close()
            return row[2]
        except:
            print("Failed to find user")
            return False

    def update_user(self, recv_userid, new_email, new_username, new_password):
        try:
            conn = sqlite3.connect('Users.db')
            print("Opened database successfully")  # check if worked
            str_update = f"update {self.__tablename} set {self.__email} = '{new_email}', {self.__username} = " \
                         f"'{new_username}', {self.__password} = '{new_password}' where {self.__user_id} = {recv_userid}"
            print(str_update)
            conn.execute(str_update)
            conn.commit()
            conn.close()
            print("The users info was successfully updated")
            return "Success"
        except:
            return "Failed to update user"

    def delete_user_by_id(self, id):  # ADMINISTRATOR ONLY
        try:
            conn = sqlite3.connect('Users.db')
            print("Opened database successfully")  # check if worked
            str_delete = f"DELETE from {self.__tablename} where {self.__user_id} = {str(id)}"
            print(str_delete)
            conn.execute(str_delete)
            conn.commit()
            conn.close()
            print("Record deleted successfully")
            return "Success"
        except:
            return "Failed to delete user"

    def get_all_users(self):
        try:
            conn = sqlite3.connect('Users.db')
            print("Opened database successfully")  # check if worked
            str1 = "select*from " + self.__tablename
            print(str1)
            cursor = conn.execute(str1)
            rows = cursor.fetchall()
            arr_users = []
            for row in rows:
                str_rows = str(row[0]) + " " + row[1] + " " + row[2] + " " + row[3] + " " + row[4] \
                           + " " + str(row[5]) + " " + str(row[6])
                arr_users.append(str_rows)
            print(arr_users)
            return arr_users
        except:
            return False

    def get_all_wins(self, email):
        try:
            conn = sqlite3.connect('Users.db')
            print("Opened database successfully")  # check if worked
            str1 = f"select*from {self.__tablename} where {self.__email} = '{email}'"
            print(str1)
            cursor = conn.execute(str1)
            print(cursor)
            row = cursor.fetchone()
            user_wins = str(row[6])
            print("User wins: " + user_wins)
            conn.commit()
            conn.close()
            return "User wins: " + user_wins
        except:
            return False

    def get_table_name(self):
        return "The name of the table is " + self.__tablename


u = Users()
u.insert_user('Johnny@gmail.com', "Johnny", "Av", "JohnnyAV", "pass123")
u.insert_user('Ron@gmail.com', "Ron", "Ha", "Ron9", "1212")
u.insert_user('Dori@gmail.com', "Dori", "Do", "Doriking", "1234")
u.insert_user('Michal@gmail.com', "Michal", "kl", "Micha8l", "M12")
# u.get_all_users()
# u.get_all_wins("Johnny@gmail.com")
# u.ret_user_by_email_and_pswrd('Ron@gmail.com', "1212")
# u.update_user(3, "NewDori@gmail.com", "NewDoriking", "12345")
# u.delete_user_by_id(4)
# u.get_all_users()
