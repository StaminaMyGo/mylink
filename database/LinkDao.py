import math

from database.Db import Db

class LinkDAO(Db):
    @classmethod
    def get_links(cls, user_id: int, search: str = None, page: int = 1, page_size: int = 10):
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM links WHERE lk_user_id = %s"
        query2 ="SELECT count(1) as total FROM links WHERE lk_user_id = %s "
        params = [user_id]

        if search:
            query += " AND lk_name LIKE %s"
            query2 += " AND lk_name LIKE %s"
            params.append(f"%{search}%")

        cursor.execute(query2,params)
        rowcount = cursor.fetchone()["total"]

        query += " ORDER BY lk_id DESC LIMIT %s , %s"
        params.extend([(page - 1) * page_size,page_size ])

        cursor.execute(query, params)
        links = cursor.fetchall()
        cursor.close()
        conn.close()
        pageCount=math.ceil(rowcount/page_size)
        return {"data":links,"rowCount":rowcount,"pageCount":pageCount}

    @classmethod
    def select_link_id(cls, id: int):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute("select * from links  where lk_id=%s ", (id,))
        link = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return link

    @classmethod
    def create_link(cls, name: str, phone: str, user_id: int, img_url: str = None):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO links (lk_name, lk_phone, lk_user_id, lk_img) VALUES (%s, %s, %s, %s)",
            (name, phone, user_id, img_url)
        )
        conn.commit()
        link_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return link_id

    @classmethod
    def update_link(cls, id:int,name: str, phone: str, user_id: int, img_url: str = None):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "update links set lk_name=%s, lk_phone=%s, lk_user_id=%s, lk_img=%s where lk_id=%s ",
            (name, phone, user_id, img_url,id)
        )
        rowcount=cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return rowcount



    @classmethod
    def delete_link(cls, id: int):
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "delete from  links  where lk_id=%s ",
            (id,)
        )
        rowcount=cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return rowcount


