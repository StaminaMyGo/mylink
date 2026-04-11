from cgi import print_exception
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse


class ErrMiddleware(BaseHTTPMiddleware):
    async def exception_handling_middleware(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exc:
            # 捕获HTTPException，返回包含错误详细信息的JSON响应
            print_exception(http_exc)
            return JSONResponse(content={"code": 5000, "msg": "服务器端错误" + http_exc, "data": None})
  