from database.Db import Db

try:
    conn = Db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")  # 查询MySQL版本
    version = cursor.fetchone()
    print("MySQL版本:", version)
    cursor.close()
    conn.close()
    print("数据库连接正常")
except Exception as e:
    print("连接失败:", e)