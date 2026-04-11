from database.Db import Db
# 用户DAO
class UserDAO(Db):
    @classmethod
    def find_user(cls, username: str):
        conn=None
        cursor=None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
            user = cursor.fetchone()
        finally:
            if cursor:
               cursor.close()
            if conn:
               conn.close()
        return user

    @classmethod
    def create_user(cls, username: str, password: str):
        conn=None
        try:
            conn = cls.get_connection()
            with  conn.cursor() as cursor:
                cursor.execute("INSERT INTO users (user_name, user_pwd) VALUES (%s, %s)",(username, password))
            conn.commit()
            user_id = cursor.lastrowid
        finally:
            if conn:
               conn.close()
        return user_id



