import sqlite3
import hashlib
# def update - one for every category or a general one; update wins - need to add


class Users:
    def __init__(self, tablename="Users", user_id="ID", email="email", username="username", password="password",
                 wins="wins"):
        self.__tablename = tablename
        self.__user_id = user_id
        self.__email = email
        self.__username = username
        self.__password = password
        self.__wins = wins

        conn = sqlite3.connect('Users.db')
        print("Opened database successfully")
        str1 = "CREATE TABLE IF NOT EXISTS " + self.__tablename + "(" + self.__user_id + " " + "INTEGER PRIMARY KEY AUTOINCREMENT ,"
        str1 += " " + self.__email + " TEXT    NOT NULL ,"
        str1 += " " + self.__username + " TEXT    NOT NULL ,"
        str1 += " " + self.__password + " TEXT    NOT NULL ,"
        str1 += " " + self.__wins + " INTEGER    NOT NULL)"
        conn.execute(str1)
        print("Table created successfully")
        conn.commit()
        conn.close()

    def insert_user(self, email, username, password):
        try:
            exist_status = self.is_exist(email, username)
            if exist_status == "Email exists":
                print("Email already exists")
                return "Email exists"
            elif exist_status == "Username exists":
                print("Username already taken")
                return "Username taken"

            conn = sqlite3.connect('Users.db')
            print("Opened database successfully")  # check if worked
            salt = 'AnyaWakuWakuSecret'  # secret key
            salt_pswrd = hashlib.md5(salt.encode('utf-8') + password.encode('utf-8')).hexdigest()
            print(salt_pswrd)
            str_insert = f"INSERT INTO {self.__tablename} ({self.__email}, {self.__password}, {self.__username}, {self.__wins}) VALUES (?, ?, ?, ?)"
            params = (email, salt_pswrd, username, 0)
            conn.execute(str_insert, params)
            conn.commit()
            conn.close()
            print("Record created successfully")
            return True
        except:
            print("Failed to insert user")
            return False

    def is_exist(self, email, username):
        try:
            conn = sqlite3.connect('Users.db')
            print("Opened database successfully")  # check if worked
            strsql = f"SELECT * FROM {self.__tablename} WHERE {self.__email} = ? OR {self.__username} = ?"
            params = (str(email), str(username))
            cursor = conn.execute(strsql, params)
            row = cursor.fetchone()
            conn.close()
            if row:
                if row[1] == email:
                    return "Email exists"
                elif row[4] == username:
                    return "Username taken"
            return False
        except:
            print("Failed to check user existence")
            return False

    def ret_user_by_email_and_pswrd(self, email, password):
        try:
            conn = sqlite3.connect('Users.db')
            print("Opened database successfully")  # check if worked
            salt = 'AnyaWakuWakuSecret'  # secret key
            salt_pswrd = hashlib.md5(salt.encode('utf-8') + password.encode('utf-8')).hexdigest()
            strsql = f"SELECT * from {self.__tablename} where {self.__email} = ? AND {self.__password} = ?"
            params = (str(email), str(salt_pswrd))
            cursor = conn.execute(strsql, params)
            row = cursor.fetchone()
            user_data = str([row[1], row[2], row[3]])
            print("User data: " + str(user_data))
            conn.commit()
            conn.close()
            return row[2]
        except:
            print("Failed to find user")
            return False

    def update_user(self, recv_userid, new_email=None, new_username=None, new_password=None):
        try:
            conn = sqlite3.connect('Users.db')
            print("Opened database successfully")  # check if worked

            if new_email is None:
                new_email = self.__email
            if new_username is None:
                new_username = self.__username
            if new_password is None:
                new_password = self.__password

            str_update = f"UPDATE {self.__tablename} SET {self.__email} = '{new_email}', {self.__username} = '{new_username}', {self.__password} = '{new_password}' WHERE {self.__user_id} = {recv_userid}"
            print(str_update)
            conn.execute(str_update)
            conn.commit()
            conn.close()
            print("The user's info was successfully updated")
            return "Success"
        except:
            return "Failed to update user"

    def delete_user_by_id(self, id):  # ADMINISTRATOR ONLY
        try:
            conn = sqlite3.connect('Users.db')
            print("Opened database successfully")  # check if worked
            str_delete = f"DELETE FROM {self.__tablename} WHERE {self.__user_id} = {str(id)}"
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
            str1 = "SELECT * FROM " + self.__tablename
            print(str1)
            cursor = conn.execute(str1)
            rows = cursor.fetchall()
            arr_users = []
            for row in rows:
                str_rows = str(row[0]) + " " + row[1] + " " + row[2] + " " + str(row[3]) + " " + str(row[4])
                arr_users.append(str_rows)
            print(arr_users)
            return arr_users
        except:
            return False

    def get_all_wins(self, username):
        try:
            conn = sqlite3.connect('Users.db')
            print("Opened database successfully")  # check if worked
            str1 = f"select*from {self.__tablename} where {self.__username} = '{username}'"
            print(str1)
            cursor = conn.execute(str1)
            print(cursor)
            row = cursor.fetchone()
            user_wins = str(row[4])
            print("User wins: " + user_wins)
            conn.commit()
            conn.close()
            return user_wins
        except:
            return False

    def get_table_name(self):
        return "The name of the table is " + self.__tablename

    def update_wins(self, username):
        try:
            conn = sqlite3.connect('Users.db')
            print("Opened database successfully")  # check if worked
            cur_wins = self.get_all_wins(username)
            new_wins = int(cur_wins) + 1
            print(new_wins)
            str_update = f"update {self.__tablename} set {self.__wins} = '{new_wins}' where " \
                         f"{self.__username} = '{username}'"
            print(str_update)
            conn.execute(str_update)
            conn.commit()
            conn.close()
            print("The user's wins was successfully updated")
            return "Success update wins"
        except:
            return "Failed to update user's wins"

# u = Users()
# u.insert_user('Johnny@gmail.com', "Johnny", "Av", "JohnnyAV", "pass123")
# u.insert_user('Ron@gmail.com', "Ron", "Ha", "Ron9", "1212")
# u.insert_user('Dori@gmail.com', "Dori", "Do", "Doriking", "1234")
# u.insert_user('Michal@gmail.com', "Michal", "kl", "Micha8l", "M12")
# u.get_all_users()
# u.get_all_wins("Johnny@gmail.com")
# u.ret_user_by_email_and_pswrd('Ron@gmail.com', "1212")
# u.update_user(3, "NewDori@gmail.com", "NewDoriking", "12345")
# u.delete_user_by_id(4)
# u.get_all_users()
# u.update_wins("RoHakim9")
