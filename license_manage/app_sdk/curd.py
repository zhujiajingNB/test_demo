from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from models.app_sdk_model import AppSdk
from utils import pages

# 添加sdk信息
def insert_app_sdk(db: Session, app_sdk: AppSdk):
    db.add(app_sdk)
    db.commit()
    db.refresh(app_sdk)

# 模糊查询
# @param
def get_app_sdk(db: Session, sdk_version: str):
    return db.query(AppSdk).filter(and_(AppSdk.sdk_version.like(f'%{sdk_version}%'), AppSdk.is_delete==False))\
        .order_by(AppSdk.id.desc()).all()

# 删除文件
def delete_app_sdk(db: Session, id:int):
    app_sdk = db.query(AppSdk).filter(AppSdk.id==id).first()
    app_sdk.is_delete = True
    db.commit()
    db.refresh(app_sdk)

# 分页查询
def query_finerpint(db: Session, page: int , page_num: int):
    count = db.query(func.count(AppSdk.id)).scalar()
    total_page = pages.get_pages(count, page_num)
    app_sdks = db.query(AppSdk).filter(AppSdk.is_delete == False).order_by(AppSdk.id.desc())\
        .limit(page_num).offset((page-1)*page_num).all()
    return {"data": app_sdks, "total_page": total_page}