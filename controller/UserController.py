from datetime import datetime

from fastapi import APIRouter
import config
from database.UserDao import UserDAO
from controller.ResponseModel import ResponseModel
import datetime
import jwt
from fastapi import Body
router=APIRouter(prefix="/users",tags=["users"])
@router.post("/login")
async def login(username: str=Body(...), password: str=Body(...)):
    row = UserDAO.find_user(username)
    if not row or row["user_pwd"] != password:
        return ResponseModel(code=4001, msg="用户名或密码不符",data=None)

    payload = {
        # "user_id": row["user_id"],
        # "user_name": row["user_name"],
        # "user_img":row["user_img"],
        "user":row,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=30)  # 过期时间
    }

    token = jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    return ResponseModel(code=2000, msg="success", data={"jwttoken":token,"user":row})


@router.post("/register")
async def register(username: str, password: str):
    if UserDAO.find_user(username):
        return ResponseModel(code=4002, msg="Username exists")

    user_id = UserDAO.create_user(username, password)
    return ResponseModel(code=2000, msg="success")
