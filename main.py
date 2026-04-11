from http.client import HTTPException
from traceback import print_exception

from fastapi import FastAPI,Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse

from controller.LinkController import router as linkRouter
from controller.UserController import router as userRouter
from controller.OSSController import router as ossRouter
from middleware.JwtMiddleware import JwtMiddleware

app = FastAPI()

# 定义中间件函数的快捷方式使用@app.middleware("http")注解注册
@app.middleware("http")
async def exception_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException as http_exc:
        # 捕获HTTPException，返回包含错误详细信息的JSON响应
        print_exception(http_exc)
        return JSONResponse(content={"code":5000,"msg":"服务器端错误","data":None})

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
#配置jwt中间件(jwtMiddleware定义在其他文件)，用这种方式来注册
app.add_middleware(JwtMiddleware)


app.include_router(linkRouter,prefix="/api/v1")
app.include_router(userRouter,prefix="/api/v1")
app.include_router(ossRouter,prefix="/api/v1")


if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)