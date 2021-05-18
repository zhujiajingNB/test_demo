from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from models.fingerprint_model import FingerPrint
from utils import pages

# 根据用户名查询
def get_fingerprints(db: Session, customer_name: str):
    return db.query(FingerPrint).filter(and_(
        FingerPrint.customer_name.like(f'%{customer_name}%'),
        FingerPrint.is_delete == False
    )).all()

# 插入指纹数据
def inset_fingerprints(db: Session, fingerprint: FingerPrint):
    db.add(fingerprint)
    db.commit()
    db.refresh(fingerprint)

# 删除指纹数据
def delete_fingerprint(db: Session, id: int):
    fingerprint = db.query(FingerPrint).filter(FingerPrint.id == id).first()
    fingerprint.is_delete = True
    db.commit()
    db.refresh(fingerprint)


# 分页查询指纹数据
def query_finerpint(db: Session, page: int , page_num: int):
    count = db.query(func.count(FingerPrint.id)).scalar()
    total_page = pages.get_pages(count, page_num)
    fingerprints = db.query(FingerPrint).filter(FingerPrint.is_delete == False).order_by(FingerPrint.id.desc())\
        .limit(page_num).offset((page-1)*page_num).all()
    return {"data": fingerprints, "total_page": total_page}




