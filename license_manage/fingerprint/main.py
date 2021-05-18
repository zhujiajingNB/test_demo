from fastapi import APIRouter, Depends, Query, Form, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
import os
import uuid
import re
import database
from database import SessionLocal
from .schemas import ReadFingerPrints, ReadFingerPrintPage, PageInfo
from fingerprint import curd
import main_settings
from models.fingerprint_model import FingerPrint


app_fin = APIRouter()



# 搜索接口
@app_fin.get("/getfingers", response_model=ReadFingerPrints, description='客户名模糊查询')
async def get_finger(db: SessionLocal = Depends(database.get_db), customer_name: str = Query(...,description="客户名")):
    list = curd.get_fingerprints(db, customer_name)
    return {"data":list}

# 文件上传
@app_fin.post("/uploadfile", description='上传指纹文件')
async def upload_file(db: SessionLocal = Depends(database.get_db), file: UploadFile = File(...,description='指纹文件'),
                      customer_name: str = Form(..., description='客户名'), comment: str = Form(..., description='备注')):
    content = await file.read()
    try:
        content_type = re.match(".*(\.\S+)", file.filename).group(1)
    except Exception:
        raise HTTPException(status_code=403, detail="Unknown file format")
    file_name = uuid.uuid1()
    file_full_name = str(file_name) + content_type
    file_path = main_settings.FINGPRINT_FILE
    with open(f'{file_path}{file_full_name}','wb') as file2:
        file2.write(content)
    fingerprint = FingerPrint(customer_name=customer_name,comment=comment,path=file_full_name)
    curd.inset_fingerprints(db=db, fingerprint=fingerprint)
    return {"detail": "success"}

# 指纹文件下载接口
@app_fin.get("/downloadfile", description="下载指纹文件")
async def download_file(fingerprint_filename: str = Query(..., description="指纹路径")):
    file_path = main_settings.FINGPRINT_FILE
    file_full_path = os.path.join(file_path, fingerprint_filename)
    return FileResponse(file_full_path)

# 指纹文件删除接口
@app_fin.get("/delete", description="删除指纹数据")
async def delete_fingerprint(db: SessionLocal = Depends(database.get_db), id: int = Query(...,description='指纹id')):
    curd.delete_fingerprint(db, id)
    return {"detail": "success"}

# 分页查询
@app_fin.post("query_fingerprints", response_model=ReadFingerPrintPage, description="分页查询指纹数据")
async def query_by_page(pageInfo: PageInfo, db: SessionLocal = Depends(database.get_db)):
    data = curd.query_finerpint(db, pageInfo.page, pageInfo.page_num)
    return data