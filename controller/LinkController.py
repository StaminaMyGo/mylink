from fastapi import APIRouter, Request, Body, Form
from pydantic import BaseModel

from  controller.ResponseModel import ResponseModel
from database.LinkDao import LinkDAO
import pprint

router=APIRouter(prefix="/links",tags=["links"])

#接收json参数，散装字段要声明Body()
@router.post("/")
async def create_link(request: Request,name: str=Body(),phone: str=Body(),img: str = Body(default=None)):
    user = request.state.user
    # pprint.pprint(vars(user))
    link_id = LinkDAO.create_link(name, phone, user["user_id"], img)
    return ResponseModel(2000, "success", {"link_id": link_id,"link_name":name,"link_phone":phone,"link_img":img})

#get传参？形式
@router.get("/page")
async def get_links(request: Request,search: str = None,page_index: int = 1,page_size: int = 10):
    user = request.state.user
    pp = LinkDAO.get_links(user["user_id"], search, page_index, page_size)
    return ResponseModel(2000, "success", pp)

#路径传参{id}
@router.delete("/{id}")
async def delete_link(id :int,request: Request):
    user = request.state.user
    link_id = LinkDAO.delete_link(id)
    return ResponseModel(code=2000, msg="success", data=None)

# json传参也可以传入字典来接收
@router.put("/{id}")
async def update_link2(request: Request,id:int, jsonData:dict):
    user = request.state.user
    link_id = LinkDAO.update_link(jsonData["id"],jsonData["name"],jsonData["phone"],user["user_id"],jsonData["img"])
    return ResponseModel(code=2000, msg="success", data=None)


# json传参也可以在request.json()获取json参数，它也是返回字典
# @router.put("/{id}")
# async def update_link3(request: Request):
#     user = request.state.user
#     jsonData=await request.json();
#     link_id = LinkDAO.update_link(jsonData["id"],jsonData["name"],jsonData["phone"],user["user_id"],jsonData["img"])
#     return ResponseModel(code=2000, msg="success", data=None);

#json传参最合理的方式,先定义一个类，它可以增加验证规则和说明，也可以不用增加
#没有验证规则
# class Link(BaseModel):
#     id: int
#     name: str
#     phone: str
#     img: str
# 改造成增加验证规则的写法，会自动验证
# class Link(BaseModel):
#     id: int = Field(..., title="Link ID", description="The unique identifier for a link")
#     name: str = Field(..., min_length=1, max_length=100, title="Link Name", description="The name of the link")
#     phone: str = Field(..., regex=r'^\+?\d{10,15}$', title="Phone Number", description="A valid phone number")
#     img: HttpUrl = Field(..., title="Image URL", description="A URL to an image")
#
# router.put("/{id}")
# async def update_link3(request: Request,id:int, lk:Link):
#     user = request.state.user
#     link_id = LinkDAO.update_link(lk.id,lk.name,lk.phone,user["user_id"],lk.img)
#     return ResponseModel(code=2000, msg="success", data=None)


# 表单传值要用Form(),不能用Body(),不写也不行 【表单传参是指在请求头中带参数 id=1&name=zhangsan&phone=12345】
# async def update_link4(request: Request,id:int,name:str=Form(),phone:str=Form(),img:str=Form(default=None)):
#     user = request.state.user
#     print(id)
#     link_id = LinkDAO.update_link(id,name,phone,user["user_id"],img)
#     return ResponseModel(code=2000, msg="success", data=None);




