# 数据库配置
from uvicorn.config import LOGGING_CONFIG

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "PhoneBook"
}

# OSS配置（需替换为你的实际信息）
OSS_CONFIG = {
    "endpoint": "your_oss_endpoint",
    "access_key_id": "your_access_key_id",
    "access_key_secret": "your_access_key_secret",
    "bucket_name": "your_bucket_name"
}

LOGGING_EXCLUDES=[
        "/api/v1/users/login",
        "/api/v1/users/reg",
        "/docs",
        "/redoc",
        "/openapi.json"
]

# JWT配置
JWT_SECRET = "123456"
JWT_ALGORITHM = "HS256"
