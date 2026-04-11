from fastapi import APIRouter, UploadFile

import oss2
from config import OSS_CONFIG
from controller.ResponseModel import ResponseModel

# 配置 OSS 客户端
# access_key_id = config.OSS_CONFIG.access_key_id
# access_key_secret = config.OSS_CONFIG.access_key_secret
# endpoint = config.OSS_CONFIG.endpoint  # 例如: oss-cn-hangzhou.aliyuncs.com
# bucket_name = config.OSS_CONFIG.bucket_name
#
# auth = oss2.Auth(access_key_id, access_key_secret)
# bucket = oss2.Bucket(auth, endpoint, bucket_name)

router =APIRouter(prefix="/oss",tags=["oss"])



@router.post("/upload")
async def upload_file(photo: UploadFile) -> str:
    auth = oss2.Auth(OSS_CONFIG["access_key_id"], OSS_CONFIG["access_key_secret"])
    bucket = oss2.Bucket(auth, OSS_CONFIG["endpoint"], OSS_CONFIG["bucket_name"])
    object_name = f"{photo.filename}"
    bucket.put_object(object_name, photo.file)
    return ResponseModel(code=2000,msg="SUCCESS"
                         ,data=f"https://{OSS_CONFIG['bucket_name']}.{OSS_CONFIG['endpoint']}/{object_name}")

@router.delete("/delete/{object_name}")
async def delete_file(object_name: str):
    auth = oss2.Auth(OSS_CONFIG["access_key_id"], OSS_CONFIG["access_key_secret"])
    bucket = oss2.Bucket(auth, OSS_CONFIG["endpoint"], OSS_CONFIG["bucket_name"])
    # 删除 OSS 中的文件
    bucket.delete_object(object_name)
    return ResponseModel(code=2000, msg=f"文件 {object_name} 删除成功",data=None)

