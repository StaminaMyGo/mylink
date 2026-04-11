
import mysql.connector
from dbutils.pooled_db import PooledDB

from config import DB_CONFIG
# DAO层基类
class Db:
    pool = PooledDB(mysql.connector, **DB_CONFIG, pool_size=5, maxconnections=10, charset='utf8mb4')

    @classmethod
    def get_connection(cls):
        return cls.pool.connection()