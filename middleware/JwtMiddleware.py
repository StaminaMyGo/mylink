from http.client import HTTPException
import jwt

from config import JWT_SECRET, JWT_ALGORITHM, LOGGING_EXCLUDES, LOGGING_EXCLUDES
from controller.ResponseModel import ResponseModel
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse


class JwtMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        for url in LOGGING_EXCLUDES:
            if request.url.path.startswith(url):
                return await call_next(request)
        token = request.headers.get("Authorization")
        if token is None:
            # return ResponseModel(4001, "请登陆", None)
            # raise HTTPException("缺少登陆凭证，请先登陆:")
            return JSONResponse(content={"code":4001,"msg":"缺少登陆凭证，请先登陆","data":None})
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
            request.state.user = payload["user"]
        except jwt.PyJWTError:
            # return ResponseModel(4001, "凭证无效，请重新登陆", None)
            # raise HTTPException("凭证无效，请重新登陆")
            return JSONResponse(content={"code": 4001, "msg": "凭证无效，请重新登陆", "data": None})
        return await call_next(request)
