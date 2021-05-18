from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from models.offline_license_model import OfflineLicense
from utils import pages

# 根据offline 版本来搜索
def get_offline_licenses(db: Session, offline_version: str):
    return db.query(OfflineLicense).filter(and_(OfflineLicense.offline_version.like(f"%{offline_version}%"),
                                         OfflineLicense.is_delete == False
                                         )).order_by(OfflineLicense.id.desc()).all()

# 添加 offfline_license 数据
def insert_offline_license(db: Session, offline_license: OfflineLicense):
    db.add(offline_license)
    db.commit()
    db.refresh(offline_license)


# 删除 offline_license 数据
def delete_offline_license(db: Session, id: int):
    offline_license = db.query(OfflineLicense).filter(OfflineLicense.id == id).first()
    offline_license.is_delete = True
    db.commit()
    db.refresh(offline_license)


# 分页查询
def query_offline_licenses(db: Session, page: int, page_num: int):
    count = db.query(func.count(OfflineLicense.id)).scalar()
    total_page = pages.get_pages(count, page_num)
    offline_licenses = db.query(OfflineLicense).filter(OfflineLicense.is_delete == False).order_by(OfflineLicense.id.desc())\
        .limit(page_num).offset((page-1)*page_num).all()
    return {"data": offline_licenses, "total_page": total_page}

