from fastapi import APIRouter, Depends, Query, Form, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from offline_license.schemas import ReadOfflineLicenses, PageInfo, ReadOfflineLicensePage
import database
from models.offline_license_model import OfflineLicense
from offline_license import curd
import main_settings
import os
import uuid
import re
from database import SessionLocal


app_off = APIRouter()

# 根据版本模糊搜索
@app_off.get("/get_offline_license", response_model=ReadOfflineLicenses, description='模糊搜索')
async def get_offline_license(db: SessionLocal = Depends(database.get_db),
                        offline_version: str = Query(..., description='版本号')):

    offline_licenses = curd.get_offline_licenses(db, offline_version)
    return {"data": offline_licenses}

# 上传offline_license数据
@app_off.post("/uploadfile", description="上传离线授权信息")
async def upload_file(db: SessionLocal= Depends(database.get_db),
                      file: UploadFile = File(..., description='公钥文件'),
                      offline_version: str = Form(..., description='版本'),
                      comment: str = Form(..., description='备注信息')
                      ):
    content = await file.read()
    try:
        content_type = re.match(".*(\.\S+)", file.filename).group(1)
    except Exception:
        raise HTTPException(status_code=403, detail="Unknown file format")
    file_name = uuid.uuid1()
    file_full_name = str(file_name) + content_type
    file_path = main_settings.OFFLINE_PUBKEY
    with open(f'{file_path}{file_full_name}', 'wb') as file2:
        file2.write(content)
    offline_license = OfflineLicense(offline_version=offline_version, path=file_full_name, comment=comment)
    curd.insert_offline_license(db, offline_license)
    return {"detail": "success"}

# 删除offline_license信息
@app_off.get("/delete_offline_license", description='删除数据')
async def delete_offline_license(db: SessionLocal=Depends(database.get_db), id: int = Query(..., description='ID')):
    curd.delete_offline_license(db, id)
    return {"detail": "success"}

# 分页查询
@app_off.post("/query_offline_licenses", response_model=ReadOfflineLicensePage, description='分页查询')
async def query_offline_licenses(page_info: PageInfo, db: SessionLocal=Depends(database.get_db)):
    data = curd.query_offline_licenses(db=db, page=page_info.page, page_num=page_info.page_num)
    return data


# 查看文件
@app_off.get("/downloadfile", description="查看公钥文件")
async def download_file(path: str=Query(..., description="公钥文件路径名")):
    file_path = main_settings.OFFLINE_PUBKEY
    file_full_path = os.path.join(file_path, path)
    return FileResponse(file_full_path)

