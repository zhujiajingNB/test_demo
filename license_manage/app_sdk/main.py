from fastapi import APIRouter, Depends, Query, Form, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from models.app_sdk_model import AppSdk
import os
from .schemas import ReadAppSdks, ReadAppSdkPage
import main_settings
import uuid
import re
import database
from database import SessionLocal
from app_sdk import curd
app_sd = APIRouter()

# 上传appsdk数据
@app_sd.post("/uploadfile", description='上传数据接口')
async def upload_file(db: SessionLocal=Depends(database.get_db),
                file: UploadFile = File(..., description='app_sdk公钥'),
                sdk_name: str = Form(default=None, description='sdk名称'),
                sdk_version: str = Form(..., description='sdk版本'),
                comment: str = Form(..., description='备注')
                ):
    content = await file.read()
    try:
        content_type = re.match(".*(\.\S+)", file.filename).group(1)
    except Exception:
        raise HTTPException(status_code=403, detail="Unknown file format")
    file_name = uuid.uuid1()
    file_full_name = str(file_name) + content_type
    file_path = main_settings.APP_SDK_PUBKEY
    with open(f'{file_path}{file_full_name}', 'wb') as file2:
        file2.write(content)
    app_sdk = AppSdk(sdk_name=sdk_name, path=file_full_name, sdk_version=sdk_version, comment=comment)
    curd.insert_app_sdk(db, app_sdk)
    return {"detail": "success"}

# 根据app_sdk_vresion 查询
@app_sd.get("/get_appsdks", description='搜索框接口', response_model=ReadAppSdks)
async def get_app_sdk(db: SessionLocal=Depends(database.get_db),
                      sdk_version: str = Query(..., description='sdk版本')
                      ):
    app_sdks =  curd.get_app_sdk(db, sdk_version)
    return {'data': app_sdks}

# 根据id删除数据
@app_sd.get("/delete_app_sdk", description='删除接口')
async def delete(db: SessionLocal=Depends(database.get_db), id: int = Query(..., description='ID')):
    curd.delete_app_sdk(db, id)


# 查看文件
@app_sd.get('/downloadfile', description='查看公钥文件')
async def download_file(path: str = Query(..., description='公钥文件路径')):
    file_path = main_settings.APP_SDK_PUBKEY
    file_full_path = os.path.join(file_path, path)
    return FileResponse(file_full_path)

# 分页查询
@app_sd.post("/query/app_sdks", description='分页查询数据', response_model=ReadAppSdkPage)
async def query_app_sdks(db: SessionLocal=Depends(database.get_db), page: int=1, page_num: int=10):
    data = curd.query_finerpint(db=db, page=page, page_num=page_num)
    return data






