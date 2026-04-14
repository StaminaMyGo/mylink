from datetime import datetime

# import jsonable_encoder
from fastapi.encoders import jsonable_encoder   # ✅ 正确
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

    # 将可能包含 datetime 的 row 转为安全字典，例如 {'created_at': '2026-04-11T10:00:00'}
    safe_row = jsonable_encoder(row)

    payload = {
        # "user_id": row["user_id"],
        # "user_name": row["user_name"],
        # "user_img":row["user_img"],
        "user":safe_row,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=30)  # 过期时间
    }

    token = jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    return ResponseModel(code=2000, msg="success", data={"jwttoken":token,"user":safe_row})


@router.post("/register")
async def register(username: str, password: str):
    if UserDAO.find_user(username):
        return ResponseModel(code=4002, msg="Username exists")

    user_id = UserDAO.create_user(username, password)
    return ResponseModel(code=2000, msg="success")
